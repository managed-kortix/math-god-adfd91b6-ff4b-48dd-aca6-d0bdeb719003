# Cycle 37: smooth averages of the complete endpoint decrement

## Exact discrete average

Let

\[
 c_a(Y)=\mu(a){\log(Y/a)_+\over\log Y},\qquad
 f_Y(t)=1+\sum_{a\geq1}c_a(Y)\{t/a\},
\]

where `log(u)_+=max(log(u),0)`. Put

\[
 P_Y=\int_1^\infty f_Y(t)^2{dt\over t^2}.
\]

Fix `W in C_c^infinity((1,2))`, not necessarily nonnegative, and define

\[
 Z_X=\sum_{N\geq1}W(N/X),\qquad
 \mathcal D_X={1\over Z_X}\sum_{N\geq1}W(N/X)(P_N-P_{2N}).
\tag{37.1}
\]

Assume `Z_X!=0`. Introduce the complete endpoint Gram coefficients

\[
 g_a=\int_1^\infty\{t/a\}{dt\over t^2},\qquad
 G_{a,b}=\int_1^\infty\{t/a\}\{t/b\}{dt\over t^2}.
\tag{37.2}
\]

Then the exact averaged decrement is

\[
 \boxed{\mathcal D_X=
 2\sum_{a\leq4X}L_X(a)g_a+
 \sum_{a,b\leq4X}Q_X(a,b)G_{a,b},}
\tag{37.3}
\]

with coefficient kernels

\[
 \boxed{L_X(a)={1\over Z_X}\sum_NW(N/X)
 [c_a(N)-c_a(2N)]}
\tag{37.4}
\]

and

\[
 \boxed{Q_X(a,b)={1\over Z_X}\sum_NW(N/X)
 [c_a(N)c_b(N)-c_a(2N)c_b(2N)].}
\tag{37.5}
\]

The upper limit `4X` can be replaced by the largest integer below twice the
largest `N` in the support. Equations (37.3)--(37.5), rather than a product of
separately averaged coefficients, are the correlation-preserving interchange.
In general,

\[
 Q_X(a,b)\ne
 \langle c_a(N)-c_a(2N)\rangle_W
 \langle c_b(N)+c_b(2N)\rangle_W.
\]

Such a factorization would discard the common-scale correlation. All
interchanges here are unconditional. The `N`, `a`, and `b` sums are finite,
while `|{t/a}|<=1` and `int_1^infinity t^(-2)dt=1`.

There is also an exact scale-space form. Reindexing only the second term of
(37.1) gives

\[
 \boxed{\mathcal D_X={1\over Z_X}\sum_{M\geq1}
 \left[W(M/X)-{\bf1}_{2\mid M}W(M/(2X))\right]P_M.}
\tag{37.6}
\]

The parity comb in (37.6) is essential. A discrete average cannot be replaced
exactly by a smooth weight on all `M`.

## Continuous model and Mellin kernels

The continuous scale average identifies what smoothing can and cannot do.
Normalize `int W(y)dy=1`, set

\[
 \ell_{X,y}(r)={\log(y/r)_+\over\log(Xy)},
\]

and omit the exterior Mobius factors. The linear and quadratic coefficient
kernels corresponding to (37.4)--(37.5) are

\[
 \mathcal L_X(r)=\int W(y)
 [\ell_{X,y}(r)-\ell_{X,2y}(r)]dy,
\tag{37.7}
\]

\[
 \mathcal Q_X(r,s)=\int W(y)
 [\ell_{X,y}(r)\ell_{X,y}(s)
  -\ell_{X,2y}(r)\ell_{X,2y}(s)]dy.
\tag{37.8}
\]

Here `r=a/X`, `s=b/X`, and `ell_(X,2y)(r)` means
`log(2y/r)_+/log(2Xy)`. The arithmetic kernels in (37.3) are
`mu(a) mathcal L_X(a/X)` and
`mu(a)mu(b) mathcal Q_X(a/X,b/X)` in this model.

For `Re z,Re w>0`,

\[
 \int_0^y\log(y/r)r^{z-1}dr={y^z\over z^2}
\tag{37.9}
\]

gives

