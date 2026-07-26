# Independent verdict on the fully shared heptacyclic censuses

## Verdict

**FAIL as an exact two-script census package; PASS for the `T^5PP` script and
for the separate fully shared structural closure.**

The `T^5PP` executable passes direct-enumeration, quotient, ledger, and
exception checks. Its `560` colored incidence classes and three ordinary-split
exceptions are correct.

The `T^6Q` leaf-extension executable is exhaustive in the sense that it omits
no admissible incidence tree, but it also generates inadmissible trees. In the
inverse operation that inserts a new degree-two cut between the new leaf
triangle and an old cycle, it enforces the `Q` capacity but does not enforce the
degree-three capacity of an old triangle. Consequently it admits `25` colored
classes having a triangle of incidence degree four. The asserted totals,
split-color support, and margin distributions in that script and its companion
note are therefore not exact censuses of realizable cactus incidences.

This defect does not undermine the simpler fully shared `T^6Q` leaf-or-split
proof, nor the analogous `T^5PP` dichotomy, in
`research/heptacyclic-residual-sacrifice-splitting-lemmas-2026-07-26.md`.
Those arguments close every realizable fully shared incidence tree without
depending on the erroneous `T^6Q` counts.

## Reproduction

I ran both executables unchanged:

```bash
python research/heptacyclic-t6q-incidence-census.py
python research/heptacyclic-tttttpp-incidence-census.py
```

They reproduce all of their embedded assertions. This confirms internal
reproducibility, but the assertions in the first script encode the overcount.

I then generated rank-seven cut-neighborhood multisets directly, using the
identity

```text
sum_x (deg(x)-1)=6,
```

required every cycle to occur, imposed degree at most three on every triangle
and the appropriate degree cap on `Q`, tested the bipartite graph for being a
tree, and canonicalized only after those tests. This direct route does not use
the rank-six leaf-extension construction.

## `T^6Q` generation defect

Every admissible `T^6Q` incidence tree does have a triangular cycle leaf. A
bipartite tree has at least two cycle-node leaves because every cut node has
degree at least two, and at most one such leaf can be the distinguished `Q`.
Deleting a triangular leaf and suppressing a newly unary cut gives a valid
`T^5Q` tree. Conversely, the two extension types in the script are the correct
inverse topological operations:

1. attach the new leaf triangle to an existing cut; or
2. join it to an old cycle through a new degree-two cut.

Thus there is no missing extension type. The error is a missing realizability
filter in type 2. At
`research/heptacyclic-t6q-incidence-census.py:179`, an old triangle is allowed
as the other endpoint even when it already has degree three. Lines 180--183
check saturation only when that endpoint is `Q`. The extension then raises the
old triangle's incidence degree to four, although a triangle has only three
vertices at which distinct cactus cuts can occur.

The invalid classes occur only at `c=4,5,6`:

| cut count | asserted classes | admissible classes | invalid degree-four classes |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 |
| 2 | 8 | 8 | 0 |
| 3 | 33 | 33 | 0 |
| 4 | 77 before `Q` filtering | 73 | 4 |
| 5 | 89 before `Q` filtering | 78 | 11 |
| 6 | 44 before `Q` filtering | 34 | 10 |

All `25` rejected color classes have maximum triangle degree exactly four; I
found no direct class absent from the extension output. The corrected exact
color-preserving counts are:

| `Q` capacity | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | total |
|---|---:|---:|---:|---:|---:|---:|---:|
| `q=3` | 1 | 8 | 33 | 71 | 74 | 29 | 216 |
| `q=4` | 1 | 8 | 33 | 73 | 77 | 32 | 224 |
| `q=5` | 1 | 8 | 33 | 73 | 78 | 33 | 226 |
| `q=6` | 1 | 8 | 33 | 73 | 78 | 34 | 227 |
| `q>=7` | 1 | 8 | 33 | 73 | 78 | 34 | 227 |

Reapplying the script's unchanged SAFE ledger to only the admissible direct
classes still resolves every nonbouquet. The corrected split-color support is:

| regime | `T` only | `Q` only | both | neither |
|---|---:|---:|---:|---:|
| `q=3` | 110 | 6 | 99 | 1 |
| `q=4` | 110 | 8 | 105 | 1 |
| `q=5` | 110 | 9 | 106 | 1 |
| `q=6` | 110 | 10 | 106 | 1 |
| `q>=7` | 110 | 10 | 106 | 1 |

The corrected best-margin distributions, in columns `>0,>1,>2,>3,>4`, are:

| regime | `>0` | `>1` | `>2` | `>3` | `>4` |
|---|---:|---:|---:|---:|---:|
| `q=3` | 6 | 13 | 66 | 89 | 41 |
| `q=4` | 6 | 13 | 74 | 89 | 41 |
| `q=5` | 6 | 26 | 86 | 66 | 41 |
| `q=6` | 7 | 15 | 74 | 89 | 41 |
| `q>=7` | 7 | 26 | 86 | 66 | 41 |

The unique ordinary-split exception remains the seven-cycle bouquet in every
regime. Therefore the qualitative statement "every nonbouquet has a SAFE
ordinary split" survives; only the claimed exact census tables fail.

## `T^5PP` completeness

