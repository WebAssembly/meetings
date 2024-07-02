![WebAssembly logo](/images/WebAssembly.png)

## Agenda for June 28th of WebAssembly's Benchmarking Subgroup

- **Where**: Google Meet
- **When**: June 28th, 4pm-4:45pm UTC (8am-8:45am PDT, 11am-11:45am EST)
- **Location**: _Link on calendar invite_
- **Contact**:
    - Name: Petr Penzin, Saúl Cabrera
    - Email: penzin.dev@gmail.com, saul.cabrera@shopify.com


### Registration

If this is your first time attending, please [fill out the registration form](https://forms.gle/QCmhyM4QwvWvZR9b8) to receive an invite.

The meeting is open to CG members only. You can [join the CG here](https://www.w3.org/community/webassembly/).

### Logistics

This meeting will be a Google Meet video conference.

## Agenda items

1. Opening, welcome and roll call
    1. Please help add your name to the meeting notes
    1. Please help take notes.
1. Announcements
1. Proposals and discussions
    1. Wasm R3: Record Reduce and Replay for Realistic and Standalone
       WebAssembly Benchmarks (Doehyun Baek)
1. Closure

## Meeting notes

### Attendees

- Andrew Brown
- Benjamin Titzer
- Daniel Lehmann
- Doehyun Baek
- Johnnie Birch
- Petr Penzin
- Tom An

### Notes

DB presenting {Wasm-R3}(https://docs.google.com/presentation/d/1Ai8R_yZ-_EDE10I_FItXI8ggPQ96U_1Lzve_Jfm5KPU/edit?usp=sharing)

AB: How to understand the slide on replay overhead - is the proportion comparing to original run time

BT & DB: Grey portion is the original application execution, red is the overhead, total wall clock is not necessarily the same

AB: Can I see what is the ratio between original and instrumented runtime from this chart?

DB: No, and it is quite hard to judge that given the set up required

BT: Because there is a whole Web app driving the Wasm execution, it’s not possible to know that level of detail. Keep in mind that the replay functions are simulating the Web event loop and driving Wasm execution frame by frame.

DB Showing a live demo, funkykarts

AB: How large is the trace file?

DB: In this case it is 33 MB, but it can be large, and we can run the same instrumentation on WebKit, Chromium, and Firefox

JB: What are you doing with those files?

DB: Captured replay trace is used to replace interactions with imports, which is added to the unchanged code of the original module.

JB: Can this be used to identify hot spots?

DB: We are preserving original code, it would exhibit original behvior

PP: I think this is useful for debugging in general

JB: How does this work for code that has host dependencies?

DB: We only record changes to observable state of Wasm but not where that is coming from.

BT: Recording detects changes by comparing externally visible state with a private copy, that is the level of detail it captures.

AB: How to tell how much time replay functionality is taking vs original code?

DB: We used Wizard’s functionality for tracking cycles counts and annotated replay functions, this would be engine-specific.

AB: meaning we need to profile running replay?

DB: yes

BT: There is also machine cycles vs wasm instruction count. We are also working on static optimizations to improve replay.

AB: How much standalone engines care about running apps that are recorded on the Web?

BT: This would work on any host environment in terms of both recording and replaying

PP: This would be a good way to check how code that already runs in one environment would behave in another one 

BT: Also useful for applying optimizations to Wasm execution only (in engines)

AB: Still wondering how creating a corpus of these benchmark would work across different environments

PP: For example the video game demo when stripped of all the graphics is just compute, which is basic physics, I think this is useful to run in any engine

DB: code repo: https://github.com/jakobgetz/wasm-r3
