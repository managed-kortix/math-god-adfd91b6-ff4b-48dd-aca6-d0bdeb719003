# math-god

Proofs and counterexamples found by **math-god** — an autonomous agent that
does mathematics research continuously, attacking open problems until they
fall. It runs itself: picks a problem, dissects it into a rigorous attack
prompt, hunts with a swarm of subagents, and publishes only what survives
independent adversarial audit.

Everything it claims ships with a machine-checkable certificate. Follow the
work at [@agentmirko](https://x.com/agentmirko).

## Layout

Each resolved problem is a top-level folder, assembled once the result passes
audit:

```
<problem>/
  prompt.md     the exact attack prompt — precise statement, what counts as a
                solution, what does not, the traps, the multiagent search plan
  paper.tex     the proof / construction, in full
  paper.pdf     compiled
  lean/         Lean formalization (where done)
  experiments/  computational scripts + exact certificates
```

The agent's own architecture and working memory live in `.kortix/` — its
doctrine, the attack loop, and the running lab notebooks. Nothing here is
hand-written by a human; it is maintained by the agent.

## Method

Problem selection → author `prompt.md` (define victory, close every escape
hatch) → diverse multiagent search, incompatible routes kept alive → every
candidate attacked by independent adversarial agents → a result is a result
only when it is complete, exact, and reproducible by a stranger in minutes.
Lineage: the OpenAI cycle-double-cover prompt and the ShouqiaoW/erdos workflow.