\[
 \boxed{\widetilde{\mathcal L}_X(z)={1\over z^2}
 \int W(y)\left({y^z\over\log(Xy)}
 -{(2y)^z\over\log(2Xy)}\right)dy,}
\tag{37.10}
\]

\[
 \boxed{\widetilde{\mathcal Q}_X(z,w)={1\over z^2w^2}
 \int W(y)\left({y^{z+w}\over\log^2(Xy)}
 -{(2y)^{z+w}\over\log^2(2Xy)}\right)dy.}
\tag{37.11}
\]

These formulas retain both members of each dyadic difference before any
estimate. Continuous `C_c^infinity` averaging gives rapid decay in `Im z` in
(37.10). In (37.11) it gives rapid decay in the total frequency `Im(z+w)`,
with the additional algebraic factors `z^-2w^-2`. It does not give independent
rapid decay along the anti-diagonal `Im(z+w)=0`. That surviving direction is
exactly a pair correlation, not a defect of the interchange.

For the continuous analogue of (37.6), changing `M=2N` yields

\[
 {1\over X}\int W(N/X)(P_N-P_{2N})dN
 ={1\over X}\int [W(M/X)-\tfrac12W(M/(2X))]P_MdM.
\tag{37.12}
\]

Under the Mellin convention `int H(y)y^zdy`, the bracket has multiplier
`(1-2^z)int W(y)y^zdy`. The zero at `z=0` is the averaged decrement
cancellation. The factor and one-half depend on using additive measure `dN`;
logarithmic measure `dN/N` instead gives the corresponding bracket
`W(y)-W(y/2)`.

## Discrete smoothing does not have global Mellin decay

The exact discrete transforms contain sums of the form

\[
 S_{X,j}(\tau)={1\over Z_X}\sum_N
 {W(N/X)(N/X)^{i\tau}\over\log^j N}.
\tag{37.13}
\]

Below the lattice scale, Euler--Maclaurin or Poisson summation recovers the
rapidly decreasing continuous transform with a discretization error. There is
no uniform Schwartz bound for all `tau`: the phase increment is `tau/N`, and
Poisson aliases or stationary points appear once `|tau|` is comparable with
`X` and beyond. Equivalently, the parity comb in (37.6) is an exact nonsmooth
remnant of the integer scale lattice.

Thus continuous scale averaging has Mellin-Schwartz decay in total frequency.
Exact integer averaging has useful pre-Nyquist decay after a quantitative
sum--integral comparison, but no global rapid decay merely because `W` is
smooth. Neither version removes the anti-diagonal pair-correlation direction.

## Comparison with the restricted shell

The normalized restricted shell is

\[
 E_N=\sum_{N/2\leq k<N}{N\over k(k+1)}
 \left(kA_N-{\psi(k)\over\log N}\right)^2.
\tag{37.14}
\]

A smooth average of `E_N-E_(2N)` can also be interchanged. It smooths the outer
scale and produces a Mellin transform in the common scale variable, but the
inner shell ratio `k/N in [1/2,1)` and the same-scale zero-pair Gram block
remain. It again decays in total pair frequency, not uniformly along the
anti-diagonal.

There are three decisive differences from (37.1):

1. Equation (37.1) is the complete endpoint decrement itself and has the exact
   coefficient kernels (37.4)--(37.5); no omitted endpoint ranges or
   unsmoothing step is present.
2. The complete average has the exact scale telescope (37.6). The restricted
   shell average telescopes only shell energies and has no identity with the
   complete `P_N` sequence.
3. Positivity or cancellation of an averaged restricted-shell decrement does
   not imply `liminf P_N=0`. A theorem for complete averages could feed a
   variable-block dissipation argument, but only after explicit covering,
   sign/error, and divergent accumulated-weight hypotheses are supplied.

## Route verdict

Smooth averaging is structurally better on the complete endpoint functional
than on the restricted shell: it preserves every coefficient correlation and
directly averages the target energy sequence. It does produce Mellin decay,
but only for the continuous scale model (or quantitatively below the integer
lattice scale), and only in total pair frequency. The hard anti-diagonal
correlation survives. Averaging is therefore not by itself a pair theorem or a
dissipation theorem; its concrete value is to replace the atomic total-
frequency kernel by (37.10)--(37.11) without losing endpoint ranges.
