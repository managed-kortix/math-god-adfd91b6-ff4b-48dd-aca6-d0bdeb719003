# Cycle 164: split adapted quotients retain the diagonal involution

Every completely adapted split-prime PEL kernel preserves the cross-factor
involution, so each quotient still contains an abelian threefold and has a
non-PEL endomorphism.  This identifies every individual target as special, but
does not by itself determine the Zariski closure of their varying Hecke orbit.

## Setup

Write

\[
A_0=X\times X,\qquad X=E_i^3,
\]

let `J=(i,-i)` be the prescribed `O=Z[i]` action, and define

\[
t(x,y)=(y,x).
\]

Then

\[
t^2=1,\qquad tJ=-Jt,
\]

and the Cycle 151 diagonal and anti-diagonal are the rational eigenspaces

\[
\Gamma=\ker(1-t)^0,\qquad J\Gamma=\ker(1+t)^0.
\]

Fix a good split prime `p>=5`.  By Cycle 163, every PEL-stable kernel with
`eta_p=1` is

\[
K_{L,\epsilon}=D\oplus JD,\qquad
D=L\oplus\ell_\epsilon\subset\Gamma[p],
\]

where `L` is Lagrangian in the four-dimensional radical and
`\ell_\epsilon` is one of the two isotropic lines in the residual split plane.
Let

\[
f:A_0\longrightarrow B=A_0/K_{L,\epsilon}
\]

be the corresponding polarized `p`-isogeny.

## Exact descent

Since `t` is the identity on `D` and minus the identity on `JD`,

\[
t(K_{L,\epsilon})=K_{L,\epsilon}.
\]

Consequently there is a unique integral endomorphism `tbar` of `B` satisfying

\[
\boxed{\ tbar\,f=ft\ },\qquad
\boxed{\ tbar^2=1,\quad tbar J=-Jtbar\ }.
\]

Thus `tbar` is again a `K`-antilinear cross-factor endomorphism.  It is not
part of the generic `K`-linear PEL endomorphism algebra.

The exact descended graph correspondence is

\[
\boxed{
[\Gamma_{tbar}]=p^{-6}(f\times f)_*[\Gamma_t]
\quad\text{in }CH^6(B\times B)_Q.}
\]

Indeed, the map from `Gamma_t` to its image has kernel `K`, of order `p^6`.
Equivalently, the two rational algebraic projectors on `H^1(B,Q)` are

\[
\boxed{
e_+={\Delta_B+\Gamma_{tbar}\over2},\qquad
e_-={\Delta_B-\Gamma_{tbar}\over2}.}
\]

These have rank six each and satisfy `e_+e_-=0`, `e_++e_-=\Delta_B`.

## The descended threefold

Put

\[
Y=f(\Gamma),\qquad Z=f(J\Gamma).
\]

Then

\[
\boxed{
Y=\ker(1-tbar)^0=\operatorname{im}(1+tbar),\qquad
Z=\ker(1+tbar)^0=\operatorname{im}(1-tbar).}
\]

Both are abelian threefolds.  The restrictions of `f` have kernels `D` and
`JD`, respectively, and hence both have degree `p^3`.  In particular the
Cycle 162 normalization has no denominator:

\[
\boxed{f_*[\Gamma]=p^3[Y],\qquad p^{-3}f_*[\Gamma]=[Y].}
\]

The addition map `Y times Z -> B` is an isogeny.  Its kernel is 2-primary:
if a point lies in both rational eigenspaces of `tbar`, then it is killed by
two.  Thus the odd split-prime quotient changes neither the rational
`(+1)/(-1)` decomposition nor the existence of the diagonal factor.

The Weil projector also descends exactly.  For `u=2+i`, let `ubar` be its
descended `O`-linear endomorphism and let `q` be the interpolation polynomial
of Cycle 152.  Then

\[
P_{\rm Weil,B}=q(\Gamma_{ubar}),
\qquad
\boxed{
P_{\rm Weil,B}[Y]=p^{-3}f_*P_{\rm Weil,A_0}[\Gamma]\ne0.}
\]

No choice of `L` or `epsilon` removes this correspondence.

## Consequence

Every one of the `2(p+1)(p^2+1)` split adapted kernels gives a point with a
rank-six `K`-antilinear involution.  Equivalently, the quotient is non-simple
and contains the abelian subthreefold `Y`.  Each individual point lies on a
proper extra-endomorphism/decomposition locus: at a very general point the
rational endomorphism algebra is `K`, whereas `tbar` anticommutes with `K`.

The involution varies by rational Hecke conjugacy with the kernel.  Therefore
these points have not been placed in one fixed proper closed subvariety.  A
countable Hecke orbit of special points can be Zariski dense, so individual
specialness does **not** close the split transport escape.  What is proved is
the exact preservation and denominator-one transport of the algebraic Weil
class.  Determining the restricted Hecke-orbit closure requires an adelic
generation/strong-approximation calculation.  No Hodge-conjecture result is
claimed.
