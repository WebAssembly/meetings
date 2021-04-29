## Agenda for the September 19 video call of WebAssembly's debugging subgroup

- **Where**: zoom.us
- **When**: September 19, 6pm-7pm UTC (September 5, 11am-12pm Pacific Daylight Time, 8pm-9pm CEST)
- **Location**: *link on calendar invite*
- **Contact**:
    - Name: Derek Schuff
    - Email: dschuff@google.com

### Registration

None required if you've attended a wasm CG meeting before. Email Derek Schuff to sign up if it's
your first time. The meeting is open to CG members only.

## Logistics

The meeting will be on a zoom.us video conference.

Installation is required, see the calendar invite.

## Agenda items

1. Opening


## Meeting Notes
### Attendees:

* Nick Fitzgerald
* Derek Schuff
* Bill Ticehurst
* Luke Imhoff
* Paolo Severini
* Yang Guo
* Yury Delendik
* Philip Pfaffe
* Z Nguyen-Huu
* Arun Purushan


Debugger modules PR: https://github.com/WebAssembly/debugging/pull/6

NF: mostly interested in people’s thoughts on that

BT: comment from PR: is there prior art? VSCode tried to standardize DAP. Anything we could apply?

NF: haven’t looked at DAP in particular. This is informed by experience with spidermokey debug API and source maps. 

BT: does wasmtime have a similar mechanism?

NF: no, it takes wasm DWARF and generates native dwarf at compile time.
Not exactly like lldb, but itj ust converts the dwarf, and then a native debugger can be used on the native code.

LI: SInce there’s an official python wasmtime binding, do the python debugging tools work? Or do you need to use lldb? E.g. in general for other languages that load wasm.

YD: wasmtime converts the dwarf, and then waits for lldb to get the debug info. Python tools wouldn’t know about native debugging AFAIK. 

NF: Similarly to another native module in python. We could extend it for python debugger.

NF: we treid to keep it a very sm all API surface, not based on firefox in particular.

LI: in terms of efficiency, would having ignore counts, or limited trips per breakpoint be better? I.e. to make it full speed until we hit the point we care about. So you woulnd’t need an API call every time.

NF: the function will need to be recompiled to hit a breakpoint, but there would be an extra call to the debug module. We would probably want to consider this and not rule it out for the future, but maybe keep an MVP really simple.

LI: yeah this should be compatible going forward.

NF: The other thing is that Wouter left a comment. He basically said why not reuse a serialization mechanism (protobuf, flatbuffers, etc). I need to respond online, but basically: how do you get that into the debugging module? We don’t have calling conventions or a function call protocol. So you’d need that anyway. But also wasm interface types already has the means to describe this, so why not use that.

BT: is there capacity to example linear memory?

NF: not yuet. We first discussed as MVP just to have source-maps replacement; i.e. line numbers, breakpoints, stepping, without inspecting variables. That would be the next milestone. I think they’d be disjoint APIs, and wojldn’t affect the line table APIs.

BT: so the goal is to prove out the architecture and not be a usable initial release?

NF: this is as good as JS debugging is now, lots of languages compile to that.

BT: you’re definitely dealing with modifying memory more often with wasm.

PS: today browsers do expose the memory and low-level primitives.

NF: true, we have 2 layers today where one is what programmers want to see (e.g. std::string rendered vs just the buffer). 
So those are different.
So this is the discussion of, do we want to have these both in the MVP or have them in 2 differebnt milestones.

LI: so this level is useful for e.g. finding out basic things like whetgher you got to the right place, which branch, etc. 

PS: we have to start with something, could be just this

NF: it might be useful for our purposes to separate these even if we want both together to advertise something useful for users.

LI: Don’t know how we’d do the graphical rendering that visual debuggers do …[missed some bit of this]

BT: it is interesting to think how the debugger would display e.g. std string

LI: JetBrains API works well for a variety of languages, e.g. java and elixir
Could think about other things like microtasks, threads, etc. How do we tell browser that our langauge supports things like that, and have it display something useful for e.g. greenthreads.

BT: also IDEs have a bunch of knowledge about e.g. things like standard library types.

NF: e.g. in gdb all the pretty formatters are python code.

LI: we’d want basic stuff like folding, grouping, color

NF: we want to start with a common base and not the union

DS: display as separate from VM and debugger nodule

YG: for things like prettyprinting, the frontend is probably the better place

BT: for every lannguage that gets reimplemented?

DS: makes sense to have it in the debugger module but some UI entity would be calling it.

BT: could be 

NF: do we want to move forward on this PR?

YG: how binding is this if we land it? What’s the process for changing it? Some staged process like JS would be good

NF: yes its definitely not final. Basically looking for consensus that this is worth doing

LI: keep in this repo?

NF:

DS: doesn’t fit with existing CG process but could be similar.

NF: LLVM itself wouldn’t generate the module but rust/emscripten would

LI: how do we coordinate it?

NF: makes sense to commit the PR rather than leaving it open forever. Then we could have new PRs to make changes 

LI: would be nice to have some way to show the implementation status, to find out where the work is going on.

DS: we don’t have this currently for wasm CG.

<discussion about vendors keeping up with a doc linking to their inplementation status>


DS: makes sense to have a vote next meeting, in two weeks, for whether to officially adopt debugging modules for stage 0

LI: does this need to be broadcast to the larger group?

DS: don’t think it is necessary for every step, but could be polite for bigger things

AI: dschuff will put something ont he CG agenda, and will schedule the agenda for next debug  meeting to vote

NF: that’s it for this agenda

BT: the only other thing is the definition of our first MVP. we seem to have different ideas of what constitutes “viable”. My perspective was that this first milestone is that it wouldn’t be useful for a user to debugg their program.

NF: yeah maybe milestones is a good term, since it doesn’t imply user value and what they’d require. The things you called out are what I imagined as the 2nd milestone.

BT: should we define some milestones, like a roadmap?

NF: that makes sense. We also want to not try to unnecessarily sequentialize. But it does make sense to align it with the capabillities

LI: a roadmap of capabilities would be useful to help users who come to the repo to find out what’s going on.

PS: technical question> looking at the dwarf prototype. See that LLVM has a stack in memory, separate from the wasm stack.

(Discussion summary)
There needs to be extra info in debug info describing the linear stack, which global is the stack pointer, which local is the frame pointer in each function etc.
There is an out-of-tree LLVM patch for part of this.

For other languages they will need to keep different data (e.g. about greenthreads).
Only the VM has access to the real callstack. Currently emscripten and Rust are calling out to JS to get error().stack info for stack traces. Eventually it would be good to have an API in wasm to get this kind of info so it wouldn’t be necessary to go to JS. Probably the debugger module would use it since each language/platform would have a different ABI and different data.

