# Cycle 248: explicit Fermat-quartic elliptic splitting for F242

## Models and quotient maps

Let

\[
 C:\ X^4+Y^4=Z^4,
 \qquad
 E:\ v^2=u^3+4u,
\]

and put `K=Q(zeta)`, where `zeta^4=-1`.  The curve `E` has `j=1728`;
the automorphism `(u,v) -> (-u,iv)` identifies its complex multiplication ring
with `Z[i]`, so this is an algebraic model of the `E_i` used in F242.  The
extension from `Q(i)` to `K` is allowed by Cycle 242.

For any ordered triple `(A,B,C_0)` satisfying

\[
 A^4+B^4=C_0^4,
\]

define the degree-two rational map `q(A,B,C_0):C -> E` by

\[
 t=B/C_0,\qquad s=A^2/C_0^2,
\]

\[
 u={2(1+s)\over t^2}={2(C_0^2+A^2)\over B^2},
 \qquad
 v={4(1+s)\over t^3}={4C_0(C_0^2+A^2)\over B^3}.
 \tag{245.1}
\]

Indeed `s^2=1-t^4`, and direct substitution gives

\[
 v^2=u^3+4u.
\]

Formula (245.1) is a rational presentation of a morphism: the induced function
field inclusion has degree two, and the rational map extends uniquely because
`C` is smooth and `E` is proper.  Thus apparent simultaneous zeros in one
projective presentation are only removable chart indeterminacies.

The three required elliptic quotients are

\[
 q_X=q(X,Y,Z),\qquad
 q_Y=q(Y,X,Z),\qquad
 q_Z=q(Z,\zeta X,Y).
 \tag{245.2}
\]

The last triple is valid because `Z^4+(zeta X)^4=Z^4-X^4=Y^4`.
Their deck involutions are respectively the three nontrivial sign involutions
of the projective Fermat quartic:

\[
 \sigma_X[X:Y:Z]=[-X:Y:Z],\quad
 \sigma_Y[X:Y:Z]=[X:-Y:Z],\quad
 \sigma_Z[X:Y:Z]=[X:Y:-Z].
\]

Projectively, `sigma_X sigma_Y sigma_Z=1`, so these form a Klein four group.
The corresponding three rational idempotents in `Q[Aut(C)]` are

\[
 e_X={1+\sigma_X-\sigma_Y-\sigma_Z\over4},\quad
 e_Y={1-\sigma_X+\sigma_Y-\sigma_Z\over4},\quad
 e_Z={1-\sigma_X-\sigma_Y+\sigma_Z\over4}.
 \tag{245.2a}
\]

They are pairwise orthogonal and sum to the identity on `H^1(C,Q)` (the
remaining trivial-character projector has zero image there).  The images of
`e_X,e_Y,e_Z` are exactly the three elliptic isotypic factors cut out by
`q_X,q_Y,q_Z`.

## The map, its differential, and the Jacobian isogeny

Fix `p_0=[0:1:1]` and use the group law on `E` to set

\[
 \phi(p)=
 \bigl(q_X(p)-q_X(p_0),q_Y(p)-q_Y(p_0),q_Z(p)-q_Z(p_0)\bigr).
 \tag{245.3}
\]

Omitting the three constants merely translates `phi(C)` and changes none of
the F242 difference, tangent, or cohomology calculations.

Let `omega=du/v`.  Differentiating (245.1) on `s^2=1-t^4` gives the exact
identity

\[
 q(A,B,C_0)^*\omega=-{dt\over s}.
 \tag{245.4}
\]

On the affine chart `Z=1`, write `x=X/Z`, `y=Y/Z`; then
`x^4+y^4=1` and `dy=-x^3dx/y^3`.  Equations (245.2)--(245.4) give

\[
 q_X^*\omega={x\,dx\over y^3},\qquad
 q_Y^*\omega=-{dx\over y^2}=-{y\,dx\over y^3},\qquad
 q_Z^*\omega=-\zeta {dx\over y^3}.
 \tag{245.5}
\]

