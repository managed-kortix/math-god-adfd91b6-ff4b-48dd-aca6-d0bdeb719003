# A marked A8 interface theorem for the rank-nine to rank-ten step

**Date:** 2026-07-26

## 1. Verdict

Write

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5,
delta=sqrt(5)-2<1/4.
```

There is a finite separator theorem strong enough to close the rank-ten
endpoint

```text
P_0 | A_8 | P_1,
```

where the two actual bridge connectors may enter the eight-triangle cluster at
arbitrary shared cuts or private triangle vertices, and may have coincident
entries. The theorem uses the rank-uniform triangle-router transition, the
proved rank-nine packet bounds, and eleven small interface surgeries. It does
not use a nearest-cycle or Voronoi territory assertion.

The finite certificate has the following exact output:

```text
126 unmarked eight-triangle incidence trees,
36414 ordered labelled placements before automorphisms,
11689 canonical marked rows,
11674 accepted by the ordinary router ledger,
15 residual rows.
```

The fifteen rows are nine labelled versions of five two-hub surgeries and six
labelled bouquet orbits. Thus no unhandled nonbouquet kernel appears at eight
triangles. This advances the rank-uniform program from the former unproved
separator Lemma S to a proved finite separator at exactly the interface needed
for rank ten; it does not prove Lemma S at arbitrary rank.

## 2. The marked theorem

An `A_8` cluster is a connected shared-cut cluster consisting of eight
triangles, with arbitrary trees attached at arbitrary vertices. An interface is
the first cyclic-hull point of an actual bridge connector. It is either a
shared cut or a private vertex of one triangle.

**Theorem (marked A8 interface).** Let `A` be an `A_8` cluster with one or two
labelled external pentagonal connectors.

1. With one connector, the complete cactus `A|P` has `sigma>0`.
2. With two connectors, the complete cactus `P_0|A|P_1` has `sigma>0`.
3. The conclusions are uniform over connector lengths, coincident entries, and
   all trees attached to the cluster or connectors.

**Proof of (1).** The complete graph is a connected rank-nine cactus, so the
proved rank-nine theorem applies. In the locked bouquet subcase one also has
the stronger direct estimate `sigma>8-delta`, because the eight triangles all
contain the hub and the established one-hostile-cycle packing-one theorem
applies to the actual joining path.

For (2), project both connectors to their first hull entries. The exhaustive
cycle-leaf insertion recurrence generates the 126 bipartite cycle-cut incidence
trees. Placing the two ordered labels on every cut and every actual private
triangle port gives 36414 placements and 11689 canonical marked rows.

On each row apply only the labelled triangle-router transition. A router with
two owner marks is divided into a singleton and complementary edge; a router
with three marks is divided into three singletons. A later split refines one
previous territory. Every incidence branch, connector remnant, and attached
tree follows its unique mark, so the resulting territories are induced,
disjoint, and exhaustive.

For retained triangular packets use

```text
b(1),...,b(8)=0,1,2,3,2,1,0,0,
sigma(A_r)>b(r) for r<=7, and sigma(A_8)>0.
```

If `c` is the sum of retained integer credits and `e` is the number of naked
private-interface intervals, the ordinary ledger is

```text
sigma(G)>c-e-2delta.
```

It accepts exactly the 11674 rows with `c-e>=1`. The best-score distribution is

| score | 0 | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|---:|
| rows | 15 | 20 | 283 | 1378 | 4817 | 5176 |

Best plans use zero, one, two, and three routers in respectively
`6,10844,838,1` rows. The local transition and its ownership proof are the same
at every rank. The remaining fifteen rows are closed in Sections 3 and 4.
QED.

## 3. The nine nonbouquet residuals

All nine labelled rows have one unmarked incidence shape. A router triangle `R`
contains two cuts `x,y`. Six leaf triangles meet `x`, and one leaf triangle
meets `y`:

```text
             six T petals
                  |
             x -- R -- y -- T
