![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the July 9, 2024 video call of WebAssembly's Threads Subgroup

- **Where**: zoom.us
- **When**: July 9, 2024, 4pm-5pm UTC (July 9, 2024, 9am-10am Pacific Time)
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
    1. TLS with context passing ([#42](https://github.com/WebAssembly/shared-everything-threads/issues/42) and [#66](https://github.com/WebAssembly/shared-everything-threads/issues/66))
    1. Thread-bound data [#53](https://github.com/WebAssembly/shared-everything-threads/pull/53)
1. Closure

## Meeting Notes

### Introduction of attendees

- Thomas Lively
- Ryan Hunt
- Manos Koukoutos
- Ilya Rezvov
- Emanuel Ziegler
- Shu-yu Guo
- Sulekha Kulkarni
- Conrad Watt
- Nick Fitzgerald
- Andreas Rossberg
- Jakob Kummerow
- Deepti Gandluri
- Luke Wagner
- Adam Klein

### Discussions

## TLS with context passing

RH: There was debate around context passing. I got lost in some of the discussion, but the last post from Luke described a design based on linear struct passing. There was discussion of whether the typing rules for context passing are a rabbit hole.

CW: Think back to the way we were discussing non-nullable locals with cross-block initialization. You need a type annotation on every block and control flow join tracking the status. If you have to describe the context shape at every join, then they're basically everywhere. The context persists across functions, so the combination with EH is worse. Doing this correctly gets complicated. Discussed recently with AR and we just kept getting more upset about how to do it correctly. Luke's latest comment doesn't fully work through that and I can write a comment in reply when I have time.

RH: Would the annotations be better if contexts couldn't change within a function?

CW: When an exception is thrown, the context would have to be in a good shape. Exception handlers would need annotations.

RH: Maybe we could put contexts on tags so the thrower and handler agree on context.

CW: Then you can only throw if you know you're going to be caught in a function with the same context.

RH: I was assuming this was very coarse-grained, so a language family would share an ABI, so this would be ok.

CW: You either end up with restrictions such that you can never use contexts unless you know all the contexts, or you put annotations everywhere. There's no in between.

RH: My intuition is that having the consistent ABI assumption would be ok. The context would be very general–a pointer into linear memory or a single GC struct reference.

CW: Do you make it a language-level feature that can't be used without such a restrictive ABI, or do you punt deciding on the ABI to the toolchain? There is a tie-in to the discussion about not having shared functions. We could have shared non-suspendable functions. The question of whether they could be used depends on…

TL: ABI changes. Importing JS tag. Concerned about non-compositionality.

LW: Wouldn't the JS tag have an empty context?

CW: But to allow it to be caught, you need to annotate the block with the context.

LW: Not every block, though.

CW: But arbitrary blocks.

LW: This gets back to how the context can change instruction to instruction.

AR: You need a sound version of higher-order type state.

LW: Doesn't seem different from the operand stack.

AR: But it's cross-block, cross-function, totally global. Needs in and out context type.

LW: If you have an ABI, it will be the same indices everywhere.

CW: Unless you throw a JS exception.

LW: Need trampolines.

CW: But breaking to a block with a different context would be a type error. Requires lots of annotations.

AR: Taking a step back, typing is just one issue. Way too much type overhead and toolchain complexity. I question whether this is the right abstraction in the first place. We understand how to implement linear thread state, but that might not be right for TLS, which is essentially dynamic scoping.

LW: But native code does this fine because registers are context-local state.

CW: But not safely.

LW: Add types to make it safe.

AR: Register analogy doesn't fly because native code can store state on the stack. TLS is bound to a stack.

LW: But you can implement that in terms of something like registers.

AR: Only works when every stack switch goes through a scheduler that saves and restores stack state.

LW: Same with thread-local globals.

CW: Native code doesn't need a type system to make this sound.

LW: If the type system is impossible, then fine, but I don't see it.

AR: It's effect typing. An update to the state is an effect.

LW: Isn't everything an effect in that case?

CW: The reason it's considered an effect is because of the cross-functional nature.

LW: But we're not talking about mutable state, we're talking about passing values around. It's value semantics.

AR: You're talking about threading state updates everywhere. If you model state in a functional manner, you get rid of the effects.

TL: Time out. Conrad has offered to write up a fuller response when he has time.

CW: Exceptions are complicated and we would need to figure out how to paper over the JS tag thing.

AR: We need something more modular.

CW: The other option would be to go whole hog for the effects, and you can alternatively view that as value passing. All control flow needs to handle it.

LW: Compiler will not have issues because it already generates safe code.

AR: But typing it is far too complicated.

TL: Thread-local globals so far have had this peanut butter cost where they make all indirect calls slow because the TLS pointer might need to be updated on every potential instance boundary.

RH: They would similarly make stack switches slow.

TL: My latest thinking is that if we can have a dense vector of TLS blocks hanging off the instance, then maybe we can just do the lookup on each thread-local global access. It will only be a sequence of loads, not a concurrent hash table lookup.

RH: Thought about this implementation. How do you allocate thread IDs? Do you reuse slots? With weak memory, reusing slots might require a barrier.

TL: Good questions. I don't have answers yet. But I agree that paying the cost on every indirect call is bad.

RH: For shadow stack pointer, I imagine it would still be faster to pass it around as an argument.

TL: That would be good to experiment with.

AR: How bad would it be if you just didn't do anything for TLS? Use ordinary parameter passing or effect handlers. There are several options.

CW: That means we're deferring work stealing. We could do the version with shared non-suspendable and use non-shared parameters, but not more.

RH: It could be useful to split the problem between shadow stack pointers and other use cases. Then we could still have shared-suspendable and pass the shadow stack pointer as a param.

SYG: On performance and whether it's good enough to do something naive. It seems analogous to the security thing V8 is doing to sandbox pointers via a trusted external pointer table. It's not all pointers. I assume the TLS stuff won't be for all accesses. The sandbox is a concurrent, thread-safe pointer table that can grow and shrink based on GC pressure. The kind of pointers they want to sandbox on real-world workloads, the overall regression was 1-2%. We're willing to eat the cost for security. Is 1% an acceptable cost?

CW: Even for shared-suspendable functions, we can have something that works. If you have thread-bound functions, the ABI could have you pass in all the thread-bound functions as shared parameters instead of unshared parameters.

CW: We want to do shared functions. It's the new capability for the platform.

TL: Shared structs and arrays are also a new capability for the platform, or at least get WasmGC languages to parity with linear memory languages.

CW: There are three levels of complexity in supporting shared functions. (1) shared-nonsuspendable with only parameter passing, (2) shared-suspendable by adding thread-bound JS functions, (3) shared-suspendable by adding true Wasm-level TLS features. The point being that it would be good to at least do (1) rather than totally giving up on shared functions!

CW: What is the motivation for reduced scope of V8 prototyping? If we had a perfect TLS design, would V8 implement the full thing now?

TL: No, the goal is to reduce complexity, so even with a perfect design, we would still start out doing the minimal useful thing.

AR: But you can't compile vtables without shared functions.

TL: You have to use indices into tables, the same as linear memory languages.

AR: Not parity if you have to fall back to tables. If you had a full GC story, you wouldn't need the tables.

TL: It's functional parity, at least, even if it requires unfortunate workarounds.

CW: Is there a wasmtime appetite to experiment with shared functions? I imagine it would be easier than in a Web engine.

LW: I imagine so, but it's unclear how much effort it would be.

CW: My concern about V8 taking their foot off the gas on shared functions is that it makes the TLS discussion less urgent. Will we be able to experiment with shared functions and TLS in addition to shared structs and arrays?

TL: Unfortunately experimentation will have to wait in V8 since we can only do one thing at once.

NF: Wasmtime won't have cycles to work on shared functions soon, except perhaps for Andrew Brown.

CW: WASI people definitely want shared functions, so are there free cycles there?

LW: Some people want threads, but except for Andrew, they're not contributing engineers. We don't want to bake in instance-per-thread because it is clearly the wrong model in the long term.

TL: We can still make progress at this early stage by discussion, so I'm not too concerned that we won't have implementers for shared functions in the short term.

CW: Two leading candidates are in tension. It can be easy in the type system or in the engine, but we need real implementations to inform the decision.

CW: How important are shared functions for the code splitting use case?

TL: For both wasm-split and dlopen, the benefit is that you can load the code once instead of once per thread. But unfortunately the immediate problem in that space is how to make splitting usable at all, not how to make it fast. Maybe eventually this will be a reason to work on shared functions, but not now.
