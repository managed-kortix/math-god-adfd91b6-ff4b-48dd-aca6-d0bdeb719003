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

## 2026-07-25 — tick 6

- Proved a complete human contradiction for the order-18 `|B|=6,m=3` shard.
  Exact budget forces the three remainder vertices to form a directed triangle,
  and deleting a triangle arc has no gain but loses its unique second endpoint,
  contradicting arc minimality. See `attempts/tick6-n18-b6-m3.md`.
- Literature classification extends blanket near-tournament coverage through
  four missing pairs: every three-edge missing graph is matching plus a star;
  every four-edge graph is covered by that theorem except `C4`, handled
  separately. No arbitrary-forest theorem exists in the verified sources, and
  `P6` shows why `m=5` is a new structural threshold. See
  `agents/tick6-missing-classes.md`.
- Consequently all order-18 shards `m<=4` are eliminated. Remaining order-18
  search is exactly `m=5,6,7,8,9` in both root branches.
- **Next queued attack:** classify the possible missing graphs at `m=5` under
  the exact B6/B7 budgets, first trying to force a known missing-graph class;
  in parallel implement the deterministic CNF generator and DRAT checker path
  for residual shapes.

### CNF scout

- Added an initial deterministic plain-CNF generator with exact adjacency,
  two-walk, exact-second, degree, deficit, missing-count, and rooted-layer
  semantics. CaDiCaL scouts on both `m=5` root branches remained `UNKNOWN` after
  900 seconds, confirming that unsharded baseline search is too weak.
- No proof or model was retained from those interrupted runs. The generator is
  provisional until exhaustive semantic mutation tests validate its
  bidirectional counters and every SAT projection is decoded by both graph
  verifiers.
- **Immediate next experiment:** implement the semantic CNF test harness on all
  oriented graphs through order four, then add exact remainder-budget shards
  before further long runs.

## 2026-07-25 — tick 7

- Hostile clause audit found the core CNF semantics sound but identified missing
  parameter validation and an opaque duplicated final strictness literal. Both
  were repaired.
- Added pure exhaustive CNF semantic tests. Exact bidirectional thresholds pass
  every input through width eight; exact two-walk and exact-second clauses pass
  every membership mutation on all 760 labelled oriented graphs through order
  four. Existing independent graph verifiers still pass their 59,809-graph
  order-five differential census.
- Derived complete scalar frontiers for both five-missing-pair root branches.
  In the B6 branch, `P6` reduces to 18 placement rows and 71 local ledgers after
  immediate arc-minimality filters; B7 has exact individual two-vertex remainder
  equations but still broad incidence freedom. See `attempts/tick7-order18-m5.md`.
- **Next queued attack:** implement a canonical `P6`-placement shard generator
  for the 71 B6 ledgers, including full arc-minimal gain/loss constraints. Any
  UNSAT shard must emit and independently verify DRAT/LRAT; any SAT projection
  must pass both graph verifiers.

## 2026-07-25 — ticks 8--10

- Corrected the five-edge classification: there are five uncovered missing
  graph types, not only `P6`. B6 reduces to 170 canonical local ledgers across
  these types; B7 has 21 canonical remainder placements for the four
  disconnected types. See `attempts/tick8-five-edge-census.md`.
- Hostile analysis confirmed that local ledger degree excess is not the same as
  badness deficit; using one as the other would unsoundly eliminate ledgers.
  Full gain/loss constraints require unresolved incidence data.
- Proved the `m=9` perfect-matching branch impossible by uncovered-set double
  counting and contraction. Any residual `m=9` graph must have an isolated
  vertex and compensating missing degree at least two. Derived a robust-witness
  residual around an isolated vertex, but its equality cases survive local
  tests. See `attempts/tick9-high-missing-structure.md`.
- Derived a robust deletion-witness normal form for `m=8` around the unique
  degree-nine vertex, reducing it to five aggregate C rows plus exact incidence
  redundancy constraints.
- Added an optional robust vertex-deletion witness family to `snc_cnf.py` and
  had its clauses independently audited. It correctly links selected witnesses
  to deficit one and preserves every old exact second endpoint via an alternate
  midpoint.
