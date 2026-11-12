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

## Leading-family structural Gram lane

The next exact lane scans all 272,520 after-SOS rows and targets the leading
family `2^3 1^9`, bundle types `(3,3,6)`, cycle rank four, and one triangle.
For the signed bundle matrix `S`, vertices are typed by

```text
(signed degree, sorted incident (multiplicity, odd-count) pairs).
```

It uses `X=D0+D1*S`, with both diagonals constant on these exact local types,
and the correlation Gram

```text
G = XX^T/M + diag(1-diag(XX^T)/M),  M=max_i (XX^T)_ii.
```

Thus every certificate is structurally PSD: the first term is a Gram square
and the completion is a nonnegative sum of coordinate squares. A deterministic
binary64 Powell proposal is rounded entrywise to rationals of denominator at
most 256, after which the complete cost is recomputed with `Fraction`.

The authenticated full scan finds 21,074 family rows and exactly owns 1,128
of them (1,173 physical rows and 18,048 canonical-plus-frontier targets). It
leaves 19,946 rows in the target family and 271,392 rows overall. These are
optimizer/grid failures, not obstructions to this Gram family. The report
replays byte-for-byte with SHA-256
`7346c593bd98880ca9599f44ae26c69d20225342d361804740742caccdc75169`.

- `experiments/rank7_order9_dominant_family_gram_lane.py` implements and audits the lane.
- `experiments/rank7_order9_dominant_family_gram_lane.json` persists the full-remainder coverage ledger.
- `experiments/rank7_order9_dominant_family_gram_owners.jsonl.xz` stores all 1,128 exact rational owners.

## Historical cycle-space witness streams

Two later commits persisted witness streams for the third and fourth largest
after-SOS families, but the shared producer module and named predecessor
artifacts are absent from the current tree and fetched reachable history.  The
full optimization runs and rejected classifications therefore cannot be
reproduced from the committed artifacts.  The surviving accepted witnesses
can, however, be authenticated and checked without trusting that optimizer.

`experiments/rank7_order9_cycle_gram_engine.py` is a fail-closed verifier for
that surviving certificate language.  It authenticates the complete 272,520-row
after-SOS source stream, requires every stored owner row to equal its uniquely
indexed source row field-for-field, pins both historical report identities,
and checks the reports' source, family, owner, denominator, and immediate-chain
accounting.  On the 15 physical paths it forms the rational cycle projector

```text
P_cycle = I - B^T(BB^T)^(-1)B
```

and, for signed endpoint incidence `A`, verifies

```text
H = XX^T + w A P_cycle A^T,
G = H/M + diag(1-diag(H)/M),
X = D0 + D1 S.
```

Every stored rational pair is required to be reduced with positive
denominator; every Gram parameter and cycle weight is additionally required to
have denominator at most 256.  Every parameter and every entry of `P_cycle`,
`H`, and the path-chain cost is then recomputed with `Fraction`; no
floating-point value participates in mathematical ownership acceptance.  The
stored numerical diagnostic is required only to be finite.  The PSD proof is
explicit:
`XX^T` and `w(A P_cycle)(A P_cycle)^T` are Gram squares for `w>=0`, and the
diagonal completion is a sum of nonnegative coordinate squares.  The verifier
also binds source kernel, parity row, family, local-type ordering, unique source
index, physical multiplicity, canonical witness bytes, compressed and raw
SHA-256 identities, exact family totals from the source, and report owner and
denominator totals.

The authenticated owner totals are:

| Family | Exact owners | Physical rows | Canonical-plus-frontier targets |
| --- | ---: | ---: | ---: |
| `2^3 1^9`, `(3,3,6)`, rank 4, 2 triangles | 631 | 748 | 10,096 |
| `2^3 1^9`, `(4,3,5)`, rank 4, 2 triangles | 1,036 | 1,283 | 16,576 |

The raw owner-stream SHA-256 identities are respectively
`2f35c2a76ce054be0d5b2ed18c0bfd77f163c1429af35ca48b91313ba77d0154`
and
`a347d2d7891609156692d0bf0614783d79a9b84c6f4e0902ef6672f1cb4c96f5`.
The two streams are disjoint.  The fourth report's immediate predecessor link
is authenticated against the pinned third-report identity.  The third report,
however, only *asserts* an earlier 1,018-owner lane and a 270,374-row remainder:
its referenced report, owner stream, and producer are absent.  Consequently the
later figure 268,707 is preserved only as unauthenticated historical metadata,
not established as a remainder by this verifier.  This audit establishes only
the 1,667 witnesses persisted in these two cycle-space streams.  It does not
reproduce their optimizer failure sets, authenticate the missing predecessor,
prove a full family, or prove the order-nine theorem.

Reproduce the exact replay with:

```bash
uv run --with networkx \
  python3 positive-square-energy/experiments/rank7_order9_cycle_gram_engine.py \
  --audit-historical
```

The regression suite additionally mutates source identity and multiplicity,
exact cost, rational canonicality, and report identity, and requires fail-closed
rejection in every case:

```bash
uv run --with networkx --with pytest \
  pytest -q positive-square-energy/experiments/test_rank7_order9_cycle_gram_engine.py
```
