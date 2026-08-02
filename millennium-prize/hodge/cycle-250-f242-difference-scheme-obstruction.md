# Cycle 250: F242 difference-scheme obstruction

## Exact difference divisor

Retain the Cycle 248 notation

\[
 C:X^4+Y^4=Z^4,\qquad A=E^3,\qquad
 \phi=(q_X,q_Y,q_Z):C\longrightarrow A
\]

up to translation, and let

\[
 \delta_\phi:C\times C\longrightarrow A,\qquad
 (p,q)\longmapsto\phi(p)-\phi(q).
\]

Write `D` for its scheme-theoretic image.  The map from `C-C` in `J(C)` to
its image in `A` is generically one-to-one.  Indeed, the usual difference map
is generically one-to-one because the nonhyperelliptic plane quartic has no
`g^1_2`.  The degree-eight isogeny `Psi:J(C)->A` does not change the generic
degree: for every nonzero element `h` of its finite kernel, a divisor and its
translate by `h` meet in dimension at most one, since the principal theta
divisor has trivial translation stabilizer.

The product quotient map `phi` itself is a closed immersion.  A fiber of
`q_j` is an orbit of its deck involution `sigma_j`.  Two distinct points in a
common fiber of all three quotients would therefore be exchanged by at least
two distinct nontrivial elements of the Klein four group.  Their product would
fix both points; the third quotient is ramified there and has a singleton
geometric fiber, a contradiction.  Formula (245.5) also shows that `dphi` is
nowhere zero, because its three components form the canonical linear system.
Properness then proves the assertion.  In particular
`delta_phi^{-1}(0)=Delta_C` set-theoretically, so no nonzero kernel point of
`Psi` contributes another branch of `D` at zero.

Consequently the fundamental class of the image is the Pontryagin square, not
one half of it.  With the Cycle 248 normalization

\[
 \gamma=2(\eta_2\eta_3+\eta_1\eta_3+\eta_1\eta_2),
\]

the same-coordinate products have image of dimension one and vanish as
two-cycles, while the two orders of every pair of distinct coordinate curves
give the corresponding coordinate surface.  Hence

\[
 \boxed{[D]=\gamma*[-1]^*\gamma
 =8(\eta_1+\eta_2+\eta_3)\in H^2(A,\mathbb Z).}
 \tag{250.1}
\]

Thus `D` is an effective ample Cartier divisor.  Scheme-theoretically it is
the elimination image of the explicit Cycle 248 degree-two quotients:

\[
 I_D=\left(
 I_C(p)+I_C(q)+I_E(a)+
 \langle a_j-(q_j(p)-q_j(q))\rangle_{j=X,Y,Z}
 \right)\cap K[A],
 \tag{250.2}
\]

where subtraction is imposed by the projective group-law equations of
`E:v^2=u^3+4u` and all chart ideals are homogenized and saturated before
elimination.  Formula (250.2) is a finite exact construction of the full
divisor; it does not replace the scheme image by its set of points.  Since
`C x C` is integral and the difference map is generically one-to-one, this
scheme image is an integral, reduced, symmetric divisor.

## The identity singularity

The diagonal of `C x C` is contracted to zero.  Its normal directions map to
the canonical tangent directions of `C`.  In invariant tangent coordinates
`(z_X,z_Y,z_Z)` dual to `du/v` on the three elliptic factors, (245.5) sends the
canonical point to

\[
 [z_X:z_Y:z_Z]=[x:-y:-\zeta],
\]

and `x^4+y^4=1`, `zeta^4=-1`.  Therefore

\[
 \boxed{\operatorname{TC}_0(D):
 z_X^4+z_Y^4+z_Z^4=0.}
 \tag{250.3}
\]

In particular `mult_0(D)=4`.  This is also the tangent-cone description of the
contracted diagonal in the classical difference surface of a nonhyperelliptic
genus-three curve, transported through the invertible tangent map of `Psi`.

## Correction to the proposed scheme gate

For a candidate `M=[L_1 L_2 L_3]:A^3->E^6`, geometric injectivity is the
set-theoretic condition

