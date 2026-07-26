# E2 only: two labelled entries through a shared `TTTP` cluster

## Statement

Let `G` have shared-cut cluster partition

`A|B|C = TTTP0 | T4 | P1`,

and suppose the `B-C` path in the reduced cluster tree passes through `A`.
Then `G` has a legal induced territory decomposition with positive total
surplus. Thus the family called E2 in
`research/hexacyclic-ttttpp-disconnected-audit-2026-07-26.md` is resolved.
This note makes no claim about E1 or any broader hexacyclic family.

Write `sigma(H)=s+(H)-|V(H)|` and `delta=sqrt(5)-2`. The only packet bounds
used below are

```text
sigma(TP)>1-delta,  sigma(TT)>1,
sigma(H)>=0 for every tricyclic cactus,
sigma(TTTP)>1 when two triangles in the shared cluster meet.
```

The two connector arms are labelled by their remote cycles: the `b`-arm ends
at `B=T4`, and the `c`-arm ends at `C=P1`. Their first vertices in the cyclic
core of `A` are allowed to coincide.

## The eight colored incidence trees

Let `I` be the bipartite cycle-cut incidence tree of `A`, with triangle nodes
`0,1,2`, pentagon node `3`, and cut nodes numbered from `4`. If `c` is the
number of cut nodes, then

`sum_x (deg_I(x)-1)=3`,

so `1<=c<=3`. Every cut has degree at least two; triangle degrees are at most
three; and the pentagon degree is at most five. Exhaustion modulo permutations
of the three triangles and of the cut nodes gives respectively `1,3,4` trees
for `c=1,2,3`:

```text
c=1
((0,4),(1,4),(2,4),(3,4))

c=2
((0,4),(0,5),(1,4),(2,4),(3,5))
((0,4),(0,5),(1,4),(2,5),(3,4))
((0,4),(1,4),(2,5),(3,4),(3,5))

c=3
((0,4),(0,5),(0,6),(1,4),(2,5),(3,6))
((0,4),(0,5),(1,4),(1,6),(2,5),(3,6))
((0,4),(0,5),(1,4),(2,6),(3,5),(3,6))
((0,4),(1,5),(2,6),(3,4),(3,5),(3,6)).
```

The first seven trees contain a cut incident with at least two triangles. For
such an incidence the established shared-triangle bound gives

`sigma(A)>1`.

Keeping the three clusters as bridge-separated territories therefore gives

`sigma(G) >= sigma(A)+sigma(B)+sigma(C) > 1-delta>0`.

This argument is independent of both entry positions. Consequently only the
last incidence tree needs entry analysis. It is the three-petal hub: the three
triangles are pairwise disjoint and meet `P0` at distinct vertices
`x1,x2,x3`.

## Reduction of entries to five pentagon positions

For the hub, project each labelled entry to a vertex of `P0` as follows.

- An entry on `P0`, or through a tree rooted at a vertex `z` of `P0`, projects
  to `z`.
- An entry on `Ti`, at `xi`, or through a tree rooted on `Ti`, projects to
  `xi` and is forced to travel with the whole petal `Ti`.

This loses no relevant cyclic-order information. A triangle petal has only the
one core attachment `xi`; all routes from that petal to the rest of `A` use
`xi`. If both labelled arms enter through the same petal, both therefore stay
with that petal. Relative positions of roots around the triangle do not affect
the split of `P0`.

It remains to place three unlabeled distinct petal marks and the ordered roots
`b,c` on the five vertices of `P0`. Coincidences with each other and with petal
marks are allowed. Modulo the dihedral group of `P0`, there are exactly 26
configurations.

## Exhaustive interval certificate

For every one of the 26 configurations there is a nonempty proper consecutive
interval `J` of `P0` satisfying both conditions:

1. `J` contains the `c`-root, so `P1` and its whole connector arm are assigned
   to `J`;
2. after assigning `T4` according as the `b`-root lies in `J`, the number of
   triangles assigned to `J` is either one or two.

Here an internal petal `Ti` is assigned to `J` exactly when `xi` lies in `J`.
If a labelled root coincides with `xi` because its arm enters through `Ti`, the
root and `Ti` are consequently assigned together, as required.

The exact verifier independently enumerates all proper cyclic intervals and
chooses the first one satisfying these conditions. It also asserts that the
complement is nonempty and consecutive and that the `c`-root is owned by the
chosen interval. Among the 26 dihedral orbits it obtains

```text
20  certificates of type TP + TTT,
 6  certificates of type TTP + TT.
```

The complete orbit representatives and chosen intervals are printed by
`research/hexacyclic-e2-tttp-entry-census.py`. This includes `b=c`, roots at
petal cuts, consecutive or separated petal marks, and both possible cyclic
gap patterns for three marks on a pentagon.

To translate a certificate into territories, cut the two cycle edges forming
the boundary of `J`. Give `J`, every petal whose mark lies in `J`, the `c`-arm
and `P1`, and the `b`-arm with `T4` when its root lies in `J`, to one territory.
Give the complementary interval and all remaining petals and arms to the other
territory. Assign every hanging tree wholly to the territory owning its unique
core attachment.

Both intervals are nonempty and proper. They partition every vertex of `P0`;
in particular, each shared cut `xi` has exactly one owner. Each arm is assigned
with its actual entry root, so both territories are connected. They are induced
because the only crossing edges of `P0` are the two boundary edges and bridge
arms have no second attachment. Thus these are legal induced territories, not
only symbolic cycle packets.

For a `TP+TTT` certificate the packet ledger gives

`sigma(G) > (1-delta)+0>0`.

For a `TTP+TT` certificate it gives

`sigma(G) > 0+1>0`.

This proves the stated E2 result.

## Reproduction

Run

```bash
python research/hexacyclic-e2-tttp-entry-census.py
```

The script asserts the incidence counts `{1:1,2:3,3:4}`, that seven trees have
an intersecting triangle pair, that the unique remaining tree is the
three-petal hub, and that all 26 ordered-entry orbits receive one of the two
legal packet certificates above.
