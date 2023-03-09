# Overview
GitHub is the primary location for the development of WebAssembly, along with
the Community Group meetings. The CG has a GitHub
[organization](https://github.com/WebAssembly) which any CG member can join.
Several different types of repositories are hosted there. Examples
(non-exhaustive) include:

- [spec](https://github.com/WebAssembly/spec): WebAssembly specification documents, reference interpreter, and test suite.
- [design](https://github.com/WebAssembly/design): Design documents and general design discussion
- [meetings](https://github.com/WebAssembly/meetings): WebAssembly meetings (VC or in-person), agendas, and notes
- [proposals](https://github.com/WebAssembly/proposals): A tracking list of WebAssembly proposals
- [website](https://github.com/WebAssembly/website): The sources of [webassembly.org](https://webassembly.org)
- [tool-conventions](https://github.com/WebAssembly/tool-conventions): Documents for conventions supporting interoperability between tools working with WebAssembly.
- A repository for each proposal. For general spec proposals, these are forks of the spec repository with the proposed changes applied. 
  WASI API proposals have a separate [template](https://github.com/WebAssembly/wasi-proposal-template). For example:
    - [gc](https://github.com/WebAssembly/gc): Integration with host garbage collection facilities
    - [memory64](https://github.com/WebAssembly/memory64): 64-bit memory support
    - [js-promise-integration](https://github.com/WebAssembly/js-promise-integration): Integration with JavaScript promises
    - And many others (see the proposals repo for a full list)
- A few repositories with shared code projects
    - [binaryen](https://github.com/WebAssembly/binaryen): Optimizer and toolchain library
    - [wabt](https://github.com/WebAssembly/wabt): Low-level wasm binary toolkit
    - [wasi-libc](https://github.com/WebAssembly/wasi-libc): C library implementation on WASI
    - And a few other projects and test suites
  
# Administration
The GitHub organization is managed by the CG and subject to the same
decision-making processes as proposals or other CG activity.  It has several
organization owners (for redundancy and to cover several time zones): these are
usually the CG/WG chairs and spec editor.

Any CG member can be a Member of the organization. Being a member allows you to
be selected as a reviewer for PRs, easily @-mentioned in discussions, and a few
other practical conveniences, but otherwise doesn't confer any special
permissions or status.  Members will be added on request (contact
webassemly-cg-chair@chromium.org).

Repository ownership and committer status are determined for each repo
individually, depending on the nature of the repo.  Proposal repos are owned by
the proposal champions; the spec repo is owned by the spec editor; the meetings
repo by the CG and subgroup chairs; software projects by their respective
maintainers; other repos default to the CG chairs.  Commit permissions on
repositories can be given by the owner to any CG member based on a history of
contributions and/or expectation of future contributions. Again, this is a
practical consideration and not a special designation for decision-making
purposes.  Contributors may have permissions revoked (e.g. if they are inactive
for a long period of time) as a matter of routine security practice, but can be
restored as needed.
