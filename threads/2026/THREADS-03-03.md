![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the March 3, 2026 video call of WebAssembly's Threads Subgroup

- **Where**: Google Meet
- **When**: March 3, 5pm-6pm UTC (March 3, 9am-10am Pacific Time)
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
    1. Status updates
    1. Waitqueue as a packed type ([#102](https://github.com/WebAssembly/shared-everything-threads/issues/102)), (Thomas Lively, 15 minutes)
1. Closure

## Meeting Notes

### Attendees

 - Thomas Lively
 - Benbuck Nason
 - Conrad Watt
 - Daniel Phillips
 - Jakob Kummerow
 - Manos Koukoutos
 - Matthias Liedtke
 - Rezvan Mahdavi Hezaveh
 - Ryan Hunt
 - Sankalp Jha
 - Steven Fontanella
 - Yage Hu
 - Derek Schuff

### Discussions

#### Status Updates

TL: On our agenda today, we have a continuation of the waitqueue discussion from last time. But I thought we could start off with some updates. So, I will share my updates. I've been doing a little bit of work in binaryen on the optimization of relaxed atomics. So in particular, allowing memory operations to move past acquire and release operations but only in the single allowed directions. We'll see what happens with that. Right now the binaryen effect analyzer has no notion of directionality. So fixing that is a fun initial project. And I don't know, except for very careful manual testing, how are we going to catch bugs here. Because we're not really going to have fuzzer support for finding bugs when we reorder things incorrectly. So I know we have an issue about fuzzing techniques for multi-threaded code. But this is becoming perhaps more urgent. Steven, can I put you on the spot? Do you want to share an update about what you've been up to?

SF: For the waitqueue support, we have the initial support in binaryen. So we support `struct.wait` and `struct.notify`. We have the parsing and some initial roundtripping, and all of the passes can support interpreting it. The effects analysis. Besides that, I'm working on the interpreter support in binaryen and the fuzzing support. But I think for now, at least, it should support if you want to optimize a program that uses waitqueues.

TL: For now we have the packed type version implemented just to match V8. Rezvan, can I put you on the spot? You want to share an update?

RMH: Yeah, sure. So, we completed the implementation in Liftoff for V8, and TurboFan also completed to a good extent. The next thing I'm going to work on is figuring out what benchmarks we can use to possibly get some numbers and to compare between the acquire-release and the sequentially consistent versions of the instructions.

TL: Thanks, Rezvan. Exciting progress. Manos, do you want to share what you've been working on?

MK: Sure. I've been implementing the packed type version of waitqueue in V8, and the implementation is mostly complete, although we still have a couple of bugs that we're trying to fix with some data races, but that should be feasible to fix.

TL: Anybody else have any sort of status updates? Derek.

DS: Yes, I have started working on this now in LLVM too, adding support in the back end, and have not yet, but will soon try to wire up everything from C and C++.

TL: And that's for the release acquire stuff, so that we'll be able to get those benchmarks that Rezvan finds working end to end.

CW: Are these the same benchmarks from the Java paper?

RMH: So the benchmarks that I started looking into are the ones from the paper. We don't have access to the link that is shared inside the paper. So I'm going to contact the authors and also look into the repositories, because they collected benchmarks from other repositories. I will look into those repositories as well and try to find the benchmarks. So that's the first set of benchmarks I'm looking into.

CW: If it's ever helpful for me to annoy them from an academic email address as well, let me know.

TL: Thanks for the updates everyone. It's exciting that there's so much work going on in this space. So let's talk about waitqueues again, and maybe for the last time, that would be nice.

#### Waitqueue as a packed type ([#102](https://github.com/WebAssembly/shared-everything-threads/issues/102))

TL presenting [slides](https://docs.google.com/presentation/d/1MvE9Gktuw02D6lHif2ox78qeI8pv684jA_CJDuUmbuU/edit?usp=sharing)

CW: This last one seems a little scary. I'd want to think through it in more detail.

TL: In terms of the actual language, this bottom half is not visible. That's just an implementation strategy. So to the extent it's scary, it's scary for implementers. But it's no scarier than just doing the packed type thing, which we're already doing because that seemed the easiest.

CW: In this design, are you expecting that `ref waitqueue` will be a subtype of anything that looks more normal, like a struct?

TL: Yeah. So this is just an implementation note. The actual design here is exactly the original design.

CW: So how could you potentially have a struct with a field that's a super type of ref waitqueue that then wouldn't be inlined, and would that cause you to have problems with code generation?

TL: The waitqueue is not inlined here. This is the user visible struct that has a ref waitqueue field. The waitqueue is not inlined in that. This is different from option two, where in the user-defined struct, the waitqueue is an inlined field. It's not a reference.

CW: Maybe I misunderstood what "desugars 2" means in this context.

TL: Yeah. So in WebAssembly, the language, there's just an abstract waitqueue heap type, and because it's a subtype of that defined struct type, it has a visible i32 field that you can struct.get and struct.set, and so on. And this is just saying that in the implementation, the representation of this abstract waitqueue heap type would just be the same as a struct type with a special field that is not something any other struct type can have. And so when we, for example, do a cast at runtime from waitqueue or to waitqueue, this is implemented exactly the same as a cast to any other struct type because internally the waitqueue just is a struct type, even though it's not in the WebAssembly language.

CW: Oh, okay. I think I understand.

CW: So, is this essentially like saying, "Oh, it's unproblematic for us to implement the packed field, but we're just not going to expose it to users."

TL: Exactly. So internally we use the packed field, but it's not exposed in the language.

CW: And the reason for that is because the user level copy semantics is irregular.

TL: Exactly because people didn't want the packed field in the language.

RH: Is there any downsides to number three? I mentioned the indirection may be okay, but at least to me this one seems the conceptually easiest. You just add a waitqueue heap type and a single instruction to get the control word or to construct it with referencing a control word, and then it just kind of works out. We don't have to sweat at all about type system stuff or anything like that.

TL: Manos, you've been actually implementing this stuff. Can you think of any issues this would have? What's your opinion?

MK: I can't think of any issue right now. So from a perspective of the waitqueue itself, this is quite similar to the packed field implementation, right? Except instead of an i32, we have a reference at the beginning, so I don't see any major issues. Also, I guess all the subtyping issues get resolved here because there is no subtyping.

RH: I looked at the issue just before the meeting, and of all the different options, this one seemed to be the one I prefer the most. I don't know, I haven't gone to implement option number one, so I don't know all the tricky things with casting or all that. I just know, for example, our struct code is very optimized and complicated in our VM, and it's one of those things that if we can avoid adding special cases to it—for instance, if this struct is inherent, has a waitqueue, and we have to deal with finalizers and all sorts of stuff as a special case—then that would be really helpful. Which is why I like number three. Number four was also fine, but three seemed like it didn't have many downsides.

CW: Sorry if I'm being slow here because it's like 1:30 a.m. but what's the difference between three and the new desugaring approach you explained? Is that just a refinement of three, or is there an observable difference?

TL: It's pretty different. So, again, the desugaring thing was just a way to implement one. So, the difference between one and three is this subtyping. Here we're saying that the waitqueue is a subtype of this struct type. And so the waitqueue inside itself contains this i32 field that you can construct, get, or set. Three, in contrast, the control word is not inside the waitqueue now. Now it's in some normal struct outside the waitqueue and you have to add this extra instruction to get a reference to that other struct and then you can manipulate the waitqueue the control word.

CW: Oh, you actually need a separate instruction. Yeah, sorry that was my misunderstanding. Yeah, I got it. Why does the control word need to be observably boxed if you just have special instructions to get and set the control word?

TL: Okay, so that's another option here. We could just have waitqueue be its own thing with a control word and a bunch of new instructions to get and set the control word. I should have added that as an option here too. The problem is we have so many struct accessors for i32 fields if you count all of the read modify write operations and all of the different memory orders and all of that. And we want to be able to reuse all those instructions for the control word rather than define copies of them.

CW: Is this not something we discussed before in other contexts, and we thought, oh, this was something about memory loads and stores, right?

TL: Yeah, similar to the discussion we're having for the multibyte array access proposal.

CW: Yes, that one.

TL: Do we reuse a bunch of existing memory accessors or do we just copy a bunch of instructions?

CW: I thought we had gone in a different direction for that where we were going to take all the memory instructions and add a modifier to them to retarget them to the arrays. That seemed to be where I remember we left the conversation.

TL: Yes. So for that proposal, basically, the options are brand new instructions or new variants of existing instructions. For example, if you have a different bit, then you can give it an array type. Either way, it's not just reusing something existing. Here, we have the opportunity to just reuse the existing struct accessors, and there's no extra bit, no new anything; it's just a struct accessor. So I think that is clearly a win if we can make it happen.

CW: But it does mean you have to box the control word like this. It's actually observable; there'll be an extra indirection every time you want to modify the control word.

TL: That's true. So if we go with three, that's the case. If we go with one, that's not the case.

CW: But I could imagine a variant of three where we take some lessons from the multibyte array accessors, and whatever solution we pick for that, we do the same thing to avoid redundancy with a version of three where the control word isn't boxed.

TL: Right. I think another way to view that is that this other option is also a variant of one without the subtyping. Right? So it's a variant of one where waitqueue is just like its own abstract heap type but it's not a subtype of this struct type.

CW: I guess my point is we shouldn't overindex on being scared of having to duplicate instructions because we're already going to have to engage with this problem in other proposals.

TL: The control for multibyte array access, though, that question has not been resolved. We don't have a guiding principle and a precedent that we've all agreed on yet.

CW: But we've got to resolve it. And this is going to come up again when we do some other first class thing.

TL: Yeah, we could consider them together and try to go the same direction in both.

RH: How many of these objects are we thinking are going to be allocated? Is it like one per mutex in the application, or is it the sort of thing like every Java class implicitly has a mutex?

TL: One per mutex is what I would expect. If you actually just implemented Java as-is, then I believe every single class would get one of these things. We would try to optimize them out. I'm sure they're not all used. I imagine we can be pretty successful with that. We do extremely aggressive optimizations. But yeah, it's a good question.

CW: Yeah, to be honest, the more I think about this, the more I'm scared about a version that has indirection or for three because it seems like quite a sad cost to pay every time you want to access the control word.

TL: Mhm. You're thinking about the performance of just following that pointer or the memory overhead?

CW: Yeah, just everything, it's an extra indirection overhead that we're effectively putting into the language, and if you want to use waitqueue, you can't avoid it no matter how clever you are.

TL: I'm a little more worried about the memory overhead here. Because you've got an extra pointer, you've got the extra struct header here. This adds up, especially if you have a whole ton of these. I imagine you're mostly modifying these control words when you're about to go to sleep on a mutex or try to acquire a mutex. In the fast case where there's no contention, I guess maybe it would matter that you're doing that extra interaction. Certainly in the case where you actually go to sleep on the mutex, it doesn't matter at all.

MK: How does this dereference interact with atomic accesses to the control word?

TL: So this would be an immutable reference. So you do your waitqueue.get control word, and then you have a reference to this struct, and then you could do atomic whatever you want to the control word once you have the reference to the struct. And I guess if you were doing a bunch of operations on the control word in the same function, you would only need to do this get control once because then you would already have a reference to the struct.

RH: I was thinking through what people would actually hold a reference to, and they would hold a reference to the waitqueue, not the underlying struct. They wouldn't try and cache that because you can only do the wait or the notify on the waitqueue. Yeah. My gut feeling is that the indirection, at least in terms of the cost of requiring the mutex, is probably not going to be the big thing. It's an atomic load and comparison on the control word to see if you need to actually do the lock or not. So I would imagine that that would dominate the cost, but I don't know. I think the big question is that it's nice in theory that the packed type could maybe inline some of this, but I think there's just going to be interactions to feasibly implement it. And also, with the lock generally, I think there is some amount of allocation to add yourself to the waitqueue itself too. So that's not exactly a free operation either. I'd prefer to optimize for a little bit of simplicity here and benchmark it, and if there's a problem, try and add some extra instructions to remove the indirection, but that's mostly just from my fear of a) touching our struct code and b) anything to do with the type system because both of those things have hit us.

CW: I don't think so, please correct me if I'm wrong, my interpretation of the argument against inlining, at least in the case of three, isn't so much that it makes the type system more scary. It's more the boredom of having to deal with the duplicated instructions. Is there a more fundamental issue we're seeing than that?

RH: No, that would be my second step. First, I'd say, have the indirection, see if that works, and then do the extra instructions or find something like that. And then after those options, my preference would be to figure out a type system extension.

CW: Okay. I think I'm almost with you except I would swap two and one.

RH: Why?

CW: We're working at the language level here, and this is the best interface anyone's ever going to be able to interact with to get waiting for GC languages. We should put in a bit of extra effort to not put in a random indirection that's not necessary.

TL: Yeah. So the question is, do we start with three and then try to benchmark it and characterize whether there is a problem, and then only reactively try to remove that indirection? And then if we do decide to remove that indirection, there are two options: you introduce some subtyping so you can reuse the existing struct accessors, or you don't introduce new subtyping and you just duplicate all the struct accessors. Actual tool chains trying to produce code might have an opinion about that, but I'm not sure yet. It might be a pain to actually have different instructions for modifying this thing. I don't know. Okay, so the question is, do we start with three and then benchmark and then reactively try to make it better, or as Conrad is saying, do we just try to make it a little better to start with? And it depends on how confident we are that the benchmarks are going to show a problem, right? If we think that there's going to be a measurable problem, then we should just skip three and go directly to something that eliminates the indirection. If we think the indirection probably won't matter at all in any case, then of course starting with three is fine. So I think it just depends on your priors there.

CW: I expect that at least on x86 you could come up with some slightly silly looking low contention microbenchmark where it's very visible that you're having to do an extra access to get to the wake just because on x86 atomic loads are the same as regular loads.

TL: Yeah. Jakob in chat said that instead of introducing a bunch of new instructions in the case where we don't have subtyping, we could also just update the typing of the existing struct accessors to say it takes a waitqueue. Unclear what you'd put as the type index for struct.get in that case. Maybe it'd have some special sentinel value that means that it's a waitqueue.

CW: Yeah, actually, I wouldn't be against that. I think that's a reasonable solution.

TL: Maybe that could work out. Having this sentinel value for the type index is very similar to having this extra bit on the memory loads and stores to say that actually these are going to an array. So it's changing the immediate of the instruction to say that you're actually accessing something.

CW: It doesn't necessarily extend to what we're trying to do with arrays. Or were you just about to say it does? But were we planning to use the memory immediate as minus one to show, because that's not a bad idea actually.

TL: What we've currently implemented in binaryen at least for that is that we've allocated bit 4 in the alignment field, and if that bit is set, then it's going to access an array and it takes an array type immediate.

CW: Yeah, that actually probably is a better idea. Okay. I don't mind that. Well, also I mean as a theme for solving this problem,

TL: Yeah. I don't know. We could get into the weeds with that. Jakob says, "For the record, his preference is the packed type." Jakob, with restrictions that you can't use the packed type in arrays, or with some magical array copy that requires special casing to only copy the control word.

JK: No strong feelings on that. I don't think waitqueues in arrays are particularly useful, and so I would be fine if we just limited it to structs, which is what we discussed in the last meeting, right? Some of these proposals can actually be seen as syntactic sugar for each other. And so, if we had a packed field that is limited to only show up in structs and limit it to being the second field after an i31, then it's basically the same as design number two or whatever it was. Actually, not quite, because in this version of this design, there's still more flexibility, right? You can have any number of waitqueues in a struct. So I guess it would be closer to the special subtype thing where you could read that as just shorthand in the binary format that says now append one of these fields as a packed type to the supertype struct. So I don't feel strongly about any of these differences, and we can probably implement all of them except for the one that has the explicit indirection the other way around. But all of the others we can basically implement the same way under the hood and just do the desugaring that we want in the parser or in the decoder. But that's why I'm weakly leaning towards the design that reflects most closely in the language what an engine is going to do under the hood.

TL: Yeah. And Conrad, if you're worried about indirection, this is the option that minimizes indirection, right? Because everything is totally inlined into the user struct.

CW: Yeah, I mean I don't mind this option. I do get Andreas's point about the copies. I guess I would weakly lean towards being okay with a world where it's banned in arrays. I would maybe want to think a little harder about that.

JK: So if waitqueue is its own heap type, whether it's subtyping from something or standalone doesn't matter, then it's also not copyable, right? You could have an array of references to these things and then copy all the references, but you couldn't copy the waitqueues themselves. And if we allow them as a packed type in a struct, then they're still not copyable. But structs don't generally have to be copyable; there is no struct.copy instruction, so that's not a problem.

RH: I would expect that we'll have a struct.clone instruction at some point that makes a memory copy of the struct. I think that'd be very reasonable.

TL: It's just so easy to do that in user space though. I'm not sure it would ever be compelling enough to add it.

RH: So, array copying. You can do that too. But you set instructions to do that copy.

CW: Well, you can do it. I guess the problem is you can do it until you start trying to play these games with magical fields because that's kind of the point at which we're taking the advantage of not being able to memory copy. So actually, I hadn't really had on my radar that we might try and do a struct clone that's based on memory copying. Does anyone else think this is going to exist? I'm again not necessarily against it. Just hadn't thought of it.

RH: I don't know. The reason I throw it out there is because it fits within the design criteria of what we've done before with array.copy and has very similar justifications to it. So, I wouldn't want to just assume that arrays are different. We need to be able to do copies with those packed types, but structs would never have anything like that because that doesn't seem to be the case.

JK: One quick comment on the idea of a struct copy that's based on memcpy, it's not going to be based on memcpy because for any reference type field we need a write barrier, and so we're going to have to special case each field type anyway, and it doesn't seem super hard to have another special case for waitqueue in there.

TL: What do you do for array copy of arrays of reference types? Is that a memcpy?

JK: No.

RH: It's a specialized one for references that does all the GC bookkeeping. So, we've got data ones and then also GC ones. The special case is for sure annoying. The bigger thing is semantically it just feels very weird to have a field that has state that cannot be copied. That's just odd to me, and I don't have a concrete example where it would at a semantics level bite us, but I think it's kind of odd and would not put it past it.

JK: I agree that's kind of weird. I think this brings us to a fairly fundamental dilemma. If on the one hand we say we want to be able to reuse struct operations on waitqueueref control words, and so in that sense we want waitqueues to be like all other structs, but at the same time we say we want all other structs to be compatible with a future struct.clone instruction, and that doesn't work with waitqueue. If we insist on both of these demands, then I think we have no other option, just generally speaking, than to have some kind of indirection between the control field and the waitqueue field itself.

RH: Backing up slightly because I don't know our implementation of waiting and notifying as well as I should. When you have a waitqueue type, what is the queue aspect of it? Is there an ordering requirement here, or is that non-deterministic? What would actually be the state in it? For example, today I was looking over our code. The way we implement it for memories is on the shared array buffer that underlies it all, we have a big linked list of waiters that we iterate over and check/compare different offsets. So, for a whole linear memory application, there's really just one queue part; there are different offsets that index different things in there. So, I'm just curious, does this imply that we're going to have a lot of different queues if we have a lot of different waitqueue refs here? Is that intentional or just a detail?

TL: Yes, it's kind of the whole point. It's all a big opportunity to actually do better than linear memory Wasm does in this regard.

JK: So we have the same situation that for linear memory waiting, we have one massive central registry of all the waiting threads, and we need a global lock to add or remove any of them to that. And so you can't actually have independent locks under the hood. And basically, as far as I'm aware, the big reason why we want waitqueues is because for waitqueueref we would not need a global lock anymore. We would have one queue per waitqueue under the hood, and so one lock per waitqueue, and multiple waitqueues can operate entirely independently from each other.

RH: Then another follow-up question. The reason why we have a general purpose control word is that because in addition to mutexes, we also want semaphores and things like that that have more than zero and one states?

TL: Yeah, it's just like the linear memory wait and notify operations. It's very much like a futex-based operation. So it's kind of like a condition variable, right? You check the control word has some expected value, and only if it does, then you go to sleep, and that check and sleeping is all atomic so you don't miss any notifications. So, it's just a very low-level flexible primitive that you can build anything else on top.

RH: Do you need just the simple case?

RH: Zero and one are the only two values you're ever checking for, or is it any arbitrary integer? I don't know how tool chains actually use instructions under the hood.

TL: It should be arbitrary. Yeah, because you can build all sorts of different stuff on top of this. For example, every single linear memory multi-threaded program has a start function that's injected by the linker that actually uses a waitqueue to determine who gets the privilege of initializing memory. And that protocol uses zero, one, and two as its three values.

RH: It feels like for the performance reasons with design number three, where you have the extra indirection, you want to bias access to the control word for the uncontended case. And I think you'd be more okay with indirection for accessing the queue because it's more likely that if you're going to sleep, you don't really care about that as much.

TL: Yep.

RH: So if every Java class had one of these on them, it'd be nice if the instruction took a pair of things. It was like atomic.wait and it took a pair. Well, it'd be nice if the Java classes pointed at the box and also the actual waitqueue because then you could just do the operation right there with the same amount of interactions as before. And then in the case that you actually need to get to the underlying waitqueue, it's also there too. Uses slightly more memory, but not terrible.

TL: Yeah, you can imagine having these point to each other. One is the one to the control word, but then they can only point to each other if you have a field that can point to the waitqueue, but we're saying that waitqueue is its own heap type here, so that would be very natural, right?

RH: You could do that if you wanted to. It's a little weird.

TL: Yeah, actually, that would be fine; you wouldn't be able to give it the struct allocation because you'd want to allocate that cycle all at once.

RH: Yeah. Well, and it'd be weird because they'd both be immutable fields. So, it would be a truly engine-only thing that could do both of those at the same time.

TL: Yes. And we currently completely disallow such cycles of immutable references. That's weird.

RH: I mean, maybe if it was like waitqueue.new gives you two results, or all it gives you is the struct back with the i32 thing and then a reference to an opaque waitqueue which is completely opaque you can't do anything with it, and so really there's only an implicit edge back to that struct, but there's no explicit edge, and then everything would operate on this fixed type representation where the struct's got the control word and it points at an opaque thing. You could have all the atomics wait notify take that struct as the input type. That one might need to be written down to ensure everyone understands.

TL: Yeah. This is great. Okay. So, my takeaway so far is that there are a bunch of additional ideas, and I haven't heard anyone say they super strongly prefer one idea over all the others, right? It's just a bunch of little tradeoffs, and we're ultimately going to want some data to back them up. So, I think getting as many ideas written down as we can and then getting a big table of all the trade-offs, the known trade-offs, is definitely the best next step.

JK: There's a possible tweak of the packed field idea. What if we introduce the waitqueue field as just the magic part and not the control word, and struct.get would just not work on it. It would be a validation failure if you try to directly struct.get or struct.set anything; that field could also be a validation error if it doesn't immediately follow an i32 field that's supposed to be used as the control word. So it would not address the concern obviously that it's not copyable. But it might address your implementation concerns about struct machinery being somewhat complicated because I suppose adding one more type of possible struct field is probably not a big burden as long as it doesn't impact what all the other existing struct field accessors do.

RH: So would it have an implicit thing where the waitqueue has to be right next to an i32 field?

JK: Yeah, it could be. I don't feel strongly about that. As we discussed this design number three, we already discussed that it might be possible or at least not problematic if you can arbitrarily combine the actual waitqueue and the control word. So I don't feel strongly about whether we put any requirements up there. We could say the waitqueue field has to follow an I32. Yeah. Or we could not have that limitation. I don't know if they would have drawbacks. I was mostly thinking it's not a fundamental new thing. It's just a slight tweak of the proposed idea that's on the slides and maybe that makes it more palatable.

TL: If you don't have that limitation, how would struct.wait or struct.notify find the control word?

JK: I'm not super sure. Maybe wait and notify could actually be the ones that get the field index of the control word of the actual waitqueue, and not of the control word.

MK: You could pass both offsets, right? Both indexes actually.

TL: Or, you don't even need to limit them to being in the same struct, right? You could say the waitqueue is a totally opaque struct field like you're saying, and you can do struct.gte on it, but you pass in as an argument some arbitrary struct with some arbitrary i32 field for it to look at as the control word, which may be the same struct and just a different field, or it could be a completely different struct if you wanted to. I don't think it actually matters.

CW: And that could work. I do find the idea of splitting these quite interesting now it's been brought up. I think I'm most attracted to the version where it's a different field of the same struct just because that seems very compact and probably what you'd want most of the time.

TL: Yeah, that's true.

CW: But that actually seems to fit quite nicely with how engines would want to implement this anyway.

RH: In the case Thomas, you're talking about where there's just a waitqueueref that's floating on its own, and when you want to wait, you pass a struct and a field index. You're essentially creating an interior reference into it because it needs to know the address that you're looking up, and then it needs to retain it to be notified later. So, if the engines wanted to copy a struct around, like generational GC, those waitqueues would need to be updated to know I was pointing at this struct field, and then it got moved somewhere else, and I need to look at the new location for it.

TL: Do you need a persistent reference to the control word when you go to sleep? Because I think you just atomically compare the control with the expected value, and if it's the same, you go to sleep. And then I don't think you need a reference to the control word anymore at that point because notify is on the queue, not the control word. And notify doesn't modify the control word at all.

RH: Okay, I guess I'm thinking of our shared array buffer implementation that needs to compare offsets because it will only wake up those on those offsets. But if you're okay with waking up anyone who's on the queue, then yes, you don't actually need that.

TL: Right. We've got separate queues now.

CW: Yeah, I actually quite like that idea.

TL: Yeah. The idea of separating out the control word and the waitqueue, and saying these are two separate fields or two separate things, we have not explored that at all yet. There seems to be some possibilities there.

CW: Yeah. And it's quite a minimal extension to the wait instruction where you just give it a second field, and that field just has to be typed as i32.

RH: Could you just do an atomic load comparison? If it matches, you wait. Then on the other side, just do notify.

CW: I believe there are use cases where you need the read comparison and the subsequent wait to all be atomic with each other. I would need to work that out on pen and paper, but I think that's the case.

TL: Yeah. No, you definitely do.

CW: Someone could write something else in between the read and the wait, and then you're screwed. But then you've got to implement the lock using something else.

RH: Okay. So, you need to acquire the lock for the wait, then do the comparison at that point.

TL: Pretty much.

RH: I understand what you're saying now.

TL: Yeah. The time of check, time of use bugs here where you miss your notify and then you just sleep forever, and the other thread thought it already told you to wake up, but you're asleep. That's bad.

RH: If on the notify side you don't actually need a reference to the original thing, then just having it be generic where you say I want to wait on this random struct field. That seems the simplest thing to me, and then you don't need that control word paired with it.

TL: Cool. I will take it as an action item to write up a lot of these new options here and try to present it as a nice understandable table.
