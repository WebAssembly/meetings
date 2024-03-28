![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the March 22nd of WebAssembly's Benchmarking Subgroup

- **Where**: Google Meet
- **When**: March 22nd, 4pm-4:45pm UTC (8am-8:45am PDT, 11am-11:45am EST)
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
    1. wish-you-were-fast presentation, Ben Titzer
1. Closure

## Attendees

* Ajay Chhokra
* Andrew Brown
* Benjamin Titzer
* Daniel Lehmann
* Johnnie Birch
* Nick Fitzgerald
* Marco Rudilosso
* Petr Penzin
* Saúl Cabrera

## Meeting notes

###  Wish you were fast (Ben L. Titzer)

Slides: https://docs.google.com/presentation/d/18avQJS6ZUt-3du53dF8AeHlQ0SKPyRHncVQ7PRbc-ho/edit?usp=sharing_eil_se_dm&ts=65fd9e57

NF: What kind of ABI are required to drop in a Wasm to the service?

BT: Almost nothing, mostly command arguments. For the Web engines, I wrote a JS wrapper to get the environment setup to be able to run them in the Web engines. 

AC: Do you impose any kind of restrictions on the Wasm? Can you talk a little bit about how to integrate this into a CI pipeline?

BT: Through bash scripts, mostly. It's open source but not polished. In the wish-you-were-fast repo, you can take a look at the structure and that would give you an idea of how to integrate this in a CI environment for example. 

AC: How do you display results?

BT: If you just run, it'll just run the program. To display the benchmark results, you need wrappers around them that display the time taken for each benchmark. That wrapper will dump the results and some other script will consume that data and generate a report. Three tier web app and wrapper from JIT paper are in the repo.

NF: You separated out compilation and execution. Did you measure instantiation?

BT: I didn't. Only compilation and execution. Metrics are defined in the DB schema in the repository, it would be possible to add more metrics there.

NF: Most of the work that we've done in Wasmtime, has been on instantiation for horizontal scaling. I think it's worth mentioning that instantiation is important in some scenarios. 

BT: In the repo there is a script to reisntatntiate multiple times. It is possible to measure multiple instantiation within this approach.

DL (in chat): Very cool work! Uploading your own benchmark would be amazing.
Could one also extract benchmark-specific metrics, e.g., coremark outputs some throughput measure (iterations/s or fps or whatever)?

NF: It's also important to consider for non Web engines the instantiation time. Some single core instantiation optimizations make it worse on multiple threads.

AB: We might be running into a problem here in the future. A lot of benchmarks that you can compile and run easily because they rely on a preview1 ABI that's simple to work with might present a roadblock because of WASI versions, right now some people are compiling to preview2, which is more complex to easily compile and benchmark. 

NF: With tools like JCO you can transpile and polyfill preview2 programs for the web. 

AB: Just expressing the worry that it would be hard to compare newer API to older.

PP: The component model has its own memory management story. So the point that Andrew brings up is an excellent question.

BT: Replaying modules that have an interaction with the host might alleviate the worry around preview2. It seems promising in the sense that benchmarks won't need to know too much about the host. But there are overall ecosystem challenges with preview 2 adoption because of the diversity of engines.

BT (responding to DL question in chat) it is good for programs to report their own metrics.

DL (in chat): Right, I saw the coremark-5000 variants, so you fixed the iteration count_
?

BT: people should stop measuring time which adjusting iteration count, because it interacts with garbage collection and other system features, I think we should encourage people to fix the amount of work per iteration

DL (in chat): I think Coremark tries to adjust its iteration count to the execution speed, right?

BT: Yes, that is why we stopped using coremark.

AB: Back to the replay technique: you'd be able to capture any type of host-calls?

BT: Right.

AB: Then we just respond to those host calls similar to what the host responded to, in Wasm?

BT: Yes. 

DL (in chat): Ben, at some point we/you/the collaborators could present the record/repay thing here

AB: In sightglass, everything related to WASI lives outside the measurements. 

BT: We are planning to present the replay technique here soon, but are still working on the paper.
