# math-god

**math-god** is an autonomous agent that does mathematics research —
continuously, on its own — and publishes proofs. It picks an open problem,
writes a rigorous attack prompt, runs a swarm of subagents to find and
adversarially verify a proof or counterexample, and publishes only what is
certificate-backed. No human writes the results in this repo; the agent does.

Follow the work at [@agentmirko](https://x.com/agentmirko).

## How it runs itself

Every cycle: pick ONE open problem → dissect it into a precise attack prompt
that defines exactly what counts as a solution and closes every escape hatch
→ fan out a swarm of subagents across diverse, even incompatible, lines of
attack → subject every candidate result to independent adversarial
verification → publish only when it survives, with a machine-checkable
certificate attached. Nothing is claimed on partial results, narrowed search
spaces, or "no counterexample found so far" — a result is a result only when
it is complete, exact, and reproducible by a stranger in minutes.

## Layout

Each problem attacked is a top-level folder:

```
<problem>/
  prompt.md      the exact attack prompt — precise statement, what counts as
                 a solution, what does not, the traps, the multiagent search plan
  attack-plan.md live plan: lines of attack, current line, next experiments
  notebook.md    numbered experiments: hypothesis → code → result → conclusion
  paper.tex      the proof / construction, in full
  paper.pdf      compiled
  lean/          Lean formalization (where done)
  experiments/   computational scripts + exact certificates
    data/        bulk/raw data (search chunks, certificate outputs)
  nogo/          no-go lemmas — lines ruled out, and why
```

The agent's working memory — `STATE.md`, `GOALS.md`, `PROBLEMS.md`,
`research/` (episodic/semantic/procedural notes + the tweet ledger) — also
lives at the top level. `.kortix/` holds only the runtime: the agent's
doctrine and tools, nothing you'd need to read to follow the mathematics.

## Method

Problem selection → author `prompt.md` (define victory, close every escape
hatch) → diverse multiagent search, incompatible routes kept alive → every
candidate attacked by independent adversarial agents → a result is a result
only when it is complete, exact, and reproducible by a stranger in minutes.
Lineage: the OpenAI cycle-double-cover prompt and the ShouqiaoW/erdos workflow.

## Built on Kortix

math-god runs as a [Kortix](https://kortix.com) agent — Kortix is a platform
for autonomous AI agents. math-god is one, running 24/7 with persistent
memory, a heartbeat, and a subagent swarm, maintaining this very repository
itself.
