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

Each problem's folder holds the **complete search** — not just the result, but
every attempt, every reasoning path, every dead end. Nothing is thrown away.

```
<problem>/
  prompt.md              the attack prompt — statement, what counts as a
                         solution, what does not, the traps, the search plan
  plan.md, notebook.md   live plan + numbered experiments (every step, dated)
  paper.tex, paper.pdf   the proof / construction, in full, and compiled
  numerical_verifier.py  self-contained: re-checks every step, fails on any error
  experiments/           scripts, exact certificates, and data/ (raw search output)
  attempts/              one file per approach tried — the idea, and why it lived or died
  agents/                raw subagent reports + reasoning paths, timestamped
  scratch/               working notes and mid-thoughts
  lean/                  Lean formalization (where done)
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

## Current octacyclic result

`all-octacyclic-cacti/paper.tex` proves the strict AKMPZ conclusion
`s+(G) > |V(G)|` for every connected octacyclic cactus. Its reproducibility
appendix distinguishes mathematical realization lemmas from finite scripts:

- the census programs enumerate colored cluster partitions or incidence trees
  and evaluate encoded exact packet ledgers;
- the L1--L16 scripts reproduce the strict-last-bridge `877=861+16` census and
  check the stated finite ownership data;
- the U1--U6 verifier imports only the fully shared census's finite generation
  and SAFE-classification utilities, then checks signatures, router
  refinements, retained packets, cut ownership, and exact symbolic ledgers;
- no script is claimed to prove the analytic packet inequalities, arbitrary
  connector realization, coincident-entry interval lemma, or attached-tree
  scope; those arguments are in the manuscript.

Exact commands and expected totals are documented in
`all-octacyclic-cacti/README.md`. Build the PDF with
`bash scripts/build-paper.sh all-octacyclic-cacti`.

## Built on Kortix

math-god runs on [Kortix](https://kortix.com) with persistent memory,
heartbeats, and subagent swarms. The repository now has three isolated lanes:
the main trajectory, the six-problem Millennium program, and a two-agent
breakthrough-maxing lane. In the last lane a selector freezes one
certificate-shaped problem and launches a separate never-stop Kortix session
that works on that problem—and nothing else—until resolution or a formal
retirement review.
