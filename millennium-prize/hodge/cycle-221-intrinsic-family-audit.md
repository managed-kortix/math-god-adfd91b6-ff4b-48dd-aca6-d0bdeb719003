# Cycle 221: intrinsic-family audit of the frozen Chow secant

## Verdict

Cycle 218 is finite only in the scheme-theoretic existence sense.  Once an
embedding of `A_0`, equations for the three Chow schemes, and affine charts are
actually supplied, (218.4) is a finite polynomial list.  The frozen data do not
supply any of those objects.  At degree

\[
D=8387930766330029152
\]

this omission is the whole computation, not a routine preprocessing step.
The note therefore does not define an instantiable elimination problem.

There is a useful intrinsic replacement for the secant condition, but it does
not turn the unrestricted Cycle 218 search into a manageable one.  It gives a
compact verification language for a separately supplied family over
`P^1`.  A manageable search still requires a bounded sparse support ansatz.

## The intrinsic degree-one condition

Let `H` be the very ample line bundle used to embed `A_0`, and let

\[
\pi:{\cal X}\longrightarrow {\mathbb P}^1,
\qquad q:{\cal X}\longrightarrow A_0
\]

be a flat family of pure three-dimensional subschemes.  Write `X_t` for its
fundamental cycle.  The induced map

\[
c_{\cal X}:{\mathbb P}^1\longrightarrow
\operatorname {Chow}_{3,D_H}(A_0)
\]

has pullback of the Chow-form hyperplane bundle

\[
c_{\cal X}^*O_{\rm Chow}(1)
 \simeq \langle q^*H,q^*H,q^*H,q^*H\rangle_{{\cal X}/{\mathbb P}^1}.       \tag{221.1}
\]

Consequently

\[
\boxed{\deg c_{\cal X}^*O_{\rm Chow}(1)
      =\int_{[\cal X]}c_1(q^*H)^4.}                                  \tag{221.2}
\]

Thus the exact intrinsic replacement for "the Chow map has degree one" is

\[
\boxed{\int_{[\cal X]}c_1(q^*H)^4=1.}                                \tag{221.3}
\]

Together with

\[
[X_0]=Y^++C_0^-,\qquad [X_\infty]=Y^-+C_0^+,                         \tag{221.4}
\]

flatness gives the same one-step rational equivalence and hence the same
cancellation formula as (218.6).  Equations (221.1)--(221.3) are not a
relaxation to connectedness or algebraic equivalence.  They characterize the
degree of the actual Hilbert-to-Chow map made by the family.

The degree can be checked without Chow equations.  On `P^1`, the Deligne
pairing in (221.1) can be computed from determinant-of-cohomology lines.  It is
also `4!` times the coefficient of `n^4` in the total-space Hilbert polynomial

\[
\chi\bigl({\cal X},q^*H^{\otimes n}\otimes
                    \pi^*O_{{\mathbb P}^1}(k)\bigr).                 \tag{221.5}
\]

The `n^3k` coefficient separately records the common degree of the fibers.
For a proposed family given by a short resolution or sparse equations, both
are exact and usually small integer calculations.

## Explicit Hilbert-chart equations

Fix one Hilbert polynomial `P_X(n)` with leading term

\[
P_X(n)=\frac{D_H}{3!}n^3+O(n^2).                                    \tag{221.6}
\]

After choosing a Gotzmann degree `m`, a family can be represented by quotient
spaces

\[
S_m\otimes O_{{\mathbb P}^1}\twoheadrightarrow Q_m,
\qquad \operatorname {rank}Q_m=P_X(m),                              \tag{221.7}
\]

and the corresponding quotients in the finitely many degrees needed for the
Gotzmann test.  On standard Grassmann charts the equations are:

1. the fixed homogeneous equations of `A_0` act by zero;
2. multiplication by homogeneous coordinates commutes;
3. the degree-`m+1` quotient is generated from degree `m`;
4. the prescribed minors have ranks `P_X(m+j)`;
5. specialization at `0` and `infinity` equals fixed endpoint Hilbert points,
   whose fundamental cycles satisfy (221.4);
6. the determinant-of-cohomology integer in (221.2) is one.

These are explicit finite polynomial and nonvanishing equations once `P_X`,
`m`, and endpoint scheme structures are fixed.  They avoid equations for the
ambient Chow variety altogether.  The tangent and second-jet tests should then
be taken on this relative Hilbert incidence; their Jacobians come directly
from the universal quotient equations.  This tests the chosen scheme-family
architecture, not every tangent direction of the coarser singular Chow space.

## Why this is not yet a manageable Cycle 218 system

Three independent gaps prevent (221.7) from being an equivalent small
elimination problem for the frozen candidate.

First, Cycle 218 fixes only fundamental cycles.  The terms `C_0^+` and
`C_0^-` contain enormous multiplicities of the seven graphs.  A Hilbert point
requires choices of thickenings or other scheme structures realizing those
multiplicities.  Those choices change all lower coefficients of `P_X`; there is
no canonical endpoint Hilbert polynomial.

Second, fixing the leading coefficient `D_H` does not fix a Hilbert polynomial.
Allowing all embedded structures gives a countable union of Hilbert schemes,
not one finite-type scheme.  Fixing one polynomial is a new bounded
architecture, just as in the Ferrand-double campaign, and can discard Chow
families that do not admit that flat scheme realization.

Third, the ranks in (221.7), the Gotzmann bound, and the number of Pluecker
coordinates grow with the enormous degree.  The Hilbert construction proves
effectivity in principle; it does not make the unrestricted parameter space
computationally small.  Small equations arise only after imposing a sparse
resolution, determinantal, liaison, or similar support model.  Such a model is
a new ansatz and is not equivalent to the full integral non-graph Chow open.

## Embedding normalization defect

The phrase "degree one in a Chow variety" is meaningless until the embedding
of `A_0` and its Chow-form hyperplane line are specified.  The numerical
`graph_degrees` in the Cycle 218 JSON are normalized polarization Euler
characteristics: for an abelian threefold `G`,

\[
\chi(P|_G)=\frac{c_1(P|_G)^3}{3!}.
\]

They are not automatically projective degrees.  Moreover the polarization of
type `(1,1,1,1,1,3)` is not itself a projective embedding.  If the actual
embedding uses `H=P^{\otimes r}`, then

\[
D_H=3!r^3D,
\qquad
\deg c_{\cal X}^*O_{\rm Chow}(1)
 =r^4\int_{[\cal X]}c_1(P)^4.                                      \tag{221.8}
\]

For `r>1`, the right side is divisible by `r^4`; literal Chow degree one is
therefore impossible.  Choosing an unrelated very ample `H` changes both the
cycle degrees and the degree-one condition.  Cycle 218's unspecified "fixed
Chow-form embeddings" cannot simultaneously justify its displayed degree
indices and its line condition.

## Decision

Do not launch the Cycle 218 elimination.  In its current normalization it is
not merely too large: the projective degree and degree-one condition are not
defined compatibly, and under the natural embedding by a very ample multiple
of `P` the degree-one locus is empty by (221.8).

Retain (221.1)--(221.5) as the production interface.  A successor candidate
must freeze:

1. an actual very ample `H`;
2. one endpoint scheme structure and Hilbert polynomial;
3. a sparse finite presentation of a flat family over `P^1`;
4. the exact endpoint fundamental cycles;
5. the intrinsic intersection certificate (221.3), with whatever degree is
   arithmetically possible for `H`.

This replacement makes verification manageable when the family presentation
is manageable.  It does not provide a manageable exhaustive representation of
all Cycle 218 Chow points, and no such representation follows from the frozen
data.
