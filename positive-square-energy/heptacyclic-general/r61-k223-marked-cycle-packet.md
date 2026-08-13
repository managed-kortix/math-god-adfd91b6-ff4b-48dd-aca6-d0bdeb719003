# R61-K223 marked-cycle packet

## Theorem

Let `B` be the canonical all-unit rank-six kernel `K223`, with edge set

`03,04,05,12,14,15,24,25,34,35,45`.

Let an arbitrary cycle `Q` meet `B` in one marked cut vertex `x`, and attach
arbitrary finite rooted trees at all vertices of `B union Q`. Then

`sigma(G)=s^+(G)-|V(G)|>0`.

Thus the complete `R61-K223` residual is closed, for every marked cut and every
cycle length.

## Marked-cut orbits

The complement of `K223` is the four-cycle with edges `01,02,13,23`, together
with the two isolated vertices `4,5`. Hence the automorphism group has exactly
two vertex orbits:

| orbit | vertices | degree | representative |
|---|---|---:|---:|
| `L` | `0,1,2,3` | 3 | `0` |
| `H` | `4,5` | 5 | `4` |

For both representatives use the induced partition

`A={0,3,4,5}`, `T={1,2}`.

The marked cut belongs to `A`, the graph induced by `A` is an actual `K4`, and
the graph induced by `T` is the nonempty tree consisting of edge `12`.
Transporting this partition by an automorphism supplies a partition for every
marked vertex. Equivalently, for any low vertex choose its partner on the same
edge of the induced matching `03+12`, together with `4,5`, as the `K4`; for a
high vertex either matching edge works.

## Coupled packet proof

Keep the marked cut `x`, the actual `K4` on `A_x`, and all rooted branches
owned there in one induced territory `U`. Put the two vertices of `T_x`, their
edge, and all rooted branches they own in a second induced territory `W`.
Boundary-open `Q` at `x`: the territory `V=Q-x`, together with every rooted
branch owned away from `x`, is a nonempty tree. The three territories are
disjoint and exhaustive. Edges between `A_x` and `T_x`, and the two cycle edges
from `x` to `V`, are crossing edges and are harmless for induced square-energy
superadditivity.

The established attachment-uniform actual-`K4` packet gives `sigma(U)>2`.
Both `W` and `V` are nonempty trees, so each has credit `-1`. Therefore

`sigma(G)>=sigma(U)+sigma(W)+sigma(V)>2-1-1=0`.

Every rooted branch is assigned exactly once, and the common cut of `K4` and
`Q` remains only in `U`; no cut vertex is copied. The argument is independent
of the length of `Q`.

## Exact audit

Run

```text
python3 research/r61-k223-marked-cycle-packet-verifier.py
python3 -O research/r61-k223-marked-cycle-packet-verifier.py
```

The verifier reconstructs the graph from the canonical bit row, enumerates its
full automorphism group and marked-vertex orbits, and checks a valid marked
`K4`/nonempty-tree partition for every vertex. It also rejects mutations of the
row, orbit ledger, partitions, and packet debits.
