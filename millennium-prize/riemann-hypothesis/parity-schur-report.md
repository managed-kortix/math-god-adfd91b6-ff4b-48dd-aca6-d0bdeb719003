# Weighted parity Schur audit

The analyzer `analyze_parity_schur.py` splits the fine floor transform

\[
 F_{k,d}=\lfloor k/d\rfloor,\qquad N\leq k<2N,\quad 1\leq d\leq 2N,
\]

into even columns `E` and odd columns `O`.  The even columns are the canonical
dyadic embedding of the coarse columns because
`floor(k/(2a)) = floor(floor(k/2)/a)`.  With exact shell weights
`w_k=1/(k(k+1))`, the code selects a canonical independent basis `B` of `E`
and computes over the rationals

\[
 P=(B^TWB)^{-1}B^TWO,\qquad R=O-BP,
 \qquad S=R^TWR.
\]

It independently verifies the Schur formula

\[
 S=O^TWO-O^TWB(B^TWB)^{-1}B^TWO
\]

and the weighted orthogonality `B^T W R = 0` exactly.

## Exact ranks

| N | rank(E) | rank(O) | rank(F) | rank(S) |
|---:|---:|---:|---:|---:|
| 2 | 1 | 2 | 2 | 1 |
| 4 | 2 | 4 | 4 | 2 |
| 8 | 4 | 8 | 8 | 4 |
| 16 | 8 | 16 | 16 | 8 |
| 32 | 16 | 32 | 32 | 16 |
| 64 | 32 | 64 | 64 | 32 |

Thus the odd residual has exact rank `N/2` in every tested dyadic case.  The
Schur complement is positive semidefinite by its exact residual Gram
factorization; no floating-point rank decision is used.

In fact the even columns span the entire pair-constant space, so the Schur
complement has the exact odd-divisor incidence formula

\[
 S_{d,e}=\sum_{\substack{N<r<2N\\r\ {m odd}\\d\mid r,\ e\mid r}}
 {1\over2r^2},
 \qquad d,e<2N\text{ odd}.
\]

The analyzer verifies this entrywise over the rationals.  The residual of one
odd column is supported on pairs `(r-1,r)` for odd multiples `r`: its values are
`-(r-1)/(2r)` and `(r+1)/(2r)`, respectively, and its weighted pair energy is
exactly `1/(2r^2)`.

## Actual Mobius coefficients

At 192-bit Arb precision the analyzer uses the actual normalized coefficients

\[
 a_d=\mu(d)\frac{\log(2N/d)}{\log(2N)}.
\]

It reports weighted even and odd energies, their signed cross term, the
projected odd energy, residual Schur energy, coarse energy, and all relevant
cross terms.  The key numerical values are:

| N | even energy | odd energy | even/odd cross | residual energy | direct fine energy |
|---:|---:|---:|---:|---:|---:|
| 2 | 0.0625000 | 1.31649596 | -0.28302005 | 0.034890363 | 0.812955857 |
| 4 | 0.2925547 | 2.38881142 | -0.83224947 | 0.020916426 | 1.016867134 |
| 8 | 0.6718532 | 3.69854148 | -1.57465144 | 0.006592037 | 1.221091816 |
| 16 | 1.1835333 | 5.40124941 | -2.52678307 | 0.004243050 | 1.531216550 |
| 32 | 1.8754338 | 7.82674421 | -3.83044980 | 0.001404816 | 2.041278432 |
| 64 | 2.8751305 | 11.55558001 | -5.76315567 | 0.000711032 | 2.904399204 |

Arb certifies that projected-odd/residual and combined-coarse/residual cross
terms contain zero (radii below `3e-57` in this run).  It also verifies

\[
 \|Oa_o\|_W^2=\|BPa_o\|_W^2+a_o^TSa_o
\]

and independently cross-checks the direct fine image energy against both

\[
 \|Ea_e+Oa_o\|_W^2
 =E_e+2C_{eo}+E_o
 =E_{\rm coarse}+E_{\rm residual}.
\]

For the actual odd Mobius-log coefficients, divisor convolution removes the
Mobius signs exactly:

\[
 \sum_{d\mid r}\mu(d){\log(2N/d)\over\log(2N)}
 ={\Lambda(r)\over\log(2N)}\qquad(r>1).
\]

Therefore the Schur residual energy is not merely numerically small; it is
exactly

\[
 \boxed{R_N={1\over2\log^2(2N)}
 \sum_{\substack{N<r<2N\\r\text{ odd}}}{\Lambda(r)^2\over r^2}.}
\]

The Arb analyzer independently evaluates this prime-power formula and certifies
overlap with the projected residual energy.  Standard weighted PNT asymptotics
give `R_N~1/(4N log N)`.  Thus orthogonalization exposes a nonzero prime
diagonal at the critical normalization; it does not create extra Mobius
cancellation.

The negative even/odd cross term is substantial; the exact Schur residual is
positive but small for these actual Mobius vectors.  This is a finite audit
through `N=64`, not an asymptotic estimate.

## Reproduction

```sh
uv run --with python-flint python analyze_parity_schur.py --N 2 4 8 16 32 64
uv run --with python-flint python -m unittest -v test_parity_schur.py
```
