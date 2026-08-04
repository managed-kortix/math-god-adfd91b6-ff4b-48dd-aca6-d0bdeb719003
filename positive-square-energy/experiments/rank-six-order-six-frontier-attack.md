# Experimental rank-six order-six frontier attack

This record is experimental only. It is not a theorem claim and does not alter
the proved low-order rank-six package.

## Exact coarse census

The source is the digest-locked rank-six kernel fixture, restricted to its 216
order-six kernels K116--K331. Pair order is

`01,02,03,04,05,12,13,14,15,23,24,25,34,35,45`.

Each kernel has 11 suppressed paths. Exhausting every physical parity row and
quotienting by the exact kernel automorphism group gives:

| item | exact count |
|:---|---:|
| kernels | 216 |
| labeled physical rows | 207,358 |
| automorphism orbits | 150,734 |
| regular-tetrahedron coarse certificates at budget 5 | 148,130 |
| coarse residual orbits | 2,604 |
| canonical plus 11 coordinate frontiers | 31,248 |

The 2,604 residual orbits have total labeled orbit size 3,263 and meet all 216
kernels. The exact census is stored in
`rank6_order6_coarse_census.json`.

## Dimension-six rational search

For every residual orbit, the search attacked the canonical shortest length
vector and all 11 vectors formed by adding two to one path length. Numerical
optimization only proposed six-dimensional unit vectors. Every accepted result
was reconstructed from rational stereographic parameters, and every transformed
edge cost `(1-r)/(1+r)` was summed over `Fraction` and checked at budget 5.

The run was chunked as follows:

| residual indices | targets | exact rational | unresolved |
|:---|---:|---:|---:|
| 0--24 | 300 | 300 | 0 |
| 25--124 | 1,200 | 1,200 | 0 |
| 125--2603 | 29,748 | 29,735 | 13 |
| total | 31,248 | 31,235 | 13 |

Thus the rational search closes 99.9584% of the finite frontier. This is an
exact statement about accepted certificates, not evidence that unresolved
targets lack DNN certificates.

## Finite residual

The 13 unresolved targets collapse to four kernels. Rows below use the pair
order above; `c` denotes the canonical vector and an integer denotes the
zero-based physical path coordinate lengthened by two.

| kernel | row | unresolved frontiers | numerical fingerprint |
|:---:|:---|:---|:---|
| K223 | `001111011011111` | `c` | `5.34670847911` |
| K253 | `001001011011011` | `c,2` | `5.00000000479,5.0` |
| K253 | `001101011011011` | `c,2` | `5.0,5.0` |
| K300 | `000010010111111` | `c,0` | `5.00000124245,5.00000000651` |
| K300 | `100010010111111` | `c,0` | `5.0,5.0` |
| K302 | `000010010101100` | `c,0` | `5.0,5.0` |
| K302 | `100010010101100` | `c,0` | `5.0,5.0` |

The twelve K253/K300/K302 targets are the finite symbolic-equality residual:
all remain numerically pinned to 5 under 20 restarts, 1,500 descent iterations,
and rational denominators through 262,144. Their unresolved coordinate is a
member of a doubled bundle, and lengthening it leaves the numerical optimum at
equality. The next exact task is to recover and verify their endpoint Gram
matrices symbolically.

K223 is structurally different. Its canonical target is the all-unit simple
graph with edges

`03,04,05,12,14,15,24,25,34,35,45`.

The vertices `{0,3,4,5}` induce an actual K4, while `{1,2}` and their four
incidences to `{4,5}` form the complementary finite owner territory. The
canonical DNN optimum is numerically above budget, whereas all 11 coordinate
frontiers have strict rational certificates. This isolates one finite
structural-opening candidate rather than a symbolic equality candidate. A
proof still needs an induced owner-exact partition and packet inequalities;
the graph shape alone is not counted as a closure.

## Reproduction

```text
python3 positive-square-energy/experiments/rank6_order6_coarse_census.py --jobs 16
python3 positive-square-energy/experiments/rank6_order6_dim6_rational_frontier.py --start 0 --limit 25
python3 positive-square-energy/experiments/rank6_order6_dim6_rational_frontier.py --start 25 --limit 100
python3 positive-square-energy/experiments/rank6_order6_dim6_rational_frontier.py --start 125 --limit 2479
```

The checked-in search chunks retain `full_theorem=false`. Fixed-parity path
monotonicity may only be invoked after the 13 finite residual targets receive
symbolic or structural certificates.
