---
name: breakthrough-method
description: Reusable methodology for machine-assisted mathematical breakthroughs — formulate an exact certificate test before searching, parameterize structured families, avoid the abstract-gadget/splice trap, mine no-go lemmas, guard against false positives with exact pricing, verify unconditionally. Anchor case the DGG conjecture disproof. Load whenever attacking any open problem.
---

# Machine-Assisted Mathematical Discovery — the playbook

Anchor case: the Dinitz–Garg–Goemans (DGG) conjecture disproof, July 2026.

## 0. Thesis

Every recent AI-assisted breakthrough (DGG disproof, AlphaEvolve, FunSearch,
Boolean Pythagorean Triples, the Erdős unit-distance disproof, Erdős #1196,
AlphaProof) shares one skeleton, whatever the engine:

1. **Turn the open question into an exact, checkable separation/certificate
   test** before generating a single candidate object.
2. **Search a structured, parameterized family**, not raw combinatorial space
   — chosen so the certificate test is cheap on any member.
3. **Treat every failed attempt as data**: extract a no-go lemma that shrinks
   the family for the next round.
4. **Verify the winner exactly**, independent of the process that found it —
   floats, restricted enumerations, single-model self-report are inadmissible.

Implement this as a LOOP, not a single pass.

## 1. Formulate the certificate BEFORE searching

Never search without first writing what a positive result looks like as a
decidable predicate, ideally with an LP/ILP dual (a numerical margin you watch
converge or diverge).

### DGG separation test (template)
Conjecture: for fractional single-source flow `x` (demands `d_i`, `D=max d_i`)
there's an unsplittable routing `y` with (a) `y_a <= x_a + D` ∀a
("capacity-good") and (b) `c^T y <= c^T x` for every `c >= 0`.
Let `S(x)` = capacity-good unsplittable routings. Two equivalent tests:
- **Convex-hull view**: conjecture holds for `x` iff `x ∈ conv(S(x))`.
- **Separation LP**: `max_{c,δ} δ  s.t.  c^T y >= c^T x + δ  ∀y∈S(x)`,
  normalized `c`. `δ*>0` = counterexample certificate, and duality hands you
  the separating `c*` in the same solve.
DGG worked case: `x` costs 58; every capacity-good `y` costs ≥60 ⇒ `δ*≥2`.

### Generalize
For any "structure X always admits a good rounding/realization" conjecture,
write before searching: the feasible set of good solutions `S(instance)`; the
linear/convex functional the conjecture preserves; the separation LP/ILP whose
positive optimum is definitionally a counterexample. If you can't write this
LP, you don't have a target yet — formalize, don't generate.

## 2. Choose the object: parameterize, don't enumerate

Brute-forcing raw instances is intractable and produces structureless objects.
Instead:
- **Pick a combinatorial engine known to produce your obstruction, embed it.**
  DGG's engine was a stable-set / fractional-relaxation gap: three items
  competing for one unit of shared resource, fractional selection probs
  summing to >1 (triangle `z1+z2+z3<=1` violated at 16/15). Then you only
  realize a triangle conflict in a flow network — space collapses from "all
  7-vertex weighted digraphs" to "networks realizing a rank-3 stable-set
  violation, 2 path-choices per terminal."
- **Parameterize by the invariant driving the gap**, not raw size. DGG free
  params = demand ratios + per-arc overload; topology is a consequence.
- **Program search** (AlphaEvolve/FunSearch): family = programs reachable by
  mutation from a seed, scored by a fast EXACT evaluator (rank check, cap-set
  validity) so thousands scored/hour with no human review.
- **SAT** (Pythagorean, Schur 5): family = the CNF encoding; symmetry breaking
  + cube-and-conquer turn astronomical enumeration into parallel search.
- Rule: >2–3 free structural params and no invariant driving the obstruction
  = you're enumerating. Stop, find the invariant first.

## 3. The abstract-gadget → realize TRAP (why past attempts failed)

Most instructive DGG failure: build an ABSTRACT gadget (a cube whose
combinatorics provably has the stable-set violation), then embed it. Fails
because the concrete structure has its own closure ops the abstract design
ignores. In graphs: **path splicing** — if designed paths `P_i`,`P_j` share
vertex `v`, the hybrid (prefix of `P_i` to `v`, suffix of `P_j` from `v`) is
ALSO legal, and usually REPAIRS the obstruction by dodging the overloaded arc.
The abstract "no good rounding" proof silently assumed a closed move-set; the
realization reopened it. General phenomenon: prove an obstruction in an
abstract system, realize it in a richer structure with its own closure (graph
reachability, group generation, algebraic/geometric closure) → re-check the
closure doesn't add escape routes.

What to do instead:
1. **Design directly inside the closed structure.** DGG winner: the ONLY paths
   are the 2 intended per terminal (6 total, zero hidden splices) — spine
   entry/exit points chosen so any splice is ill-typed or reproduces a
   designed path, never a novel cheaper one.
2. **Or force the constraints to neutralize hybrids**: costs/capacities making
   every hybrid cost-dominated or capacity-infeasible — robust to closure.
3. **After realization, enumerate the closure** (all paths under reuse, all
   generated elements) up to certificate-relevant size and re-run the
   separation test against the FULL realized object.

## 4. No-go lemmas: turn failures into search-space compression

