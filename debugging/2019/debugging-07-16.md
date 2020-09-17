## Agenda for the July 16 video call of WebAssembly's debugging subgroup

- **Where**: zoom.us
- **When**: July 16, 3pm-4pm UTC (July 16, 8am-9am Pacific Daylight Time)
- **Location**: *link on calendar invite*
- **Contact**:
    - Name: Derek Schuff
    - Email: dschuff@google.com

### Registration

None required if you've attended a wasm CG meeting before. Email Derek Schuff to sign up if it's
your first time. The meeting is open to CG members only.

## Logistics

The meeting will be on a zoom.us video conference.

Installation is required, see the calendar invite.

## Agenda items

1. Opening
   1. Introduction of attendees
1. Goals and scope of upcoming debugging work
1. Future meeting schedule

## Meeting Notes

* [DS] Derek Schuff
* [YG] Yang Guo
* [YS] Yulia Startsev
* [NF] Nick Fitzgerald
* [PS] Paolo Severini
* [BT] Bill Ticehurst
* [ZN] Z Nguyen-Huu
* [YD] Yury Delendik
* [RL] Ryan Levick


Current state web assembly debugging: Not great.
  * FF devtools can show the disassembled code, set breakpoints, step.
  * Can show variables
  * Has sourcemap support, but this is only line table support.
  * Not full featured debugging info from this
  * Parses dwarf directly (pilot)

Chrome has similar support.
We would like to do better.

LLVM ecosystem Outputs dwarf (thanks yury)

[YD] Making tweaks to dwarf (a webassembly flavored dwarf)

[YD] We are lucky that dwarf already emits line information

[YD] Allow encoding local and global variables

[YD] We can generate wasm binaries with dwarf sections with special information

[YD] There is a patch to encode wasm local in expression

It’s a little controversial, contributors to llvm/dwarf recommend using existing primitives

This isn’t ideal, we would like to be able to extend this beyond what dwarf support by default.

[PS] also tried it out in V8 and it seems to work well

[YD] Idea is also not to expose dwarf to web browsers directly. Can also generate native dwarf translated from wasm dwarf for native debuggers to debug JIT code; allows attaching a native debugger to the browser

[YG] I had in mind an engine exposing an API to provide state like the wasm stack which the debugger could request, then translation wouldn’t be needed.

[YD] Trying to consider both cases; browser and more “native” case (e.g. wasmtime) because there is a lot of interest in both cases. Transformation works well there

[YG] Having VM expose wasm stack etc seems simpler than translating dwarf.

[NF] Do you mean expose the source-level stack in terms of wasm?

[YG] Give a way to expose architectural state such as wasm stack and wasm memory 

[YD] In this case, you cannot reuse most of existing native debugging capabilities. You have to implement the debugger yourself.

[YG] for this you need some sort of bridge between LLDB and ?

[DS] You would need to port your debugger, which would be some work. But there would be a number of similarities

[YD] Memory isn’t the same. There are different address spaces e.g. in ELF the code is in memory. LLDB/native debuggers have a common address space, so that idea is foreign for native debuggers.

 [PS] we will always need to attach the native debugger 

 [YG] so you’re proposing that the VM would parse the wasm dwarf, translate to native, and then provide that object to the debugger.

[YD] it works right now, I evaluated it with crane lift and it is working.

[YG]  I had assumed it would be easier to do it the other way

[NF] different environments will be easier or not, depending on the context. Inside a web browser, I am not so sure about that -- developers will want to use their existing tools. I am not sure that dwarf will work in that case 

 [YG] I was wondering if we should standardize around dwarf or not. It may or may not work for all languages that use webassembly in the future. To make this the job of the VM to transform wasm dwarf into dwarf puts a certain burden on the VMs.

 [NF] Don’t know if everyone has seen the presentation from a coruna, but briefly, the surface area of capabilities that the debugger wants to expose is much smaller than the surface area of all the debug info that we’d ever want for all languages. The VM doesn’t have to know how to parse dwarf, etc. it just knows how to make the queries. We can standardize the smallest amount possible and let the community work out the best/smallest format.

