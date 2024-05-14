![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the April 30, 2024 video call of WebAssembly's Threads Subgroup

- **Where**: zoom.us
- **When**: April 30, 2024, 4pm-5pm UTC (April 30, 2024, 9am-10am Pacific Time)
- **Location**: *link on calendar invite*

### Registration

None required if you've attended before. Fill out the form here to sign up if
it's your first time: https://forms.gle/mUp4nmiVUTNQDKcD9. The meeting is open
to CG members only.

## Logistics

The meeting will be on a zoom.us video conference.
Installation is required, see the calendar invite.

## Agenda items

1. Opening, welcome and roll call
    1. Opening of the meeting
    1. Introduction of attendees
1. Find volunteers for note taking (acting chair to volunteer)
1. Adoption of the agenda
1. Proposals and discussions
    1. Overview of overview changes since last meeting
    1. Thread-bound data [#53](https://github.com/WebAssembly/shared-everything-threads/pull/53)
1. Closure

## Meeting Notes

### Introduction of attendees

- Thomas Lively
- Luke Wagner
- Derek Schuff
- Conrad Watt
- Manos Koukoutos
- Andrew Brown
- Deepti Gandluri
- Jakob Kummerow
- Ilya Rezvov
- Zalim Bashorov
- Matthias Liedtke
- Nick Fitzgerald
- Emanuel Ziegler
- Adam Klein
- Shu-yu Guo
- Francis McCabe

### Discussions

#### Overview of overview changes since last meeting 

TL presenting overview of changes since last meeting

FM: one thing we’ve been discussing re: WebAssembly.Function, the current semantics mimics a singleton module. This is a nice property of WA.Function, one of the reasons we moved away from using it is that we wanted to preserve that. I would recommend the same here, so if we’re doing any marking, we should do it on the imports.

TL: Yes, thank you for that. We definitely want to come back and think of the JS API

CW: describes new pause instruction to optimize busy waits and minimize power consumption

SG: note that pause doesn’t yield to other threads; it keeps the current thread but hints the CPU to yield other parts of the execution pipeline (e.g. to other hyperthreads).

CW: It’s about yielding cache line resources etc. 

SG: yes, distinct from OS-level thread yield and also from blocking completely and giving up the CPU

CW: Explanation makes sense as an instruction at the CPU level

SG: this was originally a JS-side equivalent, recently renamed from microwait() to pause.

CW: Isn’t the JS one more clever? It has a built-in loop? 

SG: That's right. On the JS side the call overhead is high, so if you were writing as if you were writing assembly, the function call overhead would dominate. The JS API takes an iteration number hint that the implementation can use to implement exponential backoff. Maybe it can be used differently between baseline and optimized tiers.
I would imagine the wasm side is literally just one instruction

CW: The differences make sense, you can implement the JS behavior in the user space for Wasm by putting a loop around the pause instructions. Yeah if we have this in JS it makes even more sense to add it to wasm now too.

TL: yeah it’s one of those mutually-reinforcing things where we do the same thing on both sides

CW: Forgot to make a PR about this, but if you have a global variable that's a v128, it’s hard to define an atomic load/store values because the architectures don’t guarantee it. Brutal solution would just be to not load/store global v128s?


AB: this came up when trying to implement some of these instructions in decoding/validation in wasm-tools. I saw your comment about this, thinking it through again. Now i’m conflicted because I think there maybe a way to do lock-free atomics on these

NF (chat): Portably, though?

DS: I think Intel has 128-bit atomic instruction.  On arm, you might need to do a load-linked / store conditional, not sure how lock-free you consider that.

CW: it’s more complex to spec the fact that if you have racing stores, you might get a mix of the bytes.

AK: is there a use case for this? It seems a strange thing to do, to have v128 globals

DG: We just allow v128 globals for consistency with other types.

TL: I’ve never heard of anyone using a v128 global. I don’t know of use cases for a shared v128 global. For now I’m happy to disallow it.

CW: in principle this applies to any type larger than the native word size. The reason it shows up for v128 is that it has a defined size we can’t get around. In principle if you had funcref or externref larger than the native word size, you might be able to do that for unshared but have to use a different representation for shared because of that. So this could affect some implementations.

FM: both bag of stacks and typed continuations are expected to use a fat value to represent the suspended computation.

CW: my impression was that there was a separate boxed strategy to use native word-size values, they may have to use that for shared

FM: that would cause a lot of overhead and GC churn to collect. Why spec this at all?

CW: then you might also have to consider adding lock-like constructs and penalize the non-shared writes as well. If you abstractly spec that writing a continuation to a global and reading it on another thread, then you have to ensure that you avoid this tearing when you implement it.

FM: Why is this in the spec and not rather just an implementation detail.

CW: this surfaces in the spec with v128 because it has a defined size. With other types it doesn’t really show up in the spec level. I just wanted to raise it as a possible implementation issue

FM: IMO I would not call out v128 specially in this case. Say any type can be in a global. Then implementations would have to lock their v128.

CW: the question would be, would anyone actually want a packed representation, or would they want a boxed representation

FM: my guess is that if you have v128 you wouldn’t want to box it

TL: we won’t mention in the spec what instruction sequence people will use but we saw what we’ll allow to be global/shared. My gut feeling is to just say that the spec allows everything and implementations do what they need to do to make it work, but it’s early and we don’t have implementation feedback yet. We can’t reason about every case of every type in all engines here, we can be uniform. If it’s more trouble than it’s worth we can find out.

CW: I'm a little concerned about things working really well on one architecture but having penalties on others.

DG: There's a way to do this without a loop on Aarch64. v128 globals shouldn't be performance-sensitive anyway. So going forward there should be good support, so I don't think there's a large portability concern. +1 for not having a special exclusion.

SG: about comparison: what other systems do is they say something about requiring atomicity, but expose a primitive like isLockFree that means you can find out whether the implementation is lock free. 
Technically it means “can you make forward progress in a bounded number of steps,” but in practice means "is this fast."

JS exposes this, C++ exposes this on std::atomic too. I was looking in the wasm spec, it looks like wasm doesn’t expose this?

TL: yes, it would expose nondeterminism, which we’ve tried to avoid. About globals, people use them because they are the only reasonable things to use, and not otherwise. So I'm not worried about people being incentivized to use globals because it’s not lock free  and then getting stuff. They generally don’t use them if they don’t have to, so i’m not worried about performance problems with globals.

AB: what i meant early on was, let’s wait and see what it looks like when we implement, leaving all types of globals possible ensures that implementers will have to grapple with this and come back and re-evaluate whether we should eliminate some types.

CW: Yes, I think that makes sense. And it sounds like people are ok with keeping the specification of v128 globals to be tear-free.

AK: because I said I was fine disallowing them: I'm also fine going down this path. Implementations may leave it out on the first round if they don’t want to deal with it, but given that we don’t really expect people to depend heavily on the performance of v128 globals

TL: CW, can you add a note to the overview?

CW: yes, will do

TL continues with recent commits, GC tradeoffs.

CW: aside from the decision about strong vs weak semantics. There’s also Luke/Ryan’s idea about <?>

TL: yeah currently the overview doesn’t mention that but it should. Overview outlines all the thinking about the proposal in addition to saying here’s what's currently actually being prototyped so we can interoperate. So it’s good to draw the distinction between those 2. In V8 we currently plan to prototype thread-local globals and see how fast we can make them. I wouldn’t want to replace the mention of tha tin the overview but mentioning multiple possibilities makes sense.

CW: is this one of those plans on deferring initialization to boundary crossing or something like that?

TL: not sure yet but probably. We haven’t started on the thread-local global part yet because we’re looking at prerequisites like shared structs.

CW: yeah and we’ll need that no matter which feature surface we have.


#### Thread-bound data [#53](https://github.com/WebAssembly/shared-everything-threads/pull/53)

TL: This was a concern raised by Dart who looked at the proposal and said they wanted shared structs to hold externrefs, to DOM objects, etc. that’s a shared->unshared edge. We haven’t figured out whether we’ll have those at all but this is an idea for how they might work. Sort of a smart pointer; in JS you can create a wrapper around an y JS object, and the wrapper can convert to a shared externref and pass it around, put it in a shared struct, etc then when you pass it to JS, if JS tries to get() the wrapped object, it will throw if it’s not on the the thread the wrapper was created on. So even though the wrapper can go to different threads, the wrapped object can’t. The dynamic check lets you sidestep the normal static restrictions.

AB (chat): bikeshed: WorkerBoundData?

CW: seems sensible, it seems the same if we have the strong or weak semantics. I imagine in most use cases the wrapped object will stay on the thread. 

TL: yeah could be a case where the compilation scheme means that everything has to be a shared struct, but most of them aren't actually shared.

CW: and this isn’t  a solution for calling JS functions, just for holding JS objects

TL: but it’s very similar to thread-local function idea. But yeah currently a separate utility.

CW: yeah it seems we need both. In the linked issue, Shu sketched what an analogous feature would look like it JS. will there be confusion if we add a nerfed version of it to wasm but then get something better in JS later?

TL: i.e. what happens if we get thread-bound fields of shared structs in JS?

SYG: I think there's a case to be made that if Wasm gets this first via a programmatic API, then there's less need for the JS thing. There's two parts to the JS thing: syntax support, which isn't very important, then the explicit getters if it's an explicit smart pointer rather than a special property type.
But it’s not critical to the expressivity. My guess would be that this will mostly be used by frameworks and not by end users, it’s hard to think about and incurs cost, etc. there will have to be some education that says this isn’t something  you should use just because you got an error about shared->unshared. So given the audience the ergonomic difference doesn’t seem like a huge deal. It's Fine for wasm to get this first, and if it does, JS might not even need a parallel API unless there’s demand for implementations without wasm.


CW: I’d expect the hardest part is the web implementation because it’s effectively the ephemeron story, when you wrap this object it’s creating an ephemeron on the side

SYG: That depends on the strong or weak semantics, I think. 

CW: I’m glad you think the weak semantics is possible. Thomas says the first experiment is the strong semantics, which is the full ephemeron story?

TL: I think we think that the strong semantics is the only reasonable one.

SYG: yeah i think it’s possible but not desirable.

LW: has the shared->unshared issue been brought to TC39 with the full gory details?

SYG: Yes and no. I have presented the gory details, but it did not inspire the kind of engine deep dive I had hoped. The audience at the time was not engine hackers. People believe the shared-to-unshared restriction is right.
And the ability to use shared references as keys in weakmaps is important to continue to be possible. I think the symmetry runs deep in the language, and to carve out a subset of objects that can’t be weakmap keys is fishy and would need a lot of convincing. So from the invariant that any object can be a weakmap key a lot of the semantics come out.

CW: If engine people are saying that, that sounds like they're signing up to do the work.

SG: that’s my position but TC39 has fewer engine people than this group.
I would love to get more engine people to look at it more. Ian from SpiderMonkey has taken a look, and I know SM has concerns because of how their collector works.

LW: JSC also had a special fixpoint iteration thing that’s not just a GC. so it would be interesting to see how they think about this

SYG: on the V8 side, I think they believe that the strong semantics is what we want in the long term.
In the short term our architecture isn't set up for strong semantics either.
The way the implementation works is that  the shared space isn’t separate from all other heaps, it’s a part of the main thread heap, a subspace. 
You collect the shared space when you do a collection on the main thread. If you have cycles, the hunch is that a lot of the cycles involve DOM so they will be on the main thread, so then the shared space GC will be able to collect the cycles.

TL: so if you have a cycle that’s not involving the main thread, it won’t get collected?

SYG:  in the short term, without a global marking thing that can mark every world and see all the edges between them, yes. I”ve prototyped a global marking phase without a global sweep/compaction. There are tradeoffs, and the v8 team isn’t convinced we want something like that but it’s certainly possible.

AB: where we went with that topic was talking about what the browser vendors think and that’s why we didn’t merge it. I wanted to get some feedback or acknowledgement that at least we understand it, from e.g. Firefox and JSC. Has anyone heard anything from them?

CW: my feeling was that one reason why Ryan was going so hard about the context local alternative was that he was concerned about the full ephemeron story. So I think there’s still concern there.

AK: On the JSC side, I talked to Justin Michaud about it, but he didn't have bandwidth and has since left apple.

AB: so should we not merge the PR?

TL: it’s still that the overview is for showing what the current plan of record is, plus what else are we thinking about. So in the first category I think it’s important to to add it since this is what we are currently prototyping. Plus it’s the first request we’ve gotten from real users, the Dart folks said they wanted this. But yeah we want to respect what we’ve heard to far about the concerns. So we should make it clear that this isn’t really settled and a done deal but we should get it in the overview.

LW: once you get the prerequisites  in, would it be possible to emulate it with a finalization registry?

TL: yeah it might be possible, but distasteful

CW: Would need to have the finalization registry support in place, otherwise everything would just leak.

TL: I'll go back to the PR and make sure it has enough language making the current state clear.

AB: I did ping Ryan to try to get some feedback in the PR, that would be helpful.

TL: good discussion even though it wasn’t all on the agenda, seems worth meeting somewhat regularly and we find stuff. But having said that, please liberally add things to the agenda!
