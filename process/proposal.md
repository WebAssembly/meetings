# Creating a WebAssembly proposal

The formal process for standardizing a WebAssembly proposal is described in
[phases.md](https://github.com/WebAssembly/meetings/blob/main/process/phases.md),
but this document covers the initial stages in more detail and is meant to be
useful to you if you have an idea for a proposal and want to know how to get
started proposing it.

## Identify a problem

Any proposal to extend WebAssembly should include a clear explanation of the
problem it's trying to solve. In a way, identifying the problem is more
important than the initially proposed solution–it's the problem that will
motivate the community to get involved and help move a proposal forward, not the
details of the proposed solution.

The problem you identify should be in-scope for the WebAssembly community group,
meaning it should be about making WebAssembly faster, more capable, more useful,
or easier to compile to. If you're not sure whether your problem is in-scope,
that's ok! Part of the initial discussions about your proposal will involve
figuring that out as a community.

The most successful proposals also solve concrete problems that people are
already facing. Having real application or toolchain developers asking for your
problem to be fixed is a great motivator for the community to work on it. If
your proposal will solve a performance problem, having an estimate of how much
of a performance improvement the community can expect will also be helpful.

## Come up with a solution

You should view your initially proposed solution as a place to start the
conversation around your proposal. Most proposals go through significant changes
in response to community and user feedback as they move toward standardization,
so you shouldn't get too attached to the details of your original design. Things
like choosing encoding details and drafting formal spec text that are important
in later phases are not as useful at this early stage. That being said, your
solution should be detailed enough that it is clear how it fits in with the rest
of WebAssembly and how it might be implemented in WebAssembly engines and tools.

## Share your proposal

Congratulations! If you've made it this far, you officially have a phase 0
proposal. The next thing to do is share your idea with the community. The best
place to start is by filing a new GitHub issue on the [design
repo](https://github.com/WebAssembly/design). The issue should contain an
explanation of the problem you aim to solve and your proposed solution.

Your design issue will probably get at least a few responses and it might get a
lot of responses. For most phase 0 proposals a single GitHub issue is sufficient
to manage the discussion, but if there is too much feedback for a single issue,
you can request a dedicated GitHub repository for your proposal. A dedicated
repo will allow you to manage feedback via multiple GitHub issues or discussions
and use PRs to update your explainer document.

Once you've addressed any initial feedback it's time to bring your proposal to
the full community to advance to phase 1. Make a PR to the [meetings
repo](https://github.com/WebAssembly/meetings) to add a discussion of your
proposal and a phase 1 vote to an upcoming meeting. At the meeting, you will
present your proposal and the community will discuss it and do a consensus vote
on whether they consider your problem and proposed solution in-scope for the
community group. If consensus is achieved, and it almost always is at this
phase, your proposal will officially enter phase 1.

## Phase 1 and beyond

At phase 1 your proposal receives a dedicated proposal repo if it doesn't
already have one and it is added to the [list of
proposals](https://github.com/WebAssembly/proposals). This is where the real
work of prototyping and iterating on the proposal to achieve consensus really
begins. Unfortunately, just having a phase 1 proposal does not guarantee that
the community will work on it. Part of a proposal champion's job is to actively
solicit feedback on the proposal and to motivate others in the community to help
implement it. It's also possible for the champion to contribute implementations
themselves, but ultimately the proposal needs to be implemented and ready to
ship in two web engines and at least one toolchain before it can be
standardized, so it is typically better to make the proposal a team effort.
