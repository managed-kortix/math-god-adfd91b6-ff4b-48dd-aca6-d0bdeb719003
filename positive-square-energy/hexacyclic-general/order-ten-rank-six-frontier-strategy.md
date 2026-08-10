# Order-ten rank-six cubic frontier: exact census and strategy

## Scope

This note records an exact finite reduction for the 66 order-ten rank-six
suppressed kernels. It is a census and attack plan, not a theorem. No claim is
made that the remaining rational frontier has been closed.

Every kernel in this slice is cubic. Indeed it has 10 vertices and 15 edges,
so the degree sum is 30; minimum degree three forces degree sequence `3^10`.
The frozen rank-six fixture contains exactly K1133--K1198, hence 66 kernels.

## Exact sparse census

For a supported pair of multiplicity `m`, a physical parity state records only
the number `o in {0,...,m}` of odd paths. Thus the physical row count for a
kernel is `product_e (m_e+1)`. The implementation keeps only support
coordinates, computes the full multigraph automorphism group by exact
backtracking, and traverses the resulting mixed-radix parity orbits.

The exact totals are:

| set | count |
|:---|---:|
| cubic kernels | 66 |
| physical parity rows | 1,508,832 |
| automorphism orbits | 497,572 |
| tetrahedral DNN-certified orbits | 372,115 |
| tetrahedral residual orbits | 125,457 |
| canonical plus 15 coordinate frontiers | 2,007,312 |

The frontier policy is one canonical shortest realization plus every
one-coordinate length-`+2` realization. There are 16 targets per residual
orbit because each cubic kernel has 15 paths.

## Exact DNN tetra sieve

The coarse sieve uses restricted-growth colorings of the 10 branch vertices by
at most four colors, corresponding to a regular tetrahedron. For each sparse
support, a superset-min transform gives the least crossing weight compatible
with the mandatory odd bundles. The acceptance comparison is integral after
scaling costs by 30; no floating-point value can certify an orbit.

For a support edge of multiplicity `m` containing `o` odd paths, the sparse
implementation combines crossing weight `18m` with adjustment `10-13o` when
`o>0`. The exact threshold is `30*5=150`. This is the same tetrahedral sieve
used in the order-eight pipeline, specialized here to the cubic order-ten
support.

## Signed-five-cycle equality candidates

The candidate recognizer is structural rather than numerical. It contracts
the singleton-edge forest and asks whether the five doubled bundles form a
five-cycle on the five quotient classes. Across the high-order lineage it finds
exactly:

```text
K971  (order 9):  singles 07,16,25,34;    doubles 08,18,27,36,45
K1133 (order 10): singles 08,17,29,35,46; doubles 09,18,26,37,45
```

For K1133, every doubled bundle must be mixed: one odd and one even path. The
five singleton parities give 32 labeled rows, which collapse to 8
automorphism orbits. All 8 lie in the tetrahedral residual. They generate 128
canonical/coordinate template targets.

For every singleton parity choice, contract with its sign and use on the five
quotient classes

`Q = I - S/2`,

where `S` is the correspondingly switched five-cycle adjacency matrix. The
verifier constructs the rational 10-by-10 Gram, checks every principal minor,
checks zero transformed cost on the singleton forest, and checks exact cost
`5*(1/3+2/3)=5` on the mixed doubled cycle. Duplicating a unit vector twice
gives the zero-cost coordinate `+2` extension. These 128 targets therefore
have exact candidate templates; this remains only one component of the open
frontier strategy.

## Residual strategy

The finite attack should proceed in this order:

1. Remove the 128 K1133 signed-cycle template targets from the 2,007,312-target
   frontier and search the rest with the compact shared-witness format already
   used at order eight.
2. Optimize once per residual orbit, then try a single rational branch Gram
   shared by all 16 targets. Store only branch parameters and canonical/extended
   internal paths.
3. For failed shared witnesses, run exact per-target rational reconstruction;
   floating-point optimization may propose vectors but never closes a target.
4. Classify numerical nulls by quotient combinatorics before adding any new
   symbolic family. In particular, test signed contractions and low-rank Gram
   patterns rather than assuming K1133 is exhaustive.
5. Keep a fail-closed manifest keyed by `(kernel, parity-orbit, frontier)` and
   report the result as open unless the exact covered-key set equals all
   2,007,312 targets.

The cubic support makes this materially smaller than a dense 45-coordinate
enumeration: support width is at most 15, and parallelism lowers it further.
The expensive phase is therefore exact rational closure, not the parity census.

## Reproduction

```sh
python3 positive-square-energy/experiments/rank6_order10_cubic_frontier_census.py
python3 -O positive-square-energy/experiments/rank6_order10_cubic_frontier_census.py \
  --verify positive-square-energy/experiments/rank6_order10_cubic_frontier_census.json
```

The exact-rational generator implements the residual phase in an `R10G1`
binary stream compressed with XZ. It regenerates the canonical residual range,
uses payload-free K1133 tags, stores one realization when all 16 frontiers can
share branch vectors, and otherwise stores a 16-bit success bitmap followed by
independent exact witnesses. The verifier decodes the compressed artifact and
recomputes every rational unit vector and cost using `Fraction`:

```sh
python3 positive-square-energy/experiments/rank6_order10_cubic_exact_rational.py \
  --start 0 --count 100 --output /tmp/rank6-order10-00000.r10g.xz
python3 positive-square-energy/experiments/rank6_order10_cubic_exact_rational.py \
  --verify-pack /tmp/rank6-order10-00000.r10g.xz
```

New runs checkpoint every 500 residual rows by default. Each checkpoint is an
independently canonical, XZ-compressed `R10G1` pack in
`OUTPUT.fragments/fragment-START-STOP.r10g.xz`; no sidecar state is used. On
restart, the generator exactly replays the maximal ordered fragment prefix,
continues at its first missing row, and deterministically merges record bodies
under one unchanged `R10G1` header. `--checkpoint-rows` changes the interval and
`--fragment-directory` places the fragments explicitly. The final
`--verify-pack` path now also rejects noncanonical encodings before exact
rational replay. Existing running generators retain their already loaded code
and output behavior; this architecture applies to processes started after the
change.

A full run is deliberately not the default: the generator requires an explicit
positive `--count`. A one-residual smoke run with one restart, 80 iterations,
and denominators through 4096 took 11.1 seconds including 8.8 seconds to
regenerate the complete residual stream. Search and exact round-trip audit took
0.04 seconds, closed all 16 targets with a shared witness, and produced 799 raw
bytes or 564 XZ bytes. This smoke point is not an unresolved-rate estimate.

The canonical census artifact is
`positive-square-energy/experiments/rank6_order10_cubic_frontier_census.json`.
Its SHA-256 is
`9398293928c8ad8dfe53788f89921a3d6764a2d31eba9ec17b5e00b6578397b5`.
The verifier also derives K971 and K1133 from the frozen fixture and explicitly
prints `scope=EXACT_CENSUS_AND_STRATEGY_ONLY full_theorem=false`.
