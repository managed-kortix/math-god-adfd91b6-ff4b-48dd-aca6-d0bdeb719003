# Cycle 45: fixed-strength correlation-dispersion census

## Scope and conclusion

This is a finite, certified diagnostic anchored to the exact definitions and
normalizations in commit `4306d7ce`, especially equations (1.5), (6.3)--(6.4),
and (8.1)--(8.4), at the fixed value

\[
\theta=\frac25
\]

on the dyadic blocks \([a,2a)\), for

\[
a\in\{32,64,128,256,512,1024\}.
\]

The two row intervals were declared before the computation:
\(I=[1,2]\) and the interior interval \(I=[1,3/2]\). All reported values are
outward 192-bit Arb enclosures. An identity interval that does not contain zero
causes the driver to abort.

The census finds strong finite Möbius cancellation. The unsigned diagonal
comparison \(\Delta_a(I)\) is increasingly dominated by \(W^2\), while the
signed off-diagonal term nearly cancels it. At \(a=1024\),
\(L D_a/\Delta_a\) is only \(0.0470752\ldots\) on \([1,2]\) and
\(0.0411209\ldots\) on \([1,3/2]\). Neither \(L D_a/\Delta_a\) nor
\(L^3D_a\) is monotone over the six scales.

These facts do **not** certify convergence, a positive liminf, an asymptotic
lower bound, a projection theorem, or any implication for the Riemann
hypothesis.

## Exact normalization

For squarefree \(q,d<2a\), put

\[
b_q(n)=\frac{\log q}{\log n}-\eta_n,
\]

\[
H_a(q,d)=\sum_{\max(a,q,d)\le n<2a}
 w_nA_n b_q(n)b_d(n),
\]

\[
H_a^0(q)=\sum_{\max(a,q)\le n<2a}
 w_nA_n\eta_n b_q(n).
\]

The census uses the **unsigned** kernel

\[
W_a(q,d)=\langle\rho_q,\rho_d\rangle H_a(q,d),
\qquad
\beta_a(q)=-g_qH_a^0(q),
\]

with no \(\mu(q)\) or \(\mu(d)\) hidden in \(W_a\). The de-signed
correlation is

\[
\widehat c_a(q):=\mu(q)c_q
 =\beta_a(q)+\sum_{\substack{d<2a\\\mu(d)^2=1}}
   \mu(d)W_a(q,d).
\]

For the predeclared squarefree row set

\[
S_a(I)=\{q:\mu(q)^2=1,\ q/a\in I\},
\]

define

\[
D_a(I)=\sum_{q\in S_a(I)}\widehat c_a(q)^2
      =\|M_ax_a\|_2^2,
\]

where \(x_a=(1,(\mu(d))_{d\in\mathcal D_a})\), and

\[
\Delta_a(I)=\|M_a\|_F^2
 =\sum_{q\in S_a(I)}
 \left(\beta_a(q)^2+
       \sum_{\substack{d<2a\\\mu(d)^2=1}}W_a(q,d)^2\right).
\]

The existing `CompensatedBlock.correlation(q)` already includes the outer
\(\mu(q)\), so its exact comparison is

```text
hat_c(q) = mu(q) * CompensatedBlock.correlation(q).
```

No second Möbius factor is inserted into the existing signed Gram entries.
Thus the computed `D` is literally \(\|M_ax_a\|_2^2\), and the computed
`Delta` is literally \(\|M_a\|_F^2\); there is no normalization
contradiction with commit `4306d7ce`. The driver also checks the independent
direct contraction of \(X\), and it checks

\[
D=\beta^2+W^2+2\beta\!\sum_d\mu(d)W_d
  +2\sum_{d<e}\mu(d)\mu(e)W_dW_e.
\]

## Certified census

Here `offdiag` denotes the last signed \(d\ne e\) term in the displayed
decomposition and \(L=\log a\). Each entry is midpoint `±` Arb radius.

### \(I=[1,2]\)

| \(a\) | rows | \(D\) | \(\Delta\) | offdiag | \(LD/\Delta\) | \(L^3D\) | \(L^2\Delta\) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 32 | 19 | 0.000330397916686 ± 2.50e-29 | 0.00198646546118 ± 4.95e-28 | -0.00181248749282 ± 2.83e-28 | 0.576436864596 ± 3.50e-26 | 0.0137538314028 ± 4.37e-27 | 0.0238600829467 ± 3.40e-27 |
| 64 | 39 | 0.000167719538545 ± 4.16e-29 | 0.00160631661534 ± 2.71e-28 | -0.00151673324602 ± 1.23e-28 | 0.434239392746 ± 1.73e-26 | 0.0120646240464 ± 2.88e-27 | 0.0277833477293 ± 1.52e-27 |
| 128 | 79 | 3.73856648259e-05 ± 4.71e-30 | 0.00128184474832 ± 8.26e-29 | -0.00126137043922 ± 2.15e-28 | 0.141511971251 ± 3.30e-26 | 0.00427046937018 ± 1.34e-28 | 0.0301774424626 ± 7.32e-28 |
| 256 | 157 | 3.31719945435e-05 ± 3.28e-30 | 0.00107167402785 ± 2.86e-28 | -0.00105376752881 ± 1.32e-28 | 0.171642300878 ± 4.68e-26 | 0.00565611107259 ± 3.90e-29 | 0.0329528970635 ± 1.05e-27 |
| 512 | 310 | 4.90863811215e-06 ± 3.50e-31 | 0.000926430899527 ± 4.57e-29 | -0.000921402615362 ± 2.21e-29 | 0.0330533858770 ± 5.30e-28 | 0.00119169447680 ± 6.30e-29 | 0.0360536279470 ± 3.65e-27 |
| 1024 | 621 | 5.61768752156e-06 ± 1.10e-31 | 0.000827161850363 ± 1.23e-29 | -0.000823626539296 ± 2.06e-30 | 0.0470752400527 ± 4.47e-27 | 0.00187082843185 ± 4.07e-28 | 0.0397412404005 ± 4.15e-27 |