[PS] whether this debugger module -- would it always need to know the internal state of the engine. This part is not clear to me, how this would work if the module is completely separated and only provides an interface.

[YG] I think the way is that you’d … query the debugger module, but the engine would have a low level interface to query e.g. the stack

[NF] it would almost be the same interface, but the one exposed to the debugger UI is almost exactly the same as what the debugger uses now While the one exposed to the module is specific to the language / whatever

[YG] the frontend of devtools/debugger would set a breakpoint from a source line, request that from the debugger module, which would translate that to a wasm instruction and request the VM to break there. Then the VM would call back into the debugger module which would call the frontend.

[PS] bit the debugger module would still need to call into the VM to get the state.

[YG] that would take a couple more round trips but yes.

[NF] the other thing is that it’s possible to support something like Blazor eventually. You could have a debugger module that uses dwarf internally to answer these queries. Blazor is an interpreter, not AOT. the wasm stack isn’t useful, you’d have to look at its internal data structures. Dwarf would not be a good fit for this use case

[DS] Yeah we had talked to the Blazor folks in the past and it was not a good fit. What they are doing now is they are intercepting the chrome devtools protocol and injecting their interpreter in the middle to do what essentially we are discussing here 

[YG] This gives us the ability to not use dwarf and just use any data format that you want

[DS] Eventually in the future I think there will be a standard for a file format, if you look back on the doc that nick wrote about requirements. There will probably be a spec for a common way to format data for debug information so that tools can reason about it. 

 [BT] You’d probably want a separate v8 isolate to run the debugger module, to make those queries since they’d be privileged?

 [YG] I would assume that yeah. Previously, in V8 -- part of the JS debugger was written in JS as well. It already had privileged context, but having a privileged isolate would make it a lot nicer.

[NF] thats an implementation detail though

[YG] Yes, you could even make it out of process and use RPCs.

[PS] devtools will also need this capability to always be able to debug WASM right?

[YG] Im imaging that devtools frontend wouldn’t have too many changes. All it needs to do is give a high-level understanding of wasm debugging. But it doesn’t have to translate high-level debuggability to low level because it would have the debugger module. So it could fetch scopes, request things at the source level. All this exists for JS already, so it would map well into that.

[PS] we just need to extend the CDP to add just what is missing 

[YG] I expect that there are some things that are slightly different so we could extend the CDP a bit. So we’d probably need something that expresses types (since no types in JS) but this would be small improvements and not fundamental changes.

[PS] And you said there are other kinds of debuggers, how would that work, would it use the same api to talk to the engine? It would need to talk to the module so it would need to run webassembly

[YG] the point of having the debugger module is that you’d make that an implementation detail. It could be a shared library that you load at runtime. Having a wasm module do it seems easier.

[NF] since wasm is capabilities based, we could play with the idea of statically known debug info vs things that need to inspect memory. That could be the difference between whether the debugger imports introspection apis. And you can decide to import them or stub them out. You could build up native dwarf if you want.

 [YG] I’m not quite sure what you mean. You’re saying that if we don’t expose the lower level API to the debug module, that it would still do some (serialization?)

[NF] It depends on how we do some of these cuts. If some information like line tables don’t need to dynamically inspect runtime state. You can go through and enumerate the offsets -- and you could build up native dwarf rather than wasm dwarf. You can see how far you can push this.

[YG] I see so if you have e.g. information in a stack trace, it could be interpreted without the need for more capabilities.

[PS] What will be the next phase then? 

[NF] We could try to agree on some very minimal kernel of an idea that we can start playing with and implementing and standardizing. It seems like people generally like the idea of a debugging module. We could do a poll to see if people feel good about that? 

[YG] I am a bit torn about this being a JS api or a WASM API. It could be both and there are merits to both 

