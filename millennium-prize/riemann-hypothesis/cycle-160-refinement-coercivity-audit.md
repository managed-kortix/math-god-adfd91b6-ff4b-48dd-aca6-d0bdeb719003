# Cycle 160: Weil-spline refinement coercivity audit

The proposed finite refinement gate was

\[
W_{h,L}\succeq0,
\qquad
\lambda_{\min}(W_{h/2,L+1})
 \ge c\lambda_{\min}(W_{h,L})
\]

for one explicit `c>0`.  This is not an intrinsic gate.  If the basis at the
fine level is multiplied by a nonzero scalar `d`, its matrix is multiplied by
`d^2`; positivity is unchanged but the displayed eigenvalue ratio is multiplied
by `d^2`.  Moreover, after two positive finite eigenvalues have been computed,
some positive `c` always exists.  The second condition therefore adds no
mathematical content to finite positivity.

## Intrinsic formulation

Fix a Hilbert norm `||.||_X` on the test-function space.  For a spline basis at
level `j`, let

\[
(H_j)_{kl}=\mathcal W(\phi_{j,k},\phi_{j,l}),
\qquad
(M_j)_{kl}=\langle\phi_{j,k},\phi_{j,l}\rangle_X.
\]

The basis-independent finite coercivity constant is

\[
\alpha_j=\lambda_{\min}(H_j,M_j)
=\inf_{0\ne f\in V_j}{\mathcal W(f,f)\over\|f\|_X^2}.
\]

For nested spaces `V_j subset V_(j+1)` and exact prolongation `P_j`, consistent
assembly requires

\[
H_j=P_j^*H_{j+1}P_j,
\qquad
M_j=P_j^*M_{j+1}P_j.
\]

The variational principle then gives the exact monotonicity

\[
\boxed{\alpha_{j+1}\le\alpha_j.}
\]

Thus refinement cannot manufacture a larger intrinsic lower bound.  A useful
coercive result would require a uniform estimate `inf_j alpha_j>0` together
with continuity and density in a specified form domain.  Positivity on one or
finitely many levels cannot imply that estimate.

Equivalently, for innovation coordinates `Z` and `T=[P_j Z]`, a candidate
constant `alpha` must be tested through the generalized Schur complement of

\[
T^*(H_{j+1}-\alpha M_{j+1})T.
\]

This is exactly the original positivity/coercivity problem restricted to the
larger space, rather than a new source of sign.

## Numerical calibration

The earlier mesh-`1/2`, support-`[-1,1]` three-hat computation was reproduced.
Its ordinary eigenvalues are approximately

\[
1.7775257488\,10^{-4},\quad
8.2753029113\,10^{-4},\quad
1.1796813877\,10^{-3}.
\]

For the expanded mesh-`1/4`, support-`[-2,2]` fifteen-hat space, direct
high-precision evaluation of the same completed-form normalization found a
positive matrix with ordinary minimum eigenvalue approximately

\[
4.6950826883\,10^{-7}.
\]

The raw ratio is about `0.00264136`, but it is basis dependent and is recorded
only as a regression calibration.  The computation is not an outward-rounded
certificate.  It cannot support a positivity theorem, and the dramatic margin
loss is not by itself an asymptotic theorem.

The prime-power, pole, and archimedean channels are individually much larger
and sign-indefinite; positivity in these finite examples comes from global
cancellation.  In particular, the one-hat prime-local packet is already
strictly negative, consistently with the exact Cycle 85 operator audit.

## Decision

The raw refinement-eigenvalue gate is retired because it is basis dependent and
finite-level positivity is only a restatement of a finite restriction of the
Weil criterion.  Future spline work must specify a fixed norm, exact Galerkin
compatibility, rigorous interval assembly, and a uniform theorem over all
levels.  No such theorem is obtained here.

No Riemann-hypothesis result is claimed.
