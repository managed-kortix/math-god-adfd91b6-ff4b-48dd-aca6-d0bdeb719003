# `R31-S`: canonical doubled-`C4` plus three retained triangles

## Exact reduction

Put `sigma(X)=s^+(X)-|V(X)|`.  In the `R31-S` residual all four external
cycles are triangles.  The noncanonical doubled-path rows already pass the
rank-seven DNN gate, and the canonical doubled-triangle and one-long all-odd
`K4` rows retain an anchor of credit greater than four.  The only physical
block still requiring a new packet is therefore the canonical doubled-`C4`
class `111`.

Positive connector routes and a triangle owned by an admissible structural
opening close exactly as in the rank-six `S3+T^3` theorem.  In the remaining
bridge-free incidence choose an external triangle leaf `Q_0` and boundary-open
it.  The cut stays upstream; `Q_0` minus that cut, with all descendants rooted
away from the cut, is one nonempty induced tree `S`, so

`sigma(S)=-1`.                                                (1)

The retained induced graph `H` is exactly a canonical doubled-`C4` class
`111` block plus three triangular blocks.  Consequently the exact missing
statement is

`sigma(H)>1`.                                                 (2)

Equation (2), not a packet of threshold three, closes the original row by
`sigma(G)>=sigma(H)+sigma(S)>0`.  This saves two units relative to the coarse
ledger in the preceding nested-packet theorem.

## Marked-cut census

Normalize the doubled sides as in the two-triangle packet.  The legal owner
set for a retained external triangle is

`L={A,B,C,D,x,y}`,                                           (3)

where `x,y` are the internal vertices of the two canonical even doubled
paths.  Owners in the interior of either single connector have already been
removed by the structural-owner branch.  No kernel symmetry may be assumed:
arbitrary connector lengths and rooted branches can mark all six elements of
`L` differently.

After quotienting only by permutations of indistinguishable external triangle
blocks and by the reflection exchanging the two new vertices of a bare
triangle, the three retained block nodes have four rooted incidence shapes.

| shape | marked records |
|---|---:|
| three direct children of the doubled-`C4` | `C(6+3-1,3)=56` |
| one direct child and one length-two triangle chain | `6*6=36` |
| one direct triangle with two children | `6*2=12` |
| one length-three triangle chain | `6` |

The fork factor two records whether its two children use the same fresh vertex
of their parent or the two different fresh vertices.  Thus there are exactly

`56+36+12+6=110`                                             (4)

marked incidence records.  Equality of direct owner cuts is allowed.  A child
placed at its parent's upstream cut is not a nested block-cut record: it is a
repeated direct child at the same cut and is already in an earlier shape.
These 110 records include every repeated-cut and direct/nested configuration.
After opening `d` and cutting `b`, the legal owner sides are
`{A,B,x}` and `{C,D,y}`.  Exactly 54 records split the retained external
triangles `2+1` or `1+2`; the other 56 are one-sided.  Among the latter,
exactly 28 use the interior owner of their side and 28 do not.  Thus the two
last packet types below each represent 28 marked records, not an unspecified
incidence family.

## Structural split and proved records

Write the doubled sides as `a,A':A--B` and `c,C':C--D`, with single
connectors `b:B--C` odd and `d:D--A` even.  Open an internal vertex `v` of
`d`, together with its complete owner class.  In the present residual this is
a nonempty tree `T`, so `sigma(T)=-1`.  Cut one actual edge of `b` and put each
complete descendant class on the side of its owner.  This gives two connected
induced sides whose ranks sum to five.

Every marked record closes by already proved packets unless all three external
triangles land on one side of this split.  Indeed, when the external split is
`2+1`, each side contains its intrinsic `K3`; the established attached packets
with at most three triangular blocks give side credits greater than two and
greater than one.  Their sum is greater than three, so after charging `T` and
`S` the original graph is strict.  The splits `1+2` are symmetric.  Interior
owners with at most two external triangles produce the already proved
`D+T^k`, `k<=2`, packet and satisfy the same ledger.

Thus retaining the actual intrinsic cycles and enumerating marked cuts removes
every balanced record.  It also shows why treating the retained graph as an
unmarked five-triangle cactus loses useful information.

## Exact last obstruction

Only the 56 `3+0` and `0+3` side allocations remain.  Up to exchanging the two
doubled sides they require one of the following root-sensitive inequalities.

1. **Cactus side.**  An intrinsic triangle together with all three external
   triangles forms the marked four-triangle side, while the opposite intrinsic
   triangle is retained as an actual `K3`.  It is enough to prove

   `sigma(C)>2`                                               (C4)

   for the marked four-triangle side with arbitrary rooted trees.  Common-cut
   clusters already satisfy the stronger bound `>3`; the unresolved records
   are precisely the nested packing-three shapes for which the existing
   two-pivot phase lemma gives only `>1`.  This is the 28-record one-sided
   orbit set with no doubled-path interior owner.

2. **Interior-owner side.**  A doubled-path interior owner makes that side an
   attached diamond carrying all three external triangles.  The opposite side
   can be a tree.  It is enough to prove

   `sigma(D+T^3)>3`                                          (D3)

   uniformly over the induced marked roots and arbitrary rooted trees.
   The established favorable packet stops at `D+T^2`, where it gives `>3`;
   it does not imply (D3).  This is the complementary 28-record one-sided
   orbit set containing the doubled-path interior owner.

Either (C4) and (D3), or one coupled inequality proving (2) directly, closes
the canonical doubled-`C4` subclass and hence all of `R31-S`.  The obstruction
is root-sensitive: checking bare cores or coalesced bouquets is insufficient,
and no edge-addition monotonicity or unquantified rank-five surplus may be
substituted.  There is no remaining path-length, connector, owner, or balanced
cut orbit outside these two one-sided packets.

## Verification

Run

```text
python3 research/r31-s-doubled-c4-marked-cut-verifier.py
python3 -O research/r31-s-doubled-c4-marked-cut-verifier.py
```

The verifier regenerates (4), checks the leaf-opening and rank ledgers, and
fails closed unless the residual packet set is exactly `{C4,D3}`.
