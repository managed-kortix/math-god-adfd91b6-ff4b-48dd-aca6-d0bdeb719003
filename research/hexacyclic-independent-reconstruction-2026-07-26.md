# Independent reconstruction of the hexacyclic cactus theorem

**Date:** 2026-07-26

## Verdict

**PASS.** Independently assembling the argument from the stated lower-rank
theorems, the sharp cactus DNN inequality, the induced-territory operations,
and the new exact certificates proves the following theorem:

> **Hexacyclic cactus theorem.** If `G` is a connected cactus with six cyclic
> blocks and `n=|V(G)|`, then `s+(G)>n`.

The reconstruction does not use the conclusions of the synthesis or planning
notes as premises. In particular, the proof below rederives the DNN frontier,
separately covers each frontier family according to whether its shared-cut
graph is connected, and checks the exceptional configurations returned by the
executables. No unresolved colored partition, incidence tree, connector-entry
case, or opening cost remains.

## 1. Inputs accepted from established work

For `sigma(X)=s+(X)-|V(X)|`, I used the following proved inputs from the
manuscripts, rather than claims of completeness in the hexacyclic synthesis
notes.

1. Induced-subgraph superadditivity for every vertex partition.
2. The arbitrary-connector territory lemma and the consecutive-interval split
   construction in `all-pentacyclic-cacti/paper.tex`.
3. Every connected bicyclic or tricyclic cactus has `sigma>=0`; every connected
   tetracyclic or pentacyclic cactus has `sigma>0`.
4. The packet estimates

   ```text
   sigma(T)>0,                     sigma(P)>=-delta,
   sigma(Cq)>=-delta_q,            sigma(TT)>1,
   sigma(TP)>1-delta,              sigma(TCq)>1-delta_q,
   sigma(TTT)>2,                   sigma(TTTT)>3,
   sigma(TPP)>6-2sqrt(5),
   ```

   with the stated shared-cut hypotheses on the concentrated packets, where
   `delta=sqrt(5)-2<1/2` and `delta_q=sec(pi/q)-1<1` for `q=1 mod 4`.
5. The triangular block-graph corollary in
   `packing-two-square-energy/paper.tex`: a connected cactus with only
   triangular cyclic blocks and at least one cycle has strict positive surplus,
   with arbitrary bridges and attached trees.
6. The sharp cactus DNN formula and `s-(G)<=kappa(G)` as recorded, with proof
   mechanism, in `all-pentacyclic-cacti/paper.tex`.

The new four- and five-triangle quantitative certificates were also checked
from their arguments, not merely quoted from their concluding prose. The
four-triangle one-cluster estimate `sigma>3` covers packing at most two by the
phase theorem and covers the unique packing-three central-triangle incidence
by the displayed matching injections. Opening a private vertex of an
incidence-leaf triangle then leaves that four-triangle cluster and one induced
tree of surplus `-1`, proving the five-triangle one-cluster estimate
`sigma>2`.

## 2. Independent DNN reconstruction

Let the six cycle lengths be `l1,...,l6`, let `b` be the number of bridge
blocks, and let `n=|V(G)|`. Block counting gives

```text
b + sum_i li = |E(G)| = n+5.
```

Put

```text
epsilon_l = 0                         for even l,
epsilon_l = l tan^2(pi/(2l))          for odd l.
```

The sharp DNN formula gives

```text
s-(G) <= n+5+sum_i epsilon_li.
```

Since `s+(G)+s-(G)=2|E(G)|=2n+10`, this yields

```text
sigma(G) >= 5-sum_i epsilon_li.                 (1)
```

The odd sequence is strictly decreasing,
`epsilon_3=1`, and `epsilon_5=a=5-2sqrt(5)`. The exact comparisons needed are

```text
3a<2,       2a>1,       epsilon_5+epsilon_7<1.
```

The last inequality follows from the rational bounds
`cos(pi/7)>7/8`, `epsilon_7<7/15`, and
`7/15<2sqrt(5)-4=1-epsilon_5`.

If `t` is the number of triangles, then for `t<=3`,

```text
sum_i epsilon_li <= 3+3a < 5.
```

For `t=4`, the two remaining cycles contribute at least one only when both are
pentagons: an even cycle contributes zero, and every other odd pair is bounded
by `epsilon_5+epsilon_7<1`. For `t>=5`, write the multiset as five designated
triangles and `Q=Cq`, including `q=3`. Thus (1) leaves exactly

```text
R1 = TTTTTQ, q>=3,
R2 = TTTTPP.
```

Every other six-cycle multiset is already strict by (1).

## 3. Disconnected shared-cut graph

### 3.1 `TTTTTQ`

