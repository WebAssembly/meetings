![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the March 8th of WebAssembly's Benchmarking Subgroup

- **Where**: Google Meet
- **When**: March 8th, 4pm-4:45pm UTC (8am-8:45am PDT, 11am-11:45am EST)
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
    1. WasmScore Presentation (Johnnie Birch)
1. Proposals and discussions
1. Closure

## Attendees

* Ajay Chhokra
* Andrew Brown
* Ashley Nelson
* Daniel Lehmann
* Johnnie Birch
* Marco Rudilosso
* Nick Fitzgerald
* Petr Penzin
* Saúl Cabrera




## Meeting notes

### WasmScore presentation (Johnnie Birch)

JB presenting [slides](./wasm-score-slides.pdf)

AB (In chat): Johnnie, if you're looking for an easy way to capture hashes of various Sightglass things, including benchmarks, you might be interested in: sightglass-cli fingerprint --kind benchmark|engine|machine

PP: Is the time column  in seconds?

JB: The time column is taking the time and producing an average based on geomean.

PP: Is the geomean is suite or test based?

JB: Crypto is a suite, with N benchmarks inside it, and the efficiency is calculated per test, and then an average is calculated for all the calculated efficiencies.

PP: The score is normalized on the maximum time?

JB: There's no maximum.

JB: There are two scores: efficiency, which can't be greater than 1 and execution time which is the inverse of time 1/time (higher is better). This is done to make it consistent. 

PP: What do you mean by 1/time, is time in seconds? Would that mean that time less than 1 second then score is greater than 1 and less than one otherwise?

JB: Moving on for now. Major point: higher means the score is better and to avoid inconsistency issues.

MR (in chat): is it a bit like iterations per second?

AC (in chat): Do you consider AOT and JIT modes?

PP (in chat): There is also an output for instantiation/compilation/execution - I am wondering if that is memory footprint?

MR: Is the score iterations per second, as in how many time it can execute X per second?

JB: Great point, however this benchmark doesn’t take this into account.

JB (re AC question): it only does the default that wasmtime support, it doesn’t take AOT vs JIT into account. You can compare SIMD vs native, there can be multiple ways to provide scores.

AC: how difficult it would be to change underlying runtime?

JB: Sightglass 1.0 supported different engines, Sightglass 2.0 only supports wasmtime. There are different use cases for different engines.

PP: Right now ti only supports wasmtime?

JB: Only what sightglass supports, currently it is wasmtime

PP: Paraphrasing the Ajay’s question one more time, what would it take to get back to using other engines?

JB: I never officially upstreamed that.

AB: This draft PR might provide an idea of what that would take: https://github.com/bytecodealliance/sightglass/pull/166

AB: Johnnie, check out my chat comment about fingerprinting.




