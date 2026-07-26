# Connected octacyclic cacti: exact structural status

**Date:** 2026-07-26

**Later analytic update.** The fully shared common-cut bouquets `(F7Q)` and
the common-cut `T^6PP` bouquet are now proved, with arbitrary attached trees,
by the exact rooted Schur-Sachs inequality in
`research/common-cut-bouquet-rooted-schur-2026-07-26.md`. Its quantitative
bounds are `sigma(T^7Q)>7-delta_q>6` in the hostile case (and `>7`
otherwise), and `sigma(T^6PP)>7-4/(3sqrt(13))>6`. Statements below that list
these two bouquets as open describe the status before that update. The rooted
guard theorem in `research/rooted-hostile-cycle-guard-absorption-2026-07-26.md`
also proves every bridge-separated `T^7|Q` case. The two-pentagon endpoint and
short-router problems remain open.

## 1. Scope and verdict

Write

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5.
```

This note attacks every connected octacyclic cactus using the proved
heptacyclic theorem and the induced-territory machinery from the heptacyclic
paper. It is deliberately a status note, not a completed octacyclic theorem.

The exact sharp-DNN residuals are derived independently below. They are

```text
T^7 Q = {3,3,3,3,3,3,3,q},  q>=3,
T^6 PP = {3,3,3,3,3,3,5,5}.
```

All nonresidual cycle multisets are proved. Large structural portions of both
residual families are also proved without an incidence census:

- every disconnected `T^7Q` configuration;
- every disconnected `T^6PP` configuration except the exact entry-locked
  leaf-pentagon class (G6PP) inside `T^6P|P`;
- every fully shared `T^7Q` configuration, using the later rooted Schur-Sachs
  theorem for the eight-cycle bouquet;
- every fully shared `T^6PP` configuration with an internal pentagon;
- every fully shared `T^6PP` configuration with both pentagons as leaves and a
  safe internal-triangle split, together with the common-cut bouquet by the
  later rooted Schur-Sachs theorem.

The remaining obstruction set is structural, not enumerative. The fully shared
`T^6PP` ordinary-split census has five nonbouquet router types still requiring
a quantitative or nonadditive argument. In the
disconnected case the sole remaining locked-entry class is (G6PP) of
`research/octacyclic-disconnected-exact-reduction-2026-07-26.md`, stated by an
exact incidence degree and entry condition and not reduced to a conjectural
short-router list. The rooted guard theorem closes the former (G7Q) endpoint.
The present two-pentagon packet bounds do not close (G6PP).
In particular, the proved heptacyclic theorem is qualitative and cannot pay a
tree-opening cost or a pentagon deficit.

No complete octacyclic theorem is claimed.

## 2. Inputs

For a connected cactus with at most seven cyclic blocks, use the established
bounds

```text
rank 2 or 3: sigma>=0,
rank 4, 5, 6, or 7: sigma>0.
```

The rank-seven statement is the heptacyclic theorem. All these statements
allow arbitrary bridge connectors and arbitrary trees attached at arbitrary
vertices.

For one shared-cut cluster of `r` triangles, write `A_r`. The proved
leaf-opening recurrence gives

| `r` | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| certified `b_r` in `sigma(A_r)>b_r` | 0 | 1 | 2 | 3 | 2 | 1 | 0 |

We also use

```text
sigma(P)>=-delta,             delta=sqrt(5)-2<1/4,
sigma(TQ)>1-delta_q>0         for a hostile Q=C_q,
sigma(TP)>1-delta>0,
sigma(PP)>0                   in one shared-cut cluster,
sigma(TPP)>3/2.
```

Here `delta_q=sec(pi/q)-1<1` when `q=1 mod 4`; a nonhostile unicyclic
territory is nonnegative. Every split below is a vertex partition into induced
territories. Reduced-cluster cuts occur on actual bridges, and a split cycle is
distributed into proper consecutive path intervals, one owner per mark.

## 3. Independent sharp-DNN residual derivation

Let the eight cyclic blocks have lengths `l_1,...,l_8`, and let `b` be the
number of bridge blocks. Since an octacyclic connected graph has `m=n+7`,

```text
b+sum_i l_i=n+7.
```

Put

```text
epsilon_l=0                              if l is even,
epsilon_l=l tan^2(pi/(2l))               if l is odd.
```

The sharp cactus DNN theorem gives

```text
s-(G)<=n+7+sum_i epsilon_li,
sigma(G)>=7-sum_i epsilon_li.                         (3.1)
```

The odd sequence is decreasing. Set

```text
a=epsilon_5=5-2sqrt(5).
```

The exact comparisons needed here are

```text
3a<2,
2a>1,
epsilon_5+epsilon_7<1.
```

The first and second are respectively certified by `169<180` and `80<81`;
the last is the exact comparison already proved in the heptacyclic residual
classification.

Let `t` be the number of triangles.

- If `t<=5`, then `sum epsilon<=5+3a<7`.
- If `t=6`, the two remaining cycles contribute at least the missing one only
  when both are pentagons. Indeed, an even length contributes zero, while every
  other odd pair is bounded by `epsilon_5+epsilon_7<1`; for `P,P`, `2a>1`.
- If `t>=7`, the multiset is `T^7Q`, including `Q=T` when `t=8`, and its
  epsilon sum is `7+epsilon_q>=7`.

Therefore (3.1) is strictly positive outside exactly `T^7Q` and `T^6PP`.
This classification is complete and uses no graph census.

## 4. Disconnected shared-cut graph: `T^7Q`

Assume the shared-cut graph is disconnected. The reduced cluster tree has two
marked leaves, and at most one contains the designated block `Q`. Hence there
is a `Q`-free all-triangle leaf cluster `A_r`, `1<=r<=7`. Cutting its first
actual bridge gives `A_r` and a connected `(8-r)`-cyclic complement.

The heptacyclic theorem closes `r=1`; the lower-rank theorems and the table of
`b_r` close `2<=r<=6`. Explicitly, the complementary ranks are `7,6,5,4,3,2`,
and every row has a strict triangular term or a strict lower-rank term.

For `r=7`, the complement is the unicyclic `Q`. The coarse ledger

```text
A_7+Q > 0-delta_q
```

is not validly positive. This is the first genuinely new rank-eight issue.

An exact internal-incidence argument now closes every nonbouquet `A_7|Q`
cluster. A nonbouquet triangle incidence tree has an internal triangle. Split
it at its cyclic marks, adding a private external entry as a mark when needed.
If the `Q` territory retains at least one triangle, the heptacyclic and
lower-rank packet bounds close the split, with another strict triangular branch
in the sole weak tricyclic case. If it retains none, the entry consumes one of
the triangle's at most three marks, so the other six triangles occupy at most
two branches; one has at least three triangles and surplus `>2`, absorbing
`Q>=-delta_q`. If no triangle is internal, all triangle nodes are leaves and
the incidence tree has one cut node, so the cluster is a bouquet. A private
entry on one bouquet triangle gives a two-mark split and the positive ledger
`A_6+Q>1-delta_q`. Thus the exact obstruction is:

```text
seven triangles form one common-cut bouquet at x,
and the connector to Q enters that bouquet at x.                 (D7Q)
```

The connector may have arbitrary positive length and arbitrary attached trees.
Abstractly this is an `A_7|Q` bridge-bouquet, not a fully shared bouquet.
Opening `Q` costs one and leaves only the qualitative margin `A_7>0`; opening
triangles makes the ledger worse. Thus (D7Q) is a real gap in the additive
packet method, not an omitted easy leaf case. The later rooted hostile-cycle
guard theorem closes it uniformly over the connector and attached trees. All
`A_7|Q` incidences are therefore proved.

## 5. Disconnected shared-cut graph: `T^6PP`

If a reduced-tree leaf cluster contains only triangles, cut it off. Its size is
at most six, and the triangle-margin table together with the rank-seven and
lower-rank theorems gives a positive total in every row.

Suppose no such leaf exists. Since there are only two pentagons, the reduced
cluster tree is a path and its two endpoint clusters contain the two distinct
pentagons. If an endpoint cluster contains `1<=r<=5` triangles, cut it off whole.
For `r=1` it is a positive `TP` packet; for `r=2` it is a nonnegative
tricyclic packet and the complement has rank five and is strict; for `r>=3`
the endpoint packet is itself strict. Thus every such row closes. The value
`r=6` leaves a singleton pentagon and cannot be paid by qualitative strictness.

If both endpoint clusters are singleton pentagons and there are at least two
intervening triangle clusters, take one endpoint pentagon together with the
nearest triangle cluster as one terminal territory. The same `T^rP` ledger,
together with the nonempty remainder, closes the row. An exact colored
partition census, followed by the same reduced-tree leaf/path argument, leaves
only one concentrated row:

```text
T^6P | P.                                                (D6PP)
```

The exact census has 77 colored partitions, 76 proper partitions, 70 direct
rows, and six ledger exceptions; five exceptions are discharged by the
reduced-tree argument. In `T^6P|P`, splitting the clustered pentagon closes
every case in which it is internal. If it is an incidence leaf and the entry is
private on that pentagon, a two-mark split gives `A_6+P>1-delta>0`. The exact
unresolved class has pentagon incidence degree one and entry at its unique cut
or through the triangular component at that cut.

The former second row is now closed directly. Cutting the two bridge interfaces
gives `A_6+P+P`, with total surplus
`>1-2(sqrt(5)-2)=5-2sqrt(5)>0`. Thus `P|T^6|P` is not an octacyclic gap.

## 6. One fully shared `T^7Q` cluster

Let `I` be the cycle-cut incidence tree and inspect `Q`.

If `deg_I(Q)>=2`, split `Q` into one proper interval per component of `I-Q`.
The branch sizes `r_j` are positive and sum to seven. Since there are at least
two branches, every `r_j<=6`; hence every resulting `A_(r_j)` packet is strict
with nonnegative certified margin. The total is positive.

Suppose `Q` is an incidence leaf. If some triangle `C` is internal, split `C`.
If the `Q` branch contains `k>=1` other triangles, it is a `T^kQ` packet: it is
positive for `k=1`, nonnegative for `k=2`, and strict by the lower-rank theorems
for `3<=k<=5`; another all-triangle branch is strict. If the `Q` branch has
`k=0`, the other six triangles occupy at most two branches and one has size at
least three, hence certified margin greater than one, absorbing the hostile
bound `-delta_q`.

If no triangle is internal and `Q` is also a leaf, every cycle node of `I` is a
leaf. A bipartite incidence tree with every cycle node a leaf has only one cut
node. Thus all eight cycles share one cut vertex. The exact remaining case is

```text
the fully shared eight-cycle T^7Q bouquet.                (F7Q)
```

Opening the leaf `Q` leaves `A_7` but gives only `>0-1`; unlike rank seven,
the triangle recurrence has no unit of spare margin. Hence (F7Q) is not proved
by the heptacyclic leaf-or-split argument.

## 7. One fully shared `T^6PP` cluster

If a pentagon `P_0` is internal, split it. Let `B` be the branch containing the
other pentagon and let `a` be its triangle count.

- For `a>=1`, the mixed branch is positive for `a=1`, nonnegative for `a=2`,
  and strict for `3<=a<=5`; another all-triangle branch is strict.
- For `a=0`, the singleton pentagon costs at most `delta`. The six triangles
  occupy at most four other branches, so one branch contains at least two
  triangles and contributes more than one. Thus the total is
  `>1-delta>0`.

Therefore every internal-pentagon configuration, including every saturated
pentagon hub, is proved.

It remains to take both pentagons as incidence leaves. If an internal triangle
has both pentagons in one branch, its other branch is a strict all-triangle
packet and the mixed branch is a connected cactus of rank at most seven, so the
split is positive. If the pentagons lie in distinct branches and each side
contains a retained triangle, the two mixed packets are nonnegative/positive,
with strictness supplied by one mixed packet or a third triangular branch. A
three-way isolated-`P` case with a singleton triangular third branch is repaired
by merging those adjacent marks into a `TP` interval.

The only split not paid by the present ledger is the two-way extreme

```text
P | T^5P,
```

obtained after destroying the router triangle. The `T^5P` side is qualitatively
positive but has no known uniform margin to absorb the isolated pentagon's
deficit. The exact color-preserving incidence census in
`research/octacyclic-fully-shared-incidence-census-2026-07-26.md` finds six and
only six ordinary-split exceptions: the common-cut bouquet and five
nonbouquet common-cut/router decorations. The rooted Schur-Sachs theorem closes
the bouquet. The other five are not counterexamples, but they remain outside
the current packet and common-pivot arguments. The census does not enumerate
cyclic mark order, so it is an exact abstract-incidence boundary rather than a
spectral proof of those five classes.

## 8. Why the heptacyclic theorem does not finish the cores

The rank-seven theorem says `sigma(H)>0` but supplies no graph-independent
positive constant. Consequently none of the following deductions is valid:

```text
(heptacyclic strict packet) + (opened tree of surplus -1) > 0,
(heptacyclic strict packet) + (isolated P of surplus at least -delta) > 0.
```

This blocks the tempting operations on the remaining two-pentagon endpoint and
router cores:

- split a terminal router triangle as `P+T^5P`;

The analogous common-cut bouquet openings are no longer gaps: the later rooted
Schur-Sachs theorem closes both fully shared bouquets without opening cycles,
and the rooted guard theorem closes the bridge-separated (D7Q) endpoint.

A complete proof therefore needs one genuinely new quantitative or
non-additive ingredient. Plausible targets are a root-aware positive margin for
the bouquet/router cores, a direct spectral comparison coupling the hostile
leaf to the large triangle packet, or a new multi-cycle sacrifice that does not
charge one full tree unit per opened cycle.

## 9. Exact status

Proved by the structural reductions and exact census:

1. the complete DNN residual classification `T^7Q` and `T^6PP`;
2. every nonresidual connected octacyclic cactus;
3. all fully shared `T^7Q` incidences, including the common-cut bouquet by the
   rooted Schur-Sachs theorem;
4. all fully shared `T^6PP` incidences with an internal pentagon;
5. all other fully shared `T^6PP` incidences admitting a nonextreme
   internal-triangle split, plus the common-cut bouquet;
6. every disconnected `T^7Q` configuration, including the locked
   bridge-bouquet (G7Q) by rooted guard absorption;
7. every disconnected `T^6PP` configuration with an all-triangle leaf and
   every singleton-triangle partition row; `P|T^6|P` completely; and
   `T^6P|P` outside the exact locked-entry class (G6PP).

Not proved:

1. the exact entry-locked leaf-pentagon class (G6PP) inside `T^6P|P`;
2. the five nonbouquet fully shared `T^6PP` abstract incidence types left by
   the exact ordinary-split census;
3. a quantitative two-interface or matrix-valued phase lemma capable of
   closing those pentagonal endpoint and multi-pivot classes.

Accordingly, the statement

```text
every connected octacyclic cactus G satisfies s+(G)>|V(G)|
```

remains open in this note. No finite census is needed for the reductions above,
and no census would by itself repair the missing quantitative inequalities.