[DS] There is no WASM api at the moment, we don’t have a way to spec those. WASI is the closest we have. It probably makes sense to start thinking from the perspective of JS capabilities, and then we can change it and the way that its defined. There is hope that with the webidl proposal and build on that

[NF] I think that bindings would be very good for this purpose, since it would allow things like taking webIDL dictionaries. The property-bag approach is amenable to adding more information to a query in the future. Dwarf really bends over backwards to ensure that its future compatible and extensibile, but that makes it convoluted. Using bindings allows easily adding stuff.

[YG] To be fair, in javascript you would have the same advantage since you can just pass a bag of properties. 

[NF] not all wasm environments are going to have a JS environment. IF we use the IDL to define them it will work for all.

[YG] Thats true. Yet another way would be to have a wire protocol, could be any existing ones or a new one that we come up with. I think that could also be an implementation detail  

[DS] That is one thing that i observed, the reason that we want this as an api rather than as a protocols, is that protocols could have a lot of round trips. What I think is that in the space of debuggers, the protocol seems to be something that they do. If protocols are the best thing for native debuggers why not for us?

[NF] I would say that it wasn't just the round trips that you have to do, but standardizing a protocol is more work than standardizing an interface. You would also have to standardize the details of the wire format.

[YG] realistically there’s not going to be too much of a performance difference because you'll want the debugger module in a different VM instance anyway and copy stuff around.

[NF] I wonder how much work it will take to get around that .the dwarf expressions let you know information about a few things you might want to do all at once. Whereas if each of those steps was a round trip i can imagine a lot of latency introduced. 

[YG] Unless the debugger API is high-level enough that it asks for local variables in the sense of wasm. Or e.g. all the locals at once.

[YD] There is also type information that needs to be known by the debugger. Right now javascript doesn’t need to know about types, but we need that for wasm. 

[YS] Also one of the reasons why the JS side is interested in a standardized debug format is for things like clojurescript or other typed lanaguages that compile to JS.

[YG] That essentially is the problem of transpiling any language into javascript. The problem here is that sourcemaps are just not good enough

[YS] In this case we don’t have dwarf to start but other languages that have advanced debug environments is that they have interfaces similar to what we’ve been talking about e.g. just running a clojure REPL

[NF] That’s also the other thing - expression evaluation. There are lots of features here, it would be nice to have a small subset. 

[DS] IF we can split debugger from front end and identify the capabilities that go between those, and specify those as a protocol. Then we just need to add a serialization on top of that.

[YG] I agree, once we crystallize out the components and their responsibilities, other aspects are negotiable. 

[BT] since you’ll have multiple wasm modules being deb ugged from different compilers, they have to coexist.

[NF] If you have two things that use different types of dwarf, they can just say that they are dwarf and get different input. 

[BT] with the cross language, e.g. JS to wasm etc, mostly things will delegate cross-langauge stacks etc to the frontend. The debugger won’t know about JS Frames, etc.

[YG] I guess the font end would need to know the difference between a wasm frame and a javascript frame to understand the content of each frame.

[BT] with things like ref types and host bindings is there anything coming where reaching into other frames something that will need to be known about?

[YG] I guess reftypes are going to be interesting in that they are opaque in wasm and not so opaque outside of it

[DS] I think there is going to need to be some kind of mechanism to allow whatever component that implements the ui, to know which language this frame is from, which debugger module will be used to query information about it. There will need to be a way to hand off between debuggers.	

[BT] Interesting to thing about things like data watchpoints, etc where you have to translate data addresses. There will be minor wrinkles as we implement this.

[YG] I think at this point just being able to debug one source language would be a great progress. We will need to think about this down the line but we will get there and worry about it then.

[NF] how about this for a 0-level MVP. how about we get line tables/breakpoints working. Replace source maps first, then think about rematerializing scopes/variables, but without pretty-printing. E.g. if you get a rust string, you just get the heap pointer + size, etc.

