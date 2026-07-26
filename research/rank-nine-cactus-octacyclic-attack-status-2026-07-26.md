# Rank-nine connected cacti: octacyclic reduction and exact current obstacle

**Date:** 2026-07-26

## 1. Status and validity boundary

Write

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5,
delta=sqrt(5)-2<1/4.
```

This note attacks connected cacti of cyclomatic rank nine using the proved
octacyclic cactus theorem. It does **not** claim the rank-nine theorem. The
sharp-DNN reduction, the disconnected color-partition census, and the fully
shared abstract incidence censuses are complete. Every `T^8Q` residual is
closed. The `T^7PP` residual is reduced to three explicit two-interface
families, described in Sections 4 and 6.

The executable structural certificate is

```bash
python research/rank-nine-cactus-residual-census.py
```

It uses exact integer and `Fraction` arithmetic. As in the octacyclic census,
the fully shared computation enumerates colored incidence trees, not cyclic
mark orders or arbitrary attached trees. The positive replacement splits below
are therefore justified separately; the three remaining families are not
declared counterexamples.

## 2. Exact DNN residuals

For rank `r`, the sharp cactus DNN estimate is

```text
sigma(G) >= r-1-sum_i epsilon_(ell_i),
epsilon_ell=0                         for even ell,
epsilon_ell=ell tan^2(pi/(2ell))      for odd ell.
```

The proved all-rank residual classification applies with `r=9`. Consequently
the only multisets not made strictly positive by DNN are

```text
T^8Q={3,3,3,3,3,3,3,3,q},  q>=3,
T^7PP={3,3,3,3,3,3,3,5,5}.
```

Thus every other connected rank-nine cactus is proved by DNN alone. This step
uses no incidence census.

The packet inputs inherited from the octacyclic proof include strict
positivity for every connected cactus of ranks four through eight,
nonnegativity in ranks two and three, and

```text
sigma(P)>=-delta,
sigma(Q)>=-delta_q,  delta_q=sec(pi/q)-1<1 for hostile Q,
sigma(TQ)>0,  sigma(TP)>1-delta,
sigma(A_k)>b_k,
(b_1,...,b_7)=(0,1,2,3,2,1,0).
```

Here `A_k` is one connected shared-cut cluster of `k` triangles. The
octacyclic theorem gives `sigma(A_8)>0`, but no graph-independent positive
constant. That distinction creates the new boundary.

## 3. Disconnected shared-cut graph: exact color reduction

Contract shared-cut clusters and retain the actual bridge connections. The
reduced cluster graph is a tree, and every separation below cuts actual bridge
edges. Connector remnants and hanging trees stay with one endpoint territory.

The exact color-partition census gives

| residual | all partitions | proper partitions | direct packet rows | structural rows |
|---|---:|---:|---:|---:|
| `T^8Q` | 67 | 66 | 63 | 3 |
| `T^7PP` | 118 | 117 | 109 | 8 |

The three `T^8Q` rows are

```text
Q|T|T|T|T|T|T|T|T,
Q|T^7|T,
Q|T^8.
```

The eight `T^7PP` rows are

```text
P|P|T|T|T|T|T|T|T,
P|P|T^7,
P|T|T|T|T|T|T^2P,
P|T|T|T|T|T^3P,
P|T|T|T|T^4P,
P|T|T|T^5P,
P|T|T^6P,
P|T^7P.
```

Reduced-tree leaf and path pruning closes every row containing a singleton
triangle. A singleton-triangle leaf gives a strict triangle and a strict
octacyclic complement. If no singleton triangle is a leaf, the distinguished
end clusters are the reduced tree's leaves; the singleton triangle nearest a
pentagon or `Q` forms a positive `TP` or `TQ` terminal packet, leaving a strict
lower-rank complement. Hence only

```text
T^8|Q,
P_0|T^7|P_1,
T^7P_0|P_1                                             (3.1)
```

survive the color/topology reduction.

## 4. Disconnected residuals

### 4.1 `T^8|Q` is proved

Let `I` be the incidence tree of the eight-triangle cluster and mark the first
cyclic-hull entry of the connector to `Q`. If `I` is not a bouquet, split an
internal triangle into proper intervals at its incidence marks and at the
private entry mark when present. If the `Q` territory retains `k` triangles,
then `k=1` is a positive `TQ` packet, `k=2` is nonnegative with another strict
triangular branch, and `3<=k<=7` is strict by the rank-four-through-eight
theorems. If `k=0`, the entry uses one of the router's at most three marks, so
the other seven triangles occupy at most two branches. One branch has at least
four triangles and surplus `>3`, which absorbs `Q>-1`.

If the cluster is a bouquet, its eight triangles have vertex-packing number
one, regardless of whether the connector enters at the common cut or at a
private bouquet vertex. The established packing-one hostile-cycle lemma applies
directly to the whole cactus and gives

```text
sigma(G)>8-delta_q>0
```

for hostile `Q`; nonhostile `Q` closes by the bridge partition. Thus every
disconnected `T^8Q` cactus is proved. No all-rank Voronoi guard is used.

### 4.2 The two disconnected `T^7PP` kernels

The middle-cluster row

```text
P_0 | A_7 | P_1                                      (D9a)
```

has only the additive ledger

```text
sigma(G)>0-2delta,
```

which has no valid sign. Unlike the octacyclic row `P|A_6|P`, the available
triangle reserve has dropped from `sigma(A_6)>1` to only `sigma(A_7)>0`.
The two connector entries are independently marked and may coincide at a cut,
lie on private triangle vertices, or pass through arbitrary rooted trees.

For `T^7P_0|P_1`, splitting an internal `P_0`, or an incidence-leaf `P_0`
entered at a private vertex, works exactly as in the octacyclic reduction, now
with the octacyclic theorem available on retained sides. What remains is

```text
deg_I(P_0)=1, and the connector to P_1 enters at the unique P_0 cut or
through the triangular component incident with that cut.              (D9b)
```

This is the rank-nine analogue of the octacyclic marked-entry family `G6PP`,
but with seven triangles. The old `877=861+16` certificate is specific to six
triangles and does not imply this case. In particular, invoking the qualitative
octacyclic theorem on the marked `T^7P_0` side and adding `P_1>=-delta` would be
invalid.

No proof of `(D9a)` or `(D9b)` is asserted here.

## 5. Fully shared `T^8Q`

The exact color-preserving incidence counts by cut number are

| `Q` capacity | `c=1,...,8` | total |
|---|---|---:|
| `q=3` | `1,11,68,253,572,742,493,127` | 2267 |
| `q=4` | `1,11,68,258,586,774,525,142` | 2365 |
| `q=5` | `1,11,68,258,589,781,536,148` | 2392 |
| `q=6` | `1,11,68,258,589,783,539,151` | 2400 |
| `q=7` | `1,11,68,258,589,783,540,152` | 2402 |
| `q>=8` | `1,11,68,258,589,783,540,153` | 2403 |

The conservative ordinary one-cycle split ledger resolves every type except
the common-cut bouquet in every regime, and the following second type for
hostile odd `Q` (also retained by the conservative uniform `q>=8` regime):

1. the common-cut `T^8Q` bouquet;
2. seven triangles and one router triangle form a common-cut triangular
   bouquet, with `Q` attached at the router's second cut.

Both are packing-one triangular packets: all eight triangles contain the same
hub cut. The packing-one hostile-cycle lemma permits either direct contact or
an arbitrary joining path to `Q`, and arbitrary attached trees. It gives
`sigma>8-delta_q>0` in both cases. Therefore every fully shared `T^8Q`
configuration is proved.

## 6. Fully shared `T^7PP`: exact dichotomy

The exact census contains 8004 incidence types:

| | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | `c=8` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1 | 17 | 150 | 699 | 1856 | 2714 | 1998 | 569 | 8004 |
| ordinary-split safe | 0 | 15 | 148 | 698 | 1855 | 2714 | 1998 | 569 | 7997 |
| exceptions | 1 | 2 | 2 | 1 | 1 | 0 | 0 | 0 | 7 |

The seven exceptions split into an exact structural dichotomy.

First, six are the octacyclic `U1--U6` bouquet/router patterns with one extra
hub triangle. They close by the same legal successive interval operations:

| type | replacement packetization | certified surplus |
|---|---|---:|
| common-cut bouquet | common-cut `T^7PP` | `>8-4/(3sqrt(13))` |
| one binary triangle router | `P +` common-cut `T^6P` | `>6-2delta` |
| one saturated triangle router | `P + T +` common-cut `T^5P` | `>5-2delta` |
| two binary triangle routers | `P + P + A_5` | `>2-2delta` |
| saturated then binary routers | `P + P + T + A_4` | `>3-2delta` |
| two saturated triangle routers | `P + P + T + T + A_3` | `>2-2delta` |

Every displayed value is positive. The router intervals and cut ownership are
the same local operations checked in the octacyclic `U1--U6` audit; the extra
triangle remains in the common hub packet. Thus these six types scale without
a new analytic estimate.

Second, one genuinely new type remains:

```text
seven triangles and P_0 share a hub x;
P_0 has a second cyclic cut y, shared with the leaf pentagon P_1.       (F9)
```

Equivalently, `P_0` is a two-mark pentagon router between a common-cut
`T^7P_0` bouquet and `P_1`. Splitting `P_0` at `x,y` produces only

```text
A_7 + P_1,
```

whose available ledger is `>0-delta`, not positive. The common-cut
`T^kPP` theorem does not apply because `P_1` does not contain `x`; the
packing-one hostile-cycle lemma does not apply because there are two hostile
pentagons; and the octacyclic theorem supplies no uniform margin on the marked
`T^7P_0` side. No proof of `(F9)` is asserted here.

## 7. Exact new marked-interface obstacle

The three open families `(D9a)`, `(D9b)`, and `(F9)` have one common feature:
an octacyclic triangular/mixed core must control **two marked pentagonal
interfaces**. One-interface octacyclic tools scale:

```text
one hostile Q + packing-one triangles,
one common Schur pivot,
one marked remote pentagon after a six-triangle finite census.
```

They do not presently provide a two-interface inequality. Destroying the
interface router leaves `A_7`, whose certified reserve is only qualitative;
retaining the router creates a two-pivot Schur complement, outside the scalar
common-cut theorem. This is the exact new obstruction, rather than an
unclassified mass of rank-nine incidences.

A sufficient next theorem would be a two-root packet estimate covering an
`A_7` cluster with two labelled pentagonal arms, including coincident roots and
an arm entering through an incidence-leaf pentagon. A matrix-valued rooted
Schur-Sachs inequality or an exact marked-interface census with replacement
packetizations could supply it. The octacyclic `877=861+16` method is evidence
that a finite marked census may work for `(D9b)`, but it gives neither a proof
nor a size-independent scaling theorem.

## 8. Current verdict

Proved in this attack:

1. the exact rank-nine DNN residuals `T^8Q` and `T^7PP`;
2. every nonresidual connected rank-nine cactus;
3. every disconnected and fully shared `T^8Q` cactus;
4. 109 direct disconnected `T^7PP` color rows and all six singleton-triangle
   structural rows;
5. 7997 of 8004 fully shared `T^7PP` incidence types by ordinary splitting;
6. six of the seven remaining fully shared types by scaled octacyclic router
   packetizations.

Not proved:

```text
(D9a)  P|A_7|P with two arbitrary marked bridge interfaces,
(D9b)  entry-locked T^7P|P,
(F9)   the two-pivot pentagon-router T^7PP cluster.
```

Accordingly, the octacyclic packet architecture scales through all `T^8Q` and
through all but these exact two-interface `T^7PP` kernels. The theorem
`s+(G)>|V(G)|` for every connected rank-nine cactus is not claimed.
