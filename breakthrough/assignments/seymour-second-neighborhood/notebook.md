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

## 2026-07-25 — tick 18

- Replaced the entire 136-group `rho=5` campaign by a short human contradiction;
  see `attempts/tick18-rho5-human-proof.md`. The key is that nine B-to-C arcs
  force one B vertex to dominate both C vertices, robustness supplies a common
  degree-eight A predecessor, and the 16-vertex tournament degree census gives
  six additional exact second neighbors.
- Three adversarial proof routes checked the exact argument. Generic lifting
  counterexamples without the common dominator/robust predecessor hypotheses
  were correctly rejected as irrelevant.
- The independently verified 735-leaf cover, grouped campaign, and LRAT pilots
  remain committed as regression/audit artifacts, but bulk certification is
  cancelled because the human proof is stronger.
- **Next queued attack:** apply the generalized two-C lifting criterion to the
  remaining `m=8` rows `rho=0,1,2,3,4`. First target `rho=4`, where the induced
  16-vertex graph has one missing pair and at least three B vertices dominate
  both C vertices. Seek control of the near-tournament Seymour vertex's B-degree
  or prove one C vertex Seymour from inaccessible-inneighbor bounds.

### Publication status of the rho=5 result

- The human proof now supersedes the uncompleted bulk campaign and eliminates
  the entire corrected sixth row, not merely the audited leaves. It is a
  restricted order-18 branch theorem and not a solution of SNC.
- The next proof frontier is `rho=4`: the sole B-C missing-pair placement is
  eliminated immediately by the same tournament argument. Otherwise the
  16-vertex graph has one missing edge, at least three common C-dominators, and
  a rigid residual in which one `a* in A\{r}` is the sole predecessor of all
  common dominators and `N_T+(r)={a*} union N_T+(a*)`.

## 2026-07-26 — tick 20

- Eliminated the entire `m=8,rho=4` row by a human proof; see
  `attempts/tick20-rho4-human-proof.md`.
- The near-tournament equality case forces every common C-dominator to have the
  same sole predecessor `a*` in `A\{r}`. At least three common dominators exist.
  Any one not incident with the unique hole then dominates both C vertices,
  `v`, and all six other low A vertices, giving nine outneighbors although its
  degree is eight.
- Hostile audit identified and repaired the only quantifier hazard: the proof
  needs pointwise singleton predecessor sets, not merely one common predecessor.
  This follows because every possible predecessor obeys the same rigid
  outneighborhood identity with `r`.
- **Next queued attack:** `rho=3`. The placement of both residual holes in B-C
  is already eliminated. For one internal T-hole, all robust predecessors of
  common C-dominators satisfy a one-hole equality template. Couple these
  predecessor classes using the badness of the common dominators or
  arc-minimality at their incoming arcs; the target lemma is that at most two
  low-A vertices can occur as such predecessors, enabling the same forced
  degree count.

## 2026-07-26 — tick 21

- Human-eliminated the `rho=3` branch with one internal T-hole; see
  `attempts/tick21-rho3-one-hole-proof.md`. The same rigid predecessor identity
  used for `rho=4` applies unchanged.
- The branch with both residual holes in B-C was already eliminated because T
  is a tournament. Only the two-internal-hole branch remains for a fully human
  elimination.
- Added deterministic `experiments/rho3_shards.py`. Three exact shards (`k=0,1,2`)
  were independently LRAT-checked and all returned `c VERIFIED`; hashes and
  reproduction commands are in `experiments/rho3-certificates.md`. This
  computational theorem relies on the combined robust-witness and arc-minimal
  model and is retained as regression evidence while the human proof is pursued.
- **Next queued attack:** close the two-internal-hole human residual. Current
  compression leaves an exact three-predecessor pattern (when neither hole
  meets `r`) and a hole-supported-r template. Synchronize the two hole endpoint
  identities across the common C-dominators, using arc deletion at `a->b`.

## 2026-07-26 — tick 22

- Human-eliminated the `rho=3,k=2` subcase in which neither T-hole meets `r`;
  see `attempts/tick22-rho3-two-hole-partial.md`. The surviving human template
  has a hole incident with `r`; the checked CNF already eliminates it.
- Rejected an attractive but invalid aggregate inaccessible-incidence proof:
  with two holes, one target/hole-endpoint mark does not determine the source's
  closed outneighborhood. This failed route is now recorded explicitly.
- Began `rho=2`. Its row is `(p,rho,e)=(5,2,3)`, partitioned exactly by
  `k=0,1,2,3` T-holes. Human lifting eliminates `k=0,1`; the remaining profiles
  have respectively at least four and five common C-dominators.
- Added deterministic `experiments/rho2_shards.py` to test the four exact
  aggregate placements. **Next queued step:** solve and independently check all
  four shards, then mine the smallest obstruction in `k=2,3` while retaining
  the human lifting proof for `k=0,1`.

### Rho-2 certification result

- All four exact `rho=2` shards are UNSAT and independently LRAT-verified.
  Deterministic identities and hashes are recorded in
  `experiments/rho2-certificates.md`. Thus the entire `rho=2` row is eliminated
  in the exact minimal-counterexample normal form.
