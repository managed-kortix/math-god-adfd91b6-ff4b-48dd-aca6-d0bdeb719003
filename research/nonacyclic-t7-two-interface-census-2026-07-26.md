# Exact marked two-interface census for a seven-triangle cluster

**Date:** 2026-07-26

## 1. Scope and verdict

Write

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5,
delta=sqrt(5)-2.
```

This is the marked rank-nine interface census relevant to a connected
seven-triangle cluster carrying two labelled connector entries, one for each
external pentagon. It enumerates every color-preserving triangular incidence
tree and every ordered pair of cyclic-hull interface positions, including
coincident interfaces. It then searches exact successive triangle-router
splits with the rank-uniform state and packet ledger of
`research/rank-uniform-triangular-router-interface-theorem-2026-07-26.md`.
The two-interface model is deliberately stronger than the one-interface
`T^7P | P` last-bridge model: it forgets any pentagon already inside a cluster
and treats both pentagons as external labelled demands.

The exact result is

```text
48 triangular incidence trees,
10800 labelled placements before automorphisms,
3188 canonical marked rows,
3182 accepted by the uniform router ledger,
6 canonical residual rows,
6/6 closed by explicit interface-aware packetizations.
```

All six residuals lie on the single common-cut seven-triangle bouquet. No
nonbouquet marked incidence type survives. The weakest replacement ledger is

```text
1-2delta=5-2sqrt(5)>0.
```

This is a finite structural certificate. It relies on the cited analytic
packet inequalities and is not itself a proof of those inequalities.
The external connectors are kept through the uniform census. The `e` charge
below measures only a private interval after its demand is charged separately;
the replacement table instead rejoins each connector to its actual pentagon
packet.

## 2. Enumerated marked objects

The unmarked object is a bipartite cycle-cut incidence tree with seven triangle
nodes. Cut nodes have degree at least two and triangle nodes degree at most
three. Generation is the exhaustive cycle-leaf deletion/insertion recurrence
used by the rank-nine fully shared census.

An interface position is either:

* a shared cyclic cut; or
* an actual private vertex of a triangle.

The interfaces are labelled `A` and `B`; their ordered positions may coincide.
Private triangle positions are retained as local ports before canonicalization,
so the census distinguishes coincident marks from marks on two distinct private
vertices of one triangle. A center-rooted code canonicalizes the incidence
tree together with both labels and all unmarked local ports.

The exact completeness counts are:

```text
unmarked incidence classes                         48
ordered labelled placements before automorphisms 10800
canonical marked classes                          3188
```

The executable freezes the SHA-256 digests of all canonical codes:

```text
all rows: c317bf471f41debbdce7c09c3eb3d22359797bfb7a270bbd04c9fde3a41008ec
residuals: 93769a588fcbcd24c1a1ce54b820c047b2929c30c838828b6d972e1d2e0d76b3
```

## 3. Exact router automaton and ledger

For a retained triangular territory, the program may sacrifice a triangle
router with two or three occupied local ports. Each incidence branch receives
one proper interval. A private interface on the router is an additional port;
coincident labels at the same private vertex remain one port and one owner.
Splits recurse only within retained incidence branches, so every later split is
an induced refinement and every cyclic cut has one owner.

If the final retained triangular packets have sizes `r_1,...,r_k`, define

```text
c = sum_i b(r_i),
b(1),...,b(7) = 0,1,2,3,2,1,0,
e = number of naked private-interface intervals,
score = c-e.
```

The two external pentagons are separate unicyclic packets. Thus every ordinary
accepted row has the exact symbolic ledger

```text
sigma(G) > score-2delta.
```

Since `delta<1/4`, the accepting condition is the integer test `score>=1`.
Equivalently the finite rank-uniform state is

```text
(p,e,min(3,c),t),  p=2,
```

where `t=1` records retained strict triangular packets. No floating-point
arithmetic is used.

The best-score distribution is:

| score | rows |
|---:|---:|
| 0 | 6 |
| 1 | 10 |
| 2 | 91 |
| 3 | 1037 |
| 4 | 2044 |

The exact best state distribution is:

| state `(p,e,c,t)` | rows |
|---|---:|
| `(2,0,0,1)` | 2 |
| `(2,0,2,1)` | 42 |
| `(2,0,3,1)` | 2807 |
| `(2,1,1,1)` | 3 |
| `(2,1,2,1)` | 8 |
| `(2,1,3,1)` | 323 |
| `(2,2,2,1)` | 1 |
| `(2,2,3,1)` | 2 |

Best certificates use no split in 2 rows, one split in 3134 rows, and two
successive splits in 52 rows. Hence the census explicitly exercises both
rank-uniform router transitions and never needs more than two refinements.

### Interval realization of the 3182 ordinary certificates

The finite marks in a canonical row are not merely incidence-tree labels. Each
cut mark denotes that actual shared graph vertex. Each private mark denotes the
specified actual private triangle vertex. The connector path from the
corresponding external pentagon first meets the cyclic hull at that vertex.

For every split recorded by the executable, the marked triangle has two or
three distinct owner positions. Give two owners intervals of sizes `1,2`, or
give three owners the three singleton vertices, exactly as in the labelled
triangle-router separator theorem. A cut-position interval owns that cut, its
entire retained incidence branch, and every off-hull tree attached there. A
private-position interval owns that private vertex, the complete connector path
ending there, its external pentagon, and every tree attached along that path.
Coincident labels are one owner and their two connector paths stay together.

This assignment is a graph vertex partition: every triangle-router vertex is
in one proper interval; every retained incidence branch follows its unique
marked cut; and every off-hull component follows its unique first attachment.
Consequently the resulting territories are connected, induced, disjoint, and
exhaustive. At a second split, only one already induced territory is refined,
so a previously owned cut has exactly one descendant owner. Thus the retained
cycle profiles and the `e` naked private intervals in each of the 3182 accepted
rows are realized by actual induced graph packets, not only by the canonical
marks. The two external pentagons remain the separately charged `P` packets of
the ordinary ledger; the interval assignment realizes the connector remnants
after those demands are separated. The executable materializes every split's
active cycle set, interval sizes, position owners, and retained cycle sets, and
asserts this realization for all 3188 rows, including the ordinary 3182 that
pass the integer acceptance test.

## 4. Six canonical residuals

All seven triangles share cut `7`:

```text
edges=((0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7)).
```

Up to bouquet automorphisms, the six ordered marked types are:

| code | interface `A` | interface `B` | ordinary best state | ordinary score |
|---|---|---|---|---:|
| R1 | common cut | common cut | `(2,0,0,1)` | 0 |
| R2 | common cut | private on `T0` | `(2,1,1,1)` | 0 |
| R3 | private on `T0` | common cut | `(2,1,1,1)` | 0 |
| R4 | same private vertex of `T0` | same private vertex | `(2,1,1,1)` | 0 |
| R5 | private vertex of `T0` | other private vertex of `T0` | `(2,0,0,1)` | 0 |
| R6 | private vertex of `T0` | private vertex of `T1` | `(2,2,2,1)` | 0 |

Their numbers of labelled placements inside the canonical bouquet are
`1,14,14,14,14,168`, respectively. The order distinction between R2 and R3 is
necessary because `A` and `B` name different external pentagons.

These are residuals only for the deliberately uniform ordinary ledger that
first charges both pentagons separately and treats a naked router interval as
`-1`. The common-cut lock explains why no separator-only move improves R1.

## 5. Explicit replacement splits

The six rows close as follows. Every interval owns its connector and all trees
attached to that connector; the packet labels below therefore include arbitrary
off-hull trees.

| rows | operation and final packets | exact ledger |
|---|---|---:|
| R1 | open either remote `P`; retain the other arm with the packing-one `A_7` bouquet | `>6-delta` |
| R2-R3 | split the privately entered triangle; attach its pentagon to that private interval, yielding `P +` common-cut `T^6P` | `>6-2delta` |
| R4 | split `T0` at the common cut and coincident private port; the private interval carries the connected `PP` packet and the cut owner carries `A_6` | `>1` |
| R5 | split `T0` into its three singleton ports; the two private intervals carry `P,P`, and the cut owner carries `A_6` | `>1-2delta` |
| R6 | split `T0` and `T1` successively; their private intervals carry `P,P`, and the common-cut owner carries `A_5` | `>2-2delta` |

For R4, both connector paths meet the same private vertex and their pentagons
form one connected two-pentagon cactus packet, so the established `PP>0`
certificate applies. For R5 and R6 the entries are distinct and the two
pentagons remain separate. The `A_6` and `A_5` credits are respectively one and
two. The weakest value is R5:

```text
1-2delta=5-2sqrt(5)>0,
```

with exact positivity equivalent to `25>20`.

The residual verifier now stores these six rows as complete recipes rather than
as descriptive strings. For each labelled interface it records the actual entry
position, symbolic full connector path, external pentagon, and final packet
owner. For each router it records the active triangular territory, proper
interval sizes, and the cut/private position owning each retained branch. It
also records every final retained cycle profile, the unique owner of common cut
`7`, the order of the two refinements in R6, and an exact pair `(credit, number
of delta deficits)`. The verifier checks exhaustive disjoint branch ownership,
unique cut ownership, connector-to-packet assignment, complete retained-cycle
coverage after router removal, and positivity by squaring the relevant integer
inequality, with no floating-point arithmetic.

For R1 the opened pentagon contributes the exact tree cost `-1`.  The retained
territory has seven triangles of vertex-packing number one and one pentagonal
arm joined at their common cut, so the established rooted packing-one theorem
gives `>7-delta` before that cost.  This is not a common-cut `T^7PP` packet:
the remote pentagons do not contain the triangular hub.

## 6. Reproduction

Run from the repository root with Python 3.10 or newer:

```bash
python3 research/nonacyclic-t7-two-interface-census.py
python3 research/nonacyclic-t7-two-interface-census.py --list-residuals
```

The first command prints and asserts all census totals, state counts, score
counts, split counts, interval realizations, residual recipes, exact margins,
and canonical digests. The second additionally prints the six complete marked
codes, incidence signatures, edge lists, ordinary retained cycle profiles,
interval owners, connector paths and pentagon assignments, cut owners,
sequential splits, and replacement packetizations.

The script uses only the Python standard library. Exact integer arithmetic is
used for the uniform ledger; radical expressions appear only as symbolic final
bounds whose positivity is checked by the stated exact comparisons.
