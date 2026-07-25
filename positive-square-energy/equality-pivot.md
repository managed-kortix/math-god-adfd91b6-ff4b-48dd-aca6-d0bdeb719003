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

## The folded trace and the omitted averaged constraint

Assume first that the whole equality graph is 2-connected, and abbreviate

`q=2m-n+1`, `c=q/(2m)`, `a_v=B_vv`.

Thus `B_uv=-c` on every edge.  Let `N` be the matrix obtained by folding all
nonedges of `M=B o B`, and let `d0=tr N`.  Exactly, not just as an
inequality,

`d0=sum_v a_v^2+2 sum_{nonedges u<v}B_uv^2`.                  (13)

The diagonal equation `(PB)_vv=0`, using `P_vv=B_vv`,
`(P_uv,B_uv)=(1-c,-c)` on edges, and `P_uv=B_uv` on nonedges,
is

`sum_{w notin N(v), w!=v}B_vw^2=c(1-c)d(v)-a_v^2`.           (14)

Summing (14) and substituting in (13) gives the exact folded trace

`d0=2mc(1-c)`.                                                (15)

On the other hand, equality in LTZ Case 1 includes equality at its threshold

`2(n-1)w=q d0`,

where `w=sum_edges N_uv=mc^2`.  Since `q=2mc`, this says

`d0=(n-1)c`.                                                  (16)

Equations (15) and (16) are the same identity: after cancelling `c>0`, they
reduce to

`2m(1-c)=n-1`,

which is precisely `c=(2m-n+1)/(2m)`.  Thus the threshold equality contains
no new information beyond `PB=0`, (14), and the already known value of `c`.

There is nevertheless an omitted condition.  Although Case 1 proves the
theorem using only the flat estimate, the LTZ averaged estimate remains
valid independently:

`4S^2 <= (q-1)T+(q-1)d0/(n-2)`.                              (17)

Here DNN equality gives `4S^2=qT`, while `T=q` and (16) holds.  Comparing
with (17) yields

`d0 >= (n-2)T/(q-1)`,

and hence

`(n-1)q/(q+n-1) >= (n-2)q/(q-1)`,

because `c=q/(q+n-1)`.  Cancelling `q` and cross-multiplying gives

`q >= (n-1)^2`.                                               (18)

Simplicity gives the reverse inequality

`q=2m-n+1 <= n(n-1)-n+1=(n-1)^2`.

Consequently equality forces `q=(n-1)^2` and `m=n(n-1)/2`, so the
2-connected graph is complete.  But for `n>=3`,

`s+(K_n)=(n-1)^2 != n-1`.

This rules out a 2-connected equality graph.  Equivalently, one can obtain
the final contradiction internally from (14): completeness and
`c=(n-1)/n` give `a_v=c` for every `v`, so `B` would have diagonal `c` and
every off-diagonal entry `-c`; its all-ones eigenvalue is `c(2-n)<0`,
contrary to `B>=0`.

The same comparison applies to every 2-connected descendant in the LTZ
cut-vertex induction, because that descendant is tight, has `T=q`, and is
at the Case 1 threshold.  It follows that every cyclic block in a putative
equality graph must be a complete block.  The argument above rules it out
when that block is the whole graph; in the presence of cut vertices the
descendant Gram matrix has a redistributed cut-vertex diagonal and need not
be the Hadamard square of the corresponding principal submatrix of `B`.
There is a further exact PSD equality.  For a complete block on `h` vertices,
put `c=(h-1)/h`.  Its descendant matrix has every off-diagonal entry `c^2`,
and

`d0=(h-1)c=h c^2`.

If its diagonal entries are `c^2 b_1,...,c^2 b_h`, positive semidefiniteness
gives `b_i b_j>=1` for every `i!=j`, while their sum is `h`.  These conditions
force every `b_i=1`: if one were below one, all the others would be at least
its reciprocal and the sum would exceed `h`; if none were below one, the
sum settles the claim.  Hence the complete-block descendant is exactly

`c^2 J_h`.                                                     (19)

In any Gram representation all of its vectors therefore coincide.  This
already rules out a cyclic leaf block.  Indeed, let `H=K_h` be a leaf block,
with unique cut vertex `t`.  The LTZ split leaves the folded vectors `y_u`
unchanged for `u in H-{t}`, so (19) gives `y_u=y_v` there.  Projecting to the
original tensor coordinates gives

`x_u tensor x_u=x_v tensor x_v`.

Since `B_uv=-c`, this means `x_v=-x_u` and `||x_u||^2=c`.  If `h>=4`, three
vertices in `H-{t}` would be represented by pairwise opposite nonzero
vectors, an impossibility.  If `h=3`, write the two noncut vertices as
`u,v`.  The global equations `Sx_r=-sum_{s~r}x_s` give, using `x_v=-x_u`,

