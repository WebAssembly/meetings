![WebAssembly logo](/images/WebAssembly.png)

# WebAssembly meeting at W3C TPAC 2017
## (W3C Technical Plenary / Advisory Committee Meetings Week 2017)

- **Dates**: Monday-Tuesday November 6-7, 2017
- **Times**:
    - Monday - 8:00am to 6:00pm
    - Tuesday - 8:00am to 6:00pm
- **Location**:
  * Hyatt Regency San Francisco Airport; 1333 Bayshore Highway Burlingame, CA 94010
  * Sandpebble B, Lobby Level
- **Wifi**: TBD
- **Contact**:
    - Name: Brad Nelson
    - Phone: +1 650-214-2933
    - Email: bradnelson@google.com

## Logistics

Hosted by [W3C TPAC](https://www.w3.org/2017/11/TPAC/). See the site for details.

### Registration

Opens June 2017, see [TPAC page](https://www.w3.org/2017/11/TPAC/) for details.

### Hotels

See [TPAC page](https://www.w3.org/2017/11/TPAC/).

## Agenda items

### Day 1 : Monday, November 6th

#### 8:00am - 10:00am : Open Discussion

Swing by and talk about WebAssembly!
WebAssembly folks and others can discuss topics of interest.

#### 10:00am - 11:30am : WebAssembly Working Group Meeting

Official meeting of the WebAssembly Working Group.

1. Opening, welcome and roll call
    1. Opening of the meeting
    1. Introduction of attendees
    1. Host facilities, local logistics
1. Find volunteers for note taking
1. Adoption of the agenda
1. Approval of the minutes from last meeting
1. TPAC Welcome
   1. Welcome to TPAC (Brad Nelson).
       * [Code of Conduct](https://www.w3.org/Consortium/cepc/)
       * [Best Practices for Effective Meetings](https://www.w3.org/wiki/Meetings_Best_Practices_document)
       * [Speaker Guidelines](https://www.w3.org/wiki/Speaker_Resources#Speakers_Guidelines)
   1. Introduction of our W3C Team member [Eric Prud'hommeaux](https://www.w3.org/People/Eric/).
1. Proposals and discussions
   1. Discussion on increased coordination with other W3C Groups.
      * We'll talk about where we should be collaborating more with other groups,
        how we conduct outreach, and plan.
   1. Discussion on the status of the specification.
      1. [WebAssembly Core Specification](https://github.com/WebAssembly/spec)
      1. [WebAssembly JavaScript API](https://littledan.github.io/spec/document/js-api/)
      1. [WebAssembly Web API](https://littledan.github.io/spec/document/web/)
1. Closure

#### 11:00am - 11:30am : Proposals in Progress
Presenter: *Brad Nelson*

Brad will give a quick rundown of all current in-progress WebAssembly proposals.
We'll talk about where each is at in terms of our
[phases](http://github.com/WebAssembly/meetings/blob/master/process/phases.md)
and the obstacles each proposal faces.
[Slides](https://docs.google.com/presentation/d/1uRpS79-kAoL3EoC7IxrJFU5G7V-Sxno9pm9rVjC20yE/).

#### 11:30am - 12:30pm : WebAssembly Visits WebPerf

The Web Performance WG is discussing the
[Lifecycle API](https://github.com/spanicker/web-lifecycle/blob/master/README.md).

As modulating things like xCoin mining has bearing on WebAssembly,
our group should go to the WebPerf Room (Sandpebble C, Lobby Level).

#### 12:30am - 2:00pm : Lunch

Free-form mingling in the WebAssembly Room

#### 2:00pm - 3:00pm : WebAssembly from Above
Presenter: *Ben Titzer*

Ben will give a high level overview of WebAssembly.

#### 3:00pm - 3:30pm : Toolchains
Presenter: *Derek Schuff*

Emscripten is WebAssembly's toolchain.
Derek will give an introduction on how to use it, tips and tricks, and where it's going.

#### 3:30pm - 4:00pm : WPT

Discussion on Web Platform Tests.

#### 4:00pm - 5:00pm : Demos

Come see Demos of WebAssembly:
* Google Earth (preview) - Live demo only
* [WebDSP](https://d2jta7o2zej4pf.cloudfront.net/)
* [Construct3](https://editor.construct.net/)
* [Epic Zen Garden](https://s3.amazonaws.com/mozilla-games/ZenGarden/EpicZenGarden.html)
* [WebSight](https://websightjs.com/)
* [NASA Access Mars](https://accessmars.withgoogle.com/)

#### 5:00pm - 6:00pm : Open Discussion

WebAssembly folks and others can discuss topics of interest.


### Day 2 : Tuesday, November 7th

#### 9:00am - 10:00am : WebAudio + WebAssembly

WebAssembly and WebAudio WG folks to discuss future APIs, performance interactions, and avoiding garbage introduced by the API.

#### 11:00am - 12:00 : Exceptions and Control-flow in WebAssembly
Presenter + Moderator: *Heejin Ahn*
* Presentation on Control-flow in WebAssembly + current state of exceptions proposal. [Slides](https://docs.google.com/presentation/d/1bny3a9OFxDoJQpQXz_ZVN_bCqrTPNGEnotLaubyXrxY/edit?usp=sharing).
* Discussion

#### 12:00am - 2:00pm : Lunch

Free-form mingling in the WebAssembly Room

#### 2:00pm - 3:30pm : GPU for the Web Community Group
Presenter + Moderator: *Corentin Wallez*
* Presentation on WebGPU
* Discussion of WebGPU Topics, especially Wasm related ones:
    * Fast bindings for Web platform APIs (call overhead and GC-less render loop)
    * How to make the API interoperable between JS and WASM
    * Is the WASM host mapping buffers in the WASM module memory space a thing? (glMapBuffer equivalent)
    * Multithreading story for APIs
    * API extensibility in WASM (can't just add a dictionary entry like JS)
    *Any questions you might have!

#### 3:30pm - 4:00pm : Abusing WebAssembly
Moderator: *Brad Nelson*

Discussion on what bearing coin mining and other CPU abuse has on WebAssembly.
Follow up discussion of [Lifecycle API](https://github.com/spanicker/web-lifecycle/blob/master/README.md).

#### 4:00pm - 5:00pm : Host Bindings (JS + DOM) for WebAssembly
Presenter: *Brad Nelson*

WebAssembly currently in practice relies on a substantial amount of support from
JavaScript + Web APIs to be useful on the Web. Interoperability with JavaScript
and Web APIs will help make WebAssembly in practice more "of the Web"
while improving performance and ergonomics. Bindings for non-Web hosts embeddings are also relevant.

[Slides](https://docs.google.com/presentation/d/10vz6pldVOA8N3guv2jf4DCUujqz6jFmDnp37ax4SCc0/edit?usp=sharing).
[Proposal](https://github.com/WebAssembly/host-bindings/blob/master/proposals/host-bindings/Overview.md).

#### 5:00pm - 6:00pm : Open Discussion

WebAssembly folks and others can discuss topics of interest.

NOTE: Brad Nelson will be away presenting to the AC.


### Schedule constraints

## Dates and locations of future meetings

TBD

## Meeting Notes

###  Roll call

* Heejin Ahn
* Jacob Gravelle
* Mircea Trofin
* Eric Holk
* Thomas Nattestad
* Deepti Ganduluri
* Ben Titzer
* Derek Schuff
* Kenneth Cristiansen
* Mark Miller
* Alex Danillo
* Eric Prud'hommeaux
* Conrad Watt
* Limin Zhu

### Opening, welcome and roll call


### Find volunteers for note taking
Derek Schuff agrees to take notes.

### Adoption of the agenda
Eric Prud'hommeaux seconds.

### Approval of the minutes from last meeting
[https://github.com/WebAssembly/meetings/blob/master/2017/WG-10-23.md] 
Ben Titzer seconds

### TPAC Welcome


Welcome to TPAC (Brad Nelson).
* [Code of Conduct](https://www.w3.org/Consortium/cepc/)
If you are speaking, check out these best practices and speaker guidelines:
* [Best Practices for Effective Meetings](https://www.w3.org/wiki/Meetings_Best_Practices_document)
* [Speaker Guidelines](https://www.w3.org/wiki/Speaker_Resources#Speakers_Guidelines)

Great year for wasm, gone from being sort of a thing to shipping in all browsers. Lots of interest, and lots of proposals upcoming.

### Introduction of our W3C Team member [Eric Prud'hommeaux](https://www.w3.org/People/Eric/).

W3C has a process document which describes the roles. Mine is boring bookkeeping! We want a spec process that involves the community enough that people will actually follow it. It’s a blanket process that isn’t necessarily customized for wasm, but it works pretty well. The overall goal is to make the spec resilient, i.e. make it so everyone can implement it. My background/current skills involve JS frontend (and Node), clinical data, C++ libraries. 

### Proposals and discussions


#### Discussion on increased coordination with other W3C Groups.
 
* We'll talk about where we should be collaborating more with other groups, how we conduct outreach, and plan.

We are here! So let’s take advantage by visiting other groups and talking to folks in our room too. Best to check with the chair before sitting in on an official meeting (fit with their schedule, avoid disruption, etc).
Next door is Web Perf team, we will go visit them later.
Talking to a broad variety of folks can get us good ideas now rather than later.

#### Discussion on the status of the specification.


1. [WebAssembly Core Specification](https://github.com/WebAssembly/spec)
1. [WebAssembly JavaScript API](https://littledan.github.io/spec/document/JS.html)
1. [WebAssembly Web API](https://littledan.github.io/spec/document/web/)


Probably no real decision here in the absence of Dan and Andreas. Dan is interested in capturing the state of CSP. We talked about that last week at the CG meeting, but it’s still in flight. It might also be left for a future WG iteration.

EH: which specs?

BN: all 3: core spec, JS and web embeddings.

AD: what’s the plan to turn this from the CG format into a real W3-formatted spec? Those have lots of boilerplate. This still isn’t like those.

EP: We can paste that on the front. Good integration for bikeshed, etc

BN: the embedding specs are BS, but the core is ReST and we kind of like it that way being self-contained. 

EP: Can we fit it into a framework that can work?

AD: for a WG recommendation track doc, it has some requirements. So we need to figure out how to fit what we have into those.

BN: We are trying as much as possible to keep the CG in charge of the content. But WG can do reformatting, status section, etc

EP: Some are requirements for publication, some are for convenience. Question is whether the form can be dropped into BS, respec, etc where we can append the extra stuff.

LW: the hope was that the embedding docs could have the webIDL, links, etc.

P?: tradeoffs between the editors and publication process. Do what’s best for the editors, and tooling for publication

EP: also depends on how often we want to publish.

LW: can we put the boilerplate in our BS-based embedding spec and drop in the core spec as a component inside?

Discussion ... maybe? Is the JS-rendered math markup a problem?

P: we’ve done this on other specs, it is possible to include the JS in the published HTML.

KC: Media Capture Depth Stream Extension spec has JS rendering

P: How often do we want to publish?

BN: twice a year?

... We can publish what we have as a working draft. Best to start the patent clocks ASAP
How much iteration do we want after?
We should have a pipeline to automatically publish as much as possible.

EP: what about the opposite? Doc which just points to editor’s draft.

P: could do that too. Mostly a matter of taste.

BN to follow up with EP on tooling to satisfy the publication rules.

BN: process to kick off public working draft?

EP: add document status, ask for the right short name for spec, warn the lawyers

Plan is to start in 2 weeks at next WG meeting.

EP: also possible to let the editors push the button to publish new working drafts.

### Closure

End of agenda!
Motion to close: let’s get coffee
DS enthusiastically seconds

## WebAssembly Meeting with WebAudio

WebAudio folks came by.
They demoed a synthesizer built with WebAssembly.
It inlines the wasm bytes as javascript text, converts it to an ArrayBuffer and instantiates the module.
This is because WebAudio worklets cannot use fetch.

We discussed the current WebAudio worklet proposal.
The desire to load wasm more directly was discussed.
Eventually when wasm gets ES6 modules support, an import of wasm code would be allowed.

The current api provides buffers to the user application.
We discussed a bring-your-own buffer API that would avoid the need to copy audio data in and out of the WebAssembly heap.
A protocol to allow WebAudio to request new buffers would be required. Ideally this would allow the main callback for samples to have no arguments, avoiding any chance of a GC.

We talked about if worklets are part of the same Agent Cluster as the rest of the page.
Link from Domenic to issue discussing this:
https://github.com/w3c/css-houdini-drafts/issues/224

We discussed using the Worklet MessageChannel to pass a SharedArrayBuffer (probably WebAssembly.Memory) / WebAssembly.Module to the worklet.
This would allow fetching to happen outside the worklet.

We discussed whether 32-bit floats are still a problem. Consensus was that with this new API, most of the historical issue with larger sample sizes can be worked around.

The general sense was:
* The current API will work fairly well for now, with the use of a MessageChannel.
* It can be later improved with bring-your-own buffer.
* Hosting Bindings might help, but if care is applied won't be blocking.

## Efficient XML Interchange

Representative from Efficient XML Interface EXI WG visited.
Recommended we learn more about their compression format.

AI: Add a github issue linking to their spec.

## WebGPU CG & WebAssembly

Presentation & Discussion
[NOTES](https://lists.w3.org/Archives/Public/public-gpu/2017Nov/0001.html)
