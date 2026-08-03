# Cycle 274: shrinking-radius displacement hostile audit

## Question

Can the datum-free shrinking-Wiener gates

\[
 q(t)=q_0(1-\alpha t),\qquad
 A_{q_0}(u_0)\le M,\qquad \alpha\ge M,\qquad q(T)>1
 \tag{274.1}
\]

be structurally incompatible with the displacement needed for a factor-two
increase of the velocity `L3` norm? The answer is no. The strongest direct
displacement estimate from these controls leaves a nonempty, scale-invariant
parameter region.

## Direct displacement cap

Write

\[
 Q=q(T)>1,\qquad
 \kappa(Q)=\max_{n\ge1}{n\over Q^n}.
\]

The shrinking-radius lemma gives `A_{q(t)}(u(t))<=M` for `0<=t<=T`. For the Euler
bilinear map `B(v,w)=-P((v dot grad)w)`, the same convolution estimate used in
Cycle 265 gives

\[
 \|u_t(t)\|_3\le \|u_t(t)\|_\infty
 \le A_1(u(t))D_1(u(t))
 \le \kappa(q(t))M^2.                                  \tag{274.2}
\]

Consequently Minkowski and the fundamental theorem of calculus imply

\[
 \boxed{\ \|u(T)-u_0\|_3
 \le M^2\int_0^T\kappa(q(t))\,dt
 \le \kappa(Q)M^2T.\ }                                \tag{274.3}
\]

If `U=||u_0||_3`, an endpoint ratio strictly above two necessarily has

\[
 \|u(T)-u_0\|_3>U.                                     \tag{274.4}
\]

Energy conservation supplies the datum-dependent lower bound

\[
 U\ge E:=\|u_0\|_2,
\]

while the initial Wiener control supplies the stronger chain

\[
 M\ge A_{q_0}(u_0)\ge q_0 A_1(u_0)
 \ge q_0 U\ge q_0 E.                                  \tag{274.5}
\]

The radius gate only gives

\[
 \alpha T<1-{1\over q_0},\qquad
 MT\le\alpha T<1-{1\over q_0}.                         \tag{274.6}
\]

It does not upper-bound `M/U`. Combining (274.3)--(274.6) therefore does not
force the displacement cap below `U`.

More transparently, put

\[
 x={M\over U},\qquad \tau=MT,\qquad a={\alpha\over M}\ge1.
\]

Then, after the change of variable `s=Mt`,

\[
 Q=q_0(1-a\tau)>1,
 \qquad {M^2\int_0^T\kappa(q(t))dt\over U}
 =x\int_0^\tau\kappa(q_0(1-as))ds
 \le\kappa(Q)x\tau.                                   \tag{274.7}
\]

Indeed (274.5) says `x>=q0`, but neither it nor the `L2` lower bound gives an
upper bound on `x`. Thus even the exact integral in (274.7) can exceed one.
Under Euler amplitude scaling
`u -> lambda u(lambda t)`, the quantities `x`, `tau`, `a`, and `Q` are
unchanged: shrinking the amplitude lengthens the admitted time by the inverse
factor but does not close this dimensionless region.

## Exact abstract rational consistency assignment

No velocity datum is asserted. The following exact rational scalar assignment
satisfies every inequality used above and leaves room for the necessary
factor-two displacement. It is a nonemptiness certificate for the scalar
inequalities, not a `WITNESS` under the Cycle 274 capacity classification:

\[
 q_0=2,\quad A:=A_{q_0}(u_0)=M=\alpha=1,\quad T={1\over4},
 \quad Q={3\over2},
\]

\[
 E={1\over10},\quad U={1\over8},\quad d={3\over20}.
\tag{274.8}
\]

For `Q=3/2`, the ratio of consecutive terms `n/Q^n` is
`2(n+1)/(3n)`. It increases through `n=2`, ties at `n=2,3`, and then
decreases, so

\[
 \kappa(3/2)={8\over9}.
\]

All checks are exact:

\[
 \alpha\ge M,\qquad Q={3\over2}>1,
 \qquad U={1\over8}\ge E={1\over10},
 \qquad M=1\ge q_0E={1\over5},
\]

and

\[
 M\ge q_0U={1\over4}\ge q_0E={1\over5}.
\]

Moreover, `q(t)=2(1-t)`. On `3/2<=q<=2`, direct comparison of consecutive
terms shows `kappa(q)=2/q^2` (with only endpoint ties). Hence the sharper
time-dependent cap is exactly

\[
 M^2\int_0^T\kappa(q(t))dt
 =\int_0^{1/4}{1\over2(1-t)^2}dt={1\over6},
\]

and

\[
 U={1\over8}<d={3\over20}<{1\over6}
 <\kappa(Q)M^2T={2\over9}.                              \tag{274.9}
\]

Hence the abstract necessary inequalities are jointly feasible. This
assignment is deliberately not a Fourier field and proves no Euler orbit
exists with these values; it proves only that the proposed datum-free
contradiction cannot follow from the shrinking-radius gates, the direct `A_q`
displacement cap, and the conserved `L2` lower bound alone.

## Decision

The hostile structural no-go fails. A particular datum can still be rejected
when its certified `E`, `U`, `M`, `q(t)`, and `T` make the integral in
(274.3) at most `U`, as happened in Cycle 272. Without datum-specific control of
`M/U`, or a sharper mechanism coupling Wiener mass to velocity `L3`, the
general factor-two region remains nonempty. No datum, trajectory, Euler
crossing, Navier--Stokes conclusion, or Millennium claim is made.
