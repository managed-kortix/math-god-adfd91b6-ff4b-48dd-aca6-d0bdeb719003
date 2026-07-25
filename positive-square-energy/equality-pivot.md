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

More explicitly, first fold every nonedge entry of `M=B o B` onto the
diagonal as in LTZ.  Folding preserves the edge entries, `S`, and
`T=1^T M 1`, but its diagonal is no longer simply `B_vv^2`; subsequent
diagonal quantities in this equality trace refer to the folded matrix.  At a
cut vertex, LTZ constructs two Gram matrices satisfying

`q=q_1+q_2`, `S=S_1+S_2`, and `T=T_1+T_2`.

Equality in both induction bounds and scalar Cauchy--Schwarz forces
`T_1/q_1=T_2/q_2=T/q=1`, so each descendant remains normalized by
`T_i=q_i`.  A no-cut descendant of order at least three is 2-connected and
has positive cyclomatic number.  LTZ Case 2 uses a strict hypothesis and
therefore yields a strict final inequality, so equality must lie in Case 1.
Equality in the flat edge Cauchy--Schwarz estimate makes every edge entry of
the folded matrix equal to `r`.  Since

`4(l sqrt(r))^2=q_H T_H=q_H^2`,

we have `sqrt(r)=q_H/(2l)`.  Folding preserved edge entries, while equality
in the preceding absolute-value step gave `B_uv<=0`; this proves (27).

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

## Negative spectral Gram reduction for one 2-connected block

Assume now that the whole graph is 2-connected. Thus every edge has the
same value

`B_uv=-c`, where `c=(2m-n+1)/(2m)` and `c>1/2`.                 (5)

Factor `B=XX^T` with `X` of full column rank, denote its row vectors by
`x_v`, and put `S=X^T X`. The matrix `S` is positive definite. The identity
`AB=-B^2` does not merely give scalar quadratic constraints: it gives the
exact vector equations

`S x_v=-sum_{u~v}x_u` for every `v`.                           (6)

Indeed, `AB=-B^2` says `(AX+XS)X^T=0`; multiplication on the right by
`X S^{-1}` gives `AX=-XS`. Moreover,

`x_v^T S x_v=(B^2)_vv=c d(v)`,                                (7)

`sum_v x_v x_v^T=S`, and `tr(S^2)=2mc=2m-n+1`.                (8)

These identities expose exactly what the elementary incidence argument can
and cannot prove. Let `R` be the unsigned vertex-edge incidence matrix,
let `D` be any oriented incidence matrix, and set

`H=sum_v d(v)x_v x_v^T=X^T Deg X`.

Using (6), hence `X^TAX=-S^2`, gives the matrix identities

`sum_{uv in E}(x_u+x_v)(x_u+x_v)^T=X^T RR^T X=H-S^2>=0`,      (9)

`sum_{uv in E}(x_u-x_v)(x_u-x_v)^T=X^T DD^T X=H+S^2>=0`.     (10)

Writing `a_v=||x_v||^2` and `T=sum_v d(v)a_v`, their traces are

`sum_{uv in E}||x_u+x_v||^2=T-2mc=T-(2m-n+1)`,               (11)

`sum_{uv in E}||x_u-x_v||^2=T+2mc=T+(2m-n+1)`.               (12)

Thus incidence positivity supplies only `T>=2mc`. Equality in this bound
has a precise characterization: `x_u=-x_v` on every edge. Since the graph
is connected and every edge inner product is nonzero, this forces a
bipartition. In the present nonbipartite case the inequality is strict, not
reversed. Consequently (9)--(12) do **not** yield the hoped-for upper bound
`2mc<=m`, or `c<=1/2`.

There is a second exact constraint, obtained by retaining all coordinates in
the row norm of `B`. From (7),

`sum_{w notin N(v), w!=v} B_vw^2=c(1-c)d(v)-a_v^2`.           (13)

In particular,

`a_v^2<=c(1-c)d(v)`, and `a_u a_v>=c^2` on every edge.        (14)

The second inequality is the edge principal minor of `B`. Around a cycle
`v_1...v_kv_1`, (14) gives the necessary condition

`(c/(1-c))^k<=product_i d(v_i)`.                              (15)

This is too weak even for a bare cycle: its right side is `2^k`, whereas
`c/(1-c)=(n+1)/(n-1)<=2` (with equality for the triangle). Nor can a cycle
Gram determinant using only the
fixed edge entries prove `c<=1/2`. For example, on a triangle the partial
Gram data with diagonal `2c` and off-diagonal `-c` form the PSD matrix
`c(3I-J)` for every `c>0`. This example does not satisfy (6) unless
`3c=1`: here the nonzero eigenvalue of its Gram matrix is `3c`, while the
sum of the other two vectors is `-x_v`. Hence it rigorously isolates (6),
rather than cyclewise Gram positivity, as the indispensable constraint.

Finally, summing the squared equations (6) gives a coupled identity that
does use this constraint. If `t_uw=|N(u) intersect N(w)|` and `tau` is the
number of triangles, then

`tr(S^3)=sum_v d(v)a_v-6c tau`
`          +2 sum_{uw notin E, u<w} t_uw B_uw`.               (16)

Indeed, the left side is `sum_v||Sx_v||^2`; expanding the neighbor sums on
the right counts each pair `u,w` exactly `t_uw` times, and
`sum_{uw in E}t_uw=3 tau`. Formula (13) controls the unweighted square sum
of the unknown terms in (16):

`sum_{uw notin E, u<w}B_uw^2`
` = (1/2)sum_v(c(1-c)d(v)-a_v^2)`.                            (17)

The exact remaining gap in the 2-connected case is to combine the sign and
weight pattern in (16) with (9), (13), and the spectral moments in (8) so as
to contradict `c>1/2`. A direct Cauchy--Schwarz estimate on the last sum in
(16) loses the common-neighbor weights and has no universal sign, while
(11) has the wrong direction. Thus the negative Gram attack reduces the
problem to the weighted nonedge correlation in (16); no claimed
`c<=1/2` inequality follows from incidence traces or cycle minors alone.

## Research protocol

This is now the sole primary proof object.  New agents, if used, receive this
file and the literature audit.  One proof line is active at a time; after a
lemma is merged, one hostile audit attacks it.  Broad swarms are reserved for
separable finite cases or falsification, not for the coupled equality proof.
