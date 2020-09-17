# Meeting notes for the July 23 video call of WebAssembly's debugging subgroup

- **Where**: zoom.us
- **When**: July 23, 11am-11:30 Pacific Daylight Time (July 23, 6pm UTC, 8pm CEST)
- **Location**: *link on calendar invite*
- **Contact**:
    - Name: Derek Schuff
    - Email: dschuff@google.com
    
## Notes 

* (these are summaries from memory rather than direct transcription: errors are solely Derek's fault)

* Luke Imhoff: There's been some discussion in the broader CG about 2-phase unwinding, for which debugging is a major motivator.
There's also been some discussion about how toolchains might represent the unwinding information (which is related to the debug info).
Those folks didn't seem very aware of the stuff we are discussing here. Should we maybe make some kind of presentation in the CG or some
other way to update them?

* Derek Schuff: Seems like a good idea. There are definitely 2 competing visions for how the platform capability for 2-phase unwinding
and related capabilities will work. I think either one of those could work with what we've done for the DWARF ecosystem so far. 

* Yury Delendik: Our flavor of DWARF is only concerned with describing source-level constructs.

* DS: Right, in ELF, some of that same unwind-table data is used by libunwind to actually drive the stack unwinding, but we don't
use that in wasm. So our DWARF is less tightly-coupled than it is in ELF. I agree that most of the stuff under disagreement is pretty
orthogonal to what we have.

* LI: I'm a bit concerned about the disagreement more generally since these overall schemes seem to be a blocker for the thing we really want
for Erlang, which is stack switching.

* DS: Yeah, that's definitely part of the different visions, and it would work differently in each.
I guess one interesting difference is that Ross's version also includes a way for frames to opt-in to expose locals to a stack walker.
We've been assuming the debugger gets special APIs out-of-band to expose locals, but using marking could allow implementing a debugger
in user code.

* Wouter Van Oortmerssen: Yes, or you could even imagine not using a heavyweight interactive debugger, but just having a library that
walks the stack and formats and dumps all the information about the stack and its contents, and saves it somewhere, to allow manual inspection.

* DS: Yeah, that's similar to what you might want for more comprehensive crash dumping as well. So that might be an advantage of that kind of
scheme.

* DS: Unrelated: we've gotten reports of missing debug info in optimized builds. It would be good to get some reproducers for that so we can
find out if it's happening in LLVM IR, or in the wasm backend, or in Binaryen

* Paolo Severini: I saw it at least once where it was before Binaryen.


* DS -> Action item to prepare some kind of summary of how we are doing 
* PS (and/or Philip Pfaffe?) -> Action item to (eventually) send a reproducer of missing debuginfo.
