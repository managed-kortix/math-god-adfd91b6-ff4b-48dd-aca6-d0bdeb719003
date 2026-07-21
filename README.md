# math-god

A Kortix agent that runs 24/7 doing real mathematics research. One open
problem at a time, attacked relentlessly with a full computational harness
(sympy, PARI/GP, Wolfram Alpha, Lean). Posts to X only on genuine,
certificate-backed progress — in deadpan lowercase.

## AGI-ready architecture

- **Never stops** — two layers:
  - `never-stop` plugin (`.kortix/opencode/plugins/never-stop.ts`): a root
    session is never allowed to go idle; every idle event re-prompts the agent.
    Kill switch: `KORTIX_NEVER_STOP_DISABLED=1`.
  - `math-heartbeat` cron (30 min, `session_mode: reuse`): re-prompts the same
    session; resurrects a fresh one from repo state if it died.
- **Memory OS** (`.kortix/memory/`, all committed — only pushed state
  survives):
  - `state.md` — working memory, read first every tick
  - `goals.md` — goal tree (G-n human-owned, O-n agent-derived)
  - `problems.md` — problem queue: current (exactly one) / backlog / archive
  - `lab/<slug>/` — attack plan, notebook, scripts, certificates
  - `episodic/` — append-only per-day event logs
  - `semantic/` — distilled knowledge notes (tagged, grep-retrieved)
  - `procedural/` — evolving playbooks
  - `tweet-ledger.md` — append-only post log
  - CRUD + retrieval + daily/weekly consolidation rules in the skill.
- **Task planning**: goals → problem queue → attack plan → native todos
  (3+ queued at all times).

## Where the truth lives

- Doctrine: `.kortix/opencode/skills/math-god-operator/SKILL.md`
- Agent: `.kortix/opencode/agents/math-god.md`
- Harness bootstrap: `scripts/setup-harness.sh`

Model: `kortix/codex/gpt-5.6-sol` at max reasoning effort (gateway routing),
fallback claude-opus-4.8 → glm-5.2.
