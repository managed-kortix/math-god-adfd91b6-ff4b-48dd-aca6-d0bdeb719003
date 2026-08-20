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
