# Meeting notes for the April 30 video call of WebAssembly's debugging subgroup

- **Where**: zoom.us
- **When**: April 30, 11am-11:10 Pacific Standard Time (April 30, 6pm UTC, 8pm CET)
- **Location**: *link on calendar invite*
- **Contact**:
    - Name: Derek Schuff
    - Email: dschuff@google.com
    
## Notes:

* Paolo is working on finishing support in LLDB to debug wasm modules over the gdb-remote protocol (https://reviews.llvm.org/D78801)
There was some pushback on the architecture of the patch from the LLDB maintainers, Paolo is refactoring it a bit.

* Philip has landed the first iteration of the wasm symbol server in Chrome devtools (https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2157027)
It has support for breakpoints, listing variables, stepping. The dynamic parts like variable evauluation are still ongoing.

* Wouter is working on LLVM support for emitting debug info for stackified values. He made a prototype to update the debug_value
operands in the RegisterStackify pass, but that's brittle because other passes also sometimes create stackified values. Instead
we will try it just before WebAssemblyMCInstLower (it can't be done in MCInstLower directly because the AsmPrinter removes
things before MCInstLower gets to see them).
