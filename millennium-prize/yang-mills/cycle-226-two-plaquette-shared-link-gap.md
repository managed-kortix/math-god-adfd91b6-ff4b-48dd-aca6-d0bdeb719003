# Cycle 226: shared-link obstruction in natural spin-cutoff compressions

This bounded scout treats two `SU(2)` squares sharing one edge.  It identifies
the structural gauge-reduced space and compares natural spin-cutoff
compressions in the smallest cutoff that sees the shared-link intertwiner.  The
computed numbers are Ritz gaps of finite matrices.  They are not untruncated
spectral gaps and do not prove a gap-tensorization inequality, a
volume-uniform bound, or a continuum mass gap.

## Exact Gauss reduction

The two-square graph has seven links, six vertices, and cycle rank two.  Fix a
maximal tree.  The two remaining holonomies are `A,B in SU(2)`, and the gauge
transformation at the root acts by simultaneous conjugation.  Thus

\[
 {\cal H}_{\rm phys}=L^2(SU(2)^2)^{\rm Ad},\qquad
 f(A,B)=f(gAg^{-1},gBg^{-1}).                              \tag{226.1}
\]

This is not the tensor product of the two one-plaquette class spaces: separate
conjugation of `A` and `B` has been replaced by simultaneous conjugation.

Let `Phi_(ab)^c` be the normalized spin-network basis obtained by coupling the
left and right Peter--Weyl spins `a,b` through the unique `SU(2)` intertwiner of
spin `c`, where `|a-b|<=c<=a+b`.  Three exclusive links of each square give
`3C_a+3C_b`.  The shared edge carries the coupled generator and gives `C_c`.
Consequently the exact reduced electric operator is

\[
 T\Phi_{ab}^c=
 [3a(a+1)+3b(b+1)+c(c+1)]\Phi_{ab}^c.                     \tag{226.2}
\]

With `w_A=chi_(1/2)(A)/2`, `w_B=chi_(1/2)(B)/2`, the dimensionless
two-plaquette Hamiltonian is

\[
 K^{(2)}_\lambda=T+\lambda(2-w_A-w_B),\qquad\lambda\geq0. \tag{226.3}
\]

The decisive point is structural: the residual action is one simultaneous
conjugation, not two independent conjugations.  Accordingly the physical basis
has a shared `c` sector, and the electric energy contains `C_c`.  Neither
feature exists in the tensor product of two one-plaquette class spaces.
Multiplication by `w_A` or `w_B` changes the corresponding spin by `1/2`; its
matrix elements in the `Phi_(ab)^c` basis are the standard normalized
recoupling coefficients.

### Representation-theory trust boundary

The verifier does not derive (226.1)--(226.5) from Haar integration or from
Clebsch--Gordan tables.  It takes the displayed representation-theoretic
reduction and matrix entries as trusted input, then certifies their
characteristic polynomial, Sturm counts, and rational spectral enclosures.
Thus the algebraic spectral certificate is exact conditional on the stated
normalization and recoupling derivation.  An independent end-to-end certificate
would still need to generate the basis and matrix elements directly from
explicit `SU(2)` representation data.

## Smallest natural compression

Project to `a,b<=1/2`.  In the ordered orthonormal basis

\[
 |00;0\rangle,\ |\tfrac12,0;\tfrac12\rangle,
 |0,\tfrac12;\tfrac12\rangle,
 |\tfrac12,\tfrac12;0\rangle,
 |\tfrac12,\tfrac12;1\rangle,                              \tag{226.4}
\]

Compressing the operator to this natural spin cutoff gives the Ritz matrix

\[
 \begin{pmatrix}
 2\lambda&-\lambda/2&-\lambda/2&0&0\\
 -\lambda/2&3+2\lambda&0&-\lambda/4&-\sqrt3\lambda/4\\
 -\lambda/2&0&3+2\lambda&-\lambda/4&-\sqrt3\lambda/4\\
 0&-\lambda/4&-\lambda/4&9/2+2\lambda&0\\
 0&-\sqrt3\lambda/4&-\sqrt3\lambda/4&0&13/2+2\lambda
 \end{pmatrix}.                                           \tag{226.5}
\]

The exchange-antisymmetric vector has eigenvalue `3+2lambda`.  The remaining
four eigenvalues are the roots of a rational quartic.  At `lambda=1`, its
characteristic polynomial is

\[
 (x-5)\,[8x^4-176x^3+1354x^2-4198x+4143]/8.              \tag{226.6}
\]

Exact rational Sturm bisection for this matrix gives

\[
 E_0=1.837624330900\ldots,\quad
 E_1=4.979135845618\ldots,\quad
 \Delta_{\rm shared}^{(1/2)}=3.141511514718\ldots.        \tag{226.7}
\]

For comparison, truncate each one-plaquette Jacobi operator to spins
`0,1/2`.  Its matrix is

\[
 \begin{pmatrix}\lambda&-\lambda/2\\-\lambda/2&3+\lambda\end{pmatrix},
\]

so the gap of that two-state tensor-sum compression is exactly

\[
 \Delta_{\rm tensor}^{(1/2)}=\sqrt{9+\lambda^2};\qquad
 \Delta_{\rm tensor}^{(1/2)}|_{\lambda=1}=\sqrt{10}
 =3.162277660168\ldots.                                   \tag{226.8}
\]

Here `sqrt(10)` is only the cutoff comparator.  It is not the full
one-plaquette gap: the independently certified half-line one-plaquette gap at
`lambda=1` is approximately `3.11386381151`.  Consequently the disjoint
rational enclosures establish only that these two natural cutoff matrices have
different Ritz gaps.  Ritz gaps need not bound full gaps monotonically, so the
comparison gives no ordering between untruncated spectra and no claim that
adding a plaquette lowers a physical gap.

The robust obstruction is instead already present before diagonalization:
simultaneous conjugation produces the extra `c` sectors and the coupled
electric Casimir.  Therefore the shared-link compression is not the tensor sum
of the corresponding one-plaquette compressions.  The numerical Ritz-gap
separation is a finite-dimensional witness of that structural mismatch, not a
theorem of untruncated gap tensorization or its failure.

Reproduce the certificate with

```
python3 millennium-prize/yang-mills/verify_cycle226_two_plaquette_gap.py \
  --coupling 1 --tolerance 1/10000000000
python3 -O millennium-prize/yang-mills/test_cycle226_two_plaquette_gap.py
```
