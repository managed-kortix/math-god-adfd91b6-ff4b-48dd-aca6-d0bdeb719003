# Bipartite graphs and a weighted-theta calculation

The elementary bipartite identity below completely supersedes the attachment
budget initially derived later in this note.  The budget calculation is kept
because its supporting-plane method remains relevant for nonbipartite cores.

## Bipartite identity

For every bipartite graph `G`,

`s^+(G)=s^-(G)=|E(G)|`.

Indeed, in a bipartition ordering its adjacency matrix is

`A=[[0,B],[B^T,0]]`.

Its nonzero eigenvalues are the pairs `+sigma_i,-sigma_i`, where the `sigma_i`
are the nonzero singular values of `B`.  Hence

`s^+(G)=sum_i sigma_i^2=tr(BB^T)=|E(G)|`.

Consequently every bipartite graph in Conjecture 1.2 satisfies its conclusion:
if `m>=n+1`, then `s^+(G)=m>=n+1>n`.  In particular, a bipartite theta core
with **arbitrary** rooted-tree attachments has cyclomatic number two, remains
bipartite, and satisfies the exact identity

`s^+(G)=|E(G)|=|V(G)|+1`.

Thus no attachment budget is needed in the bipartite case.  The remainder of
this note records a weaker weighted-core argument that was found first and
illustrates what may transfer when the theta core is nonbipartite.

## Supporting-plane weighted-core theorem

Let `H=Theta(l_1,l_2,l_3)` consist of two branch vertices joined by three
internally vertex-disjoint paths.  Assume `l_1,l_2,l_3` have the same parity,
equivalently `H` is bipartite.  Form a connected graph `G` by attaching rooted
trees at vertices of `H`, and for each core vertex `v` let `t_v` be the number
of neighbors of `v` outside `H`.  If

`sum_v sqrt(deg_H(v) t_v) <= 2`,

then `s^+(G)>=|V(G)|`.

In particular, the conclusion holds if an arbitrary rooted tree is attached
to a single core vertex by one edge.  It also holds if two arbitrary rooted
trees are attached by distinct edges at a single internal vertex of a theta
path and there are no other attachments.

## Proof

Write `A=A(H)`.  The weighted 2-core reduction gives

`s^+(G) >= |G|-|H|+s^+(A-D)`,

where `D=diag(d_v)` and

`d_v=(A^-(T_v))_{vv} <= sqrt(t_v)/2`.

For a real symmetric matrix `X`, put `F(X)=s^+(X)=tr(X_+^2)`.  The variational
identity

`F(X)=max_{Y>=0} [2 tr(XY)-tr(Y^2)]`

follows by projecting `X` onto the positive-semidefinite cone.  Taking
`Y=A_+` as a competitor for `X=A-D` gives

`F(A-D) >= F(A)-2 tr(A_+D)`.

The theta graph has `|E(H)|=|H|+1`.  Since it is bipartite, its spectrum is
symmetric, and therefore

`F(A)=|E(H)|=|H|+1`.

Also `A_+=(|A|+A)/2`; because `A` has zero diagonal,
`2(A_+)_{vv}=|A|_{vv}`.  Hence

`F(A-D) >= |H|+1-sum_v |A|_{vv}d_v`.

For each `v`, Cauchy--Schwarz for the positive matrix `|A|` gives

`|A|_{vv}^2 <= (|A|^2)_{vv}=(A^2)_{vv}=deg_H(v)`.

Combining this with the rooted-tree bound yields

`sum_v |A|_{vv}d_v <= (1/2)sum_v sqrt(deg_H(v)t_v) <=1`.

Thus `F(A-D)>=|H|`, and the weighted-core reduction proves
`s^+(G)>=|G|`.

If there is a single external edge at one core vertex, the budget is at most
`sqrt(3)<2`, since theta degrees are two or three.  If exactly two external
edges meet one internal core vertex, the budget is `sqrt(2*2)=2`.  The shapes
of the trees beyond those root edges are unrestricted.

## Why the attachment budget cannot be omitted

Take `H=Theta(2,2,2)=K_{2,3}` and attach one leaf at each of its five
vertices.  Every rooted penalty equals `1/2`, so `D=I/2`.  Since the spectrum
of `K_{2,3}` is `{sqrt(6),0,0,0,-sqrt(6)}`,

`s^+(A-D)=(sqrt(6)-1/2)^2=25/4-sqrt(6)<5=|H|`.

Even one leaf at each of the two degree-three branch vertices is too much for
the weighted-core target.  The unique positive eigenvalue of the resulting
core matrix is `(sqrt(97)-1)/4`, and hence

`s^+(A-D)=(49-sqrt(97))/8<5`.

These examples do not disprove the original graph conjecture: failure of this
particular gluing lower bound need not mean failure for the full attached
graph.  They do show that pointwise bounds `d_v<=1/2`, or even
`sum_v d_v<=1`, do not by themselves force the weighted-core inequality.
