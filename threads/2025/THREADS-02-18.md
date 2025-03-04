![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the February 18, 2025 video call of WebAssembly's Threads Subgroup

- **Where**: zoom.us
- **When**: February 18, 2025, 4pm-5pm UTC (February 18, 2025, 9am-10am Pacific Time)
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
1. Proposals and discussion
    1. TLS discussion
1. Closure

## Meeting Notes

### Introduction of attendees

 - Thomas Lively
 - Conrad Watt
 - Manos Koukoutos
 - Andrew Brown
 - Ryan Hunt
 - Zalim Bashorov
 - Emanuel Ziegler
 - Matthias Liedtke
 - Jakob Kummerow
 - Thomas Trenner
 - Luke Wagner
 - Chris Woods

### Discussions

#### TLS

Recap of Conrad's slides from CG meeting (TODO: link)

CW: All solutions have someone in favor of them. CW prefers Thread ID + thread-bound data/functions. But need to figure out lifetime issues for thread-bound data.

TL: Since we need thread-bound data anyway, we still need to figure out thread-bound data lifetimes no matter what we do with TLS.

TL: I would like to return to thread-local globals and enumerate all the lazy and non-lazy strategies at some point.

LW: I like thread ID and I see how it can be used to implement context locals.

CW: Luke, we had discussed a component model ABI where there is a context slot. Would that be polyfilled via thread ID?

LW: Yes, polyfilled. A native implementation could remove indirection. Folks should use the builtins rather than thread ID when possible because they are better optimizable.

CW: Makes sense. Maybe I don't have a full sense of how component model builtins will be used in the future. Are there multiple thread-local data items?

LW: The stack pointer and everything else.

CW: Any comments on thread-bound data lifetime?

TL: We still want the full global GC semantics, which is better for users.

LW: The canonical example of a callback attached to a DOM node may have a solution by scoping the callback to the DOM node. Are there any examples where the cycle involves arbitrary objects?

TL: For example using JS regex objects.

LW: But those don't form cycles.

TL: Also Kotlin closures flowing out into JS getting wrapped in JS closures to be callable from JS.

ZB: What happens if an object referencing JS goes to another thread?

CW: Everyone agrees that dereferencing a thread-bound data from the wrong thread will throw. You could have different copies of the functions or objects

TL: Another pattern we use in Emscripten is to proxy work (for example, file system work) to other threads to provide the expected user experience.

LW: If we're talking about having some cross-thread cycles leak anyway, then maybe we can be more intelligent about saying when that will happen and reducing it. It's nice that this is equivalent in expressivity to using FinalizationRegistry.

CW: Maybe I'm convinced.

TL: I'm ok not resolving this until we have prototypes.

AB: So will we prototype thread ID?

RH: How will the shadow stack pointer be shared with thread IDs?

CW: Using an indirection into a table, just like everything else.

RH: Would want to pass the thread ID rather than having some specified algorithm.

CW: I was imagining that it would be mutable and managed in userspace.

RH: What's the benefit of it being immutable?

CW: If you get it twice in the same function, you know it will be the same both times.

AB: Could have a read-only and read-write slot.

LW: Could set the TID whenever you call into Wasm.

CW: Just like context-locals. With the same management downside when calling into JS and back.

TL: Quick plug for thread-local globals: they don't have these problems.

CW: Can we cap the number of thread-local globals at 1 or 2 per thread?

TL: This would limit the number of Wasm modules that could be instantiated on each thread, even if they're mutually unaware. Bad!

LW: Making TLS part of the ABI is business as usual on native.

TL: Yes, but we generally have stronger compositional properties than native.

CW: … Describes ABI conventions for setting up the thread ID

RH: Edge case when there are multiple realms on the same thread.

LW: We want parameter-passing semantics.

TL: Imagining how to wire that up in Emscripten, it seems complicated. Would have to rewrite all calls into Wasm to pass the extra state. We do things like that for lowering i64 parameters, for instance, but it's kind of ad hoc.

TL: V8 prototyping plans

CW: Hopefully parallel experimentation in wasmtime.

LW: Doesn't instance-per-thread cause problems for WasmGC languages as well?

TL: Yes. Because the vtables can't be shared.

LW: If you want to do a dlopen-like thing in a GC language, you'll get NxM behavior as well.

ZB: Kotlin does need to support dynamic loading.

TL: Next steps?

CW: Fastest way to advance the discussion would be wasmtime experiments.

AB: I'm working on it!

TL: I'd like to discuss thread-local globals more, too.

AB: More thinking to do about component model idea of having two context-local slots for stack pointer and thread info block.

TL: Let's continue the discussion at the next meeting in two weeks.