- **Next queued attack:** emit and check `rho=1` and `rho=0` aggregate shards.
  In parallel, continue mining compact human obstructions from the high-k
  rho-2 certificates rather than relying on bulk proofs.

## 2026-07-26 — tick 23

- Derived the final two row partitions. `rho=1` has five shards with
  `k=0,...,4` T-holes; `rho=0` has six with `k=0,...,5`. In both rows the
  common-C-dominator bound is `|K|>=k+2`, and the human tournament/one-hole
  argument eliminates `k=0,1`.
- Added `experiments/rho_low_shards.py`, a deterministic emitter for all eleven
  remaining aggregate shards.
- **Next queued step:** independently solve/check these eleven shards. Any SAT
  result is decoded immediately; UNSAT shards receive hashes and a frozen
  certificate ledger. The high-k human target is a support-synchronization
  lemma coupling the many common C-dominators to the few T-hole endpoints.

### Completion of the m=8 row campaign

- All eleven low-rho shards returned UNSAT and independently checked
  `c VERIFIED`; exact hashes are in `experiments/rho-low-certificates.md`.
- Therefore all six rows `rho=0,...,5` are eliminated in the rooted
  order-18, `m=8`, vertex-minimal then arc-minimal normal form. Rows 4 and 5
  have human proofs; rows 0--3 have deterministic checked aggregate certificates
  (with additional human subcases).
- This is not an order-18 elimination: the separate `m=5,6,7,9` families remain.
- **Next queued attack:** return to `m=9`, where the perfect-matching missing
  graph is already human-eliminated. Split the remaining nine-edge missing
  graphs by degree sequence and robust-witness overlap; prioritize an isolated
  missing-graph vertex, which yields a tournament deletion and should admit the
  same inaccessible-inneighbor lifting argument.

## 2026-07-26 — tick 24

- Recast the complete residual `m=9` branch as a 28-shard aggregate campaign.
  Every non-perfect-matching nine-edge missing graph has an isolate; rooting at
  its robust witness yields seven rho rows and `0<=k<=6-rho` T-hole counts.
  See `attempts/tick24-m9-aggregate.md` and `experiments/m9_isolate_shards.py`.
- The direct deletion `D-z` is not a tournament (all nine holes remain); this
  tempting route was rejected. The robust B7 root is obtained instead from
  exact degree tightness.
- Pilot aggregate low-k shards are tractable, but high-k unshaped shards time
  out and have no certified status. **Next queued attack:** certify the complete
  `k=0,1` strip, then subdivide `k>=2` by the exact colored high-degree core of
  the missing graph and exploit simultaneous zones of multiple isolates.

### Certified m=9 strip

- Completed all thirteen `k=0,1` aggregate shards: every one is UNSAT and
  independently LRAT-verified. Hashes are in
  `experiments/m9-lowk-certificates.md`.
- The residual campaign is exactly the fifteen pairs `(rho,k)` with
  `2<=k<=6-rho`. **Next queued step:** split these by missing-graph high-core
  type, starting with the 28 two-center cores; repeated isolate zones must use
  one of the two centers, giving a small support-signature model.

## 2026-07-26 — tick 25

- Human-eliminated the entire `m=9` isolated-root strip `k=0,1,2`; see
  `attempts/tick25-m9-k012-human-proof.md`. The key simplification over `m=8`
  is that every vertex has degree eight, so every inaccessible vertex must
  consume a T-hole. At `k=2`, each hole singly supports one inaccessible
  endpoint, forcing at most two predecessor classes and then a B-degree
  contradiction.
- Independently LRAT-verified all five `k=2` aggregate shards; hashes are in
  `experiments/m9-k2-certificates.md`.
- The residual aggregate campaign now has ten pairs with `3<=k<=6-rho`.
  For `k=3`, the matching-hole shape has a human contradiction; nonmatching
  shapes reduce to four three-edge hole graphs. Two aggregate shards
  `(rho,k)=(2,3),(3,3)` have checked LRAT proofs from pilot runs; rho 0 and 1
  remain computationally hard without shape splitting.
- **Next queued attack:** split `k=3` by the five unlabeled T-hole shapes
  (matching plus four nonmatching shapes), certify the four nonmatching shapes,
  and seek a uniform dirty-endpoint synchronization lemma.

## 2026-07-26 — tick 26

- Added an exact five-way `k=3` shape split using only the number of T vertices
  of hole-degree at least two and at least three. Under exact three-hole
  cardinality these profiles uniquely distinguish matching, path-plus-edge,
  four-path, claw, and triangle. The independent K6 census passes all 455 edge
  triples (`experiments/test_m9_k3_shapes.py`).
- Rejected a proposed uniform nonmatching human proof: clean endpoint marks
  control predecessor classes, but not their repeated incidence into several B
  columns. The claimed column-sum bound was unsupported.
- **Next queued step:** certify the ten shape shards for rho 0 and 1 using
  `experiments/m9_k3_shapes.py`; rho 2 and 3 already have aggregate checked
  proofs. Retain only independently checked outcomes.

### Completion of m=9 k=3

- All ten rho-0/1 shape shards are independently LRAT-verified; hashes are in
  `experiments/m9-k3-shape-certificates.md`. Together with the checked aggregate
  rho-2/3 runs, the entire `k=3` strip is eliminated.
