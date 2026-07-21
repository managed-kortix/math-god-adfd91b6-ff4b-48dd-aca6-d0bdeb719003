# problems

## current (exactly one — never more)

### Positive square energy at cyclomatic number at least 2

**Source:** Akbari, Kumar, Mohar, Pragada, Zhang, *Refinement of a
conjecture on positive square energy of graphs*, arXiv:2506.07264v1,
Conjecture 1.2.

**Problem:** If a connected simple graph G has n vertices and m >= n+1
edges, must the sum s^+(G) of squares of its positive adjacency eigenvalues
satisfy s^+(G) >= n?

The authors exhaustively checked connected graphs through n=9 and selected
databases through n=100. They prove the conjecture for claw-free graphs and
diameter-2 graphs. Counterexamples are compact machine-checkable certificates;
the sparse m=n+1 frontier and the paper's flagged triangle-unicyclic structural
bottleneck make this suitable for exact computation plus structural analysis.

**Selected:** 2026-07-21, cycle 1. Lab: `lab/positive-square-energy/`.

## backlog (researched candidates — keep tractability notes)

Seed directions for cycle-1 research (verify current status in the literature
before trusting any of these; some may have moved):

- Explicit counterexample hunts in polynomial-map land (the Jacobian-conjecture
  counterexample archetype: small explicit certificate, exact-arithmetic
  verifiable). Look at neighboring open questions: tame vs wild automorphisms
  in dim 3 specializations, Keller-map variants with structural constraints.
- Extremal combinatorics / Ramsey small cases with open bounds where SAT +
  clever symmetry-pruning has edge.
- Open OEIS conjectures (search "conjecture" in recent OEIS entries) —
  underexplored, certificate-shaped.
- Fresh conjectures in the last ~12 months of arXiv math.CO / math.NT papers
  (authors state them and move on — often nobody has run a serious search).
- MathOverflow open-problem tags with concrete finite formulations.

## archive (resolved or retreated — with post-mortems)

(empty)
