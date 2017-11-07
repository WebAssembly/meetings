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
      1. [WebAssembly JavaScript API](https://littledan.github.io/spec/document/JS.html)
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

Discussion on what bearing coing mining and other CPU abuse has on WebAssembly.
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

## Meeting notes

Notes added here after the meeting.