- The residual `m=9` aggregate campaign is now six pairs:
  `(rho,k)=(0,4),(1,4),(2,4),(0,5),(1,5),(0,6)`.
- **Next queued attack:** classify four-edge T-hole graphs by degree/cycle
  profile and target the `k=4` rows, where five or six B vertices dominate both
  C vertices and exact degree pressure forces at least four predecessor classes.

## 2026-07-26 — tick 27

- Classified the eleven four-edge T-hole shapes by the exact local invariant
  `(number degree>=2, >=3, >=4, triangles, core edges)`. The independent K8
  census checks all `C(28,4)=20475` edge sets; see
  `experiments/test_m9_k4_shapes.py`.
- Aggregate `k=4` rho 0--2 remains solver-hard and returned only UNKNOWN under
  the current cap. Human degree pressure forces five or six common C-dominators
  and at least four low-A predecessor classes, sharply isolating dirty endpoint
  reuse as the obstruction.
- **Next queued step:** implement the eleven-way k4 classifier in CNF and certify
  shape shards, beginning with the clean matching and star-like shapes. In
  parallel, attack the final k5/k6 rows via the C-to-root endpoint reserve and
  internal-B-hole split.

### k4 emitter

- Added `experiments/m9_k4_shapes.py`, encoding the eleven exact invariant
  profiles with bidirectional degree, triangle, and core-edge semantics.
- Human endpoint packing eliminates the pure four-star and claw-plus-edge
  shapes; the matching shape compresses to exactly four predecessor classes
  with near-complete incidence but still needs synchronization.
- **Next queued experiment:** run the 33 `(rho,shape)` shards, prioritize the
  two human-eliminated shapes as semantic regressions, and retain only checked
  LRAT completions. For k5/k6, first split by root-C hole count `g`, then by
  internal-B-hole count only on `g=0`.

## 2026-07-26 — tick 30

- Human-eliminated the four-matching `k=4` shape by a one-predecessor argument;
  see `attempts/tick30-m9-k4-matching-proof.md`. Two inaccessible vertices
  would have to be nonadjacent, contradicting that each already uses its unique
  matching hole into the predecessor's closed outneighborhood.
- Of the 33 k4 shape shards, 18 are independently LRAT-verified and 15 remain
  UNKNOWN at the current cap. The checked set includes all rho values for C4,
  four-matching, and the four-star; no claim is made for timed-out shards.
- **Next queued attack:** preserve the checked k4 ledger, rerun the 15 unresolved
  shapes with a rooted-cell incidence split. Implement the 25-shard final-row
  cover `(rho,k,g,hB)` and first certify all `g=1,2` strips.

## 2026-07-26 — tick 31

- Completed the entire 25-shard cover of the three final `m=9` aggregate rows:
  every `g=1,2` cell and every `g=0,hB` cell is independently LRAT-verified.
  See `experiments/m9-final-certificates.md`.
- Therefore the only unfinished part of the `m=9` isolated-root campaign is
  the fifteen unresolved `k=4` shape parents. Eighteen of 33 are checked; all
  fifteen unresolved were further split, but no parent yet has a complete leaf
  cover.
- Hardened `m9-final-shards.py` against invalid exact counts and hB/g arguments.
- **Next queued attack:** split each unresolved k4 parent by rooted placement of
  degree-at-least-two shape vertices among root, A', and B; only B-rich children
  then need `|K|` and internal-K-hole refinement.

## 2026-07-26 — tick 32

- Added `experiments/m9_k4_placements.py` and refactored the shape emitter so
  placement children reuse exactly the audited parent constraints. The split
  records degree-at-least-two hole vertices in A', B, and the witness root.
- A scout campaign checked 29 of 87 placement leaves; no parent is yet fully
  covered. The unresolved leaves are concentrated in B-rich placements.
- **Next queued attack:** for B-rich leaves, split by the exact number of common
  C-dominators (`5` or `6`) and holes internal to that dynamically defined set.
  This directly exposes the B-degree pressure rather than adding generic root
  degree counters.

## 2026-07-26 — tick 33

- Extended `m9_k4_placements.py` with exact dynamic predicates for the common
  C-dominator set K and exact internal-K hole count eta. All equivalences are
  bidirectional.
- A 580-cell scout (`58 placement leaves x 2 kappa x 5 eta`) independently
  verified 281 cells; 299 remain UNKNOWN and no placement parent is fully
  closed. Eight parents have only the hard `(kappa,eta)=(5,0)` cell left.
- Audited placement coverage: the permissive alpha/beta/epsilon partition is
  exhaustive (with nine harmless empty tuples). Earlier hand-pruned feasibility
  lists would have omitted three valid root-plus-A' placements and must not be
  used for cover claims.
- **Next queued attack:** isolate the eight `(5,0)` singleton residuals first;
  derive their complete predecessor-incidence equality template or split by
  whether the degree-three shape hub lies in K. Then process the other B-rich
  cells by high-degree-in-K count.

## 2026-07-26 — tick 34

- Added exact `lambda=|K intersect {hole-degree>=2 vertices}|` support to the
  dynamic placement emitter. A temporary exhaustive lambda/hub split closed all
  eight placement parents whose only residual was `(kappa,eta)=(5,0)`; all 15
  child cells were independently LRAT-verified.
