# Experimental rank-six kernel census

This is an exact computational census record, not a theorem claim. It covers
loopless multigraphs with at least two vertices, minimum degree at least three,
no cut vertex, and cyclomatic rank `|E|-|V|+1=6`.

The degree-excess identity is

`sum_v (deg(v)-2)=10`,

so the only possible orders are `2,...,10`. The exact isomorphism counts are:

| order | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | total |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| classes | 1 | 4 | 26 | 84 | 216 | 314 | 325 | 162 | 66 | 1198 |

## Degree-multiset ledger

| degree multiset | classes |
|:---|---:|
| `7,7` | 1 |
| `7,6,3` | 1 |
| `7,5,4` | 1 |
| `6,6,4` | 1 |
| `6,5,5` | 1 |
| `7,5,3,3` | 2 |
| `7,4,4,3` | 2 |
| `6,6,3,3` | 4 |
| `6,5,4,3` | 7 |
| `6,4,4,4` | 2 |
| `5,5,5,3` | 2 |
| `5,5,4,4` | 7 |
| `7,4,3,3,3` | 4 |
| `6,5,3,3,3` | 11 |
| `6,4,4,3,3` | 18 |
| `5,5,4,3,3` | 26 |
| `5,4,4,4,3` | 20 |
| `4,4,4,4,4` | 5 |
| `7,3,3,3,3,3` | 2 |
| `6,4,3,3,3,3` | 29 |
| `5,5,3,3,3,3` | 34 |
| `5,4,4,3,3,3` | 101 |
| `4,4,4,4,3,3` | 50 |
| `6,3,3,3,3,3,3` | 15 |
| `5,4,3,3,3,3,3` | 134 |
| `4,4,4,3,3,3,3` | 165 |
| `5,3,3,3,3,3,3,3` | 55 |
| `4,4,3,3,3,3,3,3` | 270 |
| `4,3,3,3,3,3,3,3,3` | 162 |
| `3,3,3,3,3,3,3,3,3,3` | 66 |

The frozen canonical fixture is
`research/fixtures/rank-six-kernels.json`. Its canonical JSON bytes have
SHA-256 digest

`5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476`.

`research/rank-six-kernel-census-verifier.py` regenerates the incidence
solutions without reading fixture rows, checks the graph predicates and exact
canonical list, and rejects nine hostile fixture or policy mutations using
explicit exceptions. Run it in both modes:

```text
python3 research/rank-six-kernel-census-verifier.py
python3 -O research/rank-six-kernel-census-verifier.py
```

As a separate generation route used while freezing the fixture, nauty 2.8.9
generated every unlabeled biconnected simple support on each order, and
`multig -e(n+5)` generated its multiplicity orbits. Filtering minimum degree
three gave the same order counts and canonical rows. This external route is
not required by the checked-in verifier.
