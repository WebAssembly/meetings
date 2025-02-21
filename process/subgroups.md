# Subgroups

Subgroups of the CG are created when one (or both) of the following apply:

- An area of interest that needs a lot of discussion. Creating a subgroup with regular meetings provides more bandwidth for this discussion.
- An area of interest is only relevant to a small group of participants. In these cases, subgroup meetings give a more focused venue. This way, participants don’t have concerns about wasting the CG’s time with something that the rest of the CG is not engaged in.

To create a subgroup, you should add a poll to a CG meeting agenda with at least 7 days notice. As part of the poll, you should provide information about:
 - The proposed scope, and deliverables of the subgroup.
 - Chairs, or co-chairs of the subgroup.
 - Information on how to join, and contribute to the subgroup.

## Current Subgroups

| Subgroup  | Chair(s)  | Discussion Repo  | Meetings  |
|---|---|---|---|
| Benchmarking | Petr Penzin (@ppenzin), Saúl Cabrera (@saulecabrera)  | [Repo](https://github.com/WebAssembly/benchmarks)  | [Agendas](https://github.com/WebAssembly/meetings/tree/main/benchmarking)  |
| Debugging  | Derek Schuff (@dschuff)  | [Repo](https://github.com/WebAssembly/debugging)  | no meetings currently scheduled, but discussion or agenda suggestions are welcome |
| GC  | Thomas Lively (@tlively)  | [Repo](https://github.com/WebAssembly/gc)  | [Agendas](https://github.com/WebAssembly/meetings/tree/main/gc)  |
| SIMD  | Petr Penzin (@ppenzin)  | [Flexible Vectors](https://github.com/WebAssembly/flexible-vectors/issues) | [Agendas](https://github.com/WebAssembly/meetings/tree/main/gc)  |
| Stack Switching  | Francis McCabe (@fgmccabe)  | [Repo](https://github.com/WebAssembly/stack-switching)  | [Agendas](https://github.com/WebAssembly/meetings/tree/main/stack)  |
| Threads | Andrew Brown (@abrown), Thomas Lively (@tlively), Conrad Watt (@conrad-watt) | [Repo](https://github.com/webassembly/shared-everything-threads/) | File issues to schedule agenda items |
| WASI  | Bailey Hayes (@ricochet), Yosh Wuyts (@yoshuawuyts)  | [Repo](https://github.com/WebAssembly/WASI)  | [Agendas](https://github.com/WebAssembly/meetings/tree/main/wasi)  |

## Subgroup Leadership Expectations

Subgroups require two kinds of leadership. These roles can be filled by the same person or multiple people:

- Chair(s)—responsible for running the group
- Champion(s)—responsible for driving technical progress on proposals
 
### Chair
A subgroup chair is expected to:

- Organize subgroup meetings:
  - Create agendas in advance so that others can add issues via PRs. These agendas should live in a subgroup-specific folder in the [WebAssembly meetings repo](https://github.com/WebAssembly/meetings). Alternatively, agendas can be organized via issues on a proposal repo for subgroups covering just a single proposal.
  
      Each agenda should have a header that includes meeting details and instructions for how to join. See [this agenda](https://github.com/WebAssembly/meetings/blob/main/wasi/2021/WASI-10-07.md) for an example.
  
      Note: If you use a Google form for registrations, ensure that you turn on email notifications:
      - Go to the "Responses" tab in the editing view
      - Click the "..." menu button in the top pane
      - Turn on "Get email notifications for new responses"

  - Add [new participants](https://www.w3.org/community/webassembly/participants) to the Google calendar event. You should ensure the participant is a CG member before adding them by searching for their name in the participant list. If they are not yet listed, explain that registration is free and that they will need to complete that first.

  - While not required, it can be helpful to work 1:1 with champions to ensure they are identifying topics for discussion at meetings and adding them to the agenda.

- Run subgroup meetings:

  - Ensure notes are taken and posted to the meetings repository within one week post-meeting. Public notes are a requirement of the W3C.

  - Facilitate the discussion and step in when disagreements are getting heated or one person is dominating the conversation in an unproductive way.

  - Identify and drive consensus among participants.

  - Identify action items and make note of commitments.

  - Enforce the CoC (see below).

- Maintain the issue queue:
  - Triage new issues as they come in to ensure that relevant issues are responded to appropriately. In subgroups that span multiple proposals, the chair is responsible for triaging group-wide repos, such as the main discussion repo or shared infrastructure repos, while champions are responsible for triaging their own proposal-specific repos.

  - Facilitate discussion and identify and drive consensus, as in subgroup meetings.

  - Enforce the CoC (see below).

- Maintain the list of active proposals:
  - Check in with champions on a quarterly basis to identify the status of the proposal, including any blockers and submit to the CG chairs.

  - Make appropriate updates to the list of active proposals.

- Enforce the code of conduct within the subgroup:
  - To ensure the safety of the community, we recommend that each subgroup have at least one chair that has completed [Otter Tech’s paid CoC training](https://otter.technology/code-of-conduct-training/) or reviewed the [related documents](https://gitlab.com/otter-tech/coc-incident-response-workshop/-/tree/master). If your organization does not have the funding to pay for this training, contact the CG chairs.
