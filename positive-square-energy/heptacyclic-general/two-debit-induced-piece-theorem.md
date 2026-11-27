# Two-debit induced-piece packet template

## Exact scope and corrected credit rule

Write

`sigma(H)=s^+(H)-|V(H)|`.

Let `A` be an induced connected attachment-uniform packet with
`sigma(A)>2`. This note concerns only a registered **bridge-free or
post-dispatch packet** after every actual bridge excluded by the packet
manifest has been handled separately. Root that packet's cyclic block-cut
incidence tree at `A`. Suppose at most two registered cyclic demands remain
outside `A`. At each first boundary keep the boundary cut upstream and take
the complete downstream side as one induced territory. Nested demands stay in
the same first-boundary territory unless a later opening is explicitly made.

For such a packet, the arithmetic conclusion `sigma>0` follows only after each
complete territory has an authenticated credit of at least `-1` and the owner
classes form an induced, disjoint, exhaustive partition of the packet. A
positive downstream territory is nonnegative when its connected rank lies in
`{2,3,4,5,6}`, or when a separately cited typed rank-one theorem applies. An
arbitrary rank-one territory is **not** nonnegative: for example,
`sigma(C5)=2-sqrt(5)<0`. Without exact rank-one typing, only the universal
floor `sigma>=-1` may be used. A nonempty tree has credit exactly `-1`.
Consequently, once those packet-specific hypotheses have been verified,
induced square-energy superadditivity gives

`sigma(packet)>2-1-1=0`.                                    (1)

This is a conditional packet template, not a theorem about the original
physical graph before bridge dispatch. The strictness comes only from the
displayed anchor. Every shared cut in the packet occurs only upstream; every
connector remnant, rooted branch, and deeper descendant represented by the
packet manifest must follow its unique first-boundary territory.

Two refinements will be used without changing (1).

1. Boundary-opening an actual `K4` at any one of its vertices leaves an actual
   `K3`, with its rooted branches, and hence a positive triangular territory.
2. If a structural opening territory owns an external cyclic block, keep the
   complete owner class together. Ownership alone does **not** make its credit
   nonnegative. Use nonnegative credit only after reconstructing connected rank
   in `{2,3,4,5,6}` or invoking a separately cited typed rank-one theorem;
   otherwise charge the universal floor `-1`. The complete class replaces,
   rather than supplements, the structural tree debit only with that
   packet-specific typed charge.

## R331 packet rows

For the registered **bridge-free/post-dispatch** `R331-S` packet, retain the
actual `K4` block as `A`. The structural rank-three block `S3` and the cycle
`Q` are the two demands. For the corresponding registered `R331-K` packet,
retain either actual `K4`; the other `K4` and `Q` are the two demands. Separate
arms produce two first-boundary territories. If the demands are nested, their
complete first-boundary side is one territory whose exact rank must be typed.
Repeated cuts remain only in `A`. Subject to those manifest checks, (1) applies
to the post-dispatch packet.

This closes only the registered bridge-free/post-dispatch R331 packet; no
full-physical closure is asserted here. In particular, the complete physical
`R331-K` inventory is handled independently by
`r331-k-adjacency-ownership-note.md`, whose dedicated owner proof types the
rank-one side as a literal triangle-with-trees. No debit or margin is imported
from the structural proof of `S3`. When the second demand is an actual `K4`,
opening it directly exposes the actual `K3` refinement above.

## R43

Perform the exact physical `S4` opening. It retains one of the established
rank-three anchors `F`: an attached actual `K4` or a favorable
three-triangle packet, with `sigma(F)>2`. Let `R` be the complete opened owner
class, and let the external rank-three block be the actual `K4` selected by the
exact residual sieve.

There are exactly two owner channels in the bridge-free hull.

- If the shared cut lies in `R`, keep the external `K4` with the complete owner
  class. The opened `S4` complement is a tree, so this connected territory has
  rank exactly three and therefore nonnegative credit by the completed
  tricyclic theorem, while `F` has credit greater than two.
- If the shared cut lies in `F`, then `R` is a nonempty tree of credit `-1`.
  Boundary-open the external actual `K4`; its other three vertices induce the
  actual `K3`, so that downstream territory is positive.

Thus the worst exact ledger is `>2-1+0>0`. This closes only the registered
bridge-free/post-dispatch `R43` packet row, without charging the coarse `S4`
DNN debit. It does not own omitted actual-bridge complements.

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
their complete class is connected of rank exactly three and hence has
nonnegative credit by the completed tricyclic theorem. Otherwise the theta
first-boundary side costs at most one unit, and the ledger is
`>2+0-1>0`.

The K22 and K71 statements apply only to the canonical/frontier structural
targets recorded by their theorem fixtures. They do not promote either family
to a DNN owner and do not lengthen an edge of the retained actual `K4`.

## Exact packet contract

The five registered post-dispatch packet keys are

`R331-S, R331-K, R43, R52-K22, R52-K71`.

For each key the persisted ledger records the anchor, strict credit threshold,
packet complementary owner, external demands, legal owner channels, and worst
territory debits. The verifier also regenerates the four K22 and nine K71
structural targets from the original theorem fixtures. It checks disjoint
exhaustive synthetic owner territories for separate, repeated-cut, nested, and
opened-owner routes, and rejects a duplicated cut, omitted descendant, changed
debit, widened packet scope, or missing family. It does not reconstruct or
own every component removed by an actual-bridge dispatch.

Run

```text
python3 research/rank-seven-two-debit-induced-piece-verifier.py
python3 -O research/rank-seven-two-debit-induced-piece-verifier.py
```

This template discharges five registered bridge-free/post-dispatch packet
rows, subject to their typed manifests. It makes no claim about their omitted
actual-bridge complements, the ten other residual packet types, the complete
multiblock problem, or the single-block rank-seven lane.
