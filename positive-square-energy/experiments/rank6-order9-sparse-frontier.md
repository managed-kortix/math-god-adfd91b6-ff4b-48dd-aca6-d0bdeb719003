# Order-nine rank-six sparse frontier

## Scope

This finite experiment covers exactly the 162 order-nine kernels K971--K1132
from the locked rank-six fixture. It is a census and search frontier, not a
theorem. Every kernel has fourteen physical paths and degree partition
`4,3,3,3,3,3,3,3,3`, hence near-cubic degree excess one.

The implementation stores only supported branch pairs. It generates
automorphisms inside equal-degree classes, traverses mixed-radix parity orbits,
and computes the tetrahedral minimum through a support-mask superset transform.
All acceptance arithmetic is integral in units of `1/30`; the rank-six budget
is 150.

## Exact census

| quantity | exact count |
|:--|--:|
| kernels | 162 |
| physical parity rows | 1,726,000 |
| automorphism orbits | 1,108,126 |
| tetrahedral closures | 921,831 |
| tetrahedral residual orbits | 186,295 |
| canonical plus 14 coordinate targets | 2,794,425 |

The compact canonical census has SHA-256
`6db83c893bc865c215ee29cdc9ad05e076ffab3e122e5fe6c51a0b25ef657712`.
Its ordered commitments are:

| stream | SHA-256 |
|:--|:--|
| kernels | `8a805c3272e75f365eb2b4ddff995882a39054e20e9ef213daed659705355620` |
| residuals | `2a6f0c88d8c03116096e583235bec1688a64ee5c4af0e2f61114be73b5e31807` |
| frontier keys | `8e4398963209a30141a4c2bbb1c3d4b2a722251fba2096674f20057a148698c2` |
| equality rows | `19f06d56a4c0d76cfd4243a534eee0d0c9dd01a5c39449edab85d40b8c6fcefc` |

The frontier stream commits to the residual source index, kernel, sparse row,
and target label (`null`, then coordinates 0--13), without storing 2,794,425
keys in JSON.

## Structural recognizers

The unsigned recognizer derives, rather than assumes, every support consisting
of four singleton edges forming a forest and five doubled quotient edges
forming a simple five-cycle. Exactly one kernel matches:

```text
K971: singles 07,16,25,34; doubles 08,18,27,36,45
```

The signed equality recognizer then requires one odd and one even path in every
doubled bundle. Singleton parities are unrestricted because the contraction
support is a forest. It finds ten residual parity orbits, representing 150
canonical-plus-coordinate template targets. After those structural tags,
2,794,275 targets remain for numerical or other exact certificates.

For every singleton signing, the program constructs the pulled-back rational
Gram and checks all 511 principal minors and exact cost five. This authenticates
the recognizer geometry only; it does not promote the census to a complete
kernel theorem. The artifact keeps `full_theorem=false`.

## Reproduction

```sh
python3 positive-square-energy/experiments/rank6_order9_sparse_frontier.py
python3 positive-square-energy/experiments/rank6_order9_sparse_frontier.py \
  --verify positive-square-energy/experiments/rank6_order9_sparse_frontier.json
python3 -O positive-square-energy/experiments/rank6_order9_sparse_frontier.py \
  --verify positive-square-energy/experiments/rank6_order9_sparse_frontier.json
```

The verifier rejects a changed source fixture, scope, near-cubic partition,
totals, structural match, stream commitments, noncanonical JSON, nonstandard
numeric constants, or canonical artifact digest. All checks use explicit
exceptions and remain active under `python3 -O`.
