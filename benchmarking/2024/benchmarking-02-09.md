![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the February 9th of WebAssembly's Benchmarking Subgroup

- **Where**: Google Meet
- **When**: February 9th, 4pm-4:45pm UTC (8am-8:45am PDT, 11am-11:45am EST)
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
    1. Logistics of this subgroup
    1. Current benchmarking related projects and a potential presentation of
       each.
1. Closure

## Attendees

* Saúl Cabrera
* Ben L. Titzer
* Andrew Brown
* Daniel Lehmann
* Marco Concetto Rudilosso
* Johnnie Birch
* Peter Penzin

## Meeting notes

### Logistics of this subgroup

SC: PR with notes templates is open

### Introduction of benchmarking projects

SC: A good next step is probably to make presentation about the various existing
benchmarking projects.

JB: Wasm Score. Built on top of Sightglass.

JB: Would it make sense to talk about Sightglass first?

AB: Would be good to have a joint presentation on sightglass. Is one of the goals to create a common benchmark suite?

BT: We created a charter that explicitly says that we won't do that. We should focus on recommendations and tools, but not necessarily a suite. Tools seem to be more important in this case.

AB: Agree that we shouldn't create a suite to rule them all. But sometimes it's easier to share a standard suite, for example when referencing papers in which people refer to performance results. 

JB: What would drive the agenda?  Good practices and understanding the lay of the land. What is that we'd try to produce. 

SC: What people are trying to measure, what things are missing currently, what to improve? I myself don’t have a great understanding of how/what to measure. There are different aspects of measuring - from compilers, hardware, etc

BT: For example, microbenchmark. IMO they have a lot of use and maybe we can think about how we are going to use micorbenches and what will we use them for: maybe measure teering or instantiation time etc. Also we should collect benchmarks together short of creating single authoritative suite.

DL: Interested in knowledge sharing and best practices. Also concrete workloads, but careful with producing a single score (which could be overfitted on). 

JB: Which is the vehicle for benchmarks? (e.g. the runtime). Maybe the benchmark has setjmp/longmp and needs to be supported by the runtime.

DL: Depends also on the host environment, e.g., V8 can rely on JavaScript. So necessarily won’t be a single suite for everywhere, but different subsets.

PP: Not every benchmark might apply everywhere, so depending on the context, you might want a different suite/engine. An interesting focus area is how to do things across different engines though.

AC: Some benchmarks could be domain specific. Real time embeddings for example are critical. 

DL: Should we start collecting current benchmark efforts in a list?

BT: There are different reasons: comparing hardware, comparing engines, comparing against native, or just even deciding if wasm would work for particular use case that you are interested in.

JB: It's important not to prescribe how the benchmarks should necessarily do or where they should run. It's context in most cases. 

PP: The hope is that we'd be able to piggyback on the current work that people are doing to point them in the right direction, depending on what they want to measure. 

BT: “Advice for the casual benchmarker”: like for example saying here are the things that you should do or shouldn't do. “You’re writing a microbenchmark? Here are some things to watch out for and maybe some reasons you see weird results.”

PP: There was a suite by Siemens (?) I don't have sources anymore. 

AC: Initially we did some latency analysis to look at Wasm in general, then we did some Wasm runtime analysis and then there's another effort to make these benchmarks more generic. 

PP: Can it be put on GitHub?

AC: GitHub not allowed, but it could maybe be shared. I'll check with Chris Woods. The newest effort is more refined and can probably do a presentation  about it. 

SC: for the next meeting, Johnnie, did you want to present wasmscore or do you want to convene with Andrew and Nick first

JB: we can talk about this offline

SC: I will check with you and then we’ll decide

AB: Let me talk with Nick and Johnnie and we will let you know

### Current benchmarking efforts
* JetStream 2 line items: https://browserbench.org/JetStream/in-depth.html 
* Some smaller/individual programs
* Sqlite3 speedtest1: https://www.sqlite.org/testing.html 
* libsodium: https://github.com/jedisct1/libsodium.js 
* Unity benchmark: https://blog.unity.com/engine-platform/webassembly-load-times-and-performance 
* PSPDFKit benchmark: https://pspdfkit.com/webassembly-benchmark/ 
* SPEC CPU / Browsix: https://www.usenix.org/system/files/atc19-jangda.pdf 
* Polybench
* Wish-you-were-fast: https://github.com/composablesys/wish-you-were-fast (titzer)
* Experiments from a couple Wizard papers (titzer)
* Sightglass: https://github.com/bytecodealliance/sightglass
* WasmScore: https://github.com/bytecodealliance/wasm-score 
* Wasm-R3: https://github.com/jakobgetz/wasm-r3
* Siemens benchmarking efforts (Ajay, Chris)
* Selected academic papers and how they benchmark Wasm
* Performance prediction using ML (Tianshu Huang)
* Lessons from benchmarking in other domains
* Java: DaCapo, SPECjbb, jolden, Renaissance