- The broad scalar identity alone does not close `(5,0)`; tournament-king
  lifting leaves sharp equality templates. The successful lambda split confirms
  that location of the marked hole vertices inside K is the decisive next
  coordinate.
- **Next queued attack:** apply lambda to the remaining 50 placement parents,
  beginning with beta<=2 where lambda has at most three values. Refine unique
  degree-three hubs only after lambda leaves time out.

## 2026-07-26 — tick 35

- A hostile audit found that `--lambda-k` was silently ignored when supplied
  without `--kappa/--eta`, and that negative lambda values reached Python's
  negative indexing. The emitter now rejects incomplete refinement coordinates,
  enforces the sharp placement-dependent range
  `max(0,beta-(7-kappa)) <= lambda <= min(beta,kappa)`, and prints every active
  split coordinate in its deterministic log line.
- Added an independent finite partition audit. It reproduces all 165 permissive
  placement leaves over 33 shape parents and checks 21,450,240 direct
  `(K,four B-holes,marked-set)` coordinate evaluations. The independent
  coordinate census passes, and the generic threshold-counter semantics pass
  the existing exhaustive tests; this does not by itself test the emitted
  placement-specific `K/HK/LK` gates.
- Proved the exact endpoint-packing inequality
  `q(t)+q(u)+1[tu hole]>=3` for two vertices inaccessible from one robust
  predecessor. It recovers the four-matching proof but is sharp for the
  `P3+2K2` shape; a three-hole local counterconfiguration shows that packing
  alone cannot synchronize predecessor sets. See
  `attempts/tick35-k4-packing-barrier.md`.
- The earlier 87-leaf and 580-cell scout totals are not independently
  reproducible from a committed parent/child manifest. They remain exploratory
  timing observations, not a cover theorem. Before any branch-level claim, the
  unresolved-parent list, every child key, CNF/LRAT hashes, and a complete
  independently checked ledger must be committed.
- **Next queued attack:** freeze that manifest and rerun the residual lambda
  cover with the repaired CLI. On any remaining hard child, split by membership
  of the unique degree-three/four hub in K and by the exact inaccessible
  three-hole packet type, rather than repeating an unchanged timeout.

## 2026-07-26 — tick 36

- Replaced the unreproducible scout-parent bookkeeping with a complete 2,925-key
  hierarchy for every `rho`, four-hole shape, rooted placement, `kappa`, `eta`,
  and valid `lambda` value in the entire isolated-root `m=9,k=4` normal form.
- An exact four-color support enumeration proves 1,785 terminal cells
  structurally empty at the missing-graph level and leaves 1,140 feasible CNF
  jobs. The converse construction fills unused cells with hole-isolated
  vertices, so this filter is complete for missing-graph compatibility.
- Production and separately implemented subset-based cross-checkers agree
  byte-for-byte on `experiments/m9-k4-cover.tsv`; this is not an independent
  derivation of the hierarchy. The key-stream SHA-256 is
  `51700d5b...b61195`; the ledger SHA-256 is `9e8ebba3...9f1cae`. See
  `attempts/tick36-k4-cover.md` for the proof and commands.
- No prior scout UNSAT status is imported. The 1,140 survivors are all `UNRUN`
  until regenerated with the repaired CLI and independently LRAT-checked.
- **Next queued attack:** rank the 1,140 surviving cells by shape and
  `eta/lambda`, rebuild the pinned CaDiCaL 1.7.3 and `lrat-check` toolchain, and
  run a small certificate-producing pilot across every shape before scheduling
  the complete content-addressed campaign.

## 2026-07-26 — tick 37

- Rebuilt CaDiCaL 1.7.3 from source commit `38e073b...` and `lrat-check` from
  `2e3b2dc...`. The checker binary reproduces the historical hash; the new
  CaDiCaL binary hash differs from the historical build, so both source commit
  and current binary hash are recorded rather than pretending binary identity.
- Added a solver-blind deterministic selector choosing one maximally
  concentrated feasible cell per shape. All eleven pilots returned UNSAT and
  were independently accepted by `lrat-check`; exact CNF/LRAT hashes and sizes
  are in `experiments/m9-k4-pilot-certificates.md`.
- The LRAT files total roughly 0.94 GB and currently live only in temporary
  storage. Therefore these are explicitly regression observations, not durable
  certificate rows: all 1,140 campaign cells remain `UNRUN` for cover purposes.
- **Next queued attack:** implement content-addressed proof retention before
  any bulk run. Begin with the 138 feasible C4 cells, where the pilot was fast,
  and commit a machine-readable completion ledger whose `UNSAT_VERIFIED` state
  requires accessible proof bytes, matching hashes, and checker readback.

## 2026-07-26 — tick 38

- Replaced the planned 138-cell C4 campaign with a uniform human contradiction;
  see `attempts/tick38-c4-human-proof.md`.
- The five or six common C-dominators require at least four distinct A'
  predecessor sources by an exact B-row degree count and the four-hole budget.
  For each source, badness forces exactly two inaccessible cycle vertices. An
  adjacent pair determines the source's closed outneighborhood and fixes both
  cycle diagonals; an opposite pair also determines it via the intersection of
  two exact outneighborhoods. At most one adjacent template and the two opposite
  templates coexist, giving at most three sources, a contradiction.
