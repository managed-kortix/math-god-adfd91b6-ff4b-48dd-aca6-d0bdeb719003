# Euler-product audit for the weighted lag-`log 2` zero Gram

## Verdict

The Euler product does constrain the unweighted **one-zero** Fourier mode at
`log 2`.  Landau's explicit formula gives, for fixed `x>1`,

\[
 \sum_{0<\gamma\leq T}x^\rho
   =-{T\over2\pi}\Lambda(x)+O_x(\log T),
\tag{1}
\]

with `Lambda(x)=0` unless `x` is an integral prime power.  Thus, at `x=2` and
under RH,

\[
 \sum_{0<\gamma\leq T}e^{i\gamma\log2}
   =-{T\log2\over2\pi\sqrt2}+O(\log T).
\tag{2}
\]

This rules out applying the phase-concentrated abstract zero models to the
actual zeta zeros: the Euler product fixes a large negative first Fourier
coefficient.  It does **not**, however, determine the sign of the finite
weighted affine Gram difference `D_N`.  The proposed use of Landau's formula
changes a one-zero statement into a claim about a two-zero quadratic statistic
without supplying the required comparison theorem.

## 1. What Landau actually controls

Formula (1) is a linear spectral identity.  Its left side has one zero index,
and its prime-power main term comes from the pole of `-zeta'/zeta`.  Uniform
versions due to Landau and Gonek add errors depending on `x`, `T`, and the
distance from `x` to a prime power; none of those complications matters for the
fixed exact value `x=2`.

Weights such as `1/rho` or a smooth height cutoff can be inserted by partial
summation or by choosing another test function in the explicit formula.  That
still produces a **linear** statistic

\[
 L_f(x;T)=\sum_{\rho\in Z(T)} f(\rho)x^\rho.
\tag{3}
\]

It can determine a rank-one quadratic expression only when that expression is
literally separable:

\[
 \sum_{\rho,\sigma}\overline{a_\rho}a_\sigma
 x^{\bar\rho+\sigma}
 =\left|\sum_\rho a_\rho x^\rho\right|^2.
\tag{4}
\]

Equation (4) is nonnegative before any arithmetic is used.  Landau may estimate
the linear factor, but supplies no ordering between two different quantities
of the form (4).

## 2. The shell Gram is a two-zero statistic

The zero block in `finite-zero-shell-gram.md` is

\[
 K^{(N)}_{\rho\sigma}={S_N(\bar\rho+\sigma)\over\bar\rho\sigma}
 \left({1\over\log^2N}-{2^{\bar\rho+\sigma}\over\log^2(2N)}\right).
\tag{5}
\]

Under RH its off-diagonal phase is
`exp(i(eta-gamma) log 2)`, but this observation does not turn (5) into the
one-zero sum (2).  Expanding `S_N` shows exactly what is present:

\[
 \sum_{\rho,\sigma}K^{(N)}_{\rho\sigma}
 =\sum_{k=N/2}^{N-1}w_k
 \left(
  \left|\sum_\rho{k^\rho\over\rho\log N}\right|^2
  -\left|\sum_\rho{(2k)^\rho\over\rho\log(2N)}\right|^2
 \right).
\tag{6}
\]

So each half is a positive Gram energy, but their difference is indefinite.
Moreover, the actual `D_N` also contains the affine row, trivial-zero and
half-jump terms, odd interpolation, `R_jump`, and the common-cutoff remainder.
The diagonal of (5), or the sign in (2), cannot dominate these terms by
positivity.

There is a limited but important distinction.  If one isolates only the pure
factor `exp(i(eta-gamma) log 2)` with separable weights, its double sum is a
modulus square and can be reduced to a one-zero sum as in (4).  The full shell
kernel is a weighted superposition over `k`, followed by subtraction at the
two scales.  Reduction of the individual squares therefore recovers the
explicit formula for `psi(k)` and `psi(2k)`; it does not prove their required
inequality.

## 3. The missing pair theorem

A genuine zero-side route needs a theorem for the **weighted two-point
measure**, not merely Landau's formula.  In one possible formulation, it must
control, with a common zero cutoff and uniformly in the dyadic scale,

