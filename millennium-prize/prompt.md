# Prompt: what counts as winning the Millennium program

## Exact target

Resolve one or more of the six unsolved problems under the official Clay
Mathematics Institute formulations: Birch--Swinnerton-Dyer, Hodge,
Navier--Stokes existence and smoothness, P versus NP, Riemann hypothesis, and
Yang--Mills existence and mass gap.

## A win

A win is a complete proof or valid counterexample/disproof where the official
formulation permits it, covering every stated quantifier and hypothesis. The
argument must be self-contained modulo explicitly cited established theorems,
must survive independent hostile review, and must be reproducible from the
committed paper and artifacts. Formalization or exact machine certificates are
required for computational steps but do not replace mathematical exposition.

## Not a win

- numerical verification to any finite height, grid, precision, or input size;
- a special case, generic case, averaged theorem, toy model, restricted circuit
  class, altered PDE, finite-volume theory, or stronger-assumption variant;
- a conditional theorem whose condition is open or equivalent to the target;
- a heuristic from physics, random models, machine learning, or experiments;
- a new equivalent formulation without proving either side;
- an argument that silently assumes existence, regularity, compactness,
  effectivity, gauge construction, algebraicity, or uniformity being sought;
- an unverified appeal to a theorem whose hypotheses do not match;
- a promising manuscript before independent reproduction and hostile audit;
- eligibility for or receipt of prize money. Clay decides that under its rules.

## Initial multiagent search

For each target, assign a route builder and an adversarial route breaker. The
builder must return one sharply stated candidate lemma, why it implies a
specific quantified portion of the official problem, and an exact first test.
The breaker must seek counterexamples, circularity, known barriers, and prior
art. A selector then chooses one main funnel using only these concrete outputs.
The other five remain bounded scouts. Repeat recursively at every serious
lemma: proof routes and counterexample routes in parallel, with no public claim
until the entire chain closes.
