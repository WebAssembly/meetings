![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the April 21st video call of WebAssembly's Community Group

- **Where**: zoom.us
- **When**: April 21st, 4pm-5pm UTC (April 21st, 9am-10am Pacific Daylight Time)
- **Location**: *link on calendar invite*

### Registration

None required if you've attended before. Send an email to the acting [WebAssembly CG chair](mailto:webassembly-cg-chair@chromium.org)
to sign up if it's your first time. The meeting is open to CG members only.

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
    1. [Special edition of the meeting to discuss subtyping](https://github.com/WebAssembly/meetings/issues/529)
1. Closure

## Agenda items for future meetings

*None*

### Schedule constraints

*None*

## Meeting Notes

### Opening, welcome and roll call

#### Opening of the meeting

#### Introduction of attendees

Ben Smith

Jacob Mischka

Ross Tate

Clemens Backes

Francis McCabe

Alex Crichton

Deepti Gandluri

Derek Schuff

Lars Hansen

Thibaud Michaud

Ryan Hunt

Mingqiu Sun

Sean Jensen-Grey

Ioanna Dimitriou

Emmanuel Ziegler

Andreas Rossberg

JP Sugarbroad

Heejin Ahn

Nabeel Al-Shamma

Thomas Lively

Bill Budge

Jakob Kummerow

Rick Baggatline

Adam Klein

Pat Hickey

Rich Winterton

Wouter Van Oortmerssen

Dan Gohman

Zalim

Zhi An Ng


### Proposals and discussions

Ben Smith Presenting [Slides](https://docs.google.com/presentation/d/1yzfLkStEjlLeK3L1WcOEijb0hfERBh9GxcNbxBjWi-Y/edit). 

AR: Point to add there that there is a eqref type - if there is a eqref type, then there’s no reason not to have anyref as well, as there’s no good way to have equality without eqref <BS Agrees>

AR: I have a slide that lists all the changes to the ref types proposal - can present that later. 

<AT Slide: Incompatible with superfluous casts>

AR: counter argument is that this is unlikely to  be applicable to Wasm, not sure how relevant it is, because we have way more notation, and avoid inference. This will be a different design direction from what we have done so far. Might be interesting from the tooling side. If there are IL that compiles to Wasm, but again this is not relevant to Wasm, would be a separate language, with a separate type system, that does not impact Wasm (inside the engine).


TL: It does become relevant as a secondary argument. It becomes relevant when all the tools are using a separate language and type imports.. There is a risk here that if we say it’s a tooling feature and not a VM feature, we might end up with something that no one used. 

AR: this isn’t about features that no one uses, this is about potential problems that might be introduced into the type system. This system is very special, the problem there is through a combination of some hairy features. It’s not clear what conclusions we can draw here. It’s a really specialised case. Not clear to me how this would carry over to the toolchain side.


RT: The high level of phrasing this is, currently we don’t have a way of getting rid of superfluous casts, there’s only one technology that has managed to get rid of them, the argument is here is it worth implementing something that’s hard to get rid of to begin with?

BS: any other For arguments that are missed?

RT: another For argument on type imports, can wait till later.

<BACK TO SLIDES>

AR: some amount of churn expected, that's why we have stages, process

<Slide Against #2>

AR: I think this is conflating other things, but not worth going into the details right now. 

<Slide Against #3>

TL: Most of the proposals that would be impacted, that would have this churn are phase 1 proposals, taking action to avoid churn in Phase 1 isn’t a precedent we should set

BS: although, there will be churn in phase 4 proposal

AR: Which phase is Exceptions?

BS: 2, I believe, almost 3.

<Slide Against #4>

AR: This came with the argument that even if we don’t have subtyping, we can have conversion operations, I would argue that this is not enough, we also need both versions boxed and unboxed so you’re not converting back and forth in an expensive manner. If you have the unboxed types, once you have more precise types, you will still need boxed types in addition to the unboxed types.

<Slide Against #5>

JP: not a big fan of having null ref, only to support default values in table, should say undefined entries in table is bad, almost like a trap value, but a little late to make that change

HA: We still need null values for local initialized values, so if you have locals for reference types, you still need them for initializing those values. 

AR: it’s hard to avoid having something like this, there are things that become more difficult if you have no way to represent an uninitialized thing explicitly. We still want to make the distinction later, know if something is inhabited by null or not

JP: Wasn’t trying to argue that we should remove null, just pointing out that null is already a wart, so we’re not without warts anyway

AR: I don’t think anybody particularly likes it

BS: end of slides, any other arguments, please share

EVERYONE: thanks Ben

BS: Hopefully fair to both sides

FGM: I’m kinda neutral, prefer there was no subtyping at all, as far as interface types, we will not be using subtyping in any meaningful way. Reason being, when you invoke a func across module boundaries, you will be coercing the data, not casting. In that world, subtype loses all meaning. If the motivation is to support inter-module operation, then IT is saying “we don’t need it for that”

AR: You would probably need it if you want some kind of cross language interop where you have a certain family of languages where you want to pass objects along. You would need some kind of abstract API like the JVM and have several languages compile to the API, that’s where you would need more explicit typing..

FGM: The thing that worried me about that; you're already talking about representing Java types in wasm. Wasm is a meta-level wr.t. to Java, you don't need it at a meta-level.

AR: Not sure I follow. Think this is unclear territory anyway, we don’t really know how/whether we can do it. Main use case for subtyping is not at boundary, but within single lang/runtime, might involve multiple modules, but won’t go through IT.

JP: Just to check one of my assumptions; the goal of removing, is to avoid the need for the runtime to use the same rep for two types, or to reduce need to boxing/unboxing correct?

RT: I have some slides on concreting what that means, can present that. 

AR: One quick comment; for any subtyping we do, it's always coercion free. It's supposed to be closely representing the value rep, we only want to have subtyping that has representations that are fully compatible.

JP: we don’t have any normative guidance in the spec for that

AR: More like a design principle that we want to follow - like a rationale - more meta level

RT: pops up in two spots, implicit direct handling between instructions, if we ever do func refs with some variance, then if a <: b, and func returns a, another func returns b, you can’t dynamically wrap func and do the coercion, has to automatically happen

AR: If you have coercive subtyping then this doesn't compose...

JP: As of last conversation, we were not talking about having coercive subtyping <AR Agrees>, or variance? 

AR: We don't currently have variance, but we may want it in the future.

JP: It’s not that we prevent runtimes from using boxed references...

RT: It's not known that future features will be compatible with it. Languages with subtyping will make it so we would have to coercions.

JP: that might be something you wanna put in the spec

AR: There are always ways to do them, it’s not going to be efficient.

JP: thinking ahead, someone reading the spec, i know whenever funcref becomes anyref, i’ll just coerce, and they get bitten

AR: Problem in general, if you look at Wasm as-is, you can miss the broader picture

JP: It factors into the cost calculation -- if we add subtyping, a VM shouldn't use coercion to implement it.

AR: currently, there are notes in the spec, or you could add notes of some kind, future versions of Wasm likely to have more subtyping

JP: Do we want to look at RT’s slides? 

Ross Tate presenting [slides](https://github.com/WebAssembly/meetings/blob/master/2020/presentations/2020-04-21-tate-embracing-heterogeneity.pptx)

LH: Spidermonkey uses NAn boxing, similar tricks with high tagging have been used, and everytime they are used, someone comes along to replace them. Just want to emphasize that it’s not as simple as presented here. 

RT: Just trying to lay out the possibilities -- I know it's not trivial to make it work efficiently. Also not insisting that everyone has to do this. This is looking toward the future, what an engine may want to do. To try to get Wasm VMs to match performance of specialized engines.


<back to slides>



AR: I don’t see why that’s the case  <LH Agrees>

RT: Imagine a Kotlin value is an anyref, so is a Scheme value, how do I interpret those bits?


LH: You’ll need contextual information <RT: You don’t have it> That’s not a problem for type safety

RT: You want deterministic encoding -- if Scheme and Kotlin have the same encoding, anyref, how do you make them work together?

LH: That’s a problem the compiler needs to solve to make sure that does not happen

RT: I can import/export my anyref

AR: Anyref is the same everywhere... but this is ignoring the abstraction level you need between the compiler and architecture they're running on. They have no way to tell the engine that they have 5 bits to use ... so how can you provide optimizations like that?

RT: This why we wrote up a whole thing to show it can happen

AR: You have to go through some abstraction, you need some types of reference types. You need to define them so you can use those bits.

JP: We’re at 14 mins..

RT: At a high level the engine needs to figure out how to adapt, and not be conflict with the GC proposal

AR: I don’t see that being in conflict with the top type. You also say, for imports, we don’t need the top type, but if you don’t have top type as a bound, you still have the same kind of isomorphic type, you have the same situation where you can mix all the types

RT: The thing about type imports is that you can still have… everybody follows the same convention that’s totally fine. The issue that comes up is that if you have anyref, all the info gets put in the same place, and there isn’t a convention of what bits represent.. Unless we dowcast.. Not sure how this would work

AR: Almost all engines out there that use GC use uniform representations. Through NaN boxing or pointer tagging. anyref is the universal type of pointer types. The difference is the pointer tagging scheme, using more or less bits. We can't easily represent that in Wasm, we can't make many assumptions about the number of bits to use. We could have some sort of abstraction with the number of bits, where those bits may end up in an allocation.


RT: You compete at the right architecture level.. If you had everything flow into the same part, then we have to have a consistent way to represent this

TL: Talking about GC proposals right now. IIUC, you're saying that using anyref as uniform rep. would prohibit the use of different language-specific optimizations. Does existence of anyref prohibit optimizations?

RT: The existence, and the assumption that it’s the top type, then any type imports being a subtype then it does

AR: I think this is false. anyref represents the thing that the GC knows about. It has to understand something about the representation. Something minimal. Everything on the GC heap has to share this representation.

<RT pointing to 64-bit machines slides: This is what it’s representing>

AR: But none of these are independent of the architecture you're running on. The anyref is the sum of all things to distinguish refs from non-refs.

TL: Can we agree that we want to leave our options open, about how this would work in the future? And that we can look at RT’s GC proposal, and agree that we leave the door open. 

AR: I don't think we're closing anything. There are assumptions here that don't make sense. It seems unrelated. If you ever want to have a built-in GC, then we need to have commonality between them. The anyref is the type of thing that the GC understands. There is no implication here that it would prohibit anything.

JP: I think the call is for general conservatism - the question is whether a funcref should be a subtype of anyref.. And not to enforce

AR: Of course. It's just capturing what is common to all implementations.


LH: RT is overstate his case, but I agree that it would be useful to have a tagging system and we’re left with anyref which is completely opaque.. As far as we’re concerned, we will probably need something like funcref being a subtype of anyref, but don’t want to commit to anything right now

AR: I don't see how that's related...

LH: Leave the relationship open without assuming it too early..

AR: Sure, if everything else is equal, yes we should defer.

LH: The engineering cost is non-trivial, I really agree with you that we will end up with some type of subtyping but we can afford to defer while we explore this further. 

AR: There are three options. 1) go ahead with what we have 2) we modify ref-type proposal to remove subtyping 3) defer ref-type proposal until we know more

LH: Not an attractive option for the web, we want to ship anyref as a container type for passing host types to WebAssembly

JP: We can include hostref type. [LH: anyref is host ref] otherwise it's just exnref and funcref.

LH: Right now, anyref only uses host types, and exn ref if we count that

AR: We should rename anyref then..

LH: Don’t care what it’s called

JP: Jakob has asked to see Rossberg's slides on chat.

<AR Presenting a slide on required design changes TODO: Add slides> 

RT: It could be useful to leave in the spec where we expect subtyping to be used in the future.

AR: It's not good to specify rules that can't be tested.

JP: It's guidance.

DG: Should we have a poll in the next CG meeting?

<discussion about how to handle poll in the next meeting>

### Closure
