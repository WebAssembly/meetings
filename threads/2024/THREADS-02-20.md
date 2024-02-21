![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the Feb 20, 2024 video call of WebAssembly's Threads Subgroup

- **Where**: zoom.us
- **When**: Feb 20, 2024, 5pm-6pm UTC (Feb 20, 2024, 9am-10am Pacific Time)
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
    1. 
1. Closure

## Meeting Notes

### Introduction of attendees
- Ashley Nelson
- Conrad Watt
- Paolo Severini
- Manos Koukoutos
- Nick Fitgerald
- Luke Wagner
- Alex Crichton
- Ilya Rezvov
- Dan Gohman
- Ryan Hunt
- Jakob Kummerow
- Sulekha Kulkarni
- Syrus Akbary
- Andrew Brown
- Thomas Lively
- Johnnie Birch
- Luis Pardo
- Emanuel Ziegler
- Deepti Gandluri
- Shu-yu Guo
- Zalim Bashorov

TL: (Presenting [slides](https://docs.google.com/presentation/d/1eJQjCyeeLy4MaUZPDVFfUHYQ39VF07CAJXt-UnWEiss/edit?usp=sharing))

CW: With respect to your with GC support bullet points, it is to that the generalized shared wrappers will need some GC support in ephemeral. Thread-bound wrappers will probably need GC support. 

TL: Yeah, two more slides: one sketches spectrum of solutions for TLS, the other the GC question

TL: (back to presenting slides)

CW: Wouldn’t be totally confident the dynamic scoping wouldn’t cause the ABI changes.

TL: Of these, dynamic scoping has the most amount of questions about how it would work. We have the effect handlers proposal, but having to switch stacks every time I want to switch my stack pointer is probably not going to fly. Need to think through how this would work.

RH: When it comes to TL-globals, does it actually work in a world where you’re suspending these and passing them around and sending them to new stacks. In that case, stack pointers are more of a stack global then.

TL: With the current explainer in the world with TL-globals, we have this rule that the shared functions don’t hold an unshareable intermediate state. But the stack pointer of course is not unshareable because it’s just an i32. If I suspend a shared function and send it to another thread. If it has a local or other intermediate stack value that is the shared pointer, that is potentially not going to be valid. Except when you send a task to another thread, maybe you send its in-memory stack with it.

CW: Sounds like general pointer problems, how do runtimes resolve pointers if they can be resumed in other threads.

TL: Yup

RH: I would assume that Emscripten entering … would need to allocate shadow stack space and when you send to the new thread use that shadow stack; it would be surprising if, on a new thread, the shadow stack was suddenly zero.

TL: Toolchain can accomplish that by storing the value of the stack pointer in a local before the transfer, then it would still be in the local after the transfer, even though the TL-global where the stack pointer canonically lives might have a different value after the transfer. Some sort of caller-save ABI contract around that would have to be managed. It would work differently for different pieces of data. The stack pointer might come along for the ride, but the live pthreads or TLS keys would be different on different threads. Some data would stay thread local. 

RH: extra information about context switching: with TL globals, what does it mean to look up one of these keys? Discussions about concurrent hash maps, dense arrays; the problem is the number of instances is dynamic. Heavy synchronization; must acquire locks. Does anyone have any clever solutions? Potentially large memory usage. Can we limit the cost of this to only users of this? Unshared functions can use TLS as well. An indirect call in SM has a check (JS realms) so in this case we would like to do: (1) either does the callee have TLS and look it up or (2) not make TLS part of the ABI and instead have each function perform a lookup on-demand

TL: One of the nice things about TL global design is that it's so declarative so you have the potential for different strategies. Of course you only want to ship one, but we can experiment. If we can come up with something that is fast, I’d be happy but I acknowledge there are performance questions here.

SYG: For Ryan, why need a concurrent hash map? My understanding is that in this part of the design you would know how many keys are necessary across all instances. A dense array could work.

RH: You have a wasm module with a TLS variable it declares locally. My understanding is you can create many different instances of that module as well. And then you can dynamically do 5 or 10 of them. Maybe the definition is different and it’s importing TLS as well.

CW: You can always create more TLS data at arbitrary points of execution. Always instantiate another module or free floating global. I think we should still make the layout dense per instance, but the question is shifting the perspective at import boundary execution?

SYG: That helps, thanks. The missing piece is that in the JS API you can create a new TLS thing.

CW: I could flip it around, you can create a TL-global in the JS API as instantiating a tiny Wasm module. I could imagine a naive implementation for dense allocation switching at the boundary if you access a TL-global that is created by the JS API to make it faster in that context.

TL: (presents last slide)

LW: Is finalization an option?

TL: If we had a finalization registry, need to track when there are no references on any thread; you need finalization to have global knowledge

CW: One way of saying this is if you have FR with shared keys, that's basically just as hard as supporting the strong semantics. So if can engine can do that, it can have a FR in the runtime.

LW: Is that really the case? It seems less arduously strong than WeakMaps.

SYG: I think it is. If you want to use FR, do you agree that we cannot use FR to collect cycles. FR originally created to collect references in the Wasm/JS boundary. The JS side has a wrapper object, to know when the wrapper dies to collect on the Wasm side. This cannot collect cycles across that boundary.

CW: You can express strong semantics in terms of strong finalization registry - a strong table, with entries that are nulled out when the finalization registry fires

SYG: Right, so the cycles thing–just clearing that up ahead of time. FRs can’t collect cycles.

LW: But if we’re not allowing cycles between shared and unshared, that’s a problem.

SYG: Even with no cycles, need to choose when the finalizer fires: dead in all threads or dead in one thread? In the former, you need a unified global GC; in the latter, this still has extra GC complexity.

LW: I think the strong semantics is what you would expect and easier.

SYG: You claim that there is semantics more intuitive than the strong semantics?

LW: I think it’s as intuitive as the strong semantics but if we’re containing ourselves to the FR, it’s categorically easier than strong semantics in general.

TL: Would the registry allow cycles?

LW: It’s not an edge, it doesn’t keep them alive, is that right? Or maybe it always keeps them alive? Or it’s not contingent on the liveness because it’s the FR? The roots, the postmortem notifier?

CW: Higher-level point, if we have a FR with that level of power, we can use it in userspace.

LW: This is less expressive than a weak map.

SYG: Right, but why?

LW: Well a weak map ends up being like adding an edge and a FR doesn’t.

SYG: Finalizer function can null out a map entry.

LW: But it will only fire when already dead.

SYG: so does a weak map. only clears the thing when the key is dead

LW: But if the thing is alive, it keeps the thing alive?

TL: Right, In a FR if the key is alive, it keeps the value alive as well.

CW: We’re getting off the reason these things are the same: the finalizer function can be a “drop” allowing it to be collected

SYG: LW’s point is the drop semantics, you can implement the drop semantics of weak map using a FR. But a weak map, also has no drop semantics, the liveness of the key implies the liveness of the value. LW’s point is that is not the case in the weak map, you’d have to implement that somewhere else.

CW: A table strongly roots the reference and then a FR where the finalizer nulls out the entry–so you get the same semantics

TL: You can implement a weak map in terms of FR and the semantics that we allow in FR correspond to the semantics we can possibly impl in the weak map.

SYG: Not sure if true, also think LW is overlooking complexity. You still have to choose a lifetime of when the finalizer fires if the key is shared. If the finalizer you want to fire is locally dead, that is pretty weird, what does that mean?

LW: That’s not the one I’m suggesting

CW: To lay out my point E2E: I don’t think we can have a strong FR without the strong semantics, because we can use one to implement the other. (see previous comment above)

SYG: finish the slides?

TL: (back to presenting the last slide, strong semantics)

LW: FR is weaker in a good way: it roots the unshared thing and thus roots the cycle.  A WeakMap in theory allows the cycle to be collected which may become the expected semantics and thus required of implementations..

CW: Can you expand?

LW: the difference is the edge; pure weak maps might be expected to be collected.

CW: Can the finalizers still run?

SYG: relaxed to allow them not to run; e.g, GC witnesses some refs die, finalizers queued up to run later on the event loop, it could be that the FR dies while queued, we shouldn’t have to cancel all those queued tasks.

TL: LW, under your idea, if weak maps and FRs are both garbage, there could be leak, right?

CW: shifts the question from “can we collect cycles” to “do finalisers fire after registry is collected”?

SYG: reframe LW’s semantics more simply as “put shared stuff into weak maps” and “don’t collect cross-heap cycles”--equal expressivity

CW: if FR kept alive, more things would get collected than in that scenario, right?

SYG: Why?

TL: all acyclic stuff gets collected and cycles leak?

SYG: if WM or FR goes away, the cycle could go away because the user code breaks the cycle; I’m not advocating for this, it’s very weird

TL: <back to presenting slides, weak semantics>

CW: weak semantics are actually my preferred semantics

CW: one way it is different: agree it is like “no support” when manipulating objects, but different when importing a callable function, this gives at least the option of calling unshared from shared

TL: Wouldn’t be scared of splitting this up; non-suspendable shared is basically the same as a shared function with a shared-barrier body.

CW: Can you expand please?  

RH: shared-barrier only prevents suspending your function into a shareable continuation. You can still suspend into an unshareable continuation.

CW: this is a problem for validation if we want to validate the that shared-non-suspendable functions cannot call shared-suspendable functions.

TL: you described three levels of functions: all three participate in rules; this would need to apply to function references. shared-barrier simplifies that: we can have only shared and unshared functions, and shared-barrier to enforce that unshared data doesn't get captured in a shared continuation at runtime.

CW: Very interesting idea, need to think it through more. Still can’t pass in non-shared things as arguments?

TL: Good point, shared-suspendable would be shared, have shared-barrier block, and allow unshared arguments.

CW: Have to think more about whether we would still need type system complexity to deal with the arguments.

TL: We should take an action item to explore and document this design space more.

RH: The optimized context-passing design has the benefit that it allows some context to be nulled out rather than implicitly rematerialized on suspension.
