# A P3-removal theorem for nonbipartite theta graphs

Let `Theta(a,b,c)` denote the simple graph formed by three internally
vertex-disjoint paths of edge-lengths `a,b,c` between the same two branch
vertices.  Its order is `n=a+b+c-1` and its size is `n+1`.

## Theorem

Suppose `Theta(a,b,c)` is nonbipartite.  Relabel the paths so that

`a == b (mod 2)` and `c != a (mod 2)`.

If `c>=4`, then

`s^+(Theta(a,b,c)) >= n+1/16 > n`.

Thus Conjecture 1.2 holds strictly for every theta graph whose unique
singleton-parity path has length at least four.

## Proof

Write the `c`-path as

`v_0 v_1 ... v_c`,

with the branch vertices at `v_0,v_c`.  Since `c>=4`, the three vertices
`v_1,v_2,v_3` exist and induce a `P_3`.  There is no chord among them because
an internal theta-path vertex has only its two consecutive path neighbors.

The improved `P_3`-removal lemma (Lemma 2.4 of arXiv:2506.07264v1) says that
for some `u` among these three vertices,

`s^+(G) >= s^+(G-u)+17/16`.

The choice of `u` is existential, so all three deletions must be checked.
Every one of `v_1,v_2,v_3` has degree two.  Deleting any one breaks the
`c`-path into at most two pendant path pieces, while the other two theta paths
remain and form the unique cycle `C_{a+b}`.  The deletion is therefore
connected and unicyclic.  Since `a+b` is even, it is bipartite.  It has `n-1`
vertices and `n-1` edges, whence bipartite spectral symmetry gives

`s^+(G-u)=|E(G-u)|=n-1`.

Consequently

`s^+(G) >= n-1+17/16=n+1/16`.

## Exact residual families

The theorem leaves exactly the following nonbipartite theta families after
the singleton-parity path has been distinguished:

* `Theta(2r,2s,1)`;
* `Theta(2r+1,2s+1,2)`;
* `Theta(2r,2s,3)`.

This is a reduction, not a proof for those families.  In the third family the
short path has only two internal vertices.  Although an endpoint together
with them induces a `P_3`, the removal lemma may select the branch endpoint;
that deletion is a forest and loses one additional unit, so the quantifier
cannot be ignored.

## Triangle subclass by induced partition

A separate exact argument settles many short-path cases.  If a theta graph
contains an induced triangle `K` and `G-V(K)` is connected, then

`s^+(G)>=|G|`.

Indeed `G-V(K)` is a tree, `s^+(K_3)=4`, and a tree `T` has
`s^+(T)=|T|-1`.  Superadditivity on the two disjoint induced subgraphs gives

`s^+(G)>=4+(|G|-3-1)=|G|`.

More generally, if `G-V(K)` is a forest with `q` nonempty components, the
same proof gives `s^+(G)>=|G|+1-q`.  For a bare theta containing a triangle,
the complement of that triangle is the connected interior of the third path,
so every such theta is settled.

## Verification cautions

1. Path lengths count edges.  A path of length four has three internal
   vertices.
2. The `P_3`-removal lemma chooses the deleted vertex; one cannot prescribe
   its middle vertex.
3. The proof above is for the bare theta.  With rooted trees attached to the
   selected three vertices, deletion can disconnect an attachment and the
   bipartite-unicyclic calculation no longer follows.
4. The result is strict but does not settle all nonbipartite theta graphs.
