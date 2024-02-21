![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the Jan 23, 2024 video call of WebAssembly's Threads Subgroup

- **Where**: zoom.us
- **When**: Jan 23, 2024, 5pm-6pm UTC (Jan 23, 2024, 9am-10am Pacific Time)
- **Location**: *link on calendar invite*

### Registration

None required if you've attended before. Fill out the form here to sign up if
it's your first time: https://forms.gle/mUp4nmiVUTNQDKcD9. The meeting is open
to CG members only.

## Logistics

The meeting will be on a zoom.us video conference.
Installation is required, see the calendar invite.

## Agenda items

1. Opening, welcome and roll call
    1. Opening of the meeting
    1. Introduction of attendees
1. Find volunteers for note taking (acting chair to volunteer)
1. Adoption of the agenda
1. Proposals and discussions
    1. Continue walkthrough of proposal overview
1. Closure

## Meeting Notes

### Introduction of attendees

- Thomas Lively
- Dan Gohman
- Daniel Hillerström
- Conrad Watt
- Sulekha Kulkarni
- Manos Koukoutos
- Francis McCabe
- Luke Wagner
- Andrew Brown
- Nick Fitgerald
- Zalim Bashorov
- Shu-yu Guo
- Ilya Rezvov
- Ashley Nelson
- Alon Zakai
- Emanuel Ziegler
- Jakob Kummerow
- Paolo Severini
- Yosh Wuyts

### Proposal Walkthrough

TL: changes from last meeting are in https://github.com/WebAssembly/shared-everything-threads/pull/28.

TL: presenting https://github.com/WebAssembly/shared-everything-threads/blob/main/proposals/shared-everything-threads/Overview.md

#### Thread management

TL: Discussion about thread management primitives in the component model is happening at: https://github.com/WebAssembly/component-model/pull/291

#### Managed waiter queues

CW: Are we considering the version where we consider an eqref instead of i32?

TL: Yes, there are a few different versions we may want to have. You can imagine you have an i64 control field instead of an i32 field. SYG suggested this so you can have more data in your control word. Extrapolating from that, you can imagine having a version with a shared eqref, let you use references or linked lists. Imagine constructing a WasmGC shared queue structure where it stores references in that control word. I suspect we’ll need these at some point but to avoid having a ton of new types in the initial proposal, right now the normative text says we only add one with i32.

CW: Provocatively, what about just an eqref?

TL: True, if you just had eqref, the problem is if you have eqref, you can store an i31 in there, but you can’t use any arithmetic that we may add for i31.

CW: Still can do the CAS loop trick we described and that's how you’ll have to do all i31 atomic operations anyway.

TL: Could start with that, the reason we started with i32 is its similar to a native lock implementation where you have a couple of bits that are useful and having i32 lets you do all the atomic arithmetic you want on those bits. Not sure how important that is. We can start and have toolchain developers tell us what they need, add more in response to that.

CW: Sure, just thinking if there is one waitqueueref type things are easier; otherwise, types are messy

TL: If you have to pick one, the most general one is the eqref one? I’d be fine changing the text so specify the eqref one first. I suspect we’ll need multiple anyway.

SYG: Not mentioned here, but we need to hammer out the lifetime of the waitqueue; if we lose references to waiters in the queue if ? dies, what happens?

TL: Great idea. Do you have any idea what behavior would make the most sense?

SYG:  From a tool view, it should be kept alive if there are things blocking or in the wait queue itself, that should keep it alive. For a linear memory lock, you wouldn’t expect that your lock would disappear from underneath you.

CW: What happens with SharedArrayBuffer (SAB) today? We can wait on a SAB and then drop it, what happens?

SYG: I think it leaks. This doesn’t show up for blocked threads because it's likely that if your thread is blocked, it's already independently keeping a reference to the SAB. But you do see leaks today with wait-async. Fire some promises and for whatever reason the SAB leaks. For the application, it would be easier not to keep these things alive if there are things in the queue. And I think even in the implementation, this object dying waking up for everything in the queue means there needs to be a finalizer and that's not a cheap operation in every VM. Maybe something we want to avoid.

CW: my instinct is if someone creates a waitqueueref and then drops it, it is the programmers responsibility–you deserve whatever happens at that point

TL: If the thread is blocked, it's not semantically visible whether it gets GC’d or not.

CW: Need to be a little careful about a wait with a timeout–some nuance there

TL: Our  current wait instruction takes a timeout and if you want infinite, you put -1 there, highest possible timeout. CW is that infinite or maximal number of nanoseconds.

CW: infinite

TL: Then you could collect those because they would never wake up on their own.

CW: that’s what I would expect; generalize to other shared things, if the things waiting are dropped, can we drop the thing we’re waiting on?

TL: Why not, no way to observe it if you collect them, right?

CW: What guarantees do we want to give in the spec? This could come up in JS today, we’re making a big deal with waitqueueref but I could imagine constructing these examples with SAB and I don’t think engines are going out of their way to specify what happens in that scenario.

SYG: No guarantees I think. Wait-queue does not add any more expressivity. This just removes the memory address key indirection. I suspect not a lot of thought has not gone into this from the JSVM folks (myself included) because the use cases are pretty well behaved. Not doing novel things here. My bias is to let it be impl driven if the collection of impl in the room say it's hard to implement. 

CW: take our lead from SAB; spec doesn’t say. You could imagine an engine doing it or not–the JS doesn’t say anything, right?

SYG: Spec does say a thing I think because it has to say a thing about finalization registry liveness. If the finalization registry itself dies, the impl is free to not fire the finalizer based on impl feedback. If you work out what the JS spec says about SAB and indefinite? Blocks, technically you can collect it all. Because we spec observable liveness without a rigorous notion of observability because we didn’t know how to write it in a way to prohibit things we didn’t want to. Not a question of reachability. If there exists some possible execution where you can observe (handwavey) the identity (reference equality of something_ if such an execution exists, you say that thing is live. If no possible execution, you say the finalizer can be fired. If a block?? Is blocked indefinitely, it seems like you could collect it all.

CW: If the thread is blocked indefinitely and the engine can prove all the waiters have been dropped, then the roots can be GC-ed.

TL: Wasm core spec says nothing about GC or when things get GC at all. But if there is a finalization registry, we would want to say something in the JS spec for Wasm about when infinitely sleeping threads are allowed to be collected.

SYG: A non-normative note explaining what the JS spec already says.

TL: CW, you agree those notes would go in the JS spec instead of the core spec?

CW: 100% until Wasm gets finalizers.

SYG: eqref is what, the things that have identity?

TL: it’s a subtype of anyref, so only Wasm-internal references (structs, arrays, i31)

CW: it’s all the types you can do a compare-exchange on.

SYG: And the atomic operations are allowed, store, load, swap, compare and swap ..

CW: You need an eqref to do a compare and swap because those are the only types that have comparison defined. You can implement any arithmetic on this type by doing a CAS loop.

NF (via chat): seems like it would be an application error if the wait queue is non-empty but the only references to the wait queue are those waiting threads. That is a deadlock, no?

CW (via chat): only if the wait doesn't have a timeout. but you could wait forever without being notified even if the SAB is kept alive

NF (via chat): we could possibly detect this case and raise traps in the waiting threads

#### Memory model

TL: (presenting)

#### JS API

TL: (presenting)

CW: `nofunc` can also be converted to `shared nofunc`--is that true when we have an exception type?

TL: This isn’t saying that nofunc can be converted to `shared nofunc`, its saying that JS values that can be converted to references to `nofunc` can also be `shared nofunc`. The only JS value that allows this conversion is null. So basically saying null can be converted to `shared nofunc`

CW: Scared of that, but need to think more about it.

TL: This conversion might be a conversion, not a cast; representation can change at the boundary (e.g., JS null is different from reference to none).

CW: Imagine you have an exnref that is unshared, I believe that is a subtype of `nofunc`. No wait, `nofunc` is a func null. Oops I’m totally wrong. Nevermind.

TL: Explaining `nofunc` is the bottom for function references.

TL: (presenting at “JS strings”)

CW: Back to `nofunc`, imagine a case where the non-shared function null has a diff representation from the shared function null which would happen if they are in different heaps. Because of JS, you now need to test the boundary to change their representation of one. I remember JK being scared of that test because you need to add a little cost to every boundary crossing.

TL: For ToWebAssemblyValue(...) the JS-side thing is a JS null; no way to refer to Wasm null, it would get converted to JS null. In SM this has the same representation but V8 does not do this.

CW: Is it already the case that Wasm null is eagerly converted to a JS null representation?

TL: Yes.

CW: Definitely true everywhere? Guess it makes things simpler.

TL: Wasm GC JS spec says this–eager conversions (should double-check this)

CW: The point about any value that can be converted to nofunc etc, the only possible value is a JS null?

TL: I believe so, yes

JK (via chat): no check/conversion happens when the Wasm-side type is externref

TL: Is it because the externref null is the same as the JS null?

JK (via chat): Yes

TL: is null a sharable value in your JS proposal?

SYG: Yes; the shared/unshared distinction does not apply to primitives. Too crazy to split the world on primitives; easy on paper. There is an implementation challenge, but mostly around string. Null is read-only, never changes.

TL: We have several null values, you can imagine saying an externref null is convertible to a shared externref null, must have the same representation. Similar to nullref null and shared null ref.

SYG: Is the set of nulls innumerable?

TL: No, only three of them.

SYG: If there’s a small, finite number of them, what’s the challenge? Make them always shared.

TL: CW, do you know if it's possible in the type system to say that a shared null ref is equivalent to a non-shared null ref. There’s no way you can compare them?

CW: It’s strange: possible in principle but it would not allow you to write more interesting programs. A bit scary…

TL: How is ref.eq going to work? Are we going to have shared ref.eq? Extend the typing of ref.eq to take as either of its arguments, shared eq or non-shared eq, mix & match, and it's fine?

CW: May bother Andreas about principal types. Also, I broadly like the waitqueueref idea but we should show it to him–he will have informed opinions.

TL: Yes we should make him think deeply about it and tell us what he thinks, for sure.

TL: (presenting at shared constructors)

TL: Do I remember correctly SYG that you do not have a strong opinion here?

SYG: No strong opinion on Shared* vs re-using the same constructors. Awkwardness in how they behave very differently if we use the same constructor. If it’s just tools that use them, not too worried. Not much prior art here (e.g., SAB vs AB)

ZB (via chat): we have separate constructors from ArrayBuffers

FM (via chat): JSPI used the same constructor for WebAssembly.Function

CW: Francis made a good point in the chat with the precedent of JSAPI using the same Wasm constructor. 

TL: Those are currently described as an option bag–a mix-and match approach

CW: For SharedGlobal not interesting; SharedFunction has all the new `bind` functions…

TL: That one is also currently specified as an option bag on SharedFunction. I’m in favor of using simple constructors and doing this all with option bags. 

ZB (via chat): in case of using the same constructor, will instances have readonly property like `shared`?

CW: For resizable buffers, is there any way to observe this in JS today?

SYG: Yes, it says false for the existing ones and true for the new ones. I guess it says undefined on the existing ones before the new proposal implemented, which is false-y

CW: Maybe do the same thing for our objects?

SYG: Caveat, for the usual use case there is a read-only property like ZB asked, the difference is resizable buffers have one getter on the prototype that’s shared and this being JS and everything observable, you can tear the getter out and keep it around as a function and observe its reference equality. For the shared stuff, you will not have the same getter. .shared is fine, but storing a reference to the same function for whatever reason, they will be different functions. Not going to be completely analogous. 

CW: Is that because of cross-realm stuff?

SYG: Yes. It’s because of cross-realm stuff, but it’s because we can’t share JS functions, why we have TLS to begin with. If we could, you could imagine having just one shared accessor, but we don’t so we end up duplicating across every realm.

TL: Existing SharedMemory has a read-only shared property; can we do the same thing for all these objects? Is it a getter or a property?

SYG: It's implemented as a getter, no implementation would incur an extra word or constant thing that never changes.

TL: Tricky.

CW: My understanding is one of the things that makes SAB weird in this context, is it's an unshared wrapper on a shared buffer - their decisions about a “shared” bit may not work for us

TL: Important note; these shared things will be different than a Wasm shared memory; SAB is a wrapper under the “actually shared” buffer. Same with WebAssembly.Memory. These new objects would actually be shareable–could postMessage it around and have reference equality. This is important for scalability: many more shared globals, e.g., than shared memories.

#### Thread-local JS Function Wrappers

TL: (presenting)

CW: Throwing around `bind` instead of `set` because we have an idea that you can only bind once per thread, otherwise there would be errors. `Set` sounds like a global variable you can reset if you want to a different value.

TL: True, we do specify that it can only be set once. Maybe `bind` is better there? Name-clashes with existing `bind` function?

CW: Very good point, I’m sorry I forgot JS exists, maybe we need to bikeshed on the name a little bit.

TL: I think `WebAssembly.Function.bind` already does a thing.

CW: Another question about inlining–can it be done with a speculative guard? Something for engine implementers to think about.

TL: I know inlining JS into Wasm is already not possible in V8 so doing it in a thread-local way.

CW: Isn’t it done for certain special-case functions: sqrt? If it’s thread-local, can we get the same benefit.

SYG: One issue: we want not only the steady state to be fast, but also loading to be fast. Need to know the structure of the thread-locals before loading a new thread. Ping-pong communication–not what we want. Hunch is it’s not a problem for Wasm: it could load the same payload on all the threads. They know the TLS structure ahead of time…

CW: Wouldn’t be a serialization point, the toolchain when it gets created by the WebWorker would have this static list of things to initialize.

SYG: Good property to keep in mind; e.g., if class loading has a handshake, it affects load time.

CW: There is a serialization point with this design. The thread that creates these thread local functions initially, is responsible for sending them out to the web workers that are created subsequently. But you could do it easily with a shared table, put all the items there, then you don’t need to serialize as much

SYG: Any postMessage at thread load is a PITA; calls for an implicit communication channel on the JS side.

TL: We’re in that world today with Wasm because today with Wasm you have to post your entire module over when you start it up before you can call into Wasm. In this shared-everything world, you have to post your entry point but also probably your exports.

CW: That’s a win: postMessaging a single function instead of the module + instantiation. We are not getting away from one initial postMessage though.