`Sx_u=x_u-x_t` and `Sx_u=x_u+x_t`.

Thus `x_t=0`, contradicting `B_ut=-c`.  Therefore every leaf block is a
bridge.  The exact remaining reduction is now: exclude an internal complete
cyclic block when all leaves of the block-cut tree are bridges.  At such an
internal block, repeated LTZ projections can alter every cut-vertex vector,
so (19) does not immediately identify two of the original tensor vectors.

## Folded Gram vectors

The folding itself contributes no further equality condition.  If
`B=XX^T`, with row vectors `x_v`, then

`z_v=x_v tensor x_v`

is a Gram representation of `M=B o B`.  Orient each nonedge `e={u,v}` and
give it a new coordinate orthogonal to all old and other new coordinates.
Define

`y_v=z_v direct-sum (alpha_{v,e})_e`,

where `alpha_{u,e}=sqrt(M_uv)`, `alpha_{v,e}=-sqrt(M_uv)`, and all other
entries in coordinate `e` vanish.  Then `Gram(y_v)=N`: on the nonedge
`uv`, the new coordinate contributes `-M_uv` and cancels the old inner
product; on an edge nothing changes; and each endpoint receives `M_uv` on
its diagonal.  Also

`sum_v y_v=(sum_v z_v) direct-sum 0`,

so folding preserves `T`.  Signed coordinates are harmless: entrywise
nonnegativity concerns the resulting inner products, and these are zero on
nonedges and unchanged nonnegative values elsewhere.  Hence there is no
incompatibility and no hidden Cauchy--Schwarz equality in the folding step.
The genuinely additional restrictions are the unused deletion estimate
(17), which forces completeness, and then PSD equality (19), which forces
the complete-block descendant to have rank one.

## Recursive deletion equality gives no contradiction

The equality in the averaged estimate is indeed forced once a 2-connected
descendant has been shown to be complete, but all of its deletion pairs are
again equality pairs.  Let the descendant be `K_h` and write its matrix as

`X=c^2 J_h`, where `c=(h-1)/h`.

Then

`S=binom(h,2)c`, `T=h^2c^2`, and `q=(h-1)^2`,

so

`4S^2=h^2(h-1)^2c^2=qT`.

Also `d0=hc^2`, `q-1=h(h-2)`, and the right-hand side of the
averaged estimate is exactly

```
(q-1)T+(q-1)d0/(h-2)
=h(h-2)h^2c^2+h^2c^2
=h^2(h-1)^2c^2
=qT.
```

Thus every inequality used to derive the averaged estimate is tight.  For
each vertex deletion, put `r=h-1`.  The deletion pair is

`(K_r,c^2J_r)`,

with the same scalar `c`, not the canonical normalization `(r-1)/r`.
Homogeneity is essential here.  Directly,

`S'=binom(r,2)c`, `T'=r^2c^2`, and `q'=(r-1)^2`,

and hence

`4(S')^2=r^2(r-1)^2c^2=q'T'`.

This recurses down to `K_2`; every nonzero scalar multiple of `J_2` is an
equality matrix in the base case.  Consequently, recursive equality in all
deletions supplies no contradiction and no condition beyond the rank-one
complete-block form already obtained in (19).

In fact, for a connected graph with at least one edge, this calculation
completes the abstract equality classification for the folded LTZ
inequality.  For each block `C`, let

`q_C=2|E(C)|-|V(C)|+1`.

Apart from the zero matrix, equality holds precisely when the folded matrix
has the form

`N=lambda sum_C (q_C/|C|^2) J_{V(C)}`, with `lambda>0`,              (19a)

and every block is either a bridge or a complete graph.  Necessity follows
recursively: cut-vertex Cauchy equality gives the common ratio
`T_C/q_C=lambda`; a terminal no-cut descendant must be complete; and its
flat, threshold, and PSD equalities give
`N_C=(lambda q_C/|C|^2)J_C`.  Recombining the orthogonal cut decomposition
adds these embedded block matrices.  Conversely, (19a) is doubly
nonnegative and

`2S=sqrt(lambda) sum_C q_C=sqrt(lambda)q`,

`T=lambda sum_C q_C=lambda q`,

so `4S^2=qT`.  For a bridge its coefficient is `lambda/4`; for
`C=K_h` it is `lambda(h-1)^2/h^2`.  The original, not necessarily
edge-supported matrix `M` is an equality matrix exactly when its LTZ fold
has this form.  In the spectral normalization used here `lambda=1`, so
(19a) is exactly the already known global block-atom matrix.  The full
recursive deletion equality therefore yields no further spectral
information.

