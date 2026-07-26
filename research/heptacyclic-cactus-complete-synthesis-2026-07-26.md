# Connected heptacyclic cacti: complete residual synthesis

## Theorem and status

For a graph `H`, write

`sigma(H)=s+(H)-|V(H)|`.

**Theorem.** Every connected heptacyclic cactus `G` satisfies

`sigma(G)>0`,

equivalently `s+(G)>|V(G)|`.

The proof below is exhaustive, conditional only on the previously established
sharp cactus DNN theorem, induced-subgraph superadditivity, the connected
bicyclic through hexacyclic cactus theorems, and the packet estimates listed in
Section 1. The three heptacyclic census programs were rerun on 2026-07-26 and
all embedded assertions passed. The censuses are independent finite audits of
the structural reductions; the proof does not infer geometric ownership from
the programs.

## 1. Inputs

Write `T=C3`, `P=C5`, and

`delta=sqrt(5)-2<1/2`.

We use the following established facts, all with arbitrary finite trees
attached at arbitrary vertices.

1. If `V(H)` is partitioned into induced subgraphs `H_i`, then
   `sigma(H)>=sum_i sigma(H_i)`.
2. Every connected bicyclic or tricyclic cactus has nonnegative surplus, and
   every connected tetracyclic, pentacyclic, or hexacyclic cactus has strictly
   positive surplus.
3. The packet bounds are

   `sigma(T)>0`, `sigma(P)>=-delta`, `sigma(TT)>1`,
   `sigma(TP)>1-delta`, `sigma(PP)>0` for one shared-cut `PP` cluster, and
   `sigma(TPP)>6-2sqrt(5)>3/2` for one shared-cut `TPP` cluster.

   The mixed `TP` estimate allows an arbitrary bridge connector.
4. If `A_r` is a connected cactus whose `r` triangles form one shared-cut
   cluster, then

   `sigma(A_r)>b_r`,

   where

   | `r` | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
   |---:|---:|---:|---:|---:|---:|---:|---:|
   | `b_r` | 0 | 1 | 2 | 3 | 2 | 1 | 0 |

   For `r<=4` this is the established shared-triangle estimate. For `r>=5`,
   repeatedly open a private vertex of an incidence-leaf triangle. Each
   opening produces a nonempty induced tree of surplus exactly `-1`, while the
   retained triangles remain one shared-cut cluster. Starting from
   `sigma(A_4)>3` gives `sigma(A_r)>7-r`.
5. A unicyclic cactus with cycle `C_q` has nonnegative surplus unless
   `q=1 mod 4`; in the latter case

   `sigma(C_q territory)>=-delta_q`,
   `delta_q=sec(pi/q)-1<1`.

We also use two standard territory operations. Cutting actual bridge edges in
the reduced cluster tree gives connected induced territories, with every
connector remnant, Steiner branch, entry, and hanging tree assigned to one
owner. If a cycle node `C` has `d>=2` incidence branches, its distinct cyclic
marks can be assigned, in cyclic order, to `d` nonempty proper consecutive
intervals. Each interval and its branch is a connected induced territory; `C`
is destroyed and there is no `-1` opening charge. If a private vertex of `C`
is opened instead, that vertex and all branches rooted there form a nonempty
tree territory of surplus `-1`.

## 2. Exact sharp-DNN reduction

Let the seven cycle lengths be `l_1,...,l_7`. Block counting and the sharp
cactus DNN theorem give

`sigma(G)>=6-sum_i epsilon_(l_i)`,

where `epsilon_l=0` for even `l` and

`epsilon_l=l tan^2(pi/(2l))`

for odd `l`. The odd sequence is strictly decreasing,

`epsilon_3=1`, `epsilon_5=5-2sqrt(5)=a`,

and the exact comparisons

`3a<2`, `2a>1`, `epsilon_5+epsilon_7<1`

imply the following exhaustive classification.

- With at most four triangles, the epsilon sum is at most `4+3a<6`.
- With exactly five triangles, the only nonsafe remaining pair is `P,P`.
- With at least six triangles, the multiset is `T^6Q` for some `Q=C_q`,
  `q>=3`; the case `q=3` includes seven triangles.

Thus the DNN bound is already strict except for exactly

`T^6Q` and `T^5PP`.

It remains to prove positivity for these two residual families.

## 3. The residual `T^6Q`

### 3.1 Disconnected shared-cut graph

