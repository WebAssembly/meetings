# Determining consensus

Consensus is critical in a standards process:

* Gathering consensus helps champions guide their proposal with confidence.
* Consensus prevents needlessly revisiting topics unless new information
  surfaces warranting such revisitation.
* If members don't believe that their voices are heard then the process can,
  over time, break down. Recording dissent is therefore a critical part of
  building consensus.

## Informal consensus

It is critical that work progresses between meetings: agreed-upon designs need
to move forward, and new ideas need to reach some level of maturity before being
discussed before the full CG. To that end, the group can reach consensus
informally via discussion either on GitHub repositories under the WebAssembly
organization or in meetings.

We introduce the following concepts to help determine when informal consensus is
sufficient:

* Contributors of *different affiliation* are individuals who are affiliated
  with different companies or institutions.
* *Interested parties* are individuals, companies, or institutions who usually
  participate in the WebAssembly Community Group or Working Group and are
  interested in a particular topic.
* *Small group* is a subset of Community Group and Working Group participants
  who decide to collaborate on a single targeted proposal.

We differentiate the following cases:

1. Editors are empowered to make changes that have no technical impact without
   explicit group decision. GitHub issues and pull requests are sufficient.
   Their title should identify them as editorial. Closing or merging them after
   a full work day of positive review by at least one contributor of different
   affiliation is acceptable as long as there is no objection. Editors shall
   revisit the editorial nature of the change if there is any contention.

2. Small technical changes or additions can be discussed in GitHub issues and
   pull requests. It is the author's responsibility to ensure that interested
   parties sign off. Simply mentioning people on GitHub may go unnoticed, the
   onus remains on the author to contact interested parties and obtain their
   feedback. Closing or merging after a full week of positive review by at least
   three contributors of different affiliations is acceptable as long as there
   is no objection. Consensus will be deemed to not have been reached if
   interested parties did not sign off. At any point in time a contributor can
   request that final consensus be delayed to a CG meeting. In this case, the
   chair puts the item on the group's agenda of upcoming discussions.

3. Substantial technical changes or additions are developed in their own GitHub
   repository by a champion. It is critical that these proposals be able to
   evolve quickly without much process. Early on in such a proposal's lifetime
   no consensus is needed and a single champion can modify the proposal at will.
   As the proposal matures it is expected that the champion will seek
   collaborators to form a small group or
   [subgroup](https://github.com/WebAssembly/meetings/blob/main/process/subgroups.md).
   Gauging consensus within small groups is left up to the champion and gauging
   consensus within subgroups is left up to the subgroup chair.

Only 1. and 2. apply to the Working Group since the Community Group is the sole
venue where substantial work can occur. It is expected that Working Group
changes or additions in 2.'s category are validated by the Community Group
before being adopted by the Working Group. It is expected that all changes or
additions which reach consensus in the Community Group will be forwarded to the
Working Group for adoption.

When a proposal is near maturity the champion shall bring it to a CG or subgroup
meeting and seek formal consensus on open design questions and contentious
issues. All decisions made by the small group can be revisited until formal
consensus is reached at a subgroup or CG meeting.

When a proposal is ready for phase advancement, the champion shall bring it to a
Community Group meeting and seek formal consensus for phase advancement. No
proposal can advance phases without formal consensus in a CG meeting.

## Formal consensus at meetings

For in-person and online meetings, champions are expected to list points for
which they will seek formal consensus in the meeting agenda at least 24 hours
before the meeting[^phase-1-exception]. Only at in-person meetings can new
formal consensus points be added as the discussion proceeds.

Polling formal consensus is done by the chair:

1. The champion asks a question, which is written down for all to see. Multiple
   related consensus points could be polled back-to-back, in which case they are
   all declared before polling takes place.

2. The chair asks all participants to express their opinion to the question,
   asking in turn whether they are `Strongly For`, `For`, `Neutral`, `Against`,
   or `Strongly Against`. Participants vote for a single option by raising their
   hand, voting in an automated poll, or typing in the chat of an online
   meeting. Alternatively, participants may choose to abstain from voting.
   Aggregate counts for each option are recorded by the note-taker.

3. If deemed relevant, the chair can ask certain participants if they wish to
   explain their vote for the note-taker.

4. The chair determines whether consensus was reached.

5. A participant may decide to register a formal objection to the decision. An
   individual who registers a formal objection should cite technical arguments
   and propose changes that would remove the formal objection; these proposals
   may be vague or incomplete. Note: in the Working Group, formal objections are
   reviewed by the W3C Director. Such review is not guaranteed for the Community
   Group. Formal objections that do not provide substantive arguments or
   rationale are unlikely to receive serious consideration by the Director.

There is no specific number of votes required to establish or block
consensus. In some circumstances a single implementor's or user's concerns may,
at the chair's discretion, block consensus. That being said, it is critical that
all participants believe the consensus process works! The chair must strive for
consensus on consensus.

Lack of consensus doesn't necessarily prevent an idea from being revisited
later. "More information requested" or "request more work" are acceptable
outcomes for lack of consensus.

In some cases where consensus seems to obviously have been reached, the chair
may poll a lighter-weight request for objections to unanimous consensus. A
single objection is sufficient to force the above consensus process.

[^phase-1-exception]: Consensus votes to move a proposal to phase 1 are exempt
from the 24-hour requirement.

## Decision process

As per the [Community Group charter](https://webassembly.github.io/cg-charter/):

    This Group will seek to make decisions where there is consensus. Groups are
    free to decide how to make decisions (e.g. Participants who have earned
    Committer status for a history of useful contributions assess consensus, or
    the Chair assesses consensus, or where consensus isn't clear there is a Call
    for Consensus [CfC] to allow multi-day online feedback for a proposed course
    of action). It is expected that participants can earn Committer status
    through a history of valuable contributions as is common in open source
    projects. After discussion and due consideration of different opinions, a
    decision should be publicly recorded (where GitHub is used as the resolution
    of an Issue).

    If substantial disagreement remains (e.g. the Group is divided) and the
    Group needs to decide an Issue in order to continue to make progress, the
    Committers will choose an alternative that had substantial support (with a
    vote of Committers if necessary). Individuals who disagree with the choice
    are strongly encouraged to take ownership of their objection by taking
    ownership of an alternative fork. This is explicitly allowed (and preferred
    to blocking progress) with a goal of letting implementation experience
    inform which spec is ultimately chosen by the Group to move ahead with.

    Any decisions reached at any meeting are tentative and should be recorded in
    a GitHub Issue for Groups that use GitHub and otherwise on the Group's
    public mail list. Any Group participant may object to a decision reached at
    an online or in-person meeting within 7 days of publication of the decision
    provided that they include clear technical reasons for their objection. The
    Chairs will facilitate discussion to try to resolve the objection according
    to the decision process.

    It is the Chairs' responsibility to ensure that the decision process is
    fair, respects the consensus of the CG, and does not unreasonably favour or
    discriminate against any Group participant or their employer.