[YG] I think implementing this MVP might not be that hard. You just need a JS implementation that understands source maps and hook that up to the right apis. 

[PS] Shouldn’t we start with dwarf, since we’ll use it anyway?

[YG] I think realistically we won’t be based off sourcemaps, but we can implement the mvp easily using sourcemaps

[BT] Either should be doable since  we have the dwarf work already

[DS] We might need something that parses the dwarf and interacts with it. It might be more work upfront but more sustainable in the long term

[YD] FF can essentially replace source maps with dwarf today. So today it can translate dwarf into JSON, which contains the dwarfdump in JS objects and can be used to get line information plus everything else dwarf contains without low-level binary stuff. 

[NF] ITs all the debug info section right?

[YD] Yes, with expanded satellite sections. 

[PS] is that scalable? Dwarf is already quite compact but it’s large anyway.

[YD] Yes its huge, but I didn't find any issue with loading. With modern computers i think they can ingest that. But we cannot browse it for huge projects. I am only using it for small projects. The dwarf that we get from llvm has a lot of dead entries. If we purge all of those dead entries it will be a lot smaller

[YG] I’m a little worried that if we just take dwarf as the standard format this way and write the parser, etc that we will just be reinventing the wheel, and catching up with the feature set will be difficult.

[PS] My experience with playing with the prototype, is that using an existing library to parse dwarf it as not so bad. It’s complicated but not huge. I have the impression that using LLDB might be overkill

[YG] I haven’t experimented yet. Iw could be that lld is overkill. But when it comes to evaluating expressions etc that we’d get that for free.

[PS] LLDB doesn't know how webassembly works, so we would need to implement everything that is web assembly specific ourselves

[NF] They don’t have an assembly script interpreter for sure

[DS] The LLDB would buy you the language specific part of that. Ie C, Rust, etc. Maybe we should find out about that, because if it is just compiling with clang it might not be so useful

[YG] Unless you ship a wasm version of clang

[YD] It doesn't matter, we have 2 use cases. Compiling LLDB to understand wasm. If we discard that we have one case. Have lldb just read native dwarf

[DS] <discussion about expression evaluation parts and also having lldb as a debugger module>

[BT] one observation is that you can connect remotely, and the remote debugger has the sources and symbols, and the local one doesn’t have the confident data. In this model the local one would have to have all the symbols.

[YG] The way i was thinking of this is that the target (production wasm binary_ doesn’t come with anything. You would have to compile for that a specific binary with a wams port of lldb and the respective adapters to the debugging apis. You would have to ship a different debugger module for every wasm module that you ship, but it would not expose any confidential information. 

[BT] youd need to run the debug module on the target you’re debugging though?

[YG] I guess so, unless you have the thing that is talking between the vm and the debugging module. I guess that would be a problem in some use cases. 

[DS] I think you can probably extend this to a simple server where you do not have to package everything. With source maps you have a url to the maps. But we could have that for the symbols and other things. 

[BT] I am thinking about the run time impact. It would be interesting to explore the security implications. Having a server that spins up a module and just starts running it is obviously something to think about.

[DS] Ok, so before we sign off. When do we meet again and how often. The other thing is what do we want to do and when do we want to start doing it. NF mentioned that we seem to be on board with the general capabilities and we have a rough sketch. Do we want to start sketching out how those interfaces should look?

[agreement]

[DS] Nick do you want to start with what you had on your slides?

[NF] Yeah, the rough edges were ignored a bit, but i think that trying to match existing source map capability is a good checkpoint 

[DS] How often do we meet?

[BT] How aggressively are people working on this? We are happy to jump in wherever we can to help

[YG] Every couple of weeks sounds good, but i dont think we will have something in two weeks. Once a month makes sense

[NF] Why don’t we start with once a month? If our meetings run more that the full hour we can bump it up.

[DS] I will start a git hub thread about scheduling.
