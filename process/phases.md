# WebAssembly W3C Process

This file describes how feature proposals will progress through
the standardization process.

A feature is a substantial change to WebAssembly, such that it for example
requires additional opcodes, types, tests, or module sections.
See case #3 [here](consensus.md).

Something is definitely a feature if it:

  * Adds an opcode or other pieces of abstract syntax
  * Changes or extends the binary format
  * Changes or extends the text format
  * Requires adding or changing tests
  * Requires extending or changing the reference interpreter

Something is out-of-scope if it doesn't fit the [WebAssembly Working Group's charter](https://www.w3.org/2017/08/wasm-charter) and there's agreement that the charter should not be amended to cover the proposal.

In general, the process moves forward through a series of numbered phases.
However, if issues are uncovered or consensus devolves,
proposals should back up to the appropriate prior step.

No vote is required for a proposal to enter phase 0. To advance from one phase
to another, a vote proposing the advancement is added to a
[Community Group meeting](https://github.com/WebAssembly/meetings/) agenda
through a pull request, and the CG votes on whether to approve it, evaluating
whether the new phase's entry requirements have been met.

## 0. Pre-Proposal [Individual Contributor]

Entry requirements:

  * A Community Group member has an idea. Notably, no CG vote is required to begin phase 0.

During this phase:

  1. An issue is filed on the [design repository](https://github.com/WebAssembly/design/issues) to present the idea.
  1. Discussion on the feature occurs on the issue.
  1. A champion or champions emerge.
  1. The champion(s) put together a somewhat-formal description of the feature in their own GitHub repository or on the issue.

## 1. Feature Proposal [Community Group]

Entry requirements:

  * There is general interest within the CG in this feature.
  * The CG believes the feature is in-scope and will plausibly be workable.

During this phase:

  1. If the proposal is not already listed, it should be added to the [proposal list](https://github.com/WebAssembly/proposals/blob/main/README.md) at this time.
  1. A new repository, forking the spec repo, is created by one of the WebAssembly organization administrators, or transferred to the WebAssembly organization by the champion. See the [how-to](https://github.com/WebAssembly/proposals/blob/main/howto.md) for this step.
  1. The champion will attempt to reach broad consensus in the Community Group.
  1. Pull requests and issues are used to iterate on the design of the feature. Specifically, an overview document must be produced that specifies the feature with reasonably precise and complete language before attempting to move to phase 2 (meaning it is sufficiently precise to be implemented following this description, without obvious holes or ambiguities).
  1. If relevant to demonstrate the viability of a feature, prototype implementations of the feature are implemented by interested embedders (possibly on a branch).

## 2. Feature Description Available [Community + Working Group]

Entry requirements:

   * Precise and complete overview document is available in a forked repo around which a reasonably high level of consensus exists.
   * *Updates to the actual spec document, test suite, and reference interpreter are NOT yet required.*

During this phase:

   * One or more implementations proceed on prototyping the feature to the point that a comprehensive set of tests can be added.
   * A test suite is added in the forked repo. These tests need not pass the reference interpreter at this point, but should pass on the prototype or some other implementation (this primarily is to check that the test suite is functional).
   * Updates to the reference interpreter are not yet required at this point, but recommended.

## 3. Implementation Phase [Community + Working Group]

Entry requirements:

   * Test suite has been updated to cover the feature in its forked repo.
   * The test suite should run against some implementation, though it need not be
     the reference interpreter.
   * *Updates on the actual spec document and reference interpreter are NOT yet required (but can happen earlier).*

During this phase, the following proceeds in parallel:

   * Engines implement the feature (where applicable).
   * The spec document in the forked repo is updated to include the full English prose *and* formalization.
   * The reference interpreter in the forked repo is updated to include a complete implementation of the feature.
   * The feature is implemented in toolchains.
   * Remaining open questions are resolved.

## 4. Standardize the Feature [Working Group]

Entry requirements:

   * Two or more Web VMs have implemented the feature and pass the test suite (where applicable).
   * At least one toolchain has implemented the feature (where applicable).
   * The spec document has been fully updated in the forked repo.
   * The reference interpreter has been fully updated in the forked repo and passes the test suite.
   * The Community Group has reached consensus in support of the feature and consensus that its specification is complete.

NOTE: By this point the proposal is basically frozen, since 
the Community Group is the sole venue where substantial changes are made.

At this point:

   * The feature is fully handed off to the Working Group.
   * During this phase, Working Group members discuss the feature,
     consider edge cases,
     work to confirm consensus that the feature is now complete,
     and fulfill requirements of the W3C standardization process.
   * Periodically, the Working Group will hold polls on how "ship worthy" the feature is,
     in order to help browsers to make decisions about when to ship.
   * Only minor cosmetic changes occur at this point.
     If substantial changes are deemed required, the feature is sent back to
     the Community Group.

## 5. The Feature is Standardized [Working Group]

Entry requirements:

   * Consensus has been reached amongst Working Group members that the feature
     is complete.

During this phase:

   * Editors perform final editorial tweaks and merge the feature into the main branch of the primary spec repo.

W3C snapshots (for REC) are made at a regular cadence (in a W3C repo), used
to stamp official version. Matching tags are added in the github spec repo.


## FAQ

#### Who owns the various existing W3C repos?

They are owned in common by the Working + Community Groups. The Working Group
uses the github.com/WebAssembly/spec repo to iterate on finalized proposals
for hand-off
to the W3C's snapshotted copy of the spec. The other repos are primarily
overseen by the Community Group.

#### What about licenses?

The [W3C Community Contributor License Agreement (CLA)](https://www.w3.org/community/about/process/cla/) governs contributions to the spec and proposal repositories.
In the Working Group, the spec and spec forks will move to a
[W3C Software and Document Notice and License](https://www.w3.org/copyright/software-license/).
Other related repos for prototypes + tools will continue under their respective
licenses.

#### What is the Community Group for?

Incubation.
To provide a safe harbor for a broad set of stakeholders to discuss, design,
and iterate on new features during Steps 1-3 above.
It should attempt to address all concerns, but need not reach 100% consensus.

#### What is the Working Group for?

To fulfill W3C standardization requirements on mostly complete specs + test suites 
from the Community Group.

Changes to the spec need not have reached full consensus in the Community Group
to move to the Working Group, but key Working Group stakeholders should resolve
outstanding mismatch in the Community Group.

#### Who will have admin rights + close issues etc?

This can be distributed and handled by multiple folks.
In terms of github issues specifically, chairs will mainly step in to drive
consensus, keep discussions civil, and as a first escalation point if someone
is unhappy with how the collaboration is conducted (for instance if someone is
unhappy a particular issue was closed over their objections).
This is a general part of their role in community building:
https://www.w3.org/Guide/chair-roles
