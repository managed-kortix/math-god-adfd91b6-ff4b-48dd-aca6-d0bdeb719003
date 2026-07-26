# Exact shell first differences

Put `n=N/2`, `L=log(2N)`, and index the coarse rows and unit triangular
shell columns by `n<=k,d<N`.  Thus

\[
 U_{k,d}={\bf1}_{d\leq k}.
\]

For the scale-`2N` odd source, define the odd-divisor Mobius--log
convolution

\[
 \chi(m)=\sum_{\substack{q\mid m\\q\ {m odd}}}
 \mu(q)\log{2N\over q},
 \qquad X(t)=\sum_{m\leq t}\chi(m).
\]

If `m_o=m/2^{v_2(m)}` is the odd part of `m`, then the elementary divisor
identity gives the exact collapse

\[
 \boxed{\chi(m)=L\,{\bf1}_{m_o=1}+\Lambda(m_o)\,{\bf1}_{m_o>1}.}
\]

In particular, `chi(r)=Lambda(r)` for every odd `r>1`.  Opening the floor
sum in `Hx` now gives

\[
 (Hx)_k={1\over L}\left(X(2k)+{k\over2k+1}\chi(2k+1)\right).
\]

Consequently, for

\[
 z_k=\bar c_k-(Hx)_k,
 \qquad
 \bar c_k=1+A\left(2k+{k\over2k+1}\right),
\]

the unique coefficient supported on the triangular shell and satisfying
`U gamma^sh=z` is obtained by first differences.  Its boundary coordinate is

\[
 \boxed{
 \gamma_n^{\rm sh}=z_n
 =1+A\left(2n+{n\over2n+1}\right)
 -{1\over L}\left(X(2n)+{n\over2n+1}\Lambda(2n+1)\right).}
\]

The boundary is essential: replacing it by an ordinary first difference
loses the constant and all arithmetic accumulated below the shell.  For every
`n<d<N`, cancellation of the two neighboring odd terms yields

\[
 \boxed{
 \gamma_d^{\rm sh}=A\left(2+{1\over(2d-1)(2d+1)}\right)
 -{1\over L}\left[
 \chi(2d)+{d\over2d-1}\Lambda(2d-1)
 +{d\over2d+1}\Lambda(2d+1)
 \right].}
\]

Here

\[
 \chi(2d)=L\,{\bf1}_{d_o=1}+\Lambda(d_o)\,{\bf1}_{d_o>1},
\]

so the interior coefficient depends only on the odd part of `d` and the two
adjacent odd von Mangoldt values.  This is an exact local collapse, not a
Mertens sum.  Only the single boundary coordinate retains the cumulative
quantity `X(N)`.

## Discrepancy from the preceding taper

With

\[
 a_d=\mu(d){\log(N/d)\over\log N},
 \qquad \alpha={\log2\over\log(2N)},
\]

compare the shell coefficient representing `z` with the preceding-scale
normalized Mobius taper by putting

\[
 \Delta_d=\gamma_d^{\rm sh}-a_d.
\]

Then, including `d=n`, the exact discrepancy is simply

\[
 \boxed{
 \Delta_d=\gamma_d^{\rm sh}
 -\mu(d){\log(N/d)\over\log N}.}
\]

For `d>n`, substitution of the local formula gives

\[
 \boxed{\begin{aligned}
 \Delta_d={}&A\left(2+{1\over(2d-1)(2d+1)}\right)
 -{\chi(2d)+{d\over2d-1}\Lambda(2d-1)
 +{d\over2d+1}\Lambda(2d+1)\over L}\\
 &-\mu(d){\log(N/d)\over\log N},
 \end{aligned}}
\]

while `Delta_n` is the displayed boundary value `gamma_n^sh-a_n`.

This coefficient comparison is a declared **shell-supported gauge**, not an
intrinsic comparison in the full coarse dictionary.  The complete coarse floor
matrix has a large right kernel, so adding any kernel vector changes the
coefficients without changing their image or energy.  All valid conclusions
below are therefore stated after applying the floor transform.  The intrinsic
objects are the preceding completed vector, the weighted pair average, and
their difference.

## Energy identity

Let `W_-=diag(N/[k(k+1)])` on `n<=k<N`, and first omit the even fine source,
so `tilde y=c-Ox`.  The pair average of `tilde y` is exactly `z`, and hence

\[
 U\gamma^{\rm sh}=z.
\]

The exact normalized odd-source fine-shell energy is therefore

\[
 \boxed{
 \|\widetilde y\|_{W_+}^2
 =\|U(a+\Delta)\|_{W_-}^2
 +\sum_{k=n}^{N-1}{N\over(2k+1)^2}
 \left(A-{\Lambda(2k+1)\over L}\right)^2.}
\]

Equivalently, its comparison with the shell image of the preceding taper is

