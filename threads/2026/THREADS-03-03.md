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

TL: Working on Binaryen optimizations for reordering memory operations past acquire and release operations in the allowed directions. Currently, the Binaryen effect analyzer has no notion of directionality, so fixing that is the initial project.

TL: Concerned about how to catch bugs here, as we lack fuzzer support for finding bugs when reordering multi-threaded code incorrectly. This is becoming more urgent.

SF: Initial waitqueue support (`struct.wait` and `struct.notify`) is in Binaryen. Parsing, roundtripping, and effects analysis are implemented. Working on interpreter support and fuzzing support.

TL: For now, Binaryen has implemented the packed type version to match V8.

RMH: Completed implementation of acquire/release in V8 Liftoff and Turboshaft. Next will be looking at benchmarks (starting with the Java paper) to compare performance between acquire/release and sequentially consistent versions.

MK: Implementing packed type version of waitqueue in V8. Mostly complete, though currently fixing some bugs related to data races.

DS: Started working on this in LLVM back end. Will soon try to wire everything up from C and C++ and LLVM's memory model.

CW: Are these the benchmarks from the Java paper or different ones?

RMH: They are the ones from the paper. Some links in the paper are dead, so I'll contact the authors and look into the original repositories they used.

CW: Let me know if I can help bother them from an academic email address as well.

#### Waitqueue as a packed type ([#102](https://github.com/WebAssembly/shared-everything-threads/issues/102))

TL presenting [slides](https://docs.google.com/presentation/d/1MvE9Gktuw02D6lHif2ox78qeI8pv684jA_CJDuUmbuU/edit?usp=sharing)

TL: Recapping four design options for waitqueues:
1. **Abstract heap type, subtype of struct**: The waitqueue is a subtype of a struct with a single mutable i32 control word. Advantage: Reuse all existing and future struct accessors (RMW, different memory orders). Disadvantage: Hard to implement subtyping and runtime casting for an abstract type that is a subtype of a defined type.
2. **Packed type**: Waitqueues are fields baked into structs (like i8 or i16). Advantage: Easy to implement in structs. Disadvantage: Cannot be easily copied; `array.copy` would need special casing or waitqueues would be banned in arrays.
3. **Boxed control word**: Waitqueue is an abstract heap type that points to a separate struct containing the control word. Advantage: Conceptually easiest, avoids type system "sweat" or special cases in optimized struct code (like finalizers). Disadvantage: Adds an observable indirection/memory overhead.
4. **Defined type**: Explicitly define waitqueues in the type section as subtypes of structs. TL finds this "weird" as it still requires the engine to represent it as a struct.

TL: Proposed a new implementation strategy for Option 1: implement it internally using a packed field (Option 2) but expose it as an abstract type (Option 1). This gains implementation benefits while keeping the language design clean.

CW: This desugaring approach seems a little scary. I'd want to think through it in more detail.

TL: In the actual language, the internal desugaring is not visible. To the extent it's scary, it's only for implementers. It's no scarier than just doing the packed type thing, which we're already doing as the easiest path.

CW: In this design, are you expecting `(ref waitqueue)` to be a subtype of anything more normal, like a struct?

TL: Yes, exactly like the original design.

CW: If you have a struct with a field that is a supertype of `(ref waitqueue)`, would that cause problems with code generation if the field then wouldn't be inlined?

TL: In Option 1, the waitqueue itself is not inlined in the user-defined struct; it's a reference. This is different from Option 2, where the waitqueue is an inlined field.

CW: So this is essentially saying we'll use the packed field internally but not expose it to users because the user-level copy semantics are irregular?

TL: Exactly.

RH: Prefers Option 3. It avoids adding special cases to optimized struct code, which is helpful for implementers.

CW: What's the difference between Option 3 and the desugaring approach?

TL: The difference is subtyping. In Option 1, the waitqueue is a subtype of the struct and contains the i32 field. In Option 3, the control word is in a *separate* struct outside the waitqueue, and you need an extra instruction to get a reference to that other struct.

CW: Why does the control word need to be observably boxed? Why not just have special instructions to get/set the control word?

TL: We have so many struct accessors for i32 (RMW, different memory orders). We want to reuse those rather than duplicating all of them just for the waitqueue control word.

CW: We're already engaging with the instruction duplication problem in other proposals, like the multibyte array accessors. We shouldn't overindex on fear of duplication if it avoids a random, unnecessary indirection.

RH: How many of these are allocated? If it's one per mutex, memory overhead might be fine. In Java, every class implicitly has a mutex.

CW: I'm more worried about the "sad cost" of the extra indirection every time you affect the control word. It's an overhead we're effectively putting into the language that users can't avoid.

TL: For performance, you're mostly modifying control words when about to sleep or try to acquire a mutex. In the contention case, it doesn't matter. In the fast case, maybe it does.

MK: How does the dereference interact with atomic accesses?

TL: You'd do `waitqueue.get_control` to get an immutable reference to the struct, and then perform whatever atomic operations you want. You'd only need to do the "get control" step once per function.

RH: The indirection cost might be minor compared to the cost of atomic operations or actually going to sleep on a mutex.

CW: We could start with Option 3 and benchmark, but I expect on x86 you could come up with a slightly silly looking low contention microbenchmark where the extra access is visible, since on x86 atomic loads are just regular loads.

JK (in chat): Suggests updating typing of existing struct accessors to accept a waitqueue (e.g., using a sentinel value for the type index) as an alternative to subtyping.

TL: A sentinel value for the type index is similar to the extra bit we've implemented in Binaryen for the multibyte array access proposal (using bit 4 of the alignment field to indicate an array access).

CW: I wouldn't be against that. It's a reasonable solution, even if it doesn't necessarily extend to everything we're doing with arrays.

JK: Leaning towards a design that reflects implementation (packed fields). Waitqueues in arrays aren't useful, so banning them there is fine.

RH: Concerned about semantically having a field that cannot be copied, especially if we add `struct.clone` in the future.

JK: `struct.clone` wouldn't be a simple memcopy anyway because reference fields need write barriers.

JK: The fundamental dilemma is between reusing struct operations and future compatibility with copying. If we want both, indirection might be necessary.

JK: Linear memory wait/notify uses one massive central registry and a global lock. Waitqueue allows independent locks per queue, enabling better performance.

TL: Control words are arbitrary integers. For example, the linker-injected start function uses 0, 1, and 2 for a memory initialization protocol.

RH: Bias access to the control word for the uncontended case; indirection is more acceptable for the queue access (sleeping).

RH: Could `waitq.new` return two results: the control word struct and a reference to an opaque waitqueue?

JK: What if we have a magic packed field that `struct.get` cannot access? It would only be used by `struct.wait` and `struct.notify`.

MK: `struct.wait` could take both the field index for the waitqueue and the index for the control word.

TL: This would even allow the waitqueue and control word to be in different structs.

CW: If they are separate fields in the same struct, it's compact and likely what users want.

RH: Why not just an atomic load + separate wait instruction?

CW: You need the comparison and the sleep to be atomic with each other to avoid "time of check, time of use" bugs where you miss a notification and sleep forever.

Conclusion: TL will take it as an action item to write up a table of these new options and tradeoffs for the next step.
