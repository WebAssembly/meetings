![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the August 6, 2024 video call of WebAssembly's Threads Subgroup

- **Where**: zoom.us
- **When**: August 6, 2024, 4pm-5pm UTC (August 6, 2024, 9am-10am Pacific Time)
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
    1. Update on toolchain feedback about the "minimal prototype" without shared functions
    1. Update from V8 GC team
    1. Using FinalizationRegistry for ThreadBoundData ([#74](https://github.com/WebAssembly/shared-everything-threads/issues/74))
    1. Alternative to ThreadLocalFunction ([#75](https://github.com/WebAssembly/shared-everything-threads/issues/75))
1. Closure

## Meeting Notes

### Introduction of attendees

- Thomas Lively
- Nick Fitzgerald
- Conrad Watt
- Emanuel Ziegler
- Zalim Bashorov
- Andrew Brown
- Ryan Hunt
- Shu-yu Guo
- Johnnie Birch
- Ilya Rezvov
- Oscar Spencer
- Matthias Liedtke
- Adam Klein

### Discussions

#### Update on toolchain feedback about the "minimal prototype" without shared functions

TL: Update is that toolchains (j2wasm, Dart, Kotlin) say they are ok with having to refer to functions via indices into tables duplicated on each thread, but are concerned about using table indices for short-lived data and still want something like thread-bound data.

RH: Specific examples?

TL: JS regexes for J2Wasm

CW: Would they be ok with explicit deallocation?

TL: No clear signal yet.

RH: Could make them shareable.

SYG: Unlikely, since they are regular mutable objects. Maybe we could scope it down.

RH: Maybe a shared Regex is something we could scope. We already are doing this for Wasm JS API.

SYG: It will be difficult to retrofit existing JS with regexes to be shared.

TL: Toy example with buttons and cycles

#### Update from V8 GC team 

TL: V8 GC team wrote a design document that concludes that GC collection of shared-unshared edges is possible with minimally invasive changes to the current implementation (still a big project, though). The team is strongly in favor of integrating with GC, not using manual memory management.

RH: Looked at the document, there was a question of feasibility in other browser architectures. Tough question because the existence proof is the implementation. Also unclear whether something will have acceptable performance. Global safepoints seem difficult to implement and potentially slow. Current work is improving single-threaded performance. Would be hard to leave this local maximum. Also our cycle collector just does different things and might run into different problems.

SYG: I agree with Ryan’s concerns… no cycle collector in V8. To the performance part, we’re optimistic that a separate shared heap is only collected by the main thread (not each thread). These pauses are already expensive anyways, so we’ll just add a bit more overhead there.

RH: What is the atomic pause?

SYG: I mean a point where you must stop the world and wait for GC to finish.

RH: The main thread stops the world from collecting the shared heap, but what if a worker “spams” the heap?

SYG: That's a good tuning question. Do you signal that back to the main thread to schedule a major collection? Don't want to design too much ahead of time without seeing workloads.

RH: Hard for me to evaluate without an end-to-end prototype.

SYG: Agreed; note that Google will be measuring our specific design decisions here.

RH: There is a high-level point that there is a philosophical position that the browser should be responsible for collecting things. SM doesn't disagree, but it's a large lift, so we're trying to be pragmatic about it.

CW: What interface does the source language represent? In the short term, it reflects the web capabilities better to require manual deallocation for shared web references.

SYG: Pragmatically, a lot of things become easier if you have the main thread own the shared heap, including cycle collection. It broadens intra-thread cycles to include shared->unshared edges where the unshared side is on the main thread.

RH: Is V8 thinking of a shared generational GC?

SYG: Current implementation only has an old generation, but there is pressure to add a shared young generation as well. The GC team will do it when they have to.

RH: Thinking this through on the SM side, we expect shared-ness to be viral and thus that the general hypothesis will hold (and will hold in the future as well).

SYG: Agree. The viralness of everything being shared puts pressure on the shared heap having a young generation.

#### Alternative to ThreadLocalFunction ([#75](https://github.com/WebAssembly/shared-everything-threads/issues/75))

RH: First, if V8 is not doing shared functions, do you need this?

TL: Probably not? But eventually we will want shared functions (e.g., stack switching). There have been questions about shared globals–need a shared function to access it (?). Need a plan for this: if plan A is “do it in GC” I think this is still useful as plan B.

RH: Could you import all your shared globals?

TL: That’s what we do with shared memory today; e.g., set up globals via JS, etc. Not a great solution.

RH: A quagmire. 

RH recapping sketch from issue

CW: It is getting close to Andreas’s dynamic context proposal–which seems more flexible?

RH: Not a coincidence that there is a similar memory model. But doing it in the JS API is less of a big lift for core Wasm.

CW: Dispatch requires the same engineering as contexts–and I’d prefer contexts.

RH: You could emulate the dispatch functions with contexts, but haven't given it much thought.

CW: New version of contexts (which I’m now championing) just uses a dynamic check, “have I defined the function in my thread-local table?” Maybe I’ll make a separate issue proposing this. Has the same characteristics as this proposal, I feel it strange to hide all this behind the JS API.

Proposal for dynamically checked contexts is here: https://github.com/WebAssembly/shared-everything-threads/issues/66#issuecomment-2168038286

RH: The overhead is probably acceptable; we need to figure out how the shadow stack pointer should work.

CW: But dispatch tables aren't solving any problems for stack pointers, so if you need another mechanism anyway, maybe you can solve both problems with one solution. There are tricks you could play to make the stack pointer use case faster with the dynamic system.

RH: One trick: type annotation on functions to avoid the check.

CW: Start with the dynamic thing, then turn off the check (unsafely) to measure performance. Secondly, it’s forward compatible in that we can add annotations in the future.

TL: A large design space for the context idea: how to systematically break this down? Still ideating with no clear winners–how to pick winners?

CW: Dynamic contexts allow you to break things down: can be iterated on based on performance analysis.

#### Using FinalizationRegistry for ThreadBoundData ([#74](https://github.com/WebAssembly/shared-everything-threads/issues/74))

CW: [TODO]

TL: Dart team worried about cycles.

RH: Understand the example with callbacks. But we already had to deal with this with linear memory Wasm. A staged approach will be useful.

TL: Yeah, makes sense. V8’s implementation will attempt to reach the end goal, for experimentation. To actually ship things, need staging.

CW: Dead air, manual deallocation would be even quicker from a staging perspective. If Dart already has the “Web DOM node” type?

TL: It’s not exactly binary, more “how painful is this?”

CW: Presents a different contract for the programmer.

TL: Assuming expressivity is OK, do we actually ship support for FinalizationRegistry but not other things? Or do we ship the whole interface but hide things from the user (i.e., things don’t get collected)?

SYG: JS complexity around weak is unfortunate; if we refine that to be “some things have identity but cannot weak-reference targets,” that complexity is harmful for JS, independent of Wasm. If you're writing a JS library dealing with weak stuff, it's more edge cases to figure out. It would be hard to take back.

RH: If engines gain the ability to collect cycles, couldn't engines remove the restriction and allow everything to be a weak target?

SYG: Sounds possible to remove in the future but I don’t know how people end up using this.

RH: I'm also assuming that it's a "you must be this tall to be using" kind of feature. Trying to give an affordance to toolchains that want to polyfill this.

SYG: Second point beyond JS complexity argument, a practical argument is that cycle collection is a core feature. We are pushing the responsibility to the program or toolchain, I’m assuming we don’t do that–the “wrong thing to do.” We just push the work elsewhere.

RH: I don't disagree it would be a better end goal. Just think it would be good to have an intermediate goal.

SYG: A legalese alternative, in the JS spec one can’t put objects without identity into a weak map (?), if such a thing could exist, we could leave a hole in the spec to do so. How comfortable are you with having the spec saying that this is the observable semantics, but "wink wink" consult particular implementations for lifetime expectations. Throwing an error is very observable, but how comfortable are you with signaling through some other channel that it will never be collected?

RH: Legally, no liveness guarantees; much push back on the web compatibility side (re: when things are collected)–want it fixed in the spec.

SYG: Want to understand that better. Given today's differences in how DOM node cycles are collected, how do we square the differences in practices? I haven't heard about interop issues here.

RH: For example, an event handler using a DOM node, if engine A and B have different collection mechanisms (one with what looks like a leak), the Dart application doesn’t get collected the same way.. 

SYG: Agree that all the common cases are handled by all the browsers. Again, we expect to get mileage out of main thread owning the shared heap to make cycle collection with at leat the main thread much easier.