- Three hostile audits independently checked the degree identity, exact-second
  count, opposite-pair intersection, source uniqueness, and diagonal table. No
  computational certificate is needed for this shape.
- This eliminates the C4 shape uniformly in rho but remains a restricted branch
  theorem inside `n=18,m=9,k=4`, not an order-18 result or SNC resolution.
- **Next queued attack:** apply the same predecessor-source lower bound to paw
  and triangle-plus-edge. Classify inaccessible packets by the four-hole support
  and seek a compatibility cap below four; preserve a sharp local breaker if
  either shape admits four source templates.

## 2026-07-26 — ticks 39--40

- Human-eliminated the paw and triangle-plus-disjoint-edge T-hole shapes; see
  `attempts/tick39-paw-human-proof.md` and
  `attempts/tick40-triangle-edge-human-proof.md`.
- In both shapes, the shape-independent B-row count requires at least four A'
  predecessor sources. Exact inaccessible-packet classification and saturated
  outneighborhood rows allow at most three sources. For the paw, five packet
  types reduce through the two present orientations incident with the pendant
  vertex. For triangle-plus-edge, packets are either two triangle vertices or
  one triangle vertex plus one isolated-edge endpoint; two distinct triangle
  packets exclude every mixed packet.
- Hostile finite analysis exposed why saturation matters: a weaker census that
  records only forced positive arcs reports spurious four-source paw and
  triangle-edge templates. Recording the complete degree-eight rows destroys
  them. Both final proofs received independent line-by-line audits.
- Together with C4 and the previously human-eliminated matching and star-like
  shapes, five of the eleven four-edge shapes now have human contradictions in
  this normal form. No claim is made for the six remaining shapes.
- **Next queued attack:** rigorously audit the proposed common cut/template
  argument for P5 and fork. It currently claims the same source cap but lacks a
  written packet table; first demand either a complete table with saturated
  negative orientations or an explicit four-source breaker.

## 2026-07-26 — ticks 41--42

- Human-eliminated the fork and P5 T-hole shapes; see
  `attempts/tick41-fork-human-proof.md` and
  `attempts/tick42-p5-human-proof.md`.
- Fork has exactly four saturated packet types. Each reconstructs the source's
  closed outneighborhood, and all four cannot coexist; hence at most three
  predecessor sources, contradicting the universal lower bound four.
- P5 has seven packet labels. Their complete compatibility depends only on the
  six orientations of present pairs on the five-vertex support. The exact
  Boolean table has maximum two compatible labels; the 64-case transparent
  checker is `experiments/check_p5_packets.py`. A hostile audit separately
  reconstructed the table from crossing-hole capacities.
- A competing exploratory claim that P5 had compatibility maximum one was
  false; an exact two-source local witness exists. The audited theorem uses the
  sharp maximum two and does not inherit that overclaim.
- Eight of the eleven four-edge shapes now have human contradictions in this
  normal form: C4, paw, triangle-plus-edge, fork, P5, four-matching, and the two
  previously handled star-like shapes (`K1,4` and claw-plus-edge, counted there
  as separate profiles). The remaining human frontier is P4-plus-edge,
  two-P3, and P3-plus-two-edges; checked CNF evidence exists but does not replace
  proofs.
- **Next queued attack:** start P4-plus-edge with a complete saturated packet
  table. Its disconnected spare edge admits the sharp `(2,1)` packet from the
  tick-35 barrier, so the next lemma must synchronize multiple sources rather
  than rely on a single-source cut count.

## 2026-07-26 — ticks 43--44

- Eliminated the three disconnected residual shapes P4-plus-edge, two-P3, and
  P3-plus-two-edges by saturated packet compatibility; see
  `attempts/tick43-disconnected-shapes.md`. The sharp source caps are 3, 2, and
  2, below the shape-independent lower bound 4.
- Added `experiments/check_disconnected_packets.py`, which independently
  enumerates 2,048, 2,048, and 131,072 support orientations and verifies the
  three caps and cut multiplicity one. Hostile audit caught and repaired two
  polarity errors in the displayed P4 formulas; the checker-derived caps were
  unaffected.
- A coverage audit found that K1,4 and claw-plus-edge had only notebook
  assertions, not reconstructible proof files. Added both proofs in
  `attempts/tick44-star-shapes.md`: K1,4 admits no inaccessible pair, while
  claw-plus-edge has only two packet labels and therefore at most two sources.
- The independent 20,475-graph shape census confirms these eleven profiles are
  disjoint and exhaustive. All eleven now have written human contradictions,
  so the complete isolated-root `m=9,k=4` strip is human-eliminated uniformly
  over rho, placements, kappa, eta, and lambda.
- This is not an order-18 elimination: other missing counts `m=5,6,7` remain,
  while `m=8` and `m=9` residual bookkeeping must be reconciled carefully.
- **Next queued attack:** update the m=9 campaign ledger to remove the entire
  k4 strip, then inspect whether all other k strips were already closed by the
  k<=3 and final-row arguments. If so, promote the full m=9 branch only after a
  hostile coverage audit; otherwise isolate the exact remaining cells.

