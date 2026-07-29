# Cycle 109: RM certification and exact contraction rank

The quartic-CM scout now has a dependency-free exact verifier for its
cohomological half.  In an exterior basis of `H^1`, with RM eigenvalues
\[
 (\lambda,\lambda,\lambda^{-1},\lambda^{-1}),
\]
the coefficients of `g^*Theta` and `(g^-1)^*Theta` are respectively
`lambda_i^2` and `lambda_i^-2`; the controlling ratios are `lambda_i^4`.
The script constructs the full `28`-column Chern-contraction matrix from
\[
 \operatorname{ch}(F_2)=g^*\Theta-rac16(g^{-1})^*\Theta^3
\]
using exact rational exterior algebra.  It certifies
\[
 \operatorname{rank}C=20,\qquad\dim\ker C=8
\]
for multiplicities `(2,2)`, and `24/4` for four distinct eigenvalues.

Representation-theoretically, the eight-dimensional kernel is
\[
 \mathfrak{sl}(U_\sigma)\oplus\mathfrak{sl}(U_\tau)
 \oplus L_\sigma\oplus L_\tau,
\]
of dimensions `3+3+1+1`.  Equivariance does not force its Atiyah obstruction
to vanish because the Ext target may contain all these isotypic components.

The explicit HPS curve remains uncertified as an RM Jacobian.  Matching local
factors through a numerical range is insufficient.  A rigorous rational
isogeny certificate could use a tailored Faltings--Serre witness set after an
exact residual representation and RM action are available; it would still not
prove integral unit action or principal-polarization compatibility.  The
cleanest direct certificate is an algebraic correspondence `Y` on `C x C`
whose exact tangent action `M` satisfies
\[
 M^2-3M+I=0,
 \quad\chi_M(T)=(T^2-3T+1)^2,
 \quad M^\dagger=M.
\]
Such a correspondence could in principle be reconstructed by certified period
and Puiseux methods, but none was produced.

The scout remains frozen behind three independent gates: exact RM
correspondence, explicit secant/gluing resolution, and Atiyah obstruction rank
`20`.  No Hodge result is claimed.
