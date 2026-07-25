# Equality pivot after Liu--Tang--Zhang

## Target

Prove AKMPZ Conjecture 9.2(i): for a connected graph `G` of order `n`,

`s+(G)=n-1` if and only if `G` is a tree.

The reverse implication is immediate because a tree is bipartite and has
`n-1` edges.

## Reduction through the DNN theorem

Write `A=P-B`, where `P=A_+`, `B=A_-`, and put `q=2m-n+1`.  If
`s+=n-1`, then `s-=q`.  Apply Liu--Tang--Zhang Theorem 2.1 to
`M=B o B`.  Its proof gives

`s-^2 <= 4(sum_edges |B_uv|)^2 <= q ||B||_F^2=q s-`.

Both inequalities are equalities.  Therefore `B_uv<=0` on every edge, and
the DNN inequality is tight for `B o B`.

Tracing equality through the folding/cut-vertex/2-connected induction gives
the following exact necessary condition.  For every block `H` of `G`, with
`h=|V(H)|`, `l=|E(H)|`, and `q_H=2l-h+1`,

`B_uv = -q_H/(2l)` for every edge `uv` of `H`.

For a bridge this is `-1/2`.  For every cyclic block it is strictly below
`-1/2`.  The cut-vertex scalar Cauchy equality also normalizes every
descendant equality pair by `T=q_H`.  In a 2-connected descendant, Case 2
of the LTZ proof is strictly incompatible with equality; Case 1 forces the
edge entries to be uniform and gives the displayed constant.

Thus the conjecture is reduced to one structural lemma:

> If the negative spectral part `B=A_-` has the displayed blockwise-constant
> edge entries, every block is a bridge.

Useful simultaneous identities are

`P,B >= 0 (PSD), PB=0, P_vv=B_vv`,

and, on an edge in block `H`, writing `c_H=q_H/(2l)`,

`B_uv=-c_H`, `P_uv=1-c_H`.

Also `AB=-B^2`, `AP=P^2`, hence

`(B^2)_vv=sum_{H contains v} c_H d_H(v)` and

`(P^2)_vv=sum_{H contains v} (1-c_H)d_H(v)`.

The missing lemma survives exhaustive checks through seven vertices.  A
generic claim `B_uv>=-1/2` on edges is false, so the proof must exploit the
simultaneous uniformity on every edge of a block and `PB=0`.

## The square-root formulation and a local obstruction

Put `C=|A|=P+B`.  If `H` is a block, write

`beta_H=l_H-h_H+1` and `k_H=-beta_H/l_H`.

The equality constants give, on every edge `uv` of `H`,

`C_uv=1-2c_H=k_H`.

Thus `C_uv=0` on bridges and `C_uv<0` on the edges of a cyclic block.  Also
`C>=0` and `C^2=A^2`, so

`(C^2)_uv=|N(u) intersect N(v)|` and `(C^2)_vv=d(v)`.

The bipartite case is already impossible.  Indeed, after ordering the two
color classes, `A^2` is block diagonal.  Its principal square root `C` is
block diagonal with the same decomposition, and hence `C_uv=0` on every
edge.  Therefore a cyclic block, for which `beta_H>0`, cannot occur in a
bipartite equality graph.

For the remaining nonbipartite case the following is a rigorous necessary
condition that uses both positivity and the square identity.  It gives a
sharpened obstruction, although it does not yet finish the lemma.

**Local square-root obstruction.**  Let `rho` be the spectral radius of `A`.
For every vertex `v`, define

`R_v=d(v)-sum_{vw in E(G)} k_{H(vw)}^2`.

If the asserted edge values of `C` hold, then for every edge `uv`, putting
`t_uv=|N(u) intersect N(v)|`, one necessarily has

`sqrt(R_u)>=d(u)/rho`,                                      (1)

and

`(k_{H(uv)}-t_uv/rho)^2`
` <= (sqrt(R_u)-d(u)/rho)(sqrt(R_v)-d(v)/rho)`.             (2)

To prove this, all eigenvalues of `C` lie in `[0,rho]`, and therefore

`Q=C-C^2/rho>=0`.

Since the prescribed edge coordinates occur among the coordinates of row
`v` of `C`, the row identity `sum_w C_vw^2=d(v)` gives

`C_vv^2 <= d(v)-sum_{vw in E(G)}C_vw^2=R_v`.

Positivity of `Q` gives `Q_vv=C_vv-d(v)/rho>=0`; this proves (1), as
`C_vv>=0`.  The `u,v` principal minor of `Q` gives

`(C_uv-(C^2)_uv/rho)^2`
` <= (C_uu-d(u)/rho)(C_vv-d(v)/rho)`.

Each factor on the right is nonnegative and is at most the corresponding
factor with `C_xx` replaced by `sqrt(R_x)`.  Substitution of
`C_uv=k_{H(uv)}` and `(C^2)_uv=t_uv` proves (2).

There is a useful coupled version.  If `K` is any clique, form the matrix
`M_K`, indexed by `K`, by

`(M_K)_vv=sqrt(R_v)-d(v)/rho`,

`(M_K)_uv=k_{H(uv)}-t_uv/rho` for distinct `u,v` in `K`.       (3)

Then necessarily `M_K>=0`.  Indeed, the principal matrix `Q[K]` is PSD, its
off-diagonal entries are exactly those in (3), and its diagonal entry at
`v` is `C_vv-d(v)/rho<=sqrt(R_v)-d(v)/rho`.  Hence `M_K` is obtained from
`Q[K]` by adding a nonnegative diagonal matrix.  In particular, testing on
the all-ones vector gives the explicit obstruction

`sum_{v in K}(sqrt(R_v)-d(v)/rho)`
` +2 sum_{uv in E(K)}(k_{H(uv)}-t_uv/rho) >=0`.               (4)

Thus violation of (4), or of any principal minor of (3), rules out the
equality constants simultaneously on the clique.

This criterion is genuinely stronger than applying Cauchy--Schwarz directly
to the rows of `C`, because it removes the Perron endpoint by passing to
`C-C^2/rho`.  It is not by itself universal enough to close the argument.
For example, for the bare 5-cycle it does not contradict the required value
`k=-1/5`: here `rho=2`, `R_v=2-2/25`, and `t_uv=0`, so both (1) and (2) hold.
The actual square root nevertheless has

`|A(C_5)|_uv=(2-sqrt(5))/5 != -1/5`

on an edge.  Consequently any completion along this route must use a
constraint coupling more than one edge (or an equality/compatibility
condition omitted by the individual `2 by 2` Schur complements); no
edgewise PSD-minor argument of the form (1)--(2) alone can prove the missing
lemma.

## Research protocol

This is now the sole primary proof object.  New agents, if used, receive this
file and the literature audit.  One proof line is active at a time; after a
lemma is merged, one hostile audit attacks it.  Broad swarms are reserved for
separable finite cases or falsification, not for the coupled equality proof.
