# Cycle 228: an untruncated two-plaquette gap bound

This bounded result concerns the full dimensionless two-plaquette `SU(2)`
Hamiltonian from Cycle 226,

\[
 K_\lambda=T+\lambda(2-w_A-w_B),\qquad \lambda\geq0,
\]

on `L^2(SU(2)^2)^Ad`. It proves an exact lower bound for the untruncated
operator, as well as every natural finite spin compression. It is not a
volume-uniform lattice theorem and makes no continuum claim.

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

Vacuum coupling does not invalidate this conclusion. For every
two-dimensional subspace `S`, there is a nonzero `psi in S cap Omega^perp`,
and (228.2)--(228.3) give

\[
 {\langle\psi,K_\lambda\psi\rangle\over\|\psi\|^2}\geq3. \tag{228.4a}
\]

Thus the maximum Rayleigh quotient on `S` is at least `3`, exactly as required
by the second min--max level. The argument never asserts that `Q` reduces
`K_lambda`.

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

## Passage to the full operator

Write a vector in the coupled basis as

\[
 \psi=\sum_{a,b,c}\psi_{ab}^c\Phi_{ab}^c,
 \qquad \tau_{ab}^c=3C_a+3C_b+C_c.
\]

The closed electric form is

\[
 t[\psi]=\sum_{a,b,c}\tau_{ab}^c|\psi_{ab}^c|^2,
 \qquad
 D(t)=\left\{\psi:\sum_{a,b,c}\tau_{ab}^c|\psi_{ab}^c|^2<\infty\right\}.
                                                               \tag{228.11}
\]

Only finitely many admissible triples have `tau_(ab)^c<=R`: already
`3C_a+3C_b<=R`. Hence `T` has compact resolvent. The magnetic multiplication
operator `V_lambda=lambda(2-w_A-w_B)` is bounded, self-adjoint, and
nonnegative, so the form sum `K_lambda=T+V_lambda` is self-adjoint,
semibounded, and also has compact resolvent.

The ranges of the nested projections `P_J` exhaust the coupled basis. For
every `psi in D(t)`, coefficient truncation gives

\[
 \|(I-P_J)\psi\|^2+t[(I-P_J)\psi]\longrightarrow0.          \tag{228.12}
\]

Thus their union is a form core for `T`. Since `V_lambda` is bounded, the
`T`-form norm and the `K_lambda`-form norm are equivalent, so the same union is
a form core for `K_lambda`. The conforming Rayleigh--Ritz/min--max theorem then
gives, for every fixed eigenvalue index `n`,

\[
 E_{n,J}\downarrow E_n(K_\lambda).                          \tag{228.13}
\]

Passing (228.4) to the limit gives `E_1(K_lambda)>=3`, while the fixed trial
space in (228.5), which lies in every `P_J` for `J>=1/2`, gives directly
`E_0(K_lambda)<=U_lambda`. Therefore

\[
 \boxed{\quad E_1(K_\lambda)-E_0(K_\lambda)\geq
 {3+\sqrt{9+2\lambda^2}\over2}-2\lambda\quad}              \tag{228.14}
\]

for `0<=lambda<12/7`. At the benchmark coupling,

\[
 \boxed{\quad \operatorname{gap}(K_1)\geq
 {\sqrt{11}-1\over2}=1.158312395\ldots>1.\quad}             \tag{228.15}
\]

In particular `E_0(K_1)<3<=E_1(K_1)`, so compact resolvent and the min--max
count also show that the ground eigenvalue is simple. Equivalently, the
one-dimensional Schur complement permits at most one eigenvalue below `3`;
the vacuum/first-shell trial guarantees that one exists.

Thus at the Cycle 226 benchmark coupling, shared `c` sectors do not create a
low untruncated gap. This conclusion concerns only the fixed two-plaquette
operator. It does not provide a volume-uniform estimate or remain coercive
through a continuum scaling in which `lambda` leaves `[0,12/7)`.

## Trust boundary

As in Cycle 226, (228.1) and the fundamental-character matrix element in
(228.5) are representation-theoretic inputs. Everything after those inputs is
an exact operator inequality, closed-form argument, min--max argument, or
one-dimensional Schur comparison; no floating-point calculation is used. In
particular, there is no flaw in the `E_1>=3` argument: its decisive content is
the codimension-one inequality `K_lambda>=3Q`, not invariance of
`Omega^perp` under `K_lambda`.
