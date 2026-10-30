![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the October 13, 2026 video call of WebAssembly's Threads Subgroup

- **Where**: Google Meet
- **When**: October 13, 4pm-5pm UTC (October 13, 9am-10am Pacific Time)
- **Location**: *link on calendar invite*

### Registration

None required. Join the WebAssembly CG and view the joining instructions on the [W3C calendar](https://www.w3.org/events/meetings/25056224-9f2f-4ce1-8c60-1ccfd43bac9d/).

## Logistics

The meeting will be on a Google Meet video conference.
No installation is required.

## Agenda items

1. Opening, welcome and roll call
1. Adoption of the agenda
1. Proposals and discussion
    1. Initial performance results from V8 shared objects prototype (Thomas Lively, 20 minutes)
    1. `publish` instruction ([#119](https://github.com/WebAssembly/shared-everything-threads/issues/119), Thomas Lively, 15 minutes)
    1. Acquire-release atomics status update and bikeshed ([#1](https://github.com/WebAssembly/acquire-release-atomics/issues/1), Rezvan Mahdavi Hezaveh, 15 minutes)
1. Closure

## Meeting Notes

### Attendees

- Thomas Lively
- Andreas Rossberg
- Conrad Watt
- Keith Miller
- Rezvan Mahdavi Hezaveh
- Ryan Hunt
- Zalim Bashorov

(Other attendees did not speak)

### Discussions

#### Initial performance results from V8 shared objects prototype (Thomas Lively, 20 minutes)

TL presenting [slides](https://docs.google.com/presentation/d/12BCBIpdcADGTg0ch9oR_7o15YDw1YmFm1LWM1MbV6Ok/edit?usp=sharing)

TL: I'm sure I don't need to remind anyone here what a shared object is, but just to refresh, the idea in V8 for now is that we're doing instance-per-thread shared WasmGC objects. We're not doing shared functions yet; we're trying to leave that to the future. What we really hope we can do is get some sort of MVP where we have some useful chunk of functionality that doesn't require shared functions. We still have web workers; all the threads are still based on web workers. You have a module, and we're still going to postMessage that module to the web worker just like it works today with linear memory threads, and instantiate the module on both threads separately. So you get two separate instances here. And then the new thing is of course the shared heap. When you compile a Java program like the Sheets calc worker, the idea is in the future all of your objects will go here on the shared heap, and so then all the instances and all the threads can be observing and accessing the same objects.

TL: The trouble begins when you try to put a method inside one of these vtables. The vtable is just a shared struct, and in a single-threaded WasmGC program compiled from Java, that vtable is full of function references. But I just said we're not doing shared functions, so how am I going to put a function reference in my shared vtable given the constraint that a shared thing cannot point to an unshared thing? These function references, because they're not shared functions, cannot actually be on the shared heap. They have to be on one of the single-threaded heaps. But then which one? There are actually two versions of bar, two instances of bar: one that closes over the instance on the main thread, and another bar that closes over the instance on the web worker. Which one's going to be in the vtable?

TL: The solution is neither and both, because instead we just replace all of the function references in the entire program with indices into tables. Each thread will get a table, and the table will basically have the same contents on every thread. So when I have an index like zero in my shared vtable, no matter what thread I'm on, I can go to index zero in the table and get function bar. Because the setup is totally mirrored on every thread, it doesn't actually matter that there are two different bars.

TL: So that's the setup. Basically what we did is we wrote a Binaryen pass called --make-shared-objects. This is upstream; you can run it. It does exactly this: it goes over the entire module and takes all of the WasmGC types, the structs and arrays, and makes them shared. If there happen to be any shared functions, it makes them unshared. It replaces every single function reference with a table index in the entire module. It actually replaces function indices with i31refs because that makes it a little simpler—you're replacing a reference with another reference, so things like null sort of translate cleanly.

TL: And you don't need to rewrite so many instructions, so that's what we did. We've got that pass. It does a few other things that I'll mention. And then we just ran the Sheets headless benchmarks before and after running this pass. Here are the results: we had the baseline, where we ran the Sheets headless benchmarks as they run today, single-threaded, nothing new, nothing unusual. And then with that transformation I described where we replace all of the function references with i31 ref indices into tables, it turns out that had a 3% overhead. So we did a version of the pass where that's the only transformation we applied and ran the benchmarks again; they were only 3% slower.

TL: The next thing we did was the same with extern refs. Extern refs have the same problem, and a lot of these extern refs are JavaScript error objects which are obviously not shared. A lot of the other extern refs are strings which are shareable, so there's some room for improvement here. But the other complication is that extern refs are leaving the module and coming back in all the time dynamically during runtime, and there's no way to have an extern ref and query what table index it is in, or whether it's in the table already. You could do it with extra imports and have that mapping on the JavaScript side, but that would be expensive. So for now we didn't do that, and instead every time an extern ref enters the program for any reason—whether it came in from an import or export, or whether you caught an exception and got an extern ref payload—whenever that extern ref comes into the program, we append it to the end of the table. So the table is just monotonically growing over the course of execution.

TL: This happens to work out for running benchmarks. Obviously, this is not productionizable. Out of, I think it was 16 or so different benchmarks, one or two of them could only get through a couple iterations before exhausting the 10 million cell table limit and crashing. So this is obviously not productionizable, but these are just initial experiments. This was a 9% overhead, and this is an overhead that we'll hopefully be able to get rid of by doing thread-bound data, which will let us have actual shared externs that can live in the shared structs that won't have to be put in tables. So that's another 9% there.

TL: And then in V8 right now, the shared heap does not have a young generation, and we thought maybe that's a problem. So what we did is we disabled the young generation on the normal heap and ran the benchmarks again. This is still not with shared objects; this is just with these module transformations applied and the young generation disabled. Disabling the young generation gave us an additional 42% overhead. This is massive, so obviously we're going to prioritize implementing some kind of young generation on the shared heap to get rid of that overhead.

TL: And then finally, we actually made the types shared and ran them on the shared heap. This was an additional 12% overhead, probably coming from things like optimizations being less aggressive when it sees shared things, and also allocations being more expensive because right now allocations on the shared heap all go through C++—they're not generated code—so there's some additional overhead there that maybe we can eliminate in the future. It's unclear what all is going into that.

TL: So anyway, that's it. Those are the results. The total is about an 80% overhead, which is pretty bad, but honestly better than I expected going in. I thought it would be several X. And so now we have some good prioritization data to inform the next steps in our prototype. And it's exciting to get real things running on the shared heap. So happy to take any questions. That's all I had. Yes, Ryan.

RH: You said that most of the extern refs are error objects. Can you explain why?

TL: Yeah. So if you remember with the exception handling proposal, we had this big debate about stack traces and whether a WebAssembly exception should have a stack trace. And the compromise we came up with was that no, it shouldn't have a stack trace because some languages want exceptions to be as fast as possible. And so if you do want a stack trace, then the way you get it is you call out to JS, have it throw a JS exception which then enters Wasm, and you can catch it with the JS tag, and then its payload is an extern that is sort of like the JS error that was originally thrown. And so they're doing that all the time. So anytime you have sort of a throw in the Java source, that's actually going to become a JavaScript throw. And then every time you have a catch, that's going to pop out an extern. Yes, Zalim. Yes, you guys do the same thing. And it would be nice to do something better.

RH: My understanding was that for exception handling we had standardized a capture stack trace flag on WebAssembly.Exception. So you could throw a WebAssembly.Exception in JS with an extra flag and it would have a stack trace attached to it.

TL: But you're still throwing the exception in JS, right?

RH: Yeah. So you do have to call.

KM: You throw it from JS, but you don't think you use the JS tag to catch it. You can catch it with a Wasm tag, right? Or no?

RH: Yeah.

TL: I see. I'm not aware of any tool chains actually using that, and I had forgotten that feature existed. So, we should probably all look into that.

RH: I don't know if that simplifies anything, but you can at least use a WebAssembly exception and get a stack property on it.

TL: Yeah, and then when you catch it, it's with a normal defined tag with whatever payload you want that's not necessarily an extern. Well, that sounds really nice. I wonder why we aren't doing that. Okay, Keith.

KM: I think the problem with it, though, is that the stack trace is attached to the JS—it's going to be a JS value in your GC, right? It's a dot stack property, like an ordinary stack property on the object, which might be problematic anyway because you need a special shared object and this won't have that shared object. Your error will still be unshared, or at least this stack property will be unshared. You'll have to have some way to put it on there like a normal JSO property, so maybe we need some extension to make it internal, or we just need to change the JS API to make it somehow internal.

RH: Yeah.

KM: To the object or our implementations.

TL: Yeah, right. So, it sounds like there's some nice room for improvement here in maybe how toolchains are doing exceptions on a single thread. But yes, for the shared heap, this doesn't help at all because we don't have shared exception stack objects. Maybe that's something we need to add, but that's pretty dangerous because once you're like, "Oh well, this kind of object, we'll just have a shared version of it," then where do you stop, right? We're going to end up with a shared version of basically every common JavaScript thing. Like, "Oh, a regex—why can't I have a shared regex, right?"

CW: This is super dumb, but could you represent the stack trace as a string? You just concatenate. And if it's a shared string, that kind of works for free.

TL: Yes, except it's not free because you have to prepare that string eagerly in advance, and often you don't end up actually needing the stack trace. So the worry is that that can be kind of expensive.

CW: Array of strings. I guess if preparing the string at all has a cost. Yeah. Okay.

KM: The way engines do it, at least for error instances, is they make a GC-allocated copy of each of the frames, and then they actually build the string when you want to look at it, and those GC-allocated frames are relatively cheap. You don't have to format them; you format them later. Certainly, we don't do this for the Wasm errors when you attach trace. We also don't lazily generate them. So it's possible that nobody uses them because they're not lazily generated either. And so then it's a chicken-and-egg problem where you have a nice thing, but it's slow so nobody uses it, and it doesn't get fast because no one uses it.

TL: Yeah, maybe. All right. Any other questions? Okay. As we do more stuff, I'll keep you all updated. Obviously it's exciting to have real prototypes running things, and obviously there are an enormous amount of problems both on the implementation side and feature-wise to solve here, so still a long road ahead. Okay, that's the end of that.

#### `publish` instruction ([#119](https://github.com/WebAssembly/shared-everything-threads/issues/119), Thomas Lively, 15 minutes)

TL: Let's talk about publish. There's a hot-off-the-presses paper from Conrad and everyone else about the Wasm 3.0 memory model, and I highly recommend you read it if you haven't, because it's great and it explains what we're going to do. One of the important things in the memory model is object initialization safety. All right, so if I allocate a shared struct on one thread and then somehow another thread gets a reference to that struct and then starts reading fields. It should never read uninitialized fields, right? It should always read the initialized fields, or if there was some write that happens to the field later, maybe it reads the result of that write. Okay, but you're never reading uninitialized data, and this is just baked into the memory model, so you can sort of just show that it's going to work out kind of axiomatically, and then everyone is happy.

CW (chat): https://dl.acm.org/doi/10.1145/3839465

CW: It's also just intuitively necessary for safety so that you're not reading random uninitialized garbage collected bits of memory. So the memory model needs to describe what we need to do for safety on a more intuitive level.

TL: Yes. And it turns out in practice on x86 you don't need to do anything, and on ARM, for example, you have to put a release fence at the end of allocation to make this safe, and the paper goes into the details there. So that's good, however, we have the same problem again in user space. Java, for example, provides very similar guarantees: specifically, what Java says is that if you construct an object and your constructors do not leak a reference to that object to another thread, then the other threads will only ever read the fully initialized final fields of the object. For Java, all bets are off if the constructors leak the object to another thread, and all bets are off for any field that's not marked final. But of course, we don't have final fields in WebAssembly, so we need to be able to provide this guarantee for arbitrary fields on the WebAssembly level. And if the WebAssembly constructors are still running—so just a bunch of arbitrary WebAssembly functions that happen to implement Java constructors—and they leak partially initialized objects (from Java's point of view) to another thread, then sure, all bets are off. But to properly implement Java, we need some way to guarantee that if these arbitrary WebAssembly functions that happen to implement Java constructors don't leak the reference to another thread, then the values written during those constructors to the final fields will definitely be visible to other threads, even if you don't use any synchronization right after the constructors are done. So you can do a non-atomic write to some shared location or a non-atomic read on the other thread of the object, and it should still read only initialized final fields. So how are we going to do that? The naive way would be to also put a release fence at the end of those user space constructors in WebAssembly. But this is a lot stronger than you need, and actually, it's technically not strong enough as well. It's stronger than you need because it inhibits all optimizations and affects all memory locations rather than just your object. And it's technically not strong enough because the fence doesn't actually do any synchronization unless there's release-acquire or stronger synchronization afterwards, so the fence is actually insufficient. Any questions about the problem here?

CW: I'm not sure it's a problem that the fence is insufficient. I thought the problem here is more motivated by not having all the optimization opportunities you wanted.

TL: No. It's also that the fence is insufficient, and C++ has the same problem. Remember, right? The C++ release fence is technically incorrect and just happens to lower to the assembly you want on every platform.

CW: But that seems to be mixing up a couple of things, right? We're in control of the memory model. So we can write the memory model so that the release fence is sufficient to give us all the initialization behavior we want.

TL: Sure, we could. That would be one solution.

CW: I'm in support of the publish instruction, but I see it as more motivated by enabling optimization opportunities in code generation and binary and V8 optimization time.

TL: Yeah, okay. Yes, thank you. One solution would be to beef up our release fence semantics so that it's sufficient. The other is to do this special publish instruction, which is kind of like a fence, but it scopes just that single object. Basically, you publish your object, and then the memory model says that after you've published the object, any sequence of operations that leads to it being read on another thread afterwards, as long as the object wasn't leaked before the publish, then everything works out and you'll see all of the writes to that object that occurred before the publish. For example, Java would just insert a publish at the end of running all of the constructors, and then Java semantics would be trivially preserved. The other benefit of publish that Conrad mentioned is, because it's scoped to a single object, it's a lot easier to optimize, right? For example, if we ever see a struct.new and then a publish, we can get rid of the publish when there are no writes in the middle because that publish is redundant with the sort of implicit publish that's happening at the end of struct.new. And if there are no writes in the middle, there are no new writes getting published by that second user-space publish, so we can just throw it out. That's the kind of optimization we can do. Also, we know that only that object is being published, so writes to other objects aren't affected and can still move around. The way it's currently proposed is that publish takes an arbitrary reference type, which seemed a lot nicer than having to give it a type annotation so that it would publish a specific struct type, for instance, or a specific array type. If we just make it take an arbitrary reference type, then we don't need a type annotation, and then it just does nothing for most reference types. But for structs and arrays, it has this effect on the memory model, and then it returns its input. Andreas, maybe you tell me, this might be controversial. I don't know.

CW: Well, actually, when we end up on T, right? Because originally T returns the local type, and then I think there was some thought that we would strengthen the typing rule. Did we actually do that?

TL: No, we never did that.

CW: Well, then this is in exactly the same bucket as select. Is it not? Help me understand why.

AR: No, it's not, because select has two inputs of the same type, right? So, you kind of need to unify them.

CW: So is this better than select?

AR: This is much better than select. I don't see any problem with it. It's just completely polymorphic in the reference type, right?

TL: Okay, great. I was hoping you would say that, and I was fearing you wouldn't, but if no one sees any issue with this, then fantastic. This just seems a lot more convenient than having to use an extra local, because you're allocating an object, you're going to do something with it, and you also want to publish it. Normally, if there are two different things you want to do with some value, you have to put it in a local and then use a local.get. Having publish return its input untouched means you can just stick it in right after the end of the constructor, and you don't need an extra local before you go on to do whatever else it is you're going to do with the object.

TL: I have a list of open questions now. We just talked about the typing, and I guess it's fine, which is cool. What does it do on null? I propose that it does nothing without trapping. I don't know, could go either way on that.

TL: Should publish return its input? The answer was yes, that seems fine. With polymorphic stacks, it would just push bot, so it still returns its input, but hopefully we solve that problem. That's all I had. Keith, go ahead.

KM: Okay, I'll start with the first thing on the null one because that's a smaller topic. But I think ideally I would almost prefer traps on null, because in theory you could—I don't know if it really matters actually, but in theory you could fold this into a store release or something if your hardware supports those in one instruction, which can have benefits sometimes. I guess maybe it doesn't matter. The upside would be that if you know the two operands are the same value, then you know they trap together and so you're fine, assuming your GC supports actually dereferencing on null. In theory, maybe that's an optimization we want to be able to do. But then if they're not, maybe that gets weirder, but maybe it's fine also because you have to have the store before. Anyway, just some thoughts thrown out randomly. But the larger question is: does this need to be an actual instruction or could it just be a tooling convention that says—assuming we take Conrad's suggestion and we can beef up release to do what we want in this context or change the behavior—would we prefer to have this instruction, or would we prefer to have some kind of tooling convention that says this store release or this release fence is what my publication barrier is?

CW: Yeah. So the main issue is that the release fence also does other things on top of acting as a publication barrier, so it's much harder to optimize it away if you have an OB. So really, I see this as actually motivated in the other direction, if you think about the natural compilation scheme for Java. If you have a Java constructor that might need to call super and then do a bunch of in-place mutation of the this object, and then eventually you finish all of your constructors and you're ready to kind of shoot the object off into the world, the Java JVM in native, once all the constructors have finished being called, will actually put a release fence at the end of all of that mutation to make the access to the object safe with respect to the garbage collector. The problem is when you try and compile that arrangement of constructors to Wasm, you can't know where to put in the release fence for free; you have to have a specific instruction for it. And we could either make that the release fence instruction or we could make it this publish instruction. The optimization opportunity we're looking for is in the simple case that you actually just call the Wasm-level object constructor, which also needs to have a release fence inside it just for safety with respect to the engine garbage collector, and then you also need a second release fence for correctness with respect to the source language semantics that you're trying to preserve. How do you recognize opportunities to merge those two release fences together and just emit one release fence instead of one after another—one coming from the create object instruction and one coming from the compilation scheme? If you're just looking at the straight-line code and you see new shared GC object and then release fence, it's very hard to recognize that you can delete the release fence. I guess it's not impossible: you would actually have to reason backwards to the object allocation and reason that it would be safe to decompose the object allocation into kind of micro-instructions, and then there'd be a release fence micro-instruction that you can optimize away.

CW: But if you have an object allocation followed by a publish of that object and you can detect it doesn't escape, it's very trivial to realize you can optimize the publish away. So it becomes a much easier optimization opportunity.

KM: Wait, how do you get rid of the publish? You still need the publish because the out of order could happen later, right?

CW: If, in the dream case, you have just the object allocation instruction, no further field mutations, and then a publish instruction, publish on ARM needs to get compiled to a release fence, but that becomes redundant with the earlier release fence of the object allocation.

KM: Wait, are you saying you keep the publish, or are you saying you keep the original one? If you keep the later one, isn't that already basically the same thing that you'd have to be doing for the general case of eliding releases because the object can't have escaped in between?

CW: Yeah, you've got to keep one of them. And it's just a case of how easy it is to recognize cases where you can optimize at least one of them away.

TL: And in the engine, you can look at both of these and optimize them individually. In Binaryen, there's no way for us to optimize out the implicit release at the end of struct.new because that's just part of the instruction's semantics, right? So in Binaryen, with all these optimizations we have now, what can actually happen is that all of your Java constructors get inlined, and what you get is a struct.new followed by a bunch of writes to the object from those inlined constructors, followed by a publish. What Binaryen will further do is see all those writes to that allocated object and say, "Hey, I see that we're just writing fields to this new object that isn't escaping." So, we're actually going to move things around and put those writes as part of the struct.new. We're just going to initialize the object in place already with those values if we can move everything around properly, which you would expect to be able to—there shouldn't be too many side effects in a constructor. And then what we're left with is just the struct.new with all of the fields ready to go, followed by the publish. At that point, Binaryen can get rid of the publish. If that were a release fence on the Binaryen side, we wouldn't be able to get rid of it at that point because that would have much broader effects that we couldn't reason about beyond that one object.

TL: And Keith, your original question was, what if we just have a user-space convention? What you could do is have a user-space, toolchain convention with an annotation on that release fence that says, "Hey, this release fence is really just scoped to this struct that comes right before it." There are a couple of practical problems, like which struct.new, how do you refer to it? So, you have to figure that out; it's a little complicated. And second of all, that would work—Binaryen could still optimize that—but any tool looking at that module that doesn't know about this annotation now thinks that the semantics of the module have changed. If there's some model checker in an automated fuzzing workflow or something, it needs to know about this annotation, which means the annotation needs to be part of the memory model. We need to give formal memory model semantics to this annotation. And at that point, why is it an annotation? It has to be part of the core spec; it has to be part of the memory model. Just make it an instruction. So I think making this an instruction is much simpler for all those reasons.

AR: Yeah, this all sounds plausible to me. I just want to make sure that we're not doing premature optimization here. Did you measure what overhead the other solutions would have in practice for real programs? Is that even relevant at all, or is it just something you believe might matter?

TL: Yeah, it's a good question. I think the only realistic alternative solution would be to use the full fence after allocation. No, we have not measured the relative overhead of doing that, and the nice thing about publish is that it's so trivial to optimize; we already have all the optimizations for it in Binaryen. So if you accept that this one extra instruction is not too much of a burden to bear for implementers, then I think it's strictly a good idea. If we wanted to save this one instruction, then yes, we could go back and do experiments and compare it with a full release fence. And with AI, those experiments are now very easy to run. So if somebody is very interested in the data and is hesitant about accepting this instruction otherwise, then we could do that. But no, we don't have that data yet.

KM: If we're going the route of arguably prematurely optimizing everything, there are possibly benefits. It depends on the architecture and possibly even the SSC in question, but having a store and publish combined could be beneficial because of optimizations at the microarchitectural level. I don't know whether we want to do that or not.

TL: Yeah. With this, where publish just returns its input, it's very easy in the Wasm source to have publish and then store. And that's the kind of instruction fusion that I hope would be okay to do in an engine, right? It's very trivial to pattern match that there's a publisher and then a store, so we'll do something special, right?

CW: The other issue is really that you would want a different variation of publish for every different kind of store.

TL: That would be unfortunate.

KM: I mean, you could do that. I guess that gets into the hazard we've tried to avoid of adjacent instruction fusion. That was part of the reason, I think, that we added with flags. People were worried about having a flags value because, in order to get good performance, it would entail requiring the instructions to be adjacent to each other. And that was some of the concern there. So I don't know if that concern applies here, but it feels like it would be the same argument.

TL: Yeah, I don't know. At this point, we have a lot of precedent for pattern matching little snippets of instructions and doing special stuff. Also, the optimizing engines are already doing way more complicated things than that. So, I'm not sure how much water that argument holds for me, but, yeah, it's fair.

KM: I agree. I'm just relaying the feedback I got when I said that we should do flags instead of wide arithmetic. And then everyone was like, "Oh, but then you have to worry about the flags being far away from the use, the def being far away from the use, and tooling." So, I don't know. I'm just relaying that feedback.

AR: So I guess I'm less concerned about this one instruction, but I wonder if that might lead to a proliferation of additional ad hoc fence instructions that we introduce. I guess I don't understand enough of the context to be able to tell, but that's the kind of thing I would want to avoid.

CW: I can only reassure you with vibes, but this publication concept is pretty fundamental to GC-ed languages, so I do see this fence as paired in a reasonably fundamental way with the concept of being able to allocate a GC object of any kind in Wasm.

AR: Okay, fair enough.

TL: This also follows the pattern we have in WebAssembly of taking things that the engine has to do internally and then exposing them to user space. It's just making things lower level. This is already built into struct.new. We should be able to access that functionality without needing to do the rest of the things struct.new does, so it's a bit of a decomposition.

AR: Yeah. And that makes total sense to me. I just wonder what the wider picture is here, if there is any.

TL: Yeah. My vibes agree with Conrad's. I'm not aware of any other use case we'd have for a special one-off fence.

AR: Okay. Cool.

KM: I do appreciate the concern, though, about having a proliferation of fences. But I agree that this one is fundamental. We should be careful to make sure we think about all the weird edge cases so that we don't end up with a million weird fences.

TL: Yep, I agree. That would be bad.

CW: Yeah. In fact, we'll probably continue using this publication fence for any future GC objects we have to add that have some kind of concept of initialization as well.

AR: Sorry. What do you mean by that?

CW: Well, you're putting me on the spot. I don't know any other kind of GC-allocated object—something that would need to be non-nullably initialized that's not a struct. I'm not creative enough.

TL: I'm thinking about shared continuations, but I don't think those are going to need this.

CW: You never mutate them after they've been created. Yeah, it's got to be mutable.

TL: If we got some new kind of combined struct array that supported interior pointers.

AR: Oh, you mean like flattened arrays or structs?

TL: Yeah, something like that. Maybe we just call that a normal struct array and so it's not new. Who knows?

TL: It sounds like this is probably fine to everyone. I'll probably merge a PR for this, and we'll just go from there.

#### Acquire-release atomics status update and bikeshed ([#1](https://github.com/WebAssembly/acquire-release-atomics/issues/1), Rezvan Mahdavi Hezaveh, 15 minutes)

RMH presenting [slides](https://docs.google.com/presentation/d/1tw-KXV7Tevc5CPsti4xxhNZYfX64WHJ7ZBhfKwbsCEo/edit?usp=sharing)

RMH: Alright, so the update that I have is pretty small. We have updated the overview with these details. Alex filed three issues on the repository and we addressed all of them. First of all, we clarified that the setting of the ordering bit on non-atomic instructions should be a decode or parse error, not a validation error. We also clarified the text syntax. We mentioned text syntax and binary encoding in the text of the overview, but we didn't have these examples, so I think that's clearer now. We clarified the text syntax, we clarified the binary encoding, and spec test additions for issues 26 and 27 are in progress. So if you're implementing the proposal, go check the overview and make sure that you have all the details that you need. And if something is still missing, please file an issue and we will address that.

RMH: And now for the discussion. We already have this issue filed on the repository about whether we want to have separate acquire and separate release ordering in this proposal. Last time, what Keith mentioned during the voting for Phase 3 was the exact same thing: do we want to add separate acquire and release or not? So these are the pros and cons of each approach that came to my mind. They are not complete, but I think that's a good start for the discussion. I think if we keep this proposal as is and add separate acquire and release in the next proposal—which is going to be adding a weaker memory ordering like load atomic, store atomic—then we don't have any churn, we don't need to change any implementation or add any tests, and we already have very simple validation because it's just one kind of memory ordering that we check for all the instructions. But in the future, maybe we have some encoding awkwardness. If we add separate acquire and separate release at some point, we need to have backward compatibility, so we probably won't be able to remove acquire-release load, and then we may have some inconsistency or mismatch.

CW: Just to make sure I'm understanding, this is just about the instruction encoding, right?

RMH: Yes.

RMH: On the other hand, if we add separate acquire and release in this proposal, then the good point is that we will have accurate naming. It's not confusing and it will be compatible moving forward. But we need to do more spec and test work. We need to have instruction-specific validations, and I think load, store, and RMW implementations won't change a lot—maybe just the test updates needed for them. But for fences, now we have only an acquire-release fence, but we need to add acquire fence and release fence, which are different and weaker fences. So these are the pros and cons that came to my mind, but they are not complete. So we can discuss which approach we want to move forward with. Keith, please.

KM: Sorry. Why does this entail that we need to have a fence? In the original proposal as it stands today, you get the acquire semantics with the acqrel load.

RMH: We have fences in this proposal. We have acquire-release fences.

KM: But I'm saying, why do we need to have just an acquire fence if we have an acquire load?

RMH: Oh, so I think if we have separate acquire and release, then we have to cover all the instructions that we currently have in the proposal and make sure that all of them accept this.

CW: The minimal version of this would be that even though we have an encoding for acquire on its own and an encoding for release on its own, and we know we'll have these fences in the future, for now it could still be just a validation error.

KM: Right. That's what I'm saying. With the current proposal, we don't have to change the total space of instructions that we support—we effectively already support them. I don't think there's necessarily a problem with adding those fences because they're de facto there, since you could just load zero-index memory acquire as your fence. I guess that doesn't work.

RMH: Okay. So what you're saying is that we can have separate acquire and release. So we will be able to have acquire load and release store instead of acquire release load and store, and that's it.

KM: Correct. It would effectively be an encoding change, but the only change would be how those instructions get encoded when you want that behavior, rather than any new functionality added.

RMH: I see. Okay. Thanks.

CW: Yeah, that would have also been my default assumption. I think there is further bikeshedding we could do about adding just an acquire fence or just a release fence. They're relatively harmless additions, but if we wanted to avoid opening too many fronts of discussion, I would see the bare minimum version of this as just an encoding change.

TL: Okay. Are acquire fences and release fences meaningful in the absence of a weaker memory ordering? They are, right?

CW: Not for the formal semantics in any way. You could potentially view them as a machine assembly emission optimization in some circumstances.

TL: Well, we had the same thing with the original atomics, right, where the fence there is a no-op, and we added it so that old programs that were compiled by LLVM that would get linked with new programs where the fence actually becomes meaningful wouldn't be broken by having their fences dropped.

CW: Yes, exactly. It's exactly the same thing.

CW: Well, it's actually even sillier than that. It's just old programs that don't work according to the formal model, but just work based off of vibes because you run them and they happen to have the right compilation scheme. The majority of C programs would have just broken in the real world if we tried to do something too close to the formal model. This is the sad side of relaxed memory: no matter how good we make the formal model, sometimes we just need to make pragmatic decisions about machine instruction emission, otherwise too much real code breaks. No, to be clear, this is a problem of C programmers. We didn't cause this.

TL: At any rate, if we do add separate release and acquire, it seems very harmless to me to also have release and acquire fences that might technically be no-ops for now, and in the future they'll mean something.

CW: Yeah, they'd be formally no-ops. You would absolutely need to emit the correct machine instructions in the actual engines. Same argument as for SC bends. There's just too much real code out there that assumes something sensible gets emitted in the machine code, even if it's formally wrong.

TL: Okay. Well, that's fine, too.

KM: Acquire. You might have written your program entirely for x86 or something, assuming that you only did a release, but then you never did some other thing. I can say release is fine for ARM.

CW: Yeah, there are all sorts of weird things you can do, especially pre-C11, and I don't want to describe them in detail in case I accidentally convince people it is okay to optimize them.

TL: All right, so this is like a total bike shed, right? We could just go either way. I wonder if we should just do a straw poll to get a sense of what the prevailing opinion is. I hope that nobody wants to die on a hill about this.

CW: My only concern would be that I don't want us to accidentally add release fence and acquire fence in kind of a cowboy way. So I'm fine with us adding them, but we really do need to be disciplined about emitting the machine instructions.

TL: Yeah, I would like to talk with you about that, but yes, that sounds fine in general. Okay, so if everybody is in the chat, we'll say option one is the status quo where we just have an acquire-release ordering. You do a load acquire-release, but everybody knows the semantics are an acquire load, similarly with the store. So that's option one. Option two is we separate it out. I guess we'd still need acquire-release for the fence, so we'd have all of acquire-release and acquire and release codings. Details may be TBD, but the general idea is that a load acquire-release would not be allowed. You would have to do a load acquire and similarly a release store. Okay, so that's option two.

KM: Wait, shouldn't there be a third option which is just the encoding change and no fences?

TL: I think the high-order bit is the encoding change or not the encoding change. And then if we do the encoding change, there's a bunch of little details to figure out, like the fences, like RMWs. Right, there's a bunch of little things, but I want this to mostly just be about the encoding change or not. And then if we decide to do the encoding change, we can figure out those details. Does that sound reasonable? So, if you prefer the status quo, single acquire-release encoding, please type one in the chat. If you prefer the separate encoding with separate acquire and release and we'll figure out the details, type two in the chat. 

| 1 (status quo) | 2 (separate `release` and `acquire`) |
|--|--|
| 1 | 2 |

TL: I'm not going to call that consensus either way.

KM: You got aggressively neutral feedback.

RMH: So I will change the overview and prepare everything to bring to the next CG meeting for consensus on this change. Does that make sense? Or, because it's just bike shedding, can we just move forward?

TL: Yeah, I think we can just move forward with whatever because nobody cares.

CW: I would say I think it's pure bike shedding and we don't need to think too much, so long as we still just have a release-acquire fence. If you really want an acquire fence, I would like a little bit of discussion about that.

RMH: Okay.

KM: But also, weirdly, we're on opposite sides of which way to go with the encoding. So, I don't know.

CW: No, I'm living in the world now where I've been defeated and we are going to the separate release encodings, and I just bought the best version possible.
