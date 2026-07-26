# Fully shared pentacyclic residual `{T,T,T,P,P}`

## Result

Let `G` be a cactus whose five cyclic blocks are three triangles `T` and two
pentagons `P`, and suppose those blocks form one shared-cut cluster. Then

`s+(G) > |V(G)|`.

This includes arbitrary trees attached anywhere. The proof below uses only
induced-subgraph superadditivity and the established packet ledger. Write
`sigma(H)=s+(H)-|V(H)|` and `delta=sec(pi/5)-1=sqrt(5)-2`. We use

- `sigma(T)>0`, `sigma(P)>=-delta`;
- `sigma(TT)>1`, `sigma(TP)>1-delta`;
- `sigma(PP)>=0`, `sigma(TTP)>=0`, `sigma(TPP)>3/2`;
- if three triangles form a connected shared-cut cluster, then
  `sigma(TTT)>2` (the packing-two phase bound);
- every tetracyclic cactus has positive surplus.

The last bound is available but is not needed in the final accounting.

## Incidence tree

Let `I` be the bipartite tree whose cycle nodes are the five cyclic blocks and
whose cut nodes are the vertices lying in at least two cyclic blocks. If there
are `c` cut nodes, then

`|E(I)|=c+4`, and sum over cut nodes of `(degree-1)` equals `4`.

Every cut node has degree at least two, so `c<=4`. A triangle cycle node has
degree at most three and a pentagon cycle node degree at most five, because
distinct incidences use distinct vertices of that cycle.

## Cycle-splitting lemma

Suppose a cycle node `C` has degree at least two in `I`. Delete that node from
`I`, obtaining branches `J_1,...,J_k`. List the corresponding shared vertices
in cyclic order on `C`. Partition `V(C)` into `k` nonempty consecutive cyclic
intervals, one containing each shared vertex, and give an interval to its
branch. Each interval is a proper path. Give every off-core tree component
wholly to the territory containing its unique core attachment.

The resulting territories are vertex-disjoint, connected, and induced. Their
remaining cycle multisets are exactly those in the branches `J_i`; the split
cycle contributes only path fragments. Thus any positive sum of packet
surpluses for the branch multisets proves `sigma(G)>0`.

The same construction may merge two cyclically adjacent marked vertices into
one interval while leaving every other marked vertex in its own interval. This
will be used once below.

## Complete packet classification

Encode a branch multiset by `(t,p)`. Splitting an internal triangle leaves a
partition of `(2,2)`. The packet ledger is positive for precisely the following
partition types needed by the incidence census:

| branches after splitting `T` | lower surplus |
|---|---:|
| `PP + TT` | `>1` |
| `T + TPP` | `>3/2` |
| `TP + TP` | `>2-2delta` |
| `P + P + TT` | `>1-2delta` |
| `P + T + TP` | `>1-2delta` |
| `PP + T + T` | `>0` |

Splitting an internal pentagon leaves a partition of `(3,1)`. The positive
types are

| branches after splitting `P` | lower surplus |
|---|---:|
| `P + TTT` | `>2-delta` |
| `T + TTP` | `>0` |
| `TP + TT` | `>2-delta` |
| `P + T + TT` | `>1-delta` |
| `T + T + TP` | `>1-delta` |

Here a displayed strict zero means that a strict triangular packet is added to
a nonnegative packet. Since `delta=sqrt(5)-2<1/2`, every displayed quantity is
positive.

For completeness, enumerate bipartite trees satisfying the excess equation,
minimum cut degree two, and the cycle-degree caps, modulo permutations of the
three `T` nodes, the two `P` nodes, and the cut nodes. The numbers for
`c=1,2,3,4` are respectively

`1, 7, 18, 14`.

Thus there are 40 colored incidence trees. A one-cycle split of one of the
types in the two tables resolves respectively

`0, 6, 17, 13`

of them. The exact enumerator
`research/pentacyclic-tttpp-incidence-census.py` checks the degree conditions,
tree condition, color-preserving canonicalization, all possible split cycles,
and all branch multisets. It leaves exactly the following four trees. This is
also a compact exhaustive leaf/degree classification.

1. **Five-cycle bouquet:** one cut `x` is incident with all five cycles.
2. **A `(4,2)` cut pair:** `x` meets `T1,T2,T3,P1`, while `y` meets `T1,P2`.
3. **A `(3,2,2)` cut tree:** `x` meets `T1,T2,T3`, `y` meets `T1,P1`, and
   `z` meets `T2,P2`.
4. **Pentagon hub:** `P1` meets `T1,T2,T3,P2` at four distinct degree-two
   cuts.

The first three are exactly the cases in which both pentagons are leaf cycle
nodes and the three triangles remain one connected shared-cut cluster after
the pentagons are opened. The fourth is the sole bad raw split type
`P+T+T+T`.

## Closing the four exceptions

In each of cases 1--3, choose a private vertex `v_i` on each leaf pentagon
`P_i`. Let `F_i` contain `v_i` and every off-cycle tree branch rooted there,
and put all other vertices in `H`. Each `F_i` is a tree, so
`sigma(F_i)=-1`. Each `P_i-v_i` is a path containing its unique shared cut,
so `H` is connected. Its only cycles are the three triangles, which form a
connected shared-cut cluster. At least two therefore meet, its cycle-packing
number is at most two, and the phase bound gives `sigma(H)>2`. Hence

`sigma(G) >= sigma(H)+sigma(F_1)+sigma(F_2) > 2-1-1=0`.

In case 4, cyclically order the four marked vertices of the hub `P1`. The mark
belonging to `P2` has a neighboring mark belonging to some triangle, say `T1`.
Split `P1` into three proper consecutive intervals: one interval contains
those two neighboring marks, and the other two contain the marks of `T2` and
`T3` separately. This gives induced territories of types `TP`, `T`, and `T`.
Consequently

`sigma(G) > (1-delta)+0+0 > 0`.

All 40 incidence trees are therefore covered, and induced-subgraph
superadditivity proves `s+(G)>|V(G)|`.

## Reproduction

Run

```bash
python research/pentacyclic-tttpp-incidence-census.py
```

The expected output reports `{1: 1, 2: 7, 3: 18, 4: 14}` and the four trees
listed above.
