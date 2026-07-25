# Spanning-bicyclic positive-subspace compression

## Purpose

The bare connected bicyclic frontier of the positive square-energy conjecture
is proved. A universal edge-monotonicity argument is unavailable: positive
square energy can decrease when an edge is added, and the disconnected
threshold-preservation statement is false. This note records an exact
multi-edge variational certificate that promotes a spanning bicyclic subgraph
without adding its omitted edges one at a time.

## Compression theorem

Let `A,C` be real symmetric matrices. Put `P=A_+`, and let `Pi` be the
orthogonal projector onto the positive spectral subspace `S=ran(Pi)` of `A`.
Regard `K=Pi C Pi` as an operator on `S` (or extend it by zero on `S^perp`).
Then

`s+(A+C) >= s+(A)+2 tr(CP)+s+(K)`.                         (1)

Indeed, the variational identity

`s+(M)=max_{Y>=0} (2 tr(MY)-tr(Y^2))`

allows the witness `Y=P+K_+`. This is positive semidefinite. Expanding the
objective gives

```
2 tr((A+C)(P+K_+))-tr((P+K_+)^2)
=s+(A)+2 tr(CP)
 +2 tr(AK_+)-2 tr(PK_+)
 +2 tr(CK_+)-tr(K_+^2).
```

Because `K_+=Pi K_+ Pi` and `A Pi=P`, the middle two terms cancel. Also
`tr(CK_+)=tr(KK_+)`. The last line is therefore `s+(K)`, proving (1).
No commutativity between `P` and `K_+` is used.

## Graph specialization

Let `H` be a spanning subgraph of `G`, put `A=A(H)`, and let `C` be the
adjacency matrix of the omitted edges. Then

`s+(G) >= s+(H)+4 sum_{uv in E(G)\E(H)} P_uv+s+(Pi C Pi)`.   (2)

Every connected graph with at least `n+1` edges has a spanning connected
bicyclic subgraph: retain a spanning tree and any two remaining edges. The
proved bare theorem gives `s+(H)>=n` for each such `H`. Consequently AKMPZ
holds for `G` as soon as one spanning bicyclic `H` satisfies

`s+(H)-n+4 sum_omitted P_uv+s+(Pi C Pi)>=0`.                 (3)

In particular, a basis with nonnegative aggregate omitted-edge correlation
proves the result without using the compression refund.

The unresolved class for (2), not a claimed counterexample class to AKMPZ,
consists of connected `G` for which every spanning connected bicyclic `H`
satisfies the strict reverse of (3). Thus every such basis must have negative
aggregate chord correlation large enough to overwhelm both the proved bare
surplus and the nonnegative positive-compression refund.

## One-edge convexity and local correction

For `E=E_uv` and `f(t)=s+(A+tE)`, the variational formula shows that `f` is
convex, because it is a supremum of affine functions of `t`. It is `C^1` and

`f'(t)=4 (A+tE)_+,uv`.                                      (4)

Hence the positive-part entry along the path is nondecreasing, but `f` need
not be monotone: the connected graph `D` with graph6 `HQzV]zn` has an exact
edge addition that decreases `s+`. The tangent certificate is

`s+(A+E)>=s+(A)+4P_uv`.                                     (5)

There is also an exact negative-part correction. Write `N=A_-`. Testing
`Y=P+s yy^T`, `s>=0`, and optimizing `s` gives

`s+(A+tE) >= s+(A)+4tP_uv`
` +(t y^T E y-y^T N y)_+^2/||y||^4`.                       (6)

For `y=e_u+e_v`, this becomes

`s+(A+tE) >= s+(A)+4tP_uv`
` +(2t-N_uu-N_vv-2N_uv)_+^2/4`.                            (7)

This strengthens the tangent bound in suitable cases. It does not yet prove
universal connected threshold preservation because simultaneous control of
the positive and negative local terms is missing.

## Hostile audit and next attack

An independent audit expanded every cross term in (1), checked noncommuting
low-dimensional examples, and found the theorem valid for arbitrary real
symmetric `A,C`. It also confirmed convexity and warned against treating a
graph edge as a positive rank-one perturbation: `E_uv` is rank two and
indefinite.

Next, search over spanning bicyclic bases of low-surplus connected graphs and
measure the exact certificate (3). If every tested graph has a nonnegative
basis, seek an exchange theorem on the cycle matroid maximizing aggregate
correlation plus compression refund. In parallel, derive structural formulas
for (3) on theta, dumbbell, and handcuff bases with multiple omitted chords.