## The global atom projection and its exact limitation

There is a useful global formulation, but it does not put the individual
block atoms in the PSD cone.  For each block `C`, set

`a_C=c_C e_C`,

where the `e_C` are orthonormal, `c_C=1/2` for a bridge, and
`c_C=(h-1)/h` for a complete block of order `h`.  Thus

`eta_v=sum_{C containing v}a_C`,

and the globally folded Gram matrix is

`N=sum_C c_C^2 J_{V(C)}`.

Identify `span{eta_v}` isometrically with the span of the explicit folded
vectors `y_v=z_v direct-sum f_v`, where `z_v=x_v tensor x_v`, and let `Q`
be orthogonal projection onto the original symmetric-tensor coordinates.
Put

`p_C=Q a_C`, `r_C=(I-Q)a_C`.

Then

`Z_v:=x_v tensor x_v=sum_{C containing v}p_C`.                 (20)

The total canonical vector is

`g=sum_v eta_v=sum_C |C|a_C`.

For a bridge, `|C|^2 c_C^2=1=q_C`; for `C=K_h`,
`|C|^2c_C^2=(h-1)^2=q_C`.  Hence `||g||^2=sum_C q_C=q`.  Its
projection is

`Qg=sum_v Z_v=sum_v x_v tensor x_v=S=X^T X`.

Since `||S||_F^2=tr(S^2)=tr(B^2)=s-=q`, equality in the contraction
`||Qg||<=||g||` gives exactly

`g in ran Q`, equivalently `sum_C |C|r_C=0`.                   (21)

Consequently

`<p_C,S>=<a_C,g>=|C|c_C^2`.                                  (22)

More generally, orthogonality of the two projection components gives the
complete pairwise bookkeeping identity

`<p_C,p_D>=delta_{CD}c_C^2-<r_C,r_D>`,                        (23)

with `sum_C |C|r_C=0`.  Thus (22) is the weighted row sum of (23).  Norm
preservation of `g` supplies no assertion that any one `r_C` vanishes and
no pairwise orthogonality of distinct `p_C`'s.

In fact, `p_C>=0` is false even for the exact equality geometry.  The path
`P_4` is a counterexample.  Its negative spectral part is

```
B = [ sqrt(5)/5,   -1/2,       sqrt(5)/10,  0;
      -1/2,         3sqrt(5)/10,-1/2,       sqrt(5)/10;
       sqrt(5)/10, -1/2,        3sqrt(5)/10,-1/2;
       0,            sqrt(5)/10,-1/2,       sqrt(5)/5 ].
```

Here every edge entry is `-1/2`.  Folding the nonedges of `B o B` gives

`N=(1/4)(J_{12}+J_{23}+J_{34})`,

because its diagonal is `(1/4,1/2,1/2,1/4)` and its edge entries are all
`1/4`.  Thus this is precisely the global block-atom model with three
bridge atoms.  Let `B=XX^T` and `Z_i=x_i tensor x_i`.  The endpoint
incidence equations and (20) force

`p_{12}=Z_1`, `p_{23}=Z_2-Z_1`, `p_{34}=Z_4`.

The vectors `x_1,x_2` are linearly independent, since their Gram
determinant is

`B_11 B_22-B_12^2=1/20>0`.

Therefore `p_{23}=x_2 x_2^T-x_1 x_1^T` is indefinite: on
`span{x_1,x_2}` the difference of the two independent rank-one PSD forms
has one positive and one negative eigenvalue.  Nevertheless `S=X^T X` is
positive definite on this span, (21) holds, and (22) gives

`<p_{23},S>=1/2>0`.

This also pinpoints the failure of leaf peeling.  A leaf bridge atom is
indeed `Z_leaf` and is PSD, but deleting it replaces the rank-one tensor at
its neighbor by `Z_neighbor-Z_leaf`; in `P_4` this is exactly the
indefinite middle atom.  Hence neither positivity nor rank one is preserved
by the peeling operation.  The norm equality for `g`, even together with
all rank-one PSD incidence sums (20) and a positive-definite total `S`,
cannot support the proposed convex-cone argument.  Any continuation must
use an additional condition specific to complete cyclic blocks; it cannot
deduce that condition from the global projection geometry alone.

## Research protocol

This is now the sole primary proof object.  New agents, if used, receive this
file and the literature audit.  One proof line is active at a time; after a
lemma is merged, one hostile audit attacks it.  Broad swarms are reserved for
separable finite cases or falsification, not for the coupled equality proof.
