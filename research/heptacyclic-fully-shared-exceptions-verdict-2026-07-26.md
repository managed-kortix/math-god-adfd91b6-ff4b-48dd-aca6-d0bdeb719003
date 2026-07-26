# Exact verdict on the fully shared heptacyclic census exceptions

## Verdict

**ACCEPT.** The fully shared censuses leave exactly `1+3` canonical ordinary-
split exceptions, and all four close by the exact private-opening sacrifice
lemma. No exception needs an unproved private vertex, a qualitative margin to
pay a fixed cost, or a concentration assumption not present in its canonical
incidence tree.

More precisely:

- the unique `T^6Q` exception is the seven-cycle bouquet and closes by opening
  one private vertex of `Q`, retaining one concentrated `A_6` territory, with
  ledger `sigma(G) >= sigma(A_6)-1 > 1-1=0`;
- the three `T^5PP` exceptions have both pentagons as incidence leaves and
  close by opening one private vertex on each pentagon, retaining one
  concentrated `A_5` territory, with ledger
  `sigma(G) >= sigma(A_5)-2 > 2-2=0`.

The conclusions are uniform over the length and parity of `Q`, all binary or
multiway shared cuts displayed by the incidence structures, and arbitrary
finite trees attached at arbitrary core vertices.

This verdict is local to one fully shared cluster. It does not settle proper
shared-cluster partitions or connector problems in a general heptacyclic
cactus.

## Exact operation being certified

Let `C` be an incidence-leaf cycle, let `x` be its unique cyclic cut, and choose
a cycle vertex `v != x`. Since `C` has only one cyclic cut, `v` is private with
respect to all cyclic blocks. Put `v` and every off-core tree branch rooted at
`v` into `F`, and put every other vertex into `H`.

Then the partition is exact and induced:

1. `F` is nonempty and is a tree, so `sigma(F)=-1`, independently of its order
   and shape.
2. `C-v` is a path in `H` containing `x`; it is retained as an attached tree
   and retains no cycle.
3. Every off-core component has one core attachment in a cactus, so every
   hanging tree goes wholly to exactly one territory.
4. Openings on distinct cyclic blocks produce disjoint tree territories,
   because the selected private vertices are distinct and their rooted
   off-core branches have unique attachments.
5. Deleting incidence-leaf cycle nodes leaves the incidence subtree on the
   retained cycles connected whenever that connectivity is visible in the
   canonical structures below. Binary cut nodes that become irrelevant are
   simply suppressed.

Thus induced-subgraph superadditivity gives

`sigma(G) >= sigma(H) + sum sigma(F_i) = sigma(H)-k`

for `k` openings. The strictness comes from the retained triangular packet;
the tree costs are exact equalities.

## The one `T^6Q` exception

The census exception in every capacity regime `q=3,4,5,6,>=7` has canonical
signature

```text
X(Q()T()T()T()T()T()T())
```

It is one color-preserving canonical structure, repeated across five capacity
regimes, not five distinct exceptions. All seven cycles meet one common cut
`x`.

The `Q` node is an incidence leaf. A cycle `Q=C_q`, `q>=3`, has `q-1>=2`
vertices other than `x`, so an admissible private vertex exists even when
`Q=T`. Open one such vertex and its entire rooted off-core tree territory.
The path `Q-v` remains attached at `x`. All six triangles are untouched and
still share `x`, hence they form exactly one connected `A_6` shared-cut
territory, with the `Q-v` path and all other attachments merely arbitrary tree
attachments.

The exact cost and credit are

```text
opened territories:  1 nonempty tree,       sigma = -1
retained territory:   one concentrated A_6,  sigma > 1
total:                                        sigma > 0
```

This one-opening repair is stronger than the also valid three-opening repair
which opens `Q` and two triangles and retains `A_4`: it spends one unit rather
than three. Neither repair retains a possibly hostile `Q`, so no parity- or
length-dependent `Q` deficit enters the ledger.

## The three `T^5PP` exceptions

Use cycle nodes `0,...,4=T`, `5,6=P`, with cut nodes beginning at `7`.