- **Next queued attack:** add dedicated exhaustive tests for the new deficit and
  witness selector CNF families, then encode the exact `m=8` five-row normal
  form and the `m=9` isolated-vertex residual as separate certified shards.

## 2026-07-25 — tick 11

- Refactored the production CNF deficit/witness clauses into directly testable
  helpers. Exhaustive tests now verify exact deficit-bit polarity through unary
  width eight and the full robust-witness selector semantics on 3,003
  graph/deletion cases through order four. A low-degree ambiguity in the
  isolated helper was removed by explicitly requiring degree at least two for
  deficit two; production graphs already have degree at least eight.
- Pushed the `m=9` isolated-missing-vertex route through all immediate local
  gain/loss equations. The equality residual remains incidence-feasible; the
  missing step is coupling its root predecessor supports to badness of the
  isolated vertex and the two remainder vertices.
- Derived the order-18 `m=7` robust-witness normal form with two degree-nine
  vertices and exact C/missing/incidence budgets; see
  `attempts/tick11-m7-normal-form.md`.
- **Next queued attack:** add simultaneous robust-witness constraints for both
  high vertices to the `m=7` shards, and encode missing-degree shape shards for
  `m=9` (perfect matching already eliminated, isolated-vertex shapes remain).

## 2026-07-25 — tick 12

- Added exact degree-nine label and distinguished robust-selector options to the
  deterministic CNF generator. The production helpers retain all exhaustive
  semantic test passes.
- Ran the first fully robust, witness-rooted `m=8` B7 shard with the unique
  degree-nine vertex fixed. CaDiCaL remained `UNKNOWN` after 900 seconds; no
  proof artifact or mathematical conclusion was retained. This confirms that
  missing-degree/C-row sharding is required before further long runs.
- Intersected simultaneous robust-witness zones for the two high vertices in
  `m=7`, producing explicit common-missing-edge and high-high support gadgets;
  see `attempts/tick12-simultaneous-witnesses.md`.
- Parameterized all residual `m=9` missing graphs with isolates by excess-degree
  partitions and high-vertex cores. The perfect matching and one-high-vertex
  (star-plus-matching) families are eliminated; core families remain.
- **Next queued attack:** implement exact cellwise missing-degree sequence
  constraints, beginning with the five `m=8` C rows. Generate standalone CNFs
  per sequence and require DRAT/LRAT verification rather than another baseline
  timeout.

## 2026-07-25 — tick 13

- Hostile audit found and repaired a completeness error: the `m=8` normal form
  has six aggregate C rows, including `(p,rho,e)=(8,5,0)`. An explicit local
  realization proves robustness/root incidence do not eliminate it. See
  `attempts/tick13-m8-sharding.md`.
- Added full exact arc-minimality clauses to `snc_cnf.py`. They use existing
  exact path/second/deficit bits and no new variables. Exhaustive deletion
  mutation tests pass 7,860 graph/arc cases through order four.
- Determined that cellwise missing-degree sharding is too coarse (about 1.6
  million sequences). The revised cover uses 762 coarse C margins followed by
  canonical colored eight-edge missing graphs and orientation-circulation
  filtering.
- Built and validated pinned `drat-trim`/`lrat-check` from upstream commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; all bundled examples verify.
- **Next queued attack:** implement the 762-row generator including the sixth
  row, canonical colored missing-graph realizations, and circulation filtering;
  then run small standalone arc-minimal shards with checked LRAT output.

## 2026-07-25 — tick 14

- Implemented and independently count-checked the exact 762-row coarse `m=8`
  C-margin enumeration, including all 36 rows with `rho=5`.
- Derived an exact max-flow orientation feasibility filter for fixed colored
  missing graphs, degree targets, root arcs, `A->C` prohibition, and B-column
  coverage. This will precede expensive SAT shards.
