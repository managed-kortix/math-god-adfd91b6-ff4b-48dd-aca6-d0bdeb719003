# prompt — rank-uniform cactus separator

## Exact target

Let `sigma(G)=s+(G)-|V(G)|`. Prove that every connected cactus with at
least two cyclic blocks has `sigma(G)>0`.

The sharp cactus DNN theorem reduces the only persistent cycle-multiset
frontiers to

```text
T^r Q,
T^r P P,
```

where `T=C3`, `P=C5`, and `Q` is the single distinguished non-triangular
cycle. Purely triangular cacti are already covered qualitatively by the
maximum-packing territory theorem, including arbitrary trees and arbitrary
rank.

The live obstruction is the shared-cut/marked-interface problem. After
actual-bridge pruning, one obtains a bipartite cycle-cut incidence tree with
triangle nodes, at most two hostile demands, and at most two external
interfaces. The proved local moves are:

1. proper-interval triangle routing;
2. coalescence of two private hostile demands into one `PP` owner;
3. certified pentagon interval routing;
4. stopping at a proved bounded-rank, common-cut, packing-one, or explicit
   ladder terminal.

The finite ledger is `(p,e,c,t,q)` with at most 144 states. The missing claim
is global reachability of an accepting state or certified terminal, with
exactly one final owner for every shared cut, interval, connector remnant, and
attached tree.

## What counts as solving it

A complete solution must provide one of the following.

### Route A — structural proof

A rank-uniform induction proving that every admissible marked incidence tree
reaches one of the certified outcomes, together with:

* a precise deterministic or existential move rule;
* proof that each move preserves connected induced territories;
* proof that every vertex and shared cut has exactly one final owner;
* a complete terminal list with an already proved spectral estimate;
* exact arithmetic showing the final ledger is strictly positive;
* treatment of arbitrary connector lengths and arbitrary attached trees.

### Route B — finite-state proof

A proof that all global information relevant to reachability is captured by a
finite rank-independent boundary state, followed by an exact exhaustive
transition certificate showing every state is winning. The verifier must
regenerate the complete state universe, fail closed under `python -O`, and
print enough canonical data for independent reproduction.

### Route C — counterexample to the separator plus replacement theorem

An exact minimal marked incidence obstruction to the augmented moves, followed
by a new local move or analytic terminal that repairs the obstruction and a
proof that the resulting enlarged system is globally complete. Merely finding
the next obstruction is progress, not victory.

## What does NOT count

None of the following solves the target.

* Proving only rank eleven, or checking finitely many triangular ranks.
* Enumerating unmarked incidence trees while ignoring cut placements,
  interfaces, cyclic order, or final ownership.
* Using qualitative strict positivity to pay a fixed pentagonal deficit or an
  exact tree opening cost `1`.
* Giving one shared cut to two retained induced territories.
* Treating an incidence-tree leaf as though it were separated by an actual
  bridge.
* Declaring every residual object a bounded-rank terminal.
* Assuming a maximum-packing Voronoi partition retains the distinguished
  `Q`-cycle, or applying a mixed-cycle packet estimate after that cycle has
  been split among territories.
* Inferring edge-addition monotonicity.
* Floating-point evidence without an exact certificate.

## Minimal known obstructions to preserve

1. `P-x-T-y-P`, `x!=y`, refutes the original terminal list. It is repaired by
   the established connected `TPP` terminal.
2. Two triangles sharing a cut, with two distinct private pentagon interfaces
   on one triangle, refutes standard distinct-owner routing. It is repaired by
   demand coalescence into `PP+T`.
3. Locked common cuts cannot be separated while retaining both incident
   cycles; they require an analytic locked packet.

Any claimed induction must reproduce these failures and repairs rather than
silently pruning them away.

## Search plan

1. Formalize admissible marked incidence trees and the augmented local moves.
2. Search exact small ranks for the next unavoidable obstruction.
3. In parallel, seek a well-founded induction invariant based on the hostile
   carrier path, branch capacities, and the finite ledger.
4. Alternate proof and breaker agents until the terminal list stabilizes.
5. Only after global completeness is proved, synthesize the DNN reduction,
   bridge pruning, shared-cluster theorem, and separator theorem into
   `all-cacti/paper.tex` and build `paper.pdf`.

No public claim is permitted before independent hostile audits, exact verifier
reproduction, and a clean paper build.
