# math-god

A Kortix agent that runs 24/7 doing real mathematics research. One open
problem at a time, attacked relentlessly with a full computational harness
(sympy, PARI/GP, Wolfram Alpha, Lean). Posts to X only on genuine,
certificate-backed progress — in deadpan lowercase.

## How it never stops

- **continuation plugin** (`.kortix/opencode/continuation/`): re-prompts the
  agent whenever it goes idle with unfinished todos; doctrine keeps the todo
  list perpetually non-empty.
- **math-heartbeat cron** (every 30 min, `session_mode: reuse`): re-prompts
  the same session; if the session died, the platform resurrects a fresh one
  which resumes from the repo-committed state.

## Where the truth lives

- Doctrine: `.kortix/opencode/skills/math-god-operator/SKILL.md`
- Agent: `.kortix/opencode/agents/math-god.md`
- State: `.kortix/memory/` (ledger, problem queue, lab notebooks, tweet ledger)
- Harness bootstrap: `scripts/setup-harness.sh`

Model: `kortix/codex/gpt-5.6-sol` at xhigh reasoning effort (gateway routing
setting), Fable 5 in the fallback chain.