If `q=3`, the triangular block-graph theorem applies directly. Otherwise take
a leaf of the reduced cluster tree not containing `Q`; it consists of `r`
triangles, `1<=r<=5`. Cutting the first actual bridge gives induced connected
territories carrying that triangular cluster and its complement.

- For `r=1`, the complement is pentacyclic and strict.
- For `r=2`, the complement is tetracyclic and strict.
- For `r=3,4`, the complement is respectively tricyclic or bicyclic and
  nonnegative, while the triangular side is strict.
- For `r=5`, the leaf is one shared-cut cluster. Its surplus is `>2`, while a
  hostile singleton `Q` has surplus at least `-delta_q` with `delta_q<1`.

Hence every disconnected `TTTTTQ` cactus has positive surplus. This argument
also checks the formerly delicate `TTTTT|Q` row without assuming packing at
most two.

### 3.2 Colored partition count for `TTTTPP`

I independently regenerated colored set partitions by ordinary set partitions
followed by canonicalizing each block to its pair
`(number of T, number of other color)` and sorting the block list. For both
color multiplicities `(4,2)` (`TTTTPP`) and `(5,1)` (`TTTTTQ`), the result is
exactly `29` colored partitions including the one-block partition, hence
exactly `28` proper colored partitions. Their common distribution by number of
blocks is

```text
1, 7, 10, 7, 3, 1       for 1,...,6 blocks.
```

Thus the claimed proper-partition count `28` is correct. The displayed
28-row table in the disconnected audit contains distinct rows and exhausts
this canonical set. Its packet ledger directly settles `23` rows.

The remaining five rows reconstruct as follows.

1. `T|T|T|T|P|P`: a triangular reduced-tree leaf gives `T + pentacyclic`.
   If there is no such leaf, the two pentagons are the only leaves, so the tree
   is a path and partitions as `TP+TT+TP`, with total `>3-2delta>0`.
2. `TTP|TTP`: if a cluster has intersecting triangles, its quantitative credit
   suffices. Otherwise each cluster is a distinct-cut `T-P-T` chain. Coordinated
   interval splits of the two pentagons, with the bridge connector assigned to
   the intervals containing its actual entries, give `TT+T+T`.
3. `TTP|T|T|P`: after the direct intersecting-triangle and reduced-edge
   separations, absence of a triangle leaf forces the reduced tree to be the
   path from `TTP` to `P`, with the two singleton triangles internal. Splitting
   the chain pentagon at its actual entry gives `TT+T+TP`.
4. `TTTP|T|P` (former E2): if the singleton-to-singleton route avoids `TTTP`,
   use `TP+tetracyclic`. If it passes through `TTTP`, seven of the eight exact
   colored incidences contain an intersecting triangle pair and have
   `sigma(TTTP)>1`, which absorbs `-delta`. The remaining three-petal pentagon
   hub has exactly `26` ordered labelled-entry orbits; every orbit has an
   induced interval certificate, `20` of type `TP+TTT` and `6` of type
   `TTP+TT`.
5. `TTTTP|P` (former E1): remove the internal pentagon node from the incidence
   tree. Because at least two triangles meet, its attached triangle-component
   sizes are exactly `(4)`, `(3,1)`, `(2,2)`, or `(2,1,1)`. Marking the component
   containing the external entry gives exactly six rows. For two or three
   components, intervals of the internal pentagon give respectively
   `TTTP+T`, `TP+TTT`, `TTP+TT`, `TTP+T+T`, or `TP+TT+T`, all positive by the
   lower-rank ledger. In the `(4)` case, opening private vertices of both
   pentagons costs exactly two and leaves one shared-cut four-triangle cluster
   of surplus `>3`, so the total is `>1`.

The component partition in item 5 is exhaustive because deleting the internal
pentagon from an incidence tree attaches every resulting component to it once
at a distinct cut, and the E1 hypothesis requires a nonsingleton triangle
component. Entry position only marks one such component; the interval proof is
independent of the internal component shape and cyclic order.

Therefore all `28` proper colored partitions, with every reduced-tree and
connector-entry subcase, are covered. The disconnected `TTTTPP` residual is
proved.

## 4. Fully shared `TTTTTQ`

For one shared-cut cluster, the cycle-cut incidence graph is a bipartite tree.
With `c` cut nodes it has `c+5` edges and
`sum_x(deg(x)-1)=5`, so `1<=c<=5`. Triangle degrees are at most three, and the
capacity of `Q` gives the three exhaustive regimes `q=3`, `q=4`, and `q>=5`.

The exact color-preserving counts by `c=1,...,5` reproduce as

```text
q=3:   1, 6, 20, 27, 14 = 68,
q=4:   1, 6, 20, 28, 15 = 70,
q>=5:  1, 6, 20, 28, 16 = 71.
```

