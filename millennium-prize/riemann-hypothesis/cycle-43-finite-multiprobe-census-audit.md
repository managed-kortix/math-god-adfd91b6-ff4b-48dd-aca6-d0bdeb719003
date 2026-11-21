# Cycle 43 bounded finite multiprobe census

## Verdict and exact scope

A 192-bit Arb census now extends the three selected Cycle 43 hard blocks to
**every first-recovery start `a=2,...,255`**, using complete restricted energies
`P_N` through the explicit cap `N=256`. For each start, the block is

\[
 [a,b(a)),\qquad
 b(a)=\min\left\{b>a:
 P_a-P_b-\sum_{a\le n<b}w_nP_n\ge0\right\},
 \quad w_n=1-\frac{\log n}{\log(n+1)}.
\]

The endpoint search is finite and fails closed: if no Arb-certified endpoint
exists by 256, the script aborts rather than silently omitting the start. In
this census all 254 starts recover by the cap. There are 242 singleton blocks
and 12 longer blocks; the longest is `[219,231)`, of length 12.

The cap 256 was chosen deliberately. It contains all first-recovery blocks
associated with the certified negative bands known through 2048, including the
longest block, while keeping a clean run around one minute on the present
machine. It is a **cost cap**, not a mathematical boundary. No assertion is
made for starts `a>=256`, for a larger finite cap, or asymptotically.

All pass/fail verdicts below use outward-rounded Arb balls. Complete restricted
Vasyunin Gram entries are used, with no unit-cell cutoff. Float conversion is
used only to order greedy gains and to choose descriptive extrema *after* the
relevant signs have been certified; no floating comparison controls a verdict.
The implementation contains no Python `assert` statements, so certification is
not changed by `python -O`.

This is a finite census, not an asymptotic theorem and not an RH result.

## Families compared

On each block, at

\[
 \theta_a=\frac1{4\log a},
\]

the exact compensated square is written

\[
 \mathcal R_{\theta_a}(a,b)=\|X\|^2-N_{\theta_a}.
\]

For a probe family `S`, the certified projection margin is

\[
 M_S=b_S^TG_S^{-1}b_S-N_{\theta_a}.
\]

A block passes exactly when the Arb ball for `M_S` is nonnegative. The census
compares these predeclared families:

- affine only `{0}`;
- fixed divisor `{1}` only;
- fixed divisor `{3}` only;
- small fixed families `{0,1}`, `{0,3}`, `{1,3}`, and `{0,1,3}`;
- all squarefree current-block admissions `d in [a,b)`;
- midpoint-greedy rank over the affine probe and all squarefree `d<b`; all
  candidate gains and the retained family are evaluated by Arb interval linear
  algebra, while floating midpoints only order the candidates.

Divisor 1 is included because it is the first divisor column and provides a
second fixed benchmark beside divisor 3. “Current admissions” can be empty on
a singleton block whose start is not squarefree; this is reported as the rank
zero projection, not sent to a singular matrix solve.

## Census results

The normalized quantity below is `M_S/N_theta`; it measures projection surplus
or shortfall in units of the negative budget.

| family | certified pass | certified fail | first failure | worst `M_S/N_theta` |
|---|---:|---:|---|---:|
| affine `{0}` | 250 | 4 | `[219,231)` | -0.0667913817644573 |
| divisor `{1}` | 243 | 11 | `[218,219)` | -0.189294108543526 |
| divisor `{3}` | 243 | 11 | `[218,219)` | -0.175071537790264 |
| `{0,1}` | 251 | 3 | `[219,231)` | -0.0346966806418608 |
| `{0,3}` | 250 | 4 | `[219,231)` | -0.0624202066929158 |
| `{1,3}` | 250 | 4 | `[219,231)` | -0.116344866897262 |
| `{0,1,3}` | 251 | 3 | `[219,231)` | -0.0346034498633611 |
| current admissions | 108 | 146 | `[4,5)` | -1 (empty family) |
| midpoint-greedy | 254 | 0 | none in census | +0.0585864629515707 |

There are no equality or unresolved verdicts.

### First certified failures

1. **Fixed divisors 1 and 3 fail first at `[218,219)`.** The affine singleton
   still passes there, with normalized margin
   `+0.100078287160816`. Both fixed-divisor failures then persist across a
   cluster around the last hard band: 11 failures each.

