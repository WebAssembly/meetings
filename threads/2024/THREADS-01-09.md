![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the January 9 video call of WebAssembly's Threads Subgroup

- **Where**: zoom.us
- **When**: January 9, 5pm-6pm UTC (January 9, 9am-10am Pacific Time)
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
    1. Walk through and discussion of proposal overview (Thomas Lively)
1. Closure

## Meeting Notes

### Introduction of attendees

- Thomas Lively
- Conrad Watt
- Zalim Bashorov
- Paul Dennis
- Paolo Severini
- Alon Zakai
- Nick Fitzgerald
- Shu-yu Guo
- Andrew Brown
- Ilya Rezvov
- Sulekha Kulkarni
- Ryan Hunt
- Manos Koukoutos
- Alex Crichton
- Ashley Nelson
- Adam Klein
- Yosh Wuyts
- Emanuel Ziegler
- Johnnie Birch
- Deepti Gandluri
- Matthias Liedtke
- Luis Fernando Pardo Sixtos

### Walk through and discussion of proposal overview (Thomas Lively)

tlively presenting [overview](https://github.com/WebAssembly/shared-everything-threads/blob/0c23f3f4b80cbc5e0cb3ebf4db02cb755a1eb25f/proposals/shared-everything-threads/Overview.md)

#### `shared` annotations

YW: does “subtyping” in this context just mean new type aliases, or also things like one type containing another?

TL: Subtyping just meaning subsumption, like how an i31ref can be received wherever an eqref is expected. Non-shared structs could contain a shared field but not vice-versa.

CW: Data segments, can we get away without shared annotations? think about memory.initl to a shared and unshared memory. You wouldn't want to have to duplicate the data segment.

CW: If you catch an exception, rethrow and catch it again, do we guarantee that you’re not rematerializing, do you have reference equality between the two exceptions in any meaningful way?

RH: exnref is not a subtype of eqref so there’s nothing you can observe for equality right now

TL: In the engine is the identity the same, even if that's not observable?

CW: The point is engines could do either right now, is that correct?

RH: Tricky because JS can throw exceptions so there has been talk of rationalizing throwing JS string, how those things materialize as an exnref. My understanding is JS can throw primitive values that are auto wrapped into a tag defined by the host. Right now, because there is no reference equality, that's all observable but it could be more observable, not the reference equality part, if we expose this tag.

CW: I’m wondering if it is possible for the existing catch all ref to blindly catch all exnref even if the thing thrown was a shared exnref. Maybe that’s suspicious and some implementations would need to materialize a separate wrapper in that case. This is very speculative.

RH: Tricky, need to think. A shared exnref means its payload can only contain shared things. There’s no subtyping relationship between exnrefs and shared exnrefs. So you couldn’t have a catch_all_ref catch all the shared type of the relationship, it needs to be one or the other.

TL: Would be nice to be a subtype so you can catch the two. But that would be consistent with everything else.

CW: Thinking of something with even less thought. If you’re in catch_all_ref you just unconditionally get a non-shared exnref, even if the thing was shared. Is that too weird?

TL: In a shared function, you would only be able to catch a shared exnref, so if the non-shared exnref appeared as a shared exnref, it would allow the non-shared payload to be observed on another thread.

CW: Totally right. Everything I said earlier was leading to nothing [nb: my train of thought was wrong]

TL: What if we had a nonshared ref with a nonshared type. If you shared it and then rethrew it on a different thread.

CW: Exactly. Maybe we need to have a total bifurcation. If you have a catch_all shared you can only catch the shared things.

TL: What do you do when you’re a JS thread local function throws a thread local exception and that ends up being caught in a shared function?

CW: Its desirable to not be able to express a non-shared catch all in a shared function

TL: You'd need two different catch_alls on your try tables, one for shared and for non-shared. They have different types so they need to go to different places, it’s quite ugly.

CW: The point is with shared continuations, a shared function shouldn’t be able to capture a non-shared exnref

RH: Exnref shows on the JS side as a prototype and it has properties and those are writable. So if you have an exnref and it puts properties on it, it can have JS strings associated with it. If you’re thinking about what is a shared exnref, you might need to think about that too. Not the case for GC objects today, but with the exception handling rules of today you can totally catch an exception and add properties to it which would make it unshared.

TL: Hadn’t thought of that, speccing shared exnref on the JS side might be weird.

CW: Is it not true in Wasm, with our new concept of exnref that has a tag you can check, it's only if you can add JS properties that things get suspicious?

TL: Right.

#### TLS

tlively asking for feedback on decision to make thread-local globals as realm local in JS

AN: What’s a realm?

TL: JS has a concept of "realms" which are essentially different copies of the JS environment, e.g. different copies of console.log, that all coexist and can interact with each other. This comes up in iframes, for instance, which have their own realms that can interact with the realm from their parent frame.

CW: Think of the interaction we do with JS in regular Wasm. When we import a Wasm function to JS, it's analogous to bringing a new function into JS and even in JS you’re allowed to bring a closure into cross-realm. And you expect the realm you’re referring to refer to inner realms. If you move that module to another realm, just because that module was a shared module, you have to redeclare your imports. Where you wouldn’t have to do that with non-shared. And even if in the non-shared Wasm world you’d potentially want some dynamic access…

TL: Simply more consistent with the things currently working if we have thread locals instead of realm locals.

RH: What's the motivation for realm locals instead of thread locals?

SYG: I take the opposite opinion to CW. DX is a good thing to focus on for sure and I think for the usual case, it doesn’t matter for DX. I imagine the usual case is 1:1 of realms and threads. I imagine people are not running Sphinx in a synchronous iFrame. How I arrived at realm-local makes more sense than thread local is if you have the mental model that JS is the syscall for Wasm, then you need to hook that up somehow. Currently you look that up in a shared world by whatever thing you’re executing. In a shared world, you end up moving to a more dynamic shared place because you don’t know what thread you’re going to be running in. Technically the syscall you’re embedding is different thread to thread and realm to realm if you make the decision to be thread local, it doesn’t take away the fact that there are multiple executions on the same thread. If your JS embedding has installed polyfill, some globals inside of an iFrame and your outer realm. If you’re running some shared payload that has some TLS table setup with JS APIs. 

CW: The scenario you’re describing where an individual iframe is doing a polyfill, the question of threads or not is orthogonal. What will happen in wasm is you’ll take the definition you originally imported at instantiation-time (fixing the realm) - if you’re in the single-threaded world and you transfer the Wasm to a new realm, you already have the issue of not seeing the new realm’s definition

SYG: True but in a single threaded world, there is no surprise because it's a lexical scope thing. You closed over them. In the shared world, it's more dynamic. You cannot access the original context. You’re running in a new thread so where do you pick up the new context.

CW: Not inconsistent to say you have a context per thread and in the same way you fix the content in the first thread by ??? you fix the content in the second by binding the secondary function.  

…

<TL, CW, SYG… too quick of an interchange to capture>

SYG: want to think more about the bad DX question; it’s only a surprise if you’re a JS wonk.

CW: My bet is 99% of the realm local storage surprises show up in the single-thread cases already.

TL: Let’s file an issue. SYG, we can have more deep discussion too.

<back to presenting>

RH: You said that you can do global.get in the initializer of a thread local?

TL: Yes it works the same way as global.get in a global initializer today, newly valid with WasmGC.

RH: When does this run? Still the very first function run on a thread? Not sure if it's observable or not.

CW: Shouldn’t be observable.

RH: I can never remember… that sounds right

CW: The timing should not be observable otherwise we should forbid these initializers.

TL: If it was a problem, it would already be a problem in WasmGC because you can already initialize globals if you want. So we must have restricted it to be immutable globals otherwise WasmGC has a bug.

CW: The main thing I’m scared about is not functional behavior but the resource budget; if you allow allocations to happen lazily that could have surprising performance implications…

TL: On the other hand, a separate allocation on each thread is very possibly exactly what you want. For example, in the C world, pthreads have a pthread struct that lives in memory of course. Each thread gets one. Has all sorts of context info. If you port that naively to a Wasm world, you can imagine having a pthread struct that is also thread specific.

CW: Do you want that allocation to happen at an unpredictable time or in a start function ???

TL: Something we should keep in mind and evaluate as we get implementer feedback, unless someone else has a strong opinion.

PD: Less features! Can always add more later!

TL: In this case, I wouldn't categorize it as adding or not adding a feature. We definitely need thread local globals as a feature. The question is how it should behave.

CW: I interpret PD’s comment to support my restricted initializers.

TL: Fine, updating the document with that and switching the note. We’ll have to spec out a subset of the instructions that are non-allocating but that seems fine.

CW: Restricts certain non-nullable thread-local globals…

RH: Could we restrict to defaultable only and not allow any sort of initializer?

CW: Yes, that’s what I’m advocating for.

RH: We could instantiate blocks eagerly. We might not be able to run the initializers….

CW: Is it the case that for every defaultable type can we initialize with zeroes?

TL: In v8, the Wasm null is not zero for anyrefs.

RH: Is it a per-thread or per-process number?

TL: Good question, shared references must be the same value across all threads. And we’re only allowing shared references and TLS globals for now.

RH: In SpiderMonkey 0 is the default value for all shared globals

TL: What if I have an i32 thread-local global and want to initialize it to 5–can I do that? We could start out super-conservative: no initializers.

RH: I have not implemented thread-local stuff but that seems to be what would work for almost anyone who needs it. 

CW: Functionally this will always work.

TL: I expect we’ll want to relax it to allow initializers. Especially concerned if we don’t allow allocations we won’t be able to have non-nullable globals.

CW: That is an implication of this and all initializers need to be default values; globals must be initialized…

PD: I was surprised it was a high-level feature, it seemed like a low-level feature. 

TL: Are you talking about having TLS globals at all?

PD: Yes, they're like thread local globals that get initialized by the C++ runtime. Hidden by the compiler.

TL: If we allowed arbitrary initializers we still wouldn’t be calling constructors; still very constrained. But your point stands–more stuff for the engine to do if we allow that.

#### Thread Management

AB: Created a draft PR (https://github.com/WebAssembly/component-model/pull/291) for adding these built-ins to the component model and Luke has already added a bunch of comments about that. And if we wanted to discuss more, that PR is a great place to discuss that.

PD: Philosophically, spawning a thread is like a goto–worse in fact (splits into two executions). WebAssembly does not have gotos; spawn reintroduces this. Found literature to do this differently: nurseries. Every spawn is “de-spawned” at some point.

TL: I’m not sure I see thread spawn and goto as similar, seems like you’re spawning a function, so it's more like a function call. The nursery idea seems like a generalization of thread spawn. If you spawn a nursery of just one thread in it. That seems awfully similar to thread spawn. Seems like a higher level feature, the nurseries. 

CW: Nurseries have a lifetime, like in structured concurrency, right?

PD: Yes, my usage point of view is less features in the sense that you can do less with Wasm and if you have to program more stuff in the runtime, you have less things you can do.

CW: The philosophical tension is Wasm is a compilation target; thus the lowest common denominator of targets people compile to Wasm. I spec-ed what goto would look like; not having goto causes a lot of pain and means that people are forced to “reloop”. The fact that there is no goto is problematic… JS backend sharing story.

PD: You can have a second function that breaks the encapsulation, the same as if you have a small function. You could have this low-level thing like for pthreads. How wuld this improve performance because if the compiler knows the parallel executions are done at some time, it could do some performance optimizations that wouldn’t be possible without. Because if you do it with Wasi, I assume it will be lots of function calls. Let's say you have two threads, one for memory 1 and one for memory 2 and they are not shared, and the threads are accessing the memory separately, no connection between them. You could actually have parallelism. Still in JS, the problem would be you can’t observe different executions, because whether it's single threaded or multi-threaded you don’t know. I would be interested if someone knows whether this cannot work or not?

AB: If you have feedback, add it to Paul’s open discussion thread: https://github.com/WebAssembly/shared-everything-threads/discussions/22. 

ZB (chat): Could shared functions access browser APIs (through import)?

SYG (chat): yes, that's what the TLS mechanism is intended to enable

ZB (chat): by storing to shared TLS global? Observation: It seems like in languages without concepts similar to "shared" (is there any?), e.g. Kotlin and Java, we will be forced to use shared annotation for everything.

CW (chat): Zalim: that's correct

SYG (chat): yeah, you can set up a TLS table that has per-thread/realm imports of say, `fetch`. each thread/realm has to re-import it before first execution, but afterwards execution on T1 will call T1's copy of `fetch` and execution on T2 will call T2's copy of `fetch`. the conceit on the web embedding is something like, yes, they can technically be different, but all the threads' copy of `fetch` is going to be the same most of the time

CW: Will start a discussion about thread-local vs realm-local

SYG: Let’s talk now if you have 30 minutes. 

TL: SYG, please drop a meet link anyone can join if they want to.
