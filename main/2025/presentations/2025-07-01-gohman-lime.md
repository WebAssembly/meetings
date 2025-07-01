---
title: "The Lime series of Wasm feature sets"
author: Dan Gohman
---

The Lime Twist
--------------

Some developers are still using the Wasm MVP or Wasm 1.0.

<!-- pause -->

Wasm 2.0 includes simd and reference-types, and excludes extended-const.

<!-- pause -->

There's a need for curated feature subsets!

<!-- end_slide -->

It's Lime Time
--------------

Lime is series of feature sets, defined here:

**https://github.com/WebAssembly/tool-conventions/blob/main/Lime.md**

With the full force and authority of... a file in
the `tool-conventions` repo.

<!-- pause -->

```
clang -mcpu=lime1 ...

wasm-tools validate --features=lime1 ...
```

<!-- end_slide -->

Lime on!
--------

Lime1 features:
  - mvp
  - mutable-globals
  - multivalue
  - sign-ext
  - nontrapping-fptoint
  - bulk-memory-opt \*
  - extended-const
  - call-indirect-overlong \*

<!-- end_slide -->

About those asterisks
---------------------

bulk-memory-opt: subset of bulk-memory
 - just `memory.copy` and `memory.fill`
 - no `table.set`, `memory.drop`, etc.

<!-- pause -->

call-indirect-overlong: subset of reference-types
 - just overlong `call_indirect` immediates
 - no actual reference types

<!-- end_slide -->

Questions?
----------
Should Lime1 include exception-handling? simd? tail-calls?
 - No, but maybe Lime2 should!

<!-- pause -->

What about something completely different?
 - Lots of other fruits available!

<!-- pause -->

Should Lime1 be a standard? A *profile*?
 - Let's talk about that when/if it becomes popular!

<!-- end_slide -->

More Questions?
---------------

<!-- end_slide -->
