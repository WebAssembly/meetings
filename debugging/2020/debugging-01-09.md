# Agenda for the January 9 video call of WebAssembly's debugging subgroup

- **Where**: zoom.us
- **When**: January 9, 11am-12pm Pacific Standard Time (January 9, 7pm-8pm UTC, 8pm-9pm CET)
- **Location**: *link on calendar invite*
- **Contact**:
    - Name: Derek Schuff
    - Email: dschuff@google.com

### Registration

None required if you've attended a wasm CG meeting before. Email Derek Schuff to sign up if it's
your first time. The meeting is open to CG members only.

## Logistics

The meeting will be on a zoom.us video conference.

Installation is required, see the calendar invite.

## Agenda items

1. Opening


## Meeting Notes
### Attendees:

* Barbara Nichols
* Alon Zakai
* Derek Schuff
* Bill Ticehurst
* Paolo Severini
* Yury Delendik
* Philip Pfaffe
* Z Nguyen-Huu

## Notes:

DS: Update on LLVM: with Yury's recently landed patch and https://reviews.llvm.org/D71681, LLVM's upstream output should be
at parity with the out-of-tree patches we've been using (actually better, since the frame base info is correct more often.

AZ: For emscripten, the .debug_line info should be correct with a PR that should land today. There will be a few
follow-ups to handle ranges and a few other places PCs need to be fixed up, but the infrastructure is all there.

BT: the wasm summit and CG meeting are a month away. Should we put something on the agenda?

DS: It's a good idea. I think we had someone raise an issue on that, which I haven't merged yet because I haven't
talked to Ben since he's been back. But we should put something on the agenda. At least an update on debug info.
Maybe the Chrome dev people can say something about what they've been doing too.

PS: there was a recent proposal for UUID/build-id custom section in wasm. That would be useful for
debugging/symbol servers, etc. should we pick that back up?

DS: yes, I think so

BT: there was a good conversation on the github issue, we should probably pick it up again there.

BT: Unrelated question: Is there a text format for DWARF that we use for testing or round-tripping?

PS: Dwarf is only a binary format.

DS: If you use LLVM assembly output in clang, it prints section-switch and numerical directives that represent
the encoded info, but it's still encoded. Otherwise we just use e.g. llvm-dwarfdump for testing but it doesn't round-trip.

