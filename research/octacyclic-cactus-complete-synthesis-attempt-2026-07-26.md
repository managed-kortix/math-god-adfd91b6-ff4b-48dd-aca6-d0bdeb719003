# Connected octacyclic cacti: complete synthesis attempt and exact frontier

**Date:** 2026-07-26

## Verdict

For a graph `G`, put

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5.
```

This note records an intermediate synthesis. Its original frontier has since
been closed by the strict-last-bridge `877=861+16` certificate for `(G6PP)`;
see `research/octacyclic-t6p-last-bridge-conservative-resolution-2026-07-26.md` and
the final synthesis `research/octacyclic-cactus-complete-synthesis-2026-07-26.md`.

**Further correction.** The all-rank rooted-guard audit in Section 3 is invalid:
the Voronoi packing-one inference at lines 128--137 does not follow from maximum
packing. The finite six-triangle replacement proves 107 of 111 marked-root
incidence classes and leaves four exact kernels; see
`research/octacyclic-rooted-six-triangle-finite-reduction-2026-07-26.md`.
Consequently every later use of that guard is invalid unless it has a separate
proof. The `T^7|Q` endpoint below does: its locked lobe is a common-cut triangle
bouquet and therefore satisfies the retained packing-one lemma directly. The
fully shared router exceptions and `(G6PP)` also have the separate replacement
proofs cited in the final synthesis.

The sharp-DNN reduction leaves exactly

```text
T^7Q={3,3,3,3,3,3,3,q}, q>=3,   and   T^6PP={3,3,3,3,3,3,5,5}.
```

Every other cycle multiset is proved. The entire `T^7Q` family is proved, and
every fully shared `T^6PP` configuration is proved. At the stage documented by
this note, the remaining class was the disconnected entry-locked class
`(G6PP)`, equivalently the two-root transfer target `(TR6)`, described in
Section 5. The later strict-last-bridge partition certificate closes that graph class
without proving the stronger standalone `(TR6)` inequality.

## 1. Corrected inputs

The synthesis uses the following results with arbitrary finite attached trees:

```text
rank 2 or 3 cactus: sigma>=0,
rank 4 through 7 cactus: sigma>0,
one shared cluster A_r of r triangles:
  sigma(A_r)>0,1,2,3,2,1,0 for r=1,...,7,
