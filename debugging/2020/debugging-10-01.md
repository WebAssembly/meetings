# Meeting notes for the October 1 video call of WebAssembly's debugging subgroup

- **Where**: zoom.us
- **When**: October 1, 11am-11:30 Pacific Daylight Time (July 23, 6pm UTC, 8pm CEST)
- **Location**: *link on calendar invite*
- **Contact**:
    - Name: Derek Schuff
    - Email: dschuff@google.com
    
## Attendees
Luke Imhoff, Philip Pfaffe, Derek Schuff, Paolo Severini, Wouter Van Oortmerssen, Alon Zakai 

## Notes 

DS: Zoom now requires either a password or a waiting room (or both) on all meetings (currently we use neither). 
Going without a waiting room is convenient because people can join before the host (or meet without the host),
so it might be better to add a password, and update the calendar invite to use a URL which embeds the password
(that way people won't actually have to type it). **I'll update the invitation with a new meeting URL**, please let me know if you don't
get a notification.

DS: Update on debug info in LLVM. The initial patch for split-dwarf (aka dwarf fission, aka -gsplit-dwarf)
is landed in LLVM. Based on initial basic testing, it seems to work, and is hopefully ready to experiment
with in a debugger. I also found out about Type Units (aka [debug types sections](https://fedoraproject.org/wiki/Features/DebugTypesSections),
aka -fdebug-types-section), which moves type information from .debug_info into an ELF COMDAT, allowing
the linker to deduplicate it. I experimented with a Linux build of Clang and found it reduced debug
info size by ~40%, so it seemed worth investigating. Since wasm comdats work like ELF, we could try it
for wasm. I uploaded a [patch](https://reviews.llvm.org/D88603) to enable it for wasm.
Question: do we know whether lldb supports it out-of-the-box?

PS: I can check on that

DS: I'm also curious why it's not just the default on Linux. Maybe because it slows down linking?
(the above link does seem to indicate that Fedora enabled it for all of their debuginfo packages)

Other discussion:
LI: Is anyone attending the virtual LLVM developer meeting? (DS is). I'm interested in the tutorials.
Mostly for Elixir when we use LLVM we end up jsut looking for prior solutions 
to the partiucular problem we're looking to solve, but sometimes we find e.g. a completely different
API that we didn't know about, or violate some assumption about the IR further down the pipeline and
don't always know how to deal with it.

DS: are you using the C or C++ API?

LI: we were using a Rust wrapper, but the maintainer had trouble keeping up with LLVM's API churn.
Now we mostly use the C++ APIj.

DS: Yeah, the C++ API makes no attempt to be stable, but always has full functionality, whereas
the C API has sort of best-effort stability but sometimes lags behind.
