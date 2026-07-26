# Cycle 38: anti-diagonal of the complete smoothed block kernel

## Exact restriction

Retain the continuous complete-endpoint quadratic kernel from Cycle 37.  Put

\[
 a=\log 2,\qquad L_y=\log(Xy),
\]

and define

\[
 \mathcal C_X(s)=\int W(y)y^s
 \left\{\frac1{L_y^2}-\frac{2^s}{(L_y+a)^2}\right\}dy.
 \tag{38.1}
\]

Then the double Mellin transform is exactly

\[
 \widetilde{\mathcal Q}_X(z,w)
 =\frac{\mathcal C_X(z+w)}{z^2w^2}.
 \tag{38.2}
\]

For a conjugate pair `z=beta+i gamma`, `w=beta-i gamma`, the surviving
anti-diagonal restriction is therefore

\[
 \boxed{
 \widetilde{\mathcal Q}_X(\beta+i\gamma,\beta-i\gamma)
 =\frac{\mathcal C_X(2\beta)}{(\beta^2+\gamma^2)^2}.}
 \tag{38.3}
\]

On RH this becomes

\[
 \boxed{
 \widetilde{\mathcal Q}_X(\tfrac12+i\gamma,
                           \tfrac12-i\gamma)
 =\frac1{(\tfrac14+\gamma^2)^2}
 \int W(y)y\left\{\frac1{\log^2(Xy)}
 -\frac2{\log^2(2Xy)}\right\}dy.}
 \tag{38.4}
\]

Equation (38.4) is one ordered conjugate-pair entry.  After folding the zero
sum to positive ordinates, the zero-frequency diagonal coefficient of a simple
pair is exactly

\[
 \boxed{\frac{2\mathcal C_X(1)}{(\tfrac14+\gamma^2)^2}.}
 \tag{38.4a}
\]

For multiplicity `m_gamma`, this is multiplied by `m_gamma^2`.  It is not zero.
The Mellin denominators become a positive real factor; they give algebraic
height decay but no cancellation.

## Sign

For general `beta>0`, the pointwise numerator in (38.1) has the sign of

\[
 (L_y+a)^2-2^{2\beta}L_y^2.
 \tag{38.5}
\]

Since `L_y>0`, this is positive precisely when

\[
 L_y<\frac{a}{2^\beta-1},
 \tag{38.6}
\]

and negative when the inequality is reversed.  On RH the transition is

\[
 L_y=(1+\sqrt2)\log2.
 \tag{38.7}
\]

Consequently, if `W>=0` is nonzero, then

\[
 X\ge 2^{1+\sqrt2}
 \quad\Longrightarrow\quad
 \mathcal C_X(1)<0,
 \tag{38.8}
\]

with strictness because `supp W` lies in `(1,2)`.  In particular every integer
`X>=6` is in the negative regime.  More explicitly,

\[
 \mathcal C_X(1)=\int W(y)y\,
 \frac{a^2+2aL_y-L_y^2}{L_y^2(L_y+a)^2}\,dy.
 \tag{38.9}
\]

For a signed smoothing weight there is no universal sign: cancellation can be
engineered in the single scalar integral (38.9), but it is not forced by the
complete kernel.  For fixed nonnegative `W`, the large-scale expansion starts
with

\[
 \mathcal C_X(1)=-\frac{\int yW(y)dy}{\log^2X}
 +O_W(\log^{-3}X).
 \tag{38.10}
\]

Thus the RH conjugate-zero diagonal is eventually strictly negative, with
size `asymp -log^(-2)(X)(1/4+gamma^2)^(-2)`.

## Cancellation audit

### Mellin denominators

On the anti-diagonal, `z^2w^2=|z|^4`.  This factor is positive, has no phase,
and cannot cancel (38.1).  It only makes the individual conjugate contribution
summable at high ordinate.  Moving the real part changes the scalar from
`mathcal C_X(1)` to `mathcal C_X(2 beta)`; for every `beta>0` its pointwise
large-`X` sign is still negative.

### Dyadic derivative

If the logarithmic normalizations were frozen, the dyadic difference would
carry `1-2^s`, whose zero is at `s=0`.  A conjugate pair has `s=2 beta`, equal
to `1` on RH, not `0`.  With the exact normalizations the multiplier is the
stronger expression

\[
 \frac1{L_y^2}-\frac{2^s}{(L_y+a)^2},
 \tag{38.11}
\]

which likewise does not vanish at `s=1`.  The zero of the scale-space
decrement on constants therefore does not extend to the RH conjugate-zero
mode.  The dyadic derivative supplies the negative sign in the large-scale
regime rather than removing the mode.

### Affine completion

The complete explicit-formula square has a zero-free constant, affine
zero terms, and the zero-zero Hessian.  Affine completion changes the first
two pieces but not the coefficient (38.2) of a product of two zero amplitudes.
Equivalently, scaling a selected conjugate pair by a formal parameter `lambda`
leaves (38.4) as the coefficient of `lambda^2`; no constant or linear term can
cancel that coefficient identically.  At the actual zeta amplitudes the affine
and endpoint packets may numerically offset the total value, but that would be
a separate arithmetic cancellation theorem, not a kernel identity or a sign
consequence of completion.

### Zero symmetry

Conjugation makes the total expression real but reinforces this diagonal.
For `rho=beta+i gamma`, the two ordered terms `(rho,bar rho)` and
`(bar rho,rho)` are both

\[
 \frac{\mathcal C_X(2\beta)}{|\rho|^4}.
\]

They contribute `2 mathcal C_X(2 beta)/|rho|^4`, or
`2m_gamma^2 mathcal C_X(2 beta)/|rho|^4` when the ordinate has multiplicity
`m_gamma`.  The same-sign terms `(rho,rho)` and `(bar rho,bar rho)` have total
frequencies `+2 gamma` and `-2 gamma`; smoothing pairs them into a real
oscillatory contribution, but does not cancel the zero-frequency conjugate
terms.  The common minus sign of the two explicit-formula zero waves also
squares to a plus sign before the dyadic kernel is applied.

## Obstruction

For standard nonnegative smoothing and complete blocks beyond the small
transition range, the surviving anti-diagonal is a negative diagonal quadratic
form after folding by zero symmetry.  None of the four proposed mechanisms
cancels it:

1. Mellin denominators give only positive algebraic damping.
2. The dyadic zero is at total exponent zero, whereas an RH conjugate pair has
   total exponent one.
3. Affine completion cannot alter the quadratic Hessian.
4. Conjugation doubles the real diagonal instead of reversing its sign.

Therefore any nonnegative complete-block dissipation theorem must obtain a
genuine cancellation against off-diagonal zero pairs and/or the exact affine
and endpoint channels.  Total-frequency smoothing alone cannot provide such a
theorem.  This is a sign obstruction for this route, not a contradiction to RH
and not a proof that the full completed decrement is negative.
