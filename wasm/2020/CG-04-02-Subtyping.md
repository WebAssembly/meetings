![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the April 2nd video call of WebAssembly's Community Group

- **Where**: zoom.us
- **When**: April 2nd, 4pm-5pm UTC (April 2nd, 9am-10am Pacific Daylight Time)
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

Ross Tate

Ben Smith

Sam Clegg

Francis McCabe

Lars Hansen

Jakob Kummerow

Richard Winterton

Zalim Bashorov

Deepti Gandluri

JP Sugarbroad

Ryan Hunt

Bill Budge

Heejin Ahn

Andreas Rossberg

Luke Wagner

Derek Schuff

Adam Klein

Emanuel Ziegler

Wouter Van Oortmersson

Thomas Lively

Petr Penzin

Pat Hickey

Dan Gohman

Zhi An Ng

Ionna Dimitriou

Jacob Mischka

### Discussion

AR: Prepared some slides for impact on proposals

[Slides](https://github.com/WebAssembly/meetings/blob/master/wasm/2020/presentations/2020-04-02-rossberg-ref-type-subtyping.pdf)

AR: We don't want to have bias in types that can be imported/exported...

RT: You already have this by restricting it to references

AR: Yes that's true, but future feature

<Back to slides>

RT: You say that subtyping is standard, but where is that standard?

AR: standard in type systems, like you have bounded type qualifications

RT: You mean Java, C#? In practical type systems, in order to make it possible, the implementers are moving away from this pattern.

For languages that do use it, to compile quickly they rely on nominal typing to compile quickly

AR: That's a separate thing here... source level types systems are different than low-level type systems. That is very close to what you care about if you care about which values are compatible (representation).

RT: You care about effective type checking correct? <yes> If you lower to representations the subtyping check is a large mutually recursive check. In scaling these things, it’s not clear that the standards implied.. It’s not clear that mixing the standards will be efficient for Wasm. 

AR: I'm not sure I'm doing that ... structural vs. nominal is orthogonal to this. For type imports, you need some structural constraint anyway. I don't see how any would be cheaper than any other one...

AR: Want to continue.. Let’s not make this another structural/nominal discussion

<Discussion about standard/canonical, back to slides>

RT: We've found that you don't need a top type to handle all the different languages ...

PP: Can you elaborate on what the C/C++ API issue was?

AR: Basically, you need to be able to pass values back and forth between C code and Engine, you need a union. What to do about references, you have one field of references. If you have an open-ended set you have a growing number of arguments in the union. It also shows up in how we deal with imports/exports, for example functions, tables, globals, memories. You can use the same reference values there too. I spent some time trying to up with a good alternative there, but so far have failed to come up with anything nice.

PP: This is .. <muffled> A good enough level of abstraction, makes sense for alignment etc. 

AR: We will eventually need this, no way around that - has been the roadmap for 2-3 years. 

<back to slides>

RT: Claim is that code will have a small change, not the spec

LH: That’s not the case, code will also have substantial changes, lots of knock on effects

RT: Want to know what that changes are

LH: I can share this offline.

<AR sharing spec change prototype>
    
AR: not a small change here either, various implications

TL: I have a question about the change in your discussion. My impression is that we're not talking about never having subtyping ever -- we're talking about splitting tree of types into top funcref and top anyref. All of them can have different representations between them.

AR: This gets back to the point about not introducing type bias - about import/export for example. If you import a type, and not have any restrictions why would you make this harder for some types of references? You can go and make a new choice for every new type, but it would be arbitrary, and akin to premature optimization. If there is evidence that for some of these there’s use in flat referencences we can always introduce them later, but we want to have a uniform system first

RT: I can think of reasons to be able to export integers instead of exporting funcref types.

AR: That you would have to box, or use a tagged type

RT: What are the uses for being able to export the funcref type?

AR: For example, can naturally use functions as capabilities.

RT: Usually capabilities are a table of functions, not just one, right?

AR: Can be single functions, too. We actually do that.

AR: Broader point is that we shouldn’t make premature decisions of what somebody might want to do

<Back to slides>

HA: Are we talking about removing subtyping altogether... for exnref does that get removed too? Is this just for funcref? It doesn't change much if it's just that.

AR: For anyref subtyping removal to make sense you also have to remove nullref - the intent is to partition type hierarchy, so if you don't remove it it doesn’t make sense

HA: In that case, if we make exnref a subtype of anyref, then we need to make a new value...

AR: One more generic instruction to take type immediate… 

AR: The other part of the question is whether to remove subtyping altogether. Just dropping funcref subtyping leaves the proposal in an incoherent state. It means we have subtyping in the proposal but no subtyping rules. It doesn't make sense to have subtyping you can't observe or test, so you'd want to remove it altogether. You'd also want to rename anyref to something else. These are at least three further steps to remove clean it up. This is just the effect on this proposal itself -- we also have effects on other proposals.

Bulk memory has a smaller change, exceptions proposal - rules about exnref that would have toc hange. Func ref, the work there is completely invalidated, would have to move that over and redo. Type imports, not much work yet there but it is a deeply impacted proposal. Also mentioned C++ API etc. At least 3 and a half of these are already implemented, they all would be impacted - all the implementations have to change. More churn - so we should seriously consider if we want to impose the change. Not a question of a couple of days, at least a couple of weeks for every implementation. This is the roadmap we had agreed on, by abandoning some aspect of it - what do we do with the rest of the roadmap - do we want to reconsider the entire roadmap? 

JP: Last time Ben asked about Luke's experience w/ subtyping?

LW: Which experience? 

BS: LW chimed in earlier about type imports in the github issue..

LW: Design we have now will work, we don’t have the weight of a full import, can also see the other side. It seems premature to commit to subtyping.. Ambivalent right now. I can imagine multiple successful paths. Let’s put our weight on subtyping.. And we can figure out all the implications. What should we have in the short term - makes sense to have the universal solution

AK: You're ok going conservative approach now, but you're thinking we will re-add this. But you're interested in more feedback.

LW: Can’t say I’m positive there are no problems, can’t point out is what we specifically will regret

RT: One thing I've pointed out is that we don't have a current language to work with the current plan. I've been worried about this for two years. I found other solutions...

AR: What part of that is related to the proposal at hand? 

RT: Something I've been wondering about is how this works with call_indirect.

<RT [Sharing slides](https://github.com/WebAssembly/meetings/blob/master/wasm/2020/presentations/2020-04-02-tate-call-indirect-subtyping.pptx) - how does this interact with call_indirect?>

RT: <bringing up issues w/ subtyping on "Test 2" slide>

JP: The current spec doesn't admit this though. The only reason for it is allowing having a heterogenous table.

RT: Do we ever want to add subtyping that people rely on? 

AR: We probably need to at some point. But we will obviously have to maintain coherence between different uses of subtyping. If we decide that extending call_indirect is not a practical choice, we can add a variant of function type that is subtypable or not. We can play around with options later.

RT: This should be known answer by now

JP: It is... 

AR: This is only relevant when you get to the GC proposal. 

RT: My question is, should this work eventually?  When that works, will this call_indirect work? 

AR: That depends on what we figure out... if we figure out that we can implement this efficiently, then we will make it work. if not introduce something else.

LW: I’ve been assuming that this wouldn’t work because it uses type equality

RT: <explains> If it doesn’t match you have to know where this type import comes from...

LW: call_indirect does a dynamic check, so...

RT: Bottom half of this program.. what should we expect?

AR: I don't disagree with you. Whatever we do has to be coherent.

RT: You are making us commit to this choice soon..

AR: Disagree, we're leaving it open. Constraining to equality is conservative.

RT: Flip side is we incorporate subtyping into call _indirect.. Callee and caller signature have to be compared by type equality

<Discussion about Test1, Test2>

JP: When you run Test1, it traps - the spec says you don’t use subtyping here <RT agress> 

AR: The program won’t link

RT: When you get to supporting subtyping correctly, this will link

AR: Once we get to the point, we have to decide on a coherent solution. 

RT: With every system.. If you make decisions one step at a time.. It’s regretted, this will come up soon

AR: Can't avoid incremental design. Question will come up in the GC proposal

JP: Where do you see this being used? 

RT: Understand now, that the behaviour is consistent, the question is has any language with subtyping have compiled to use these semantics? 

AR: Many mainstream languages don’t have contravariance

<Overlapping discussions>

AR: We are doing an incremental design process

LW: It’s hard to dismiss the possibility that we make a choice now that we regret later

BS: We only have three minutes left in this discussion

RT: Subtyping complicates everything, we haven’t gone into all the details

BS: The current use case that we have is the idea of exnref, it does feel compelling to accept some amount of churn - it seems reasonable to say that we can remove subtyping for now, and add this on later when we’ve had more investigation into figuring out exactly what we need

AR: Want to refute RT, this is the most basic subtyping, we don’t make any assumptions with what we’re introducing right now, this is how we have been doing development in wasm so far

BS: But the point is removing the any ref func ref that’s actually being introduced right now

AR: If you remove it, it’s removing all subtyping at that point

<More discussion about the cross cutting aspects of it>

LW: Makes sense to delaying the subtyping for the reference types proposal, for when we need subtyping we can make that decision later

AR: Problem is the churn, and the warts we introduce, at least leaves the C-API in limbo

**Straw poll**: Should we have subtyping in the Anyref proposal? 

Poll is not binding, only to get a sense of the room and as a way for folks to express their opinion who haven't chimed in yet.

| Agree | Neutral | Disagree |
|-------|---------|----------|
| 5 | 13 | 4 |

Conclusion: Room is pretty evenly split - what next? Another off cadence meeting to be scheduled because of Easter holidays,
and scheduling constraints, and the general interest to be able to make a decision here quickly. 

### Closure
