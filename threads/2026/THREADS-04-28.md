![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the April 28, 2026 video call of WebAssembly's Threads Subgroup

- **Where**: Google Meet
- **When**: April 28, 5pm-6pm UTC (April 28, 9am-10am Pacific Time)
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
    1. Relaxed atomics (Rezvan Mahdavi Hezaveh, 20 minutes)
        1. Present benchmarking results
        2. Discuss proposal separation from shared everything thread
    1. Discussion: Waitqueue design (Thomas Lively, 30 minutes)
        1. Should we try to update ECMA-262 and HTML to allow blocking on the main thread?
        1. Should we allow spurious wakeups?
    1. Should data segments always be shared? [#83](https://github.com/WebAssembly/shared-everything-threads/issues/83) (Thomas Lively, 10 minutes)
1. Closure

## Meeting Notes

### Attendees

- Thomas Lively
- Rezvan Mahdavi Hezaveh
- Colin Murphy
- Conrad Watt
- Deepti Gandluri
- Derek Schuff
- Manos Koukoutos
- Nick Fitzgerald
- Jakob Kummerow
- Ryan Hunt
- Steven Fontanella
- Kevin Moore

### Discussions

####  Relaxed atomics (Rezvan Mahdavi Hezaveh, 20 minutes)

RMH presenting [slides](https://docs.google.com/presentation/d/1n1q3Ha04SdlrSlcVCulkk0tlVRmk3fRA4YDxCWKfICY/edit?slide=id.g3c5f7424c85_0_0#slide=id.g3c5f7424c85_0_0)

[Sheet](https://docs.google.com/spreadsheets/d/1uRpdjRPAatsBAO6iJZvMq0YYuL8ZAG-ASEirO0O-yK0/edit?gid=540507349#gid=540507349)

[Report](https://docs.google.com/document/d/1oC6DcovIQGcfV0CYYl1R5MEqTfMWmwsh-mML0RxgUcw/edit?tab=t.0)

RMH: The last time that we talked about relaxed atomics in this meeting was when I gave an update about the V8 implementation, and also we talked about some observations like not all the memory instructions have different generated code when we use sequentially consistent and acquire release. And the feedback that we got was to do some benchmarking and bring numbers, which I will do today. And before looking into the benchmarks, let me give you another status update. The implementation in V8 is completed. It's behind the flag, and it's completed in both Liftoff and TurboShaft, which is the optimized compiler here, and it's also completed behind the flag in LLVM. So the goal of doing this benchmarking is to find out about the performance impact of switching from sequentially consistent to acquire release, and the benchmarks that I used were from this paper titled 'Toward understanding the cost of avoiding out of thin air results,' which Conrad shared with us. The authors used three benchmarks from three repositories: LibCDS, Junction, and Folly. And I used the first two. I didn't use any of the benchmarks from Folly. LibCDS is a comprehensive C++ library of lock-free and lock-based concurrent data structures. I got eight benchmarks from that repository, and Junction is a library of concurrent hash maps designed for high performance and extreme scalability, and I got two benchmarks from this repository. So to do the benchmarking, the environment that I used was a Linux machine with an x64 CPU. I used Emscripten version 5.05 with the compiler flags of -O3 to get the most optimized Wasm files, and -pthread to be able to use threads, and `-mrelaxed-atomics` is a feature flag. So it was excluded in the baseline build and included in the relaxed atomic build. And for V8, I used version 14.9.112. And the flag that I used was `--no-liftoff` to make sure that I'm testing TurboShaft code, which is the optimized version. And the `--experimental-wasm-acquire-release` was excluded in the baseline to have only sequentially consistent, and included in the relaxed version to have the acquire release memory orders. And I compared these two baselines with relaxed versions to make sure that the result is stable and I have as little noise as possible. I did CPU pinning, where I pinned the process to six CPU cores. I threw away five rounds prior to measurements for each benchmark. And after the warm-up phase, I ran each benchmark for 100 iterations and collected data. To analyze the results, I trimmed 20% of raw results on both ends of the range and focused on the 60% of the middle runs. I also calculated noise to see how stable the execution environment was. I calculated mean, median, and 95th percentile, which represent the worst-case performance. I also used p-value tests to determine if the difference that I'm seeing between baseline and relaxed results is statistically significant or not. We will take a look at the whole results in a minute. I have a sheet reporting all the analysis, and also I have a written report which I will share after the meeting; the links are here. So the results that we observed was that we observed a statistically significant improvement in seven out of 10 benchmarks. The improvement ranged from 3% to 51%. The noise after trimming is about 2% for most of the benchmarks, which I think is acceptable, and 95th percentile speedup is also aligned with median and mean improvements, which shows that the relaxed atomics improve the worst case as well as the median in these benchmarks. So from the benchmarks, seven out of 10 show statistically significant improvements. Five benchmarks have a store instruction, which we know has different generated code, in the top five improved benchmarks. Two of the benchmarks, I couldn't find any store instructions; they have load, compare-exchange, exchange, and some binary operations. But we still see 3% improvements. I'm not sure what's going on, to be honest.

TL: Maybe some reordering.

CW: So, just to understand, all of these numbers are improvements, right? Are the three out of 10 benchmarks ones that did worse or just the same?

RMH: So, yeah, let me actually show the results. That's a very good question. So what happens is that two of them don't have any significant improvements. They have improvements but the improvements are not significant and this one has 1% regression. I'm going to talk about this one in a minute. I changed this benchmark, but the last one has 1% regression, which is a benchmark using some kind of queue. So, I'm not sure what's going on on that.

CW: Interesting. I've forgotten how V8 does this, but for the SC stores, do you take those to a locked exchange or do you use fences?

RMH: I think it turns into locked exchange in the generators code in the last layer.

CW: That makes sense.

RMH: Okay. Now that we looked at these results, let's take a look at this spin lock benchmark, the original one that exists in the repository itself. I saw a huge regression, which was surprising. So I started some investigation and modified the benchmark, and after modification, this benchmark shows a 51% improvement. So let's talk about that. So, in the original spin lock benchmark, this is the main part of the benchmark where the measurement happens, and apparently, this check caused some threads to escape the loop altogether when they use sequentially consistent memory ordering.

RMH: It looks like the lock is visible to all the threads immediately. But in the relaxed version, some of the threads still see the spin lock as free and enter the block. I added a counter in this loop to make sure that it's actually true. And it looks like when we use relaxed atomics with acquire-release memory ordering, we enter the loop seven times more compared to when we use sequentially consistent memory ordering. So to make sure that we can have a fair comparison, I changed this benchmark and removed that check. So in this case, all the threads are forced to go through all these lines, and this is the benchmark that we see 51% improvement.

CW: I had a student who did some similar tests and I think they observed a similar issue. It seems that in very high contention scenarios, the fact that the lock exchange kind of artificially stops contention at the CPU level actually makes certain benchmarks faster.

TL: Maybe that's what's happening with the 1% regression.

RMH: That was all I have to share today. And based on the results we just saw, I hope to see if it's possible to split the relax atomics from the shared-everything proposal, have it as its own proposal, and hopefully bring it to a CG meeting for phase two advancement.

CW: Personally, I think yes, but obviously interested in other people's opinions.

TL: I am also strongly yes, perhaps not surprisingly. I think we should definitely take this to phase 2.

RH: These seem like good results to me. I guess the question is, do you want to do just relaxed atomics as their own, or is there anything else you'd want to bundle with it? It seems like it could be its own proposal, but I just haven't been paying attention that closely to know if there's anything else that could go with it.

CW: Yeah, actually, just to follow up on that, is this version of the relaxed atomics that we're taking to phase 2 just load and store, or is it also the RMW changes?

RMH: I think we actually have the implementation for all of them, so they can all be in the separate proposal.

TL: I think keeping it to just the memory accessors, though, right? All the memory accessors with release-acquire, without Wasm GC changes and everything else with shared-everything threads.

CW: Yep, that works for me. I'm sorry to have potentially forgotten the conversation we had before, but where did we land on the binary encoding for release acquire on RMWs?

TL: The status quo is that we are packing two memory order encodings into the same byte. So they each take a nibble, and we currently have a restriction that they must be the same. So it's a little silly right now, but looking forward to a future where you can have two different memory orderings.

CW: Where did we land on the flag for a load or a store and the flag for an RMW? Does the load and store also repeat the memory order twice or does it just do 0 and then the memory order?

TL: So it's still one byte, and the high bits need to be zero, and just the low nibble is used.

CW: Okay, that sounds good to me. So now that you have the benchmarking set up, you could also benchmark my dream second relaxed atomic order, which would be the load store ordered one.

TL: The one that paper is actually about, right?

CW: Yes, exactly.

TL: We've seen some great speed ups from release acquire here, at least in dedicated benchmark. Still a little unclear how that translates to a real application. Would you expect a similar magnitude of speed up again?

CW: So my expectation would be that if you run the benchmarks you've got today and on ARM instead of x86, you should see zero speed up because the ultimate machine code is the same. And if you added load store ordered atomics to WebAssembly that would allow ARM to get the same speed up x86 is getting here. That would be roughly my first guess about how the performance numbers would shake out. So by adding release acquire atomics we're making Intel faster and then you need to add load-store ordered atomics to make ARM get the same benefit.

TL: Interesting. Yeah, I mean I'm not opposed in principle. It's just more work. The question is, do we want to do that now sort of at the same time, or do we want to do it later as a follow-on? And until now, I'd always been assuming we would just do release acquire first and then maybe more in the future.

CW: Oh yeah, to be clear, I'm totally fine with doing release acquire first. Even on a conceptual level, there are lots of languages that don't go any weaker than release acquire because that gets scary. So it's a sensible first thing to do. But if we were trying to get the same performance on ARM, it might make sense to think of the next extension afterwards. I just got excited that you had all the benchmarking set up already and we're actually seeing some signals.

TL: We need implementation for the new memory order to be able to do the benchmark. It would be non-trivial. But it's certainly possible. We could do the benchmarking later.

CW: No pressure to do it now to be clear.

TL: I think this is also something we could potentially add in phase two, right? So, I think we've got enough data as is to go to phase two right now, and then depending on how fast things are moving, it's something we could potentially play around with and add to the proposal if we do see big benefits.

CW: Have you had the opportunity to shop these benchmark results around more widely in Google and get anyone biting saying, "Hey, we think our app might speed up." Or even better, did you find any users of these libraries?

RMH: No, not yet. But that would be interesting.

CM: I've already posted it in the Photoshop internal Slack channel. So, we'll see if we get any bites. Do you have a link? I just kind of tried to summarize.

RMH: Yes, I have a report and a sheet.

CM: Great.

TL: All right, any other thoughts for now? Obviously, the next step would be to bring this to the full CG for that phase advancement vote.

#### Discussion: Waitqueue design (Thomas Lively, 30 minutes)

TL presenting [PR](https://github.com/WebAssembly/shared-everything-threads/pull/110)

TL: The next thing on the agenda is more waitqueue stuff. So basically the idea is that we'd have the new waitqueue and nowaitqueue heap types, and then the new instructions are waitqueue.new, which just allocates a waitqueue, and waitqueue.notify, which takes a waitqueue and a count of things to wake up and tries to wake them up. This is very analogous to the existing notify instructions on linear memory. Then we have wait instructions that allow the control word to be anywhere. We have two memory waits: one for a 32-bit control word and one for a 64-bit control word. This matches the existing memory wait and notify mechanisms where you can have 32 or 64-bit control words. There's that side discussion we started with the full CG about overloading. So for example, struct.wait works with any allowed field type. So i32, i64, or eqref. But let's not talk about overloading right now since we're already talking about that in the other forum.

TL: First of all, any objections to landing the PR? And second of all, we could do some light bike shedding and design discussion here. Do we really need both wait32 and wait64? What if we just supported 32-bit control words? Another thing is spurious wakeups. Conrad, you and I were talking about this a little while ago. The current wait and notify mechanisms do not allow spurious wakeups. Wakeups only occur when there's a notify. In contrast, native primitives like pthreads condition variables or Linux futex almost universally allow spurious wakeups for performance reasons, but it's hard to find details that go into the performance reasons. So, I don't have a strong argument for allowing spurious wakeups, and I can't point to code and benchmarks and all this stuff. But hypothetically, if we were to find that allowing spurious wakeups did have performance benefits, I would be strongly in favor of allowing them in this kind of v2 of wait and notify operators. And I know Conrad doesn't agree so much, but this is all very abstract and we have no data. So, I'd be curious to get other folks' gut reactions. This is not something we're going to settle today.

CW: Yeah, just to throw out my gut reaction quickly. I think there's a lot of value to staying consistent with the choices we made previously, especially if we have any ambitions in the future to expose any of this to JavaScript, which also assumes no spurious wakeups.

TL: Yeah. And to summarize my opinion, which is yes, I love consistency. However, it's not often we get the opportunity to do a sort of clean V2 of a mechanism that we've already specified. And so we should take full advantage of that opportunity and make all the improvements that we can. So I think these are both very reasonable opinions and we have no data backing up either of them. So, we're obviously not going to settle this today, but again, very curious to hear other people's sort of gut reactions about this issue. Say I had data that was like, look, we've benchmarked it with spurious wakeups, and the common case here gets 5% faster.

TL: So let's specify that spurious wakeups are allowed. Conrad, at 5% you say yay or nay?

CW: I think I would still fight you to the bitter end on this unless the benchmark was really good. It's very easy to come up with microbenchmarks for these kind of things that look very good on paper. But if it was literally you went out into the world and found a company with no connection to Google and their end-to-end test that they had already before you even talked to them happened to give a 5% improvement when you just switched the flag to use spurious wakeups, then maybe we'd have a conversation. I think before that I would have a lot of suspicions.

TL: I don't think Google has any sort of ulterior motives for wanting spurious wakeups that would lead us to skew any results. But I hear what you're saying. Any other thoughts about this? If not, we can just move on to the next topic.

MK: About waitqueues in general: what would be the difference if we let the control word check happen in userspace instead of having all these instructions for waiting?

TL: It's very important that the check of the control word and the action of going to sleep happen atomically. Otherwise you can miss notifications between checking the control word and going to sleep. When the check and sleep are atomic, it lets you design a protocol so that you can guarantee that if the waiter thread observes the expected value, it will never miss a notification.

MK: But does it follow it's implemented atomically also in the runtime? I mean it's not that clear to me.

TL: Yes, the runtime needs to ensure that this is atomic as well. The same missed notification problem must be avoided in the runtime implementation as well.

MK: Okay, thanks.

JK: Quick question on this list of instructions. Maybe I'm missing something here, but what's table.wait doing in there? Tables can't hold i32s, can they?

TL: They can hold eqrefs.

JK: Can eqref be a control word?

TL: Yes, and this is part of the whole overloading disagreement. The allowed control words are i32, i64, and eqref, which is the same set of types we allow for compare exchange operations.

TL: The other consideration is waiting on the main thread. This is not directly related to the design of our WebAssembly instructions, but is in the spirit of fixing all the little warts as we design a v2 of the wait and notify system. The status quo is that you cannot block the main thread. So in JavaScript, if you call Atomics.wait on the main thread, it throws. In WebAssembly, if you do a memory.atomics.wait32 or wait64 on the main thread, it traps. It doesn't even check the control word first. And this comes ultimately from the HTML spec, which sets [[CanBlock]] to false on the main thread. All that does is make Atomics.wait and the corresponding WebAssembly instructions trap. And over the last 10 years, the result of this has been that everyone just does a spin loop on the main thread instead, which is strictly worse. And so it's still not a good idea to block the main thread, that's not changing. But if the choice is between Atomics.wait and a spin loop, we'd rather have Atomics.wait. This is not something we can change on our own here in this forum or even in the full WebAssembly CG. It's sort of out of scope, but this is something we can engage with the JavaScript and HTML folks on to get fixed.

CW: If someone really did execute a program that just started waiting on the main thread and never got productively woken up, would you get the behavior of the browser tab graying out and saying your thing is unresponsive? Is that okay?

TL: Exactly. This is the same behavior you get with a broken spin lock today, where the spin lock just loops forever and nothing happens.

CW: Are we confident that the browser is set up to give that feedback because I thought there was something about some instrumentation that needs to be inserted to make that happen with busy loops?

TL: Yeah. I think it's going to be a little non-trivial. Certainly, as a first step, we would simply move the busy loop into the browser. After that, we could look at actually making it better. But yeah, you're right. This is non-trivial, and there's clearly some stuff that would need to happen here.

RH: As far as I know, when I was looking into it in Firefox, I didn't test it out, but I did see in our Atomics.wait code, we do handle interrupts, which is the mechanism that Gecko uses to do the slow script dialogue. It's the same thing we do with loops. We have an interrupt check in our loop headers. And so it seems to me, as far as I can tell, that you would give slow script dialogues in both cases, which is what you would want. But I haven't tested it out.

CW: That sounds like a very positive thing to be able to tell.

CW: Yeah. To be clear, I really like this. I think we should do it. My only concern is stereotypically we didn't pursue this for years because of wider politics in the W3C TAG.

TL: Understood. And I think there's some combination of us having 10 years of experience with this now and being able to very clearly show that it's a bad option or a worse option that we're picking between, and the worse option is the status quo. So a mixture of that and the fact that people have just sort of moved on in the past 10 years, and so we're dealing with different folks over there now. I've been shopping this around. I sent an intent to prototype to blink-dev, for instance, about this. I've linked to an explainer. So far no one has told me no. Some people have said, "This makes me uncomfortable, and what about X, Y, and Z?" and then I respond, "Here's why X, Y, and Z don't work," and they're like, "Oh, okay." So no one has told me no yet. So I'm happy to just keep working on this.

CW: That sounds quite positive.

RH: I've started to shop it around internally. We were going to have a discussion on it with the DOM team this Monday, but that got delayed. So no final conclusions or anything on our side, but we're trying to figure it out. It's very similar reactions; everyone's gut reaction is initially uncomfortable because if you tell anyone on the DOM team, "Hey, I want to block on the main thread," instantly they get very uncomfortable. But you kind of work through the details, and it is one of those situations where it does need to happen in some cases that you really just can't eliminate, and what we currently do is just worse than what we could do. So I'm cautiously optimistic, but it's not entirely in my sphere of influence.

CW: What's the top level new user experience you'd expect to get if people compile to Wasm and we have this new capability? What gets better for them?

TL: Developers see no difference because they're not writing these APIs by hand anyway. Users see no functional difference because their spin locks just get replaced with actual wait locks. So ideally, there's some small measurable performance improvement because you don't get the priority inversion, and ideally, there's some small energy usage improvement, so it's better for your battery life. It's super unclear if that's something we could measure.

CW: But then, is the real story that it's making the compilation scheme more uniform? Is that the real benefit here?

TL: That is a benefit. I don't think it's very compelling. It certainly is not compelling for the HTML folks because they've got their hierarchy of constituencies where the end user is really the only important one. And honestly, I don't think it's really that compelling even for us. That's the same argument we always have about the JavaScript glue code where people are like, "Oh, it's ugly. I don't like it." But it works, so it's ok. I'm happy we can talk about performance and power savings instead.

CW: But to be clear, if we're not talking about compilation uniformity, the next argument we have to reach for is performance and power savings.

TL: That's right.

CW: Any chance we can get numbers that make us look good?

TL: I'm hoping we don't need to get numbers to get this through, and then everyone can just be happy. If someone really insists on numbers, we'll have to look into it.

CW: Officially what is the proposal mechanism for this? Do we need to do a full request for comment through the TAG and all of that stuff?

TL: Yes, it's okay. Again, no one has told me no yet. I've already been talking to TAG members about this. Cautiously optimistic, as Ryan said. And if we do run into a hard block, then my goal is that nobody else will have wasted any time on this.

DS (chat): I think there's potentially a debugability advantage, where the browser can recognize the blocking directly, rather than having to infer it by seeing the spinloops in userspace.

TL: Yeah, there's also a possibility that this helps debugging because the browser has more visibility into what's actually going on at the application level with the locking, because a spin loop is indistinguishable from any other loop.

CW: That actually seems like quite a compelling argument to me.

TL: It could be if we had concrete plans to actually take advantage of that, but that would require getting something onto the dev tools team's planning, and that actually sounds way harder than convincing the TAG.

RH: One concrete issue that has been raised internally is that a lot of our workers code relies on transparently proxying things to the main thread in different cases and synchronously waiting for that to get handled. With spin loops, it can lead to unexpected deadlock where the worker thread is blocking for the main thread to do something, and the main thread is blocked waiting on the worker thread. All you had done was call some web API that you didn't actually know was going to do that behind the scenes, and I don't think it's even necessarily specified by the spec. I think it's just how our implementation has done it for convenience. And so it's one of those things that makes everyone uncomfortable, but it also doesn't necessarily get worse by allowing these blocks on the main thread. There was some discussion around, would we, if we had this, would it make sense to specify that there could be a nested event loop at these waits, or maybe not necessarily a user visible one? But could we take this as an opportunity? When there is an Atomics.wait on the main thread, we could have a special mechanism where we can service these synchronous things from the worker, and in that case, it might actually make it easier for us because we have a well-identified point where we can handle those synchronous proxies. But it's a big open question. So that would fit into the whole idea that maybe it would actually make the browser's job easier by having a well-identified point where it's blocking and we could actually do something useful with it.

TL: It's kind of fun because we've been dealing with the exact same issues at the Emscripten runtime level. Emscripten also proxies a bunch of stuff to the main thread and also has to solve the problem of what if the main thread is blocking. So we have mechanisms for injecting a wake up into the main thread if it happens to be sleeping so that it can wake up and process these work queues. So it sounds like exactly the problem you're describing, Ryan. Thankfully we have some precedent in Emscripten, if you want to call it that, that these problems can be solved. Not to say that the implementation in the browser is going to look the exact same as the implementation in Emscripten but there's certainly going to be similarities there.

TL: I haven't heard anyone say this sounds like a bad idea, so I will keep working on it with the HTML folks and I'll bring updates back here as I have them. Ryan, thanks for engaging with your folks on this on your side. I know I've reached out to Keith and Shu about this to see if they can get movement on the Apple side as well. Haven't really heard back from them. But yeah, we'll just see where this goes. And in the meantime, I also didn't hear anyone say that they hated this new waitqueue design in the PR. So, I'll go ahead and land the PR. Of course, all of this is still open to bike shedding and fine-tuning, and if there are other ideas, we can discuss them.

CW: Sorry to be totally pedantic, but the new design does not include spurious wakeups, right?

TL: It is not documented to allow spurious wakeups. There's a note saying we could consider adding them in the future.

CW: Okay. Totally okay with the note.

#### Should data segments always be shared? [#83](https://github.com/WebAssembly/shared-everything-threads/issues/83) (Thomas Lively, 10 minutes)


TL: The last thing on the agenda is this issue about the data count section being insufficient. So basically the gist of it is that when you're compiling the code and some instruction refers to a data segment, you might need to know whether that data segment is shared or not. Just like you need to know whether the index to the data segment is out of bounds or not. And so the data count section currently exists to tell you how many data segments there are so that you can validate whether an index is in bounds or not. But it doesn't tell you whether each of those data segments is going to be shared or not. And so the problem is the data segments come after the code section. So when you're compiling the code or validating the code, you don't necessarily know whether it's shared. And so the sort of leading solution is just like pretend they're all shared, and that's fine because they can be used from anywhere when they're shared. Then there's another wrinkle about the semantics of data.drop when it races on one thread with a bulk table operation on another thread. I have no answer there. We need to say something. I think in the short term, at least for implementations and prototypes, just pretending all the data segments are shared sounds great. So we can just roll with that in the prototype, but I don't know what the spec should say.

CW: I've not totally thought this through, so I'm not sure what I think about it, but it's not something we explicitly discussed. We could jump all the way into still having to declare data segments shared or unshared, and we do whatever section finagling we need to get the declaration early, and then we prevent data.drop of shared segments. The reason we can't do that second thing on its own is because if we make every segment shared, that obviously breaks all the existing code that uses data.drop.

TL: Fortunately, there might not be any existing code that uses data.drop.

CW: Well, then can we deprecate all the drop instructions, or is elem.drop used?

TL: Oh, I think we do emit code that uses elem.drop. We could just redefine it to be a noop though. That's not strictly backwards compatible, but it might be backwards compatible in practice.

CW: Yeah. Maybe then the path of least resistance is to deprecate the drop instructions. I mean, I was actually surprised that Jakob was so negative about the existence of the drop instructions. Is this some internal conversation that's been happening about them being useless?

JK: No, I don't feel strongly about it. I don't really care. It's just completely useless. It's a few CPU cycles that we spend for really no benefit. I assume that the hope was that it would save memory. If you can indicate that you don't need the segments anymore, but it saves zero memory because we don't make a copy of the segments anyway. We just leave them in the wire bytes until they're needed. And so dropping them does nothing. At least for data segments. I'm not exactly sure what the story is for element segments. I think for those we actually do make, well, not a full copy, but they have initializers that we have to evaluate, and so the results of those initializers do get stored. And so I think elem.drop would actually save at least a bit of memory, but data.drop definitely does not.

RH: Could someone explain what the issue is with data.drop? I missed this in the discussion.

CW: So the issue with data.drop on its own would be what its concurrent semantics are. Right now, the sequential semantics are that it sets the length of the segment to zero so that subsequent accesses that try and do a nonzero amount of work on the segment go out of bounds immediately, and that's meant to give you cover to garbage collect it or something like that. But then we'd have to ask if you have multiple threads and only one of them does the drop and another thread concurrently tries to do a bulk operation referencing the segment. What's the expected semantics of the bounds check? Which is something I've thought about a lot, but doesn't make the right thing easier to implement necessarily.

RH: Okay. Could you change the semantics? So instead of it setting the length to zero, because the way we model it is we have an atomic ref pointer to a vector of bytes. So when we drop it, we literally just clear that ref pointer from the instance. So a natural way of implementing it would be if you wanted to do a data copy, you grab the ref pointer, then you do a null check, and if it's null, then trap; otherwise, you continue on, and data.drop is writing null there.

JK: I think that's pretty much option two that you see on the shared screen here. Right now, I assume in your engine as well, these pointers have to be on the instance, right? So they're effectively per thread. And so if we just didn't do anything, then that would make data segments effectively thread local. Which might be weird, but at least it's easy to implement.

TL: That's already not a correct implementation with today's semantics though. Oh no, because you can't import or export a data segment.

CW: It can still be a correct implementation because in the one thread case, there's only one thread that can do the drop, right? So everything is thread local.

TL: So even with shared shared Wasm GC, because it's still instance per thread, this is not a problem we can possibly have. So this is another problem that we only get with shared functions, which again we definitely want, but okay, this is not super urgent.

CW: Yeah, that's totally correct. Or although I mean if we want to fix the data count thing right now with a particular solution, we might want to be a little forward-looking as to what the implications for this would be. But I agree we can fumble our way through later when we get to shared functions if we absolutely have to.

TL: Jakob, how hard would it be for us to add a use counter for data drop?

JK: It should be reasonably simple.

TL: I think actually every single multi-threaded module does do data drop because it's in the initialization sequence added by wasm-ld. Not in a way that's ever observed; like if it became a no-op, that would be fine. But I guess a use counter isn't the right thing because I think there will be lots of uses.

JK: It seems safe to assume that some modules out there might contain the instruction, and we shouldn't just make them invalid. So, we probably shouldn't undefine the op code, but we can make it a no-op. As I wrote in that post, technically it's a breaking change. But in a way, it's no different from, for example, adding a new opcode where bytes that were previously either invalid or trapping are then no longer invalid or trapping. And that's generally a type of change that we accept and assume is backwards compatible. So if it only turns something that used to trap into something that no longer traps, then that's probably fine in practice.

CW: I actually totally agree with that reasoning.

TL: I wish Andreas were here. I imagine he'd have a different and spicy take about this, but I don't want to put words in his mouth.

CW: Well, if I were to try and steelman the existence of these drop instructions, I think one thing we're seeing here is that elem.drop is more interesting than data.drop. So, we should potentially be thinking more about that. Or do we solve this problem just by deprecating data.drop, with elem.drop having the same behavior?

TL: Potentially, you're going to end up with the same problem with shared element segments, presumably because we have bulk table operations that use those.

CW: Is there not something about them appearing earlier in the module, though?

TL: Oh yeah, they do. So we don't have the validation problem. So the whole data count section thing, we don't need that for element segments, but the concurrent semantics is still something we need to figure out.

JK: I think it's less of a problem there because if we introduce shared elem segments, then they are new anyway and they can have additional overhead. Most shared things will have additional overhead compared to their unshared equivalents. The issue with data drop was that one option was to redefine all existing data segments to implicitly be shared, which is fine because they're read-only, but that would mean making accessing them any slower by introducing additional locking requirements or whatnot would regress the performance of existing modules, and that's not a problem that we have for elem segments because there is no reason to make any changes to the behavior of unshared elem segments.

TL: If we make data.drop a no-op, where does that leave us with this issue? We still have a problem, right? Because the data count section is still insufficient for validating if we're going to have shared and unshared data segments; it just says that every data segment is shared.

CW: I would be interested to understand if that makes things slower because if they're all shared, it might be that depending on the engine architecture, you might have to then put them in a shared heap if you're allowing them to be post messaged. I don't know. Can they be?

RH: They already can post messages through modules effectively, unless you're going to actually copy between threads.

CW: Yeah, that's a good point.

RH: Just a quick tangent. As far as I know, in SpiderMonkey, if you data.drop and it is that last reference to that data segment, it does go away and it does release memory for us. So I'm not necessarily sold that we should redefine data.drop to a no-op. I don't think it's quite a slam dunk there.

CW: No, you're totally right.

TL: So you're not implementing the data segments as just like views into the wire bytes?

RH: No.

TL: I'd be interested to hear more about that because other than the point that it's actually meaningful memory savings in Spider Monkey, this plan sounds pretty good.
