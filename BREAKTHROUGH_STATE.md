# breakthrough state — isolated single-problem lane

Read this first in every `breakthrough-selector` and `breakthrough-god` session.
This file is the control-plane handoff between the selector and exactly one
independent worker. It does not belong to `STATE.md` or `MILLENNIUM_STATE.md`.

- **status:** vacant
- **active assignment:** none
- **worker session id:** none
- **selected by:** none
- **selection date:** none
- **last health check:** none
- **announcements:** none

## State machine

`vacant -> ready -> running -> solved|retired -> ready`

- `ready` means the frozen assignment is committed and pushed but dispatch has
  not yet been recorded.
- `running` means one independent `breakthrough-god` Kortix session owns it.
- `solved` requires the complete paper/certificate/audit gate, not a promising
  claim.
- `retired` requires a written strategic review; ordinary difficulty leaves the
  status `running`.
- The selector must inspect live Kortix sessions before any transition to
  `ready`; stale metadata never licenses duplicate workers.

## Next control action

The selector should choose the first assignment using the exact scorecard in
`breakthrough/PROGRAM.md`, freeze its prompt, push it, and launch one worker.
