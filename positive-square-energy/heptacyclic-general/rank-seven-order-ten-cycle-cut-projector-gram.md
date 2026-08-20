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

## Non-scalar cycle metrics

The extended lane fixes the canonical greedy spanning tree and writes its seven
fundamental flows as columns `z_i`.  It tests exact diagonal cycle metrics

`Q_w = Z diag(w_1,...,w_7) Z^T`

in addition to the intrinsic scalar projector.  If `L_i` is the physical
length of the fundamental cycle, `s_i=z_i^T z_i` its flow support, and
`R_i=(P_cut)_{e_i,e_i}` the effective resistance of its chord, the rational
profiles are

`w_i=1/L_i`, `w_i=(1-R_i)/R_i`, `w_i=1/s_i`, and
`w_i=(1-R_i)/(L_i R_i)`.

All weights are nonnegative rationals: a chord lies on a cycle, so
`0<R_i<1`.  Hence `Q_w=sum_i w_i z_i z_i^T`, and the congruence and
diagonal-completion argument above proves PSD without numerical eigenvalues.

## Representative result and boundary

The deterministic leading sample contains 1,000 authenticated structural
remainder orbits, all from the degree multiset `(5,3^9)`.  The exact finite
ratio family

`a=1`, `b/a in {0,1/16,1/8,1/4,1/2,1,2,4,8,16}`, `D_defect=2/3`

owns 16 rows.  Its minimum exact bound is `21287/4290 < 6`.  Thus it yields
272 exact sample target certificates.  Fifteen accepted rows use the pure cut
projector (`b=0`); one needs the balanced cut/cycle metric (`b=1`).

The extended deterministic scan uses the same leading 1,000 authenticated
rows, all five cycle profiles, the same ten cycle/cut ratios, and defect scales
`{1/3,1/2,2/3,3/4,1}`.  It owns 25 rows, or `2.5%`, with minimum exact bound
`431/90`.  This adds 9 rows and raises coverage by `56.25%` relative to the
persisted `1.6%` baseline.  Each accepted row owns its canonical target and
sixteen single-path plus-two frontiers, for 425 exact sample certificates.
The optimizer selects the projector profile for all 25 witnesses, at defect
scale `3/4`; the new diagonal profiles add no incremental owner in this sample.
Thus the gain is real for the extended exact lane, but is attributable to the
broader defect scaling rather than to a non-scalar cycle weight.

This remains a sampled lane, not a full owner theorem: no full
8,196,239-row scan is claimed.  It does establish materially stronger exact
coverage from rational non-scalar flow metrics and defect scaling while
retaining a symbolic PSD certificate.

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
