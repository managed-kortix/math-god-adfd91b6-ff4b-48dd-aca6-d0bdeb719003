# Cycle 43 finite multiprobe: independent reproduction

## Scope

This is a finite computational cross-check only. It is not an asymptotic
statement and not a claim about the Riemann hypothesis.

The reproduction used 256-bit Arb arithmetic and did **not** import
`cycle43_divisor_admission_multiprobe.py`. It independently:

1. assembled each block vector in the direct sum
   \(\bigoplus_{a\le n<b} L^2(0,1)\) from coefficient rows in the basis
   \(\chi,\rho_1,\rho_2,\ldots\);
2. contracted those rows against the complete restricted Vasyunin Gram kernel;
3. reconstructed endpoint energies by a separate dense coefficient
   contraction;
4. evaluated rank-one projections as \(c^2/g\) and rank-two projections by the
   explicit two-by-two adjugate formula, without the Cycle 43 solve routine;
5. used a separately assembled Arb matrix only for the rank-4 and rank-8 local
   full spans; and
6. failed closed whenever a required interval sign was not strict.

After all values had been reconstructed, the verifier compared its intervals
with the existing 192-bit result JSON. There were **zero discrepancies**.

## Reproduced data

### Endpoint residuals

The direct compensated-square residual and the independently assembled dense
endpoint expression

\[
 P_a-P_b-2\theta\sum_{a\le n<b}w_nP_n
\]

overlap on every block:

| block | 256-bit residual |
|---|---:|
| `[39,42)` | 0.003901062344163216373919192028210443360794617555920 |
| `[95,103)` | 0.002128104513152294800733944945012148049092865679358 |
| `[219,231)` | 0.000856062369488739248499647681556222556494788081302 |

All three residuals are certified positive.

### Exhaustive singleton census

The atomic pool is the affine column `0` together with all squarefree divisor
columns below the right endpoint.

| block | passing / pool | passing labels |
|---|---:|---|
| `[39,42)` | `14/28` | `0,1,2,3,5,6,7,10,11,13,14,15,17,19` |
| `[95,103)` | `7/64` | `0,1,2,3,5,6,7` |
| `[219,231)` | `0/144` | none |

Thus rank one is impossible in the stated atomic pool for `[219,231)`. This
minimality statement is pool-relative, not a claim about arbitrary probe
classes.

### Rank-two families on `[219,231)`

The independent adjugate calculation reproduces:

| family | projection margin | verdict |
|---|---:|---|
| `{0,215}` | +0.000541095490072153224415352224986421610524306126146 | PASS |
| `{3,215}` | +0.000345482926515570288104440144694461250201313421398 | PASS |

The verifier additionally scanned every rank-two family of the two natural
forms:

- affine plus one divisor: `129/143` pass;
- two distinct divisor columns: `538/10153` pass.

This confirms rank-two existence independently of the midpoint-greedy
selection. It also shows the examples are not unique.

### Full local-admission spans

Using every squarefree divisor first admitted in the current block still
fails:

| block | local family | rank | projection | margin | verdict |
|---|---|---:|---:|---:|---|
| `[39,42)` | `{39,41}` | 2 | 0.000657551536670901566684679747227251343 | -0.000682733076477011544339807408626184857 | FAIL |
| `[95,103)` | `{95,97,101,102}` | 4 | 0.000109650248090062552037075376232896636 | -0.001285805403127520654054131584003727826 | FAIL |
| `[219,231)` | `{219,221,222,223,226,227,229,230}` | 8 | 0.000180757113542042399654318664948748030 | -0.000791763517893860253999673451483615599 | FAIL |

Each determinant and final sign is strict at 256 bits.

### The 227/229 edge

For the last block, the independent rank-two formula gives:

| family | margin | verdict |
|---|---:|---|
| `{0,227}` | +0.000028078565171581225616117105159550214582457763615 | PASS |
| `{0,229}` | -0.000038912550272026534711082041396017159896528504968 | FAIL |

The scan of all current local affine pairs is monotone at this edge in the
listed order: `219,221,222,223,226,227` pass, while `229,230` fail. The
published 227/229 boundary is therefore reproduced.

## Independence audit of the listed tests

The original nine-test suite is useful regression coverage but is **not fully
independent** of the implementation it tests:

- Strongest existing check: the endpoint identity calls
  `complete_energies`, which is a genuinely different recurrence/dense-energy
  route from the Cycle 43 positive-square assembly.
- Weak/tautological checks: `test_probe_gram_and_correlation_match_direct_column_expansion`
  rewrites the same methods, coefficients, base Gram object, and sums used by
  the implementation. It would not catch a shared definition or normalization
  error.
- Internal-consistency checks: projection monotonicity/boundedness are valuable
  invariants, but they do not independently reconstruct the claimed values.
- Regression rather than independent verification: singleton counts, selected
  families, local-span failures, prefixes, and 227/229 verdicts all call the
  production `certificate()`/`projection()` routines whose outputs they
  assert.
- Shared dependency remains here too: both implementations use
  `certify_complete_gram.RestrictedGram` for the complete Vasyunin kernel and
  `mobius_sieve`. Thus this reproduction is independent of the Cycle 43
  projection code and block assembly, but it does not fully replace the
  analytic Vasyunin formula. As a spot-check of that shared layer, direct
  reciprocal-cell integrals rigorously bracketed the entries `(1,2)`, `(3,5)`,
  `(39,41)`, and `(227,229)`. Existing small symbolic and recurrence tests add
  partial coverage; neither the spot-check nor those tests constitute a second
  derivation of every Gram entry.

Bottom line: the listed tests are adequate as regression tests but, by
themselves, are not independent enough to justify calling the multiprobe
numbers independently reproduced. The direct block-Hilbert reconstruction,
dense endpoint path, closed rank-one/rank-two formulas, 256-bit precision, and
exhaustive pair scans close the main projection-level independence gap. The
selected direct cell brackets also probe the shared base kernel. A still
stronger audit would independently evaluate every base Gram entry, or provide a
separately derived cotangent implementation.

## Verifier artifacts

Both files are under the RH dossier:

- `cycle43_independent_multiprobe_verifier.py` — independent reconstruction and
  fail-closed checks;
- `cycle43-independent-multiprobe-results.json` — full 256-bit interval output,
  singleton margins, local spans, pair-scan summaries, and post-reconstruction
  discrepancy list.

Reproduce with:

```bash
cd /workspace/research/millennium-prize/riemann-hypothesis
uv run --with python-flint python cycle43_independent_multiprobe_verifier.py
```
