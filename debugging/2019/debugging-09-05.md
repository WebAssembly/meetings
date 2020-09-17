## Agenda for the September 5 video call of WebAssembly's debugging subgroup

- **Where**: zoom.us
- **When**: September 5, 6pm-7pm UTC (September 5, 11am-12pm Pacific Daylight Time, 8pm-9pm CEST)
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
2. DWARF and Wasm


## Meeting Notes

# Attendees

- Yang Guo
- Paolo Severini
- Derek Schuff
- Nick Fitzgerald
- Yury Delendik
- Bill Ticehurst
- Till Schneidereit
- Eric Leese
- Philip Pfaffe
- Z Nguyen Huu
- Deepti Gandluri
- Luke Imhoff

Yury has prototype of DWARF w/ extensions to encode wasm locals.
Patch posted upstream for LLVM but questions about approach, not landed yet

Paolo also using this patch for debugging wasm running in v8 from lldb

Alternative suggestion from adrian on llvm review was to reuse a different target’s expression type, seems like a big stretch.

Philip Pfaffe and Eric Leese are going to work on Wasm debugging on v8 for google

BT: any progress in other areas?

YG: Ingvar (RReverser) worked on a Rust tool to extract DWARF from wasm binary for making source maps. Based on Gimli

PS: have done something similar

BT: do we want to base the work on this:

PS: it’s pretty rough, maybe not


NF: update on Interface work: working on some webIDL interfaces. It’s almost ready to share. Should I do that in the form of a PR to the repo?

DS: yes

BT: how far along is the wasmtime work?

YD: it only support what we output in wasm dwarf today, and converts it into native dwarf. So it has the same gaps that wasm dwarf has

BT: does it use a separate wasm debug module concept?

YD: no, it just does everything at JIT time and registers the module with the debugger

BT: Nick’s design would be the debug module API, but that’s not part of this prototype
Right.

NF: this is more for people who are AOT compiling their library into a native lib/executable, who want to work with native tools that expect native dwarf. The APIs assume a situation where theres’a runtime that has its own tools that want to support source-level debugging.

BT: Paolo’s design the target wasm engine would expose the lldb interface

PS: or expose the debugger directly.

BT: at LLDB level you talk at the wasm layer.
But these are sort of separate parallel tracks?

TS: in some sense yses. For wasmtime we focuse on the debug info and extending the DWARF for wasm, and make wasmtime interpret that. Whether we’d keep that, we’ll see. It wouldn’t work for every case (e.g. a system like Mono). But we’ll need the debug format in any case. So this is a subset of what we need anyway. Bundling LLDB as a debug server on the side would still need a debug format, which could be the dwarf extension.

BT: this demo only works with interpreted wasm. If we JIT the engine has to track a lot more.

YG: currently the plan is an interpreter PoC first. For V8 weve talked about also adding debugging support in Liftoff, which is simple enough that there’s still 1:1 mappings for things like stack slots, so it could have the same set of features.

BT: so that’s nice that we woudln’t have to run things in an altenate mode or something

YG: yes. Turbofan would be much harder, to track everythign through the optimizations.

BT: so you’d have to fall back to the baseline for those.

YG:yes. Turbofan does smater regalloc

NF: that makes a lot of sense for recovering variables, scopes, etc. IDeally you should be able to access line table info anyway, even for e.g. the profiler.

YG: yeah line table info tracking is easier, that could be done.
BT: we can’t deopt, right? So we’d have to reload the wasm to debug it?

YG: right, for wasm. For JS we do have to be able to deopt so we have a way to do that for debugging too. But not for wasm; its unlikely because it would only be used for debugging.

YG: my understanding is that cranelift tracks the source info through to optimized code already?

YD: yes

BT: would you have it on by default? There must be a cost to that?

YD: hard to say currently. The code is not super optimized in any case yet, but it’s acceptable so far.

BT: are there things we need to agree on further in this group, in terms of standards?

YG: so far it seems that we are wanting to keep up

DS: one issue is API vs protocol, there was some reaction to that 

YG: the main thing is that we want the debugger out of process. We used to have it directly in the JS process but it caused 
a lot of issues. Once you move out of process, message-passing is easier than an API

NF: that could be an impl detail. You could have message-passing under the hood behind the API

YG: true, they could wrap.

PS: we could have 2 protocols: one higher-level exposed by the debugger module (could be an API). the way to talk to the debugee in the runtime. In my prototype that’s the low-level LLDB protocol. It’s a detail.

YG: that could make sense.

NF: I’m not sure we want to standardize 2 protocols.

PS: we might need to make some wasm-specific changes to the protocol but it wouldn’t necessarily have to be a new protocol, or standardized.

NF: the other thing about apis vs wire protocols is that as soon as we talk about wire protocol we have to talk about bytes, serialization, how to extend, etc. that question is easier with interfaces. If things can be impl details, it’s easier not to standardize them.

BT: you’d want protocols to be able to talk to multiple engines. I you define it as an interface how do you avoid specifying formats?

YG: you could just have a JS function interface

PS: do you want the debug module in the engine or in the program?

YG: []

DS: non-JS?

NF: definition would be in interface types eventually, not webIDL. We should also move DWARF doc into debugging repo

NF: other document this group should take responsibility of is the DWARF & Wasm document

BT: DWARF&Wasm doc is almost an appendix

DS: we make similar separation between conventions and standards in tools-conventions repo

TS: do MS have plans to extend PDB for wasm?

BT: no plans that I know of; don’t know what blazor team does

LI: related to blazor/mono question: Erlang/elixir just released our compiler. We’d like to debug the runtime and generated code. The runtime is in Rust, and the erlang is on top of LLVM. 
Blazor proxies the CDP

NF: we probably don’t want to worry about debugging interpreted code for the MVP

DS: you said you compile erlang to llvm ir; do you statically link that with your rust runtime code?

LI: yes

DS: if you generate llvm debug info for the erlang-generated llvm ir, then llvm should handle the linking of debug info for you and it should Just Work
Post-compile tools are breaking the debug info, its something they need to fix.

LI: we are very interested in the debugger module proposal because our language is so different from C

YD: lld can link any object file that has wasm dwarf, so you could link them and get DWARF

LI: we are interested in browser having similar UI for debugging wasm compared to JS

NF: that’s certainly something we want to eventually have.

AI: for moving the DWARF doc from the tool-conventions repo to the debugging repo. (there is an open issue but not a PR).

BT: there’s nothing for the API yet.

NF: I’ll put something there when I’m ready

BT: do we want MVP goals or scenarios we want to capture there?

NF: good to file an issue and hopefully come to an agreement about that next meeting. Previously we had discussed source-level stepping first, before doing scopes, vars, etc

BT: sounds good to capture that. I guess things like implentation details don’t necessarily need to be in standards

BT will open issue for dicussion on MVP. NF will open one when he has a proposal for API

LI: it would be great to have a link to flags and other implementations for people to try

DS: yeah, something like we have in the CG

LI: it would be good to have actual flags or instructions to make it easy to try


