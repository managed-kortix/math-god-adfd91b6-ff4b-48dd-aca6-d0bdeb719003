# Millennium Prize research program

## Purpose

Run a permanent, public, exact research program on the six unsolved Clay
Millennium Prize Problems. Ambition is unlimited; epistemic standards are not
negotiable. The program may produce valuable partial theorems, but only a proof
or disproof meeting the full official statement is a solution.

## Portfolio architecture

- **One main proof funnel:** one named problem, one sharply stated bottleneck,
  and one next exact lemma or counterexample test. Most compute goes here.
- **Five bounded scouts:** each maintains a live map and tests one concrete
  route. Scouts stop broad surveying once they can return an exact lemma,
  obstruction, contradiction, or no-go theorem.
- **Adversarial mirror:** every promising route gets a separate agent tasked
  with breaking assumptions, locating prior art, testing boundary cases, and
  checking that the implication reaches the official statement.
- **Rotation gate:** rotate the main funnel only after a proved checkpoint, a
  decisive falsification, or a written strategic review. Never rotate merely
  because the proof became difficult.

## Required dossiers

Create one subdirectory for each target:

```
millennium-prize/
  birch-swinnerton-dyer/
  hodge/
  navier-stokes/
  p-vs-np/
  riemann-hypothesis/
  yang-mills/
```

Each dossier must contain `statement.md`, `routes.md`, `notebook.md`, and
`audit.md`. `statement.md` quotes or faithfully fixes the official formulation,
its quantifiers, accepted alternatives (proof or counterexample where
applicable), and explicit non-solutions. Every research claim links back to the
quantifier it advances.

## Verification ladder

1. Heuristic exploration may use numerics, but labels them non-rigorous.
2. Candidate claims are rewritten exactly and checked symbolically or in a
   proof assistant whenever feasible.
3. Independent agents reproduce derivations without relying on the author's
   notebook.
4. Counterexample agents attack endpoint cases, regularity assumptions,
   hidden finiteness hypotheses, model restrictions, and circular dependence
   on results equivalent to the target.
5. Literature agents check novelty and theorem hypotheses against primary
   sources.
6. A complete candidate solution receives a standalone top-level paper folder,
   compiled PDF, all certificates, line-by-line hostile audits, and independent
   reproduction before any public claim.

## Resource discipline

Prefer structural attacks and falsifiable lemmas over indefinite brute force.
Checkpoint long computations atomically. Exact arithmetic and formal proof are
mandatory for certificates; floating-point screens only choose candidates.
Keep all durable reasoning in git and coordinate with the main lane via
`git pull --rebase` before every push.