\[
 \ker(M)(\bar K)\cap D(\bar K)^3=\{0\},
 \tag{250.4}
\]

together with the requirement that every preimage of zero under
`delta_phi^3` is diagonal.  Closed immersion is most safely tested by the
original fiber product

\[
 C^3\times_{E^6}C^3=\Delta_{C^3}
 \tag{250.5}
\]

scheme-theoretically.  The stronger assertion

\[
 \ker(M)\cap D^3=\{0\}\quad\hbox{as schemes}
 \tag{250.6}
\]

is never true for a full-rank `M` and therefore is not equivalent to (250.5).
At the identity, `ker(M)^0` is a smooth threefold.  Each of the three pulled
back equations of `D` lies in the fourth power of its maximal ideal by
(250.3).  Their ideal cannot equal the maximal ideal, by Nakayama.  If the
three tangent-cone quartics form a regular sequence, the intersection is
isolated and its local length is

\[
 \boxed{4^3=64,}
 \tag{250.7}
\]

not one.  If they do not form a regular sequence, their leading-form
intersection is positive-dimensional; higher terms must then be retained to
determine the actual local length.  Every case still rejects (250.6), already
by Nakayama, but does not reject the closed immersion (250.5): passing from
`C x C` to its difference image contracts the diagonal and necessarily loses
its reduced scheme structure.

There is also a global consistency check.  If `K=ker(M)` meets `D^3` properly,
then

\[
 \deg(K\cdot D_1D_2D_3)
 =8^3\deg\bigl(K\cdot\Theta_1\Theta_2\Theta_3\bigr),
 \tag{250.8}
\]

so the total intersection length is divisible by `512`.  For a parametrization
`N:E^3->K^0` with three row blocks `N_r`, put
`H_r=conjugate(N_r)^t N_r`.  The pullback intersection is

\[
 8^3[t_1t_2t_3]\det(t_1H_1+t_2H_2+t_3H_3).
 \tag{250.9}
\]

The appropriate isogeny degree and component-group factors convert (250.9) to
the intersection on the full kernel.

## Executable finite gate

For each full-rank matrix, compute an exact `9 x 3` nullspace matrix `N`, split
it into blocks `N_r`, and form

\[
 F_r(t)=\sum_{j=1}^3((N_rt)_j)^4.
 \tag{250.10}
\]

The three affine Groebner tests obtained by setting each projective coordinate
of `t` equal to one decide whether `F_1,F_2,F_3` have a common projective zero.
A common zero says that the quartic leading-form prefilter is degenerate and
that a full local Groebner calculation is needed; no common zero certifies the
isolated fat identity of length 64.  The companion script
`verify_cycle250_f242_difference_gate.py` executes this exact test for a JSON
candidate matrix.  In both cases the requested identity-scheme gate fails, so
future F242 enumeration must use (250.5), not (250.6).

The corrected closed-immersion gate is nevertheless finite and executable.
For each of the `3^6` standard projective charts on the two copies of every
source factor:

1. substitute the rational formulas (245.1) for `q_X,q_Y,q_Z` and clear the
   denominators, saturating by their product;
2. impose the six elliptic group-law equations for
   `sum_r L_r(phi(p_r)-phi(q_r))=0`;
3. reduce the resulting ideal together with the six Fermat equations and
   compare its saturation with the diagonal ideal
   `I_Delta=(p_1-q_1,p_2-q_2,p_3-q_3)` in homogeneous coordinates;
4. accept G0 exactly when every chart gives the diagonal ideal (equivalently,
   when saturation away from `I_Delta` is the unit ideal and the diagonal
   conormal map is an isomorphism).

Only addition, negation, and the CM automorphism `(u,v)->(-u,iv)` occur because
the matrix alphabet is `{0,1,-1,i,-i}`.  Thus every equation is over
`Q(zeta_8)`, and this is an exact finite Groebner gate for each candidate.  The
nullspace test (250.10) is a cheap prefilter for the invalid contracted-image
scheme condition, not a substitute for this corrected source-level gate.