Contract every shared-cut cluster in the block-cut tree and take the reduced
cluster tree `R`. If the shared-cut graph is disconnected, `R` has at least two
marked leaves. At most one leaf cluster contains the distinguished cycle `Q`,
so another leaf cluster consists of `r` triangles, for some `1<=r<=6`.

Cut an actual bridge leaving that cluster. The leaf territory is an `A_r`
packet and the complementary territory is a connected `(7-r)`-cyclic cactus
containing `Q`. The complete ledger is

| `r` | triangle leaf | complementary territory | total |
|---:|---|---|---|
| 1 | `>0` | hexacyclic `>0` | `>0` |
| 2 | `>1` | pentacyclic `>0` | `>0` |
| 3 | `>2` | tetracyclic `>0` | `>0` |
| 4 | `>3` | tricyclic `>=0` | `>0` |
| 5 | `>2` | bicyclic `>=0` | `>0` |
| 6 | `>1` | unicyclic `Q` | `>0` |

In the last row a nonhostile `Q` is nonnegative. A hostile `Q` is bounded by
`-delta_q`, and `1-delta_q>0`. This proves every disconnected `T^6Q` case,
with arbitrary reduced-tree topology, connector entry, connector length,
Steiner branches, and attached trees.

### 3.2 One fully shared cluster

Let `I` be the bipartite cycle-cut incidence tree and consider the distinguished
node `Q`.

- If `deg_I(Q)=1`, open a private vertex of `Q`. Removing this incidence leaf
  leaves the six triangles in one shared-cut cluster. Hence

  `sigma(G)>=sigma(A_6)-1>1-1=0`.

- If `deg_I(Q)=d>=2`, split `Q` into one proper consecutive interval per
  component of `I-Q`. If those components contain `r_1,...,r_d` triangles,
  then every `r_j>=1` and `sum_j r_j=6`. The resulting exact induced
  territories are `A_(r_1),...,A_(r_d)`, so

  `sigma(G)>=sum_j sigma(A_(r_j))>sum_j b_(r_j)>=0`.

The strict conclusion follows because every packet inequality is strict. This
dichotomy includes a saturated `Q` hub and all dispersed branch patterns. In
the seven-cycle bouquet `Q` is a leaf, so the first case is the common-cut
sacrifice.

Therefore every `T^6Q` residual has positive surplus.

## 4. The residual `T^5PP`: disconnected shared-cut graph

Encode each shared-cut cluster by `(t,p)`, its triangle and pentagon counts. The
exact colored-partition recursion has 47 partitions of `(5,2)`, including the
one-cluster partition, and hence 46 proper partitions. Applying the packet
bounds of Section 1 directly resolves 41. The exact five remaining color rows
are

`P|P|T|T|T|T|T`,

`TTP|P|T|T|T`,

`TTTP|P|T|T`,

`TTTTP|P|T`,

`TTTTTP|P`.

Here the first four have the form

`A_k | T | ... | T | P_1`,

where `A_0=P_0` and, for `k>=2`, `A_k=T^kP_0` is one nontrivial cluster.

If a singleton triangular cluster is a leaf of the reduced cluster tree, cut
its first actual bridge. This gives a strict triangular unicyclic territory and
a strict connected hexacyclic territory. Otherwise no singleton triangle is a
leaf. The only possible leaf marks are then `A_k` and `P_1`; consequently they
are the two leaves and the reduced tree is their path. Let `T_*` be the
singleton triangle nearest `P_1`. Cutting actual bridges on the two sides of
the terminal packet gives

`TP + (connected pentacyclic cactus)`,

and both terms are strict positive. This resolves the first four exceptional
rows for every reduced-tree topology and connector realization.

For the final row, let `A=T^5P_0` be the nontrivial cluster, let `P_1` be the
remote pentagon, and put `d=deg_I(P_0)` in the incidence tree of `A`.

- If `d>=2`, split `P_0` into one interval per incidence branch. Adjoin the
  external connector and `P_1` to the interval owning the connector entry. If
  that branch contains `r` triangles, its territory has type `T^rP_1`: it is
  strict positive for `r=1`, nonnegative for `r=2`, and strict positive for
  `r>=3`. Every other branch is a strict all-triangle territory, and at least
  one other branch exists. The total is strict positive.
- If `d=1`, choose a private vertex of `P_0` away from the connector entry and
  a private vertex of `P_1` away from its entry, and open both. The five
  triangles remain one shared-cut cluster, while the two opened territories
  are disjoint nonempty trees. Thus

  `sigma(G)>=sigma(A_5)-2>2-2=0`.

