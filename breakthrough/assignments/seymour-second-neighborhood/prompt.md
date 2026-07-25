# Frozen assignment: Seymour's Second Neighborhood Conjecture

## Exclusive ownership and operating rule

Own only this problem. Do not resurvey the problem portfolio and do not switch
targets. Continue the autonomous proof/counterexample loop indefinitely. Every
failed computation or argument must be compressed into a reusable obstruction,
lemma, reduced model, or documented no-go result before the next route begins.
An unchanged larger brute-force run is not progress.

The assignment is frozen by the selector. Research updates belong in
`notebook.md`; code and certificates belong in `experiments/`; individual route
reports belong in `attempts/`; same-target subagent reports belong in `agents/`.

## Exact sourced statement and open-status gate

All graphs below are finite. An **oriented graph** is a directed simple graph
with no loop and with at most one of `u -> v` and `v -> u` for each distinct
pair. For a vertex `v` in an oriented graph `D`, define

```
N+(v)  = {u : (v,u) is an arc},
N++(v) = {z not in N+(v) union {v} : (v,y) and (y,z) are arcs for some y}.
```

Thus `N++(v)` is the set at directed distance exactly two, not the set of all
endpoints of length-two walks.

> **Conjecture (Seymour).** For every finite oriented graph `D`, there exists a
> vertex `v` in `V(D)` such that `|N++(v)| >= |N+(v)|`.

Exact quantifiers:

```
forall finite D [D is oriented => exists v in V(D): d++_D(v) >= d+_D(v)].
```

Primary-source status checks at assignment freeze time:

1. Bai--Li--Park, *Towards a strengthening of the second neighborhood
   conjecture*, arXiv:2607.18047v1 (20 July 2026), Conjecture 1.1 and its
   abstract/introduction explicitly say the conjecture remains open for general
   oriented graphs:
   <https://arxiv.org/abs/2607.18047v1> and
   <https://arxiv.org/html/2607.18047v1>.
2. Sadhukhan--Sandeep--Sen, *A proof of Seymour's second neighborhood
   conjecture for oriented graphs with minimum out-degree equal to 7*,
   arXiv:2606.30588v1 (29 June 2026), Theorem 1.1 proves the conjecture when
   `delta+(D) <= 7` and describes the general conjecture as largely open:
   <https://arxiv.org/abs/2606.30588v1> and
   <https://arxiv.org/html/2606.30588v1>.
3. Huang--Peng, *An improved bound on Seymour's second neighborhood
   conjecture*, arXiv:2412.20234v1, Conjecture 1.1 and Theorem 1.3. It proves the
   general factor `gamma = 0.715538...`, with `gamma` the unique root in `[0,1]`
   of `8x^5+4x^4-12x^3-7x^2+2x+4`, and says the factor-1 conjecture remains
   open: <https://arxiv.org/abs/2412.20234v1> and
   <https://arxiv.org/html/2412.20234v1>.

Before claiming a result, repeat the literature search across arXiv, journal
databases, authors' pages/repositories, and citing papers. Resolve the apparent
chronology and scope of all newer 2026 papers. Read the full proofs and
artifacts most relevant to the claimed route; abstracts are not a literature
gate.

## Why this target won the selector scorecard

The frozen shortlist (scores are 1--5 in the order: significance, certificate
compactness, structural leverage, exact verifiability, workflow transfer,
decisive-obstruction probability) was:

| candidate | scores | total | selector decision |
|---|---:|---:|---|
| Seymour second neighborhood | 5,5,5,5,5,4 | 29 | winner: a disproof is one small oriented graph and recent exact local-model methods transfer directly |
| Caccetta--Haggkvist, triangle case | 5,5,4,5,4,3 | 26 | excellent certificate, but a counterexample must cross an exceptionally mature extremal barrier |
| `3 x 3` matrix multiplication rank at most 22 | 5,4,4,5,3,2 | 23 | exact identity, but continuous/algebraic search and equivalence auditing are substantially harder |
| Rota basis conjecture, small `n` | 4,4,3,4,3,2 | 20 | small cases risk being only restricted-model progress rather than resolution of the universal conjecture |

Do not revisit this selection.

## What constitutes a win

Exactly one of the following:

### A. Counterexample win

A finite explicit oriented graph `D` such that, for **every** vertex `v`,

```
|N++(v)| < |N+(v)|.
```

The deliverable must include a canonical vertex-labelled arc list, a checksum,
the complete per-vertex first- and second-neighborhood table, two independent
exact verifiers, and an independently reproduced hostile audit. Prefer the
smallest graph found, but minimality is not required to disprove the conjecture.

