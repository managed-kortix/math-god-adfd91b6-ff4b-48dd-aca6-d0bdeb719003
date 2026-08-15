# Rank-seven order-eight parametric Gram lane

## Exact family

For a residual row, let `S` be its signed bundle matrix,

```text
S_uv = m_uv - 2 r_uv,  S_uu = 0,
```

where `m_uv` is bundle multiplicity and `r_uv` is its number of odd paths. For
any rational `t >= 0`, define

```text
H(t) = (I+tS)^2,
M(t) = max_i H(t)_ii = 1+t^2 max_i (S^2)_ii,
G(t) = H(t)/M(t) + diag(1-H(t)_ii/M(t)).                 (1)
```

This is a correlation Gram. Indeed, `H(t)/M(t)` is a square Gram, and the
diagonal correction in (1) is nonnegative. Equivalently, a feature embedding is
obtained by taking the rows of `(I+tS)/sqrt(M(t))` and appending one private
coordinate of squared length `1-H(t)_ii/M(t)` to vertex `i`. This gives a
sum-of-squares PSD proof for every signed support and every nonnegative `t`.

For a path of length `L` from `u` to `v`, put

```text
z = (-1)^L G(t)_uv.
```

Whenever `z>-1`, the usual equal-angle/geodesic construction has cost at most

```text
(1-z)/(L(1+z)).                                         (2)
```

Thus a row is certified if the sum of (2) over its fourteen canonical paths is
at most six. Replacing one `L` by `L+2` leaves `z` fixed and decreases its
summand, so one accepted Gram owns the canonical target and all fourteen
coordinate frontiers.

The family is exactly the requested polynomial ansatz with a diagonal
correction:

```text
G_off = (2t S + t^2 S^2)/M(t).
```

The normalization is deliberately global. Vertexwise normalization of
`(I+tS)^2` gives a larger numerical lane, but generally introduces square roots
and therefore does not directly supply rational waypoint certificates.

## Exact order-eight scan

The verifier searches all reduced positive rationals `t` in `[1/32,4]` with
denominator at most 32. Binary64 arithmetic only orders proposals; every
accepted cost is recomputed with `Fraction`. On the authenticated 492,812-row
rational-search complement it gives:

| quantity | count |
|:--|--:|
| certified rows | 204,766 |
| certified canonical-plus-frontier targets | 3,071,490 |
| unresolved rows | 288,046 |
| unresolved targets | 4,320,690 |
| certified among the solved first 5,000 | 1,356 |
| unresolved among the solved first 5,000 | 3,644 |

Hence (1) is a substantial payload-free theorem lane, covering 41.55% of the
rational-search rows, but it is not a complete order-eight theorem. The
committed report has SHA-256
`57bd9da7d1483f6132a3cf54f15bf18b4733c74a384395585cc208b876d3b6fe`.

Including the 605 rows already removed by the balanced-rank-one,
signed-imbalance, and simplex/mixed lanes, the payload-free union on the full
493,417-row order-eight residual manifest is 205,371 rows and 3,080,565 of
7,401,255 targets. The same 288,046 rows and 4,320,690 targets remain.

The most frequently selected grid value is `t=1/2`, owning 16,813 rows after
the recognizer chooses the cheapest successful grid coefficient. The first
stream obstruction already has best grid cost

```text
6670661/974170 > 6.
```

The hardest grid obstruction found has best cost

```text
289662404903/28660388465 > 10.
```

These are obstructions to this one-parameter SOS family, not to the desired
spectral inequality and not to arbitrary low-rank Grams.

## Ansatz obstructions and next theorem lanes

1. A fixed global pair `(alpha,beta)` in
   `I+alpha S+beta S^2+diagonal correction` cannot close even the solved sample:
   the larger exact PSD cone `beta>=alpha^2/4`, normalized by
   `1+beta max_i(S^2)_ii`, covers only 1,347 of the first 5,000 on the tested
   denominator-16 grid. The square curve `alpha=2t,beta=t^2` covers 1,356.
2. Signed degrees alone are too coarse. The solved sample has 1,262 degree
   signatures but 5,000 distinct exact witness Grams, and the prior exact
   finite-library audit found no witness transferable to a second row.
3. The unnormalized diagonal-dominance ansatz
   `G_off=alpha S+beta(S^2)_off` is too conservative: no tested
   denominator-12 pair certified any of the first 5,000 rows under its direct
   row-sum PSD proof.
4. The feature-square family with vertexwise unit normalization numerically
   certifies 347,781 rows (70.57%) when `t` is searched on a coarse logarithmic
   grid, but its correlations contain graph-dependent square roots. A theorem
   lane would need an algebraic Gram/waypoint audit or a rational lower envelope
   preserving the cost bound.
5. The remaining viable parametric direction is not a universal scalar pair.
   It is a typed diagonal scaling
   `X=D_0+D_1 S` keyed to signed degree/local parity, followed by an SOS
   diagonal completion. Fitting parameters by vertex type, while retaining a
   rational global normalizer, preserves the proof shape of (1) and directly
   addresses the 3,644 solved-sample obstructions.

## Reproduction

```text
python3 positive-square-energy/experiments/rank7_order8_parametric_gram_ansatz.py
python3 positive-square-energy/experiments/rank7_order8_parametric_gram_ansatz.py \
  --audit positive-square-energy/experiments/rank7_order8_parametric_gram_ansatz_coverage.json
```

The report locks the source-stream digest, exact coefficient grid, exact
coverage arithmetic, explicit obstruction rows, and classification-stream
SHA-256.
