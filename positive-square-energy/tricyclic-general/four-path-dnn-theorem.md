# Four-path tricyclic blocks via an exact DNN dual

## Theorem

Let `G` have one cyclic block consisting of four internally disjoint paths of
positive lengths `l_1,...,l_4` between two terminals, and arbitrary rooted trees
attached at single vertices. If `G` is simple (so at most one `l_i` is one),
then

`s^+(G) >= |V(G)|`.

## DNN constant and correlation dual

For a graph `H`, put

`kappa(H)=sup_{M psd, M>=0} 4(sum_{uv in E} sqrt(M_uv))^2/<J,M>`.

The exact dual is

`kappa(H)=min_{C psd, diag C=1} sum_{uv in E} 2/(1-C_uv)`.          (1)

Weak duality follows from weighted Cauchy--Schwarz and

`<J,M>-sum_E 2(1-C_uv)M_uv
 =<C,M>+2 sum_{nonedges}(1-C_uv)M_uv >=0`.

For completeness, reverse duality follows after normalizing `<J,M>=1` from
`(sum sqrt(x_e))^2=min_{a in simplex} sum x_e/a_e`, Sion minimax (the
normalized DNN section and simplex are compact after an epsilon truncation),
and `(PSD intersect N)^*=PSD+N`.  If
`tau J-Q(a)=P+N`, where `Q(a)_uv=2/a_uv` on edges, then
`C=(P+diag(tau-P_vv))/tau` is a correlation matrix and
`sum_E 2/(1-C_uv)<=tau`. Conversely, for a correlation matrix C, put
`q_e=2/(1-C_e)`, `a_e=q_e/sum q`; then
`(sum q)J-Q(a)=(sum q)C+N_0`, with `N_0>=0` supported on nonedges.
This proves (1), including boundary limits.

The known LTZ/DNN inequality is `s^-(H)<=kappa(H)`.

## Exact path and multipath formula

Fix endpoint correlation `rho` on a path of `l` edges. Alternately negate its
unit Gram vectors. The transformed endpoint angle is

`beta_l=acos((-1)^l rho)`.

Spherical triangle inequality and convexity of `sec^2(x/2)` show that the path
cost in (1) is at least

`l sec^2(beta_l/(2l))`.

Equally spaced vectors on the shortest planar arc attain equality. Different
paths can use the same endpoint vectors, so for an r-path theta this proves

`kappa=min_{0<=theta<=pi} [sum_{l even} l sec^2(theta/(2l))
 +sum_{l odd} l sec^2((pi-theta)/(2l))]`.                    (2)

For four paths write `L=sum l_i` and subtract the baseline L. It remains to
prove

`min_theta Phi(theta)<=2`, where

`Phi(theta)=sum_even l tan^2(theta/(2l))
 +sum_odd l tan^2((pi-theta)/(2l))`.                         (3)

## Four-term tangent lemma

Put `x=theta/2` and `h_s(y)=s tan^2(y/s)`. For fixed positive y, `h_s(y)` is
strictly decreasing in s, because

`d h_s/ds = tan(z)/cos^2(z) (sin(z)cos(z)-2z)<0`, `z=y/s`.

If no length is one, replace every even length by 2 and every odd length by 3.
If e is the number of even lengths, the resulting upper bound is

`F_e(x)=2e tan^2(x/2)+3(4-e)tan^2((pi/2-x)/3)`.

For e=0,4 it vanishes at an endpoint; for e=3, `F_3(0)=1`; for e=1,
`F_1(pi/2)=2` and its left derivative there is positive; for e=2,
`F_2(0)=2` and its right derivative there is negative. Hence the minimum is
strictly below two.

If exactly one length is one, its term is `cot^2 x`. If e of the remaining
three lengths are even, replace evens by 2 and odds by 3. For e=0 the bound
vanishes at `x=pi/2`; for e=1,2, testing `x=pi/3` and using
`tan(pi/18)<1/3` gives a value below two. For e=3,

`Phi(2x)<=cot^2 x+6tan^2(x/2)`.

With `u=tan(x/2)`, the right side is

`1/(4u^2)-1/2+25u^2/4 >=2`,

and its minimum is exactly two at `u^2=1/5`. This is an upper bound on Phi,
but evaluating at this minimizer and using strict decrease of `h_s` shows
`Phi<2` unless all three even lengths are two. For `(1,2,2,2)` equality is
an identity. Thus (3) holds, with equality only for that tuple.

Consequently `kappa(B)<=L+2`. The core has `m=L`, `n=L-2`; therefore

`s^+(B)=2L-s^-(B)>=2L-kappa(B)>=L-2=n`.

Finally kappa is additive under one-vertex sums. This follows either from (1)
by rooted correlation gluing or directly after folding DNN matrices to edge
support and orthogonally splitting the two sides. Since `kappa(T)=|E(T)|` for
a tree, attaching t tree edges adds t to both kappa and the vertex count, and
the same conclusion holds for arbitrary rooted-tree attachments.

## Sharp DNN exception inside the family

For `(1,2,2,2)`, `kappa=9=L+2`; the core spectrum is
`{3,-2,-1,0,0}`, so `s^+=9>5`. Equality in the auxiliary DNN bound is not
equality in the target theorem.
