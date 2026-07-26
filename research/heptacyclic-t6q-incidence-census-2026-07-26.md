# Safe exact incidence census for fully shared `T^6Q`

## Scope and status

This note records an exact color-preserving census of the fully shared
seven-cycle incidence trees with six interchangeable triangles `T` and one
distinguished cycle `Q=C_q`. It also records a conservative one-cycle split
test using only packet bounds established through rank six. It is a finite
structural audit, not a heptacyclic theorem claim.

The executable certificate is

```bash
python research/heptacyclic-t6q-incidence-census.py
```

It uses only the Python standard library and asserts every count, split-color
count, and exception stated here.

When `q=3`, the symbol `Q` remains distinguished. Thus the quotient is by
`S_6` on the six `T` nodes and not by `S_7`. Cut nodes are uncolored. This is
the color-preserving census needed to follow a designated cycle through a
split.

## Objects and structural compression

For `c` shared cyclic cuts, the incidence tree has seven cycle nodes, `c` cut
nodes, and

`|E(I)|=c+6`, with `sum_x(deg(x)-1)=6`.

Every cut has degree at least two, every cycle has positive degree, each `T`
has degree at most three, and `Q` has degree at most `q`. Hence `1<=c<=6`.

The script avoids direct generation of every rank-seven neighborhood tuple.
Every such bipartite tree has a cycle-node leaf, and at most one leaf can be
`Q`, so it has a leaf `T`. Delete one leaf `T` and then suppress its incident
cut if that cut has become degree one. The result is an established
rank-six `T^5Q` incidence tree. Conversely, every rank-seven object is obtained
from a rank-six object by exactly one of these inverse operations:

1. attach a new leaf `T` to an existing cut; or
2. insert a new degree-two cut between a new leaf `T` and an existing cycle.

After each extension the center-rooted color code canonicalizes the whole
tree. This leaf-extension construction is exhaustive but is materially smaller
than a direct seven-cycle product over cut neighborhoods. It also reuses the
previously asserted rank-six counts `68,70,71` as its seed census.

Only six cut incidences can occur on `Q`, so the abstract capacity regimes are
`q=3,4,5,6,>=7`; the last two have the same incidence trees, although their
safe packet ledgers differ because `q=6` is nonhostile while `q>=7` is treated
uniformly over all parities.

## Exact color-preserving counts

| `Q` capacity | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | total |
|---|---:|---:|---:|---:|---:|---:|---:|
| `q=3` | 1 | 8 | 33 | 71 | 74 | 29 | 216 |
| `q=4` | 1 | 8 | 33 | 73 | 77 | 32 | 224 |
| `q=5` | 1 | 8 | 33 | 73 | 78 | 33 | 226 |
| `q=6` | 1 | 8 | 33 | 73 | 78 | 34 | 227 |
| `q>=7` | 1 | 8 | 33 | 73 | 78 | 34 | 227 |

These are isomorphism classes preserving the `T/Q/cut` colors. They are not
counts of cyclic orders, graph realizations, attachment trees, or choices of
entry vertices.

## Safe one-cycle test

For every cycle node of incidence degree at least two, delete that node and
record the cycle multiset in each resulting branch. The intended realization
assigns the incident marks nonempty proper consecutive intervals of the split
cycle. The split cycle is destroyed into path fragments, so this operation has
no separate `-1` tree charge.

The acceptance ledger uses the following exact rational proof margins. Here a
strict sign belongs to the cited packet bound; it is not a claim that the
displayed rational is the optimal infimum.

