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

## 2026-07-25 — tick 3

- Proved that universal incidence `A->B` cannot occur in the `|B|=6` branch;
  see `attempts/tick3-universal-incidence-nogo.md`. Any viable obstruction must
  use non-universal predecessor signatures and some reverse `B->A` arcs.
- Derived a Hall expansion theorem for the six root predecessor signatures and
  exact transport bounds `M>=E_BR>=P-21>=15`. Sharp examples show aggregate
  transport alone cannot contradict badness; overlap structure inside
  `X_A,X_B` is the next human target. See `attempts/tick3-b6-transport.md`.
- Extended the finite signature framework through exact `B`-badness. Local
  iteration has no proved depth bound, but Seacrest's `n<=36` reduction makes a
  complete finite direct model valid for a globally vertex-minimal degree-eight
  counterexample. See `attempts/tick3-b-badness.md`.
- Added `experiments/direct_smt.py`, an exact Z3 adjacency model with the rooted
  six/seven-vertex second layer and deficit exactly one or two at every vertex.
  Orders `n<=16` are rigorously impossible already by edge capacity
  `C(n,2)<8n`. The initial baseline searches at `n=17` for both root branches
  timed out after 600 seconds, but a subsequent exact argument eliminates that
  order: minimum outdegree eight forces all 136 possible arcs and every
  outdegree to equal eight, hence a regular tournament. For any `x->v`, if no
  `v->y->x` existed then `x` would dominate `v` and all eight outneighbors of
  `v`, contradicting `d+(x)=8`; thus every in-neighbor of `v` is in `N++(v)`
  and every vertex has `d++=d+=8`. The direct script now records this presolve.
- **Next queued attack:** encode the proved Hall/root-signature constraints and
  staged rooted symmetry into the direct model, then seek a model at `n=17`
  while independently deriving overlap lower bounds for `L-e`. Any SAT graph
  must pass both external verifiers; any UNSAT status needs a certificate.

## 2026-07-25 — tick 4

- Derived the exact near-tournament budget `X+m=9` at order 18 and a sharper
  root remainder identity forcing two or three vertices outside
  `{s} union N+(s) union N++(s)`. The deficit-two branch has only three units of
  residual arc/excess/missing-pair budget; see `attempts/tick4-order18.md`.
- Strengthened `direct_smt.py` with the universal outdegree upper bound,
  exact deficits, root layer implications, degree-18 missing-pair branching,
  and proved root signature constraints. Experimental results: both root
  branches are Z3-UNSAT at zero missing pairs; the six-vertex second-layer
  branch is also Z3-UNSAT at one and two missing pairs. These are not yet
  independently certified and carry no theorem status. The seven-vertex branch
  timed out at one and two missing pairs.
- A breaker destroyed naive lower bounds on internal transport: one reversed
  `A-B` pair can satisfy all root/Hall constraints with `L-e=-10` due to exact
  second-neighborhood overlap. Preserved in `attempts/tick4-overlap-breaker.md`.
- **Next queued attack:** translate the order-18 exact budget (2) into the SMT
  model, add arc-deletion minimality constraints, and rerun each missing-pair
  shard. In parallel, derive a human contradiction for the zero-missing-pair
  tournament branch so solver UNSAT is replaced by proof.

## 2026-07-25 — tick 5

- Near-tournament literature eliminates all oriented graphs with at most two
  missing pairs. A hostile audit found flaws in a proposed shortcut proof, so
  the theorem is recorded with Fidler--Yuster/Ghazal provenance; see
  `agents/tick5-near-tournament.md`.
- Independently eliminated the order-18, `|B|=7`, `m=1` shard by a short
  arc-minimality argument and reduced `m=2` to two templates. The known theorem
  supersedes those templates; see `attempts/tick5-n18-b7.md`.
- Hostile-audited the triangular `n<=36` reduction. The cited paper's printed
  set-distance convention has a gap; a corrected proof using external set
  neighborhoods and asymmetric prefixes is valid. See
  `agents/tick5-order-bound-audit.md`.
- Added exact necessary arc-minimality constraints and tight vertex-deletion
  witness relaxations to `direct_smt.py`. The `n=18,|B|=6,m=3` minimal shard
  returned provisional Z3-UNSAT; this is not a proof certificate.
- **Next queued attack:** focus order 18 on `m=3,...,9`, encode exact B6/B7
  remainder budgets, and begin a deterministic CNF/LRAT pipeline so any
  computational elimination is independently checkable.
