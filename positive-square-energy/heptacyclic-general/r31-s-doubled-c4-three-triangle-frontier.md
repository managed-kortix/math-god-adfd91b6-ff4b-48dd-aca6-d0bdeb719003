# `R31-S`: doubled-`C4` orbit reduction with one open D3 packet

## Exact reduction and present status

Put `sigma(X)=s^+(X)-|V(X)|`.  In the `R31-S` residual all four external
cycles are triangles.  Boundary-open one external triangle leaf `Q_0`; the
cut stays upstream and the opened side is a nonempty induced tree `S`, so
`sigma(S)=-1`.  The retained graph `H` is a doubled-`C4` block plus three
triangular blocks.  The parent row would close if

`sigma(H)>1`.                                                 (1)

The finite orbit and owner transport needed to state (1) uniformly is now
exactly authenticated.  The analytic one-sided packet `D3` is not.  Therefore
`R31-S` remains open and is the final residual in the authoritative
heptacyclic multiblock ledger.

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

## Analytic dispositions

The balanced records are owned by the previously established two-side packet
ledger.  The 28 `C4` records are closed by
`r31-s-c4-marked-four-triangle-theorem.md`, which proves the stronger bound
`sigma(C)>3>2`.

The complementary 28 interior-owner records require

`sigma(D+T^3)>3`,                                              (D3)

where `D=Theta(1,2,2)`, uniformly over the marked rooted incidence and all
rooted trees.  The diagnostic D3 program proves an exact imaginary Sachs
carrier lemma, but does not construct the real Sachs polynomial, prove
`I>=0 => R<0`, track the continuous argument, or establish the required
phase-area integral.  Accordingly (D3), (1), and all of `R31-S` remain open.
No counterexample to (D3) is claimed.

## Verification

Run

```text
python3 research/r31-s-doubled-c4-marked-cut-verifier.py
python3 -O research/r31-s-doubled-c4-marked-cut-verifier.py
python3 research/r31-s-c4-marked-four-triangle-verifier.py
python3 -O research/r31-s-c4-marked-four-triangle-verifier.py
python3 research/r31-s-d3-diamond-packet-verifier.py
python3 -O research/r31-s-d3-diamond-packet-verifier.py
```

The orbit and C4 programs exit zero.  Both D3 invocations deliberately exit
nonzero after printing their exact diagnostic result.  The multiblock master
also exits nonzero while `R31-S:D3` is open.
