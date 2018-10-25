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
       1. [Tail calls](https://github.com/WebAssembly/tail-call) (Andreas Rossberg)
          - status update, resolution of open issues
          - poll: advance to stage 3?
          - 30 min
       1. [C/C++ API](https://github.com/rossberg/wasm-c-api) (Andreas Rossberg)
          - new proposal presentation
          - poll: advance to stage 1?
          - 30 min
       1. [Threads](https://github.com/WebAssembly/threads) (Ben Smith, Andreas Rossberg, Conrad Watt)
          - Update on memory model and spec
          - [Race between memory.grow and access](https://github.com/WebAssembly/threads/issues/26#issuecomment-424742576)
          - 1 hour
       1. [Bulk Memory Operations](https://github.com/WebAssembly/bulk-memory-operations) (Ben Smith)
          - poll: advance to stage 2?
          - 30 min
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
       1. [ES6 Module Integration](https://github.com/WebAssembly/esm-integration) (Lin Clark)
          - 30 min
       1. [Multiple values](https://github.com/WebAssembly/multi-value) (Andreas Rossberg)
          - quick status update
          - 15 min
       1. [Reference types](https://github.com/WebAssembly/reference-types) (Andreas Rossberg)
          - quick status update
          - 15 min
       1. [Host Bindings](https://github.com/WebAssembly/host-bindings) (Luke Wagner)
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

Posted after meeting.
