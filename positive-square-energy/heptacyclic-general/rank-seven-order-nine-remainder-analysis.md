# Rank-seven order-nine structural remainder analysis

## Scope

The committed payload-free structural scan leaves exactly 385,829 residual
orbits, 442,225 physical rows, and 6,173,264 canonical-plus-frontier targets.
This report authenticates that exact remainder stream and stratifies every row.
It tests one scalar SOS Gram lane and one typed-diagonal SOS lane on the entire
remainder. Nothing here claims ownership outside exactly replayed finite-grid
coverage.

## Exact stratification

The census records 3,799 kernels represented in the remainder. Exact invariant
class counts are:

| Invariant | Classes | Largest class | Top 10 | Top 100 |
| --- | ---: | ---: | ---: | ---: |
| support multiplicities and degrees | 91 | 39,351 | 211,527 | 385,829 |
| parity profile | 25,138 | 1,998 | 12,062 | 56,847 |
| signed-degree profile | 5,119 | 6,633 | 41,915 | 158,302 |
| graph invariants | 1,948 | 15,541 | 92,651 | 282,290 |
| combined structural signature | 48,790 | 863 | 5,611 | 30,541 |

The support axis is highly concentrated while exact parity and combined types
remain broad. The dominant-family key consists of multiplicity partition,
zero/mixed/full bundle counts, cycle rank, and triangle count. Its first ten
families contain 166,587 rows. The largest families are:

| Rows | Multiplicities | Bundle types `(zero,mixed,full)` | Cycle rank | Triangles |
| ---: | --- | --- | ---: | ---: |
| 31,518 | `2^3 1^9` | `(3,3,6)` | 4 | 1 |
| 21,547 | `2^3 1^9` | `(4,3,5)` | 4 | 1 |
| 21,278 | `2^3 1^9` | `(3,3,6)` | 4 | 2 |
| 19,729 | `2^3 1^9` | `(4,3,5)` | 4 | 2 |
| 14,246 | `2^4 1^7` | `(2,3,6)` | 3 | 1 |
| 14,118 | `2^3 1^9` | `(2,3,7)` | 4 | 1 |
| 13,285 | `2^3 1^9` | `(3,3,6)` | 4 | 0 |
| 12,651 | `2^4 1^7` | `(2,3,6)` | 3 | 0 |

Thus a small practical family list is: three doubled bundles on a 12-edge,
cycle-rank-four support (the first, second, third, fourth, sixth, seventh, and
ninth families), and four doubled bundles on an 11-edge, cycle-rank-three
support (the fifth, eighth, and tenth families). These are search families, not
theorem owners.

## Scalar SOS owner lane

For signed bundle matrix `S_uv=m_uv-2r_uv`, the full scan tests rational
`0 <= t <= 4` with denominator at most 16 and forms

```text
X = I + tS,
M = max_i (XX^T)_ii,
G = XX^T/M + diag(1 - diag(XX^T)/M).
```

This is an exact rational correlation Gram: `XX^T/M` is a Gram square and the
diagonal completion is nonnegative. Binary64 only selects a deterministic grid
proposal. The selected proposal and every cost classification are replayed with
`Fraction`. The full authenticated scan verifies 7,796 owners and 124,736
targets. It leaves 378,033 rows unowned by this lane. Because path lengthening
by two preserves parity and decreases the affected positive summand, exact
canonical ownership covers all 16 targets for each accepted row.

This is a theorem-owner lane only for those 7,796 rows. The report's
classification digest and coefficient histogram bind the exact covered set; it
does not promote the scalar obstruction set to a mathematical obstruction.

## Typed SOS full lane

The full typed lane uses `X=D0+D1*S`, where both diagonals are constant on exact
local types `(signed degree, sorted incident (multiplicity,odd-count) pairs)`.
It initializes from the scalar proposal and performs three coordinate passes
over ratios from 0 through 2 with denominator at most 4 and five exact scales
`1/2, 2/3, 1, 3/2, 2`. Binary64 proposes a tuple, but every accepted tuple,
Gram correlation, and cost is replayed with `Fraction`.

With scalar ownership taking precedence, the exact exclusive accounting is:

| Stratum | Orbits | Physical rows | Canonical-plus-frontier targets |
| --- | ---: | ---: | ---: |
| scalar SOS | 7,796 | 10,958 | 124,736 |
| typed SOS, additional | 105,513 | 123,941 | 1,688,208 |
| finite-grid failures | 272,520 | 307,326 | 4,360,320 |
| total | 385,829 | 442,225 | 6,173,264 |

Thus the lane owns 113,309 remainder orbits, 134,899 physical rows, and
1,812,944 canonical-plus-frontier targets. The exact orbit partition is
`385829 = 7796 + 105513 + 272520`.

## Final failure strata

The 272,520 finite-grid failures occupy 3,339 kernels, 91 support classes,
18,859 parity classes, 4,249 signed-degree classes, 1,409 graph classes, 354
dominant families, and 34,097 full joint classes. The largest joint class has
only 601 orbits, while the ten largest dominant families contain 122,708.
The leading dominant families are:

| Orbits | Physical rows | Multiplicities | Bundle types | Cycle rank | Triangles |
| ---: | ---: | --- | --- | ---: | ---: |
| 21,074 | 22,100 | `2^3 1^9` | `(3,3,6)` | 4 | 1 |
| 17,592 | 18,479 | `2^3 1^9` | `(4,3,5)` | 4 | 1 |
| 17,507 | 20,496 | `2^3 1^9` | `(3,3,6)` | 4 | 2 |
| 16,183 | 19,053 | `2^3 1^9` | `(4,3,5)` | 4 | 2 |
| 10,823 | 11,308 | `2^3 1^9` | `(2,3,7)` | 4 | 1 |
| 10,587 | 11,236 | `2^4 1^7` | `(2,3,6)` | 3 | 1 |
| 8,932 | 10,339 | `2^3 1^9` | `(2,3,7)` | 4 | 2 |
| 7,333 | 8,996 | `2^3 1^9` | `(3,3,6)` | 4 | 0 |
| 6,365 | 6,720 | `2^4 1^7` | `(3,4,4)` | 3 | 1 |
| 6,312 | 7,070 | `2^4 1^7` | `(3,4,4)` | 3 | 0 |

These are failures of this deterministic finite grid, not nonexistence
certificates for the Gram ansatz or mathematical obstructions.

## Artifacts and claim boundary

- `experiments/rank7_order9_unowned_structural_stratification.json` is the exact full-remainder stratification.
- `experiments/rank7_order9_unowned_search_indices.json` binds source indices for every recorded signature and candidate family.
- `experiments/rank7_order9_remainder_gram_lanes.json` is the exact scalar full scan and typed pilot report.
- `experiments/rank7_order9_typed_sos_owner_manifest.json` authenticates the full scalar/typed ownership partition.
- `experiments/rank7_order9_typed_sos_owners.jsonl.xz` stores all exclusive owner records and exact certificates.
- `experiments/rank7_order9_after_sos_remainder.jsonl.xz` stores the final finite-grid failures.
- `experiments/rank7_order9_after_sos_stratification.json` gives the exact final failure strata.
- `experiments/rank7_order9_unowned_stratifier.py` and `experiments/rank7_order9_remainder_gram_lanes.py` reproduce and authenticate the reports.
- `experiments/rank7_order9_typed_sos_owner_lane.py` and `experiments/rank7_order9_after_sos_stratifier.py` reproduce and audit the full lane and final strata.

The scalar and typed lanes are merged only under explicit scalar-first
precedence. The 272,520-row updated remainder is unclassified, so no full
rank-seven/order-nine theorem is claimed.
