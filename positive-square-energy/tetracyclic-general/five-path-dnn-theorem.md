# The five-path rank-four block

## Theorem

Let `B` be the union of five internally vertex-disjoint paths with common
terminals `a,b` and positive lengths `l_1,...,l_5`. Suppose that `B` is simple;
equivalently, at most one of the lengths is one. If `G` is obtained from `B`
by attaching arbitrary trees at single vertices, then

`s^+(G)>|V(G)|`.

In particular, every five-dipole subdivision, with arbitrary rooted-tree
attachments, satisfies the required non-strict inequality. There is no simple
exception and equality cannot occur.

## The DNN correlation dual

For a graph `H`, define

`kappa(H)=sup {4(sum_{uv in E(H)} sqrt(M_uv))^2/<J,M> : M psd, M>=0}`.

The correlation form of this constant is

`kappa(H)=min {sum_{uv in E(H)} 2/(1-C_uv) : C psd, C_vv=1}`.       (1)

Here and below a term with `C_uv=1` is interpreted as `+infinity`. For
reference, weak duality follows directly from weighted Cauchy--Schwarz and

`<J,M>-sum_{uv in E(H)}2(1-C_uv)M_uv
 =<C,M>+2 sum_{uv notin E(H), u<v}(1-C_uv)M_uv>=0`.

The reverse inequality is the standard conic dual: normalize `<J,M>=1`, use
`(sum_e sqrt(x_e))^2=min_{a_e>0, sum a_e=1} sum_e x_e/a_e`, and use
`(S_+ intersect N)^*=S_++N`. Thus (1) is exact, not merely a certificate.
The LTZ/DNN inequality gives

`s^-(H)<=kappa(H)`.                                                (2)

We shall also use the one-vertex-sum identity

`kappa(H_1 vee H_2)=kappa(H_1)+kappa(H_2)`.                         (3)

One proof of (3) is to use (1): correlation matrices on the two summands can
be glued at their common unit vector, placing their orthogonal complements in
orthogonal subspaces. Conversely, restriction of any feasible correlation
matrix to each summand gives the opposite inequality. In particular,
`kappa(T)=|E(T)|` for every tree `T`.

## Exact elimination of the five paths

Fix the terminal correlation `C_ab=cos(theta)`, where `0<=theta<=pi`, and
consider a path `v_0...v_l`. Represent `C` by unit vectors `p_j` and put
`q_j=(-1)^j p_j`. If `alpha_j` is the angle between `q_{j-1}` and `q_j`, then

`2/(1-C_{v_{j-1}v_j})=sec^2(alpha_j/2)`.

The angle between the transformed endpoint vectors is

`beta_l=theta` if `l` is even, and `beta_l=pi-theta` if `l` is odd.

The spherical triangle inequality gives `sum_j alpha_j>=beta_l`. Since
`sec^2(t/2)` is increasing and strictly convex on `[0,pi)`, Jensen's
inequality yields

`sum_{j=1}^l sec^2(alpha_j/2)>=l sec^2(beta_l/(2l))`.               (4)

Equality is attained by placing the transformed vectors at equal intervals
on a shortest planar arc. The five paths may all use the same two terminal
vectors, so the five equality constructions are compatible. Consequently,
if `L=sum_i l_i`, then

`kappa(B)=min_{0<=theta<=pi} [
 sum_{l_i even} l_i sec^2(theta/(2l_i))
 +sum_{l_i odd} l_i sec^2((pi-theta)/(2l_i))]`

`          =L+min_{0<=theta<=pi} Phi(theta)`,                      (5)

where the exact five-term DNN excess is

`Phi(theta)=sum_{l_i even} l_i tan^2(theta/(2l_i))
            +sum_{l_i odd} l_i tan^2((pi-theta)/(2l_i))`.          (6)

Thus all that remains is the following sharp-threshold tangent lemma.

## Five-term tangent lemma

**Lemma.** If `l_1,...,l_5` are positive integers and at most one is one,
then

`min_{0<=theta<=pi} Phi(theta)<3`.                                 (7)

In particular, equality in the bound `min Phi<=3` never occurs under the
simplicity hypothesis.

**Proof.** Put `x=theta/2` and

`h_s(y)=s tan^2(y/s)`.

For fixed `0<y<=pi/2`, this function is strictly decreasing in `s`. Indeed,
with `z=y/s`,

`d h_s(y)/ds=tan(z)sec^2(z)(sin(z)cos(z)-2z)<0`,                   (8)

because `sin(z)cos(z)<z<2z`. The assertion at `y=0` follows by continuity.
Hence every even length may be decreased to two and every odd length greater
than one may be decreased to three when constructing an upper bound for
`Phi`.

First suppose that no length is one, and let `e` be the number of even
lengths. By (8),

`Phi(2x)<=F_e(x):=2e tan^2(x/2)
                    +3(5-e)tan^2((pi/2-x)/3)`.                    (9)

For `e=0` and `e=5`, respectively, `F_e(pi/2)=0` and `F_e(0)=0`. For
`e=1,3,4`, respectively,

`F_1(pi/2)=2,   F_3(0)=2,   F_4(0)=1`.

Finally, `F_2(0)=3`, but

`F_2'(0)=-8/sqrt(3)<0`.

Thus in the last case `F_2(x)<3` for all sufficiently small positive `x`.
This proves (7) when every length is at least two.

Now suppose that exactly one length is one. It is odd and contributes
`cot^2 x`. Let `e` be the number of even lengths among the other four. Again
by (8),

`Phi(2x)<=Q_e(x):=cot^2 x+2e tan^2(x/2)
              +3(4-e)tan^2((pi/2-x)/3)`.                          (10)

For `e=0,1`, evaluation at `x=pi/2` gives `Q_0(pi/2)=0` and
`Q_1(pi/2)=2`. For `e=2,3`, evaluate at `x=pi/3`. Since
`tan(pi/18)<tan(pi/12)=2-sqrt(3)<1/3`,

`Q_2(pi/3)<1/3+4/3+2/3=7/3`,

`Q_3(pi/3)<1/3+2+1/3=8/3`.

For `e=4`, set `u=tan(x/2)`. Then

`Q_4(x)=1/(4u^2)-1/2+33u^2/4`,

whose minimum over `u>0` is attained at `u^4=1/33` (which lies in the
permitted interval `0<u<=1`) and equals

`(sqrt(33)-1)/2<3`.                                               (11)

Every case gives a strict upper bound below three. This proves the lemma.

## Completion and equality analysis

The five-path core has `L` edges and

`|V(B)|=2+sum_i(l_i-1)=L-3`.

Equations (5) and (7) therefore give the strict estimate

`kappa(B)<L+3`.                                                    (12)

If the attached trees have altogether `t` edges, then (3) gives
`kappa(G)=kappa(B)+t<L+3+t`. Also `|E(G)|=L+t` and
`|V(G)|=L-3+t`. Since `s^+(G)+s^-(G)=tr(A(G)^2)=2|E(G)|`, (2) and
(12) imply

`s^+(G)=2|E(G)|-s^-(G)
       >=2(L+t)-kappa(G)
       >L-3+t=|V(G)|`.

The only structural exclusion is the nonsimple situation in which two or
more paths have length one: those paths would be parallel terminal edges.
Within the simple five-dipole family there is no exceptional length tuple,
no equality case in `min Phi<=3`, no equality case in `kappa(B)<=L+3`, and no
equality case in the final spectral inequality.
