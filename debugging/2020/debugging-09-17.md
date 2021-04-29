# Meeting notes for the September 17 video call of WebAssembly's debugging subgroup

- **Where**: zoom.us
- **When**: September 17, 11am-11:30 Pacific Daylight Time (July 23, 6pm UTC, 8pm CEST)
- **Location**: *link on calendar invite*
- **Contact**:
    - Name: Derek Schuff
    - Email: dschuff@google.com
    
## Attendees
Yury Delendik, Luke Imhoff, Philip Pfaffe, Derek Schuff, Paolo Severini, Wouter Van Oortmerssen, Alon Zakai 

## Notes 


* DS: I'm about to land the first patch for split-dwarf in LLVM. Haven’t tested the contents against any debugger code yet, just checks that it gets the right sections. I also asked for some advice from llvm-dev about the best approach (e.g. old-school gcc dwarf fission vs the dwarf 5 version, etc). Haven’t heard back yet.

* AZ: in emscripten we now don’t run binaryen in O0 and O1 in simple cases (e.g. when using bigint, not using setjmp, etc). Useful for speeding up linking in any case, and also needed for split-dwarf (since binaryen doesn’t support split-dwarf and it would be nice if it didn’t have to).

* PS: have we talked about crash dumps or postmortem debugging?

[the following is DS’s “post-mortem” summary of the discussion]

Currently the VM can give us backtraces with module offsets, which the LLVM tools (e.g. addr2line) are able to turn into line information. We can also get the state of any exported globals and linear memory from JS (e.g. on trap). But we don’t have a way to get information about locals at runtime.
We need a way to get local state from the VM programmatically. In general this is a challenge, as current VMs (V8 and SM at least) track this local information in the baseline but not the optimizing compiler. (And there has been resistance from implementers to doing all this tracking at the top tier). So for general production use (i.e. postmortem debugging of production builds and runs) this is going to be a challenge. Probably for now there’s going to have to be some way for a build/run to “opt-in” to this bookkeeping at some cost.


Since the baseline compilers do keep track of all of the locals, we could have some way to ask the browser to only use the baseline tier (a la the compilation hints proposal idea that was floated in the past), and then also specify some API either in wasm or in the embedder (e.g. JS) to have the VM walk the stack and provide all the local values. You’d probably also still need a way to handle a trap that’s more flexible than the current one (i.e. turning it into a JS exception after the wasm frames have all unwound).  The result could be in the embedding, or it could even have the VM write the information into wasm linear memory to be collected by wasm code.

The stack walking spec proposal might be another way to do this. It allows specifying which variables to make available and a way to walk the stack in wasm and get those values. If we could launch a stack-walk e.g. when a trap or some other event occurs, then we could just opt all locals into being tracked, and we could could write stack-walk to collect their values at crash time. Debugging in general is a use case we should advocate for in the stack-walking discussions in the new stack walking subgroup.
