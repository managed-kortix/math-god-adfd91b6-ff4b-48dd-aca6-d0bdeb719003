# Beta-five block graphs with cyclic blocks `K4, K3, K3`

## Result

Let `G` be a connected block graph whose cyclic blocks are one copy `Q` of
`K4` and two copies `T1,T2` of `K3`, with every other block a bridge. Then

\[
s^+(G)>|V(G)|.
\]

This includes arbitrary trees attached at arbitrary vertices. Together with
the already established bridge separation of distinct cyclic clusters, this
settles the `K4+2K3` case at cyclomatic rank five.

In fact the one-cluster argument below proves the stronger uniform estimate

\[
s^+(G)>|V(G)|+1.                                        \tag{0}
\]

The block contributions are `3+1+1=5`, so if `n=|V(G)|`, then

\[
|E(G)|=n-1+5=n+4.                                      \tag{1}
\]

## Tools used

We use the following previously proved facts.

1. If `H1,...,Hr` are pairwise disjoint induced subgraphs of `G`, then
   \[
   s^+(G)\geq \sum_j s^+(H_j).                         \tag{2}
   \]
2. A connected block graph consisting of one triangle and bridges satisfies
   `s^+(H)>|V(H)|` (the triangular unicyclic theorem).
3. Connected block graphs of cyclomatic rank two and three satisfy
   `s^+(H)>|V(H)|`. In particular, this applies respectively to two
   triangular blocks, and to one `K4`, with arbitrary bridge trees.
4. In the normalized Sachs expansion
   \[
   \Psi_G(t)=\sum_{\mathcal C}
      \left(\prod_{C\in\mathcal C}q_{|C|}\right)
      Z_{G-V(\mathcal C)}(t),
   \qquad q_3=-2i,\quad q_4=-2,
   \]
   every carrier `Z_H(t)` is positive for `t>0`. If
   `Im Psi_G(t)<0` for every `t>0`, the continuous-argument/Coulson theorem
   gives `s^+(G)>s^-(G)`.

No domination-number theorem is needed. In a bouquet the common cut vertex
dominates the vertices of the three clique blocks, but it need not dominate
vertices at distance at least two in attached trees, so global domination one
is not available.

## Exhaustive one-cluster classification

Assume the three cyclic blocks form one cluster under intersection. Consider
the minimal subtree of the block-cut tree containing the three clique-block
nodes. Because there is no bridge block between two blocks in one cluster,
this subtree has one of the following forms.

1. **Common-cut bouquet:** `Q,T1,T2` all contain one cut vertex `c`.
2. **Middle `K4`:** `T1` meets `Q` at `x`, `T2` meets `Q` at `y`, and
   `x != y`. Thus the clique-node path is `K3-K4-K3`.
3. **Middle triangle:** after relabeling, `Q` meets `T1` at `x` and `T1`
   meets `T2` at `y`, with `x != y`. Thus the clique-node path is
   `K4-K3-K3`.

This is exhaustive: the minimal subtree on three specified block nodes is
either a three-leaf star centered at a cut node, or a path with one of the
three block nodes in the middle. Since the two triangles are interchangeable,
there are only the two path types above. It also shows that purported extra
pairwise intersections cannot occur; they would create a cycle in the
block-cut graph.

All bridge-only material is harmless in this classification. Every component
outside the union of the cyclic blocks attaches to that union at a unique
vertex. Otherwise the block-cut graph would contain a cycle. We call the
resulting components the bridge branches rooted at that vertex.

## Uniform private-vertex partition

There is one short proof covering all three incidence types. At most two
vertices of `Q` are used to meet the two external triangles. Choose a vertex
`v in V(Q)` that belongs to neither triangle. Let `U` consist of `v` together
with every bridge branch rooted at `v`, and put `R=G-U`.

Both `G[U]` and `G[R]` are induced. The first is a tree (possibly the
one-vertex tree), so symmetry of a forest's spectrum gives

\[
s^+(G[U])=|U|-1.                                        \tag{3}
\]

Deleting `v` turns `Q` into a triangle and does not affect `T1,T2`. Hence
`G[R]` is a connected triangular block graph of cyclomatic rank three. Its
three triangle blocks have packing number at most two in every one-cluster
incidence type: this is immediate in the bouquet, and on either clique-node
path the middle block meets both end blocks. The packing-two sign theorem
therefore gives

\[
s^+(G[R])>|E(G[R])|=|R|+2.                              \tag{4}
\]

Superadditivity now yields

\[
s^+(G)\geq s^+(G[U])+s^+(G[R])
>(|U|-1)+(|R|+2)=n+1.                                  \tag{5}
\]

This proves the target, including all arbitrary bridge trees, without a
case-specific matching comparison. The remaining case analyses explain the
available direct Sachs signs and the requested middle-block splits.

