# Cycle 226: coefficient-variety finite-mode rigidity

## Result and correction to the Cycle 224 loophole

Work on the normalized-Haar `2 pi` torus, remove the spatial mean by a
Galilean transformation, and write

\[
 \omega(x,t)=\sum_{k\ne0}z_k(t)e^{ik\cdot x},\qquad
 z_{-k}=\overline{z_k}.
\]

The full two-dimensional Euler vector field is

\[
 F_r(z)=\sum_{p+q=r}{p\wedge q\over2}
 \left({1\over |q|^2}-{1\over |p|^2}\right)z_pz_q.       \tag{226.1}
\]

Cycle 224 left open the possibility that a fixed finite support might be
invariant only on a special coefficient-dependent algebraic variety. For real
Euler fields that loophole is closed by Theorem 5.1 of
Elgindi--Hu--Sverak, *On 2d Incompressible Euler Equations with Partial
Damping*, Commun. Math. Phys. 355 (2017), 145--159,
doi:`10.1007/s00220-017-2877-y`:

> If a 2D Euler solution on the torus is supported in one fixed finite set of
> Fourier modes on a time interval, then, after removing the constant velocity
> mode, it is independent of time, and its nonzero support is contained in a
> line through the origin or in one circle centered at the origin.

The displayed theorem is in the paper's real-valued setting. Its proof says
that "the statement remains true for complex solutions," but the printed
combinatorial argument then uses the symmetry `k -> -k` supplied by reality
and gives no replacement complex argument. Thus the real conclusion is proved;
the fully complex conclusion below relies on an explicit author assertion.
Reality imposes the conjugation equations `z_-k=conj(z_k)`.

Consequently there is no smallest nonstationary exact real solution confined
to one finite set beyond one line or circle: there is none at any finite
cardinality. Galerkin triads and coefficient cancellation loci can be
nonstationary only because the discarded exterior equations of (226.1) are not
all satisfied.

## Exact algebraic formulation

Fix a finite symmetric set `S` of nonzero frequencies and let
`A_S=C^S` be its complex coefficient space. For `r in S+S`, let `F_r` be the
quadratic polynomial (226.1), with `z_k=0` for `k notin S`. Define

\[
 I_{\rm out}(S)=(F_r:r\in(S+S)\setminus S),\qquad
 I_{\rm eq}(S)=(F_r:r\in S+S).                           \tag{226.2}
\]

Let `X` be any reduced algebraic subvariety of `A_S`. The exact conditions for
`X` to carry full-Euler trajectories without leaving `S` are

\[
 I_{\rm out}(S)\subset I(X),\qquad
 D_F I(X)\subset I(X),                                   \tag{226.3}
\]

where

\[
 D_F=\sum_{k\in S}F_k{\partial\over\partial z_k}.
\]

The first condition kills every exterior mode, while the second makes the
internal quadratic vector field tangent to `X`. These conditions allow all
coefficient-dependent cancellations, reducible varieties, singularities, and
support drops.

### Theorem (coefficient-variety no-go)

For a reduced real algebraic invariant set in the Fourier-real coefficient
space, the analogue of (226.3) implies containment in the equilibrium set. The
same conclusion for an arbitrary complex subvariety `X subset C^S` is
conditional on the complex extension asserted in the cited paper:

\[
 X\subset V(I_{\rm eq}(S)).                              \tag{226.4}
\]

Equivalently, the restriction of the Euler vector field to the relevant set is
zero. Over the real coefficient space, this says
`F_k in sqrt[R]{I(X)}` for every `k in S`; over the complex numbers, subject to
the caveat above, `F_k in I(X)` because `X` is reduced.

### Proof

Take any point `a in X` (a Fourier-real point for the unconditional real
version). Polynomial ODE existence gives the local
integral curve `z(t)` of the internal field through `a`. The tangency condition
keeps `z(t)` in `X`; the exterior equations then vanish along the curve.
Extending by zero outside `S` therefore gives an exact full-Euler solution with
support in the one fixed finite set `S`. The real finite-mode rigidity theorem,
or its asserted complex extension, makes this solution
stationary, so `F_k(a)=0` for every `k in S`. The exterior components already
vanish by (226.3), hence `a in V(I_eq(S))`. This holds for every point of `X`,
which proves (226.4); the ideal statements follow from the complex and real
Nullstellensatze. No generic-coefficient or universal-support assumption is
used. `square`

The argument also shows that allowing a constructible set, an analytic
submanifold, or a single exceptional coefficient orbit inside one fixed finite
support does not help (unconditionally for real fields, and subject to the same
caveat for complex fields). It does not address a merely pointwise-finite
solution whose union of supports over time is unbounded.

## Equilibrium variety exactly

Call `T subset S` degenerate when either all points of `T` are collinear with
the origin or all have one common Euclidean length. Let

\[
 L_T=\{z\in A_S:z_k=0\text{ for }k\notin T\}.
\]

For a finite `S`, let `M(S)` be the finite collection of inclusion-maximal
degenerate subsets. On the Fourier-real locus, the equilibrium set is exactly
the union below. As a statement about all complex points, the reverse inclusion
again uses the asserted complex extension:

\[
 V(I_{\rm eq}(S))=\bigcup_{T\in M(S)}L_T,                 \tag{226.5}
\]

and its radical ideal has the squarefree coordinate-subspace decomposition

\[
 \sqrt{I_{\rm eq}(S)}=
 \bigcap_{T\in M(S)}(z_k:k\in S\setminus T).             \tag{226.6}
\]

Indeed, on a line `p wedge q=0`, and on one circle
`|p|=|q|`, so every pair coefficient in (226.1) vanishes. Conversely, the
finite-mode rigidity theorem puts the nonzero support of every equilibrium on
one such line or circle. Thus (226.5)--(226.6) classify all complex coefficient
components if the complex extension is supplied. The Fourier-real locus has
the analogous real set-theoretic classification. There is unconditionally no
hidden real nonlinear component and no positive-dimensional real component
carrying Euler motion.

## Mean mode and the only apparent exception

The theorem as printed does not state a mean-zero qualification, although a
nonzero mean makes literal time-independence false. After separating the
conserved mean velocity `U`, Galilean translation gives

\[
 u(x,t)=U+v(x-Ut),                                       \tag{226.7}
\]

where `v` is one of the stationary line/circle fields above. Its nonzero
coefficients acquire only the phases `e^{-it k dot U}`. Hence the smallest
time-dependent finite Fourier expression in a fixed coordinate frame is a
constant mean plus one conjugate pair, but it is merely a traveling single
harmonic. After the standard mean-zero normalization it is stationary. For real
solutions with one common finite support, (226.7) exhausts finite-mode time
dependence and produces nothing beyond one line or circle.

## Strategic consequence

Exact finite-dimensional real Euler closure is completely retired, not merely
for universal supports but also for coefficient-dependent invariant sets. The
same algebraic statement over all of `C^S` requires the complex extension noted
above.
Any Navier factor-two falsifier based on 2D Euler must start with a finite
packet and certify its genuinely infinite generated tail. Enlarging a
Galerkin support, imposing polynomial phase cancellations, or searching
singular invariant coefficient loci cannot produce an exact nonstationary
finite-mode orbit. This is an architecture theorem, not a Navier--Stokes
regularity result or a Millennium solution.
