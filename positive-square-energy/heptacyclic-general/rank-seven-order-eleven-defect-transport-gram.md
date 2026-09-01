# Rank-seven order-eleven defect-transport Gram lane

## Exact remainder

The authenticated order-eleven census has 11,424,569 coarse residual orbits.
The existing payload-free lanes own 29,944: 20,447 balanced rank-one rows,
4,572 signed-imbalance rows, and 4,925 simplex/mixed-atom rows. The cubic
cycle-space lane owns zero. The exact remainder is therefore 11,394,625 orbits,
16,263,341 physical rows, and 205,103,250 canonical-plus-frontier targets.

Every kernel has degree sequence `(4,3^10)`. Equivalently, relative to cubic
degree, `sum_v(deg(v)-3)=1`; in the handshake identity the total degree defect
is two. This explains the zero cubic-lane count: its recognizer requires a
cubic kernel and rejects every order-eleven kernel before searching. The
signed-imbalance lane is local and discards cycle transport, while the
six-state three-ray geometry quantizes correlations and has no continuous
parameter for transporting the unique degree-four hub defect. The atom lane
only sees sparse equality profiles.

## Defect-transport typed SOS

For signed bundle matrix `S`, type vertex `v` by

```text
(deg(v)-3, signed_degree(v), sorted incident (multiplicity,odd-count) pairs).
```

Let `X=D0+D1*S`, with both diagonals constant on these exact types. Expand the
kernel to its seventeen physical paths. If `B` is reduced oriented incidence,
`P_cycle=I-B^T(BB^T)^-1B`, and `A` is signed endpoint incidence, use

```text
H = X X^T + w A P_cycle A^T,
G = H/M + diag(1-diag(H)/M),  M=max_i H_ii.
```

The second summand transports signed endpoint mass through the physical
seven-dimensional cycle space, including away from the unique degree-four
hub. Both summands are exact rational Gram squares and the diagonal completion
is nonnegative. Thus PSD is symbolic, not a floating-point eigenvalue claim.
Binary64 Powell search only proposes coefficients; all accepted coefficients,
Gram entries, and costs are rounded to denominator at most 128 and replayed
with `Fraction`.

For path `p=(u,v,L)`, put `t_p=(-1)^L G_uv`. The exact acceptance test is

```text
sum_p (1-t_p)/(L_p(1+t_p)) <= 6.
```

Fixed-parity lengthening decreases every summand, so each accepted row owns
its canonical target and all seventeen single-path `+2` frontiers.

## Exact scans

The full coarse stream was stratified exactly. The twelve dominant families
contain between 189,007 and 319,522 rows each. Eight deterministic
representatives from each family were searched. Exact rational replay owns 85
of 96 representatives; every dominant family contributes between five and
eight owners. These 85 persisted owners cover 1,530 targets.

The leading family has multiplicities `2,1^15`, bundle types `(6,1,9)`, support
cycle rank six, and two triangles. It contains 319,522 structural-remainder
rows. A full-family run was started and reached 16,000 exact rows, owning
15,324 (`95.775%`), before the bounded execution window ended. This partial
progress is diagnostic only and is not included in the persisted owner count.
No incomplete family scan is promoted to a theorem claim.

## Artifacts

- `experiments/rank7_order11_defect_transport_gram_lane.py` implements the exact lane.
- `experiments/test_rank7_order11_defect_transport_gram_lane.py` checks the defect sequence, rational PSD cycle core, and exact replay.
- `experiments/rank7_order11_defect_transport_gram_lane.json` authenticates the full stratification and representative classifications.
- `experiments/rank7_order11_defect_transport_gram_owners.jsonl.xz` persists the 85 exact owner records and certificates.

This is a new partial owner lane, not a full order-eleven theorem. Exactly
11,394,540 structural-remainder orbits remain after its persisted owners.

## Dominant-family closures

The completed full-family scans now close the first three dominant families.
The leading family has `319,522` rows: typed defect transport owns `319,513`
and nine stronger direct rational correlation Grams close the exact failure
stream. The second family has `300,610` rows and no failures. The third family
has multiplicities `2,1^15`, bundle types `(5,1,10)`, support cycle rank six,
and one triangle. Typed defect transport owns `297,395` of its `297,397` rows.

The two third-family failures are source rows `212134` and `3924348` (kernel
identities `(15429,52)` and `(15932,555)`, with orbit sizes one and two). For
each row the closure stores a stronger direct spectral/packet rational Gram:
eleven rational unit branch vectors together with exact equal-angle rational
chains for the canonical realization and every one-path `+2` frontier. Exact
`Fraction` replay verifies every Gram inner product and every path cost, with
the maximum frontier cost at most six. Thus this is a rational Gram proof, not
a numerical eigenvalue acceptance.

Canonical-plus-coordinate domination and fixed-parity path-cost monotonicity
lift these packets to every simple realization with the prescribed parity.
One-vertex DNN additivity, assigning each attached tree its tree Gram, supplies
the arbitrary rooted-tree lift. Hence all `297,397` third-family rows are now
theorem-owned. Removing the two rescued rows from the global stream leaves the
exact remainder at `10,477,105` orbits and `15,035,535` physical rows.

Additional authenticated artifacts are:

- `experiments/rank7_order11_leading_family_closure.py` and its persisted report/owners close the nine leading-family exceptions.
- `experiments/rank7_order11_third_family_closure.py` extracts, verifies, and removes exactly the two third-family exceptions.
- `experiments/rank7_order11_third_family_closure_owners.json.xz` stores the two stronger rational Gram packets.
- `experiments/rank7_order11_after_third_family_closure_remainder.jsonl.xz` is the updated exact global remainder.
