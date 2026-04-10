Agenda for Phase 3 Vote of `Rounding Variants Proposal`

---

# presenting the test cases

- [testcases](https://github.com/WebAssembly/rounding-mode-control/blob/main/test/core/rounding-variants.wast)

- they detect mix ups of all four rounding variants
- minimal; so that they can be useful while implementing the extension and for test suites
- there is a reference runtime update that implements the opcodes
- the testcases are cross tested with several implementations
  - nasm (Kloud Koder)
  - RoundingFiasco library (public on hackage)
  - wabt implemention (via `include "fenv.h"`)
  - v8 raw JIT compiled machine instructions (x86)
  - v8 c++ for compile time constant propagation (via `include "fenv.h"`)
  - fork of the reference runtime (ocaml, via mopsa)

---

# presenting helpers

- two selfcontained html test pages
- two examples for feature detection
- post for performance comparison

---

# What we can offer to implementers

- the bytes forming the relevant machine instructions (on different hardware)
- support for the test cases
- reported edge cases shall be included in the test suite
- help with the hex ASCII representations of the numbers in the test cases

---

# poll for phase 3

- I feel confident that the material is mature enough for phase 3