## 2026-07-26 — tick 45

- A durability audit found that the historical LRATs for all four `k=3` rows
  and the three final `k=5,6` rows are absent; hashes alone are not currently
  checkable certificates. Thus the complete m=9 branch cannot yet be promoted
  from those ledgers.
- Replaced the full `k=3` certificate dependence by a human proof; see
  `attempts/tick45-k3-human-proof.md`. The three-hole B-row count requires at
  least three predecessor sources. Matching, P3-plus-edge, P4, and claw admit
  at most 0, 2, 2, and 0 sources. Triangle admits three packet labels, but the
  tight all-label case synchronizes the triangle outneighborhoods, forces the
  three sources to be the triangle vertices, and makes four common dominators
  have at most four internal B-arcs against the required six.
- Therefore the entire isolated-root `m=9,k=3` strip is now human-eliminated,
  uniformly in rho. Together with ticks 25 and 30--44, all `k=0,...,4` rows
  are durable human theorems.
- The exact durable residual for m=9 is now only `(rho,k)=(0,5),(1,5),(0,6)`.
  Historical checked-LRAT claims cover their 25 final shards, but no proof bytes
  are retained. **Next queued attack:** derive a human final-row contradiction,
  starting with k=6 where all six residual holes lie in T and the source lower
  bound is strongest; use saturated packet compatibility rather than regenerate
  bulk certificates.

## 2026-07-26 — tick 46

- Compressed the k=6 final row to seven simultaneous bad A' source rows. Layer
  capacity forces `P=A'`, and exact row sums require
  `e(A',B)=29+h(A')+Q>=29`.
- Temporary tests reject a solver-inspired lemma claiming every bad source has
  at most four B-outneighbors: a relaxed one-source model reportedly has five
  B-outneighbors and a sharp three-hole packet. No witness artifact was retained,
  so this remains an unverified breaker observation. Likewise, reported
  six-of-seven badness tests are exploratory rather than durable conclusions.
- Derived the exact packet pressure: inaccessible triples avoid B and consume
  all six holes; inaccessible pairs contain at most one B vertex and consume at
  least three holes, or at least five when they contain B. Hole loads cannot be
  summed without controlling reuse.
- A tentative arc-minimal charging route appears vulnerable to gain cycles but
  has no retained exact breaker. See `attempts/tick46-k6-frontier.md`.
- **Next queued attack:** classify the maximal six-bad relaxations. Test whether
  their six-hole graph is necessarily `2K3` and whether the omitted Seymour
  source is forced by a triangle-row synchronization theorem. If false,
  enumerate the exact finite family of hole-support cores rather than all
  six-edge graphs.

### Reduced-model sharp fixture

- Added a deterministic 16-vertex relaxation with exact reduced degrees and
  existential inaccessible witnesses. It removes C and all full-CNF path,
  deletion, and arc-minimality machinery while preserving every genuine k=6
  counterexample as a model.
- A directly verified six-of-seven witness has holes exactly `2K3` on the six
  selected A' vertices. Each selected source has the other two triangle vertices
  inaccessible; the omitted source has none. This sharp fixture is committed
  with SHA-256 `c6f958a...979c7e` and prevents overclaiming from six rows.
- The all-seven reduced CNF is only 3,105 variables/12,128 clauses but remains
  solver-hard under current direct runs. No reduced UNSAT claim or 2K3-forcing
  theorem is accepted: packet-only censuses admit many spurious cross packets,
  and full closed-row/rooted coupling is essential.
- **Next queued attack:** cube the reduced CNF first by six-hole support, retain
  explicit SAT leaves and LRAT for UNSAT leaves, and build an assumption-cover
  checker. This is the smallest currently proved-sound finite terminal model.

### Canonical primary cube cover

- Replaced the raw hole-support split by a stronger 65-leaf semantic symmetry
  cover fixing one complete A' source row and its two selected inaccessible
  witnesses. The stabilizer `S6(A'\{2}) x S7(B)` reduces 63,063 labelled
  row/witness objects to 65 keys.
- `check_k6_reduced_cubes.py` independently enumerates every labelled object,
  reproduces all orbit multiplicities, and matches manifest SHA-256
  `3936f5da...b4a7ab`. Each cube fixes all fifteen source-row arc decisions and
  two selectors, giving stronger propagation than coarse hole counts.
- This is semantic graph symmetry: sequential-counter auxiliaries receive fresh
  satisfying extensions after relabelling and are not treated as syntactic CNF
  automorphisms.
- **Next queued experiment:** scout all 65 leaves under a fixed cap. Refine only
  hard leaves by the incoming-versus-hole status of the seven non-outneighbors,
  yielding at most 1,110 complete-cut orbits rather than a raw six-hole census.

### Primary cube scout

- Ran all 65 canonical leaves with CaDiCaL 1.7.3 under a deterministic 20-second
  cap. Twenty-nine returned UNSAT and 36 timed out; no SAT leaf appeared. The
  unresolved leaves represent labelled multiplicity 39,339 of 63,063.
- Results are frozen in `experiments/k6-reduced-scout-20s.json`. They are timing
  observations only: no LRAT was retained and no leaf is mathematically closed
  by this scout.