A failed attempt is worthless unless distilled into a theorem ("no instance
with P works, because Q") that prunes the family. DGG examples:
- **Equal demands can't work** (min-cost-flow integrality absorbs any gap) →
  restrict to strictly unequal demand multisets.
- **Three tracks can't enforce a permutation at additive error exactly D**
  (slack too forgiving) → search ratios/overloads where the fractional
  stable-set violation exceeds 1 by MORE than one unit of slack can absorb
  (exactly how 15,10,15→16/15 was targeted, not stumbled on).
Discipline: every terminated branch produces (a) a positive certificate, (b) a
machine-checked no-go lemma with precise scope logged to a shared registry so
parallel subagents don't re-explore it, or (c) an inconclusive tag with the
specific reason. Never silently drop a branch. Spend real time sharpening lemma
scope — tighter scope reclaims more space.

## 5. Avoid false positives: exact pricing over the ENTIRE family

Most dangerous failure: solve the separation LP over an enumerated SUBSET, get
`δ*>0`, but an OMITTED family member closes the gap to zero. Fix (column
generation / cutting plane):
1. Solve restricted LP over current subset → candidate `(c*,δ*)`.
2. **Exact pricing oracle** over the FULL legal family (shortest-path /
   min-cost-flow / a MIP over all integral routings under the true
   constraints): "does a capacity-good `y` outside the subset have
   `c*^T y < c*^T x + δ*`?"
3. If yes: add it as a column, re-solve.
4. If no: `δ*` is certified against the entire family — real counterexample.
5. Report ONLY step 4. Restricted-LP positives are "candidate, pricing
   pending" until the oracle exhausts.
SAT/ILP analogue: constructive answers need the witness re-checked by an
independent evaluator; impossibility answers need a machine-checkable proof
(DRAT/LRAT) replayed by a formally verified checker.

## 6. Verification discipline for a claimed breakthrough (none optional)

1. **Restate the target verbatim** against the primary source — wrong
   quantifier/missing "∀c≥0"/wrong constant invalidates everything. Most
   common self-report failure.
2. **Independent re-derivation** by a second agent from the raw object alone
   (the instance, the routing set), not seeing the first derivation.
3. **Exact arithmetic only** — CAS/PARI/rationals, no floats; exact/rational
   simplex for the LP (float simplex has produced false small-positive gaps).
4. **Exhaustive check when small** — DGG has 2^3=8 routings, enumerate all 8,
   don't trust "the LP found the min."
5. **No-omitted-object proof** (§5) closed, not pending, before "unconditional."
6. **Mechanize when feasible** (Lean/Coq/ACL2) — what separates a proof from a
   plausible transcript.
7. **Publish the full search transcript**, solicit external review — an
   unreviewed transcript is a lead, not a result.
8. **Sensitivity pass** — perturb params (demands ±1, +1 vertex); a structural
   gap persists, a knife-edge coincidence (often a verification bug) doesn't.

## 7. Portfolio: grind vs pivot

- Allocate parallel subagents across: (i) deepen the best-lead construction,
  (ii) stress-test it for §5 false positives, (iii) mine the no-go registry
  for an unexplored corner, (iv) a long-shot structurally-different object.
- **Keep grinding** when the separation margin `δ*` trends UP over refinements
  (restricted problem getting more infeasible), or a no-go lemma just cleared
  a big region.
- **Pivot** when multiple distinct constructions in a family all converge to
  `δ*=0` after exact pricing — evidence the conjecture is TRUE there, itself a
  result (write the no-go/partial-proof up).
- **Kill criterion**: fixed budget/branch with a mandatory no-go write-up on
  expiry. Never let a branch go quiet without depositing negative information.
- **Escalate to "unconditional breakthrough"** only after §6 fully passes.

## 8. DGG end-to-end (case study)

| stage | what happened |
|---|---|
| certificate | convex-hull membership `x∈conv(S(x))` / separation LP, not direct construction |
| object | rank-3 stable-set violation (`z1+z2+z3<=1` broken at 16/15), unequal demands (15,10,15), D=15 |
| first failures | abstract cube/hypercube gadgets — valid combinatorics, but graph realization admitted spliced hybrids that repaired the overload |
| no-go lemmas | equal demands can't work; 3 tracks at exactly D-slack can't force a permutation |
| winner | 7 vertices, 3 terminals, exactly 2 paths each (cheap Z through shared spine, expensive direct E), 6 paths total, no hidden splices |
| numbers | fractional cost 58; each Z-pair overloads a shared arc by exactly 1 past x_a+D; all 8 {Z,E}^3 checked ⇒ every good routing ≥60 ⇒ δ*≥2 |
| false-positive guard | only 6 legal paths by construction ⇒ "no omitted routing" is trivial exhaustive enumeration |

## 9. Certification regimes
Two failure-resistant regimes: (a) exact finite enumeration (DGG, Pythagorean,
cap sets); (b) machine-checked formal proof (AlphaProof, Erdős #1196 in Lean).
Still-risky: (c) pure human peer review of NL argument (unit-distance) — treat
(c) as provisional until formalized or independently re-derived.

## 10. One-page checklist
1 exact statement quoting source · 2 separation LP + dual meaning · 3 the
invariant to violate, parameterize around it · 4 check ambient closure before
trusting an abstract obstruction; prefer designing inside the closed structure
· 5 every dead branch → scoped no-go lemma in the registry · 6 restricted-LP
positive → exact pricing over the whole family before "candidate" · 7
independent re-derivation from the raw object · 8 exact/rational recheck, no
floats · 9 exhaustive brute-force if small · 10 formalize (Lean) or external
review before "solved" · 11 publish the transcript · 12 reallocate compute from
flat-margin branches to growing-margin or freshly-pruned regions.