I additionally compared the center-rooted colored-tree classes with the
explicit canonical edge minimization under `S5 x S_c`; every class count
agreed in every capacity regime.

Deleting a cycle node of degree at least two corresponds to a legal
consecutive-interval split. If `Q` is split, all branches are nonempty
all-triangle packets and are positive. If a triangle is split, exactly one
branch contains `Q`:

- singleton hostile `Q` loses less than one, while the other four triangles
  occupy at most two branches and one contains `TT`, with surplus `>1`;
- `TQ` is positive;
- generic `TTQ` is nonnegative and another all-triangle branch is strict;
- larger `T^kQ` branches are covered by tetracyclic or pentacyclic positivity.

The census resolves `67`, `69`, and `70` trees, respectively. In each regime
the unique exception is the six-cycle bouquet. There, open a private vertex of
`Q` and one designated triangle. The two induced tree territories cost exactly
two, and the other four triangles remain one shared-cut bouquet of surplus
`>3`; hence the total is `>1`. This also covers `Q=T`.

Thus every fully shared `TTTTTQ` incidence is covered.

## 5. Fully shared `TTTTPP`

The exact census quotients by `S4 x S2 x S_c`. It returns

```text
c:              1,  2,  3,  4,  5
colored trees:  1,  9, 40, 62, 38      total 150
SAFE resolved:  0,  9, 40, 62, 37      total 148.
```

All `900=6*150` cycle choices are recorded in `26` split-profile classes. The
SAFE test checks retained incidence, not colors alone: in particular, stronger
`TTP`, `TTTP`, `TTT`, `TTTT`, `TPP`, and shared-`PP` bounds are used only when
the required cut remains in that actual branch. Generic tetracyclic or
pentacyclic positivity is never used to cancel a negative singleton pentagon.
Recomputing the `Decimal` bounds confirms every accepted total is positive, or
zero with a strict summand.

Exactly two canonical trees lack an ordinary SAFE split.

1. **Six-cycle bouquet.** Open private vertices of the two pentagons. The
   retained four-triangle bouquet has surplus `>3`, while the two trees cost
   two, giving total `>1`.
2. **Saturated pentagon hub.** One pentagon has five distinct marks, with four
   triangular petals and one pentagonal petal. In cyclic order, merge the
   pentagonal mark with either adjacent triangular mark and assign the other
   three marks separate proper intervals. This exact interval partition gives
   `TP+T+T+T`, whose total is positive because `sigma(TP)>1-delta>0` and each
   triangle is strict. Every marked vertex and attached tree has one owner.

These repairs cover the only executable exceptions. Thus every fully shared
`TTTTPP` incidence is covered.

## 6. Script reproduction

I ran every hexacyclic verification script unchanged from the repository root:

```text
python research/hexacyclic-tttttq-incidence-census.py
python research/hexacyclic-ttttpp-incidence-census.py
python research/hexacyclic-e2-tttp-entry-census.py
python -m py_compile research/hexacyclic-tttttq-incidence-census.py \
  research/hexacyclic-ttttpp-incidence-census.py \
  research/hexacyclic-e2-tttp-entry-census.py
```

All commands exited successfully. The first two reproduced the incidence totals
and exceptions in Sections 4 and 5. The E2 script reproduced `1,3,4` colored
`TTTP` incidence trees by cut count, seven intersecting-pair trees, one
three-petal hub, `26` ordered entry orbits, and the exact `20/6` certificate
split. Bytecode compilation reported no error.

I also ran two independent short checks not imported by the certificates:

- canonical colored set-partition generation returned `28` proper partitions
  for each of the color multiplicities `(4,2)` and `(5,1)`;
- explicit canonical-edge minimization matched every center-code class in all
  three `TTTTTQ` capacity regimes.

## 7. Exhaustion and exact reason for PASS

The proof tree is exhaustive:

1. The independently derived DNN inequality proves every cycle multiset except
   `TTTTTQ` and `TTTTPP`.
2. Each residual has either disconnected or connected shared-cut graph.
3. The disconnected `TTTTTQ` leaf argument and the disconnected `TTTTPP`
   28-partition/entry analysis cover the first alternative.
4. For the connected alternative, all six cycles form one shared-cut cluster;
   the exact incidence censuses cover every color-preserving incidence tree.
5. The only census exceptions are one bouquet in `TTTTTQ`, and one bouquet plus
   one saturated hub in `TTTTPP`; their explicit induced-territory constructions
   are positive.
6. Every cycle opening is charged exactly one per induced tree, every interval
   split charges no fictitious opening cost, and no shared cut is assigned to
   two territories.

Therefore the theorem is **PASS**, with no qualification beyond the established
lower-rank and sharp-DNN inputs listed in Section 1.
