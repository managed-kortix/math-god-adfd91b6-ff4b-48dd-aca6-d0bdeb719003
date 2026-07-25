# breakthrough state — isolated single-problem lane

Read this first in every `breakthrough-selector` and `breakthrough-god` session.
This file is the control-plane handoff between the selector and exactly one
independent worker. It does not belong to `STATE.md` or `MILLENNIUM_STATE.md`.

- **status:** ready
- **active assignment:** `breakthrough/assignments/seymour-second-neighborhood/prompt.md`
- **worker session id:** none
- **selected by:** `breakthrough-selector` session `a9b4115e-c21f-4ee6-8a73-3f5501419e3c`
- **selection date:** 2026-07-25
- **last health check:** 2026-07-25; no `breakthrough-god` session present in `kortix sessions status --all --json`
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

Push the frozen assignment, launch exactly one worker pinned to
`breakthrough-god`, and replace `worker session id: none` with the returned id
while changing `status` to `running`.
