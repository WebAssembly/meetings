![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the October 10, 2024 video call of WebAssembly's Threads Subgroup

- **Where**: zoom.us
- **When**: October 10, 2024, 4pm-5pm UTC (August 6, 2024, 9am-10am Pacific Time)
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
    1. Discussion of V8 prototyping plans
    1. Discussion of coordinating design with JS structs
1. Closure

## Meeting Notes

### Introduction of attendees

- Thomas Lively
- Conrad Watt
- Nick Fitzgerald
- Ryan Hunt
- Shu-yu Guo
- Sulekha Kulkarni
- Emanuel Ziegler
- Zalim Bashorov
- Andrew Brown
- Jakob Kummerow
- Manos Koukoutos
- Ilya Rezvov
- Adam Klein
- Andreas Rossberg
- Luis Pardo

### Discussions

#### Discussion of V8 prototyping plans

TL: shares doc

JK (chat): to avoid misunderstandings, I'd to emphasize that it's not so much "we won't do Shared Functions", but rather: we realized that Shared Objects are enough work, and Shared Functions have enough open questions about them, that as a means of prioritization we'll aim to get Shared Objects working before spending bandwidth on Shared Functions.

The other stuff (Shared Globals) will likely happen in between those two: after the very basics, before the really hard stuff.

SYG: Want to get away with shipping only cycles that involve the main thread. This is implementable incrementally because the main thread GC can also scan the shared heap.

RH: How are you going to know if it's enough?

SYG: Not that far along. Was thinking we would just see if workloads run out of memory or not.

#### Discussion of coordinating design with JS structs

SYG: For this room, you can basically consider work on implementing JS structs paused in favor of making progress on shared-everything Wasm. We are working on the spec to reach JS stage 3 (prototyping) after all the important decisions have been made for Wasm.

SYG: Right now JS structs have properties and other JS infrastructure that Wasm structs don't have, so they're not currently the same. If we want ot unify them, it makes sense to start from the minimal WasmGC structs.

RH: It would make sense to figure out a design for JS struct / WasmGC interop before JS structs go to phase 3.

CW: Since non-shared GC structs have shipped, we have to figure out how they will interop with JS structs first.

SYG: For shared weakmap keys, whatever the WasmGC decision is on usability, we will want to align with it on the JS side. There is not currently machinery for saying some objects cannot be used as weakmap keys.

CW: If we decide we don't want them to be weakmap keys, would TC39 go along with that?

SYG: I would be unhappy but wouldn't block. There was another TC39 delegate who didn't want a new kind of object, but I don't want to speculate too far.

#### Questions on prototyping doc

CW: Question on the prototype doc: there is a comment saying that scalar field accesses should be allowed to tear, but we decided that shouldn't be the case for globals.

TL: Good point. These should be unified, but they're inconsistent right now. Will take an action item to file an issue about that.

SYG: right now no such fields in JS - somewhat independent decision in Wasm

CW: What is the lifetime of the realm-local prototypes for shared JS structs? 

SYG: If we can have-heap GC cycles in WasmGC, then we can tie the lifetime of per-realm prototypes to object lifetimes, otherwise they would live for the life of the thread.

CW: Since the timelines for the Wasm side are so long, will the JS decisions be able to wait to follow from the Wasm decisions?

SYG: Yes, there's no rush there.

TL: We expect to be done with the initial prototype sometime in 2025, but probably won't get hands on with shared functions yet.

AB: Announcement: proposal is nearly complete in wasm-tools.

TL: Binaryen supports shared structs, arrays, and functions. Next step is accessors, but waiting until it's closer in V8. Have been thinking about fuzzing.

CW: Idea of starting with the happens-before graph and creating a program from it doesn't work well in practice. Can scrounge up some literature on it.

AB: Should I upstream the encoding, decoding, and validation tests?

TL: Yes!

AR: Will want to disable test running on CI to avoid failures.

SYG: We want release-acquire on the JS side.

CW: As long as we reserve space in our encoding, we can defer release-acquire in Wasm as long as we want.

TL: If we do release-require in JS, we should take the opportunity to split out linear memory release-acquire for Wasm and let it advance more quickly than the rest of the shared-everything proposal.
