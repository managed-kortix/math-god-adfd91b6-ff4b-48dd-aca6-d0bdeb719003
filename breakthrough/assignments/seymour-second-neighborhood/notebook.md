# Seymour second neighborhood — worker notebook

The frozen contract is `prompt.md`. Record dated research updates below without
editing the contract. Distinguish theorem, conjectural lemma, computation,
negative result, and unverified observation. Link every experiment to exact
commands, artifacts, and commits.

## Status

- Assignment frozen: 2026-07-25
- Worker session: `e973f064-cda3-4154-b6cc-1df9e400b99f`
- Result status: no claim
- Announcement status: prohibited until every publication gate passes

## Literature ledger

Populate before relying on prior results.

## Attempt ledger

For each route record: hypothesis, exact method, output, breaker result, reusable
compression, and next decision.

## Audit ledger

No audits yet.

## 2026-07-25 — tick 1

- **Control state:** accepted exclusive ownership; status changed from `ready`
  to `running`.
- **Immediate frontier:** establish two exact neighborhood implementations and
  an exhaustive small-order differential oracle, while independent agents audit
  current structural reductions, construction families, literature, and model
  failure modes.
- **Queued falsifiable target:** determine the strongest sound constraints on a
  vertex-minimal counterexample that can be added to a direct exact model,
  emphasizing the minimum-outdegree-8 layer signature funnel.

### Exact experiment result

- Added independent Python/set and Node.js/Boolean-matrix certificate verifiers,
  strict parsers, hostile fixtures, and exhaustive ternary oriented-graph
  generation in `experiments/`.
- Commands passed:
  `python3 test_verifiers.py` and
  `python3 exhaustive_crosscheck.py --max-n 5`.
- Exact census: `1+3+27+729+59049=59809` labelled oriented graphs; both
  implementations agreed on every `N1` and `N2` set; zero counterexamples.
- **Classification:** regression/oracle validation only, explicitly not a
  finite-order solution.

### Structural compression

- Independent reports are preserved in `agents/tick1-*.md`.
- Without minimality, a degree-eight obstruction reduces to ten
  `(|B|,|A1|,r)` branches listed in `agents/tick1-literature.md`.
- Choosing a counterexample first vertex-minimal and then arc-minimal gives a
  stronger root result: `|B| in {6,7}`. Arc deletion shows every vertex deficit
  is 1 or 2 and yields exact restrictions on singleton predecessor signatures;
  see `agents/tick1-structure.md`.
- The signature projection remains feasible, so it is not a contradiction.
  This is a useful hostile failure: the next model must include witness badness
  and completion, not merely root row-degree constraints.
- Cayley orientations, their positive independent blow-ups, and complete cyclic
  substitutions cannot produce a counterexample; exact formulas are recorded
  in `agents/tick1-constructions.md`.

### Audit status and next attack

- No solution claim. No announcement permitted.
- **Next falsifiable lemma:** in the arc-minimal degree-eight case, extend the
  root predecessor signatures to exact badness constraints for `A`, beginning
  with `|B|=6`; either prove the finite signature system infeasible or emit its
  smallest exact feasible signature and identify the first missing global
  completion condition.
- **Queued implementation:** build an enumerator/CP-SAT-independent finite
  search for `(H,{P_b})` satisfying the proved root constraints, canonicalize
  under permutations of `A` and `B`, and use feasible points as adversarial
  inputs before adding any boundary multiplicity assumption.

## 2026-07-25 — tick 2

### Hostile repair

- A hostile agent challenged the tick-1 arc-deletion proof. Non-tail exact
  second neighborhoods can change after deleting `x->y`, but only by losing
  `y`; first neighborhoods are unchanged. Hence no non-tail bad vertex can
  become Seymour, and the tail must become Seymour. The deficit-1-or-2 and
  `|B| in {6,7}` conclusions survive with this missing monotonicity argument
  inserted. See `agents/tick2-hostile-structure-audit.md` and the clarification
  in `agents/tick1-structure.md`.

### New finite projection

- For the `|B|=6` branch, derived exact formulas for all first and second
  neighborhoods of `A` in terms of arcs on `A union B`, boundary arcs, and 63
  nonempty predecessor-signature multiplicities.
- Every relevant exterior multiplicity has the proved bound `0<=m_S<=12`; no
  speculative trimming or completion bound is needed. Boundary minimum
  outdegree is also exact in these variables.
- The resulting finite system captures all `A`-badness and boundary outdegree,
  but not yet `B`-badness or vertices with empty boundary predecessor signature.
  It is therefore a forward-sound local projection, not a counterexample model.
  Full details: `attempts/tick2-b6-finite-model.md`.
- The smallest simple partial obstruction has `A=Z_8` with arcs of differences
  1 and 2 and all arcs from `A` to six `B` vertices. Every `A` vertex is bad,
  but every `B` vertex has outdegree zero. This is retained as a breaker fixture.

### Literature correction

- A hostile read of arXiv:2501.00614v14 found an unsupported degree inference
  at Lemma 2.2, a five-vertex counterexample to the stated partition in Lemma
  3.1, and circular/arithmetic errors in Theorem 3.2. It does not establish SNC;
  see `agents/tick2-claimed-proof-audit.md`.

### Next queued attack

- Encode the finite `|B|=6` system (equations (1)--(4) in the attempt report)
  using an independently checkable backtracking or SAT model. First seek an
  exact boundary-feasible local obstruction. If one exists, add exact
  `B`-badness signatures; if none exists, extract a checkable UNSAT certificate
  or human inequality. No local UNSAT result will be called a solution without
  the proved universal reduction and all remaining branches.
