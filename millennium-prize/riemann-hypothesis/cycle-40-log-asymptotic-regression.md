# Cycle 40: finite logarithmic-asymptotic regression diagnostic

## Status and method

This note is **explicitly nonrigorous as asymptotics**. It fits finite certified
values to

\[
 P_N={C\over\log N}+{D\over\log^2N}
\tag{40.1}
\]

but does not prove that this expansion exists, bound omitted terms, provide a
statistical sampling model, or support any RH inference. The input energies for
every integer `2 <= N <= 2048` are rigorous 192-bit Arb enclosures from the
complete Vasyunin Gram evaluation. The least-squares arithmetic is also done
with Arb, so each printed coefficient ball encloses the coefficient obtained
from every point selection in the input balls under that fixed regression.
These tiny balls measure numerical enclosure error only. They do **not** measure
model misspecification or asymptotic uncertainty.

For each suffix `[N_0,2048]`, two unweighted fits are compared:

1. `P-OLS`: regress `P_N` on `1/log N` and `1/log^2 N` through the origin.
2. `LP-OLS`: regress `(log N)P_N` on `1` and `1/log N`.

The two parameterizations encode the same pointwise model but weight residuals
differently. Their agreement is a limited stability check, not a theorem. The
full energy is reconstructed exactly at finite `N` as

\[
 \mathcal P_N=P_N+A_N^2,
 \qquad
 A_N=\sum_{n\leq N}{\mu(n)\over n}
       \left(1-\frac{\log n}{\log N}\right).
\tag{40.2}
\]

## Restricted fits

The `P-OLS` results are:

| `N_0` | points | `C` | `D` | RMS residual | `cond(X'X)` |
|---:|---:|---:|---:|---:|---:|
| 32 | 2017 | 0.04649971 | 2.54700138 | 3.35e-4 | 9.60e2 |
| 64 | 1985 | 0.04469455 | 2.55892080 | 2.78e-4 | 1.65e3 |
| 128 | 1921 | 0.04520568 | 2.55548350 | 2.28e-4 | 3.00e3 |
| 256 | 1793 | 0.04458453 | 2.55974449 | 1.93e-4 | 6.13e3 |
| 512 | 1537 | 0.04510138 | 2.55614192 | 1.70e-4 | 1.59e4 |
| 1024 | 1025 | 0.04200647 | 2.57866810 | 1.36e-4 | 7.37e4 |

For `LP-OLS`, the corresponding `(C,D)` pairs are

```text
N_0=32:   (0.04587363, 2.55093006)
N_0=64:   (0.04476670, 2.55845778)
N_0=128:  (0.04504914, 2.55651759)
N_0=256:  (0.04461737, 2.55952143)
N_0=512:  (0.04484361, 2.55795474)
N_0=1024: (0.04175176, 2.58052860)
```

Across the windows ending at 2048, `D_restricted` stays in the narrow numerical
band `2.5470--2.5806`, while `C` is around `0.0445--0.0465` until the shortest
late window drops to about `0.042`. The conditional first-order constant
`C_0=2+gamma-log(4*pi)=0.0461914179...` lies near the broad-window estimates,
but this finite agreement is not evidence for the hypotheses behind that
asymptotic theorem. The late-window drift and rapidly growing normal-equation
condition number show that `C` and `D` are strongly confounded over this short
logarithmic range. High `R^2` values (`0.9977` or better for `P-OLS`) therefore
do not establish the model.

## Full versus restricted

The full `P-OLS` fits give

```text
N_0=32:   (C,D)=(0.04661851, 3.54620320)
N_0=64:   (C,D)=(0.04460149, 3.55951879)
N_0=128:  (C,D)=(0.04521435, 3.55539692)
N_0=256:  (C,D)=(0.04448602, 3.56039932)
N_0=512:  (C,D)=(0.04505995, 3.55639558)
N_0=1024: (C,D)=(0.04153749, 3.58203434)
```

Thus `D_full-D_restricted` equals, by suffix,

```text
0.99920182, 1.00059799, 0.99991342,
1.00065483, 1.00025366, 1.00336625.
```

The `LP-OLS` differences are similarly

```text
0.99964021, 1.00048073, 1.00007094,
1.00066033, 1.00048124, 1.00348669.
```

Meanwhile the fitted changes in `C` are below `1.2e-4` through `N_0=512`, with
the ill-conditioned `N_0=1024` window reaching about `-4.9e-4`. This is the
expected finite signature of `A_N^2 ~ 1/log^2 N`: restricted and full fits have
nearly the same first coefficient, while the full second coefficient is nearly
one larger. It is a diagnostic confirmation only. In particular, the exact
finite identity (40.2) does not by itself provide the asymptotic estimate or a
signed remainder needed to rigorously conclude a shift of exactly one.

## Interpretation

The robust finite observation is a positive fitted second coefficient:
approximately `D_restricted=2.56` and `D_full=3.56` over most windows and both
weightings. If (40.1) held with a sufficiently controlled remainder, Cycle 39's
calculation would predict

\[
 P_N-T_N\sim {D_{\rm restricted}\over2\log^2N}>0.
\]

That conditional sentence must not be reversed: the regressions do not prove
the expansion, eventual positivity, the critical tail inequality, or RH.
Finite Mobius oscillations, omitted higher logarithmic terms, and the severe
`C`/`D` collinearity can all bias the estimates. Extension substantially beyond
2048 and fits including a `1/log^3 N` term would test stability, but still would
not turn numerical fitting into rigorous asymptotics.

Reproduce the table with

```text
uv run --with python-flint python diagnose_log_asymptotic.py \
  --max-N 2048 --bits 192
```

and run the exact-profile regression tests with

```text
uv run --with python-flint python -m unittest -v \
  test_diagnose_log_asymptotic.py
```