```

The third vertex of `R` is private. Up to exchanging the labels of the two
pentagons, the five marked patterns and repairs are as follows. Splitting `R`
always means its forced three-singleton split, with the `x`, `y`, and private
owners kept distinct.

| marks | final packets | certified surplus |
|---|---|---:|
| both at the private vertex of `R` | `A_6 + T + PP` | `>1` |
| private `R`, and `y` | `A_6 + TP + P` | `>2-2delta` |
| private `R`, and `x` | common-cut `T^6P + T + P` | `>6-2delta` |
| private `R`, and private on the `y` petal | `A_6 + TP + P` | `>2-2delta` |
| private `R`, and private on an `x` petal | packing-one `T^6P + T + P` | `>6-2delta` |

The second through fifth patterns each have two labelled orders, giving
`1+2+2+2+2=9` rows.

These are graph-level surgeries, not only incidence moves. In the first row the
coincident connectors remain together and form the established positive `PP`
packet. In the second and fourth rows the `y` petal stays with its connector and
pentagon, giving the established `TP>1-delta` packet. In the third row all six
`x` petals and the `x`-entered pentagon really contain one cut, so the scalar
common-cut `T^6P` estimate applies. In the fifth row all six triangles contain
`x`; the pentagon joins through one petal's private vertex, so the established
packing-one theorem applies to that actual joining route. This is a direct
packing check, not a Voronoi guard.

## 4. The six bouquet residuals

Now all eight triangles contain one hub `x`. Up to bouquet automorphisms the
ordered interface types are the same six types as for marked `A_7`:

| interfaces | operation | certified surplus |
|---|---|---:|
| hub, hub | open one remote `P`; retain packing-one `A_8+P` | `>7-delta` |
| hub, private, either order | split the entered triangle: `P +` common-cut `T^7P` | `>7-2delta` |
| coincident private vertex | split that triangle: `A_7+PP` | `>0` |
| two private vertices on one triangle | open one remote `P`; retain packing-one `A_8+P` | `>7-delta` |
| private vertices on two triangles | split both: `A_6+P+P` | `>1-2delta` |

The hub/private line gives two labelled rows, hence six rows in total.

For a pentagon opening, retain its connector-side root and put the four private
pentagon vertices, together with every tree rooted there, into one nonempty
induced tree `E`. Then `sigma(E)=-1`. The complementary packet contains all
eight hub triangles, the other pentagon, both connector remnants, and all trees
rooted there. Its triangles have packing number one by direct inspection, so

```text
sigma(H)>8-delta,
sigma(E)+sigma(H)>7-delta>0.
```

This opening is useful in the same-triangle/two-private row, where the naive
three-singleton split would leave only `A_7+P+P> -2delta` and therefore has no
valid sign. The opening is the required small surgery; pretending that a
nearest-cycle territory has packing one would be invalid and is not done.

## 5. Rank-ten induction route

For a connected rank-ten cactus the sharp DNN estimate is

```text
sigma(G)>=9-sum_i epsilon_(ell_i).
```

The same exact comparisons used at rank nine give the rank-ten residual list

```text
T^9Q,  q>=3,
T^8PP.
```

Indeed, at most seven triangles give `7+3epsilon_5<9`; with eight triangles the
only hostile remaining pair is `PP`; and at least nine triangles gives `T^9Q`.

After contracting shared-cut clusters, ordinary leaf/path pruning uses the
rank-nine theorem on the complementary side. The marked theorem above closes
the new two-ended endpoint `P|A_8|P`. The same local router transition also
handles nonlocked one-interface descendants, while a genuinely locked
one-pentagon fan is discharged only by the directly checked common-cut or
packing-one packet.

This does not yet constitute a complete rank-ten proof. A complete proof must
still certify the fully shared `T^8PP` incidences and the corresponding `T^9Q`
locked/nonlocked endpoint list. The important reduction is that no new
two-interface obstruction survives on `A_8`: all failures of the ordinary
ledger are the five two-hub patterns and six bouquet orbits above.

## 6. Validity boundary

The result deliberately avoids three invalid upgrades.

1. It does not claim the all-rank candidate separator Lemma S.
2. It does not infer packing one from nearest-cycle or Voronoi territories.
   Packing one is invoked only for an explicitly displayed common-hub family.
3. It does not split cycles sharing a retained cut between two owners. Locked
   cuts remain one analytic packet, or one pentagon is explicitly opened at
   exact cost `-1`.

The finite counts above are frozen in
`research/decacyclic-t8-two-interface-census.py`, which extends the existing
marked-interface generator to eight triangles and uses `b(8)=0`. Its canonical
row and residual SHA-256 digests are respectively

```text
77468da6a473a52ece68d6e4319f78337feb17941e615e2a0ae65032f826cc86
1f41279dad404a97627da24f1fa67e720f6a0d2ffc67b3c28bf1521ebeb11ca0.
```

The executable checks the census, ordinary interval ownership, exact integer
ledgers, residual shape split `9+6`, and positivity of all fifteen replacement
ledgers. The explicit graph-level realization of each replacement is the audit
in Sections 3 and 4.