### \(I=[1,3/2]\)

| \(a\) | rows | \(D\) | \(\Delta\) | offdiag | \(LD/\Delta\) | \(L^3D\) | \(L^2\Delta\) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 32 | 11 | 0.000324778529885 ± 2.28e-29 | 0.00191489346974 ± 1.89e-28 | -0.00174383631449 ± 1.21e-28 | 0.587811608985 ± 9.42e-27 | 0.0135199071111 ± 3.12e-27 | 0.0230004084717 ± 4.88e-27 |
| 64 | 21 | 0.000151912062624 ± 1.75e-29 | 0.00150391697565 ± 3.06e-28 | -0.00142383047929 ± 4.59e-28 | 0.420092676412 ± 4.56e-27 | 0.0109275397463 ± 1.38e-27 | 0.0260122119709 ± 2.64e-27 |
| 128 | 39 | 3.66178686261e-05 ± 2.04e-30 | 0.00117963821590 ± 5.92e-29 | -0.00116078147041 ± 4.53e-28 | 0.150614827817 ± 4.48e-26 | 0.00418276596383 ± 4.19e-28 | 0.0277712760719 ± 1.95e-27 |
| 256 | 75 | 2.78849292223e-05 ± 2.18e-30 | 0.000985861056167 ± 1.28e-29 | -0.000971246237316 ± 9.62e-30 | 0.156844496085 ± 8.97e-27 | 0.00475462085119 ± 3.81e-28 | 0.0303142346074 ± 3.31e-27 |
| 512 | 154 | 4.78630522996e-06 ± 1.01e-31 | 0.000857728903643 ± 2.91e-29 | -0.000853429077211 ± 2.98e-29 | 0.0348111456338 ± 2.58e-27 | 0.00116199511484 ± 4.60e-28 | 0.0333799733873 ± 2.63e-27 |
| 1024 | 313 | 4.55442628982e-06 ± 7.96e-32 | 0.000767708509816 ± 6.44e-30 | -0.000764873046858 ± 2.54e-29 | 0.0411209163568 ± 3.35e-27 | 0.00151673623018 ± 4.45e-28 | 0.0368847867352 ± 2.02e-27 |

The full JSON also records \(\beta^2\), \(W^2\), the beta-signed-\(W\)
cross term, four divisor-range decompositions, and all identity error balls.
For example, on \([1,2]\), \(\beta^2/\Delta\) decreases from
\(0.0263687\ldots\) at \(a=32\) to \(0.00178397\ldots\) at \(a=1024\),
while `offdiag/Delta` reaches \(-0.9957259742\ldots\).

## Reproduction and verification

From this directory, reproduce the complete 192-bit census with:

```bash
uv run --with python-flint python cycle45_dispersion_census.py \
  --starts 32 64 128 256 512 1024 \
  --intervals 1,2 1,3/2 --bits 192 \
  --json cycle45-dispersion-census-results.json
```

Run the independent selected-scale reconstruction at 256 bits with:

```bash
uv run --with python-flint python \
  cycle45_independent_dispersion_verifier.py --starts 32 128 --bits 256
```

It does not import the production Cycle 45 driver or `CompensatedBlock`. It
rebuilds \(w,A,\eta,H,H^0,W,\beta,\widehat c\) and the direct \(X\)
contraction. It reproduces the full-interval rows:

| \(a\) | \(L^3D\) | \(L^2\Delta\) | \(LD/\Delta\) |
|---:|---:|---:|---:|
| 32 | 0.013753831402791398266897174366789 ± 4.68e-34 | 0.023860082946675736591024236602093 ± 1.48e-34 | 0.57643686459638340207277646505898 ± 3.54e-33 |
| 128 | 0.0042704693701754239677975231331584 ± 3.63e-35 | 0.030177442462558831428744150731403 ± 3.21e-34 | 0.14151197125050598765082326708699 ± 3.51e-33 |

The verifier still shares `RestrictedGram` and `mobius_sieve`, so it is an
independent contraction/normalization check, not a second derivation of every
restricted Vasyunin entry.

Run the exact-rational coefficient/sign audit with:

```bash
python cycle45_exact_rational_sign_audit.py
```

This isolates Möbius placement from transcendental evaluation and verifies the
signed-row identity exactly for arbitrary rational stand-ins at
\(a=4,8,16\).

Artifacts:

- `cycle45_dispersion_census.py` — fail-closed production census;
- `cycle45-dispersion-census-results.json` — consolidated certified output;
- `cycle45_independent_dispersion_verifier.py` — independent selected-scale
  reconstruction;
- `cycle45_exact_rational_sign_audit.py` — exact-rational normalization audit;
- `test_cycle45_dispersion_census.py` — interval, identity, regression, and
  sign-audit tests.

## Finite-only interpretation

The samples show that a diagonal or random-sign heuristic does not explain the
observed correlations at these scales: structured signed off-diagonal
cancellation is decisive. They do not decide whether the small ratios persist,
recover, vanish, or oscillate later. In particular, the data provide no
certified asymptotic pattern and no theorem beyond the twelve explicitly
computed finite rows.
