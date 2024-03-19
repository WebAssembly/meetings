![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the March 5, 2024 video call of WebAssembly's Threads Subgroup

- **Where**: zoom.us
- **When**: March 5, 2024, 5pm-6pm UTC (March 5, 2024, 9am-10am Pacific Time)
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
    1. Typing shared-suspendable and shared-fixed functions ([#44])
1. Closure

## Meeting Notes

### Introduction of attendees

- Thomas Lively
- Andrew Brown
- Nick Fitzgerald
- Manos Koukoutos
- Ryan Hunt
- Sulekha Kulkarni
- Conrad Watt
- Ilya Rezvov
- Zalim Bashorov
- Jakob Kummerow
- Ashley Nelson
- Alex Crichton
- Shu-yo Guo
- Luke Wagner

[#46]: https://github.com/WebAssembly/shared-everything-threads/issues/46
[#44]: https://github.com/WebAssembly/shared-everything-threads/issues/44

### Typing shared-suspendable and shared-fixed functions ([#44])

CW: feeling optimistic about [#46]; everyone seemed to agree on a variant of context-locals.

TL: Tied to context locals, right?

CW: Yes, main concern is it requires a more ambitious design for the function return type.

TL: Still has separate types for shared suspenable.

CW: With the latest variation we should avoid that.

TL: avoiding by only doing shared-suspendable?

CW: Yes, you can have just shared suspendable but you can have non-shared elements, accessed in the barrier block. Change the semantics of non-shared locals to avoid capturing? Currying?

RH: storing things on the VM context–we need an implementation limit. With many functions we may need boxing. Did this require the shared-barriers instruction?

CW: If you want to box them, you’ll need the more general barrier instruction which is fine. One motivation for the fused call instruction is I would expect inlining to be easier if you’re doing speculative evaluation on the shape of the context locals.

RH: random thing–is there an expectation that engines would inline thread-local functions?

CW: Some of the V8 people they feel that is a pretty important requirement.

JK: Concrete example is string.toLowerCase(). When we see it as a string, we can fast-path it and create it to an intrinsic, at the very least reduce call overhead instead of going through javascript. When we built it, was an important optimization, it would be a shame to lose that because of Shared Everything.

RH: V8 would see that a TL function was imported and each thread would need to check that each import was the same one?

JK: need a guarantee that all threads interacting with this module has the same import or provide the same value for the shared global or whatever.

CW: every context change requires a speculative guard–at each JS to Wasm crossing or at some other bind point (like the bind function suggested). Works best with the fused instruction; all calls to that variable can be inlined then.

TL: Can you explain fused?

JK: what I described does not require guards; the check is at instantiation

CW: Yes but these are two different techniques, you’re describing inlining static calls, i would expect it to not work with call ref, right?

JK: True, won’t work for call_ref

RH: In the case where you are instantiating something and you receive a thread local function, you only instantiate it once and you only know provisional threads local value, all the threads will eventually buy into that thread local function. So when you emit the code, you need to have a guard that the thread bound on this thread is the built-in you expect it to be. So I think you will still need the call site guard after that to do the lookup?

JK: (thumbs up)

CW: can get away without a call-site guard if you have a context switch guard; if you eagerly know then you can do this at the context switch. The context-local design makes it easier to do this optimization.

RH: On the topic of context locals, I didn’t fully understand the outcome: what are the concerns with the two types? Is it engine complexity? Type system complexity?

CW: It’s feasible but there is a lot of complexity in the design and ecosystem. You’d forever have this fragmentation of different worlds that you need to take care to move between. There is always going to be one direction that is hard, so we need to stack what does that look like? Toolchain needs to work with these forever. Feasible, but if we avoid it, we avoid complexity that might be unnecessary.

TL: More detail from toolchain side: if the goal is with shared continuations in a toolchains we want to do work stealing AND have shared functions with unshared parameters, the problem is we want indirect calls to work between these two kinds of functions. We should only need the signature, but with this division (shared-fixed (SF) vs shared-suspendable (SS)) we can no longer do this indirect call between the different types. E.g.: vtables, function pointers, closures, any indirect call will run into the split type problem. Toolchain could just give up–choose one or the other–don’t like this. Another solution is to convert from one to the other, likely SS to SF–a wrapper function with a shared barrier. If all you have is a function pointer, then you need some kind of func.bind before doing the barrier, etc. That would be even more complexity; these conversions are pretty unsatisfying, even if possible. Strongly prefer one shared type, even with SS and SF semantics.

RH: You were talking about having a program that has some SF and some SS. My thought, originally, was SF would be useful for cases where you need to call JS, interop points, and need to go into the local world. My hope was that those could be the leaf points of the call stack. If you compile, all your functions would be SS, in the indirect case. But web api, those would go through a suspendable wrapper that does a barrier, or just a barrier that would do the call itself. My goal is that it would not be arbitrary. The ABI would be that languages are all SS and when you need to call out, you make the switch.

CW: The designs we’ve discussed can’t cover that; need the JS function as a parameter, calling SF we don’t have that parameter in the first place.

TL: Assuming we don’t have a way to import thread-bound functions as SF.

CW: In that case we don’t need SF because they can be called from SS.

TL: You still might want SF to pass unshared params around. Maybe that would be easier to get away with, but there is a reasonable world where we want SF anyway.

CW: that’s not a world where we call from SS to SF; there are always some use cases. Need a reasonable semantics without that division, that would be preferable.

TL: RH, your Q would this just be on the boundary? I agree. The use case for SF is on or near the boundary where we’d pass these JS references around. Toolchains, thinking about Emscripten, do not differentiate between functions that are or or aren’t in the boundary. I can declare a function in the header, implemented in JS, so a boundary function, but I can still take its address and make an indirect call to it. Yes it’s on the boundary, but I still think we need to support indirect calls.

RH: On CW’s point with SF, even if they are the leaf, we need to get the shared parameters to them–need the context locals to smuggle them down to the leaf.

CW: That is the design that would require clearing the variables when you suspend, right?

RH: Or the thing you mentioned where the context variables are inherited where with whatever you resume with.

CW: I’d hope if that works SF gives you little as a separate type; hopefully we don’t need a new type.

RH: Interesting, the tricky part is that you need locals and if the type is fixed, then you could have unshared locals. And if you just have that barrier, it gets difficult. We ruled out let which rules out dynamic locals in a shared context. I guess you could just use the value stack. But I believe with let, this is tricky for toolchains to use.

CW: Interesting point; I’ll think about that more. My feeling is that it is ugliness that we could solve some other way, but I see the value.

TL: Because the locals are useful to have SF and SS functions, it’s very plausible we want both. They would be differentiated in their declaration so SF can have unshared locals, but my point is with a single type, once I have a reference to that function, I shouldn’t be able to differentiate. The declarations can be different, it’s the references to the functions that should have the same type.

CW: Maybe that’s possible–need to think through that in more detail.

RH: One other thing I mentioned in the issue, the question of the ordering: which one calls which? Which one needs a barrier? CW had mentioned that SS could call SF to go back down we need a dynamic check. SS could be a subtype of SF and choose SF as the type for all function references. One difficulty: if your function is SS and you do a call ref to a SF, we would need a barrier. 

CW: I think all calls end up needing the barrier if you don’t know whether the ref is SS or SF

CW: How complicated are the calls into JS? How much do we lean on locals?

TL: Need locals all the time: compilers only differentiate between locals and stack values very late. A dumb algorithm at the very end–the majority of the compiler does not differentiate them. It would force more of the compiler to understand the difference.

CW: Then we need to take this seriously as a design constraint.

RH: In the case of the current design (thread-local functions), call `new WebAssembly.Function` my sketch would be to generate a trampoline that either calls or traps if not bound. Every call would have to go through one of these wrappers. If you squint, it’s similar to SS and SF: engines have to implement a shared barrier anyway for TL functions and have a shared continuation capture local state. If you have context locals and shared barriers you could probably emulate what TL is doing.

CW: The problem is the same if we’re talking about…

RH: Thread-local allows a call stack that interleaves local/shared and requires an engine barrier already.

CW: It would not be ok for a…

TL: Right. TL functions would not be able to return non-shared references. For JS, we have toWebAssemblyValue() that is a builtin conversion that will trap if it can’t be represented as shared.

CW: If we think that TL world is ok, then I think the world with context locals is ok, even with just SS, by analogy. In both cases they take shared things and scalars; if not the case, then we need to address SF.

SYG: Q about stack switching, the SS thing is to support the ability to suspend a stack on one thread and resume it from another thread, is that the use case?

CW: Yes and wouldn’t be safe if you have a shared externref of a JS function on a stack, wouldn’t be ...

SYG: is there analogy here to the TLS story: there’s a TL cell and the thread-bound storage only accessible by its bound thread. You can suspend anything but if you capture a local value you bind it to the thread that captured the values?

CW: Can’t–need static annotations everywhere

SYG: Does that need to reflect in the type system?

CW: Need to know statically whether you have a shared or non-shared suspension

SYG: At the point of execution could you just keep a bit? If it’s not a use case then this doesn’t matter.

CW: I believe if you keep the bit you are forced into SS and SF as static annotations.

SYG: Have you thought about restricting the threads on which a continuation may resume?

CW: Interesting idea but how does that gives us an out to the problem? If a continuation is classified as shared so long as there’s one other thread it can be resumed in, seems as bad as the general case

SYG: It makes it a dynamic issue: if the app calls fetch on your stack…. Punts the problem to the application.

TL: An interesting idea… It's like thread-bound continuations that are typed as shared, but trap if you try to resume them on anything but the owning thread. Just like our idea for thread-bound data, which is typed as shared but traps if you try to resume it.

SYG: It is data at that point–maybe extend the thread-bound concept to continuations. Not too familiar with that proposal…

CW: In JS we may have thread-bound things, I expect that to be a shared thing in Wasm. When we suspend and capture a continuation we believe we know whether it’s shared/unshared

RH: How is a runtime check like this implemented? Don’t have a good idea of acceptable costs in stack switching proposal; dynamic checks might have to search through many stacks, suboptimally.

CW: A cost per call stack is acceptable if it is “check a bit” per call but not “walking all the elements of the call stack.”

IR: Right now it is a constant operation; in the future it will be constant as well. You always know where to switch because you know where it came from.

RH: If you search for call frames we would have to maintain that?

CW: Getting into delimited (Andreas) vs non-delimited (Ilya) debate; depending on which one is preferable the costs are different. The hope in delimited is constant per call frame; no scanning.

SYG: My intuition is that it would be more expensive than a bit. You probably need to keep a count of local things pushed and popped. Propagate that count forward on calls. Then check the count when suspending.

CW: in the case where you’re producing a shared or non-shared continuation you just prohibit non-shared continuations from showing up in a shared stack anywhere in the function

TL: when you leave a barrier, need to know how many are stacked up

CW: depends on the strategy for implementing the handler, block structure vs pushing into call sites

LW: missing a constraint: pass unshared stuff into shared and then pluck out an unshared funcref or callref and pass it unshared stuff plucked from the context, seems like there should be some scoped control flow instruction which validation prevents from calling shared–this forces us to be a leaf. Why is that not sufficient?

CW: unshared locals

LW: gets into “let” and all that;...

CW: this is exactly “let;” do we want to reopen that discussion?

LW: it was complicated because it got conflated with other issues…

CW: there was an engine concern that you’d need to dynamically resize the number of locals

LW: don’t know the max local depth up front? Let’s say we solve that; wouldn’t that solve this problem?

CW: In our existing design, we assume parameters are only scalars or other shared things; we can get pretty far with that.

LW: When we call to JS we need an unshared funcref

CW: Still need a shared barrier but don’t need additional locals/let

LW: …

CW: …

LW: Maybe there's an externref that’s unshared, assembling a call stack; a very specific, leaf case. A constrained situation.

CW: This is about interacting with JS from a shared context

SYG: How can we control that the JS doesn’t call back into a shared Wasm?

CW: Suspension barrier… <TODO> Where do we get the unshared externref from in the first place? If we get it from the context, we don’t need locals for that.

LW: If it’s just brute-force currying, maybe that’s sufficient.

CW: Shared barrier protects the <TODO>

TL: Shared barrier is fine. This conversation assumes we have a context we can attach an unshared thing to; not bought into that yet. Prefer thread-local globals but its another form of the same thing. “Let” is problematic.

CW: Can you work with just scalars and shared things as parameters?

TL: If we can pass things but not use them as locals–that sounds very risky.

CW: Our choices: no non-shared locals, or SS + SF, or make “let” work

RH: Another choice: function definition that implicitly has a shared barrier; that function can have locals there.

TL: That’s what I thought SF should be.

CW: I was worried that we start with SF; if we add SS and SF at the same time, maybe that’s more OK. If SF is just a barrier with locals.

TL: In toolchains, only at the very end “do we have non-shared things in this function?” then make it SF

CW: you might end up with type errors if you have a suspension inside

TL: Allow it to validate but trap.

CW: Need to think more about it.

LW: There do seem to be some good options. I like CW’s first proposal. Any strong arguments against?

RH: If you have different modules with different contexts you either have ABI problems or context switches at each boundary. Hash-table lookup for generic contexts.

TL: An ABI break: downcasts, lookups, etc. At that point we should have just put the context in the engine.

CW: Mismatched contexts? Two modules compiled separately that you try to fit them together later?

LW: Or they all follow the same ABI because they use the same toolchain.

TL: A generic ABI means some kind of downcast or lookup to recover the specific context information. Might as well put that overhead in the engine and keep the language simpler and avoid an ABI break.

RH: Performance question: no worse than doing thread-local lookups (some concerns with that)... a longer topic. We are calling into JS after all.

CW: The difference is that with thread-local functions you’re using strings, but with the context you have a dense array, so harder to just work with subsets of it

TL: TL functions can be imported as shared; no need to pass around an imported context.

