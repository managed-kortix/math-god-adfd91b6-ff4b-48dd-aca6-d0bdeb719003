# Rank-seven order-ten weighted-cycle Gram lane

## Family and exact PSD certificate

For the sixteen physical paths, let `B` be reduced oriented incidence,
`P_cut=B^T(BB^T)^-1B`, and `P_cycle=I-P_cut`.  Let `A` be signed endpoint
incidence, with endpoint signs `1` and `(-1)^L`, and let `D` scale the unique
degree-five vertex or the two degree-four vertices.  The new family is

`H = D A (a P_cut + b P_cycle diag(q) P_cycle) A^T D`,

`G = H/M + diag(1-diag(H)/M)`, where `M=max(1,max_i H_ii)`.

This is genuinely non-scalar on cycle space.  For each physical path `e`, put
`R_e=(P_cut)_{e,e}` and use one of

- cycle leverage: `q_e=1-R_e`;
- exact resistance ratio: `q_e=(1-R_e)/R_e`;
- inverse physical length: `q_e=1/L_e`;
- leverage per unit length: `q_e=(1-R_e)/L_e`.

Every physical path lies in a cycle, so `0<R_e<1`; all four profiles are
positive rational vectors.  If `p_e=P_cycle e_e`, then

`H = a(DA P_cut)(DA P_cut)^T + b sum_e q_e (DA p_e)(DA p_e)^T`.

The remaining diagonal completion is a sum of nonnegative coordinate squares.
This is a rational PSD decomposition, with no floating point PSD decision.

## Exact cost bound

For a path `p=(u,v,L)`, set `t_p=(-1)^L G_uv`.  Exact convexity gives

`L tan^2(arccos(t_p)/(2L)) <= (1-t_p)/(L(1+t_p))`.

The lane accepts exactly when every `t_p>-1` and

`C(G)=sum_p (1-t_p)/(L_p(1+t_p)) <= 6`.

All arithmetic in `G` and `C(G)` is rational.  Lengthening any path by two
preserves its parity and weakly decreases the corresponding upper bound, so an
accepted canonical row owns itself and all sixteen one-coordinate `+2`
frontiers: seventeen targets.

## Scan result

The deterministic leading authenticated sample contains 10,000 structural
remainder rows.  The exact grid tests cycle/cut ratios
`{1/16,1/8,1/4,1/2,1,2,4,8}` and defect scales
`{1/2,2/3,3/4,1}` for every profile.

The family owns 132 rows (`33/2500`, or `1.32%`) and 205 physical orbits,
giving 2,244 exact frontier certificates.  The minimum exact bound is
`431/90`.  Selected witnesses use cycle leverage 121 times, inverse length
seven times, and leverage per unit length four times.  Thus every persisted
witness uses a non-scalar cycle metric weighted by exact effective resistance
or physical path length.

The report also counts coarse remainder signatures combining degree pattern,
multiplicity partition, parity bundle counts, odd/negative support cycle ranks,
and triangle count.  None of the 25 most frequent signatures contributes an
owner.  Owner-focused signatures are individually sharp (the largest has
26/26 sampled owners), but each has fewer than 100 sampled rows; no signature
therefore reaches the predeclared promising-family gate of at least 5%
ownership on at least 100 sampled rows.

A follow-up promotion scan uses the sharper empirical gate `owned=tested>0`.
It selects 19 owner-bearing signatures, authenticates the complete 8,192,460
row structural remainder, and finds 4,279 rows in those families.  Exact replay
owns 4,277 of them.  Eighteen signatures are uniform on the full remainder;
the remaining signature owns 57 of 59 rows.  Thus the original non-scalar
effective-resistance/length metrics already separate the promoted families;
no additional metric is needed for this pass.

After deduplication with the 132 pilot owners, the exact union contains 4,281
rows and 5,143 physical orbits, giving 72,777 frontier certificates.  Of these,
4,149 rows are new.  The two full-family failures and every row outside the
promoted signatures remain explicit: the updated remainder has 8,188,179 rows
and 11,130,021 physical orbits.  This remains a partial exact owner lane, not a
full remainder theorem.

## Artifacts and reproduction

- `experiments/rank7_order10_weighted_cycle_gram_lane.py` implements the exact lane.
- `experiments/rank7_order10_weighted_cycle_gram_lane.json` is the canonical report.
- `experiments/rank7_order10_weighted_cycle_gram_owners.jsonl.xz` stores all 132 owners and certificates.
- `experiments/rank7_order10_weighted_cycle_family_scan.py` stratifies the pilot and replays selected families completely.
- `experiments/rank7_order10_weighted_cycle_family_scan.json` records exact promoted-family coverage.
- `experiments/rank7_order10_weighted_cycle_family_owners.jsonl.xz` stores the deduplicated 4,281-owner union.
- `experiments/rank7_order10_after_weighted_cycle_remainder.jsonl.xz` stores the exact 8,188,179-row remainder.

From the repository root:

```sh
python3 -m unittest \
  positive-square-energy/experiments/test_rank7_order10_weighted_cycle_gram_lane.py

python3 positive-square-energy/experiments/rank7_order10_weighted_cycle_gram_lane.py \
  --sample-size 10000 --workers 32 --progress

python3 -m unittest \
  positive-square-energy/experiments/test_rank7_order10_weighted_cycle_family_scan.py

python3 positive-square-energy/experiments/rank7_order10_weighted_cycle_family_scan.py \
  --workers 32 --progress
```