### B. Proof win

A complete rigorous proof for every finite oriented graph, including all
reductions from an arbitrary counterexample to the terminal contradiction.
Computer assistance is allowed only when the finite reduction is proved sound
and complete and the terminal check emits independently checkable proof
artifacts (or is small enough for a second transparent exhaustive verifier).

## Important non-wins and overclaim traps

None of the following solves the assignment:

- verifying the conjecture through any finite order;
- proving it for tournaments, planar graphs, bounded minimum out-degree,
  bounded anti-transitivity, random graphs, regular graphs, strongly connected
  graphs, or another restricted class;
- finding a vertex with `|N++(v)| >= c|N+(v)|` for any `c < 1`;
- proving the newer **strong Seymour vertex** conjecture only in a restricted
  class, or confusing that strengthening with the assigned statement;
- an unoriented digraph, a graph with a digon/loop, or use of walk endpoints
  rather than directed-distance-exactly-two vertices;
- a SAT/CP-SAT `SAT` report without a decoded graph and direct verifier, or an
  `UNSAT` report without a sound universal reduction and checkable certificate;
- a floating-point, randomized, heuristic, or solver-version-dependent check;
- a local obstruction whose completion to a finite oriented graph is unproved;
- a proof relying on an unproved structural assertion, hidden exhaustive case
  split, or unavailable proprietary artifact;
- novelty, a stronger bound, a useful lemma, or a new computational record.

Treat every promising claim as false until the hostile audit survives.

## Reproducible counterexample verifier specification

Use a plain text certificate with first line `n`, followed by sorted distinct
integer pairs `u v`, `0 <= u,v < n`, denoting arcs. Reject malformed input.
Verifier 1 must:

1. require `n >= 1`, `u != v`, no duplicate arc, and never both `(u,v)` and
   `(v,u)`;
2. for each `v`, compute `N1[v]` directly from the arc set;
3. compute `R2[v] = union_{y in N1[v]} N1[y]` and then
   `N2[v] = R2[v] \ (N1[v] union {v})`;
4. require `len(N2[v]) < len(N1[v])` for every `v`;
5. print deterministic sorted `N1`, sorted `N2`, cardinalities, margins
   `d+(v)-d++(v)`, SHA-256 of normalized input, and PASS/FAIL;
6. exit nonzero on malformed input or failure.

Verifier 2 must be independently implemented (different language or independent
bitset/matrix formulation): Boolean adjacency matrix `A`; first neighborhood is
row support; length-two reachability is Boolean support of `A^2`; remove the
row support and diagonal; check every strict inequality. Cross-check every set,
not merely the final Boolean. Include tiny positive and negative unit tests that
catch the exact-distance, digon, loop, duplicate, and universal-quantifier bugs.

For proof artifacts, specify an equally explicit checker contract before using
the artifact. Pin tool versions and commands, log seeds and resource limits, and
make every experiment resumable.

## Required literature and artifact gates

1. Build an annotated bibliography starting from all three primary sources
   above, Espuny Díaz--Girão--Granet--Kronenberg (arXiv:2403.02842), and the
   cited foundational reductions. Record exact hypotheses and reusable lemmas.
2. Pull and reproduce the public CP-SAT artifacts associated with
   arXiv:2606.30588 (`rbsandeep/Seymour-Vertex-delta7`) before extending them.
   Audit model soundness rather than trusting solver status.
3. Search specifically for claimed counterexamples, order lower bounds,
   vertex-minimal/edge-minimal counterexample structure, regular/tight
   orientations, and post-publication corrections.
4. Maintain a claim-to-source table with theorem numbers and scope. A missing
   source blocks a novelty or priority claim, not experimentation.

## Diverse attack routes

Run routes in parallel when useful, but keep all agents on this one conjecture.
Do not let one encoding monoculture dominate.

### Route 1: direct counterexample SAT with exact decoding

Encode each unordered vertex pair as absent/one of two orientations and impose
for every vertex the strict negation `d++ < d+`. Develop independent encodings:
reachability auxiliaries with cardinality networks; bit-vector/SMT; and a
CP-SAT model. Add only proved symmetry breaking. Enumerate by degree sequence,
strong components, and automorphism orbits; independently decode every model.

### Route 2: minimal-counterexample structure into search

Re-derive and audit all valid facts about vertex-minimal and edge-minimal
counterexamples. Translate each proved fact into tested constraints. In
particular exploit the current `delta+ <= 7` theorem, strongly connected
reductions where valid, minimum-outdegree neighborhoods, tight degree margins,
and near-regular/tight orientations. Never import a reduction without checking
its exact minimality notion and direction.

