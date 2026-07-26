# Cycle 40: certified local kappa and half-surplus diagnostics

## Scope

This is finite diagnostic computation, not a theorem. The script
`cycle40_complete_diagnostics.py` evaluates the complete restricted energies
`P_N` from the Vasyunin Gram formula and derives, for `2 <= n < 2048`,

\[
 \kappa_n={P_n-P_{n+1}\over 2w_nP_n},\qquad
 s_n=P_n-P_{n+1}-w_nP_n,
 \quad w_n=1-\frac{\log n}{\log(n+1)}.
\]

It also scans every finite block surplus

\[
 S(a,b)=P_a-P_b-\sum_{a\leq n<b}w_nP_n
       =\sum_{a\leq n<b}s_n
\]

and records the minimum over every available endpoint `a < b <= 2048`.
All values in the CSV and JSON files are outward-rounded 192-bit Arb balls.
The PNG uses ball midpoints only and is not itself a certificate.

## Certified finite data through 2048

There are 2046 certified unit comparisons and no unresolved signs. Exactly 12
unit cells have `kappa_n < 1/2`:

```text
2, 39-40, 95-96, 99-100, 219-222, 226
```

The certified local range is

```text
minimum: n=96,  [0.3547986979999973846627614434598728203480 +/- 2.58e-41]
maximum: n=199, [1.526154189086237307702703833126310589510 +/- 1.18e-40]
```

The closest observed local value to one half is at `n=98`:

```text
[0.5007487496837444359577992296403639407211 +/- 1.95e-41]
```

No unit failure occurs from `n=227` through `2047`; the weakest local value in
that range is at `n=592`:

```text
[0.5069675703460458997180736973132578536017 +/- 1.94e-41]
```

These finite facts do not imply eventual pointwise half strength.

## Structural near-failures

The nontrivial negative units cluster in three short bands, near `39-40`,
`95-100`, and `219-226`, rather than appearing as isolated noise. Positive
unit cells inside the latter two bands do not prevent a negative cumulative
excursion. Starts with some negative finite-prefix surplus are exactly

```text
2, 39-40, 93-100, 217-222, 224-226
```

The deepest excursion is the small-index block `[2,3)`:

```text
[-0.2163669852151686212562080999600917448073 +/- 4.51e-41]
```

Away from that initial outlier, the deepest negative band starts at `a=95`
and bottoms at `b=101`:

```text
[-0.0001740937006704931758058895284638583774730 +/- 1.59e-44]
```

The longest first recovery is `[219,231)`, of length 12. Its minimum occurs at
`b=223`:

```text
[-5.009989935826748050494060361521502816857e-5 +/- 1.64e-45]
```

Every start through `2047` has a nonnegative endpoint by `2048`, reproducing
the finite stopping phenomenon while exposing where compensation is most
delayed. The data show a staircase/band structure in `kappa_n`, long smooth
arches at larger `n`, and sparse early threshold crossings. They do not
identify an asymptotic law or exclude a later failure.

## Artifacts and reproduction

The generated artifacts are:

```text
cycle40-data/local-unit-kappa.csv
cycle40-data/cumulative-half-surplus.csv
cycle40-data/summary.json
cycle40-data/diagnostics.png
```

Reproduce them with:

```text
uv run --with python-flint --with matplotlib python \
  cycle40_complete_diagnostics.py --max-N 2048 --bits 192 \
  --output-dir cycle40-data
```

Run the focused consistency tests with:

```text
uv run --with python-flint python -m unittest -v \
  test_cycle40_complete_diagnostics.py test_complete_gram.py
```
