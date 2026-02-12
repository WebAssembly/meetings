![WebAssembly logo](/images/WebAssembly.png)

## Agenda for the February 3, 2026 video call of WebAssembly's Threads Subgroup

- **Where**: Google Meet
- **When**: February 3, 5pm-6pm UTC (February 3, 9am-10am Pacific Time)
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
    1. Check in on status of threads repo (Thomas Lively, 5 minutes) 
    1. Update and discussion on relaxed atomics prototyping (Rezvan Mahdavi Hezaveh, 30 minutes)
    1. Shared string builtins ([#103](https://github.com/WebAssembly/shared-everything-threads/issues/103)), (Thomas Lively, 10 minutes)
    1. Waitqueue as a packed type ([#102](https://github.com/WebAssembly/shared-everything-threads/issues/102)), (Thomas Lively, 15 minutes)
1. Closure

## Meeting Notes

### Attendees

 - Thomas Lively
 - Matthias Liedtke
 - Rezvan Mahdavi Hezaveh
 - Steven Fontanella
 - Andreas Rossberg
 - Conrad Watt
 - Deepti Gandluri
 - Emanuel Ziegler
 - Manos Koukoutos
 - Nestor Mata Cuthbert
 - Nick Fitzgerald
 - Jakob Kummerow
 - Ryan Hunt
 - Derek Schuff
 - Kevin Moore

### Discussions

#### Check in on status of threads repo (Thomas Lively, 5 minutes) 

TL: What's up with the PR to restore the tests?

CW: I was hoping to go back and run all the tests individually. Are you happy with a rubber stamp?

TL: I ran all the tests, and to be clear they all existed before. I'm happy with a rubber stamp

CW: Is there not a separate folder for threads tests? How did they end up in core?

TL: Oh maybe there were moved. Yes, looks like the tests just moved. I will double check everything in the PR.

CW: Ok sorry I thought this was a bigger PR. Weren't there issues with other non-thread tests?

TL: This started because importing tests into V8 complained about missing tests. I guess they were just moved. So I think this is a nothingburger, but I'll double check.

TL: The other open PRs are about memarg alignments.

CW: Updating the binary format in the overview and making non-natural alignment a validation error in the interpreter. I guess we can just accept these as-is. I just want to check that this is consistent with the way we do single-threaded memargs. Want to make sure the check is in the same place.

TL: For single-threaded memargs the check is that the alignment is not greater than the natural alignment. I think that's validation.

AR: Yes, I just reviewed a PR about that.

CW: That's the PR we're talking about. So we just have to follow up on Andreas's nits and then we can merge these.

#### Update and discussion on relaxed atomics prototyping (Rezvan Mahdavi Hezaveh, 30 minutes)

RMH sharing [slides](https://docs.google.com/presentation/d/1ubKhrGBEGIVr4AgzUmJgnGEgPU8jArK-skN5sadjrcA/edit?slide=id.g3c5f7424c85_0_0#slide=id.g3c5f7424c85_0_0)

RMH: We are prototyping release/acquire atomic accesses to memory and planning to split them out as a separate proposal from shared-everything. It uses bit 5 of the memarg to signify that an ordering immediate follows. If there is no memory ordering immediate, it uses seqcst by default.

RMH: RMW operations require two ordering immediates, but they must match.

CW: Is the immediate an LEB or a byte? Are they distinguishable?

TL: It's a byte, but we don't use the high bit. The difference is that we don't accept the longer encodings. It would be backward compatible to make it an LEB in the future.

CW: How many orderings does the current encoding support?

TL: For RMW instructions we're packing both arguments into the same byte, so each one gets four bits.

AR: If you want to keep it extensible to LEB, then only 3 bits.

CW: True, so only 8 orders.

TL: I hope we never get there.

SF: I've been working on Binaryen support. It's done. We can parse and print the new instructions in binary and text. It's exposed in the libraries. We have fuzzing support. We also have initial spec tests.

RMH: On the V8 side the implementation is started behind a disabled flag. Working on validation and liftoff implementation for ARM, ARM64, ia32, x64. Observed that acquire loads generate the same code as seqcst loads on all architectures. For release stores we have shorter generated code in three architectures. RMW operations are identical on all architectures. Fence is shorter in two architectures. Feedback about this? Is it worth including release/acquire RMW ops?

AR: It makes more sense to consistently add them everywhere even if it doesn't make a difference. It might make a difference on future or esoteric architectures. I would like to see some numbers about what these can achieve before we add more memory orderings.

RMH: Getting numbers makes sense.

CW: It should be possible ot make a microbenchmark on x86 that looks ridiculously good. The question is about macrobenchmarks. With respect to adding acquire/release to only some instructions, it's safe to do that as long as we have a path to add them to all instructions in the future. But I would prefer to be uniform. I have a roadmap for more relaxed orderings in my head, but other languages are slightly regretting trying to add more relaxed orderings, e.g. C++ with their relaxed ordering. I have a pet ordering that I'd be happy to pitch at some point. It does for ARM what this proposal does for x86.

JK (chat): adding two separate immediates for RMW operations, while also requiring them to be the same, seems particularly unnecessary when they have zero effect on codegen. We can always add them if/when some architecture can benefit from them.

CW: I see your point. IIRC, there is a way in ARMv7 that having two different orders matters, but it requires a weaker ordering. So this is a forward-looking thing for when we have more orders.

TL: And the reason to include both encodings or both orderings now is that if we had the one immediate and only included one ordering, that would be hard to differentiate in the future where we want both immediates. It gives us more optionality in the future to encode both now.

CW: I agree. If we want acquire/release RMWs, we should definitely have two immediates. It's not so bad for binary size because they're packed. It's just annoying in the decoding. But that could also be an argument against having acquire/release atomics at all for now. I don't have a strong opinion.

JK: It's already not uniform. It doesn't reuse anything. It's a special case just for the RMW instructions. It has zero benefit. We have bigger fish to fry.

CW: I think it's too strong to say that it's not uniform, but I agree with your other points.

JK: I would buy an argument that we want all memory immediates to have the same bits. But loads and stores have one byte and RMWs have two nibbles.

CW: Can you just see the byte on loads and stores as two nibbles?

AR: Could also use the eighth bit in the future to signal that there's a second order following. So it would be safe to have only one immediate on RMWs now.

JK: Right. We could split the byte in the future.

CW: I'm willing to concede any binary encoding argument. Whatever makes people happier.

AR: Yeah we're well into bikeshedding territory.

CW: But maybe the higher level point is that maybe this complexity is a sign that we should just defer release/acquire RMWs.

JK: That would be my suggestion. We can add relaxed RMWs once there is an architecture that benefits.

AR: Well I don't know, there is the precedence in C++.

JK: C++ is not a good example for WebAssembly.

CW: Technically release/acquire RMWs already have different codegen on PowerPC. So that's an architecture that would benefit today.

AR: It doesn't seem a big deal either way. If it doesn't matter for your architectures, you just ignore the bits after validation.

DG: Are there also languages besides C and C++ that could benefit from release/acquire in their toolchains?

CW: IIUC, there are a couple more optimizations allowed. I don't know what they are. I can try to talk to an expert and find out.

DG: But that would indicate production compilers probably aren't doing those things.

DS: I looked and could not find any instance of LLVM taking advantage of this.

CW: What do folks think of the PowerPC argument? It's a less powerful barrier.

AR: It's an existence proof that it might matter, even if you don't consider it a relevant architecture now. It might be relevant in the future. If we defer, we will have all these toolchains emitting suboptimal code. And it's not much extra work.

TL: Yeah the extra work is so low that it seems worth it even if we don't care particularly much about PowerPC.

ML: This is split out of shared-everything, which is usecase-driven. Is there anyone asking for this? Or do we just assume it's useful for C++?

TL: We still need to get numbers.

CW: Procedurally we're on the path to split out the proposal to take to phase 2 for relaxed atomics, right? The barrier for phase 2 is low enough that we don't necessarily need numbers before going further.

AR: Right, that's the phase or even phase 3 is where you get numbers in the first place.

CW: Eventually we have to go to the full CG.

AR: Yeah this is the first time I'm hearing about this plan. It makes sense, but this group can't decide that.

TL: Yeah. Did we have a timescale in mind?

RMH: We can do it soon, but we're not in a rush.

TL: Whenever it makes to move to phase two.

RMH: I'll try to get the numbers so we have something to talk about.

#### Shared string builtins ([#103](https://github.com/WebAssembly/shared-everything-threads/issues/103)), (Thomas Lively, 10 minutes)

TL: Planning to overload the existing builtins with additional shared function types that take shared externrefs. You can round-trip an unshared string to shared by passing it out to JS and back in and vice versa.

CW: Could you just feed the same string in twice as both shared and unshared without the round trip?

TL: You could, at the price of having two imports. If at runtime you have some dynamic string you still need to pass it out and back in to convert.

AR: So your point is you can cast from one to the other by going through JS essentially.

TL: Exactly. V8 will prototype this, with the exception that the overloaded function types will not be shared because we don't support shared functions yet.

AR: In theory you could overload it three ways.

TL: Yes, but in the long run we should only have two. Ryan, you've thought about this before. Any concerns?

RH: This seems reasonable. Tangential question: What JS primitives are allowed to inhabit shared externref? You could have a shared struct with a shared extern field and you could put JS numbers there. What's the semantics of that? Just strings or other stuff, too?

TL: What's written down and envisioned is that any JS primitive can be shared.

ML: But that's not what we implemented. So far we don't support bigints and some other cases.

RH: Right, I was thinking of bigints and Symbols.

ML: Those are the two v8 doesn't support right now. And everything else was implemented for the JS shared structs prototype, but parts are missing.

TL: It's a bit of a sticky situation. The overview for shared-everything points to JS shared structs and says we'll inherit all its functionality, but it looks like shared-everything threads will move faster. Maybe we need to just support shared strings for now to move forward. If JS adds more shared things in the future, then great, those will work, too.

CW: Is there any value to this proposal if you don't have shared GC structs? That seems like the only reason you'd want this.

TL: Yeah, we're talking about shared JS structs.

CW: Right, but just checking that shared strings are only useful if you already have shared Wasm structs?

TL: Yes.

RH: Are there any JS spec changes necessary for shared JS primitives? You can't necessarily observe that they have been shared. Is there really a dependency on JS shared structs?

TL: You're right. Technically there are no spec changes on the JS side. For JS, the question is what you can put into a shared struct, it becomes visible on that assignment. For us that would be what JS values we allow to enter Wasm as shared externrefs in the ToWebAssemblyValue algorithm. That's under our control.

CW: We shouldn't be more permissive than the ideas around JS shared structs. So we shouldn't do more than allowing primitives.

TL: Agree. And we don't know of use cases besides strings yet. I wouldn't be surprised if they come up.

RH: This makes sense. Is it written down in the proposal or do I have to go to the JS structs proposal?

TL: It just points to shared structs. We can clean that up and be more precise.

CW: Can we expect an update about shared Wasm structs?

TL: We are working on them. There is a prototype that may or may not be usable behind a flag. We're waiting for Conrad's paper to tell us how to do barriers on initialization.

CW: You should already know how to do that.

TL: Sure, but we're not doing it yet.

CW: That's wrong.

TL: We know. There are other problems like our load elimination pass incorrectly eliminating atomic loads. We don't have these problems for linear memory because we can't optimize it as much. So that's why you haven't heard a more formal update yet. It's horribly broken.

#### Waitqueue as a packed type ([#102](https://github.com/WebAssembly/shared-everything-threads/issues/102)), (Thomas Lively, 15 minutes)

TL presenting [slide](https://docs.google.com/presentation/d/175WlQpDu944ogvC1_DYENaUV9Es7BvQBW1ND3MSxE6U/edit?usp=sharing)

AR: What if I do struct.get on this field?

TL: It behaves like an i32 field with additional wait and wake instructions.

CW: That's a little scarier than I thought from the previous sketch. If you allocate a new one, what's the value of the field?

TL: Zero, probably.

CW: If you have two structs with the same value and they both wait, do they see each other's signals?

TL: no no, the value is for the control word for atomically checking a condition and going to sleep. Separate wait queues never interfere with each other.

AR: We have assumptions all over the place that packedtypes are transparent. This is scary.

CW: It can't show up in a memory load, for instance.

AR: Exactly. It it adds a new kind of type to the whole algebra which seems slightly ad hoc.

TL: Do we express memory loads in terms of packed types? I thought it was only GC fields.

AR: Why can't this be a separate hierarchy not compatible with anything?

TL: We would need to duplicate every instruction for manipulating the control word. Get and set and all the RMW instructions.

CW: That would involve extra boxing, too.

TL: We're not too worried about that aspect, but it's nice to avoid the indirection.

CW: I don't hate it. I actually quite like it.

AR: It's still a new class in the type algebra, which is already super complicated.

TL: I'm happy for us all to noodle on this one a bit. Meanwhile we (V8) will go ahead and implement the new design for our prototype.

RH: Having these in arrays and updating array.copy is scary. I have to think through some other implications, but maybe it's fine.

AR: I also think it's scary. For example when we do a struct.get, we assume there's a sign extension precisely when it's a packed type. There are all these little things we can fit in somehow. The lattice is huge.

TL: I'm sympathetic to concerns about the complexity and the type algebra. This was motivated by other complexities the old design had. We have to put the hair somewhere. Ryan has a good point about array copies, though. Maybe we need this only in structs. Or maybe array.copy would only copy the control words, but then it couldn't be a memcpy anymore.

AR: There's the post-MVP feature of flatting arrays of structs. So this wouldn't compose well.

TL: Let's noodle on it more.
