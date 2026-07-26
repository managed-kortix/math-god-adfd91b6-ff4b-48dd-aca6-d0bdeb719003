# Rank-nine fully shared incidence census: `T^8Q` and `T^7PP`

**Date:** 2026-07-26

## Status

This note records a compressed exact census experiment for the two prospective
rank-nine residual multisets

```text
T^8Q and T^7PP.
```

It is intended to measure incidence-type growth and locate exception families.
It is not a theorem claim. In particular, the executable checks abstract
colored incidence trees and an ordinary one-cycle split ledger; it does not
establish arbitrary-tree realization, induced territory, cyclic interval
ownership, or any new analytic packet inequality.

Run from the repository root:

```bash
python research/nonacyclic-fully-shared-incidence-census.py
```

The script uses only the Python standard library. Every ledger value and every
SAFE comparison uses `fractions.Fraction`; no floating-point arithmetic enters
the classification.

## Compressed generation

An object is a bipartite tree with nine colored cycle nodes and uncolored shared
cut nodes. Cuts have degree at least two, while cycle capacities are
`deg(T)<=3`, `deg(P)<=5`, and `deg(Q)<=q`. Isomorphisms may permute equal-color
cycles and all cut nodes but preserve cycle colors.

Generation is by exhaustive cycle-leaf extension. Deleting a cycle leaf and,
when necessary, suppressing the resulting degree-one cut gives a rank-eight
tree. The two inverse operations are:

1. attach the new cycle leaf to an existing cut; or
2. create a new binary cut joining the new leaf to an old cycle whose capacity
   is not saturated.

Every extension is quotiented immediately by a center-rooted colored-tree code.
This avoids labelled incidence enumeration. As internal regression tests, the
same generator reproduces the established rank-eight totals for `T^7Q` in the
`q=3` and saturated regimes and for `T^6PP`.

## Ledger boundary

For a sacrificed cycle, each component of the remaining incidence forest is a
retained packet. A split is marked SAFE when the exact sum of packet lower
bounds is positive, or is zero and at least one summand is strict.

The experimental ledger is the rank-eight continuation of the prior census:

| retained packet | bound entered in the script |
|---|---:|
| `A_r=T^r`, `1<=r<=7` | `>0,>1,>2,>3,>2,>1,>0` |
| isolated `Q=T` | `>0` |
| isolated even `Q` | `>=0` |
| isolated hostile/arbitrary odd `Q` | `>-1` |
| `TQ` | `>0` |
| `TTQ` | `>=0` |
| `T^kQ`, `3<=k<=7` | established lower-rank strict positivity |
| `P` | `>-1/4` |
| `TP` | `>3/4` |
| `PP` | `>0` |
| common-cut `TTP` | `>7/4` |
| `TPP` | `>3/2` |
| generic rank three | `>=0` |
| shared-pair `TTTP` | `>1` |
| generic mixed ranks four through seven | established lower-rank strict positivity |

No rank-eight retained-packet estimate is needed: a proper split of a nine-cycle
tree has at least two nonempty components, so each retained component has rank
at most seven. Any future use must still re-audit that every cited lower-rank
packet matches its actual incidence and realization hypotheses.

## Exact `T^8Q` counts

Only eight distinct cuts can meet `Q`, so the structural census stabilizes at
`q=8`. Counts by number `c` of cut nodes are:

| `Q` regime | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | `c=8` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `q=3` | 1 | 11 | 68 | 253 | 572 | 742 | 493 | 127 | 2267 |
| `q=4` | 1 | 11 | 68 | 258 | 586 | 774 | 525 | 142 | 2365 |
| `q=5` | 1 | 11 | 68 | 258 | 589 | 781 | 536 | 148 | 2392 |
| `q=6` | 1 | 11 | 68 | 258 | 589 | 783 | 539 | 151 | 2400 |
| `q=7` | 1 | 11 | 68 | 258 | 589 | 783 | 540 | 152 | 2402 |
| `q=8` | 1 | 11 | 68 | 258 | 589 | 783 | 540 | 153 | 2403 |
| `q>=9` | 1 | 11 | 68 | 258 | 589 | 783 | 540 | 153 | 2403 |

