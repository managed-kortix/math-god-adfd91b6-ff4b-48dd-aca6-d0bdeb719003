# Cycle 181: a finite-cutoff gauge-invariant `SU(2)` plaquette block

This bounded scout instantiates the smallest lattice cell carrying a magnetic
interaction: one oriented square, with four links and four vertices.  It gives
a finite-cutoff atomic criterion and a reproducible finite-matrix benchmark.
It is a finite-volume toy model and does not address the continuum, uniform
volume, or four-dimensional existence quantifiers in the Clay statement.

## Gauss reduction

Let the link variables be `U_1,...,U_4 in SU(2)` and let

\[
 U_p=U_1U_2U_3^{-1}U_4^{-1}.
\]

Gauge transformations act at the four vertices.  Gauge fixing three tree links
leaves `U_p`, with residual conjugation at the root.  Haar integration (or the
unitary tree-gauge map) therefore identifies the physical Hilbert space with

\[
 \mathrm{L}^2(SU(2)^4)^{SU(2)^4}
 \simeq \mathrm{L}^2(SU(2))^{\rm Ad}.
\tag{181.1}
\]

The irreducible characters `chi_j`, `j=0,1/2,1,...`, are an orthonormal basis
of this class space.  Each of the four link Laplacians acts on `chi_j(U_p)` by
the same Casimir `j(j+1)`.  With the normalization of Cycle 178,

\[
 C\chi_j=4j(j+1)\chi_j.
\tag{181.2}
\]

Put `w=chi_(1/2)/2` and use the nonnegative Wilson potential `W=1-w`.  For this
note, `lambda` is an arbitrary nonnegative dimensionless parameter and

\[
 K_\lambda=C+\lambda W,
 \qquad \lambda\geq0.
\tag{181.3}
\]

The optional identification `lambda=2/g^4` and
`H=(g^2/(2a))K_lambda` applies only after adopting the particular
Kogut--Susskind normalization used in Cycle 178; it is not part of the
finite-matrix certificate.  The character product rule

\[
 \chi_{1/2}\chi_j=\chi_{j+1/2}+\chi_{j-1/2},\qquad\chi_{-1/2}=0,
\]

gives the character-basis Jacobi recurrence

\[
 K_\lambda\chi_j=
 [4j(j+1)+\lambda]\chi_j
 -{\lambda\over2}(\chi_{j+1/2}+\chi_{j-1/2}).
\tag{181.4}
\]

Equation (181.4) records the character-basis recurrence.  No claim about the
spectrum, ground state, heat kernel, or gap of its half-line closure is used or
certified below.

## Finite atomic synthesis

Index `e_n=chi_(n/2)`, `n>=0`, and let `P_N` project onto
`V_N=span(e_0,...,e_N)`.  In this orthonormal atomic synthesis, the exact Ritz
matrix is

\[
 (J_N)_{nn}=n(n+2)+\lambda,
 \qquad (J_N)_{n,n+1}=(J_N)_{n+1,n}=-\lambda/2.
\tag{181.5}
\]

This is the finite principal matrix `J_N` of dimension `N+1`.  The omitted
boundary channel is `-(lambda/2)e_(N+1)<e_N,cdot>`, but its presence does not
turn a certificate for `J_N` into an enclosure for any half-line eigenvalue.
No cutoff convergence rate or infinite-operator error bar is claimed.

Let `Omega_N=sum_(n=0)^N a_n e_n` be a normalized lowest eigenvector of `J_N`
and put `xi_(n,N)=e_n-a_n Omega_N`.  For `I subset {0,...,N}`, the finite
centered atoms have Gram matrix

\[
 G_{N,I}=(\langle\xi_{m,N},\xi_{n,N}\rangle)_{m,n\in I}
     =I-a_Ia_I^*,
\tag{181.6}
\]

and temporal matrix

\[
 M_{N,I}(t)=(\langle\xi_{m,N},e^{-t(J_N-E_{0,N})}\xi_{n,N}\rangle)_{m,n\in I}.
\tag{181.7}
\]

For `f=sum_(n in I)c_n xi_(n,N)`, its finite-matrix variance-normalized temporal
quotient is

\[
 {c^*M_{N,I}(t)c\over c^*G_{N,I}c}.
\tag{181.8}
\]

Hence the finite atomic criterion is the generalized matrix inequality

\[
 M_{N,I}(t)\preceq q_{N,I}(t)G_{N,I},
\qquad
 q_{N,I}(t)=\sup_{c^*G_{N,I}c>0}
 {c^*M_{N,I}(t)c\over c^*G_{N,I}c}.
\tag{181.9}
\]

It tests every coherent linear combination of the chosen finite-cutoff atoms,
unlike generatorwise diagonal correlators.  It is a statement about `J_N` only.
Passing either this criterion or its gap to the half-line problem requires a
separate tail theorem, which is not supplied here.

## Computable gap benchmark

The script `verify_cycle181_one_plaquette_gap.py` forms `J_N` over
`fractions.Fraction` and bisects its exact Sturm count.  Its output consists of
closed rational intervals for `E_0(J_N)`, `E_1(J_N)`, and their difference;
the displayed cutoff `N` is part of every run.  There are no floating-point
eigenvalue, exponential, or cutoff-drift claims.  For example:

```
python3 millennium-prize/yang-mills/verify_cycle181_one_plaquette_gap.py \
  --cutoff 32 --couplings 0 1/10 1 --tolerance 1/1000000000000
python3 -O millennium-prize/yang-mills/test_cycle181_one_plaquette_gap.py
```

The certificates concern only the named finite matrices.  They provide no
volume-uniform lower bound, no half-line spectral enclosure, and no
Osterwalder--Schrader continuum construction.