\[
 \boxed{\begin{aligned}
 \|\widetilde y\|_{W_+}^2-\|Ua\|_{W_-}^2
 ={}&2\langle Ua,U\Delta\rangle_{W_-}
 +\|U\Delta\|_{W_-}^2\\
 &+\sum_{k=n}^{N-1}{N\over(2k+1)^2}
 \left(A-{\Lambda(2k+1)\over L}\right)^2.
 \end{aligned}}
\]

For completeness, the actual fine completed vector is `y=tilde y-Ee`, whose
pair average is `z-Ce`; the even columns do not alter the jump square.  Define

\[
 \xi(m)=\sum_{\substack{q\mid m\\q\ {m odd}}}\mu(q)\log{N\over q}
 =\log N\,{\bf1}_{m_o=1}+\Lambda(m_o){\bf1}_{m_o>1}.
\]

The shell first differences of `Ce` are

\[
 p_n=-{1\over L}\sum_{m\le n}\xi(m),\qquad
 p_d=-{\xi(d)\over L}\quad(n<d<N),
\]

because `e_q=-mu(q)log(N/q)/L` for odd `q` and is zero otherwise.  Thus the
actual effective shell coefficient is `gamma^sh-p`, and the corresponding
actual discrepancy from `a` is `Delta-p`.  Exactly,

\[
 \boxed{\|y\|_{W_+}^2=\|U(a+\Delta-p)\|_{W_-}^2
 +\sum_{k=n}^{N-1}{N\over(2k+1)^2}
 \left(A-{\Lambda(2k+1)\over L}\right)^2.}
\]

In the original unscaled fine weights, divide these normalized energy
identities by `2N`.  The convolution collapse makes every interior coordinate
local, but it gives no sign for the mixed discrepancy energy; the affine odd
prime-power jump remains a separate positive square.

## Exact/Arb analyzer through N=8192

`analyze_effective_shell.py` evaluates the complete actual vector `y`, rather
than forming dense floor matrices.  A linear Mobius sieve and divisor-sum
prefixes evaluate every floor transform, while one first-difference pass
inverts `U`.  Its complexity is `O(N log N)` time and `O(N)` storage.

The analyzer independently computes the fine cells, their weighted pair
average, the shell-supported effective coefficient and its reconstruction.  It
also computes the actual preceding completed vector

\[
 u_k=1+kA_N-\sum_{d\le N}a_d\lfloor k/d\rfloor
 =kA_N-\psi(k)/\log N,
\]

not merely the raw floor image of `a`.  Put `delta=z-u`.  Then

\[
\boxed{E_N-E_{2N}
=-2\langle u,\delta\rangle_{W_-}
-\|\delta\|_{W_-}^2-R_{\rm jump}.}
\]

This is the invariant image-space comparison.  Contraction is equivalent to

\[
\langle u,\delta\rangle_{W_-}
\le-{1\over2}(\|\delta\|_{W_-}^2+R_{\rm jump}).
\]

At 192-bit Arb precision the principal values are:

| N | preceding completed | effective coarse | `||delta||^2` | affine jump | complete fine | decrement |
|---:|---:|---:|---:|---:|---:|---:|
| 32 | 0.230388530474 | 0.159014339830 | 0.188351590541 | 0.055787361239 | 0.214801701070 | +0.015586829405 |
| 128 | 0.265616480213 | 0.295574521456 | 0.645617098547 | 0.056781250899 | 0.352355772355 | -0.086739292141 |
| 512 | 0.343600905034 | 0.664406178981 | 1.39449796470 | 0.050669504613 | 0.715075683595 | -0.371474778561 |
| 2048 | 1.31472424493 | 2.29132937697 | 5.81223026251 | 0.046377909798 | 2.33770728676 | -1.02298304183 |
| 8192 | 2.39909254553 | 6.21871415002 | 10.6054806940 | 0.041563921340 | 6.26027807136 | -3.86118552583 |

Every run certifies entrywise pair-average reconstruction and the independent
energy identity

\[
 \boxed{E_{\rm fine}=E_{\rm effective\ coarse}+E_{\rm affine\ jump}.}
\]

The shell contribution is not monotonically contracting: it is positive at
`N=32` and negative at the four larger displayed scales.  These values concern
this normalized shell recurrence, not the complete Nyman--Beurling norm over
all ranges.  They demonstrate that the needed correlation has no persistent
finite sign in this formulation.  This is a finite exact/Arb audit, not an
asymptotic estimate.

Finally, the jump square itself has the unconditional asymptotic

\[
 R_{\rm jump}={1\over2\log(2N)}
 -{1/4+\log2\over\log^2(2N)}+o(\log^{-2}N).
\]

Its leading prime-square term is not canceled by the affine center.  Any
contraction theorem must obtain a matching favorable contribution from the
mixed image-space correlation.

## Reproduction

```sh
uv run --with python-flint python analyze_effective_shell.py
uv run --with python-flint python -m unittest -v test_effective_shell.py
```
