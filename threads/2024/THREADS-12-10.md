![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the December 10, 2024 video call of WebAssembly's Threads Subgroup

- **Where**: zoom.us
- **When**: December 10, 2024, 5pm-6pm UTC (December 10, 2024, 9am-10am Pacific Time)
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
    1. Discussion: thread.spawn signature ([#89](https://github.com/WebAssembly/shared-everything-threads/issues/89))
    1. Discussion: Consistent tearing behavior ([#87](https://github.com/WebAssembly/shared-everything-threads/issues/87))
1. Closure

## Meeting Notes

### Introduction of attendees

- Thomas Lively
- Conrad Watt
- Andrew Brown
- Luke Wagner
- Shu-yu Guo
- Emanuel Ziegler
- Nick Fitzgerald
- Zalim Bashorov
- Jakob Kummerow
- Sulekha Kulkarni
- Ryan Hunt
- Deepti Gandluri


### Discussions

####  Discussion: thread.spawn signature ([#89](https://github.com/WebAssembly/shared-everything-threads/issues/89))

AB: Context: we need a way to spawn a thread. Originally a `thread.spawn` instruction, but after lots of discussion, now a component model intrinsic. Want the intrinsic to behave exactly how the instruction would have. Other proposals doing experimental things (e.g. WASI threads) have users even though the full group is not happy with it.

CW: Platonic ideal for a thread spawn instruction would be taking a typed function reference. Could have a more restricted version to start that only takes one signature. Could then have it take the reference from the table.

AB: Not using tables in the current version, so we can statically check the type of the reference.

CW: This is the version that doesn't work with the tools?

AB: Right. Got it mostly working, but there were gaps. Alex and Nick suggested not filling in the gaps because it was too much work. Options: wait to fill in gaps (must happen once GC is better integrated with the component model) or use a version that looks like a call_indirect. Andreas thinks the spawn_indirect idea is a hack.

CW: Looking at call_indirect for inspiration makes sense. Can it have a type parameter? Because imported functions have no place to put such a type parameter.

NF: We're mixing layers a bit here. It's a component model intrinsic, not a WASI import, so there is no name.

LW: We've been choosing "canonical" names with versions, etc. mangled in for toolchain convenience. As a starting point I do like the idea of taking an i32 index with call_indirect semantics with a fixed signature. We could generalize it later as much or as little as we want.

TL: And no need for a type parameter at all because there's just one supported signature?

LW: Right.

CW: How do component model builtins refer to tables?

LW: By convention if you're doing the easy thing, but the component model has a place to say which table to use in the section where you declare the builtin import.

CW: This makes sense to me. Sounds like the only one who doesn't like it is Andreas.

NF: The thing that is difficult right now is when a type references another type. But with a call_indirect-style instruction, that's not a problem. Can't have a function type that takes typed function reference arguments yet.

CW: Sounds like this is a specific limitation of the tools that's the result of some engineering decision a few years ago?

NF: Right. But spawn_indirect is also useful on its own. It's what WASI libc ultimately wants. So if we want both eventually, then starting with just one makes even more sense.

LW: And before 1.0 we would be allowed to mechanically make breaking binary changes, so we could change it then.

CW: Could put "i32" in the name to maybe make Andreas happier.

LW: That could be discussed.

NF: Trying to separate the CM spec from what tools support. The CM spec can be more general and tools can just happen to generate just the fixed signature.

AB: Could implement and spec spawn_indirect now and make a note about a future, more general spawn_ref. It's just as expressive.

NF: Just as expressive, but the spawn_indirect version has more checks. Hopefully it shouldn't be a super long period of time when we don't have both. The wasmtime WasmGC implementation is maturing and adding it to the component model is going to involve fixing all the issues that are blocking you.

AB: Timescale?

NF: Perhaps H1?

TL: Andrew, you raised a concern about people using this in production too early. Is the thread spawn intrinsic enough to enable that misuse, or are we safe because the rest of the proposal is not yet implemented?

CW: But even spawn_indirect would require shared functions, right? And those haven't been implemented anywhere.

AB: But people want threads for WASIp3 next year.

LW: We can have cooperative threads via stack switching and add pre-emptive threads later. But this lets us figure out a lot of things like shadow stacks, mutexes, etc. at the CM level.

TL: Andrew, do you have the next steps you need?

AB: Yes, will summarize on the thread.

#### Discussion: Consistent tearing behavior ([#87](https://github.com/WebAssembly/shared-everything-threads/issues/87))

TL: We currently document that globals are not allowed to tear but WasmGC fields are allowed to tear for performance reasons. Allowing them both to tear requires re-specifying them in terms of byte sequences. Is that what we want?

CW: Can re-specify fields and globals as byte sequences. Will just make the spec harder to write. Cannot allow references to tear.

SYG: What do we mean by tear? Arbitrary values?

CW: Multiple writes to a field, then reads to the fields, the reads will see one of the written values if they are all aligned. I32s cannot tear, but everything else is allowed to tear. Want to match JS.

SYG: The reason i32s don't tear in JS is because they can only be accessed by typed arrays that can ensure alignment.

CW: We would also have to disallow packed representations that could lead to tearing. So i32s would also never tear in struct fields. Jakob, is it important to do this kind of more aggressive packing optimization?

JK: We reorder fields to save space, but we would not pack so aggressively that we would violate natural alignment.

TL: Sounds like we have agreement. I will make a PR to the overview.

CW: i32, refs, and i31ref will not be allowed to tear.

#### V8 prototyping update

TL: Currently hoping to have an initial prototype of shared objects (not shared functions) ready for experimentation halfway through 2025.
