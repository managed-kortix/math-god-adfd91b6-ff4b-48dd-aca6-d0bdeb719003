# Three-core research architecture

The autonomous fleet has exactly three persistent `math-god` root sessions.
Their IDs, names, triggers, and state files are authoritative in
`CORE_SESSIONS.json`.

## Continuity contract

- Each heartbeat is pinned to one exact session ID. A heartbeat resumes that
  conversation; it does not create a fresh research thread.
- Main, Millennium, and Breakthrough have immutable state ownership and target
  boundaries.
- Run `python3 scripts/check-core-sessions.py --strict-running` when reconciling
  the fleet. An unregistered running `math-god` root is a policy violation.
- Ordinary human-created sessions may exist transiently, but receive no
  heartbeat or never-stop contract and may not be autonomous research workers.
- A stopped historical session is harmless and is not part of the active fleet.

## Scaling contract

Scale inside a core with the Task tool, not with additional Kortix sessions.
Use parallel waves only for non-overlapping roles or methods. A typical wave may
contain proof construction, counterexample search, exact certification,
literature checking, hostile review, and independent reconstruction. The core
owns synthesis, state updates, Git integration, communication, and publication.

Subagents are intentionally disposable; their durable output must be committed
as notebooks, reports, scripts, or certificates. They cannot contact people,
publish, mutate another lane, or launch root sessions.

## Replacement

Pinned continuity is preferred over automatic replacement. Temporary failure is
not death: inspect status, pending prompts, logs, and restartability first. If a
core is irrecoverable, preserve its branch and follow the atomic replacement
protocol in `CORE_SESSIONS.json`. Never leave both old and replacement roots
autonomously active.
