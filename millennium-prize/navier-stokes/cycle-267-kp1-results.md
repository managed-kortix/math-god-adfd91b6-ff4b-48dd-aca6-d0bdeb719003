# Cycle 267 KP1 numerical outcome

`C267-KP1` froze one independently selected profile,
`u_0=K-F(K)/32`, before trajectory computation. The positive initial
velocity-`L3` derivative selected the forward direction. The declared forward
horizons were `0.5,1,2`; no output was used to alter the profile, direction,
horizons, levels, steps, gates, or thresholds.

Implicit midpoint ran at `K=7`, step `1/64`, and `K=10`, step `1/128`, with no
more than two numerical-library threads. All residual, energy, helicity,
divergence, reality, doubled-cubature, and cross-resolution gates passed. The
primary directed endpoint ratios were:

| horizon | K=7 | K=10 | absolute difference |
|---:|---:|---:|---:|
| 0.5 | 0.9716972511 | 0.9707212901 | 0.0009759610 |
| 1.0 | 0.9533249935 | 0.9515109457 | 0.0018140478 |
| 2.0 | 0.9545870128 | 0.9613563047 | 0.0067692919 |

The maximum fine-level ratio is `0.9707212901`. Thus the profile reaches
neither the frozen `1.2` architecture-signal threshold nor the `2.2`
certification threshold. The bounded singleton experiment stops without
extension or tuning.

This is finite-dimensional numerical evidence only. It is not a full Euler or
Navier--Stokes enclosure and makes no Millennium claim.