- Easy UNSAT is strongly concentrated when z is one of source 2's selected
  inaccessible witnesses, or when source 2 has very high A'-outdegree. The hard
  set includes every low-A/high-B profile and most witnesses involving w.
- **Next queued attack:** implement the 1,110 complete-cut orbit enumerator and
  restrict it to the 36 hard parents. Distinguishing incoming arcs from holes is
  the missing propagation in those leaves; preserve the independent labelled
  orbit-multiplicity audit before any certification campaign.

### Complete-cut refinement

- Added the full incoming-versus-hole refinement of the source-2 cube cover.
  There are exactly 1,110 semantic orbits representing 3,171,168 labelled
  complete source cuts with two selected witnesses.
- Production and independently implemented labelled enumeration agree on every
  key, orbit multiplicity, and canonical representative; manifest SHA-256 is
  `3979f9dc...abbb970`.
- Each complete cube fixes outgoing, incoming, and hole status for all fifteen
  source pairs, plus the two witness selectors. This is the frozen secondary
  split for the 36 hard primary leaves.
- **Next queued experiment:** map complete-cut children to their primary parent,
  run short scouts only below the 36 hard parents, and retain the first LRAT
  pilots to measure whether per-leaf proofs are small enough for durable Git or
  require external content-addressed storage.

### Packet-pressure breakthrough in the complete-cut split

- Exactly 671 of the 1,110 complete-cut orbits refine the 36 hard primary
  parents. A naive two-second scout left every child unresolved, confirming that
  merely fixing one full source cut does not expose the collective obstruction.
- Derived a new exact selected-pair identity. For source `a`, selected
  inaccessible witnesses `t,u`, eight outneighbors `O`, five remaining vertices
  `R`, and `h` holes incident with `a`, let `i_v` indicate `v->a` and `b_v`
  indicate `v in B`. Then
  `e+({t,u},R)+h_other = 5-h-i_t-i_u-2b_t-2b_u`, where `h_other` counts holes
  outside the source/witness support. This follows by summing the exact witness
  outdegrees and the global exact six-hole count.
- Immediate consequence: `h+i_t+i_u+2b_t+2b_u <= 5`. This rejects 279 of the
  671 hard children structurally, representing labelled multiplicity 969,048.
  The sound upper-bound half was added as redundant propagation clauses.
- With those clauses, a one-second CaDiCaL scout returns UNSAT on 430 children
  and leaves 241 UNKNOWN. These remain scout statuses except for the retained
  pilot below.
- Retained and independently checked the first compact LRAT pilot, complete-cut
  index 1, key `(0,1,7,0,0,0,2)`: CNF SHA-256
  `e386e22a...6736cb20`, LRAT SHA-256 `d9922feb...73845cf9`; `lrat-check`
  returned `c VERIFIED`. Files are `k6-pressure-pilot-0001.{cnf,lrat}`.
- **Next queued attack:** encode the exact identity rather than only its
  outgoing-arc upper bound by introducing explicit semantic hole variables and
  a redundant exact-six-hole cardinality. Then rescout the 241 residual leaves
  and retain LRATs for all compact terminal leaves.

### Reduced k=6 certificate closure

- Encoded the exact packet identity with explicit hole variables and a
  redundant exact-six-hole cardinality. Independent hostile audit verified the
  support partition, formula, hole equivalence, and exact-cardinality semantics.
- Certified every one of the 1,110 complete-cut orbit representatives. Each
  leaf was generated deterministically, solved by pinned CaDiCaL, accepted by
  pinned `lrat-check`, compressed into a content-addressed object, then freshly
  regenerated and rechecked by `k6_exact_verify.py`.
- Fresh readback result: `PASS leaves=1110 labelled=3171168`. The archive has
  SHA-256 `e44f8ff8...4bb80402`, size 103,486,540 bytes, and represents
  602,210,046 uncompressed LRAT bytes in 651 deduplicated proof objects.
- Therefore the 16-vertex all-seven reduced model is now durably UNSAT. Combined
  with the written forward reduction, this closes the remaining `(rho,k)=(0,6)`
  isolated-root `m=9` row.
- **Next queued attack:** return to the two exact durable residuals
  `(rho,k)=(0,5)` and `(1,5)`. Reconstruct their strongest reduced collective
  models and require retained proof bytes rather than historical checked-run
  hashes.

### Common k=5 reduction and direct-proof recovery

- The two residual rows project to the same 16-vertex degree sequence:
  `8^9,7^1,6^6`, hence exactly five holes. The exceptional B vertex has degree
  seven; the other six dominate both deleted C vertices and have degree six.
- Every A' row requires at least one inaccessible T vertex, and rows pointing
  to a degree-six B vertex require at least two. This conditional model was
  independently audited and encoded in `k5_reduced_cnf.py` (3,112 variables,
  12,177 clauses). A direct 600-second scout remained unresolved.
- In parallel, `k5_final_campaign.py` regenerated all sixteen historical full
  shards byte-for-byte, and every retained LRAT was independently checked. The
  direct proof objects compress to about 3.88 GB, too large for ordinary Git;
  they remain local recovery evidence until immutable external storage is
  arranged. Historical LRAT hashes were reproduced exactly.