## Case 1: common-cut bouquet

Every `4`-cycle in `Q` contains `c`. The only cycle in `Q` avoiding `c` is
the triangle on the other three vertices. It can be disjoint from either
external triangle, but `T1` and `T2` meet each other at `c`. Consequently:

- there is no collection of three pairwise vertex-disjoint cycles;
- every collection of two cycles has real Sachs phase;
- every odd-cardinality collection contributing to the imaginary part is a
  singleton triangle.

The singleton `4`-cycles are real. Hence, for every `t>0`,

\[
\operatorname{Im}\Psi_G(t)
=-2\sum_{T\text{ a triangle of }G}Z_{G-V(T)}(t)<0.       \tag{6}
\]

The arbitrary bridge trees only change the positive matching carriers in
(6). Coulson's identity therefore gives `s^+(G)>s^-(G)`. By (1),

\[
s^+(G)>|E(G)|=n+4>n.                                   \tag{7}
\]

## Case 2: chain `K3-K4-K3`

Write

\[
V(Q)=\{x,y,z,w\},\qquad x\in T_1,\quad y\in T_2.
\]

There is again a direct Sachs proof. The external triangles are disjoint.
However, every `4`-cycle in `Q` contains both `x,y`, and every triangle in
`Q` contains at least one of `x,y`. Thus no cycle in `Q` is disjoint from
both external triangles. There is no disjoint triple, and a `4`-cycle cannot
be paired with either external triangle. As in (3), the entire imaginary
part consists of negative singleton-triangle terms. Therefore (7) holds.

There is also a useful induced-partition proof. Put in the first part all of
`T1`, the vertices `z,w`, and every bridge branch rooted at one of those
vertices. Put in the second part all of `T2` and every bridge branch rooted
there. Equivalently, `x,z,w` induce a triangle from `Q`, while `y` stays with
`T2`. The two parts induce connected block graphs `H1,H2`:

- `H1` has exactly two triangular blocks, `T1` and `Q[{x,z,w}]`, so it has
  rank two;
- `H2` is triangular unicyclic.

Every core vertex and every bridge branch belongs to exactly one part. Thus
(2) and the rank-two/unicyclic results give

\[
s^+(G)\geq s^+(H_1)+s^+(H_2)
>|V(H_1)|+|V(H_2)|=n.                                  \tag{8}
\]

Edges of `Q` crossing the partition do not matter: (2) only requires the
pieces themselves to be induced on their respective vertex sets.

## Case 3: chain `K4-K3-K3`

Let the middle triangle be

\[
T_1=G[\{x,y,z\}],
\]

where `Q cap T1={x}` and `T1 cap T2={y}`. Split the middle triangle between
its two branches as follows:

\[
V(H_1):=V(Q)\cup\{z\}\cup
  \{\text{bridge branches rooted in these vertices}\},
\]

\[
V(H_2):=V(T_2)\cup
  \{\text{bridge branches rooted in these vertices}\}.
\]

The edge `xz` remains in `H1`, so `H1` is connected; its only cyclic block is
`Q`, and its remaining blocks are bridges. Thus `H1` has rank three. The
second graph `H2` is triangular unicyclic. They are disjoint induced graphs
whose vertices partition `V(G)`. Therefore

\[
s^+(G)\geq s^+(H_1)+s^+(H_2)
>|V(H_1)|+|V(H_2)|=n.                                  \tag{9}
\]

This partition is preferable to an unqualified imaginary-sign assertion.
Indeed, `Q` and `T2` are vertex-disjoint. A `4`-cycle of `Q` paired with
`T2` has phase

\[
q_4q_3=(-2)(-2i)=4i,
\]

so positive imaginary Sachs terms really occur. More explicitly,

\[
\operatorname{Im}\Psi_G(t)
=-2\sum_{T\text{ a triangle}}Z_{G-V(T)}(t)
+4\sum_{C\subset Q,\ C\cong C_4}
 Z_{G-V(C)-V(T_2)}(t).                                 \tag{10}
\]

Thus the packing-two half-plane argument does not apply directly in this
case without an additional matching domination inequality. Formula (9)
avoids that unnecessary comparison and remains valid for completely
arbitrary bridge attachments.

## Conclusion

The private-vertex partition proves `s^+(G)>n+1` uniformly. In addition, the
common-cut bouquet and the chain with middle `K4` have a strict negative Sachs
imaginary part and satisfy `s^+(G)>n+4`; the chain with middle `K3` admits the
requested split into induced rank-three and rank-one block graphs. These are
all one-cluster configurations. Combined with the existing bridge partition
for multiple clusters, every connected beta-five block graph with cyclic
blocks `K4,K3,K3` satisfies `s^+(G)>n`.
