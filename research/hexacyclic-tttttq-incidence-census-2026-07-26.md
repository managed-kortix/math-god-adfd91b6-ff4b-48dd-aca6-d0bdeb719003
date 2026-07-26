# Exact symbolic incidence census for fully shared `TTTTTQ`

## Scope

This note records a finite, exact census and a deliberately conservative packet
test for a fully shared six-cycle cactus with five equal triangle symbols `T`
and one distinguished symbol `Q=C_q`. It is a computational proof object for
structural work. It is **not** a hexacyclic theorem, does not claim that the DNN
reduction is exhaustive, and does not claim that every induced-territory detail
needed by a future global argument has been proved.

The word "symbolic" is important when `q=3`: `Q` is still kept as a distinguished
color. Thus the census quotients by `S_5` on the five `T` nodes, not by `S_6`.
Cut nodes are uncolored and freely permuted. This is the color-preserving census
needed to track a designated cycle through later packet operations.

The executable is

```bash
python research/hexacyclic-tttttq-incidence-census.py
```

It uses only the Python standard library and contains assertions for every
count and exception stated below.

## Objects enumerated

Let `I` be the bipartite incidence tree with six cycle nodes and `c` shared-cut
nodes. A cut node represents a vertex lying on at least two cycles. Since `I`
is a tree,

`|E(I)|=c+5`, and `sum_x(deg(x)-1)=5`,

where the sum is over cut nodes. Consequently `1<=c<=5`. The enumerator imposes
all of the following conditions directly:

1. every cycle node has positive degree;
2. every cut node has degree at least two;
3. the graph is a connected acyclic bipartite graph;
4. every `T` node has degree at most three;
5. the distinguished `Q` node has degree at most `q`;
6. isomorphisms may permute the five `T` nodes and all cut nodes, but must fix
   the `Q` color.

Only five shared-cut incidences can occur on any cycle, so the capacity regimes
are exactly `q=3`, `q=4`, and `q>=5`. No later value of `q` changes the abstract
incidence census.

For auditability, generation is by ordered cut neighborhoods with total degree
`c+5`, followed by the tree and cycle-cap tests. Deduplication uses the standard
center-rooted canonical code of a vertex-colored tree. Canonical edge sets for
reported exceptions are independently minimized over all `5! c!` allowed
label permutations.

## Exact counts

The numbers of color-preserving incidence trees are:

| `Q` capacity | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | total |
|---|---:|---:|---:|---:|---:|---:|
| `q=3` | 1 | 6 | 20 | 27 | 14 | 68 |
| `q=4` | 1 | 6 | 20 | 28 | 15 | 70 |
| `q>=5` | 1 | 6 | 20 | 28 | 16 | 71 |

The two trees admitted at capacity four but excluded at capacity three are:

```text
c=4: ((0,6),(1,6),(2,7),(3,8),(4,9),(5,6),(5,7),(5,8),(5,9))
c=5: ((0,6),(0,7),(1,6),(2,8),(3,9),(4,10),(5,7),(5,8),(5,9),(5,10))
```

The single additional capacity-five tree is the five-petal `Q` hub:

```text
c=5: ((0,6),(1,7),(2,8),(3,9),(4,10),(5,6),(5,7),(5,8),(5,9),(5,10))
```

Here cycle nodes `0,...,4` are `T`, node `5` is `Q`, and cut nodes begin at
`6`. These labels are only canonical display labels.

## Conservative one-cycle split test

For every cycle node `C` of incidence degree at least two, the script deletes
`C` from the abstract tree and records the symbolic cycle multiset in every
branch. This is the combinatorial input to the established consecutive-interval
cycle split: the marks on `C` receive nonempty proper cyclic intervals, and the
split cycle contributes path fragments rather than a retained cycle or a
separate tree cost.

The acceptance test uses only these established packet facts:

- `T` is strictly positive, `TT` has surplus `>1`, and connected all-triangle
  packets with three, four, or five cycles are positive by the established
  tricyclic, tetracyclic, and pentacyclic results (with the stronger audited
  all-triangle estimates where applicable);
- `TQ` is positive for every parity of `q`: hostile `q=1 mod 4` has the bound
  `>1-delta_q`, while even and `3 mod 4` cycles are nonhostile;
- a generic `TTQ` branch is nonnegative by the established tricyclic result,
  so a separate strict all-triangle branch supplies strictness;
- `TTTQ` and `TTTTQ` branches are positive by the established tetracyclic and
  pentacyclic results;
- if a split triangle leaves a singleton `Q` branch, the other four triangles
  occupy at most two branches because a triangle has incidence degree at most
  three. One branch therefore contains at least `TT`, whose `>1` credit absorbs
  the hostile singleton loss `delta_q<1`; `q=3,4` are no worse.

No prospective hexacyclic margin, unproved entry-sensitive lemma, or numerical
surplus guess is admitted. The test is qualitative: it certifies a positive sum
for the branch packets, but it does not assign unused external opening credit.

## Split results and the exact exception

Every non-bouquet tree has at least one accepted one-cycle branch split. Counts
resolved by `c` are therefore:

| `Q` capacity | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | resolved total |
|---|---:|---:|---:|---:|---:|---:|
| `q=3` | 0 | 6 | 20 | 27 | 14 | 67 |
| `q=4` | 0 | 6 | 20 | 28 | 15 | 69 |
| `q>=5` | 0 | 6 | 20 | 28 | 16 | 70 |

Counting trees by which color can furnish at least one accepted split gives:

| `Q` capacity | `T` only | `Q` only | both | neither |
|---|---:|---:|---:|---:|
| `q=3` | 36 | 4 | 27 | 1 |
| `q=4` | 36 | 5 | 28 | 1 |
| `q>=5` | 36 | 6 | 28 | 1 |

The unique one-cycle-split exception in every capacity regime is the universal
six-cycle bouquet:

```text
c=1: ((0,6),(1,6),(2,6),(3,6),(4,6),(5,6))
```

Every cycle node is a leaf of the incidence tree, so deleting any one cycle
node leaves only one branch. There is no multi-branch interval split to test.
This is a structural exception to the one-cycle split mechanism, not evidence
of a spectral exception.

There is a separate already-ledgered candidate construction for this bouquet:
open a private vertex of `Q` and a private vertex of one triangle. The retained
four-triangle bouquet has surplus `>3`, while the two opened tree territories
cost two. This observation is not folded into the one-cycle census counts and
is not promoted here to a hexacyclic theorem statement.

## What the census does not establish

The abstract interval split still has to be instantiated with all attached
trees assigned to their unique core attachments; that standard construction is
not re-proved by the script. The census concerns one fully shared-cut cluster
only. It says nothing by itself about disconnected shared-cut clusters, bridge
territories, the completeness of the candidate residual families, or the DNN
reduction. Finally, a positive branch sum cannot automatically pay a later tree
opening: only the quantitative rows in the existing packet ledger may be used
for that purpose.

Accordingly, the exact output should be used as a finite structural audit and
as a list of safe first moves, not as a theorem claim.