The direct `T^5PP` generator correctly enumerates unordered cut-neighborhood
multisets. A cut of degree `d` contributes excess `d-1`; partitions of total
excess six cover every possible number and multiset of cut degrees. Repeated
neighborhoods are allowed where combinatorially possible and are subsequently
rejected if they create a cycle. Coverage, positivity of cycle degrees,
triangle capacity three, pentagon capacity five, and the tree test are all
applied before quotienting.

The resulting counts independently remain

```text
c=1,...,6: 1, 12, 68, 177, 211, 91; total 560.
```

The potentially delicate no-triangle-leaf case is present. There is exactly one
colored class with no triangular incidence leaf: the `c=6` alternating
cycle-cut path whose two endpoint cycle nodes are the pentagons. Both pentagons
have incidence degree one, and the ordinary SAFE test resolves this class. It
is not lost by a triangle-leaf assumption because this script uses direct
generation rather than leaf extension.

## Canonical forms and color quotients

The center-rooted code used by both scripts is a complete invariant of a
vertex-colored unrooted tree: rooted subtree codes classify rooted colored
trees, and rooting at the one or two centers removes the choice of root. The
colors distinguish cycle types from cut nodes, so no forbidden cycle/cut or
`T/P/Q` exchange is introduced.

I cross-checked every `T^5PP` class against the independently computed
lexicographically least edge representative under `S_5 x S_2 x S_c`. The
numbers of brute color orbits are exactly `1,12,68,177,211,91`, with one orbit
per center code. I likewise checked that every generated `T^6Q` center code is
distinct under brute `S_6 x S_c` relabeling. Keeping `Q` distinguished when
`q=3` intentionally gives a designated-cycle quotient rather than the smaller
uncolored `S_7` quotient; that convention is stated and consistently applied.

Canonicalization is therefore sound. It does not cure the `T^6Q` defect,
because the degree-four objects are genuine abstract colored-tree orbits even
though they are not realizable on triangular cycles.

## Bounds and SAFE decisions

I rechecked every numerical comparison and strictness rule used by both
acceptance ledgers.

- The all-triangle margins `b_1,...,b_6=0,1,2,3,2,1` are used only for one
  retained connected incidence component. Each inequality is strict.
- `P>-1/4`, `TP>3/4`, `TTP>7/4`, and `TPP>3/2` are valid rational weakenings of
  the cited estimates because `delta=sqrt(5)-2<1/4`.
- Strong `TTP` and `TTTP` credits in the `T^5PP` script are granted only after
  checking the required retained common cut or retained shared triangle pair.
- Generic tricyclic branches get only `>=0`; generic tetra-, penta-, and
  hexacyclic branches get strict qualitative positivity but zero rational
  credit. None is used to cancel a negative singleton pentagon.
- Exact `Fraction` addition and the rule "positive rational sum, or zero with a
  strict summand" preserve all endpoint distinctions.

For `T^6Q`, direct admissible classes retain exactly one exception. For
`T^5PP`, the script correctly records all `3920=7*560` cycle choices, the SAFE
choice distribution `3,67,211,206,67,6`, and exactly three exceptions. I found
no accepted split whose retained-incidence hypothesis fails.

## Realizability and repairs

For an abstract incidence tree satisfying the cycle capacities, realizability
as a fully shared cactus is straightforward: assign distinct vertices of each
cycle to its incident cut nodes and identify all cycle vertices adjacent to
each cut node. The incidence-tree condition prevents a second intersection or
a cyclic chain of block identifications. Conversely, distinct cut nodes on a
cycle require distinct cycle vertices, which is precisely why the omitted
triangle capacity check is essential.

The ordinary split realization is also sound. Deleting an internal cycle node
orders its distinct cut marks cyclically; one nonempty proper consecutive path
interval per mark gives one owner to every mark, and each incidence component
receives its corresponding interval. Hanging trees follow their unique
attachment. No additional `-1` opening charge occurs because the split cycle is
destroyed rather than retained as a cycle.

The exception repairs in the separate sacrifice/splitting note pass:

1. For the `T^6Q` bouquet, `Q` is an incidence leaf and has a private vertex.
   Opening only `Q` costs one and leaves a connected six-triangle shared
   cluster with margin `>1`, hence a strict net `>0`. The older three-opening
   repair is valid but unnecessarily weaker.
2. In each of the three `T^5PP` exceptions, both pentagons are incidence
   leaves. Each has private vertices; the two opening territories are disjoint,
   and deleting both leaf nodes leaves the five triangles in one connected
   incidence cluster. The exact ledger is `>2-2=0`.
3. More generally, an internal `Q` can be split into positive all-triangle
   branches. An internal pentagon can be split so that either its companion
   pentagon has a triangle partner and another branch is strict, or the
   companion is singleton and five triangles in at most four remaining
   branches force a `TT`-or-larger margin `>1` against loss `<1`.

These are induced-territory constructions with explicit cut ownership and do
not rely on qualitative positivity paying a fixed opening cost.

## Required correction

Before the `T^6Q` executable or note is cited as an exact census, the new-cut
extension must reject an old triangle already at degree three, and every
embedded expected count, support count, and margin distribution must be updated
to the corrected tables above. A direct-generation regression check should be
kept alongside the compressed extension test. With that repair, both census
programs support the stated fully shared conclusions; without it, only the
`T^5PP` census is exact.
