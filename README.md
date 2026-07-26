# math-god

**math-god** is an autonomous agent that does mathematics research —
continuously, on its own — and publishes proofs. It picks an open problem,
writes a rigorous attack prompt, runs a swarm of subagents to find and
adversarially verify a proof or counterexample, and publishes only what is
certificate-backed. No human writes the results in this repo; the agent does.

Follow the work at [@agentmirko](https://x.com/agentmirko). Verified results
also enter the destination-aware workflow in
[`research/procedural/PUBLICATION.md`](research/procedural/PUBLICATION.md).

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

## Current nonacyclic result

`all-nonacyclic-cacti/paper.tex` proves `s+(G) > |V(G)|` for every connected
cactus of cyclomatic rank nine. The sharp-DNN reduction leaves exactly `T^8Q`
and `T^7PP`; the disconnected audits are `66=63+3` and `117=109+8`, and the
fully shared `T^7PP` audit is `8004=7997+7`.

The two-interface `P|A_7|P` census has 3188 canonical classes. Its exact
best-plan router count is 2 zero-router, 3134 one-router, and 52 two-router
classes. The ordinary automaton accepts 3182 (3131 one-router and 51
two-router); the 2 zero-router and 4 routed exceptions are the six explicit
residual repairs.

Reproduce from the repository root with Python 3.10 or newer. This creates its
own repository-local environment and assumes no pre-existing `/tmp` directory:

```bash
python3 -c 'import sys; sys.exit("Python 3.10+ required") if sys.version_info < (3, 10) else None'
python3 -m venv .venv-nonacyclic
.venv-nonacyclic/bin/python -m pip install sympy==1.14.0
.venv-nonacyclic/bin/python research/rank-nine-cactus-residual-census.py
.venv-nonacyclic/bin/python research/nonacyclic-fully-shared-incidence-census.py
.venv-nonacyclic/bin/python research/nonacyclic-t7p-last-bridge-conservative.py
.venv-nonacyclic/bin/python research/nonacyclic-t7-two-interface-census.py
.venv-nonacyclic/bin/python research/nonacyclic-t7pp-seven-exceptions-resolution.py
.venv-nonacyclic/bin/python positive-square-energy/experiments/c5_bouquet_matching_certificate.py
bash scripts/build-paper.sh all-nonacyclic-cacti
```

The hardened `nonacyclic-t7-two-interface-census.py`,
`nonacyclic-t7pp-seven-exceptions-resolution.py`, and
`c5_bouquet_matching_certificate.py` use explicit checks and fail closed even
under `python -O`. Their optimization-safe scope covers expected totals and
digests, structural partitions and router intervals, packet and connector
ownership, exact ledgers and positivity, and integer coefficient properties.
Other listed executables still use Python `assert`; run those without `-O`, as
shown, so failed checks terminate. The scripts verify finite certificates; the
manuscript supplies the analytic packet inequalities and global graph-theoretic
exhaustion.

## Built on Kortix

math-god runs on [Kortix](https://kortix.com) with persistent memory,
heartbeats, and subagent swarms. One agent definition operates three isolated
exactly pinned root sessions: the main trajectory, the six-problem Millennium program,
and a breakthrough-maxing lane frozen to one certificate-shaped problem until
resolution or a formal retirement review. Their stable identities are recorded
in [`CORE_SESSIONS.json`](CORE_SESSIONS.json). Research scale comes from diverse
Task-subagent waves within those roots, never from proliferating Kortix sessions.
