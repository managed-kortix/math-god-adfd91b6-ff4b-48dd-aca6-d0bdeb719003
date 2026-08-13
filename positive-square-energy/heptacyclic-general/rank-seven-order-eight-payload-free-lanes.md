# Rank-seven order-eight payload-free lanes

## Scope

The exact residual manifest contains 493,417 rank-seven/order-eight coarse
residual orbits.  Each row has fourteen canonical paths and therefore fifteen
targets: the canonical row and every one-coordinate length-plus-two frontier.
The complete target universe is

```text
493417 * 15 = 7401255.
```

The recognizers below are sufficient lanes only.  They do not classify every
possible equality Gram and do not promote the residual census to a theorem.

## Payload-free certificates

### Balanced signed rank one

If every bundle is parity-uniform, require that the signed support be balanced.
Thus there are signs `epsilon_u` such that an even bundle has
`epsilon_u epsilon_v=1` and an odd bundle has `epsilon_u epsilon_v=-1`.
The Gram matrix `G_uv=epsilon_u epsilon_v` is PSD of rank one.  After the odd
endpoint switch, every physical path has coincident endpoints and cost zero.
The same remains true after adding two to any path length, so the mode owns all
fifteen targets without a numerical payload.

### Signed-imbalance PSD

For a bundle of multiplicity `m_uv` with `r_uv` odd paths, put

```text
s_uv = m_uv - 2 r_uv,
d = max_u sum_v |s_uv|,
G(q) = I + S/q,  q >= d.
```

The matrix `qI+S` is symmetric diagonally dominant with nonnegative diagonal,
hence PSD; consequently `G(q)` is a rational correlation matrix.  For a path
of length `L`, set `t=(-1)^L G_uv`.  Its exact geodesic upper bound is

```text
(1-t)/(L(1+t)).
```

The recognizer checks integer `q` from `d` through twice the maximum weighted
degree and accepts only when the exact sum is at most six.  Lengthening one path
replaces `L` by `L+2` with the same `t`, so every accepted canonical row also
owns all fourteen frontiers.  The finite `q` interval is a deterministic
sufficient search policy, not a converse statement.

### Simplex and mixed atoms

Signed zero-cost singleton contractions form a quotient.  A mixed doubled pair
has correlation `-sigma/2` and cost one.  A regular simplex on `w` quotient
classes prescribes correlation `-sigma/(w-1)` on its complete support and has
cost

```text
C(w-1,2): K3 -> 1, K4 -> 3, K5 -> 6.
```

The exact cost-six profiles found at order eight are `K5`, `K4+K4`,
`3 mixed+K4`, and `6 mixed`.  The recognizer requires consistent prescriptions
and an exact PSD completion via the running-intersection or signed path/cycle
criterion.  Zero-cost contractions remain zero after lengthening; every other
atom path becomes strict.  Thus a recognized atom row owns all fifteen targets
without storing vectors or rational parameters.

## Exact coverage

The lanes are applied in the disjoint owner order balanced rank one, signed
imbalance PSD, then simplex/mixed atom.  The exact full-manifest scan gives:

| exclusive owner | rows | targets |
|:--|--:|--:|
| balanced signed rank one | 86 | 1,290 |
| signed-imbalance PSD | 291 | 4,365 |
| simplex/mixed atom | 228 | 3,420 |
| union | 605 | 9,075 |

The raw atom lane recognizes 230 rows; two are also balanced rank one and are
assigned to the first lane.  The atom owner's disjoint profile counts are 113
`K5`, 43 `K4+K4`, 63 `3 mixed+K4`, and 9 `6 mixed`.

The resulting rational-search universe is exactly

```text
493417 - 605 = 492812 residuals,
7401255 - 9075 = 7392180 targets.
```

The reduction is modest (0.1226% of rows and targets), but all 9,075 removed
targets need only a mode tag and exact reconstruction rather than an expensive
rational witness search.

## Reproduction

```text
python3 positive-square-energy/experiments/rank7_order8_payload_free_lanes.py recognize \
  --output positive-square-energy/experiments/rank7_order8_payload_free_lane_coverage.json \
  --unresolved-output positive-square-energy/experiments/rank7_order8_rational_search_indices.json

python3 positive-square-energy/experiments/rank7_order8_payload_free_lanes.py audit \
  positive-square-energy/experiments/rank7_order8_payload_free_lane_coverage.json
```

The recognizer authenticates every compressed census chunk and emits exact
coverage arithmetic plus a classification-stream SHA-256.  Auditor mode
regenerates the selected scan and requires byte-identical canonical JSON.
