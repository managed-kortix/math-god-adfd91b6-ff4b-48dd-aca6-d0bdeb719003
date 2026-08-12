# Heptacyclic counterexample hunt

This is a reproducible counterexample search for connected simple graphs with
cyclomatic rank seven, hence `m=n+6`. It deliberately targets the unresolved
single-positive-block lane beyond the completed hexacyclic theorem.

## Scope and result

`nauty-geng -cq n n+6:n+6` was exhausted for every order `6 <= n <= 11`, a
total of 2,104,016 connected isomorphism classes. No counterexample to
`s+(G)>=n` occurs. The numerical low-tail minimizer at every order was then
recomputed using only its integer adjacency matrix, exact characteristic
polynomial, and rational Sturm intervals. Every exact lower bound is positive.

The hardest graph found is the order-eleven graph ``J?`DA`gNCh?``. It is itself
2-connected, so it is one rank-seven block rather than a favorable multiblock
example. Its exact characteristic polynomial is

```text
(x - 1)^2 (x^4 + 2x^3 - 4x^2 - 5x + 3)
          (x^5 - 10x^3 - 5x^2 + 11x - 2).
```

The accepted artifact contains no floating-point numbers. It records rational
isolating intervals for every positive root, a rational interval for `s+-n`,
and the suppressed multigraph kernel with each subdivision-path length.

## Reproduction

Run the exact fail-closed audit:

```sh
python3 positive-square-energy/experiments/heptacyclic_counterexample_hunt.py
python3 -O positive-square-energy/experiments/heptacyclic_counterexample_hunt.py
```

Reproduce an exhaustive numerical scout, for example the hardest completed
slice (the output intentionally lists graph6 codes rather than accepted
floating-point values):

```sh
python3 positive-square-energy/experiments/heptacyclic_counterexample_hunt.py --scout 11
```

The exact artifact is
`positive-square-energy/experiments/data/heptacyclic-low-surplus-exact.json`.
The census does not prove the inequality beyond order eleven; it maps the
small-order low-surplus frontier and supplies structured kernels for the next
subdivision search.
