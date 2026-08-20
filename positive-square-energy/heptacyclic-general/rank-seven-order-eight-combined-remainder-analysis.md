# Rank-seven order-eight combined remainder analysis

## Scope

The precedence-aware combined ledger leaves exactly 84,152 order-eight coarse
rows after payload-free, committed direct-rational, scalar SOS, and typed-
diagonal lanes. These rows represent 92,670 physical rows and 1,262,280 finite
canonical-plus-coordinate targets. This report authenticates that exact stream,
stratifies it, and applies induced-packet and direct-spectral detection to all
15 targets of every row.

The resulting packet/spectral lanes are exact finite owners. A subsequent
boundary-closure scan replaces all 296 of them by shared exact rational DNN
Grams, promoting every row to full same-parity all-length plus arbitrary
rooted-tree ownership.

## Exact stratification

The input remainder has 3,072 kernels. Its requested invariant concentrations
are:

| Invariant | Classes | Largest class | Top 10 | Top 100 |
| --- | ---: | ---: | ---: | ---: |
| support | 178 | 5,139 | 27,198 | 78,923 |
| parity | 13,025 | 311 | 2,086 | 10,820 |
| signed degree | 3,071 | 1,504 | 8,517 | 34,169 |
| joint structural signature | 21,143 | 178 | 1,110 | 6,108 |

The dominant finite-family key records the multiplicity partition, bundle
types `(zero,mixed,full)`, support cycle rank, and triangle count. Its first ten
families contain 31,010 rows. The leading families are:

| Rows | Physical | Multiplicities | Bundle types | Cycle rank | Triangles |
| ---: | ---: | --- | --- | ---: | ---: |
| 6,929 | 7,620 | `2^3 1^8` | `(2,3,6)` | 4 | 2 |
| 4,316 | 4,764 | `2^3 1^8` | `(3,3,5)` | 4 | 2 |
| 3,801 | 3,952 | `2^3 1^8` | `(2,3,6)` | 4 | 1 |
| 2,928 | 3,060 | `2^4 1^6` | `(2,4,4)` | 3 | 1 |
| 2,731 | 2,968 | `2^3 1^8` | `(1,3,7)` | 4 | 2 |
| 2,571 | 2,694 | `2^4 1^6` | `(1,3,6)` | 3 | 1 |
| 2,167 | 2,275 | `2^2 1^10` | `(2,2,8)` | 5 | 3 |
| 2,027 | 2,192 | `2^2 1^10` | `(3,2,7)` | 5 | 3 |
| 1,788 | 1,958 | `2^3 1^8` | `(2,3,6)` | 4 | 3 |
| 1,752 | 1,798 | `3 2^2 1^7` | `(2,3,5)` | 3 | 1 |

Thus the dominant search territory consists of three doubled bundles on an
11-edge, cycle-rank-four support, followed by four doubled bundles on a
10-edge, cycle-rank-three support. These family labels describe the finite
remainder; they are not theorem owners by themselves.

## Induced-packet lane

For every canonical target and each of its 14 physical-path frontiers, the
scanner constructs the exact simple graph. It searches induced `K5`, `K4`, and
diamond anchors supported by unit odd edges. Every component outside an anchor
must be an induced tree or odd-unicyclic graph, and the number of such debit
components must not exceed the anchor allowance `1`, `2`, or `1`, respectively.

This exact combinatorial test owns 45 rows, 50 physical rows, and 675 finite
targets. Across those 675 target certificates, the selected anchors are 72
`K4` packets and 603 diamond packets. Packet ownership takes precedence over
the spectral lane.

## Direct-spectral Rayleigh lane

For each target graph with adjacency matrix `A` and order `n`, the new lane
stores an integer vector `x` and verifies

```text
x^T A x > 0,
(x^T A x)^2 > n (x^T x)^2.
```

The Rayleigh principle gives `lambda_max(A) > sqrt(n)`, so the square of this
one positive eigenvalue already exceeds `n`. Hence `s^+(G)>n` exactly. Floating
point is used only to propose `x`; the persisted numerator, denominator, and
strict integer difference are independently checkable exact certificates.

After packet precedence, this lane owns 251 rows, 256 physical rows, and 3,765
finite targets. Every accepted row has a separate integer certificate for its
canonical target and all 14 coordinate frontiers. This is a new exact owner
lane for the order-eight combined remainder.

