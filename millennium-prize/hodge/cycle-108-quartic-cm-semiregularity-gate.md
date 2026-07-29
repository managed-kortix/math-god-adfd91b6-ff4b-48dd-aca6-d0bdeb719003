# Cycle 108: quartic-CM semiregularity mechanism gate

## Explicit arithmetic-instance search

The strongest candidate curve is the canonical genus-four complete intersection
from Hanselman--Pieper--Schiavone, Example 5.3:
\[
 Q=x^2-xz-xw-y^2-yw+2z^2+zw-4w^2
\]
and
\[
\begin{aligned}
G={}&2xyw-2xz^2-12xzw-10xw^2-y^2z-2y^2w\\
 &+yzw+4yw^2+2z^3-20zw^2-18w^3.
\end{aligned}
\]
The doubled symmetric matrix of `Q` has determinant `113`, so the quadric is
smooth and the curve has the required two geometric `g^1_3` pencils.  Its
candidate modular factor has Hecke field `Q(zeta_15)^+`, containing
`F=Q(sqrt(5))`, with norm-one unit `(3+sqrt(5))/2`.

However the source labels the Jacobian/modular identification heuristic: it is
based on numerical Schottky reconstruction and local-factor comparisons.  No
explicit algebraic correspondence certifies the RM action on this exact
Jacobian, and integrality of the unit in its actual endomorphism ring is not
proved.  Thus it is a finite certification target, not a verified Markman
instance.

## Exact contraction rank

For
\[
 \operatorname{ch}(F_2)=N\left(g^*\Theta-rac q6(g^{-1})^*\Theta^3\right),
\]
the Chern-contraction map on
\[
 HT^2=H^2(\mathcal O_X)\oplus H^1(T_X)
 \oplus H^0(\wedge^2T_X)
\]
splits into a `16 -> 12` middle block and a `12 -> 16` outer block.  In an
eigenbasis, every two-index minor is controlled by
\[
 a_ic_j-a_jc_i=c_ic_j(r_i-r_j),\qquad r_i=a_i/c_i.
\]

For four pairwise-distinct ratios the rank would be `24`.  Markman's genuine
real-quadratic fourfold instead has forced multiplicities `(2,2)`:
\[
 r_1=r_2\ne r_3=r_4.
\]
The exact ranks are therefore
\[
 \operatorname{rank}C_{\rm mid}=10,\qquad
 \operatorname{rank}C_{\rm out}=10,
\]
and
\[
 \boxed{\operatorname{rank}C_{F_2}=20,\qquad
 \dim\ker C_{F_2}=8.}
\]
This corrects the provisional rank-`24` target in Cycle 107.  Semiregularity on
the obstruction image requires
\[
 \operatorname{rank}(ob_{F_2})=20,
 \qquad \ker(ob_{F_2})=\ker(C_{F_2}).
\]

## Structural obstruction

Serre duality gives a nondegenerate trace pairing on the full
`Ext^2(F_2,F_2)`.  The kernel equality is equivalent to nondegeneracy of that
pairing restricted to the Atiyah-obstruction image.  Simplicity does not imply
this: a one-dimensional isotropic subspace of a hyperbolic plane is an exact
linear countermodel.

Riemann--Roch computes only the alternating Ext Euler characteristic.  The
glued sheaf has a two-term presentation whose derived endomorphism differential
contains the gluing map and whose Atiyah class contains its off-diagonal
derivative.  These data can change the obstruction image while leaving the
Chern character and contraction matrix fixed.  Generic gluing may therefore
create trace-radical Ext directions; dimension counts cannot rule them out.

## Rotation decision

The route is not promoted.  Its next valid checkpoint is stricter than Cycle
107's: certify an explicit RM curve and integral unit action, instantiate every
secant/gluing map and a finite resolution, and prove exact equality of the
eight-dimensional kernels (equivalently obstruction rank `20`).  No such
integrated certificate exists.  No Hodge result is claimed.
