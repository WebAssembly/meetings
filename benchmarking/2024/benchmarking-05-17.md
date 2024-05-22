![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the May 17th of WebAssembly's Benchmarking Subgroup

- **Where**: Google Meet
- **When**: May 17th, 4pm-4:45pm UTC (8am-8:45am PDT, 11am-11:45am EST)
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
    1. PERFWUME: A model based toolchain for evaluating performance of wasm runtimes, Ajay Chhokra (Siemens)
1. Closure

## Attendees
* Ajay Chokkra
* Andrew Brown
* Ayako Akasaka
* Doehyun Baek
* Jhonnie Birch
* Saúl Cabrera

## Meeting notes

###  PERFWUME: A model based toolchain for evaluating performance of wasm runtimes

[slides](./perfwume.pdf)


JB: What contributes to jitter? Is it latency or performance?

AC: Context switching was contributing to jitter. 

JB: Is there any difference if you were running native?

AC: The jitter observed was very similar in both native and Wasm.

JB: Are there any plans on open sourcing the work done as part of this
toolchain?

AC: Study A is already open source. It doesn't exist in a GitHub repository, it's a zip file. Other studies are not open and need approval.

AB: Each experiment is a complex row. One of the slides is using a very specific WASI-SDK and a different version of wasm-opt. All those variables matter and make the benchmarking more complex. 

AC: The last study is taking care of ensuring that the toolchains versions are controlled.

DB: Different wasm-opt versions might impact performance, as pointed by Adrew. Has anyone experienced performance differences between wasm-opt versions?

AB: Hasn't experienced performance differences, but sometimes in different versions different sizes are observed.




