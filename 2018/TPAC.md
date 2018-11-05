![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the October meeting of WebAssembly's Community Group

- **Host**: W3 TPAC, Lyon, France
- **Dates**: Thursday-Friday October 25-26, 2018
- **Times**:
    - Thursday - 9:30am to 5:00pm
    - Friday - 9:00am to 5:00pm
- **Location**:
    - Cité Centre de Congrès de Lyon
    - 50, quai Charles de Gaulle
    - 69463 Lyon Cedex 06
    - France
- **Wifi**: TBD
- **Dinner**: TBD

- **Contact**:
    - Name: Ben Smith
    - Email: binji@google.com


## Registration

Full information for TPAC is available at https://www.w3.org/2018/10/TPAC/,
including registration, fees, venue, transporation information, accommodations,
etc.

## Agenda items

To attend, you must [complete the TPAC registration](https://www.w3.org/2018/10/TPAC/#registration), pay the registration fees, and be a Community Group member. You do not need to be a Working Group member to attend.

* Thursday - October 25th
    1. Opening, welcome and roll call
        1. Opening of the meeting
        1. Introduction of attendees
        1. Host facilities, local logistics
    1. Find volunteers for note taking
    1. Adoption of the agenda
    1. Proposals and discussions
       1. [Multiple values](https://github.com/WebAssembly/multi-value) (Andreas Rossberg)
          - quick status update
          - 15 min
       1. [Tail calls](https://github.com/WebAssembly/tail-call) (Andreas Rossberg)
          - status update, resolution of open issues
          - poll: advance to stage 3?
          - 30 min
       1. [C/C++ API](https://github.com/rossberg/wasm-c-api) (Andreas Rossberg)
          - new proposal presentation
          - poll: advance to stage 1?
          - 30 min
       1. [Bulk Memory Operations](https://github.com/WebAssembly/bulk-memory-operations) (Ben Smith)
          - poll: advance to stage 2?
          - 30 min
       1. [Threads](https://github.com/WebAssembly/threads) (Ben Smith, Andreas Rossberg, Conrad Watt)
          - Update on memory model and spec
          - [Race between memory.grow and access](https://github.com/WebAssembly/threads/issues/26#issuecomment-424742576)
          - 1 hour
       1. [WebAssembly Content-Security-Policy](https://github.com/WebAssembly/content-security-policy) (Ben Titzer)
          - [How does CSP affect postMessaging of modules](https://github.com/WebAssembly/content-security-policy/pull/16)
          - 30-60 min
       1. [WebAssembly Spec Update](https://github.com/WebAssembly/spec) (Ben Smith)
          - 15 min
    1. Adjourn
* Friday - October 26th
    1. Opening, welcome and roll call
        1. Opening of the meeting
        1. Introduction of attendees
        1. Host facilities, local logistics
    1. Find volunteers for note taking
    1. Adoption of the agenda
    1. Proposals and discussions
       1. [Exception handling](https://github.com/WebAssembly/exception-handling) (Ben Titzer)
          - 1 hour
       1. [JS BigInt to WebAssembly i64 Integration](https://github.com/WebAssembly/JS-BigInt-integration) (Dan Ehrenberg)
          - 15 min
       1. [ES6 Module Integration](https://github.com/WebAssembly/esm-integration) (Dan Ehrenberg)
          - 30 min (slides: https://docs.google.com/presentation/d/1KleWN1nni_sKpPMLxC_R2tBTdozdrtJhEX7_ZWZztto)
       1. [Reference types](https://github.com/WebAssembly/reference-types) (Andreas Rossberg)
          - quick status update
          - 15 min
       1. [Host Bindings](https://github.com/WebAssembly/host-bindings) (Luke Wagner)
          - [Slides](https://docs.google.com/presentation/d/1ciUHPjNdD3-OGqDjYGNI_Uqod8y3yQOVOnKI3urr2v0)
          - Recap developments since TPAC last year: factoring out the Reference Types proposal
          - Short browser update on any browser implementation progress toward Reference Types
          - Presentation: Given Reference Types, what's left for Host Bindings to do?
          - Poll: Rename "Host Bindings" to something less abstract better capturing its purpose?
          - Poll: Define a Reference Types + Host Bindings milestone based on removing JS glue from wasm&rarr;WebIDL calls?
          - Discussion: Best way for C++ to utilize this milestone?  (c.f. [Rust's wasm-bindgen](https://fitzgen.github.io/wasm-cg-wasm-bindgen))
          - 1+ hour?
       1. [Garbage collection](https://github.com/WebAssembly/gc) (Andreas Rossberg)
          - overview of current MVP proposal
          - 1+ hour?
    1. Closure

## Meeting notes

### Opening, welcome and roll call

#### Opening of the meeting

#### Introduction of attendees

* Adam Klein
* Alex Crichton
* Andreas Rossberg
* Ben Bouvier
* Ben Smith
* Ben Titzer
* Boris Zbarsky
* Conrad Watt
* Dan Ehrenberg
* Deepti Gandluri
* Joachim Breitner
* Julian Seward
* Keith Miller
* Lars Hansen
* Limin Zhu
* Lin Clark
* Luke Wagner
* Michael Holman
* Nick Fitzgerald
* Nidin Lin
* Sam Clegg
* Till Schneidereit

#### Host facilities, local logistics

### Find volunteers for note taking

Found.

### Adoption of the agenda

Should we move items around? Move multi-value up?
Rossberg: yes, doesn’t require lots of discussion and attendance
Ben Smith: will move up, will open up some time on Friday
Rossberg to present.
(presentation pandemonium ~10 min)

### Proposals and discussions

#### [Multi-value](https://github.com/WebAssembly/multi-value) (Andreas Rossberg)

- status update

- probably the easiests topic

- no update on the status

- generalize all instructions and blocks to go from M values to N values

- no change to the format, except for generalizing block signatures

- still an open question about how to do the JS API

- want to await implementation feedback for how to do JS API?

- Can’t remember if we wanted to use a Typed Object for the return value?

- Is there any alternative to allocating an object on the JS side?

- A “sufficiently smart” VM could inline and escape analyze the allocation

- DE: there is a proposal for i64 in JavaScript, and it’d be great if we could call everything from JS

- LH: is there any compelling reason not to just do a JavaScript array

- proposal is at stage 3

- KM: JSC is pretty close to finishing the implementation, probably only a couple weeks of work

- poll: do we like arrays?

- Need to check meeting notes from last time: did we like arrays last time?

Poll phrasing: We should use JavaScript arrays for the return value for a multi-return-value Wasm function called from JavaScript. JavaScript returning multiple values to Wasm could return an iterator.

- this has been polled before, people were in favor of arrays, but we punted because it wasn’t considered critical.

- destructuring in JS uses the iterator protocol

- if we allow iterators, we might be forced to a slowpath everytime

- one direction is relatively easy (Wasm returning mv to JS), which can be an array, but should it be frozen?

#### POLL: Add JS API for multi-values into this proposal?

| SF | F | N | A | SA |
| - | - | - | - | - |
| 4 | 6 | 4 | 0 | 0 |

Anyone willing to spec this? Dan Ehrenberg has volunteered.

- DE: WebIDL does prefer the iterator protocol. If we want to maintain consistency, we should probably do that.

- DE: Can implementations check if the array prototype has ever been messed with?

- KM: JSC has some support for these things, most engines probably have this

- BT: does have some global checks for things like this too

- AR: I think the iterator is a wrong thing, but don’t feel strongly

- DE: WebIDL doesn’t have any tuples

- AR: which is why this might not be the best precedent here

- AR: there is precedence in TypeScript

- DE: TypeScript tuples can be used as WebIDL references

- DE: the whole point is to stay idiomatic with the web platform

#### POLL: We should use the WebIDL sequence type for taking and returning multiple values.

| SF | F | N | A | SA |
| - | - | - | - | - |
| 0 | 5 | 7 | 1 | 0 |

- any more on this topic? No…

- 15 mins coffee

#### [Tail calls](https://github.com/WebAssembly/tail-call) (Andreas Rossberg)

[Slides](https://github.com/WebAssembly/meetings/blob/master/2018/presentations/2018-10-rossberg-tail-calls.pdf)

- status update, resolution of open issues

- recap: support proper tail calls for languages and implementation techniques

- tail calls free the stack space of the caller

- main property: unbounded sequences does not exhaust stack space

- implementation is allowed to “amortise”, finitely many tail calls use stack space

- add two instructions:

return_call[func_index]

return_call_indirect[table_index][type_index]

- previous discussion: should the wasm type system make a distinguish the types of callers and/or callees?

- discussion of various uses, e.g. mutual recursion, marking callers and callees, e.g. implementation of inline caches

- checkin with Mike Holman on action item from last meeting

- MH: did performance measurements, did not observe any perform impact by not having the distinguished types

- LW: we thought it could be useful to have a different ABI

- DE: tail calls across compartments?

- LW: it was tail calls across instances

- the main blocker (wanting to distinguish) is now removed

- cross-module tail calls?

- implementers seem to think this is possible, because you can reuse the previous adapter frame (or overwrite it)

- some discussion of details of how the frame overwriting works, MS uses a C++ frame in-between.

- not possible to guarantee a tailcall to the host doesn’t need a frame

- cross-origin calls? membranes?

- LW: we are relaxing membranes so that they are no longer needed within an origin

- discussion about cross-instance call implementations; v8 uses all caller-save registers, and spidermonkey needs to go through a thunk to restore it.

- upshot: previous conclusion was to wait for impl feedback

- given discussion, more confident implementations could make this guarantee this.

- how is this related to funclets? funclets can only call within a function, not across modules, they are essentially goto

- KM: probably don’t want producers to use tail-calls to get goto

- current status: prose spec, formal spec, interpreter, and tests are there. Ready to move stage 3. (probably should be stage 3 given its current status).

- CW: what does the formal spec look like for cross-instance calls that aren’t guaranteed?

- AR: not in the current spec. It assumes we can optimize across modules, but would be an easy change.

- DE: multi-stage hops have worked fine in TC39.

- TC39 encourages presenters to state their stage goals from the beginning.

#### Poll: Advance to Stage 2?

| SF | F | N | A | SA |
| - | - | - | - | - |
| 16 | 0 | 1 | 0 | 0 |

#### Poll: Advance to Stage 3?

| SF | F | N | A | SA |
| - | - | - | - | - |
| 4 | 6 | 7 | 0 | 0 |

- tail calls are now stage 3.

- remaining steps: implementation work.

- CW: will funcrefs need a new tail call?

- AR: yes. Every call instruction will need a tailcall version. Should be a prefix? Probably not worth it.

#### [C/C++ API](https://github.com/rossberg/wasm-c-api) (Andreas Rossberg)

[Slides](https://github.com/WebAssembly/meetings/blob/master/2018/presentations/2018-10-rossberg-c-api.pdf)

- new proposal presentation

- Wasm is starting to spread to other embeddings. E.g. blockchain space. (8 smart contracts/blockchain companies?)

- AR: our (Dfinity’s) embedding is Haskell, but using C API and binding via Haskell FFI

- want an API for embedding Wasm into other applications

- this proposal is a “black box” embedding, wasm engine as library, e.g. non-goal to hook into the GC

- Want to enable 3rd language APIs via FFI bindings (via plain C API)

- Want to be compatible across VMs by being VM-agnostic, but maybe VM-specific extensions

- Want binary compatibility; can swap VMs at link time (no need to recompile client code)

- Want to standardize similar to the JS API

- Rossberg implemented both C and C++ APIs

- C is preferable for foreign language interoperability, avoids vargs, val structs, etc, but requires explicit management of memory of interface objects

- C++ preferable for safe native use because of convenience and use of smart pointers

- Proposal defines both but focusing on C now

- AR: implemented the C++ layer first, and C is implemented on top of C, but would need to copy at some points to do that cleanly. Instead did some nasty casting tricks that might not be strictly correct C++.

- API: engine and store. A store is currently thread local (kind of like an Isolate in V8). Modules, instances, functions, globals, tables, and memories. Anticipate multi values and reference types. Type representations and queries over them.

- discussion about the serialization API functions. The functions assume the engine can serialize a module to an engine-specific format which is writeable to disk.

- AR: remember this is an embedder-facing API, not a user-facing API

- further discussion about serialization: maybe this is an engine-specific API, maybe needs to use file descriptors

- LW: more nuanced API than this here

- AR: we need this API, but still want to be engine agnostic

- LW: needs to be abstract enough to be implementable without a file system

- KM: cannot just write machine code to disk and read it back on iOS

- AR/KM: we don’t make any guarantees about when deserialization fails? Would have to be specified in more detail. Intended for caching on the same device with the same version of the engine.

- MH: how do we do error handling?

- AR: most return values are pointers, and they would just be null if an error occurred, should probably introduce error results.

- also an API for sharing a module between stores explicitly, the shared module type separates sharing modules from their underlying representation.

- values are tagged unions; should be sufficient to pass the union value

BT: When you have an array of values; unless you know the signature of these things, the GC will need to know which ones are references. So they’ll need to be tagged.

LW: I was assuming that these things are not GC’d once they leave the JS heap. The GC doesn’t know about these things.

AR: Yes, references need to be deleted manually. Not sure about the SIMD case.

BT: If you have a tag that you can implement an interpreter easily. It’s nicer to have a tag, and this is currently just a space optimization. Maybe not worth it.

LH: Untagged union seems unmotivated. Not sure we want it yet.

BT: we probably want fast “unboxed” C calls in the future.

AR: There might be some implementations that cannot do fast unboxed calls, so wanted to make the values efficient, but maybe not that important right now.

AR: references need to be manually deleted (conceptually some API handle).

AR: ref_t is the top type, including API things such as functions and modules.

BT: may want to consider that anyref would then allow referencing meta-level objects (e.g. some things only implemented in C++ with no GC’d on on-heap equivalent) that could then flow into Wasm

- there are also representations of functions and ways to create importable functions from C functions, including ones that have environments

- APIs for creating tables and memories, instances, etc

- also a meta-representation for types

- implemented in V8 on top of V8’s internal JS API

- C API implemented on top of C++ API, has some extra cost

- currently external calls have to go through the JSP API, can’t use i64 currently or multi-value returns

- to create host functions and globals has to create small auxiliary modules

- open question: how to create high-performance call interfaces? Probably requires platform-specific implementation details like generating stubs: make this a post-MVP feature, or optional somehow?

- open question: tagged value or not

- open question: simplify use of vectors?

- KM: we would have to decide how many/which language APIs we would support as a committee? E.g. C seems reasonable, maybe Rust?

#### Poll: Advance to stage 1?

| SF | F | N | A | SA |
| - | - | - | - | - |
| 7 | 6 | 5 | 1 | 0 |

MH: looking at C API right now. Seems not very usable for people right now. Difficult and leaky.

AR: probably want C++ API

MH: it needs significant changes

AR: C API will be extremely brittle and probably should not do it by hand

LW: just like Wasm *laughs*

AR: should probably use C++, much safer

AR: can imagine building some abstractions to make this safer, but don’t want to build this in at the bottom

AC: it’s the higher level language’s job to make this safe, not the C API

DG: maybe we should have a different a set of things we define APIs; separate the API from the specification may be easier to move forward

KM: for Apple, every API has to be extremely robust for backwards compatibility

*** break for lunch ***

#### [Bulk Memory Operations](https://github.com/WebAssembly/bulk-memory-operations) (Ben Smith)

BS Speaking about splitting up proposals from the main threads repository, Bulk memory operations

AR: Comment, we don’t have table fill because we don’t have reference types, similarly we might also want to add Table.Grow - missing right now, but needed to achieve symmetry between memory and tables; both are currently part of the ref types proposal for that reason

BS: If reference types happens before bulk memory, we should add those as well

BT: It should still be possible to add table.fill

BS: Like a placeholder that doesn’t validate?

LH: We’ve implemented the reference types proposal

<BT, AR, LH Discussing status of proposals landing>

CW: Firefox implementation isn’t up to date with the changes a few weeks ago. Do people thing that it should still be changed?

LH: It’s not observable without shared memory

<BS explaining the recent changes>

CW: Mainly motivated by JF bringing up racy mprotects

BS: Recent change - when validation happens of passive segment indices..

AR: We just treat it as a passive check that was dropped, which makes sense as a desugaring

BT: When does loading of an active section happen?

BS: Before the start function

LH: Is that change observable?

BS: Only if it does a partial fill and traps

CW: Drop on a segment, no validation error on an active segment - will trap later

BS: Maybe active segments were a design mistake

LW: Maybe not..

<Discussion about active segments>

SC: Use case is to fill memory blocks efficiently

Is the spec complete? ⅔

LH: Stage two, too much information is in random github issues and not in the spec

AR: Do we know what’s missing?

POLL: Move bulk memory operations to stage 2:

| SF | F | N | A | SA |
| - | - | - | - | - |
| 8 | 9 | 0 | 0 | 0 |

- poll: advance to stage 2?


#### [Threads](https://github.com/WebAssembly/threads) (Ben Smith, Andreas Rossberg, Conrad Watt)

- Update on memory model and spec

<CW Presenting - “Threads and Weak Memory”>

[Slides](https://drive.google.com/open?id=11TmIKejgYtBic0W1vsQc17DNP3bPDMNS)

Talking through the threads proposal, and walking through the memory model, and some principles on which we’re making decisions.

Wasm memory model is a superset of the JS memory model

If this is true, a lot of design choices are forced based on the SAB behavior in JS

Live range splitting example

C/C++ Model: Racy write is undefined behaviourm JS: Data races are bounded

Wasm -> LLVM -> native assembly will probably not preserve semantics

BT: How does LLVM on linux work?

CW: It just happens to work

CW: Because linux will be compiled up to LLVM, there are transformations that LLVM can do that breaks the semantic, it just happen right now - when compiling the linux kernels some optimizations need to be disabled

DE: Link to memory model info in IRC (TODO: Dan Ehrenberg to paste link in notes)

CW: Only making a point that people have been making assumptions that it’s been working so far

AR: Note that WAVM’s approach will break once we bring threads into the picture

LW: Can we turn the same optimizations off for WAVM?

CW: Pragmatically that could just work

AR: What you’re doing is abusing compiler optimization switches as semantics mode switches (with no defined semantics)

BT: Where does gcc fall into this picture?

CW: Not sure about gcc internals, their IR might just be c++ like semantics

KM: What are some examples of stronger memory model assumptions in Linux than wasm?

CW: There is a data structure called lockref that makes assumptions -- they assume strong guarantees about mixed size accesses are true, true in hardware but not LLVM.

<Paper referenced in the slides>

CW: Hardware follows C++ behavior, but mixed size falls outside this

DE: Running linux will be a design goals for most ARM chips

AR: Right people are not even making the assumptions, they’re working on top of the assumptions already made

CW: small step semantics for webassembly makes the formal model easier to define. This was not as easy w/ JavaScript, since the steps are more like big steps.

CW: It will be a state of the art memory model. But it does have holes in it, since the research is not quite there.

CW: Change of spec to accommodate weak memory - Loads/Stores change operational state, but now when execute a memory access, some abstract change will take place, which may or may not reflect in an operational change so the spec is hard to write. Include operational, and axiomatic definitions

We can isolate the axiomatic version, but it doesn’t scale well - for example if we decide to share more state like tables - it’s an editorial decision - WDYT?

LW: I would like to see it separated. Since I would like to read the single threaded, but also the axiomatic. It makes it easier to see the shared load/shared store, etc in one area.

AR: Much more verbose

CW: It means that every feature becomes double the size.

LW: Actual execution semantics are not that large

CW: You need to define what a store looks like, it needs to go all the way back to the primitive definitions.

AR: Every thing that comes after will have to define a shared and non-shared version - the more state we add, the longer that section gets, it’s not very scalable

EP: From a presentation perspective, can you intersperse them with a different style to indicate the difference. So I can just read single threaded separately in one color, and shared memory case in another color.

CW: Shared version would not be an extension, of the non-shared version, but will have different state

AR: That’s difficult. The difference between the two semantics -- you are going from direct operation to indirect operation. You don’t say what you’re doing, just an abstract operation. It’s up to the axiomatic layer to define what it’s actually doing.

CW: We could still have 2 interpretations

AR: In terms of intuitive reading, it’s not that bad, might be more readable - the thing that becomes harder is building a formal model, and you only want to reason about sequential code that you might not have to do otherwise

EP: You have to rederive the current model.

AR: Extra indirection for formal model

CW: We’re planning to use the axiomatic model and see how surprised people are.

AR: This is already landed in the threads proposal, you can look at it. I would argue it’s not bad

BS: People don’t look at the spec, they just look at the overview - people reading the spec will not be scared by an axiomatic model

AR: They should be :)

EP: Operational model - assumptions?

CW: If we want to draw a line -- the current model is executable, but the axiomatic model is not.

EP: Is that example text?

AR: If you take the fragment that doesn’t include shared memory you could make it executable.

CW: Yey, but in terms of justifying through spec text it’s non-trivial.

- [Race between memory.grow and access](https://github.com/WebAssembly/threads/issues/26#issuecomment-424742576)

CW: This is an issue of -- memory.grow in one thread and accesses in another thread. These writes are implicitly observing the size of the memory.

CW: Many flavors of the same issue

BT: For reads I can see this, we can just reorder reads to make it easier/faster.

DG: It still doesn’t address seq cst.

CW: If you suspend both threads, you might fix it. Andrew Scheidecker said he would be uncomfortable doing it.

LW: Has anyone shown that mprotect commits incrementally?

CW: In research we have no definition for the OS behavior. Maybe just accepted wisdom.

CW: If we did allow only seq-cst behavior, it may not work for a simple example where you allocate memory ahead of time and update length.

DG: You still have to atomically check whether you’re growing?

AR: Only on trap.

EP: From a programmer’s side - I would still be accessing only in a safe way

LW: It’s only a way to spec this, and ok to let this slide for bad programs

LW: Does it still fit into the axiomatic model? If we make everything non-deterministic

CW: It mostly works.

CW: Only observable in the racy case. Weaken the guarantees for bounds checks, if you explicitly observe mem.length, the behavior is still the same

EP: Timing issues on traps are a security issue

CW: Code is so broken anyway, that not sure if it matters

If memory.grow is properly synchronized, no change in semantics

Memory.grow is still sequentially consistent with itself and memory.length

Accesses may independently succeed

POLL: Change access observation of bounds checks to be unordered (relaxed), rather than sequentially consistent

| SF | F | N | A | SA |
| - | - | - | - | - |
| 1 |  9 | 4 | 0 | 0 |

This adds new potential implementations.

CW: This means that you can commit pages in any order, because observing one write doesn’t mean anything about writes to previous pages.

LW: Is the formulation axiomatic because of JS? Or it’s just that operational semantics are not there yet?

CW: State of the art is not there, if you mean an operational semantics in the academic sense…


BS: Let’s talk about the state of the proposal, we have implementations that are being used by customers - phase says we need formal spec

CW: We have a formal spec in a pdf of the memory model and semantics that are not integrated to the github repo, but no spec tests - attaching the pdf to the repo - would that be enough?

EP: IS there a hurry to do this before it’s been in the spec?

BS: Saying that it’s in stage 1, implies we might change the api, or the instructions - there are edge cases, but the progress doesn’t reflect the phase of the spec.

CW: Semantics of wait - decision about making it trap - why was that?  After 2^32 why not just wake instead of trap? Current semantics of wake - represented as a signed int32. If number is negative and there are > 2^32 threads - it traps

LH: You can’t represent more than 2^32 because you can’t represent the return value so you trap

CW: Why can’t the implementation just use unsigned values?

LH: The only way to have more than 2^32 threads if you use wait async, because you can’t have that many threads, but can have that many waiters - its an edge case so nobody really cares about what happens

KM: Make it an unsigned number - just wake 2^32 threads, that’s almost equivalent to current semantics

LH: Parity with JS about negative numbers wanting to wake everything

BS: It’s negative infinity because JS uses doubles

LH: We should spec it, because it’s a boundary condition that can happen - but there’s no realistic way to test it

MH: Is this possible in practice?

LH: If you can represent that many promises..

BT: If the number is not representable, you should trap

<Bikeshed, this can be discussed later>

POLL: Move phase to stage 2? With the memory model spec appended to the current spec.

| SF | F | N | A | SA |
| - | - | - | - | - |
| 10 | 5 | 1 | 0 | 0 |

CW: Neutral because I want the memory model to be as good as possible.

LH: Do we have anything for a post-threads MVP?

BS: Nothing so far, it would be nice to have thread creation

KM: Do you already have customers using it?

Multiple: Shared origin trial with Mozilla, prototyping - lot’s of customers lined up

BT: Engine can’t purely implement threads on it’s own - needs to co-operate with the embedding environment

KM: Bulk memory operations would be nice as function imports

#### [WebAssembly Spec Update](https://github.com/WebAssembly/spec) (Ben Smith)

BS: Giving a spec update - high level overview of where we are at the Spec

2 working drafts, move to candidate representation - we had two changes

Added new JS tests, more stringent than the previous one - only one implementation was passing - no implementation is passing the test suite - the tests are failing are edge cases like is the object configurable? Unicode vlaues not handles properly etc. Similar state for both Firefox and Chrome - maybe not a concern because for the spec to move forward, we don’t need to have a 100% test coverage

EP: People approach candidate representations is - we have two implementations of the feature. Because we are doing a more diligent job on specifying negative behaviors - maybe stratify the tests into positive and negative cases? The other thing that might be worth doing is that looking into negatives - does anybody accept a bad data structure, or do they just reject in terms on the spec? Latter is more preferable

Having some sense of you reject the things you should reject will make sense - to present a credible path for users that are not in this room and doesn’t paint an implementation into a corner.

BS: Number of the issues are in the js-api section, but the core spec the implementations are doing well

LW: This happens in browsers years after - let’s put them in a 2020 folder

EP: The director will be sympathetic to that, your responsibility is to the user case so make sure it works the way you want it to

LW: There are coercion tests, that are ordering based, proxies.. Really to the edge

EP : You can say here are the cases that will affect interoperability - have gradations, we have done a good job of separating the finicky tests from the tests your users care about - better than css acid tests

BS: Because of the way that ms2ger labelled these tests, pedantic tests are easily separable

EP: We have machinery to write a test matrix - write the code to spit it out, look at the test fails - are those pedantic? If so annotate them, and present them

BS: Sounds like we have a process to move forward with the tests. The other thing I was concerned about changes to the text format - the thing that will require a restructuring are the things that breaks implementations, but as none of the implementations rely on the exact names, we could move forward to say the text format is more of a debugging feature - so let’s move forward with the CR. Any issues with that?

EP: Figure out which open issues are there, triage and label them accordingly, so there are no changes to the outcome of the tests, but semantic changes are ok. Address the tests with substance, and then we can figure out what to do wuth the rest.

#### [WebAssembly Content-Security-Policy](https://github.com/WebAssembly/content-security-policy) (Ben Titzer)

- [How does CSP affect postMessaging of modules](https://github.com/WebAssembly/content-security-policy/pull/16)

<Ben Titzer Presenting> [TODO slides]

BT: Any questions about WebAssembly.instantiate being blessed?

KM: I might need to talk to other people about this, who do our CSP stuff.

KM: Can come back, not promising anything

Anne: I think this should be named unsafe-wasm-eval

MH: Why does WebAssembly validate need to be restricted?

BT: It may not need to be

LW: I thought there was a practical use case. People want to check whether wasm is available then do it. We want new Module to match ...

MH: Is there a way to test for WebAssembly instead?

KM: Do you other spawn threads for your compilation?

LW: It might be nice to have “if WebAssembly” and “WebAssembly.validates”, and not require “new WebAssembly.Module”

KM: If someone wants to figure out what features are enabled and report back, that might be a use case, in the end everyone will find the canonical way to feature detect

LW: You may be using validate to see if you can do compileStreaming. Validate should be allowed always, then (even for unsafe-eval)?

DE: There’s nothing there for unsafe eval blocking instantiation, that should be blocked by construction

BT: instantiation should always be allowed, there was a previous proposal that checks beyond instantiation - compilation makes sense.

KM: Are you providing resource integrity?

BT: instantiateStreaming and compileStreaming perform a CSP check, so they can be used in any configuration even “unsafe-eval”

BZ: Why do you need wasm eval in this case?

BT: You don’t you can use this in any case.

LW: Eval works if the hash of the bytes matches?

KM: No.

AVK: Works for inline scripts, onclick handlers, etc.

TS: Slight detour, there’s talk about sandboxing apis for JS where you can create realms from script source - would we do the same thing for that?

AVK: Those should also be applicable here

TS: We should align the two in whatever direction w.r.t hash matches

KM: The realms proposal?

TS: Yes.

KM: They’re also top-level -- the inline source can see outside itself. You know what your scope is, you can’t capture outside of that. That’s my intuition.

DE: The streaming API already checks the mimetype.

LW: It won’t work on a type mismatch

BT: That means the mime type has to be associated with the response type

KM: Aren’t there other places that check for response types?

AVK: classic scripts don’t check mimetype. In the header -- if there is a content-type header, yes. But otherwise it’s undefined.



AK: You don’t mean a shared worker? Just a regular worker?

BT: Terminology may be wrong

AVK: Agen clusters are also same size, and not same origin, workers are always same origin

BT: There is a CSP feature, if you create a worker with a script, that can come back with more CSP on it. The worker could have more restrictions than the document. The only difference is that if you had this more CSP policy -- whether this is a feature or a bug. Google people want it to all have the same CSP policy, not more restrictive.

AVK: I don’t think that works, a shared worker can be used across shared documents

BT: You wouldn’t be able to post message between those modules

Many: you can

BZ: Yes, there are other cases where you can have CSP in a different iframe or worker.

BT: We need to figure out how this will work

AVK: Subtle issues, but general direction is correct

AK: Which of the two CSP policies need to be respected?

BZ: The reason workers have a different CSP policy, is because they can import scripts.

BT: If they have different policies postMessage could be a back channel to work around?

AVK: Only if they opt-in, the idea with postMessage is that you can take it or reject it.

KM:What’s the process for rejecting?

AVK: It’s up to the developer

KM: Is it explicit code that the user writes, or something else?

AVK: No explicit way.

AK: Why is this not true for modules?

AVK: The way message channels work -- it’s based on object-based capabilities, it is a different security model…

BT: We can’t postMessage a script between them

AVK: You can postmessage a blob to someone, and they can create a URL out of that blob that is same origin, and then load it….

LW: You can create the URL, then it’s the same origin

KM: Do you provide your own stuff?

AVK: If you trust that blob, you can do that thing.

BT: Isn’t that eval? [AVK: yes] Restricting sources of code is defeated by this?

AVK: If your origin has different CSP policies on different documents you are already exposing yourself to XSS. In most of the cases, since you’re similar origin restricted, you can document.domain each other, you can synchronously hand a function and call it.

LW: Then passing a reference to the realm on the same side..

AK: Once one member has access to eval, then they all do. So you need to set them all to the same restriction.

AVK: <indiscernible>

KM: I’m gonna talk to my CSP people about all this -- sounds reasonable.

BT: Sounds reasonable, the upshot is the same - we don’t need to put origin info on modules

<BT Presenting Specs that need to be changed/updated for WebAssembly CSP>

AVK: Responses have an internal concept of a URL list, the specification has access to. You can create synthetic responses in service workers. Maybe only valid for same origin requests, but maybe with CORS requests, could be the only way you could fake it. If it is same origin, maybe OK.

LW: The js-api - all it needs the book to stop compiling, but use the streaming api

BT: The check is dynamic, it might need to hash bytes, etc.

LW: The arraybuffer can have bytes that match the hash..

AVK: CSP policies can also change over time.

KM: I need to talk to other people, don’t make the decisions

BT: Next steps - I can work with Dan to write Spec text, will close the issues we decided on, figure out how to move forward.

### Adjourn

### Opening, welcome and roll call

#### Opening of the meeting

#### Introduction of attendees

* Adam Klein
* Alex Crichton
* Andreas Rossberg
* Barbara [...]
* Benjamin Bouvier
* Benoit [...]
* Ben Smith
* Ben Titzer
* Boris Zbarsky
* Conrad Watt
* Dan Ehrenberg
* Deepti Gandluri
* Derek Schuff
* Eric Faust
* Heejin Ahn
* Joachim Breitner
* Julian Seward
* Keith Miller
* Lars Hansen
* Limin Zhu
* Lin Clark
* Luke Wagner
* Michael Holman
* Michael Starzinger
* Nick Fitzgerald
* Ross Tate
* Sam Clegg
* Sven Sauleau
* Till Schneidereit

### Find volunteers for note taking

Lars will take notes

### Adoption of the agenda

Ben Titzer seconds

### Proposals and discussions

#### [Exception handling](https://github.com/WebAssembly/exception-handling) (Ben Titzer)

[Slides](https://github.com/WebAssembly/meetings/blob/master/2018/presentations/2018-10-titzer-exceptions.pdf)

Titzer presents, notes will gloss on slides when relevant

EH not just for C++ but for other languages too

"Low-cost" EH as zero cost is probably not quite attainable

We have two possible proposals to choose between for try/catch structure, one allows factoring and the other does not (broadly)

EH object (proposal #2) needs storage management but RC is probably sufficient if the embedding does not support GC

AR: Proposal #2 is more expressive and Proposal #1 desugars into it, so producers are not disadvantaged by proposal #2

AR: Proposal #1 seems to require duplicating all code for finally clauses?

HA: We haven't tried to compile finally yet with the current IR.

DS: One unimplemented idea is to enclose things in a bunch of blocks and then keep rethrowing until we reach the block where the code is.

AR: But can code paths be properly joined that way?  finally clauses should be executed both on the normal return and an exceptional return. Artificially throw in normal return case?

HA: C++ doesn't have finally so we haven't really run into this...

HA: Sharing does indeed seem a problem

BT: Destructors?

HA: Destructors are currently modeled as catch_all

BT: Would that work for finally then?

HA: Remains to be seen, really

AR: So are you duplicate the code for destructors?

HA: The code for destructors is not shared currently

AR: Destructors are finally in disguise

BS: Are there concerns about switching to flavor 2

HA: C++ would probably not benefit from this (?? inaudible)  Primary concerns are about lifetime issues and the requirement for reference types + storage management, esp for non-GC-enabled embedding

HA: Also a concern if the source language does not have a concept of reference types (?) but a minor point

CW: Can we elaborate on why Proposal #2 is more expressive?

HA: Code sharing and ease of rethrow (which are restricted to catch blocks in proposal #1)

MS: Indeed ease of rethrow is the most notable difference, proposal #1 prevents code sharing

CW: Would it make sense to decouple creating the exn object and throwing it?

MS: Symmetrical, sure, but this can be done with a try { throw } catch { } cliché

AR: The exn value is not just the values in it but also the stack trace, potentially, so it matters where it's created; this is a mess in JS where the trace becomes attached to the exn object by the throw operator, a mutation operation that is not pretty.

(Broad agreement from the v8 team)

MS: The proposal we choose may affect how we see the exn, since proposal #2 keeps the original trace with the object while proposal #1 that unpacks and repacks for throw may attach the trace of the rethrow to the exn

AR: There are reftype proposals in the pipeline, that may not be optional in the spec, that could make proposal #2 more attractive

BT+AR+HA: (Internal discussion re generalizations, not immediately comprehensible to the rest of us)

AR: One could consider a branch-on-tag instruction, a la br_table, can be used to encode catch clauses

BT: (demurs)

AR: Possibly useful for languages with more complicated pattern-matching instructions.  Compositional.

JB:

AR: These objects are expensive, probably

SC: So proposal #2 depends on reftypes proposal landing first?

AR: Yes

POLL: Should do flavor 2"

| SF | F | N | A | SA |
| - | - | - | - | - |
| 5 | 5 | 4 | 1 | 0 |

LH: This shouldn’t depend on allocation, storage management. Benefits of code sharing could be overstated.

HA: Can exn objects be stored in all the things? (Locals, globals, object fields, tables)

AR: If they are subtypes of anyref there's no way you can restrict that; if we want to restrict that it'll have to be a different type

BT: exn object is kept alive while it's reachable, can't be destroyed by the program

BB: why do exn objects reference the fn type space?  to avoid depending on gctypes?

BT: well, it had that effect, anyway

BT: are exns generative?  yes, they must be, but this has implications on other types that you may define, possibly

AR: disagree, exception tags and types can be viewed as seprate concerns

AR: exception tags have to be exported/imported, they are not structurally equivalent across objects

BB: can you catch thrown JS exn?

BT: only in catch_all

BB: so will host bindings solve this somehow to allow better catching in wasm?

BT: seems reasonable but unclear what WebIDL allows us to express in this regard

AR: will probably add WebAssembly.Exception so that JS can create exns that wasm can process properly, unclear whether DOM exns will map to these, "not impossible"

LW: Or we could have a "js exception" tag that could be caught specifically

(BS: 15 minute break)


#### [JS BigInt to WebAssembly i64 Integration](https://github.com/WebAssembly/JS-BigInt-integration) (Dan Ehrenberg)

<Dan Ehrenberg presenting>

AK: Have you run into any problems?

SS: No

BS: This is currently phase 2? What do we need for the next phase?

DE: Need an implementation, can’t be implemented in the spec interpreter, so we need an implementation

AR: You need tests, and a POC implementation at least

DE: Cannot be implemented in the reference interpreter

#### [ES6 Module Integration](https://github.com/WebAssembly/esm-integration) (Dan Ehrenberg)

Dan presenting, notes will gloss on slides when appropriate

important part of this is to work with bundlers to harmonize with their work

no current meaning possible for live bindings that doesn't depend on anyref, hence no live bindings in this proposal yet

(discussion re obscure corner cases of node.js)

webpack semantics more flexible but require trampolines for live fn bindings

async instantiation in wasm (brought on by the occasional need to recompile code for smaller memories at instantiation time) creates requirements for the ESM integration, making modules awaitable (though top-level await is not a done deal)

(obtuse discussion re top-level await in JS)

It comes down to: which semantics do we choose? how do we build consensus among implementations?

DE: What are the problems with the webpack semantics?

SS: Can't import memories or tables and that's a difficult restriction to live with

DE: Also concerned about magic semantics / ordering, and function trampolines

AR: how do globals work?

SS: rewriting globals as mutable to make things work, type checking has already happend?

AR: mutable globals are not constant exprs and can't be used in init expressions and a few other places, so that rewriting is not always valid. Compile-time validation may fail

DE: also visibility is greater this way, worrisome for integrity

(Wide ranging discussion, hard to capture)

(discussion: TDZ errors with circular imports w/ new semantics -- issues w/ webpack model w.r.t. semantics)

LW: Suggest people use JS module as wrapper to handle circularity, then if it happens a lot we could optimize that.

DE: We should make a concrete proposal for migration path.

AK: Migration path from where to where?

DE: For programs from webpack to the new thing we decide.

AK: I followed up on evaluate w/ AVK and Domenic -- it must be synchronous.

KM: It must be draining promises somewhere…

LW: I’d be happy to discuss more.

#### [Reference types](https://github.com/WebAssembly/reference-types) (Andreas Rossberg)

[Slides](https://github.com/WebAssembly/meetings/blob/master/2018/presentations/2018-10-rossberg-reference-types.pdf)

(AR presents)

Recap: motivated by opaque host references

New value type, anyref, a top type that can be used everywhere, including in tables, can be passed to/from embedder, but not otherwise manipulated from wasm

(Pretty picture with all the types including funcref)

Recently, dropped eqref and ref.eq; added all JS values into anyref (with some boxing scheme)

Status: all of the specs should be up to date, two implementations under way

LH: Proposes to split proposal: funcref/callref goes into one proposal (reftype v2); generalized table could stay in this proposal which can land separately.

AR: agreed, what would that mean for table of func?

LH: Table.get/set on anyfunc (funcref) table would be a static error in the meanwhile.

LH: Reftypes part 1 should have the table ops.

AR: Table instructions should also move to a separate proposal as well?

LH: we could, but Table.grow very valuable.

KM: not valuable if you don’t support multiple tables.

LH/AR: multiple tables are part of this proposal

JB: host functions subtype of funcref or expressible by funcref


AR: so anyfunc isn’t a subtype of anyref with your proposal?

LH: yes, not yet.

CW: what happens when a table.get on funcref table returns null?

AR: funcref is inhabited by null. There’d be a check before the call anyway. Typed func tables wouldn’t get this.

POLL: splitting off funcref (ie funcref not a subtype of anyref yet)

| SF | F | N | A | SA |
| - | - | - | - | - |
| 4 | 4 | 10 | 0 | 0 |

AR: some table ops (fill, grow, size) would logically be included in bulk memory proposal, but depend on anyref.

LH: Table.grow is the most important.

AR: reason Table.grow depends on this is because we need an initializer value (e.g. null).

MH: Don’t we have Table.grow already?

AR: only in JS. This would include it in wasm too.

CW: Uninitialized table slots (for typed tables) could also trap.

AR: we don’t want that (additional runtime check). There should be a default initializer.

LH: but then how do we declaratively initialize tables that require an initializer?

BS: could start at size zero and grow programmatically

AR: could do but seems silly. Table defs should allow explicit default initializer

LH: yet rational, since it allows a program-constructed type

All: (bikeshedding)

All: we will cross this bridge when we get to it

POLL: should we include these 3 table instructions in this proposal?

| SF | F | N | A | SA |
| - | - | - | - | - |
| 5 | 7 | 6 | 0 | 0 |

#### [Host Bindings](https://github.com/WebAssembly/host-bindings) (Luke Wagner)

[Slides](https://docs.google.com/presentation/d/1ciUHPjNdD3-OGqDjYGNI_Uqod8y3yQOVOnKI3urr2v0)

LW: Talking about host binding again.  What is host bindings? Is sharing memory?  Is it dlopen?

LW: Proposal has been inactive for almost a year.  With the progress of reftypes it's time to revive.

LW: What are we trying to solve: (a) removing JS stub code.. (b) Avoid constructing temporaries at the boundaries. (c) Make imported reflect methods fast

LW: Out of scope: (a) A set of portable interface definitions (b) binding to naive dlls (dlopen). © WebIDL callbacks (d) Binding to all the JS things (beyond whats needed to Web APIs) LW: Questions.

AK: Is web APIs that much narrower than all of JS. Promises, so…

LW: Large overlap, wasm automatically doesn’t need to make a new JS class. How can we hop from wasm to some web API, that’s what motivates. What if I want to make this look nice to JS, that may be separate.

LW: Idea 1: Web IDL coercions (see presentation).  Mapping wasm value types to JS type(s)

?: This is about passing something out, so shouldn’t it be spec’d on the outside?

LW: Sure.

AK: You mean  webIDl types no JS types?

BZ: There are many integer types

DE: Luke and I have talked about this -- should be Number on the right side.

LW: We can drill into that level of specificity later

<example>

NF: That 0 you’re is the memidx? [LW: yes]

AR: You also have the inverse for results? [LW: yes]

LW: For incoming values we can use anyref most of the type and import functions to decompose them.

AR: What about function arguments, callbacks? You then need a higher order coercion.

LW: You can think of a function has having multiple entries, that is how we would probably implement, a JS entry and wasm entry.

AR: You can pass the same wasm function as multiple different wasm functions -- it’s first class, you can’t statically know. That’s higher-order use case, maybe doesn’t come up with DOM?

DE: I think it would be useful to export host functions with attributes

LW: What sort of thing -- wasm with reference types can use anyref, so what automatic things.

DE: JS string to exported wasm function, you might want that to be unpacked.

LW: But thats a hard questions because then you have to call malloc.  Seems simpler to me that wasm just revieces the anyref and can call its own malloc

DE: We could say that many of these types don’t have a version that allocates in wasm. If you have a dumb function that returns a string, that wants to allocate a string in wasm space. There are 4 different edges, return values and parameters in both directions that requires memory allocation.

LW: I assume because we have references types wasm can do that itself and I don’t see a huge performanc benfit do doing that in the glue layer.

DE: That’s a reasonable starting point -- no coercion from wasm strings to JS strings. In comes up in either case.

AR: It’s worth a clarification -- main goal of the proposal is performance not convenience?

LW: Yes, we are trying to remove glue code because it hurts perf

AK: Is it trying to get rid of JS glue code in particular?

LW: Yes I think it’s just removing the glue code.

KM: Let’s you directly call the webidl entry points -- one is the wasm callable target, another that is the JS entry point.

AK: Was just wondering if we also trying to get rid of JS stuff because of JS performance.

LW: Yes, are we trying to go to all JS, or just on this hot path. For MVP just the hot path, removing glue.

DE: The lone term goal is to try to have wasm programs that don’t include any JS at all.

LW: Yes, I think that’s where we want to get to. You should be able to do wasm as script src.

LW: How fast can rust-wasm go -- walks over the DOM, firstSibling and Child, and it was 3x faster in JS than wasm.

Alex: It’s on the web if you want to look it up.

JB: No way to get rid of the glue code without reference types?

LW: I guess once we have reference types we can possibly remove all the glue code by importing functions on the reftypes.

<explains coercions to allow calling methods/getters/setters with anyrefs>

DE: do you really want to encource people to use things like reflect.contruct.

LW: They could use it, but can we make it faster. In terms of raw expressivity we should in theory we have the builtins to create all the anyrefs we need.

AK: What about functions with Function.prototype.call

LW: Yes, so technically we don’t even need the receiver.

DE: I think there are technically some differences between call and construct but…

<explains mapping from WebIDL types>

AR: It seems when you have aggregate types like tables, structs, you need to convert their elements, too. Requires a combinator language for coercions.

LW: Agrees

TS: YOu need the coercion for strings -- that seems more fundamental, Reflect.set and get need you to pass strings.

LW: Oh yes, if you import the string constructor

TS: You do you create a string?

LW: This utf8_string would let you take some bytes in memory and create a DOMString

TS: That is more fundamental, these are more for performance is what you said, but you need a way to turn bytes into strings so you can’t just use Reflect.get/set

LW: OK do you are saying how do we turns bytes into strings.

DE: I don’t really understand how we can go about this in principled way.  What do you mean you say something “can be done’ because as you say if you have anyref you can do anything.

LW: Yes, we definitely need strings.

TS: How would it work at all?

LW: You would have to call JS

Idea 2: WebIDL constructs as type imports

<explains type imports, see slides>

AR: Instead of “type $Node” you mean “ref $Node”?

LW: One way or another that type import references that thing.

LW: We already throw in wasm if the types of function imports from other wasm modules don’t match

Idea 3: Required Original Builtins.

TS: It would be unfortunate, if the module requires fetch, but you don’t want to give it fetch then it wouldn’t work. If you require the original.

LW: Thats preceily what we want, to konw for sure that we got it . We could consider a small fixed set of things we can require original.  If we whitelist them to just the core JS ops. Probably people are sensoring reflect.get.

KM: I’m not sure that’s better or worse than having a special import in JS API that .. it’s an import that never gets passed in that magically is there and doesn’t get passed in. That avoids the problem of … polyfilling is important, but ...

LW: I’d be happy to consider that, there is a space of options here.

DE: I don’t think it would violate object invariance to allow you to import ..  if thats that main thing we need to assert to origniallity of.

KM: If it’s just the core JS things...

TS: A use case I can think of -- analysis frameworks where you want to observe these. If that’s ...

LW: There are rewritting so they would strip this requirement.

BT: We shouldn’t have throwing for semantically invisible operations, for tracing say. You couldn’t do that at all.

LW: Thats true, but then we couldn’t statically optimize.

BT: You are introducing a namespace for a new bytecode.

LW: In effect yes.

DE: What if we add wasm insgructions for doing code JS ops.

BT: Is the the morally equivelent.

LW: I proposed this because it seme slike the just the next level but I’d be hapy to consider.. It seems like there are 3 options now.

AC: When you were talking about stubs before, you couldn’t skip all of it, is that primarily typechecks?

LW: I think there’s nan canonicalization that has to stay. If you pass anyref also, because that requires dynamic checks.

AC: are those things that wasm would eventually want to grow?

LW: Nan canon -- that’s a special case, we could remove these things with static type info.

BT: what's the delta to the original host bindings.

LW: I’ve not computed that.

MH: Are these all valid JS types? If the signature doesn’t match?

LW: That was idea 2 was if they don’t match we could throw.

AK: You use webidl types for idea 1, but you only need JS types for idea 1, not idea 2.

LW: That is confusing.

DE: This comes back to what luck and I have disucess two somewhat related idea. HB could map between JW and wasm and between webidl and wasm.

LW: pointed out some examples that don’t match up -- iterable?

BZ: Se webidl sequences are actually implemented as iterator so there is all sorts of observable points in trying to get data out of a sequence right now.  If we want to allow browsers to optimise this stuff internally we would have hide this .

AK: It’s not up to this group to make the non-optimized semantics, right?

BZ: This hasn’t been an issue until now -- webidl defines a type system, and how the system works and a coercion layer from JS. You could write a new coercion layer for something not JS.

LW: that what this was written that way it was becasue it is that same as going striaght.

AK: The problem here -- idea 1 doesn’t explain how you get webidl things, just JS functions.

BZ: so domstring is a webidl type, if you were definging this you would need to defined webidl coosersions for wasm

AK: I’m saying something different -- you’re importing JS functions, not webidl functions.

LW: in a sense we are importing webidl functions

DE: wasm can also import JS functions -- what do the module records consist of?

AK: I think there are a lot of questions we can ask here, you’ve tried to seperate them into 3 ideas but I’m not sure there are necessarily separable as you’d like.

LW: Idea 2 throws in more cases, by giving us more semantics.

AK: Idea 1 doesn’t make sense by itself, you’re importing JS functions not webidl functions.

LW: Today we’re importing JS things...

BT: The code that’s generated is by a JS engine, not … only JS types, no web platform bindings.

LW: So when you import yes you have a JS function.  When wasm imports it if could grap the internal webidl slot and use it directly.

AK: That’s not in idea 1 that you presented here…

KM: Is it better -- can I import a webidl function, this now converts the calling convention, look at the webidl signature, if the signature doesn’t have the same signature?

LW: So your saying we could derive it from the import.  So that was my initial attempt but that fixes the problem only for a single cooerion.  The nice thing about idea 1 is that a given webidl type can be produced in several ways.

TS: also DOM APIs have overloads, so you have to specify what to call.

DE: You could put it in the module specifier.

LW: There would only be one way to construct a given webidl type.

AK: There’s also an evolution problem, it constrains the platform to grow in pieces. YOu may break wasm code. I think something similar to what Dan was saying, trying to use JS, but ...

LW: Thats another way to specify, as long as we have the guaranteed optimization and its not observable.

AK: That makes sense in my head, this one doesn’t yet.

TS: What about non-web host environments.

BT: I think the reason to do it delcatatively is that you can skip it, like if the entire signature match you can skip all the layers.

TS: I’m not talking about something that dynamic -- I think the host environment would have to have knowledge about how that works and be able to skip. You would want to have it declarative.

LW: I guess that abstract reason if you imagine a platform them implements webapi but don’t have the JS to go along with it.   Either way I think it could achieive the goal of making things fast.

LW: I think the reason to go though JS is becasu there is this idea to put more webidl in JS.

DE: There is a separate idea of removing the two-layer abstraction in webidl, so you can make webidl into JS. Some people want one way and some another.

LW:

BS: Type imports would be pulled from the GC proposal

LW: I have a sequencing slide.



Poll: Do people think these are ideas worth digging into more?  By show of hands

Idea1 Coercions: Majority hands go up.

Idea2 Type Imports: Many hands go up.

Idea3 Required original builtins, many methods:

LH: I don’t care about JS, but this seems like … does this pay for itself? You have to modify some builtin, now you can’t talk about builtins anymore. Now you’re requiring … do you really want this?

LW: That would be a reason not to do it, but just one of the downsides.  I think it would make sense to motivate this by people wanting to have fast access from wasm.

AK: Seems like conceptually we are saying ..we got rid of all the JS semantics and then we are putting it back in again.

DE: I bet people want to do this kind of thing. They can use JS already for it though.

KM: If we go this way, probably we will want to do operations that need to be standardized but specific to certain hosts. Is that done via special custom sections? Magic imports? Functions that you call?

BT: I think importing host functions is that right answer here.  If you want a combined system where the host and wasm engine are optimizing together you are are eventually going to need something like this .

KM: Is it something that can be dynamically changed, or a regular import. You don’t know at compile time that it is semantically a “reflect.get”.

BT: I would basically argue it’s a question of where do you inline.

KM: Is there enough value in providing this statically. If it is a special opcode.

BT: It opens up a pandora box because every time you have wasm imported in another language you end up importing all the that languages semantics into wasm.

BT: I would say that is just more awkward way to say “this is a byte code”.

KM: Yeah but you don’t have to deal with your opcode space overflowing.

LW: does anyone argue for more than delaying it? [No one]

LW: Bikeshed time (see slides)

LW: In a way reference types is host bindings.

Fast bindings? Web host bindings?

BT: To the point you made earlier there would be host that provides webidl without JS, so i think making calling it webidl might make make sense.

AK: It will reduce confusion but add more confusion, so it’s ...

AK: We can just call it webidl bindings now and change to JS bindings.

LS: I like webidl bindings, does anyone argue against

BS: IIRC we didn’t have it always has host bindings anyway

LW: That very general things is reftypes.  This is more specific so  thats why think webidl makes sense.

Poll: Should we rename to WebIDL bindings

| SF | F | N | A | SA |
| - | - | - | - | - |
| 6 | 5 | 3 | 2 | 0 |

DG: None of this very fleshed out to me to warrant a name change. Maybe a calling convention makes more sense. Mostly I want to see how this plays out before committing to a name change.

LW: Would you be ok with calling it WebIDL for now. And the giving it a better name if we find out.

TS: I feel like there is something more precise we can all it .. fast bindings?

LH: It really is a FFI, these are annotations on interfaces that you can already import. This is how you’re really supposed to interpret this.

But they are webidl specific annotations.

DE: If we think of this as FFI, then we may want to have a place to define how we want to bind -- like node will want to bind to JS and different things to native.

LW: Oh yes, I was imagining this would be one way to say this, and there might be other way to express other kinds of coerciations.

LW: If we were to call it FFI people might assume its the back door out of the sandbox.

BT: This is specific to webidl and I don’t think it will be general enough to transfer.  So I think scoping it is good.

AR: I agree.

<presents sequence slide>

AR: I think function references are more important than finishing all of this.

LW: Yes, so we are not committing the order, they are separable units.. Well some block others.

AK: The combining of the type stuff with webidl -- I think of types as further improvements on idea 1.

LW: The type import lets us do instantiation time type checking and avoid runtime type checking.

AR: Doesn’t -- as soon as you have a callback, don’t you need function references?

LW: Bind needs GC so was imaging bind coming with GC or GC types

AR: Then in general we have dependency on GC proposal?

LW: Yeah, or weakref, and bind.. So yeah.  Ultimately you can do this in JS so things will get faster with bind or weakrefs.

LH: If you control the C++ side, the closure can be a fat pointer with the instance and an environment.

AR: Not technically but in practice the closure environment has to be GCed.  With bind you can create arbitrarily many closures dynamically.

LH: You are suggesting that has to be heap allocated in some cases.

AR: Yeah

LW: Any questions…  we’re done.


#### [Garbage collection](https://github.com/WebAssembly/gc) (Andreas Rossberg)

[Slides](https://github.com/WebAssembly/meetings/blob/master/2018/presentations/2018-10-rossberg-c-gc.pdf)

<AR presents slides>

AR: We didn’t do much work on this for some time.  Briefly a year ago.  Last extensive discussion at last july’s meeting.  Main thing that happened since then is we split of the reftype proposal, and more recently defined proposal for an MVP which is what I want to talk about.  I think we have good handle on the rough scope of the MVP but technical details are more open.


JB: These downcasts will always incur a runtime cost, even though the language knows it is OK?

AR: Yes, we can’t do better than that, would require the grand universal type system more expressive than all languages

<back to presentation>

JB: By closures you mean, binding one of these to a funcref?

AR: Yes, closures may move up to MVP, or maybe funcref proposal directly.

<back to presentation>

AR: questions about func.bind … may need closures as pairs or fat pointer. Some self-hosted wasm implementations may not do it this way in some cases, but most will probably.

CW: Will it be possible to store a reference in a table?

AR: It’s in the ref types proposal, so it will be already dealt with. Table is less interesting once you have call_ref, which doesn’t require runtime check.

BT: do you also need downcast from funcref to ref?

AR: I’ll get to that

MH: Why does ref.func not give you a funcref?

AR: It gives a typed func ref, funcref is the supertype of all func refs.

RT: Isn’t there a problem with having closures be a subtype of funcs?

AR: yes, when you inject the subtype you would need to coerce

LW: Because of the non-coercive subtyping they all have to have the same representation

AR: Yes you basically have to normalize, but if you just use the subtype consistently

LW: but anyfield on any struct could later be views via anyref.

AR: If you store it somewhere you have to use the universal representation.

LW: Maybe we wouldn’t want to make it subtype but just a completely separate type.

AR: We definitely want non-coercive subtyping in general.   The whole func.bind thing we need to think through a little more carefully.

<back to presentation - instructions - structs>

BT: You also need a cast if you can override a method with a more specific type…

AR: No, only because the receiver’s variance goes in the opposite direction. Method type specialisation is fine. For nothing else with plain classes you would need this, only for overriding method. Java interfaces are more work, and more expensive.

<presentation - instruction - casts>

JB: [br_on_cast] Is there a precedence for this type of chaining. Other operations you have to store in a local.

AR: It has a builtin tee, that’s true. But this seems what you usually want. With exceptions for example, you may want to match multiple cases. If we do it there, maybe nice to have symmetric thing too. Languages with typecase would want this too.

<presentation - instruction - RTTs>

BT: But the thing you get could also cast another type F to t’.

AR: What this means is that with this instruction you are constructing an explicitly subtype hierarchy for runtime checks.

BT: It could be unrelated to the structural type hierarchy.

AR: It’s not unrelated, just a smaller relation. Typing rules ensure implication

BT: I wonder if this could be turned into a static version?

L: When you say subtype you mean that t is a prefix of t’.

AR: In the first order case yes.

L: But then given that this defines how you can cast down, there are things that can automatically be cast up that cannot be cast down?

AR: Yes.

BT: I mention this -- if you haven’t seen the code yet, then you see this, you may need to keep meta information to keep these at runtime, which may be as expensive.

AR: Right, so presumably you would at compile time already generate these.

BT: This is more like an import. In the case of imports you would not know, whatever information you have, you need to keep it around.

AR: Yes whenever you have an rtt.new instruciton in your program you have to construct a sort of template.

BT: The difference is only whether you have to do something different at ...

AR: that cost we are trying to reduce is not the representation, it’s the runtime check.

BT: This is basically just a cache for that check.

AR: Yes

RT: I don’t understand why it needs to be dynamic, many languages it can be static.

AR: The answer is that this is kind of forward looking.  I’m pretty sure that something we’ll need to add later is some kind of type parameters.  Then once you want compile a language that has fully reified generics then you cannot do that statically in all cases, you actually have to do that at runtime, e.g. in a generic function.

BT: It’s a runtime of instantiations.

AR: Runtime language of the host, and the representation which you need ot perform the downcast. You need to dynamically create runtime types for languages in general.

AR: With the current MVP proposal, they could be static but that wouldn’t scale.

RT: Yes.

<back to presentation>

JB: But you’re still paying for the cost of storing the ref.

AR: Implementation detail. In JS, it is stored in a descriptor somewhere, more overhead to do something else.

<break>

<instructions - optref >

BT: Why not ref_isnull?

AR: This refines your type information, ref.is_null already exists in ref type proposal.

LH: The other instructions you show go from optref -> optref, but they go from ref -> ref.

AR: Do any output an optref? I think it’s always an input. If we did have that we may want to have two versions. We can get away with subtyping here.

<Br_on_cast> AR: But that’s just passing through the input, right? LH: yes.

<instructions - equality>

AR: somewhat funny, subtyping implies heterogeneous ref equality

LW: Maybe ref.eq could be polymorphic?

AR: maybe

RT: My question about anyref may help with this issue

<unboxed scalars>

AR: If you have a more dynamic language, you need to do runtime jitting (like CLR) or you need to use a single universal representation, all values word-sized. Still want to avoid boxing small scalars.

<instructions - scalars>

RT: Why go from i31ref to anyref.

AR: For uniform representation, you need anyref everywhere.

RT: For ocaml i31ref would be universal.

AR: You want to use them interchangeably with other references

BT: It’s definitely an integer, not another ref. But you use it where you use a ref.

AR: It’s conceptually a reference to an integer, not a union of int or ref.

RT: Ah I see.

AR: Different use case than i32ref. i32ref could be just a struct with an immutable i32 field.

LH: On 64-bit platforms, it would be a huge advantage to have that as a native type.

AR: I agree, the only advantage of i32ref, the engine can unbox it on 64-bit architectures. But that is a performance thing, not expressiveness. Much less important. This you need otherwise you can’t compile things.

LH: I think of this an ML ref, not as much for scheme.

AR: should apply to scheme and other, too

LH: You want more information in the pointer than this.

AR: That’s a separate problem, you’re asking about more tag bits in the pointer. You can have at most two on 32 bit  -- or maybe more if you waste more space with alignment. Other problem are existing engines, already use tag bits in their own way.

LH: I understand all the problems, yeah I just…

AR: It is far post-MVP thing -- maybe abstract to a union of tagged variants as another form of GC type. The optimal representation of the type can be abstracted to the engine.

BT: This would be useful if you want to implement bigint, or other things.

LH: One bit tagging scheme, it’s clearly useful.

AR: Inside the integers you could use more bits for tagging, that’s up to producer. Kind of ad-hoc but hard to see how we can do better.

<type imports/exports>

AR: <import eq types> useful for typed objects proposal.

<open questions>

TS: <JS API> To make it work -- in wasm we don’t have named fields, to reflect that on JS side is to have something similar to heterogenous typed arrays, with indexed fields, which you can optionally give names. Subtyping adds to the indexed fields, and I think we can reflect them in a way that makes them feel like JS objects but have fixed structure and be realizable on the JS side, and we can optimize the field accesses better, or at least in lower optimization tiers in JS. They should be able to flow into normal JS functions, and the dev won’t have to care. Explainer: https://github.com/tschneidereit/proposal-typed-objects/blob/master/explainer.md

RT: Note: we found there is some work in the gradual typing space that covers this.

MH: i31ref -- if you pass in a tagged int from JS, you can’t cast this to a tagged ref. There’s going to be a …

LW: If there is an integer, and it fits in i31, then we can put it into i31ref. When it goes back out it turns back into a Number, but if you flow in and out then you get the same value.

BT: If you have an i32, and we have to_int32, you could chop of bits out of range…

AR: I would expect that you wouldn’t use i31ref at the boundary.

LW: Anyref at the boundary, right?

AR: Yes, maybe something more canonical.

LW: It would be sad if JS passes in a 1, so we have to box it up as a hostref. It would be nice to have an i31 for that.

AR: So do you normalize a boxed integer that happens to fit? I don’t know what engines do here -- do they canonicalize boxed small numbers.

KM: Yeah, we canonicalize small integers.

MH: Always? You can’t have a float 2.0.

KM: Yeah, it’s special.

LW: If I have two doubles that add to 2.0, you do that? For us it’s best effort. Since it’s semantically …

AR: The semantics suggest that certain engine choices observable.

LW: I think it requires you to normalize at the boundary.

RT: I see the appeal of having top type of anyref, seems like the most constraining type of it. It seems like it requires making funcref a fat pointer. Or for example, virtual table, vs. class objects. Function pointers won’t be in the same space as class pointers. Using anyref forces them to be in the same space. I understand the uniformity reason, is there a reason why you have a global one?

BT: You could do that with an empty struct that creates the top type, and you can use that to slice it up more fine grained. This is more machine level.

RT: But since they all could become anyref, it means the system has to consider that. Certain differences are required to be dealt with.

BT: We do this in v8, we have things that are heap allocated that are very different, there’s always a user level language on top of this. But this is for wasm.

AR: But that’s what Ross is worried about, this makes it harder for the VM to be aware of the constraints by the language.

BT: There are things at the source language level, you can make fat pointers into flat tuples. You’re right about closures, the engine would have this cost. It is the cost for using wasm, it’s not a big one.

RT: Making every single pointer double width for that.

LW: We would just box those.

RT: Do you need that, though? Seems like a huge constraint that doesn’t provide value.

AR: Could rephrase: should we have other types not under anyref, those could be added later if we see the value.

RT: I would get rid of funcref as anyref

LW: I think we need it, for JS values.

RT: You could have a separate space for that type of reference,

LW: I think the more interesting thing is, how much can you put in the bits -- I think i31ref gives that and then everything else has to be boxed.

BT: I think Ross is talking about a funcref that doesn’t subtype anyref.

AR: You could still have a separate funcref that isn’t a subtype and that could be converted to a funcref that is a subtype. I don’t see the advantage of not making funcref a subtype of anyref.

RT: It’s harder to remove a subtyping relation than to add it layer. Why is anyref required?

AR: Wouldn’t remove it, just add a new type later.

DE: Reason is this all has to be reified in JS.

BT/AR: that’s not the reason.

AR: I can imagine cases where you want to put a function into a tuple. I don’t see the benefit of removing this.

RT: You said it might be better to have funcrefs as a different representation.

AR: But we could add that later.

BT: YOu can do fat pointers in user space, everything is flattened out. You can just manage your own fat pointers, the engine doesn’t need that.

RT: There is no reason to force the engine to do that.

AR: What about putting a function in a tuple.

RT: It’s not actually part of the uniform wrapping, the function pointer is not in that space.

AR: If everything is a closure, but some languages don’t do that in all cases, I think -- e.g. for top-level functions. Then they are in the same space.

RT: Then you have a wrapper for that language, rather than something else for everyone else.

AR: You are asking to complicate it up front…

RT: It’s simpler.

BT: No engine will do fat pointers, they’ll do one pointer and box.

RT: I don’t know of languages that have this behavior, use this as a concrete example. Ask why we need anyref, that’s what I want to know.

LW: I talked to Rodrigo about this, because C# has this problem. They pass around a bunch of raw sizes and dictionary and do memcpys so they can wrap bitblits. If they can’t do that, because it’s unsafe, they need anyref.

RT: But they use anyref for the C# values, not ref right?

AK: high-level question: MVP => what does the V mean. Who is the target audience.

AR: I think in the first iteration of this proposal, mainly statically typed languages, people who currently compile to JS. E.g. Scala folks, functional programming languages, Kotlin, …

AC: In terms of users of GC types, we’ve been talking about this for Rust. It integrates well with anyref, we have some ideas about this.

AK: Is the working model you’re using to refine this with implementors?

AR: Yes, we are in contact with languages with different levels of interest and commitment. It’s a substantial investment, not too easy to find the early adopters.

DE: What sorts of feedback have you gotten.

AR: Talked to e.g. Ocaml folks, haskell folks, scala folks, some scheme folks. Some commented extensively on GH. Seem satisfied so far

LW: Elm, and perhaps Kotlin.

DE: What have they been saying?

LW: They want typed objects.

DE: Have you heard feedback about i31ref?

AR: Haskell and Ocaml need it. Not sure about scala. Basically if you want to implement larger integers you want to do this unboxing trick. Not just for integers, any scalar you want to do this.

RT: Scala might not use i31ref, unless you want to throw away JVM semantics

AR: Yeah, perhaps. scala.js is somewhat different than scala

RT: True.

### Adjourn