### Route 3: local-layer/signature obstruction models

Extend the successful local setup around a minimum-outdegree root:
`A=N+(s)`, `B=N++(s)`, subsequent layers, and outside predecessor signatures.
Prove a trimming/signature lemma before bounding outside multiplicities. Seek
finite obstruction models for minimum outdegree 8 and upward. Require model
soundness (`genuine obstruction => feasible model`) and machine-checkable UNSAT
or complete enumeration. Compress each eliminated branch into a human lemma.

### Route 4: blow-ups, substitutions, and near-regular constructions

Search structurally generated families: cyclic/circulant orientations,
compositions and substitutions, iterative blow-ups, sparse cycle powers,
near-regular tournaments with deleted arcs, lifts/covers, Cayley orientations,
and strongly connected gluing gadgets. Derive symbolic formulas for `N+` and
`N++` before optimization. Test whether local deficit gadgets can be composed
without creating a Seymour vertex at interfaces.

### Route 5: proof inequalities and weighted potentials

Audit and strengthen Huang--Peng's weighted-minimizer/CSP route toward constant
1. Search for an additional universally valid inequality from third/fourth
layers, edge-minimality, mass transport, or a nonlinear potential. Every
candidate inequality gets a breaker search on small oriented graphs before use.
Use exact rational/SOS/Farkas certificates where possible.

### Route 6: probabilistic and extremal obstruction/no-go analysis

Study why random, dense, and regular families tend to contain Seymour vertices.
Turn this into rigorous forbidden parameter regions for a counterexample rather
than a heuristic. Combine flag-algebra/linear constraints only with exact
rational rounding and a clear path from finite flags to all graph orders.

## Breaker and adversarial routes

- Differentially fuzz all verifier and encoding implementations on exhaustive
  small oriented graphs and randomized graphs.
- Given every proposed proof lemma, ask a dedicated breaker agent to negate it,
  search the smallest countermodel, and inspect boundary/equality cases.
- Given every SAT graph, permute labels, independently recompute with matrix and
  set semantics, minimize arcs/vertices, and check that minimization did not
  change the certificate being claimed.
- Given every UNSAT branch, remove constraints one at a time, generate witnesses
  for satisfiable relaxations, and map every constraint back to a proved lemma.
- Stress hidden assumptions: connected versus strongly connected, exact versus
  at-most distance two, zero-outdegree vertices, missing arcs, loops/digons,
  vertex-minimal versus edge-minimal, and strict versus non-strict inequality.

## First exact experiment and next-lemma funnel

1. Implement the two certificate verifiers and exhaustive labelled generation
   for very small `n`; cross-check all outputs.
2. Reproduce the published `delta+ <= 7` CP-SAT artifacts in a pinned
   environment and write a soundness audit identifying each mathematical
   constraint.
3. Build a baseline direct negated-conjecture SAT model for fixed `n`, with no
   unproved structural constraints. Confirm that it reports no model at the
   exhaustively cross-checked small orders and that planted malformed variants
   trigger expected failures.
4. Funnel the first serious work into one exact next lemma:

   > **Target lemma:** either derive a sound finite signature model eliminating
   > all minimal counterexamples with `delta+(D)=8`, with checkable terminal
   > certificates, or extract the smallest feasible local obstruction and prove
   > precisely which additional global completion condition it lacks.

This lemma is not itself a solution; it is the first structural compression
step. If it fails, preserve the smallest obstruction and use it to redesign the
next route rather than merely increasing solver limits.

## Mandatory hostile audit and publication gates

No result may be marked solved until all gates pass:

1. a complete top-level paper states the exact theorem, definitions, proof, and
   role of computation;
2. a clean PDF builds from repository sources;
3. all code, certificate files, normalized inputs, checksums, commands,
   environments, and raw logs are committed;
4. at least two independent same-target agents perform hostile proof audits,
   and at least one independent verifier reproduces the certificate from a
   clean checkout;
5. every audit objection is answered in writing or the claim is withdrawn;
6. a fresh literature/novelty search checks work through the claim date and
   distinguishes priority from correctness;
7. the final commit is pushed and its hash recorded;
8. only after all above gates may `BREAKTHROUGH_STATE.md` become `solved`, and
   only then may a simple result post be drafted. Never announce from a search
   log or provisional solver output.

If no complete win is reached, remain `running`. Retirement requires a written
falsification/no-go review; ordinary difficulty is not retirement.