The SAFE and unresolved totals are:

| ledger regime | SAFE | unresolved | unresolved by `c` |
|---|---:|---:|---|
| `q=3` | 2266 | 1 | `1` at `c=1` |
| `q=4` | 2364 | 1 | `1` at `c=1` |
| `q=5` | 2390 | 2 | `1,1` at `c=1,2` |
| `q=6` | 2399 | 1 | `1` at `c=1` |
| `q=7` | 2400 | 2 | `1,1` at `c=1,2` |
| `q=8` | 2402 | 1 | `1` at `c=1` |
| `q>=9` | 2401 | 2 | `1,1` at `c=1,2` |

The universal exception is the common-cut bouquet with cut profile `(8T,Q)`.
For the hostile odd/arbitrary ledger there is one additional type:

```text
cut profiles: (8T) and (T,Q), joined through the common triangle
signature:    T(X(Q())X(T()T()T()T()T()T()T()))
```

Sacrificing the router triangle exposes the hostile isolated `Q>-1` beside the
strict but zero-margin `A_7>0`; the entered ledger is not positive. For even
`Q`, the isolated `Q>=0` row makes the same split SAFE. Thus this extra type is
a parity-ledger obstruction, not a new structural class at each odd capacity.

Growth is mild. The saturated rank-eight `T^7Q` universe has 726 types and one
ordinary-split exception. The saturated rank-nine universe has 2403 types, a
factor of about 3.31, while the exception set remains one type for the even
ledger and grows to two for the hostile ledger.

## Exact `T^7PP` counts

The complete color-preserving census is:

| | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | `c=8` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all trees | 1 | 17 | 150 | 699 | 1856 | 2714 | 1998 | 569 | 8004 |
| SAFE | 0 | 15 | 148 | 698 | 1855 | 2714 | 1998 | 569 | 7997 |
| unresolved | 1 | 2 | 2 | 1 | 1 | 0 | 0 | 0 | 7 |

The seven unresolved canonical types, compressed by cut profiles, are:

1. `c=1`: `(7T,2P)`, the common-cut bouquet.
2. `c=2`: `(7T,P)` joined through a pentagon to a binary `(2P)` cut.
3. `c=2`: a `(7T,P)` hub with a `(T,P)` tail through one hub triangle.
4. `c=3`: a `(6T,P)` hub with a `(T,P)` tail and a binary `(2T)` petal routed
   through one saturated hub triangle.
5. `c=3`: a `(7T)` hub with two `(T,P)` tails on distinct hub triangles.
6. `c=4`: a `(6T)` hub with two `(T,P)` tails and one binary `(2T)` petal,
   with one tail and the petal sharing a saturated router triangle.
7. `c=5`: a `(5T)` hub with two symmetric saturated router arms, each carrying
   one `(T,P)` tail and one binary `(2T)` petal.

The executable prints the canonical signature and a labelled edge
representative for every row. The first `c=2` row, in which a pentagon is an
internal router between the triangle-rich hub and the other pentagon, is the
clearest new shape relative to the rank-eight six-row list. The remaining rows
continue the common-cut hub and short saturated-triangle-router ladder.

The rank-eight `T^6PP` universe has 2116 types and six exceptions under the same
style of ledger. Rank nine has 8004 types, a factor of about 3.78, but only seven
exceptions. No exception occurs for `c>=6`, and no long or diffuse incidence
family appears. The experiment therefore suggests stable low-cut hub/router
families rather than rapid exception proliferation. This is evidence for where
to search, not a proof that later ranks behave similarly.

## Certification limits

The executable certifies the leaf-extension enumeration, color-preserving
canonical quotient, cut-count totals, exact rational additions, strictness
bookkeeping, and the listed abstract ordinary-split exceptions. Assertions pin
all headline counts and reproduce selected rank-eight totals before the new run.

It does not enumerate cyclic mark order, bridge connectors, connector entries,
off-core trees, or induced vertex ownership. It does not test multi-cycle
sacrifices, replacement routers, common-cut Schur--Sachs arguments, direct
spectral coupling, or root-aware quantitative bounds. An unresolved row is only
an exception to this conservative ledger and is not a graph counterexample.
No rank-nine theorem is claimed.
