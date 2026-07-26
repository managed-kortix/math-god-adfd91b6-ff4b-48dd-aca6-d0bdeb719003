# Rank-ten compressed incidence experiments: `T^9Q`, `T^8PP`, and marked `A_8`

**Date:** 2026-07-26

## Status and scope

This note records exact finite experiments, not a theorem claim. The executables
enumerate abstract color-preserving cycle-cut incidence trees and marked cyclic
interfaces. They do not establish graph realization, induced territory or
connector ownership, cyclic interval order, or any new packet inequality.

Run from the repository root:

```bash
python research/rank-ten-fully-shared-incidence-census.py
python research/rank-ten-a8-two-interface-census.py
```

Both scripts use the compressed cycle-leaf recurrence and center-rooted
canonical codes from the pinned rank-nine census. All ledger entries, sums,
thresholds, and displayed scores are `fractions.Fraction` values; there is no
floating-point classification. Rank-nine counts are rerun as regressions before
the rank-ten shared census.

## Ledger boundary

The ordinary-split experiment carries forward the rank-nine conservative
ledger. It additionally enters `A_8>0` and treats mixed retained packets of
ranks four through eight as strict-positive lower-rank inputs. These are inputs
to the experiment, not results proved by the script. A one-cycle split is SAFE
when its exact lower-bound sum is positive, or zero with a strict summand.

The marked `A_8` experiment places two labelled interfaces on every shared cut
and every actual private triangle vertex, allowing coincidence. Its recursive
router score is exact triangular credit minus exact naked private-interval
charges. The threshold `score>=1` is a conservative rational surrogate for
paying two pentagonal deficits. It does not model the remote pentagons,
connectors, or final graph territories.

## `T^9Q` census

Counts by shared-cut number `c` are:

| `Q` regime | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | `c=8` | `c=9` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `q=3` | 1 | 12 | 91 | 406 | 1178 | 2115 | 2250 | 1246 | 275 | 7574 |
| `q=4` | 1 | 12 | 91 | 412 | 1203 | 2187 | 2361 | 1340 | 306 | 7913 |
| `q=5` | 1 | 12 | 91 | 412 | 1208 | 2201 | 2393 | 1372 | 321 | 8011 |
| `q=6` | 1 | 12 | 91 | 412 | 1208 | 2204 | 2400 | 1383 | 327 | 8038 |
| `q=7` | 1 | 12 | 91 | 412 | 1208 | 2204 | 2402 | 1386 | 330 | 8046 |
| `q=8` | 1 | 12 | 91 | 412 | 1208 | 2204 | 2402 | 1387 | 331 | 8048 |
| `q=9` | 1 | 12 | 91 | 412 | 1208 | 2204 | 2402 | 1387 | 332 | 8049 |
| `q>=10` | 1 | 12 | 91 | 412 | 1208 | 2204 | 2402 | 1387 | 332 | 8049 |

The structure stabilizes at capacity nine. For `q=3,4,6,8`, the only exception
is the common-cut `(9T,Q)` bouquet. For hostile ledger regimes `q=5,7,9` and
uniform `q>=10`, there are exactly three exceptions:

1. the common-cut `(9T,Q)` bouquet;
2. an `(9T)` hub and `(T,Q)` tail sharing one router triangle;
3. an `(8T)` hub, `(2T)` petal, and `(T,Q)` tail sharing one saturated router
   triangle.

The second row continues the rank-nine hostile exception. The third is its next
saturated-router extension. Thus the measured hostile exception family grows
by one short arm, rather than spreading to high cut counts. This is a stable
template observation only.

The saturated universe grows from 2403 rank-nine types to 8049 rank-ten types,
the exact factor `2683/801`, approximately `3.3496`. Even-ledger exceptions stay
at one; hostile-ledger exceptions grow from two to three.

## `T^8PP` census

| | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | `c=8` | `c=9` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all trees | 1 | 19 | 204 | 1155 | 3990 | 8135 | 9615 | 5843 | 1424 | 30386 |
| SAFE | 0 | 17 | 200 | 1154 | 3989 | 8135 | 9615 | 5843 | 1424 | 30377 |
| exceptions | 1 | 2 | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 9 |

The nine exceptions are compactly described as follows:

1. `c=1`: common-cut `(8T,2P)` bouquet.
2. `c=2`: `(8T,P)` hub joined through a pentagon to a binary `(2P)` cut.
3. `c=2`: `(8T,P)` hub with a `(T,P)` tail through one hub triangle.
4. `c=3`: `(7T,P)` hub with `(T,P)` tail and `(2P)` pentagon tail through one
   saturated hub pentagon.
5. `c=3`: `(8T)` hub with two `(T,P)` tails on one common router triangle.
6. `c=3`: `(7T,P)` hub with `(T,P)` tail and binary `(2T)` petal through one
   saturated router triangle.
7. `c=3`: `(8T)` hub with two `(T,P)` tails on distinct hub triangles.
8. `c=4`: `(7T)` hub with two `(T,P)` tails and a binary `(2T)` petal, with one
   tail and the petal sharing a saturated router triangle.
9. `c=5`: `(6T)` hub with two symmetric saturated router arms, each carrying a
   `(T,P)` tail and a binary `(2T)` petal.

Rows 1, 3, and 6--9 are direct one-rank enlargements of previously observed
hub/router forms. Rows 2 and 4 form the short internal-pentagon branch. Row 5 is
the new same-router version of the familiar two-tail bouquet. All exceptions
remain at `c<=5`; none occurs among the 25017 types with `c>=6`.

The universe grows from 8004 rank-nine types to 30386 rank-ten types, the exact
factor `15193/4002`, approximately `3.7964`. The ordinary-split exception count
grows from seven to nine. The evidence favors a finite-width common-cut
hub/saturated-router grammar, but does not prove stabilization at later ranks.

## Marked `A_8` two-interface census

There are 126 unmarked eight-triangle incidence trees. Across them, the script
examines 36414 labelled placements before automorphism quotient and obtains
11689 canonical marked classes. Exact router scores are:

| score | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| classes | 15 | 20 | 283 | 1378 | 4817 | 5176 |

Hence 11674 rows meet the conservative `score>=1` threshold and 15 do not.
Best plans use zero, one, two, and three routers in 6, 10844, 838, and 1 rows,
respectively. The rank-nine marked universe had 3188 rows, so marked growth is
the exact factor `11689/3188`, approximately `3.6666`.

The 15 residuals lie on only two unmarked incidence templates:

- six mark orbits on the common-cut `A_8` bouquet, extending the six rank-nine
  bouquet residuals;
- nine mark orbits on the two-cut shape consisting of a seven-triangle hub and
  a binary triangle petal through a shared router triangle.

The second template is precisely the one-step saturated-router extension that
also appears in the hostile `T^9Q` and `T^8PP` exception lists. This cross-census
recurrence is the strongest measured candidate for a stable marked-interface
template. No repair or graph-level ownership certificate is asserted here.

## Certification limits

The scripts certify their abstract leaf-extension enumeration, canonical
quotient, exact rational ledgers, score distributions, exception lists, and
SHA-256 digests for the marked rows. They do not enumerate cyclic orders,
connector lengths, off-core trees, arbitrary-tree attachment ownership,
replacement packetizations, or spectral inequalities. An exception means only
that the stated conservative finite ledger did not accept that abstract row.
No rank-ten theorem is claimed.