2. **Affine only fails first at `[219,231)`.** Its projection misses the budget
   by

   \[
   \frac{M_{\{0\}}}{N_\theta}
   =-0.0667913817644573\ldots .
   \]

   The affine failures are exactly `[219,231)`, `[220,231)`, `[221,231)`, and
   `[222,226)` within the census.

3. **Adding divisor 1 is the strongest tested fixed repair, but it still
   fails.** `{0,1}` reduces the worst normalized deficit to
   `-0.0346966806418608`; `{0,1,3}` changes this only slightly to
   `-0.0346034498633611`. The fixed families therefore do not certify all
   finite blocks.

4. **Current-block admissions are not a robust mechanism.** They fail on all
   three originally selected hard blocks and on 146/254 blocks overall. Many
   failures are the structural rank-zero case in which `[a,a+1)` contains no
   squarefree admission. Even when nonempty, current admissions fail at such
   blocks as `[39,42)`, `[95,103)`, and `[219,231)`.

5. **Greedy rank succeeds throughout this finite range.** Rank 1 suffices on
   250 blocks; exactly four blocks need rank 2. They are

   | block | greedy family | certified `M_S/N_theta` |
   |---|---|---:|
   | `[219,231)` | `{0,215}` | +0.556384587207409 |
   | `[220,231)` | `{0,215}` | +0.576892465734975 |
   | `[221,231)` | `{0,215}` | +0.603305949820445 |
   | `[222,226)` | `{0,215}` | +0.600896295531877 |

   Thus the same **old** divisor 215 repairs every affine failure. This is a
   useful finite geometric fact, but it does not give a current-admission-only
   or uniform arithmetic theorem.

## Projection and budget-margin scaling

The finite data show a clear late-band compression of the normalized margin.
For affine only, the smallest passing margin is

\[
 M_{\{0\}}/N_\theta
 =+0.0585864629515707\ldots
 \quad\text{on }[226,230),
\]

whereas the worst affine failure is `-0.0667913817644573...` on `[219,231)`.
The large positive maximum `50.779289099955...` occurs at the early singleton
`[5,6)` and should not be read as an asymptotic scale. It mainly demonstrates
that raw margins across very small and moderate starts are incomparable;
normalization by `N_theta` is essential.

The exact compensated residual itself stays positive on every first-recovery
block, as it must for this choice of endpoint, but its ratio to the budget is
smallest on `[219,231)`:

\[
 \mathcal R_\theta/N_\theta
 =0.880251114287194\ldots .
\]

The successful greedy projection has a still smaller worst surplus ratio,
`+0.0585864629515707...`, on `[226,230)`. Hence the difficult regime is not a
loss of positivity of the exact residual; it is failure of low-complexity
fixed probe families to capture enough of the positive square.

These are extrema of a 254-block finite table. They are not fitted rates, do
not establish monotonicity in `a`, and do not justify extrapolation.

## Reproduction

From this directory:

```text
uv run --with python-flint python cycle43_finite_multiprobe_census.py \
  --cap 256 --bits 192 \
  --json cycle43-finite-multiprobe-census-results.json

uv run --with python-flint python -m unittest -v \
  test_cycle43_finite_multiprobe_census.py \
  test_cycle43_divisor_admission_multiprobe.py \
  test_complete_gram.py test_cycle40_complete_diagnostics.py
```

The focused census tests use cap 16 to keep routine test cost small. The saved
JSON is the reproducible full cap-256 certificate table, including every Arb
interval, every selected family, every greedy trace, family counts, first
failures, and normalized extrema.

## Limitations

- This is an exhaustive census of starts only in `2<=a<256`; it is not an
  exhaustive search over all possible blocks or all possible probe families.
- The endpoint of each block is selected by the half-strength first-recovery
  rule; other endpoints may behave differently.
- The greedy family is optimization-dependent in its *ordering*. Its reported
  certificate is rigorous, but the chosen family and rank are not claimed
  canonical or globally minimal.
- Only singleton rank minimality is immediate when rank 1 passes. No exhaustive
  combinatorial rank-2 search was performed.
- Fixed-family failures refute only those finite certificates; they do not
  prove that the exact residual is negative.
- Current-admission failures do not exclude useful old-divisor, mixed, or
  differently organized probes.
- No later-scale uniformity, asymptotic estimate, Nyman--Beurling closure, or
  Riemann-hypothesis conclusion is claimed.