\[
 \sum_{\rho,\sigma\in Z(T)}
 {S_N(\bar\rho+\sigma)\over\bar\rho\sigma}
 \left({1\over\log^2N}-{2^{\bar\rho+\sigma}\over\log^2(2N)}\right),
\tag{7}
\]

together with the affine and truncation terms, strongly enough to establish
the desired sign after cancellation.  Equivalently, it could establish a
one-sided comparison between the two weighted norms in (6), with an error
smaller than their difference.  No theorem of this form has been identified.

Montgomery's pair-correlation theorem is not that result.  Even under RH, its
proved asymptotic concerns a particular height-localized, translation-type
pair statistic in a restricted Fourier-support range.  The pair-correlation
conjecture extends the limiting law, but remains an averaged asymptotic.  The
present kernel has `1/(bar rho sigma)` weights, a finite Mellin shell factor,
two unequal logarithmic normalizations, boundary and affine terms, and asks
for a one-sided statement at every relevant `N`.  A limiting pair-density law
does not by itself give such a finite, cancellation-scale sign.

In particular, the fact that fixed physical lag `log 2` corresponds to a small
normalized pair-correlation frequency at large height does not solve the
problem.  It may describe a bulk average, while the target is a difference of
two nearby Gram energies whose residual can be much smaller than either bulk
term.

## 4. Circularity on returning to primes

Applying the explicit formula separately to the two linear sums in (6) gives

\[
 \sum_\rho {k^\rho\over\rho}
 = k-\psi_0(k)-\log(2\pi)-{1\over2}\log(1-k^{-2})
\tag{8}
\]

in the symmetric limiting convention.  Substituting (8) into (6), with the
required endpoint corrections, reconstructs the original prime-side shell
square difference.  This is an exact change of coordinates, not a new bound.

Likewise, standard derivations of pair correlation through the explicit
formula turn the off-diagonal zero sum into mean squares or correlations of
Dirichlet polynomials supported on prime powers.  For this kernel, the needed
one-sided error is precisely a weighted prime/prime-power correlation across
the moving dyadic window.  Assuming that correlation in order to prove the
Gram sign assumes the unresolved arithmetic content in another notation.

The circularity test is therefore:

1. expand the proposed zero theorem by the explicit formula;
2. retain all diagonal, endpoint, and truncation terms;
3. compare the resulting prime sum with the original `D_N`;
4. if the claimed input is the same one-sided cross-window quadratic bound,
   the route is circular rather than an Euler-product proof.

## 5. Adversarial conclusions

1. **Euler-product constraint exists:** (2) is real, sign-sensitive arithmetic
   information absent from the abstract density models.
2. **Wrong statistic for the target:** it controls a one-zero Fourier
   coefficient, whereas the Gram sign depends on a weighted two-zero measure
   plus affine and remainder terms.
3. **Squaring does not fix the comparison:** separability yields positive
   individual norms, but `D_N` is their difference and has no PSD sign.
4. **Known pair correlation is insufficient:** its averaging, normalization,
   test class, and error scale do not provide the uniform one-sided comparison
   required here.
5. **Prime-side conversion is circular unless new:** an explicit-formula
   reduction reproduces the original weighted prime-pair/cross-window problem.

Accordingly, Landau's formula closes the logical gap in the abstract-model
audit only to this extent: actual zeta zeros cannot have arbitrary lag-`log 2`
one-point phase.  It does not close the sign gap for the weighted shell Gram.
The missing ingredient is a new, quantitatively sharp weighted pair-correlation
inequality (or an equivalent prime-pair theorem), not another invocation of the
Euler product identity.

## References

- E. Landau, *Ueber die Nullstellen der Zetafunktion*, Math. Ann. 71 (1912),
  548--568; classical source of (1).
- S. M. Gonek, uniform Landau-type formulas for sums over zeta zeros; the
  uniform refinements affect errors, not the one-zero/two-zero distinction.
- H. L. Montgomery, *The pair correlation of zeros of the zeta function*,
  Proc. Sympos. Pure Math. 24 (1973), 181--193.
- D. A. Goldston, *Notes on Pair Correlation of Zeros and Prime Numbers*,
  arXiv:math/0412313.
