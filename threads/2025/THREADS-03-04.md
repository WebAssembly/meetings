![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the March 4, 2025 video call of WebAssembly's Threads Subgroup

- **Where**: zoom.us
- **When**: March 4, 2025, 5pm-6pm UTC (March 4, 2025, 9am-10am Pacific Time)
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
    1. TLS discussion (continued)
1. Closure

## Meeting Notes

### Introduction of attendees

- Thomas Lively
- Andrew Brown
- Ryan Hunt
- Nick Fitzgerald
- Conrad Watt
- Emanuel Ziegler
- Manos Koukoutos
- Zalim Bashorov
- Jakob Kummerow
- Luke Wagner
- Matthias Liedtke
- Shu-yu Guo
- Thomas Trenner
- Andreas Rossberg

### Discussions

#### Announcement about spawn_indirect

AB: We decided long ago that the way to spawn threads for non-browser engines would be builtins for the component model. The original version took a reference, and we decided that we needed another that would spawn indirectly through a table. This PR adds that new builtin: https://github.com/WebAssembly/component-model/pull/447. Here it is in the CM spec: https://github.com/WebAssembly/component-model/blob/main/design/mvp/CanonicalABI.md#-canon-threadspawn_indirect. Now is a good time to take a look and leave feedback. Even if you're not interested in the CM, you still might be interested in this because the signature might be reused in an eventual core Wasm instruction.

CW: Looks good! Luke, would we get instructions that look like these for the stack-switching-based threads we talked about.

LW: Yes, we would do something similar. We could have an immediate on the builtin saying whether it is shared or not.

#### TLS discussion (continued)

TL presenting [slides](https://docs.google.com/presentation/d/1cuE3RkRcENpdwJEyLT5OxR4oz5xMiJDRRWjPtF1aqrs/edit?usp=sharing)

AR: Is this referring to static linking?

TL: Yes.

RH:  Would you use thread_local for the shadow stack pointer if you’re doing work stealing?

TL: If you were doing work stealing in a language like Rust/C/C++, probably you need a high-level definition of a task that can be moved between threads; implementing it today in C with a void pointer, the stack pointer does not come into it and nothing is unusual. To use stack switching, you would need to redefine what it means to be a task; in that case we wouldn’t be using the stack pointer in the normal way.

AR: The main use addressed is for C-like languages, but Java has a more dynamic concept of thread-local: a class can have an arbitrary number of thread-local things (similar to OCaml). How will this work in those cases?

TL: The JVM has a single thread-local hash map mapping the identity of the field paired with the thread ID to point to the actual value. The source code looks like it implements as much TLS as you want. Thread-local globals help because… essentially this is what a native JVM does. There is not too much thread-local state in either the C or Java case: a stack pointer + pthread self in the one and this hash map in the other.

SYG (chat): it has to be an ephemeron map or it leaks, but maybe it leaks in jvm!

?? (chat): I’ve seen a number of comments cautioning folks from using Java TLS, so I think it leaks.

CW (chat): Technically it sort of doesn’t leak if you use real Java threads. But it leaks if you use thread pools and don’t manually clear. So everyone just says “manually clear all the time”, just in case the code is used in a thread pool.

RH: …do we need to compile to a different kind of shadow stack pointer?

TL: A task library would need some hand-written assembly to manage this… a pointer into a table of continuation references plus a pointer into linear memory to know where the shadow stack goes.

RH: Makes sense to me; my concern is that in resuming a stack, if the engine had spilled any thread local variables on the stack, it needs to unwind the stack and rewrite these values for the new stack. But then if the user written code clobbers it after that, all that work was wasted.

TL: The compiler would have to understand all this… It would need to mark the functions as "shared-suspendable" and would need to know not to stash the stack pointer in those functions. Seems complicated.

AR: Circling back, I’m wondering how this is all related: when instantiating modules dynamically, wouldn’t the engine have to implement this under the hood. Don’t we need the same mechanism already for first-class thread locals? Why not expose this directly?

TL: Thinking about LLVM, it understands the various TLS schemes (e.g., local_exec), because that’s all implemented in LLVM userspace, there is no need from those languages to provide this in WebAssembly. You’re right that the engine already does this for instances added to the store, I haven’t thought much about whether we need to expose it.

(TL presenting “Implementation Strategies”)

AR: We already have global instances so this would be a pair of the global and instance…

TL: But at compile time you don’t know which instance the global may be imported from.

AR: That’s true of all globals, so that’s a step to be done before.

(TL presenting “Group by Instance”)

SYG: On the web, the number of threads is small and the cost to spin them up is high, which is why we roll our own thread pool. So making this startup cost slower is acceptable. I would like to hear from the server-side folks.

LW: Ideally we would use virtual threads for things like goroutines. Java now does this with Project Loom.

SYG: TLS in this model is per virtual thread, right?

LW: Yes.

SYG: I wonder how Loom figured this out.

RH: The SharedInstance points to a big block of threads, must we have a bounded number of threads? How do we synchronize growing this block of memory?

TL: If we can grow this, we need some kind of registry, etc.

SYG: There’s a standard trick here: allocate a new table but don’t deallocate the old table immediately.

RH: I agree, but we need a safe point to free the old one.

CW: We assume we have stop-the-world GC.

LW: Is it a problem when we mutate the old version of a global?

TL: The tables are all pointers to the actual cells.

SYG (chat): sorry i misspoke earlier, i meant RCU (the linux kernel thing), not LRU. Like you can bound your threads in practice. Stupid question, what's the shadow stack pointer used for?

LW (chat): Address-taken C local variables, e.g.

(TL presenting “Group by Thread + Instance”)

RH: Back to tradeoff slide, to maintain an engine, I don’t know how to answer any of these questions. I have to support the worst case here and when I was reading this, I felt the toolchain should figure out what the implementation strategy should be.

TL: That’s fair. Knowing that thread creation is expensive is helpful. The web doesn’t have bounded instances and bounded threads: the workload could be anything. But we can work around that with more engine complexity–totally worth it in this case. But a reasonable position.

CW: The JS community may be unhappy if JS workers are slower only because there is some WebAssembly on the page.

SYG: Who?

CW: I thought it was you!

SYG: It depends: if it gets more expensive but only a tiny percentage, then “sure”--it’s not an absolute thing. Growing this table is not a lot slower but we need to prototype.

LW: One worry I have is that accessing the stack pointer is one load in the instance-per-thread model, but it could be slower here. Ideally we need a way to maintain this SP access as a single load.

TL: Jakob or Ryan, is it a single load today?

RH: Is the SP imported?

LW: No, in the case it is not imported.

RH: We have a pinned register so it is a load into an offset. The global is inlined into the instance; if imported then there’s an extra indirection. Any global that is not imported is baked into the code.

TL: If your instance is pointing to this table (“group by instance + thread”), you might have an extra indirection. In the “group by thread + instance,” hand-waving we hope there is some addressing mode that makes this fast.

RH: In “group by instance + thread,” there would be an extra two loads; an extra one for the table. This would be very cool if it could be made fast.

TL: Can we pick out the SP and treat it specially? E.g., in a register?

RH: A new hard-coded WebAssembly semantics… “thread ID.” Another SM issue with cross-instance indirect call is that we do more work on the caller side; we don’t know if the callee has TLS stuff, so we have to eat this cost for every indirect call–that’s another concern.

TL: Prefer allocate eagerly to avoid lookup cost; for “group by instance + thread” you don’t need to do any extra work on cross-instance calls.

RH: That makes sense; I thought we were doing the lookup on cross-instance calls.

LW: FWIW, we do want runtime instantiation for CM eventually.

TL: Don’t expect to convince anyone today, just want to convince people that this is worth prototyping; we have tenuous plans to eventually prototype this, not the initial one.

LW: Within the year we should have a prototype of the context.get|set builtins and show that working for pthreads.

TL: Andrew, what do you plan to prototype?

AB: Would like to prototype everything, but time constraints will probably be a factor.

TL: Anyone else interested in helping to prototype?

AB: Lots of people interested in using this, can't predict if they'll help with prototyping.

LW: The folks working on WASI 0.3 are working on a collaborative version of all this and real sharing will be the next big thing after async.

AB: How to test these?

CW: The original threads proposal adds WAST constructs for testing threads.

NF (chat): jepsen style checking + chaos mode schedulers probably the best bet for cost-benefit?