This exhausts the last row. Therefore every disconnected `T^5PP` residual has
positive surplus.

## 5. The residual `T^5PP`: one fully shared cluster

Let `I` be the incidence tree and inspect the two pentagon nodes.

### 5.1 Both pentagons are incidence leaves

Open one private vertex on each pentagon. The opened territories are disjoint
nonempty trees. Successive deletion of the two leaf cycle nodes leaves the five
triangles connected in one shared-cut incidence tree. Therefore

`sigma(G)>=sigma(A_5)-2>2-2=0`.

This is the exact repair for the seven-cycle bouquet, the six-cycle common-cut
`T^5P` core with a `TP` tail, and the five-triangle common-cut core with two
separate pentagon tails.

### 5.2 An internal pentagon exists

Choose an internal pentagon `P_0`, with `2<=d=deg_I(P_0)<=5`, and split it into
one proper consecutive interval per component of `I-P_0`. There is a unique
branch `B` containing the other pentagon `P_1`; let `a` be the number of
triangles in `B`.

- If `a>=1`, then `1<=a<=4`, because another nonempty branch exists. The
  `B` territory is `T^aP`: it is positive for `a=1`, nonnegative for `a=2`,
  and positive for `a=3,4`. At least one other branch is a strict
  all-triangle territory. Hence the total is positive.
- If `a=0`, the `B` territory is a singleton pentagon and contributes at least
  `-delta`. The five triangles occupy at most `d-1<=4` other nonempty
  branches. One branch therefore contains at least two triangles and has
  surplus `>1`; every remaining triangular branch is strict. Thus the total is
  `>1-delta>0`.

This includes saturated pentagon hubs and every dispersed two-pentagon
configuration. Therefore every fully shared `T^5PP` residual has positive
surplus.

## 6. Exhaustiveness and census cross-check

Sections 2--5 form a disjoint and exhaustive proof tree:

1. sharp DNN settles every cycle multiset except `T^6Q` and `T^5PP`;
2. each residual shared-cut graph is either disconnected or one cluster;
3. disconnected `T^6Q` always has a `Q`-free all-triangle reduced-tree leaf;
4. all 46 proper `T^5PP` cluster-color partitions are covered by the 41 direct
   rows and the five topology/entry rows proved in Section 4;
5. fully shared `T^6Q` is exhausted by `deg_I(Q)=1` or `deg_I(Q)>=2`;
6. fully shared `T^5PP` is exhausted by both pentagons being leaves or the
   existence of an internal pentagon.

The rerun exact censuses give the following independent checks.

- Fully shared `T^6Q`: corrected totals are `216,224,226,227,227` in the regimes
  `q=3,4,5,6,>=7`. Every nonbouquet tree has a SAFE ordinary one-cycle split;
  the unique unresolved ordinary-split type in every regime is the bouquet,
  closed by the `Q`-leaf sacrifice in Section 3.2.
- Fully shared `T^5PP`: there are 560 color-preserving incidence trees. The
  ordinary ledger resolves 557. Its three exceptions are exactly the bouquet,
  the `T^5P` common-cut core with a `TP` tail, and the five-triangle common-cut
  core with two pentagon tails. In all three both pentagons are incidence
  leaves, so Section 5.1 closes them.
- Disconnected `T^5PP`: the exact partition script returns 47 total colored
  partitions, 46 proper partitions, 41 direct rows, and exactly the five rows
  treated in Section 4.

The abstract incidence censuses do not enumerate cyclic orders, connector
entries, or attached trees. No gap results: interval realizability follows from
the distinct cyclic marks and the cycle degree bounds; entry, connector, and
hanging-tree ownership is supplied by the territory lemmas used explicitly in
Sections 3--5. The sacrifice cases separately verify private vertices,
disjointness, ordinary connectivity, and retained shared-cut concentration.

Combining all cases proves `sigma(G)>0`, and hence `s+(G)>|V(G)|`, for every
connected heptacyclic cactus.

## 7. Reproduction

From the repository root:

```bash
python research/heptacyclic-t5pp-disconnected-partition-audit.py
python research/heptacyclic-t6q-incidence-census.py
python research/heptacyclic-tttttpp-incidence-census.py
```

These are all current heptacyclic Python certificates. All three commands
complete with their asserted counts and exception lists; all Python files in
`research/` also pass byte-compilation.