## Descendant-lift audit

### Rayleigh zero extension is bounded

Let a certified target have order `n` and Rayleigh quotient

```text
R = (x^T A x)/(x^T x) > sqrt(n).
```

If a descendant contains that target as an induced subgraph, extending `x` by
zero leaves the quotient equal to `R`. It certifies only descendants of order

```text
N < R^2.
```

For the stored integer certificate this gives the exact additional-vertex
capacity

```text
floor(((x^T A x)^2-1)/(x^T x)^2) - n.
```

This is useful finite induced-supergraph evidence, but never a uniform
all-length or rooted-tree lift: the capacity is finite for every stored vector.
Moreover, subdividing an edge does not retain the unsubdivided graph as an
induced subgraph. A subdivision-specific spectral monotonicity statement would
therefore be an additional theorem, not a consequence of zero extension.

That caution is necessary. Subdividing an edge twice need not preserve the
strict test `lambda_max^2>|V|`: `K3` has `lambda_max^2=4>3`, while replacing one
edge by a path of length three gives `C5`, with
`lambda_max^2=4<5`. Hence none of the 251 direct-spectral owners has a valid
general descendant lift from its persisted evidence. Arbitrary rooted-tree
attachments are also unbounded in order and are not covered by a fixed
Rayleigh quotient.

### Packet owners have conditional structural lifts

The 45 induced-packet rows already use structural induced-piece evidence. Fix
one target certificate and leave every unit edge of its selected `K4` or
diamond anchor unchanged. Same-parity subdivision of edges outside the anchor
preserves the anchor as an induced subgraph. The outside components remain
trees or odd-unicyclic graphs: subdividing an edge preserves cycle rank, and
adding two vertices preserves cycle parity. Attaching rooted trees preserves
the same component classification. Thus the existing packet debit proof is
uniform over those descendants, including arbitrary rooted trees.

This is only a conditional lift. A general same-parity descendant may lengthen
an edge of every available unit-edge anchor, destroying each selected induced
`K4` or diamond. The fifteen finite checks do not prove that some alternate
anchor survives simultaneous lengthening. Consequently all 45 packet rows are
classified `conditional-structural-lift`, not full descendant owners.

### Exact eligibility result

The exhaustive classification is

```text
45  conditional structural lifts (anchor-preserving descendants only),
251 finite direct-spectral owners (bounded zero-extension scope only),
0   full same-parity all-length plus arbitrary rooted-tree lifts.
```

Therefore the packet/spectral lanes remove 296 rows from the finite-target
remainder but remove zero rows from the theorem-eligible remainder. Relative to
their 84,152-row input, the exact theorem-eligible remainder is still 84,152
coarse rows and 1,262,280 frontier targets. Relative to the full combined
ledger, its theorem-eligible status is unchanged by these two lanes.

### Shared rational DNN replacement

The finite-only classification is not the final owner assignment. The boundary
closure reruns the exact rational Gram engine on precisely these 296 stream
indices. Every row admits one shared rational branch Gram whose exact path-chain
cost is at most six for the canonical target and for each of the fourteen
one-coordinate length-plus-two targets. All 296 use the shared-witness mode;
none needs a target-specific fallback.

These are theorem owners under the canonical-plus-coordinate reduction. For a
proper same-parity descendant, select a canonical or coordinate target that it
dominates, retain that target's branch Gram, and lengthen every required path.
Fixed-parity path monotonicity weakly decreases each eliminated path cost.
One-vertex DNN additivity then supplies arbitrary rooted-tree attachments.
Thus this replacement closes both gaps left by the packet and spectral
evidence without asserting subdivision monotonicity for either finite lane.

The exact theorem-eligible update is therefore

```text
84152 = 296 shared-rational DNN frontier owners + 83856,
1262280 = 4440 theorem-owned frontier targets + 1257840.
```

In the full precedence-aware ledger, the theorem-owned total becomes 409,561
rows and the exact theorem-eligible remainder becomes 83,856 rows. The order-
eight theorem is not yet complete; this closes only the 296-row boundary gap.

## Updated remainder

The disjoint finite accounting is

```text
84152 = 45 + 251 + 83856,
1262280 = 675 + 3765 + 1257840.
```

