# [DRAFT] WebAssembly W3C Process

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

In general, the process moves forward through a series of numbered phases.
However, if issues are uncovered or consensus devolves,
proposals should back up to the appropriate prior step.

## 0. Pre-Proposal [Community Group]

Entry requirements:
  * A Community Group member has an idea.

During this phase an issue issue is filed to track a feature idea.
Discussion on the feature occurs.
A champion or champions emerge.
At a point where a written proposal is useful to ground the discussion
of the feature, a new repository is requested.

## 1. Feature Proposal [Community Group]

Entry requirements:
  * A Community Group member requests a repository in which to develop a
    feature.

During this phase a new repository forking the spec repo is created (Community
Group members can request this). PRs + Issues iterate on the design of the
feature.
If a high level descriptions in a design repo style .md files is useful,
these are added to describe the feature as it's being designed.
A [tracking](https://github.com/WebAssembly/design/labels/tracking)
issue is created in the design repo.

If relevant to demonstrate the viability of a feature, prototype
implementations of the feature are implemented in interested embedders (possibly
on a branch).
The Community Group will attempt to reach broad consensus.

## 2. Proposed Spec Text Available [Community + Working Group]

Entry requirements:
   * Full proposed English spec text available in a forked repo around which a
     reasonably high level of consensus exists.
   * *Updates to the formal notation, test suite,
      and reference interpreter are NOT yet required*.

During this phase:
   * One or more implementations proceed on prototyping the
     feature to the point that a comprehensive set of tests can be added.
   * A test suite is added.
     These tests need not pass the reference interpreter at this point,
     but should pass on some implementation.

## 3. Implementation Phase [Community + Working Group]

Entry requirements:
   * Test suite has been updated to cover the feature in its forked repo.
   * The test suite should run against some implementation, though it need not be
     the reference interpreter.
   * *Formal notation in the spec need not be updated.*

During this phase, the following proceeds in parallel:
  * Embedders implement the feature.
   * The forked repo is updated to include revisions to the formalization.
   * The forked repo spec is updated to include implementation of the feature
     in the reference interpreter (OCaml).
   * The feature is implemented in toolchains.

## 4. Standardize the Feature [Working Group]

Entry requirements:
   * Two or more Web VMs implement the feature.
   * At least one toolchain implements the feature.
   * The formalization and the OCaml reference interpreter are usually updated
     (though these two can be done as part of step 3 at the Working Group
      chair's discretion).
   * Community Group has reached consensus in support of the feature.
   * NOTE: By this point the proposal is basically frozen,
     the Community Group is the sole venue where substantial work can occur.

At this point:
   * The feature is fully handed off to the Working Group.
   * During this phase, Working Group members discuss the feature,
     consider edge cases, and work to confirm consensus that the feature is now
     complete.
   * Only minor cosmetic changes occur at this point.
     If substantial changes are deemed required, the feature is sent back to
     the Community Group.

## 5. The Feature is Standardized [Working Group]

Entry requirements:
   * Consensus is reached in amongst Working Group members that the feature
     is complete.

When Working Group consensus is reached (online), editors can merge the feature
into master on the spec repo.
The W3C snapshots (for REC) are made at a regular cadence (in a W3C repo), used
to stamp official version. Matching tags are added in the github spec repo.


## Example how this might work

### Worker based Threads

0. Pre-Proposal
   * Someone proposes adding threads to WebAssembly.
   * They file an issue to discuss this possibility.
   * Discussion continues and a champion for the feature emerges.
   * A request is made to add a threads proposal fork of the spec.

1. Feature Proposal
   * A threads repo is created: https://github.com/WebAssembly/threads
   * Once a human readable .md is agreed on describing behavior + opcodes,
     work to update the spec's English text to reflect the change in a branch
     occurs.
     A few browsers begin to prototype atomic opcodes behind flag to demonstrate
     feasibility.
2. Proposed Spec Text Available
   * The Working Group is informed of the thrads proposal.
   * The proposed spec text is finalized describing the new opcodes for atomics,
     memory model, etc.
   * A test suite exercising threads is created. All the prototype
     implementations can run it.
3. Implementation Phase
   * Work progresses to implement the agree opcodes for atomics in several
     browsers.
   * The OCaml interpreter is updated to simulate threads.
   * The formal language in the spec is expanded to describe atomics and the
     memory model.
4. Standardized the Feature
   * The Working Group examines the spec, looking for edge cases, testing gaps,
     and unforseen interactions with other standards.
   * Everything is in order.
5. The Feature is Standardized
   * Working Group member consensus is reached (potentially by distributed means).
   * Editors merge the spec changes from the branch to master on the spec repo.
   * Browsers turn on atomic ops by default.
   * Profit!

## FAQ

#### Who owns the various existing W3C repos?

They are owned in common by the Working + Community Groups. The Working Group
uses the github.com/WebAssembly/spec repo to iterate on finalized proposals
for hand-off
to the W3C's snapshotted copy of the spec. The other repos are primarily
overseen by the Community Group.

#### What about licenses?

The spec and spec forks will move to a
[W3C Software and Document Notice and
License](https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document).
Other related repos for prototypes + tools will continue under their respective
licenses.

#### What is the Community Group for?

Incubation.
To provide a safe harbor for a broad set of stakeholders to discuss, design,
and iterate on new features during Steps 1-3 above.
It should attempt to address all concerns, but need not reach 100% consensus.

#### What is the Working Group for?

To finalize and ratify mostly complete specs + test suites from the Community
Group.
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