- **Next queued attack:** add explicit five-hole variables and the exact
  defect-weighted pair/singleton packet identities to the common reduced model;
  then construct a canonical source-cut cover under `S7(A') x S6(K)` and retain
  compact LRAT objects from inception.

### k=5 defect-packet orbit cover

- Added explicit semantic holes and exact-five propagation to the common model,
  then classified a canonical source's complete cut and required singleton/pair
  packet under `S6(A'\\{a}) x S6(K)`.
- The packet-pressure filter leaves exactly 931 semantic orbits representing
  758,181 labelled source-cut/witness objects. Independent exhaustive labelled
  enumeration agrees key-by-key; payload SHA-256 is
  `020cbf13...9f45deb5`.
- Each leaf encodes the full defect-weighted packet identity, not only its
  nonnegative bound. A two-second CaDiCaL scout returned UNSAT on 928 leaves and
  timed out on only indices 915, 918, and 921; all three solve UNSAT under a
  longer cap. These are not yet certificate claims.
- **Next queued attack:** launch a content-addressed LRAT campaign across all
  931 leaves, first piloting the three hard singleton leaves and a stratified
  sample to bound proof storage. Independently regenerate and fresh-check every
  retained object before closing both k=5 rows.

### Reduced k=5 certificate closure

- Completed all 931 packet leaves. The campaign represents 917,003,695 raw LRAT
  bytes and compresses to a 120,197,280-byte archive with SHA-256
  `d3f845d9...137c0f1d`.
- Fresh deterministic CNF regeneration, object hash readback, decompression, and
  pinned `lrat-check` acceptance succeeded for every leaf:
  `PASS leaves=931 labelled=758181`.
- Together with the independently audited common projection, this durably closes
  both final isolated-root rows `(rho,k)=(0,5)` and `(1,5)`. Thus every row in
  the isolated-root `m=9` aggregate is now eliminated.
- Combining the isolated-hole closure with the earlier perfect-matching theorem
  closes the complete `m=9` branch: a nine-edge missing graph on 18 vertices
  without an isolate has average and minimum degree one, hence is exactly
  `9K2`. The normalization and complement argument are consolidated in
  `attempts/tick48-complete-m9-closure.md`.
- Scope remains restricted: the exact order-18 residual is `m in {5,6,7}`; this
  is not all order 18 and not SNC.
- **Next queued attack:** complete the existing 170-ledger `m=5`, B6 frontier
  by adding exact A-B incidence, simultaneous badness, and arc-deletion private
  endpoint constraints. In parallel, construct the currently missing six-edge
  support census for `m=6`.

### Fresh m=5 B6 placement cover

- The historical 170-ledger boundary is not reproducible from committed files:
  its scratch enumerator and at least one immediate filter were never retained.
  Replaced it with a broader first-principles cover that does not trust those
  counts.
- The five uncovered support shapes have exactly 4,355 canonical rooted-layer
  placements under support automorphisms and layer permutations, with counts
  `688,1459,283,194,1731`. Independent enumeration agrees; payload SHA-256 is
  `e5873a71...7d305ed9`.
- Every placement emits a standalone full order-18 CNF containing exact first
  and second neighborhoods, badness, all robust deletion witnesses, full arc
  minimality, and every missing-pair unit. A one-second scout eliminated 4,332
  parents and left only 23 hard placements.
- Splitting each hard parent by the exact number of high vertices in C and the
  exact C-to-B arc count leaves one hard child per parent: either `(highC,r)=(1,0)`
  or `(2,1)`. All other children solve immediately. This recovers the structural
  hinge without relying on the missing old ledger filters.
- **Next queued attack:** refine those 23 children by the three C-pair states
  and robust-witness location for high C vertices; freeze a complete child cover
  and retain LRATs only after an independent partition audit.

### m=5 B6 internal hinge

- Exhaustively refined the 23 hard `(highC,r)` cells by the exact high mask,
  three internal-C pair states, and (when `r=1`) the unique C-to-B tail modulo
  `S6(B)`. Independent audit confirms exactly 155 disjoint exhaustive cases.
- A five-second scout eliminates 120 cases. The remaining 35 collapse to only
  three human templates: 24 transitive-C rows with two high vertices and the
  middle as unique B-tail; nine one-high source rows with the other C-pair
  missing; and two one-high transitive-C rows.
- A robust witness for a high C vertex lies in B or its internal C-inneighbors.
  Normalizing selected witnesses yields one B-witness leaf in the one-high rows
  and three leaves in two-high rows (internal middle witness, same B witness,
  distinct B witnesses). Twenty-four of the resulting 83 witness leaves solve
  in 20 seconds; 59 remain hard, concentrated in the internal and distinct-B
  branches.
- The first easy-parent LRAT pilot is compact: 6,635,496 raw bytes and 462,504
  bytes under xz-3, independently accepted by pinned `lrat-check`.
- **Next queued attack:** freeze a hierarchical cover consisting of easy
  parents, easy `(highC,r)` children, easy internal-C children, and witness
  refinements for the 35 residuals. Split the 59 hard witness leaves by the
  exact gain/private-loss status of the distinguished B-to-C witness arc.
