# Rank-seven order-ten cycle/cut projector Gram

## The exact family

Let a residual order-ten kernel be expanded into its sixteen physical paths.
Orient each path from `u` to `v`, let `B` be the reduced `9 x 16` oriented
incidence matrix, and put

`P_cut = B^T (B B^T)^-1 B`,  `P_cycle = I - P_cut`.

The support is connected, so `B B^T` is a nonsingular reduced Laplacian.
Both projectors are therefore rational.  They are independent of the chosen
orientation, and

`P_cycle = Z (Z^T Z)^-1 Z^T`

for any full-rank fundamental cycle matrix `Z`.  Thus this construction uses
the intrinsic physical cut and cycle spaces rather than the Euclidean metric
of an arbitrary fundamental basis.

Encode path parity in the signed endpoint matrix `A`: the column for a path of
length `L` has value `1` at `u`, value `(-1)^L` at `v`, and zero elsewhere.
For the order-ten degree multisets, let `D` have entry `1` at degree-three
vertices and `2/3` at the defect vertices (the unique degree-five vertex or
the two degree-four vertices).  For rational `a,b >= 0`, define

`H = D A (a P_cut + b P_cycle) A^T D`,

`M = max(1, H_11, ..., H_10,10)`, and

`G = H/M + diag(1 - diag(H)/M)`.

### Rational PSD proof

The reduced Laplacian inverse is rational.  Moreover `P_cut` and `P_cycle` are
symmetric orthogonal projectors.  Hence

`H = a (D A P_cut)(D A P_cut)^T + b (D A P_cycle)(D A P_cycle)^T`

is a rational Gram matrix.  Every diagonal-completion coefficient is
nonnegative by the definition of `M`, so `G` is a rational PSD correlation
matrix.  This proves PSD symbolically for every connected physical support;
the verifier does not use floating point eigenvalues or numerical rounding.

## Exact path-cost theorem

For a physical path `p=(u,v,L)`, put `t_p=(-1)^L G_uv`.  If `t_p > -1`, the
standard convexity estimate gives

`L tan^2(arccos(t_p)/(2L)) <= (1-t_p)/(L(1+t_p))`.

Consequently the displayed Gram owns the residual row whenever the exact
rational quantity

`C(G) = sum_p (1-t_p)/(L_p(1+t_p))`

is at most six.  Replacing any `L_p` by `L_p+2` preserves its parity and weakly
decreases its summand.  One accepted Gram therefore owns the canonical row and
all sixteen single-path plus-two frontiers, for seventeen targets total.

## Representative result and boundary

The deterministic leading sample contains 1,000 authenticated structural
remainder orbits, all from the degree multiset `(5,3^9)`.  The exact finite
ratio family

`a=1`, `b/a in {0,1/16,1/8,1/4,1/2,1,2,4,8,16}`, `D_defect=2/3`

owns 16 rows.  Its minimum exact bound is `21287/4290 < 6`.  Thus it yields
272 exact sample target certificates.  Fifteen accepted rows use the pure cut
projector (`b=0`); one needs the balanced cut/cycle metric (`b=1`).

This is a genuine new geometry and a positive exact lane, but not yet a broad
owner theorem: sample coverage is `1.6%`, and no full 8,196,239-row scan is
claimed.  In particular, the result shows that the intrinsic projector metric
repairs some rows missed by the previous raw fundamental-basis pilot, while
also showing that this one-parameter spectral weighting alone is unlikely to
cover a large fraction of the remainder.  A next extension should weight the
seven cycle coordinates by signed-flow type or effective resistance rather
than by one scalar `b`.

## Reproduction

From the repository root:

```sh
python3 -m unittest \
  positive-square-energy/experiments/test_rank7_order10_cycle_cut_gram_lane.py

python3 positive-square-energy/experiments/rank7_order10_cycle_cut_gram_lane.py \
  --sample-size 1000 \
  --output positive-square-energy/experiments/rank7_order10_cycle_cut_gram_lane.json

python3 positive-square-energy/experiments/rank7_order10_cycle_cut_gram_lane.py \
  --sample-size 1000 \
  --output positive-square-energy/experiments/rank7_order10_cycle_cut_gram_lane.json \
  --audit
```

The JSON report binds the structural-owner manifest hash, records every exact
cost and selected parameter, and states the claim boundary explicitly.
