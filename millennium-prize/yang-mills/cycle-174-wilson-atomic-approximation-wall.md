# Cycle 174: Wilson contraction plus atomic approximation

This note isolates the exact nonterminal finite-volume estimate that can be
composed into a full transfer contraction.  It also identifies the equivalence
wall: generatorwise contraction plus qualitative density is useless, while
approximation strong enough to close the argument already controls the full
operator norm.

## Atomic Wilson lemma

Let `D={w_alpha}` be normalized centered generating Wilson-loop states.  Assume
the generatorwise estimate

\[
 \|S w_\alpha\|\le\rho
\]

and the following quantitative atomic approximation: every `f in H_0` has a
finite Wilson expansion `g=sum_alpha c_alpha w_alpha` such that

\[
 \|f-g\|\le\epsilon\|f\|,
 \qquad
 \sum_\alpha|c_\alpha|\le A\|f\|.
\]

Then the triangle inequality gives the exact composable estimate

\[
 \|Sf\|\le\|S(f-g)\|+
 \sum_\alpha|c_\alpha|\|Sw_\alpha\|
 \le(\epsilon+\rho A)\|f\|.
\]

Hence `epsilon+rho A<1` implies a full transfer contraction and a gap
`-log(epsilon+rho A)/(aN)`.  If only
`<w_alpha,S w_alpha><=q` is known, positivity and `||S||<=1` imply
`||S w_alpha||^2=<w_alpha,S^2w_alpha><=<w_alpha,S w_alpha><=q`, so one may take
`rho=sqrt(q)`.

The coefficient bound is essential.  Generatorwise contraction plus even exact
finite-dimensional spanning does not suffice.  In `R^2`, take

\[
 S=P_{e_1},\qquad
 w_+=(e_1+e_2)/\sqrt2,\qquad
 w_-=(e_1-e_2)/\sqrt2.
\]

Both generators satisfy `||S w_+||=||S w_-||=1/sqrt(2)` and their span is all
of `R^2`, but `||S||=1`; their weakly contracted images add coherently to the
uncontracted vector `e_1`.  The atomic lemma sees the obstruction sharply:
representing `e_1` has coefficient cost `A>=sqrt(2)`, so `rho A>=1`.

Thus "contraction on generating Wilson loops plus density" is false unless
quantitative approximation controls a synthesis norm that pays for coherent
linear combinations.  Equivalently one may estimate the full Gram matrix
`(<S w_alpha,S w_beta>)`, but diagonal loop bounds alone are insufficient.

## Abstract lemma

For comparison, let `H` be a Hilbert space, let `Omega` be a unit vacuum, and put
`H_0=Omega^perp`.  Let `S:H_0->H_0` be a positive self-adjoint contraction; in
the lattice application `S=Q T^N Q`, where `N=ceil(r_0/a)` and `Q` removes the
vacuum and every exactly transmitted superselection label.  Let `A` be a
linear span of centered generating Wilson-loop states.

Assume there are constants `0<=q<1` and `0<=epsilon<1`, uniform in cutoff,
volume, boundary condition, and physical sector, such that

1. `||Sg|| <= q ||g||` for every `g in A`;
2. for every `f in H_0` there is `g in A` with
   `||f-g|| <= epsilon ||f||`.

Then

\[
 ||S||_{H_0\to H_0}\le q+(1+q)\epsilon.
\]

Consequently, if `q+(1+q)epsilon<1`, then

\[
 Q T^N Q\le [q+(1+q)\epsilon]Q,
\]

and the usual transfer-matrix argument gives the finite-cutoff lower gap

\[
 m_{a,L}\ge {-\log(q+(1+q)\epsilon)\over a\lceil r_0/a\rceil}.
\]

Indeed, for a unit vector `f` and its approximant `g`,

\[
 \|Sf\|\le\|S(f-g)\|+\|Sg\|
 \le\epsilon+q\|g\|
 \le q+(1+q)\epsilon.
\]

If the available Wilson estimate is only the positive quadratic-form bound
`<g,Sg> <= q||g||^2`, positivity gives `||Sg|| <= sqrt(q)||g||`; the conclusion
becomes

