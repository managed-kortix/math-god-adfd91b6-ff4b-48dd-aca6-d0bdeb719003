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

## Research protocol

This is now the sole primary proof object.  New agents, if used, receive this
file and the literature audit.  One proof line is active at a time; after a
lemma is merged, one hostile audit attacks it.  Broad swarms are reserved for
separable finite cases or falsification, not for the coupled equality proof.
