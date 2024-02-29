![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the February 23rd of WebAssembly's Benchmarking Subgroup

- **Where**: Google Meet
- **When**: February 23rd, 4pm-4:45pm UTC (8am-8:45am PDT, 11am-11:45am EST)
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
    1. Sightglass Presentation (Andrew Brown + Nick Fitzgerald)
1. Proposals and discussions
1. Closure

## Attendees
* Andrew Brown
* Saúl Cabrera
* Ben L. Titzer
* Nick Fitzgerald
* Ashley Nelson
* Ajay Chhokra
* Johnnie Birch
* Rahul 



## Meeting notes


### Sightglass Presentation

Slides: https://docs.google.com/presentation/d/1NCBCZB1YfUnXtXwYQKXeoVf5_KkYhKBMbOXD1WCHVlU/edit	

AC: Do you consider different compilation flags? The compilation optimization makes a difference.

JB: Try to use consistent flags, but also try to consider all flags. Generally an open question. There hasn't been a deep study to determine the upper bound.

AC: This is what we (Siemens) did. Compare the fastest Wasm code. Having the best or the fastest as the upper bound makes sense. 

AB: Would love to hear more details from Siemens. No special care is taken to hyper-optimize the Wasm for benchmarks.

JB: WasmScore. Built on top of Sightglass. Not try to compare to other runtimes, but to compare Wasm <> Native; to understand how good the Wasm is.

AC: (Analyzing benchmarks) Do you use a real time kernel to minimize jitter?

NF: These are intended to be run on regular developer machines. That's why statistical rigor is important. 

BT: Great presentation. Might be able to repeat calls to `bench_{start, end}`.

NF: That would be nice. More boring/dev x could be how do you configure most of the options from the CLI (sightglass). How to keep Sightglass usable with good defaults vs surfacing multiple options that are overwhelming. 

AB: There are many knobs currently.

NF: If users are trying to compare multiple engines via Sightglass then caring about those knobs becomes more relevant.

BT: Have you thought about engines that do dynamic compilation (lazy compilation)? 

NF: Sightglass is not oriented for JITs that have complex tiers. Might not be impossible, but would require a different design. V8/SpiderMonkey were included in Sightglass, through some settings around forcing eager compilation. 

AB: V8, using turbofan directly without going through the baseline tier.

BT: Reasonable if you're interested in the cost of moving between tiers.


