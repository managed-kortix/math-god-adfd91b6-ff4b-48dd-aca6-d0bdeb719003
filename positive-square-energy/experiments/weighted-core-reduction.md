# Weighted 2-core reduction for sparse bicyclic graphs

This note records an exact reduction suggested by the gluing lemma in
arXiv:2506.07264v1.  It is a route toward Conjecture 1.2, not a proof of the
conjecture.

## Proposition

Let `G` be a connected graph, let `C` be its 2-core, and suppose every
component of `G-V(C)` is a tree attached to exactly one vertex of `C` (as is
automatic when `C` is the 2-core).  For each `v in V(C)`, let `T_v` be the
induced rooted tree consisting of `v` and all vertices outside `C` whose unique
path to `C` first meets `C` at `v`.  Put

`d_v=(A^-(T_v))_{v,v}`

when `T_v` is nontrivial, and put `d_v=0` otherwise.  If

`Gamma=A(C)-diag(d_v : v in V(C))`,

then

`s^+(G) >= |V(G)|-|V(C)|+s^+(Gamma)`.

Consequently, the weighted-core inequality `s^+(Gamma)>=|V(C)|` implies
`s^+(G)>=|V(G)|`.

## Proof

Take `C` as the base graph in the gluing lemma and glue the rooted trees
`(T_v,v)` at their distinct roots.  Since a tree is bipartite and has
`|E(T_v)|=|V(T_v)|-1`, its positive and negative square energies are equal and

`s^+(T_v)=|V(T_v)|-1`.

The gluing lemma therefore gives

`s^+(G) >= sum_v (|V(T_v)|-1)+s^+(Gamma)`.

The sets `V(T_v)-{v}` partition `V(G)-V(C)`, so the sum is
`|V(G)|-|V(C)|`, proving the claim.

## A sharp local bound on the diagonal penalties

If the root has degree `t` inside `T_v`, then

`0 <= d_v <= sqrt(t)/2`.

Indeed `A^-= (|A|-A)/2`, and the adjacency matrix has zero diagonal, so
`d_v=|A|_{v,v}/2`.  Apply Jensen's inequality to the spectral measure of the
positive matrix `A^2` at the unit vector `e_v`:

`|A|_{v,v}=<e_v,sqrt(A^2)e_v> <= sqrt(<e_v,A^2e_v>)=sqrt(t)`.

The bound is sharp: for the star `K_{1,t}` rooted at its center, the spectral
measure at the center assigns mass `1/2` to each of `+sqrt(t)` and
`-sqrt(t)`, hence `d_v=sqrt(t)/2`.

In particular, a single pendant branch at a core vertex contributes a penalty
at most `1/2`.  No universal bound `d_v<1` is possible when arbitrarily many
branches meet the same core vertex.

## Sparse bicyclic specialization

When `G` is connected with `|E(G)|=|V(G)|+1`, its cyclomatic number is two.
Cyclomatic number is additive over blocks.  Thus its 2-core has either two
unicyclic blocks (cycles joined through the block-cut tree) or one
2-connected bicyclic block.  In the latter case, suppressing degree-two
vertices gives a theta kernel: two branch vertices joined by three internally
disjoint paths.  The proposition reduces the entire sparse frontier to
weighted cycle-pair and weighted-theta inequalities, with the diagonal weights
constrained by rooted-tree spectral measures.

This formulation also explains why deleting pendant trees one vertex at a
time is too lossy: the exact composable datum is the rooted diagonal
`(A^-(T))_{v,v}`, not merely the unrooted deficit `s^+(T)-|T|=-1`.

## Verification cautions

1. The proposition does not assert that `s^+(A(C)-diag(d_v))>=|C|` for
   arbitrary nonnegative `d_v`; rooted-tree origin matters.
2. Adding an edge is not known to increase `s^+`, so a proof on the sparse
   frontier cannot simply be promoted to all denser graphs.
3. The theta statement concerns the unique 2-connected bicyclic block after
   separating cyclic blocks at cut vertices; a figure-eight has two cyclic
   blocks and belongs to the first case.
