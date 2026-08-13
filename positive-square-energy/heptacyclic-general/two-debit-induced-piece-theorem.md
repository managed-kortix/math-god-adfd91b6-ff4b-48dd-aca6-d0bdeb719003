# Two-debit induced-piece theorem

## The theorem

Write

`sigma(H)=s^+(H)-|V(H)|`.

Let `A` be an induced connected attachment-uniform packet with
`sigma(A)>2`. Root the cyclic block-cut incidence tree at `A`. Suppose that,
after all actual bridges have been cut, at most two cyclic demands remain
outside `A`. At each first boundary keep the boundary cut upstream and take
the complete downstream side as one induced territory. Nested demands stay in
the same first-boundary territory unless a later opening is explicitly made.
Then

`sigma(G)>0`.                                                   (1)

Indeed, every complete downstream territory is connected. If it has positive
cyclic rank, its rank is at most six in the applications below, so the complete
lower-rank theorem gives nonnegative credit. If opening its boundary destroys
all cycles, it is a nonempty tree and has credit `-1`. Thus each of the at most
two territories has credit at least `-1`, and induced square-energy
superadditivity gives

`sigma(G)>2-1-1=0`.

This is an induced-piece theorem, not a sum of unspecified theorem margins.
The strictness comes only from the displayed anchor. Every shared cut occurs
only upstream; every connector remnant, rooted branch, and deeper descendant
follows its unique first-boundary territory.

Two refinements will be used without changing (1).

1. Boundary-opening an actual `K4` at any one of its vertices leaves an actual
   `K3`, with its rooted branches, and hence a positive triangular territory.
2. If a structural opening territory owns an external cyclic block, keep the
   complete owner class together. It then has positive rank and nonnegative
   credit, so it replaces rather than supplements the structural tree debit.

## R331

For `R331-S`, retain the actual `K4` block as `A`. The structural rank-three
block `S3` and the cycle `Q` are the two demands. For `R331-K`, retain either
actual `K4`; the other `K4` and `Q` are the two demands. Separate arms produce
two first-boundary territories. If the demands are nested, their complete
first-boundary side is one positive-rank territory. Repeated cuts remain only
in `A`. In every case (1) applies.

This closes both physical `R331` subkeys. No debit or margin is imported from
the structural proof of `S3`; only its actual complete induced side is used.
When the second demand is an actual `K4`, opening it directly exposes the
actual `K3` refinement above.

## R43

Perform the exact physical `S4` opening. It retains one of the established
rank-three anchors `F`: an attached actual `K4` or a favorable
three-triangle packet, with `sigma(F)>2`. Let `R` be the complete opened owner
class, and let the external rank-three block be the actual `K4` selected by the
exact residual sieve.

There are exactly two owner channels in the bridge-free hull.

- If the shared cut lies in `R`, keep the external `K4` with the complete owner
  class. This territory has positive rank and nonnegative credit, while `F`
  has credit greater than two.
- If the shared cut lies in `F`, then `R` is a nonempty tree of credit `-1`.
  Boundary-open the external actual `K4`; its other three vertices induce the
  actual `K3`, so that downstream territory is positive.

Thus the worst exact ledger is `>2-1+0>0`. This closes every physical `R43`
row without charging the coarse `S4` DNN debit.

## R52

Use the exact structural openings from the rank-five theorem fixtures.

For `R52-K22`, the retained six unit edges induce an actual attached `K4` with
credit greater than two. Its complementary owner territory `R` is a nonempty
tree. If `R` owns the theta block, keep the complete class; it has rank two and
nonnegative credit. Otherwise `R` costs one unit and the theta is treated at
its first boundary. The complete theta-minus-cut side is connected and is
either a nonempty tree or unicyclic, so it costs at most one unit. Hence the
worst ledger is `>2-1-1>0`.

For `R52-K71`, the same six retained unit edges induce the actual attached
`K4`. The complementary owner territory `U` is the favorable unicyclic packet
from the exact K71 opening and has positive credit. If `U` owns the theta,
their complete class has positive rank and nonnegative credit. Otherwise the
theta first-boundary side costs at most one unit, and the ledger is
`>2+0-1>0`.

The K22 and K71 statements apply only to the canonical/frontier structural
targets recorded by their theorem fixtures. They do not promote either family
to a DNN owner and do not lengthen an edge of the retained actual `K4`.

## Exact owner contract

The five closed keys are

`R331-S, R331-K, R43, R52-K22, R52-K71`.

For each key the persisted ledger records the anchor, strict credit threshold,
physical complementary owner, external demands, legal owner channels, and
worst territory debits. The verifier also regenerates the four K22 and nine
K71 structural targets from the original theorem fixtures. It checks disjoint
exhaustive synthetic owner territories for separate, repeated-cut, nested, and
opened-owner routes, and rejects a duplicated cut, omitted descendant, changed
debit, widened physical scope, or missing family.

Run

```text
python3 research/rank-seven-two-debit-induced-piece-verifier.py
python3 -O research/rank-seven-two-debit-induced-piece-verifier.py
```

This theorem removes five owner-registry keys. It makes no claim about the ten
other residual packet types or the single-block rank-seven lane.
