# Dyadic endpoint cell-pairing audit — 2026-07-26

This finite audit attacks local spatial pairing and fixed-window positivity for
the complete dyadic endpoint cell contributions `J_k`. It is reconnaissance
plus selected 192-bit Arb certificates, not an asymptotic theorem.

## Certified counterexamples

- `N=8`: `J_35=-0.000117934772969833...`, although the centered triple
  `J_34+J_35+J_36=0.00201529155187544...` is positive.
- `N=16`: adjacent triple absorption fails:
  `J_38+J_39+J_40=-0.00209987729926661...`. The larger block `[34,49]` is
  positive, with sum `0.00328417374383206...`.
- `N=32`: the length-512 block `[91,602]` is negative,
  `-0.000111843568435015...`; extending to `[91,741]` makes it only barely
  positive, about `4.35e-7`.
- `N=64`: the length-4096 block `[91,4186]` remains negative,
  `-0.00179856827752541...`.

## Pairing failures

A greedy rule pairing each negative cell with the nearest unused positive
divisor-event cell required maximum distances `1,7,105,508` for
`N=8,16,32,64` on `[1,16N]`, and failed outright for `N=128` and `256`.
Fixed lags `+-1,...,+-4` already all fail for `N=16` in the tested range.

Finite-horizon candidate shortest positive window lengths changed as the
horizon increased. At horizons up to roughly one million, candidates were `5`
for `N=8`, `22` for `N=16`, `651` for `N=32`, and no success through `4096`
for `N=64`. The first two margins were around `1e-12`, so they are not robust
structural patterns.

## Verdict

No fixed nearby pairing or fixed translated-window positivity principle is
supported. The viable target must be anchored and cumulative, or aggregate
across dyadic scales before taking absolute values. Exact Abel identities for
that target are recorded in
`millennium-prize/riemann-hypothesis/abel-divisor-impulses.md`.
