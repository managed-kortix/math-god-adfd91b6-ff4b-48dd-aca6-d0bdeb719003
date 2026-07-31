# Cycle 176: simultaneous arbitrary-depth Laurent filtering

The Cycle 175 filter can be populated at all scales at once. The correct
object is a factorization of one terminal geometric series, rather than the
additive union of the sequential stage fields. Every factor may be assigned
to either of two silent shear families. Their complete quadratic convolution
then has only the terminal boundary quartet.

Fix `R,Y` nonzero, a depth `D>=1`, and even integers
`m_0,...,m_{D-1}>=2`. Set

\[
 R_0=R,\qquad R_{n+1}=m_nR_n,
\]

and define

\[
 A_r(z)=z^{-r}-z^r,
 \qquad
 H_n(z)=B_{m_n,R_n}(z)
 =\sum_{j=0}^{m_n-1}z^{(2j-m_n+1)R_n}.
\]

Repeated use of the Cycle 175 identity gives the exact all-depth formula

\[
 \boxed{A_{R_0}(z)\prod_{n=0}^{D-1}H_n(z)=A_{R_D}(z).}
 \tag{1}
\]

This is simultaneous: all factors in (1) are present in one field and no
stagewise replacement or amplitude renormalization is performed.

## Split-factor construction

Partition the scale indices as `I disjoint union J={0,...,D-1}`, with `J`
nonempty, and put

\[
 F_I(z)=A_{R_0}(z)\prod_{n\in I}H_n(z),
 \qquad
 G_J(z)=\prod_{n\in J}H_n(z).
 \tag{2}
\]

Thus `F_I G_J=A_{R_D}`. Alternating indices between `I` and `J` makes both
families genuinely contain factors from arbitrarily many separated scales.
Each `H_n` is reciprocal, so `F_I(z^{-1})=-F_I(z)` and
`G_J(z^{-1})=G_J(z)`. Write

\[
 F_I(z)=\sum_x f_xz^x,\qquad G_J(z)=\sum_s g_sz^s.
\]

Define one real Fourier field by

\[
 u_{(x,Y,0)}=f_xe_3,
 \qquad u_{(s,0,0)}=g_se_2,
 \qquad u_{-k}=u_k.
 \tag{3}
\]

Zero coefficients are omitted. There is no zero pump: mixed-radix
uniqueness, or the geometric-series product, shows that every exponent in a
nonempty product of the even-length `H_n` is a nonzero odd multiple of the
smallest selected scale. The field is divergence free. It is also real because
the reciprocity properties in (2) make (3) consistent under negation.

All interactions internal to either family vanish. Rail frequencies are
planar and rail polarizations are `e_3`, while pump frequencies are parallel to
`e_1` and pump polarizations are `e_2`. For a rail `k=(x,Y,0)` and pump
`ell=(s,0,0)`,

\[
 P_{k+\ell}\big((e_3\mathbin\cdot\ell)e_2
 +(e_2\mathbin\cdot k)e_3\big)=Ye_3.
\]

The complete ordered Euler/Navier--Stokes convolution on the `+Y` layer is
therefore

\[
 YF_I(z)G_J(z)e_3=Y(z^{-R_D}-z^{R_D})e_3.
\]

On the `-Y` layer both the rail sign and the symbol's factor `Y` reverse, so
the same coefficients result. Hence the complete nonlinearity has exactly
four nonzero modes:

\[
\begin{array}{c|c}
q&\widehat{(u\cdot\nabla u)}_q\text{ before the common Fourier scalar}\\
\hline
(-R_D,\phantom{-}Y,0)&\phantom{-}Ye_3\\
( R_D,\phantom{-}Y,0)&-Ye_3\\
(-R_D,-Y,0)&\phantom{-}Ye_3\\
( R_D,-Y,0)&-Ye_3.
\end{array}
\]

Every interior and cross-scale channel is included in the convolution and
cancels algebraically. The depth, multipliers, and nontrivial partition are
arbitrary.

## Why the construction is necessarily rank one

There is also a sharp obstruction to turning (1) into a genuinely
independent-variable telescoping filter within this two-shear scalar-product
ansatz. Let `K` be a field and suppose nonzero Laurent polynomials in any
number of variables satisfy

\[
 P(X)Q(X)=cX^a+dX^b,
 \qquad c,d\ne0,
 \tag{4}
\]

with `a!=b`. Newton polytopes obey

\[
 \operatorname{Newt}(PQ)=\operatorname{Newt}(P)+\operatorname{Newt}(Q).
\]

The right side of (4) has a line-segment Newton polytope. A Minkowski sum is a
segment only if both summands are points or segments parallel to it. Therefore
the support of each nonunit factor lies on an affine line parallel to `b-a`.
After removing monomial units, both factors are one-variable Laurent
polynomials in a common monomial (or in its primitive root when available).

Consequently a product with only two scalar outer boundaries cannot retain two
algebraically independent scale directions. The formal multiscale version of
(1) lives in the quotient

\[
 \mathbb Z[X_0^{\pm1},\ldots,X_D^{\pm1}]
 /(X_{n+1}-X_n^{m_n}),
\]

not in the free multivariate Laurent ring: the carry relations are exactly
what create the cancellations. The construction above attains arbitrary
simultaneous depth, while the Newton-polytope argument proves that its rank-one
collapse is unavoidable for any two-shear factorization with only two scalar
boundary monomials.

This closes the finite-depth-versus-simultaneous algebraic question for this
ansatz. It does not populate the intermediate rails as independent additive
modes, control critical energy or viscosity, produce an invariant Euler
subsystem, or give a Navier--Stokes solution or regularity result.

Run the exact full-convolution certificate with

```sh
python3 millennium-prize/navier-stokes/verify_cycle176_multiscale_filter.py
```
