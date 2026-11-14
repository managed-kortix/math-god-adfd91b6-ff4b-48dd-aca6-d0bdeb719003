# `R31-S`: doubled-`C4` orbit reduction and physical closure

## Exact reduction and present status

Put `sigma(X)=s^+(X)-|V(X)|`.  The finite orbit reduction below remains the
exact input sieve, but its old `D3` interpretation was not physical: the
purported second degree-two diamond vertex has no preimage in the doubled
fibre.  The full parent-graph theorem
`r31-s-physical-shared-triangle-closure.md`, authenticated from adjacency by
`research/r31-s-physical-parent-verifier.py`, now closes the physical `R31-S`
packet via an ordered bridge / connector-fibre / two-triangular-side dispatch.

This is an `R31-S` closure receipt only.  The global multiblock master remains
fail-closed because the generic hull-bridge sentence in the upstream reduction
has not been repaired for every other packet; a rank-one pentagon already
shows why rank `1..6` cannot uniformly be called nonnegative.

## Physical exceptional orbit

Write the six suppressed paths in order `a,A,b,c,C,d`, with doubled fibres
`{a,A}` and `{c,C}` and connectors `{b,d}`.  A bit is the parity of the
physical path.  The old description as one canonical switching class was too
coarse: switching equivalence need not preserve a marked physical owner,
connector, or rooted descendant.

The first-simple structural frontier is exactly the genuine multigraph-
automorphism orbit

```text
010011  010101  011010  011100
100011  100101  101010  101100.
```

It contains four switching-class-`110` rows and four class-`111` rows.  No row
has an odd--odd doubled fibre.  The doubled-`C4` kernel has 16 genuine
`(vertex map, edge map)` automorphism pairs.  Exactly two pairs carry the base
row `010011` to each target row: one preserves the two doubled sides and one
exchanges them globally.

For every witness the audit transports, rather than renames abstractly:

* the full first-simple length vector;
* the even opening connector and odd cut connector;
* all six physical owners (four branch vertices and the two interiors of the
  even doubled paths);
* exact symbolic connector lengths, endpoint orientations, opening/cut
  positions, and both path remnants; and
* every decorated rooted block-cut record, including fresh-child markers and
  fork same/split data.

Thus arbitrary connector lengths are not silently reset to their first-simple
values, and a switching quotient is never used as a graph isomorphism.

## Marked-cut census and recordwise transport

For any physical anchor the legal owner set has six elements.  After
quotienting only by permutations of indistinguishable external triangles and
by reflection of each bare triangle, the three retained block nodes have four
rooted incidence shapes:

| shape | marked records |
|---|---:|
| three direct children | `C(8,3)=56` |
| one length-two chain plus one direct child | `6*6=36` |
| one direct triangle with two children | `6*2=12` |
| one length-three chain | `6` |

Hence there are exactly `110` records.  Classification is performed after the
physical transport on every individual record, not merely by comparing total
counts.  For every one of the eight anchors and both genuine witnesses the
result is

`110 = 54 balanced + 28 C4 + 28 D3`.                          (2)

The side map is required to be one global preserve/swap.  In particular an
abstract owner permutation that preserves the aggregate numbers in (2) but is
not induced by a kernel automorphism is rejected.

## Arbitrary path lengths

The structural orbit applies only while all four doubled members are
first-simple.  If one is lengthened first by two, there are exactly 32 cases
(eight anchors times four members).  Each has exactly one genuine
automorphism to representative row `011010` with the selected member in the
canonical slot:

* even member: full vector `(4,1,1,2,1,2)`, exact bound `1862/1000<2`;
* odd member: full vector `(2,3,1,2,1,2)`, exact bound `1662/1000<2`.

The full vector, not just the parity bit, is checked.  Larger additions by two
on any physical path are covered by the established componentwise
fixed-parity DNN monotonicity.  Connector variables remain exact symbolic
lengths and transport with their endpoint orientation and cut/open position.
This proves the finite all-length scope reduction without importing the
analytic one-sided packet.

## Physical disposition (superseding the synthetic `D3` label)

The balanced/`C4`/`D3` labels in (2) are retained only as historical finite
classifier outputs.  They are not biconnected topologies.  Reconstructing the
actual first-simple parent shows that each doubled side contains one intrinsic
triangle.  After the ordered full-parent dispatch and one deepest boundary
opening, deleting a complete clean even-connector fibre and cutting an actual
odd-connector edge leaves two connected induced shared-cut triangular cacti
of positive ranks `r_0,r_1<=4` with

`r_0+r_1=5`.

The universal shared-cut cluster corollary gives each side credit `>r_i-1`, so
their sum is `>3`.  The boundary-open tree and the connector-fibre tree each
cost exactly one, giving total credit `>1>0`.  If a hull bridge or a cyclic
connector fibre occurs, it is dispatched strictly before this tree ledger.
See the physical theorem note for the proof and exact dependency list.

The standalone diamond diagnostic remains useful only as an audit of a
synthetic graph family.  It is not a premise of, and supplies no obstruction
to, the physical `R31-S` theorem.

## Verification

Run

```text
python3 research/r31-s-doubled-c4-marked-cut-verifier.py
python3 -O research/r31-s-doubled-c4-marked-cut-verifier.py
python3 research/r31-s-physical-parent-verifier.py
python3 -O research/r31-s-physical-parent-verifier.py
```

The first program authenticates the exact finite input orbit and all-length DNN
routes.  The second starts from full physical adjacency, reruns Tarjan blocks,
first-owner fibres and the ordered dispatch, checks all 110 retained incidence
outputs on all eight anchors, and rejects bridge-priority, connector-fibre and
rank-formula mutations.  Neither program launders the synthetic diamond as a
physical side.