### U1: seven-cycle bouquet

```text
((0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7))
```

Both pentagons are incidence leaves at cut `7`. Each has four cycle vertices
other than the cut, so choose one private vertex on each. The two choices and
their rooted tree territories are disjoint. Both pentagon remnants remain as
paths attached at `7`; all five triangles still share `7`. The retained cyclic
part is therefore one `A_5`, not five separately credited triangles.

### U2: six-cycle common-cut core with a `TP` tail

```text
((0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(0,8),(6,8))
```

Pentagon `5` is an incidence leaf at `7`, and pentagon `6` is an incidence leaf
at `8`. Open one of the four private cycle vertices on each pentagon. Triangle
`0`, not either pentagon, owns the incidence route between cuts `7` and `8`.
After the openings, cut `8` is no longer a shared cyclic cut and the pentagon
remnant there is only a tree branch on triangle `0`. The five retained
triangles remain connected through their common cut `7`, so the retained
territory is exactly one concentrated `A_5` with arbitrary tree attachments.
There is no ownership conflict between cuts `7` and `8`.

### U3: five-triangle common-cut core with two pentagon tails

```text
((0,7),(1,7),(2,7),(3,7),(4,7),
 (0,8),(5,8),(1,9),(6,9))
```

Pentagons `5` and `6` are incidence leaves at cuts `8` and `9`, respectively.
Open one private cycle vertex on each. Their path remnants become separate tree
branches on triangles `0` and `1`. Cuts `8` and `9` cease to be shared cyclic
cuts, while all five triangles remain joined at cut `7`. Thus the two tails do
not disperse the retained triangles: the retained cyclic incidence is exactly
the five-triangle common-cut cluster `A_5`.

For each of U1--U3 the exact common ledger is

```text
opened territories:  2 disjoint nonempty trees,  sigma = -2
retained territory:   one concentrated A_5,       sigma > 2
total:                                             sigma > 0
```

This checks the point not certified by the abstract census itself: private
vertices exist, the two induced tree territories are disjoint, all five
triangles retain one shared-cut component, and arbitrary attached trees have a
unique owner.

## Splitting side of the dichotomies

The sacrifices above close all four census exceptions. The companion splitting
lemmas explain why no saturated or dispersed structure creates an additional
fully shared exception.

- If `Q` is internal in `T^6Q`, split it into one proper consecutive interval
  per incidence branch. Every branch contains `r_j>=1` triangles and becomes
  one connected `A_(r_j)` territory. The split destroys `Q`, costs no tree
  territory, and has strict positive total because every triangular packet is
  strict and every certified `b_(r_j)` is nonnegative.
- If a pentagon is internal in `T^5PP`, split it similarly. If the branch
  containing the other pentagon also contains triangles, that mixed branch is
  nonnegative or positive and another all-triangle branch is strict. If the
  other pentagon is a singleton branch, five triangles occupy at most four
  remaining branches, forcing an `A_r`, `r>=2`, with margin `>1`; this absorbs
  the singleton pentagon deficit `delta=sqrt(5)-2<1`.
- Proper consecutive intervals assign every hub mark and every hanging tree to
  one owner. The split cycle is retained by no territory, so there is no hidden
  `-1` opening cost and no need for a private hub vertex.

Accordingly the leaf cases are paid sacrifices and the internal cases are
cost-free splits. This dichotomy covers common-cut locks, saturated hubs, and
dispersed branches without mixing qualitative positivity with a fixed charge.

## Exact returned conclusion

The executable censuses assert one unresolved canonical `T^6Q` incidence type
and three unresolved canonical `T^5PP` incidence types. Direct inspection of
all four canonical structures verifies the hypotheses of the sacrifice lemmas
exactly. Therefore:

```text
fully shared T^6Q census exceptions:   1/1 closed
fully shared T^5PP census exceptions:  3/3 closed
combined canonical exceptions:         4/4 closed
remaining fully shared exception:      none
```

The exact verdict is **ACCEPT: the fully shared heptacyclic census exceptions
close, uniformly with arbitrary attached trees, by the stated sacrifice/
splitting dichotomies.**