- Completed the first full certificate pipeline on one genuine corrected-sixth-
  row leaf: deterministic CNF, CaDiCaL textual LRAT, and independent
  `lrat-check` verification (`c VERIFIED`). The uncompressed CNF/LRAT hashes and
  compressed artifacts are in `experiments/m8pilot.*`. This eliminates exactly
  one leaf and is not a branch-level theorem.
- The sixth row itself reduces to nine C-margin states and two regimes for the
  unique degree-nine vertex; tournament equalities alone do not close it.
- **Next queued attack:** generate all colored missing-graph leaves beneath the
  36 `rho=5` coarse rows, filter them by max-flow orientation feasibility, and
  issue checked LRAT jobs for every surviving canonical leaf. Maintain a cover
  hash so no leaf is omitted or duplicated.

## 2026-07-25 — tick 15

- Derived and implemented the complete corrected-sixth-row cover: 323 canonical
  colored missing graphs and 735 leaves after C-to-B orientation orbits. The
  leaf key is `(C-state,rho0,rho1,n0,n1,epsilon0,epsilon1,k,t)` and fully
  reconstructs the eight holes and C-B directions.
- Tightened the pilot manifest after hostile audit: its LRAT eliminates exactly
  one rooted robust-witness orbit modulo `S7(A\{r}) x S7(B)`, not a broader
  missing-graph class.
- No whole C-margin state or `mu_r` regime in the sixth row is eliminated by
  current human inequalities. The nine states remain incidence-feasible; the
  pilot is a strict subleaf.
- **Next queued attack:** implement an independent labelled-orbit cover checker
  for the 735 leaves, then add a generic leaf-to-CNF emitter and max-flow filter.
  Schedule checked LRAT runs by leaf complexity and preserve a completion
  ledger keyed by the cover hash.

### First generic leaf run

- Added a generic canonical leaf-to-CNF emitter. Leaf 0, key
  `('M',0,5,0,0,0,0,0,0)`, returned CaDiCaL UNSAT and independently checked
  LRAT `c VERIFIED`. This is a second certified leaf observation, but its bulk
  artifact is deferred until the cover checker/ledger prevents bookkeeping
  omissions.

## 2026-07-25 — tick 16

- Added an independent labelled-mask orbit checker for the complete `rho=5`
  cover. It does not import production cover/reconstruction code, audits
  63,517,608 labelled configurations through exact orbit multiplicities, and
  reproduces 36 rows, 323 colored missing graphs, 735 leaves, and cover hash
  `0e4aa222...6171e`.
- Hostile audit tested all 735 production representatives and found no subset,
  overlap, `state=10`, missing-count, or orbit-reconstruction error.
- An external triage census reports all 735 current leaf CNFs solver-UNSAT, but
  only checked LRATs count. The safest grouping can reduce certification to 136
  margin CNFs by leaving both intersection parameters symbolic; this grouping
  still needs its own cover proof and emitter.
- **Next queued attack:** freeze the campaign manifest against the independently
  verified cover, implement the content-addressed batch runner, and certify
  leaves (or audited grouped margins) with immutable per-index LRAT evidence and
  a generated completion ledger.

## 2026-07-25 — tick 17

- Implemented the representative-free 136-margin grouping of all 735 certified
  leaves. Each group fixes C state, rho split, root/high missing indicators, and
  exact A-hole/B-outneighbor cardinalities while leaving both intersections
  existential. An independent weighted checker reproduces group hash
  `cd8ff2b4...54f4`, leaf cover hash `0e4aa222...171e`, and all 63,517,608
  labelled configurations.
- Hostile audit caught a reversed missing-variable name for C-B units in the
  initial grouped emitter. Global `m=8` made it accidentally redundant, but the
  variables were disconnected; the names are now corrected to ascending pair
  order.
- A pilot grouped CNF returned CaDiCaL UNSAT and independently checked LRAT
  `c VERIFIED`, establishing the grouped proof path operationally.
- **Next queued attack:** rerun the pilot after the C-B variable-name repair,
  freeze grouped campaign hashes, then certify all 136 groups with a generated
  immutable completion ledger. Any SAT group stops the campaign for graph
  decoding and dual verification.