P: sigma>=-(sqrt(5)-2),
TP: sigma>1-(sqrt(5)-2),
PP in one shared cluster: sigma>0,
TPP: sigma>3/2.
```

The four-triangle base used in the `A_r` recurrence has been corrected. The
central-triangle/three-petal bare core has spectrum

```text
3, sqrt(3), sqrt(3), 0, -sqrt(3), -sqrt(3), -1, -1, -1
```

and hence `sigma=6`, not `3`. More importantly, the matching-injection phase
argument proves the uniform statement `sigma(A_4)>3` with arbitrary trees.
Successive incidence-leaf openings therefore rigorously give

```text
sigma(A_5)>2, sigma(A_6)>1, sigma(A_7)>0.
```

No retracted multiplicity-blind Sturm increment is used here.

## 2. Exhaustive DNN reduction

If the eight cycle lengths are `l_1,...,l_8`, cactus block counting and the
sharp cactus DNN estimate give

```text
sigma(G)>=7-sum_i epsilon_li,
epsilon_l=0                         for even l,
epsilon_l=l tan^2(pi/(2l))          for odd l.
```

The odd sequence decreases, `epsilon_3=1`, and with
`a=epsilon_5=5-2sqrt(5)` the exact comparisons

```text
3a<2, 2a>1, epsilon_5+epsilon_7<1
```

show the following. At most five triangles give a strict DNN bound; six
triangles fail only for the other two cycles both equal to `P`; and at least
seven triangles give `T^7Q`. Thus the two displayed residual families are
exhaustive and all nonresidual connected octacyclic cacti are proved.

## 3. Exact audit of the `T^7|Q` endpoint

The all-rank Voronoi extension of the rooted guard is retracted, but its
packing-one Lemma 2 remains valid. The disconnected reduction below needs only
that lemma. Its unique interval-locked case is a seven-triangle bouquet entered
at its common cut `x` and bridge-joined to `Q`. Since all seven triangles
contain `x`, no two are vertex-disjoint, so the whole triangular lobe has
packing number one.

Lemma 2 allows an arbitrary joining path and arbitrary attached trees. Its
matching-message/Sachs comparison gives, for hostile `Q=C_q`, `q=1 mod 4`,

```text
D(G)>-2 delta_q,  sigma(G)>7-delta_q>0.
```

Thus this endpoint uses no nearest-cycle partition and no all-rank conclusion.
For even `Q` or `q=3 mod 4`, the separated `Q` territory is nonnegative and
`A_7` is strict positive; `Q=T` is nonhostile as well.

## 4. Disconnected shared-cut graph: complete census reduction

The exact colored cluster-partition census gives:

| residual | all partitions | proper partitions | direct packet rows |
|---|---:|---:|---:|
| `T^7Q` | 45 | 44 | 42 |
| `T^6PP` | 77 | 76 | 70 |

For `T^7Q`, the two structural rows are

```text
Q|T|T|T|T|T|T|T,  Q|T^7.
```

Reduced-tree leaves solve the all-singleton row. Internal-cycle splitting
solves every nonbouquet `T^7|Q` incidence, and a private bouquet entry gives
`A_6+Q>1-delta_q`. The only formerly locked incidence is a seven-triangle
common-cut bouquet entered at its common cut and bridge-joined to `Q`. The
packing-one lemma from Section 3 applies directly to this bouquet. Hence every
disconnected `T^7Q` configuration is proved.

For `T^6PP`, the six structural rows are

```text
P|P|T|T|T|T|T|T,
P|T|T|T|T|T^2P,
P|T|T|T|T^3P,
P|T|T|T^4P,
P|T|T^5P,
P|T^6P.
```

Reduced-tree leaf/path pairing eliminates the first five. The apparently
separate row `P|T^6|P` is positive because

```text
sigma(G)>1-2(sqrt(5)-2)=5-2sqrt(5)>0.
```

Thus only the entry-sensitive part of `T^6P_0|P_1` remains.

## 5. Exact disconnected frontier `(G6PP)`

Let `I` be the cycle-cut incidence tree of the `T^6P_0` cluster and let the
external connector lead to the singleton `P_1`.

If `deg_I(P_0)>=2`, split `P_0` into branch intervals and assign `P_1` to the
entry-owning interval. The mixed branch is `T^rP_1`, while another triangular
branch is strict; all such cases are proved. If `deg_I(P_0)=1` and the external
entry projects to a private vertex of `P_0`, splitting between that vertex and
the unique shared cut gives

```text
A_6+P_1>1-(sqrt(5)-2)>0.
```

The remaining class is exactly

```text
(G6PP): deg_I(P_0)=1, and the connector to P_1 enters at the unique
         P_0 cut or through the triangular incidence component attached there.
