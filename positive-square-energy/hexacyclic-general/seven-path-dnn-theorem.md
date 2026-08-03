# The seven-path rank-six block

## Theorem

Let `B` be the union of seven internally vertex-disjoint paths with common
terminals `a,b` and positive integer lengths `l_1,...,l_7`. Suppose that `B`
is simple, equivalently that at most one `l_i` equals one. Then

`kappa(B)<|E(B)|+5`.

Consequently, if `G` is obtained from `B` by attaching arbitrary rooted trees
at arbitrary vertices, then `s^+(G)>|V(G)|`.

## Exact path elimination

The correlation dual is

`kappa(H)=min {sum_{uv in E(H)} 2/(1-C_uv) : C psd, C_vv=1}`.

Fix `C_ab=cos(theta)`, with `0<=theta<=pi`. Alternating signs along each path,
applying the spherical triangle inequality and strict convexity of
`sec^2(t/2)`, and realizing equality by equally spaced vectors on a common
planar arc gives

`kappa(B)=L+min_{0<=theta<=pi} Phi(theta)`,

where `L=sum_i l_i` and

`Phi(theta)=sum_{l_i even} l_i tan^2(theta/(2l_i))`
`           +sum_{l_i odd} l_i tan^2((pi-theta)/(2l_i))`.

For completeness, if `h_s(y)=s tan^2(y/s)`, then for `s>=2` and
`0<y<=pi/2`,

`d h_s(y)/ds=tan(z)sec^2(z)(sin(z)cos(z)-2z)<0`, `z=y/s`.

Thus an even length may be replaced by two and an odd length greater than one
by three when seeking an upper bound.

## Seven-term tangent lemma

Put `x=theta/2`. First suppose no length is one, and let `e` be the number of
even lengths. Then

`Phi(2x)<=F_e(x)=2e tan^2(x/2)+3(7-e)tan^2((pi/2-x)/3)`.

The two endpoints give

`F_e(pi/2)=2e`, and `F_e(0)=7-e`.

For `e=0,1,2`, use `x=pi/2`, obtaining `0,2,4`. For `e=3,...,7`, use
`x=0`, obtaining `4,3,2,1,0`. Every value is strictly below five.

Now suppose exactly one length is one. It is odd. Let `e` be the number of
even lengths among the other six. Then

`Phi(2x)<=Q_e(x)=cot^2(x)+2e tan^2(x/2)`
`                 +3(6-e)tan^2((pi/2-x)/3)`.

For `e=0,1,2`, the endpoint `x=pi/2` gives `0,2,4`. For `e=3,...,6`, use
`x=pi/3`. Since `3 tan^2(pi/18)<1/3`,

`Q_e(pi/3)<1/3+2e/3+(6-e)/3=(7+e)/3<=13/3<5`.

This exhausts all parity counts and proves `min Phi<5`.

## Completion

The core has `L` edges and `L-5` vertices. Hence

`kappa(B)<L+5`.

The DNN estimate `s^-(H)<=kappa(H)`, one-vertex-sum additivity of `kappa`, and
`kappa(T)=|E(T)|` for a tree show that attaching trees with `t` total edges
gives

`s^+(G)>=2(L+t)-kappa(G)>L-5+t=|V(G)|`.

The strict inequalities above also cover endpoint witnesses: no appeal to an
unattained limiting correlation matrix is needed.