| retained branch | rational margin used | status |
|---|---:|---|
| `T` | `>0` | strict unicyclic triangle |
| `TT` | `>1` | established bicyclic packet |
| `TTT` | `>2` | established all-triangle packet |
| `TTTT` | `>3` | established four-triangle shared packet |
| `T^5` | `>2` | rank-five leaf-opening packet |
| `T^6` | `>1` | rank-six leaf-opening packet |
| `Q`, `q=3` | `>0` | `Q` is a triangle |
| `Q`, `q=4,6` | `>=0` | nonhostile even cycle |
| `Q`, `q=5` or uniformly `q>=7` | `>-1` | safe rational weakening of `>=-delta_q`, `delta_q<1` |
| `TQ` | `>0` | established mixed bicyclic packet |
| `TTQ` | `>=0` | generic tricyclic packet |
| `T^kQ`, `3<=k<=5` | `>0` | established rank-four through rank-six result |

Margins add as exact `fractions.Fraction` values. A split is accepted precisely
when the sum is positive, or is zero with at least one strict summand. In
particular, an isolated hostile `Q` is accepted only if another branch supplies
strict rational credit at least one. No qualitative packet is silently used to
pay a positive cost.

## Split census

Every non-bouquet incidence tree has a safe one-cycle split under this ledger.
Thus the safe counts by cut number are the exact census rows with the `c=1`
entry removed:

| `Q` capacity | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | safe total |
|---|---:|---:|---:|---:|---:|---:|---:|
| `q=3` | 0 | 8 | 33 | 71 | 74 | 29 | 215 |
| `q=4` | 0 | 8 | 33 | 73 | 77 | 32 | 223 |
| `q=5` | 0 | 8 | 33 | 73 | 78 | 33 | 225 |
| `q=6` | 0 | 8 | 33 | 73 | 78 | 34 | 226 |
| `q>=7` | 0 | 8 | 33 | 73 | 78 | 34 | 226 |

The availability of split-cycle colors is:

| `Q` capacity | `T` only | `Q` only | both | neither |
|---|---:|---:|---:|---:|
| `q=3` | 110 | 6 | 99 | 1 |
| `q=4` | 110 | 8 | 105 | 1 |
| `q=5` | 110 | 9 | 106 | 1 |
| `q=6` | 110 | 10 | 106 | 1 |
| `q>=7` | 110 | 10 | 106 | 1 |

For each resolved tree, maximize the rational part of the accepted margin,
breaking a tie in favor of strictness. The resulting exact certificate-margin
distribution is:

| regime | `>0` | `>1` | `>2` | `>3` | `>4` |
|---|---:|---:|---:|---:|---:|
| `q=3` | 6 | 13 | 66 | 89 | 41 |
| `q=4` | 6 | 13 | 74 | 89 | 41 |
| `q=5` | 6 | 26 | 86 | 66 | 41 |
| `q=6` | 7 | 15 | 74 | 89 | 41 |
| `q>=7` | 7 | 26 | 86 | 66 | 41 |

These margins are credits of the displayed branch packetization. They do not
include any later external opening and do not assert optimality among all
possible decompositions.

## Exact exception

The unique tree with no multi-branch one-cycle split in every regime is the
seven-cycle bouquet:

```text
X(Q()T()T()T()T()T()T())
```

All cycle nodes are leaves at one common cut, so deleting any cycle node leaves
one branch. This is an exception to the tested operation, not a spectral
exception. A separate already-audited sacrifice opens `Q` and two triangles at
private vertices; the four retained triangles remain a common-cut packet with
margin `>3`, exactly paying the three nonempty tree territories and leaving a
strictly positive ledger. That construction is reported separately and is not
counted as a one-cycle split.

## Safety boundaries

The census classifies abstract incidence trees only. A later proof must still
instantiate consecutive intervals, give every shared cut one owner, and assign
each hanging tree wholly to its unique core attachment. The script does not
enumerate cyclic orders or external entries. It also says nothing about proper
shared-cluster partitions or the other heptacyclic residual family `T^5PP`.

Most importantly, the table certifies a safe first split with a stated packet
margin. It does not turn qualitative positivity into opening credit, does not
establish a global induced partition in an arbitrary surrounding cactus, and
makes no theorem claim for heptacyclic cacti.