```

There are exactly 226 color-preserving abstract incidence trees for a fully
shared `T^6P_0` cluster. Their counts by number of cut nodes are

```text
c=1,2,3,4,5,6: 1,8,33,73,78,33.
```

Exactly 111 have `P_0` as an incidence leaf, with distribution

```text
c=1,2,3,4,5,6: 1,5,20,38,36,11.
```

These 111 are precisely the possible unmarked abstract incidence trees
underlying `(G6PP)`. They are not a count of marked kernels or graph
realizations: the two cyclic-hull roots, cyclic mark positions, connector
length, and arbitrary attached trees remain free. The exact normal form is a
connected six-triangle cactus `A` with ordered cyclic-hull vertices `x,z`
(possibly equal), `P_0` coalesced at `x`, and `P_1` joined to `z` by an
arbitrary path, with arbitrary trees attached everywhere. Equivalently the
unproved statement `(TR6)` is the signed-Coulson bound for every such two-root
kernel and every admissible rooted-tree matching message. This degree-and-entry
normal form, rather than a conjectural short-router picture, is the exact map.

The one-hostile-cycle guard cannot be iterated here: treating one pentagon as
the hostile cycle leaves the other as a cyclic lobe, not an allowed tree, and
opening it costs one while the guard supplies only `1-delta<1`. The common-cut
two-pentagon Schur theorem applies only when both pentagons and all retained
triangles share one pivot. Neither result proves general `(G6PP)`.

## 6. Fully shared configurations and exact frontier

The exact color-preserving incidence-tree census gives the following totals.

For `T^7Q`, counts depend on the incidence capacity of `Q`:

| `Q` capacity regime | counts by cut number `c=1,...,7` | total |
|---|---|---:|
| `q=3` | `1,9,49,142,236,191,60` | 688 |
| `q=4` | `1,9,49,145,243,202,66` | 715 |
| `q=5` | `1,9,49,145,245,205,69` | 723 |
| `q=6` | `1,9,49,145,245,206,70` | 725 |
| `q>=7` | `1,9,49,145,245,206,71` | 726 |

Every nonbouquet type has a safe ordinary cycle split. The unique exception is
the common-cut `T^7Q` bouquet, proved by the exact rooted Schur-Sachs bouquet
inequality. Therefore every fully shared `T^7Q` configuration is proved.

For `T^6PP`, the exact counts are

| | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1 | 14 | 106 | 377 | 728 | 657 | 233 | 2116 |
| ordinary-split safe | 0 | 13 | 104 | 376 | 727 | 657 | 233 | 2110 |
| ordinary-split exceptions | 1 | 1 | 2 | 1 | 1 | 0 | 0 | 6 |

The `c=1` exception is the common-cut `(6,2)` bouquet. The exact rooted
Schur-Sachs inequality proves it with the uniform margin

```text
sigma(T^6PP)>7-4/(3sqrt(13))>6.
```

The five nonbouquet exceptions to the original conservative ledger are:

1. `c=2`: a `(6,1)` hub and a `TP` tail joined through one hub triangle;
2. `c=3`: a `(5,1)` hub, a `TP` tail, and a binary `TT` petal routed by one
   saturated triangle;
3. `c=3`: a six-triangle hub with two `TP` tails on distinct hub triangles;
4. `c=4`: a five-triangle hub, with one router carrying a `TP` tail and a
   binary `TT` petal and another router carrying the second `TP` tail;
5. `c=5`: a four-triangle hub with two symmetric saturated-router arms, each
   carrying one `TP` tail and one binary `TT` petal.

They are color-preserving incidence types, not five graph realizations. Cyclic
mark orders and arbitrary attached trees are not enumerated. Every type has
both pentagons as incidence leaves. No ledger exception exists with an internal
pentagon or with six or seven cut nodes.

All five are nevertheless proved without the rooted hostile-cycle guard
theorem. Successive proper interval splits of the displayed router triangles
give the following exact induced packetizations:

```text
U2: P + common-cut T^5P,       surplus >5-2delta;
U3: P + T + common-cut T^4P,   surplus >4-2delta;
U4: P + P + A_4,               surplus >3-2delta;
U5: P + P + T + A_3,           surplus >2-2delta;
U6: P + P + T + T + A_2,       surplus >1-2delta.
```

Here `delta=sqrt(5)-2`, `sigma(P)>=-delta`, `sigma(A_r)>r-1` for
`1<=r<=4`, and the common-cut theorem gives `sigma(T^kP)>k-delta`.
Degree-two routers split into a singleton marked vertex and a complementary
edge; saturated degree-three routers split into three singleton marked
vertices. Thus every operation is valid for every cyclic order and arbitrary
attached trees. Since `1-2delta=5-2sqrt(5)>0`, all five router types close.
Together with the common-cut bouquet bound, all 2116 fully shared `T^6PP`
incidence types are proved, and the fully shared configuration set is empty.

## 7. Structural and census conclusion

The current proof covers:

```text
all nonresidual cycle multisets;
all T^7Q, disconnected or fully shared;
all disconnected T^6PP except (G6PP);
all fully shared T^6PP.
```

At the stage of this note, the remaining frontier was one infinite entry-locked
disconnected class, supported on 111 unmarked abstract `T^6P` incidence trees
and finitely many marked cyclic kernels, with arbitrary connector length and
rooted-tree messages. There was no remaining fully shared type. The later
strict-last-bridge census resolves all 877 graph classes as `861+16` by
conservative one-router and verified two-router partitions, so this is no
longer a frontier for the octacyclic theorem; only the
stronger standalone two-root inequality `(TR6)` remains unproved.

The direct two-root inequality `(TR6)` is not supplied by the qualitative
heptacyclic theorem, the one-cycle rooted guard, or the common-cut bouquet
theorem. It is also unnecessary for the octacyclic theorem: the later
strict-last-bridge decomposition closes all marked graph classes with
common-cut/shared-cut packets and at most two router splits.

## Reproduction

Run:

```bash
python research/octacyclic-disconnected-partition-census.py
python research/octacyclic-fully-shared-incidence-census.py
```

The partition and incidence censuses use exact integer or `Fraction`
arithmetic. The two-pentagon common-cut polynomial certificate is recorded in
`positive-square-energy/experiments/c5_bouquet_matching_certificate.py`; it
requires SymPy to rerun.
