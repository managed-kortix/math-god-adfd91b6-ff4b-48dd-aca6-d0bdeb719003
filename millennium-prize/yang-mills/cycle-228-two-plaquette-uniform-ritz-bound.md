# Cycle 228: a cutoff-uniform two-plaquette Ritz-gap bound

This bounded result concerns the dimensionless two-plaquette `SU(2)` Hamiltonian
from Cycle 226,

\[
 K_\lambda=T+\lambda(2-w_A-w_B),\qquad \lambda\geq0,
\]

on `L^2(SU(2)^2)^Ad`. It proves an exact lower bound for every natural finite
spin compression. It is not a volume-uniform lattice theorem and makes no
continuum claim.

## Representation-theoretic electric floor

In the normalized simultaneous-conjugation basis `Phi_(ab)^c`,

\[
 T\Phi_{ab}^c=[3C_a+3C_b+C_c]\Phi_{ab}^c,
 \qquad C_j=j(j+1),\qquad |a-b|\leq c\leq a+b.             \tag{228.1}
\]

Let `Omega=Phi_(00)^0` and `Q=I-|Omega><Omega|`. If exactly one of `a,b`
is nonzero, the triangle rule forces `c` to equal that spin, and (228.1) is
`4C_a>=3` or `4C_b>=3`. If both are nonzero, then
`3C_a+3C_b>=9/2`, independently of `c`. Hence

\[
                         T\geq 3Q.                         \tag{228.2}
\]

The bound is sharp on `Phi_(1/2,0)^(1/2)` and
`Phi_(0,1/2)^(1/2)`. In particular, the shared `c` sectors cannot form an
electric-energy sequence approaching zero: `C_c` has a positive sign, while
the only way to set `c=0` away from the vacuum has `a=b>0` and electric energy
at least `9/2`.

For a half-integer `J>=1/2`, let `P_J` project onto all `Phi_(ab)^c` with
`a,b<=J`, and put `K_(lambda,J)=P_J K_lambda P_J`. Since `w_A,w_B` are
multiplication by numbers in `[-1,1]`,

\[
                 \lambda(2-w_A-w_B)\geq0.                 \tag{228.3}
\]

Compression preserves (228.2)--(228.3). The min--max principle therefore
gives, with eigenvalues in increasing order,

\[
                         E_{1,J}\geq3.                     \tag{228.4}
\]

This is uniform in `J`; it uses the simultaneous-conjugation triangle rule
rather than a tensor-product reduction.

## Exact comparison and Schur lemma

Set

\[
 u={1\over\sqrt2}\left(\Phi_{1/2,0}^{1/2}
                  +\Phi_{0,1/2}^{1/2}\right).
\]

The exact fundamental-character rule gives the following compression to
`span{Omega,u}`:

\[
 \begin{pmatrix}
  2\lambda&-\lambda/\sqrt2\\
  -\lambda/\sqrt2&3+2\lambda
 \end{pmatrix}.                                           \tag{228.5}
\]

Thus Rayleigh--Ritz gives, for every `J>=1/2`,

\[
 E_{0,J}\leq U_\lambda
 :=2\lambda+{3-\sqrt{9+2\lambda^2}\over2}.                \tag{228.6}
\]

There is also a direct Schur formulation. Relative to `Omega direct-sum Q`,
write the off-diagonal column as `b=QK_(lambda,J)Omega`. The character rule
gives `||b||^2=lambda^2/2`. For every real `x<3`,

\[
 Q(K_{\lambda,J}-x)Q\geq(3-x)Q,
\]

so this block is positive and the inertia below `3` is controlled by the
one-dimensional Schur complement

\[
 F_J(x)=2\lambda-x-
 \langle b,[Q(K_{\lambda,J}-x)Q]^{-1}b\rangle,             \tag{228.7}
\]

with the exact comparison

\[
 2\lambda-x-{\lambda^2\over2(3-x)}\leq F_J(x)
 \leq2\lambda-x.                                         \tag{228.8}
\]

Consequently there is at most one Ritz eigenvalue below `3`. Equations
(228.4) and (228.6) now prove the cutoff-uniform gap estimate

\[
 \boxed{\quad
 E_{1,J}-E_{0,J}\geq
 L_\lambda:={3+\sqrt{9+2\lambda^2}\over2}-2\lambda
 \quad}                                                   \tag{228.9}
\]

for every natural cutoff `J>=1/2`. The right side is positive exactly for
`0<=lambda<12/7`. In particular,

\[
 E_{1,J}-E_{0,J}\geq {\sqrt{11}-1\over2}>1
 \qquad(\lambda=1,\ J\geq1/2).                            \tag{228.10}
\]

Thus at the Cycle 226 benchmark coupling, shared `c` sectors do not create
arbitrarily low Ritz gaps as the spin cutoff grows. The argument does not
assert monotonicity of Ritz gaps, identify the untruncated gap, or remain
coercive through a continuum scaling in which `lambda` leaves the interval
`[0,12/7)`.

## Trust boundary

As in Cycle 226, (228.1) and the fundamental-character matrix element in
(228.5) are representation-theoretic inputs. Everything after those inputs is
an exact operator inequality, min--max argument, or one-dimensional Schur
comparison; no floating-point calculation is used.