Consequently, for a tangent vector `a d/dx` in this chart,

\[
 d\phi_p(a\partial_x)=
 a\left({x\over y^3},-{1\over y^2},-{\zeta\over y^3}\right)
 \tag{245.6}
\]

in the invariant tangent coordinates dual to `omega`.  Formula (245.5), rather
than the displayed affine denominators in (245.6), is the global definition at
points on the omitted charts.  The three pullbacks are a basis of
`H^0(C,Omega_C^1)`: they are nonzero scalar multiples of the standard canonical
basis

\[
 {dx\over y^3},\quad {x\,dx\over y^3},\quad {y\,dx\over y^3}.
\]

The induced homomorphism

\[
 \Psi:J(C)\longrightarrow E^3,
 \qquad
 [D]\longmapsto((q_X)_*D,(q_Y)_*D,(q_Z)_*D)
 \tag{245.7}
\]

has invertible tangent map by (245.5), and hence is an isogeny.  More exactly,
if `Psi^vee:E^3 -> J(C)` is the sum of the three pullbacks, then

\[
 (q_j)_*q_k^*=\begin{cases}[2],&j=k,\\0,&j\ne k.\end{cases}
 \tag{245.8}
\]

The diagonal assertion is degree-two push-pull.  For `j != k`, `q_k^*H^1(E)`
is anti-invariant under the deck involution of `q_j`, while
`q_j^*(q_j)_*=1+sigma_j^*`; injectivity of `q_j^*` proves the zero assertion.
Thus

\[
 \Psi\Psi^\vee=[2]_{E^3},\qquad \deg\Psi=8.
 \tag{245.9}
\]

This proves the claimed Jacobian decomposition, rather than assuming it.  The
map (245.3) is the Abel--Jacobi map followed by (245.7), up to its printed
translation.

## The exact curve class

Choose an oriented integral symplectic basis `alpha_j,beta_j` of the `j`th
copy of `H^1(E,Z)`, normalized by

\[
 \int_E alpha_j\wedge beta_j=1,
 \qquad eta_j=alpha_j\wedge beta_j.
\]

For `gamma=phi_*[C] in H^4(E^3,Z)`, degree two of each quotient and (245.8)
give

\[
 \int_Cq_j^*alpha_j\wedge q_j^*beta_j=2,
\]

and every mixed pairing between two distinct factors is zero.  Poincare
duality therefore determines all 15 coordinates of the class:

\[
 \boxed{\gamma=
 2(eta_2eta_3+eta_1eta_3+eta_1eta_2).}
 \tag{245.10}
\]

Equivalently, if `e_a:E -> E^3` is the `a`th coordinate inclusion, then

\[
 \gamma=2\sum_{a=1}^3(e_a)_*[E].
 \tag{245.11}
\]

This also supplies a smaller exact expansion for every F242 class.  If
`ell_(r,a):E -> E^6` is the homomorphism given by column `a` of `L_r`, then

\[
 (L_r)_*\gamma=2\sum_{a=1}^3(ell_{r,a})_*[E]
\]

and hence

\[
 \boxed{
 z_L=8\sum_{a,b,c=1}^3
 (ell_{1,a},ell_{2,b},ell_{3,c})_*[E^3].
 }
 \tag{245.12}
\]

Pushforward in (245.12) includes the generic degree when a displayed
homomorphism has finite kernel; no primitivity assumption is being made.

## Consequence for F242

There is no genus or Jacobian-decomposition obstruction to the proposed map.
The Fermat quartic has genus three, the three quotient differentials form its
entire canonical space, and (245.9) is the required explicit isogeny.  Equations
(245.1)--(245.6) and (245.10) remove the missing fixed-input defect identified
in Cycle 243.  They do not by themselves decide the closed-immersion,
seven-graph-span, Weil-projector, or deformation gates for all matrices `L`.