The updated remainder therefore contains 83,856 coarse rows, 92,364 physical
rows, and 1,257,840 finite targets. The dominant top-ten family counts are
unchanged: the 296 newly owned rows lie in smaller finite strata. The updated
remainder still has 3,006 kernels, 178 support classes, 12,994 parity classes,
3,062 signed-degree classes, and 21,078 joint classes.

## Artifacts and reproduction

- `experiments/rank7_order8_combined_remainder_analysis.json` is the canonical exact report with input and output strata.
- `experiments/rank7_order8_packet_spectral_owners.json.xz` stores all 296 owner rows and all 4,440 target certificates.
- `experiments/rank7_order8_after_packet_spectral_remainder.jsonl.xz` stores the exact updated 83,856-row remainder.
- `experiments/rank7_order8_combined_remainder_analysis.py` authenticates the combined ledger and indices, reconstructs every target, and reproduces all artifacts.
- `experiments/rank7_order8_theorem_dnn_owners.json.xz` stores the 296 shared rational DNN witnesses.
- `experiments/rank7_order8_theorem_eligible_combined_ledger.json` is the theorem-eligible combined ledger with exact remainder 83,856.
- `experiments/rank7_order8_theorem_boundary_closure.py` regenerates and independently audits the replacement owners and ledger.

```text
python3 positive-square-energy/experiments/rank7_order8_combined_remainder_analysis.py
python3 positive-square-energy/experiments/rank7_order8_combined_remainder_analysis.py --audit
python3 positive-square-energy/experiments/rank7_order8_theorem_boundary_closure.py --audit
```

The v2 packet/spectral report remains a finite-target result. The separate DNN
replacement ledger is theorem-eligible but does not mark the full order-eight
theorem complete.

## Leading-family structural cycle-Gram lane

The next theorem-eligible lane authenticates and stratifies the complete
83,856-row remainder. It records all 318 exact dominant-family classes. The
leading class has 6,929 orbits and 7,620 physical rows, with multiplicity
partition `2^3 1^8`, bundle types `(2,3,6)`, support cycle rank four, and two
triangles.

Every row in that leading class is scanned with the structural Gram

```text
H = XX^T + w A P_cycle A^T,
X = D0 + D1 S,
G = H/M + diag(1-diag(H)/M).
```

Here `S` is the signed bundle matrix, `D0,D1` are constant on the exact local
type `(signed degree, sorted incident (multiplicity,odd-count) pairs)`, `A` is
the parity-signed physical-path incidence matrix, and
`P_cycle=I-B^T(BB^T)^-1B`. Both terms of `H` are explicit Gram squares for
`w>=0`; the diagonal completion is another nonnegative coordinate-square sum.
Numerical optimization only proposes parameters. Every parameter is rounded to
a rational of denominator at most 256, and every accepted cost is recomputed
exactly.

The full 6,929-row family scan owns 112 orbits, 128 physical rows, and 1,680
canonical-plus-coordinate targets. For each accepted Gram, every path summand

```text
(1-t)/(L(1+t)),  t=(-1)^L G_uv,
```

is nonnegative and weakly decreases under `L -> L+2`. The certificate therefore
owns all same-parity path lengths directly, rather than only the fifteen finite
frontiers. DNN one-vertex additivity supplies arbitrary rooted-tree
attachments. These 112 records are consequently exact induced owners with the
required all-length and rooted-tree lift.

The reduced theorem-eligible remainder has 83,744 rows. The 6,817 unsuccessful
rows in the target family and every non-target family remain unclassified;
optimizer failure is not treated as an obstruction.

- `experiments/rank7_order8_structural_cycle_gram_lane.py` implements the authenticated full-family scan and exact replay.
- `experiments/rank7_order8_structural_cycle_gram_lane.json` stores all 318 family strata and the exact coverage ledger.
- `experiments/rank7_order8_structural_cycle_gram_owners.jsonl.xz` stores the 112 rational owner certificates.
- `experiments/rank7_order8_after_structural_cycle_gram_remainder.jsonl.xz` stores the exact 83,744-row complement.

```text
python3 positive-square-energy/experiments/rank7_order8_structural_cycle_gram_lane.py --workers 8
python3 positive-square-energy/experiments/rank7_order8_structural_cycle_gram_lane.py --workers 8 --audit
```