\[
 ||S||\le \sqrt q+(1+\sqrt q)\epsilon.
\]

Thus the composable version must specify whether its loop contraction is an
operator-norm estimate or only a same-state correlator estimate.

## Exact relative-width formulation

The preceding hypothesis with one fixed `epsilon<1` is not ordinary density.
For a linear subspace `A`, qualitative density in each fixed finite-volume
space actually gives `epsilon=0` after taking an infimum, so boundedness extends
the contraction from `A` to all of `H_0` immediately.  The nontrivial
cutoff-uniform statement must instead restrict the approximants by complexity.

Let `A_M` be the span of centered Wilson words of complexity at most `M`, and
define

\[
 q_M=\sup_{0\ne g\in A_M}{\|Sg\|\over\|g\|},\qquad
 \delta_M=\sup_{\|f\|=1}\inf_{g\in A_M}\|f-g\|.
\]

Then, exactly,

\[
 \|S\|\le\inf_M\{q_M+(1+q_M)\delta_M\}.
\]

This is useful only if one proves, uniformly in all regulators, a single
complexity scale `M` for which the right side is below one.  But for every
linear subspace `A_M`,

\[
 \delta_M=0\quad\hbox{if }\overline{A_M}=H_0,
 \qquad
 \delta_M=1\quad\hbox{otherwise}.
\]

The second assertion follows by taking a unit vector perpendicular to
`overline(A_M)`.  Therefore a global relative approximation of every Hilbert
state by one proper Wilson trial space cannot have error below one.  The stated
lemma is mathematically exact but, with unrestricted target states and linear
trial spaces, it collapses to full density at the same complexity scale and
hence to full-operator contraction.

## A genuinely weaker sufficient inequality

A nontrivial decomposition is possible only by controlling the residual with
a second norm on which `S` is strictly contractive.  Let `Pi_M` be an orthogonal
projection onto a Wilson-generated trial space and assume

\[
 \|S\Pi_M\|\le q_M,
 \qquad
 \|S(I-\Pi_M)\|\le r_M,
 \qquad q_M^2+r_M^2<1.
\]

Then for every unit `f`, writing `x=||Pi_M f||` and
`y=||(I-Pi_M)f||`,

\[
 \|Sf\|\le q_Mx+r_My
 \le\sqrt{q_M^2+r_M^2},
\]

so `||S||<1`.  More generally, if the two images are orthogonal, the sharper
bound is `||S||<=max(q_M,r_M)`.

This pair is weaker in form than estimating every state by Wilson loops: the
first inequality concerns the generated low-complexity block and the second is
a quantitative ultraviolet/high-complexity tail estimate.  It is composable,
but the tail estimate is indispensable.  Calling it "density" does not weaken
it: it must control `S` on the moving orthogonal complement where escaping
states live.

The hostile diagonal model makes the wall exact.  On `ell^2(N)`, let

\[
 S_n=qI+(1-q)P_{e_n},\qquad
 A_M=\operatorname{span}(e_1,\ldots,e_M).
\]

For every fixed `M`, `S_n` contracts `A_M` by `q` once `n>M`, and the union of
the `A_M` is dense.  Nevertheless `S_ne_n=e_n`.  No approximation rate stated
only for each fixed vector, no growing list of Wilson loops, and no convergence
of fixed loop correlators controls this moving residual.

## Yang--Mills checkpoint

The precise nonterminal target can therefore take either of two forms:

* prove generatorwise Wilson contraction together with a regulator-uniform
  atomic approximation bound satisfying `epsilon+rho A<1`;

or construct physical Wilson trial projections `Pi_(a,L,M)` after the Gauss and
OS quotients and prove both `||S Pi||<=q_M` and
`||S(I-Pi)||<=r_M`, with `q_M^2+r_M^2<1` at one regulator-independent physical
scale.

This is strictly more structured than a bare full-gap inequality and may admit
different mechanisms on the two pieces.  Logically, however, the two estimates
compose immediately to a full finite-volume spectral contraction.  There is no
intermediate theorem based on Wilson contraction plus qualitative density:
either quantitative approximation is too weak and escaping states survive, or
it is uniform enough to imply the full norm bound.  No Yang--Mills construction
or mass gap is proved here.
