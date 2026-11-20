# Complete physical closure of `R221 = D+D+T^3`

## Status, scope, and supersession

**Status:** packet-local theorem artifact, conditional only on the pinned
analytic inputs listed in §10.  This file is not a publication claim, global
rank-seven theorem, or claim about any residual packet other than literal
`R221`.

For a finite graph `X`, let

\[
 s^+(X)=\sum_{\lambda_i(A(X))>0}\lambda_i(A(X))^2,
 \qquad
 s^-(X)=\sum_{\lambda_i(A(X))<0}\lambda_i(A(X))^2,
 \qquad
 \sigma(X)=s^+(X)-|V(X)|.
\]

For a connected graph, write

\[
 \beta(X)=|E(X)|-|V(X)|+1
\]

for its cyclomatic rank.  A **block** below is a maximal
vertex-biconnected edge block reconstructed from the physical adjacency;
every physical bridge edge is therefore a `K2` block.  A block has positive
rank when its cyclomatic rank is positive.

This note expressly excludes the old `R221` paragraph in
`positive-square-energy/heptacyclic-general/nested-induced-piece-packet-theorem.md`.
That paragraph extended

\[
 \sigma(D+T^k)>1+k
\]

unsupportedly to `k=3`, where it would assert `>4`.  No statement, threshold,
certificate, or verifier conclusion from that paragraph is used here.  The
replacement is the original-vertex cut argument in §5.  It proves the narrow
floor needed by this packet and, at `k=3`, gives `>2`; it is **not** a
`D+T^3` determinant-phase theorem and makes no `>4` claim.

The word “complete” in the title means complete for the one literal physical
packet stated next.  It has no broader meaning.

## 1. Packet-local physical theorem

A **literal diamond** is

\[
 D=\Theta(1,2,2)=K_4-e,
\]

with four original vertices, five edges, and internal degree multiset
`(3,3,2,2)`.  A **literal triangle** is a `K3` block.

### Theorem 1.1 (complete physical `R221`, packet-local)

Let `G` be a finite simple connected graph whose positive-rank maximal blocks
are exactly

\[
 D_0,D_1,T_1,T_2,T_3,
\]

where `D_0,D_1` are literal diamonds and `T_1,T_2,T_3` are literal triangles.
Every other block is a physical bridge `K2`.  Thus the positive block-rank
inventory is exactly

\[
 2+2+1+1+1=7.
\]

Arbitrary finite bridge paths, connector branching, repeated articulation
vertices, block nesting, and finite tree payloads are allowed.  Conditional
on the analytic theorems pinned in §10,

\[
 \boxed{\sigma(G)>0.}
\]

The theorem is literal-block specific.  Subdividing an edge inside a named
diamond or triangle changes that physical block and leaves the theorem's
scope.

## 2. Exact DNN arithmetic forces the sole residual `D+D+T^3`

This section is a self-contained reduction of the rank partition
`2+2+1^3` to the literal packet in Theorem 1.1.  It classifies failures of the
specified DNN certificate; it does not call such a failure a graph
counterexample.

### 2.1 The exact DNN quantity

For an edge-containing graph `H`, define

\[
 \kappa(H)=
 \sup_{\substack{M\succeq0,\ M\ge0\\
                  \mathbf1^TM\mathbf1>0}}
 \frac{4\left(\sum_{uv\in E(H)}\sqrt{M_{uv}}\right)^2}
      {\mathbf1^TM\mathbf1},
\]

where `M>=0` is entrywise.  The DNN dual theorem gives

\[
 s^-(H)\le \kappa(H),
 \qquad
 s^+(H)=2|E(H)|-s^-(H)\ge2|E(H)|-\kappa(H).       \tag{2.1}
\]

Moreover, `kappa` is additive under one-vertex sums and
`kappa(K2)=1`; hence every bridge/tree edge contributes exactly one.

A simple rank-two 2-connected block is a theta subdivision
`Theta(a,b,c)`.  Put `L=a+b+c` and

\[
 \Delta(a,b,c)=\min_{0\le\theta\le\pi}
 \left(
 \sum_{\ell\in\{a,b,c\},\ \ell\ {
m even}}
       \ell\tan^2\frac{\theta}{2\ell}
 +
 \sum_{\ell\in\{a,b,c\},\ \ell\ {
m odd}}
       \ell\tan^2\frac{\pi-\theta}{2\ell}
 \right).                                             \tag{2.2}
\]

For a cycle, put

\[
 \epsilon_q=
 \begin{cases}
 0,&q\text{ even},\\
 q\tan^2\!\left(\dfrac{\pi}{2q}\right),&q\text{ odd}.
 \end{cases}                                          \tag{2.3}
\]

The exact path elimination theorem gives

\[
 \kappa(\Theta(a,b,c))=L+\Delta(a,b,c),
 \qquad
 \kappa(C_q)=q+\epsilon_q.                            \tag{2.4}
\]

Consequently, if the two rank-two blocks have excesses
`Delta_1,Delta_2` and the three cycle blocks have excesses
`epsilon_1,epsilon_2,epsilon_3`, block additivity gives the exact identity

\[
 \kappa(G)=|E(G)|+\Delta_1+\Delta_2
                  +\epsilon_1+\epsilon_2+\epsilon_3.  \tag{2.5}
\]

A connected rank-seven graph has `|E(G)|=|V(G)|+6`.  Therefore (2.1)
closes `s^+(G)>=|V(G)|` whenever

\[
 \Delta_1+\Delta_2+\epsilon_1+\epsilon_2+\epsilon_3
 \le6.                                                \tag{2.6}
\]

Equality in (2.6) is closed.  Only strict failure of (2.6) survives this
DNN sieve.

### 2.2 Exact theta/cycle classification and arithmetic

The exact classification in `all-tricyclic-graphs/paper.tex`, lines 289–417
of the pinned bytes, says:

* `Delta(a,b,c)>1` exactly for the sorted triples `(1,2,r)`, `r>=2`;
* with
  \[
   d=\frac{\sqrt{17}-1}{2},
  \]
  one has `Delta<=d`, with equality only for the literal diamond
  `Theta(1,2,2)`;
* every non-diamond theta has `Delta<4/3`: the nonexceptional thetas have
  `Delta<1`, and the remaining `(1,2,r)` cases with `r!=2` have the stated
  strict `4/3` bound;
* `epsilon_3=1` and `epsilon_5=5-2sqrt(5)<2/3`;
* `epsilon_q<2/5` for every odd `q>=7`, while even cycles have zero excess.

Thus `C5` has the largest nontriangular cycle excess.  The complete forcing
arithmetic is now short.

If at least one of the three cycles is nontriangular, then the other two
cycle excesses are at most one and

\[
 \begin{aligned}
 \Delta_1+\Delta_2+\sum_{i=1}^3\epsilon_i
 &\le 2d+2+(5-2\sqrt5)\\
 &=\sqrt{17}+6-2\sqrt5<6,
 \end{aligned}                                        \tag{2.7}
\]

because `sqrt(17)<2sqrt(5)`.  If all three cycles are triangles but at least
one theta is not the literal diamond, then

\[
 \Delta_1+\Delta_2+3
 <d+\frac43+3<6,                                      \tag{2.8}
\]

because `d<5/3`, equivalently `sqrt(17)<13/3`.  Finally, two literal
diamonds and three literal triangles give

\[
 2d+3=\sqrt{17}+2>6.                                  \tag{2.9}
\]

Hence the **only** strict post-DNN residual in the block-rank partition
`2+2+1^3` is

\[
 \boxed{D+D+T^3}.                                     \tag{2.10}
\]

Sections 4–8 prove that this literal residual is itself strict.

## 3. Analytic inputs—and no hidden `D+T^3` input

The physical proof uses only the following imported results.

1. **Induced superadditivity.**  For every partition into sets of original
   vertices,
   \[
    V(X)=V_1\mathbin{\dot\cup}\cdots\mathbin{\dot\cup}V_m,
   \]
   one has
   \[
    \sigma(X)\ge\sum_{j=1}^m\sigma(X[V_j]).            \tag{3.1}
   \]
   Crossing edges are allowed.  Every charged graph is the induced graph on
   its assigned original vertices.

2. **Triangular block graphs.**  If a connected graph has at least one cyclic
   block and every cyclic block is a literal triangle, with arbitrary bridge
   blocks and finite attached trees, then
   \[
    \sigma(X)>0.                                       \tag{3.2}
   \]

3. **Connected fixed-rank floors.**  Every connected graph of cyclomatic rank
   `r in {2,3,4,5}` satisfies
   \[
    \sigma(X)\ge0.                                     \tag{3.3}
   \]
   Only the weak floor is used.

4. **Exact attached-diamond packets.**  The `D` and `D+T` bounds come
   specifically from `all-pentacyclic-graphs/paper.tex`, lines 239–290 of the
   pinned bytes.  Its packet ledger and weighted-state/one-sum calculation
   prove, with arbitrary one-root tree branches and a bridge-free positive
   hull,
   \[
    \sigma(D)>1,\qquad \sigma(D+T)>2.                  \tag{3.4}
   \]
   The separate exact `D+T+T` theorem proves
   \[
    \sigma(D+T+T)>3                                   \tag{3.5}
   \]
   when the two triangles are direct/direct at arbitrary, possibly equal,
   diamond cut vertices, or direct/nested.  It also permits arbitrary
   one-root tree branches and excludes positive `K2` connectors from the
   positive hull.

There is **no imported `D+T^3` estimate**.  In particular, (3.5) is not
iterated by a monotonicity or phase argument.

We also use the following elementary identity, proved here.  If `F` is a
nonempty tree, its bipartite spectrum is symmetric, so

\[
 s^+(F)=\frac12\operatorname{tr}A(F)^2=|E(F)|=|V(F)|-1.
\]

Therefore

\[
 \sigma(F)=-1.                                        \tag{3.6}
\]

No rank-six theorem, generic rank-seven bridge theorem, universal
nonunicyclic-cactus theorem, `R21` narrow-packet theorem, old nested `R221`
paragraph, or `R322` result is used.

## 4. Original-vertex topology lemmas

Let `BC(H)` be the physical block-cut tree of a connected graph `H`.  Its
block nodes are all maximal edge blocks, including every bridge `K2`; its
other nodes are the physical articulation vertices.  Paths, ancestry, and
incidence below always refer to this actual tree.

### Lemma 4.1 (maximal-block owner fibres)

Let `B` be a nontrivial maximal 2-connected block of a connected graph `H`.
Then every component of `H-E(B)` meets `V(B)` in exactly one original vertex.
Consequently the components are canonically indexed by the original vertices
of `B`.

**Proof.**  Every component meets `B`: from any vertex, take a path in
connected `H` to its first vertex of `B`; the prefix uses no edge of `B` and
lies in one component of `H-E(B)`.

Suppose one component met distinct `u,v in V(B)`.  Inside that component take
a shortest path whose endpoints are distinct vertices of `B`, and then take
two consecutive occurrences of `B` on it.  The resulting path uses no edge
of `B` and has no internal vertex in `B`.  It is an open ear (a one-edge chord
is included) whose addition to the 2-connected graph `B` remains
2-connected.  It contains an edge outside `B`, contradicting maximality of
`B`.  Thus each component meets at most one vertex of `B`.  Every vertex of
`B` remains in `H-E(B)` and one original vertex cannot lie in two components,
so there is exactly one component for each vertex of `B`. ∎

No articulation is copied in this statement: each physical vertex has one
owner.

### Lemma 4.2 (one-root attachment from the physical tree)

Let `P_1,...,P_t` be selected positive blocks of `H`.  Suppose their minimal
incidence subtree in `BC(H)` contains no `K2` block and no positive block
other than the selected ones.  Form its **cut closure** by adjoining every
articulation node incident with a selected positive block.  If every block
outside the selected list is a `K2`, then every remaining physical piece,
after adjoining its unique attachment vertex in the cut closure, is a tree
attached at exactly one original vertex.

**Proof.**  The cut closure is a connected subtree of the tree `BC(H)`.
Every component left after its deletion has exactly one incidence edge back
to it; two such edges would form a cycle in `BC(H)`.  Every block node in a
remaining component is a `K2`.  On restoring the unique boundary cut vertex,
the corresponding physical subgraph is therefore connected and acyclic and
meets the core only at that vertex.  In particular, no acyclic router meeting
two core vertices is silently absorbed as a one-root branch. ∎

This lemma verifies the tree-attachment hypotheses of (3.4)–(3.5) from
physical adjacency; a packet name alone does not verify them.

## 5. The narrow root lemma; `k=3` by an induced cut, not phase

### Lemma 5.1 (narrow `D+T^k` root floor)

Let `H` be connected.  Suppose its positive blocks are exactly one literal
diamond `D` and `k` literal triangles, where `0<=k<=3`; every other block is
a `K2`.  Suppose the minimal subtree of `BC(H)` spanning the positive blocks
contains no `K2` block.  Then

\[
 \sigma(H)>1.                                         \tag{5.1}
\]

**Proof for `k=0,1,2`.**  With no `K2` in the positive hull, the physical
incidences are exhaustive:

* for `k=0`, the attached diamond;
* for `k=1`, one triangle direct at a physical diamond cut;
* for `k=2`, direct/direct (allowing the same diamond cut twice) or
  direct/nested.

Lemma 4.2 proves that all remaining material consists of genuine one-root
trees.  Equations (3.4)–(3.5) give respectively `>1`, `>2`, and `>3`, each
stronger than (5.1).

**The `k=3` induced-cut argument.**  Root `BC(H)` at the diamond block node.
Choose the two triangle block nodes of least depth, using any fixed tie-break,
and call them `T_a,T_b`; call the omitted triangle `T_o`.

Let `S` be the minimal incidence subtree spanning `D,T_a,T_b`.  The node
`T_o` is not in `S`.  If it were, it would be a proper ancestor of one of the
selected triangles and would have strictly smaller depth, contradicting the
choice of the two least-depth triangle nodes.  Equivalently, neither selected
triangle is a descendant of `T_o`.

The retained incidence is therefore exactly one of the forms allowed by
(3.5).  If `T_a,T_b` are incomparable, no positive block and no `K2` lies
internally on either root route, so they are direct/direct from `D`, possibly
at the same cut.  If, say, `T_a` is an ancestor of `T_b`, the route is

\[
 D-c_0-T_a-c_1-T_b,
\]

with `c_1!=c_0`; otherwise the two triangle block nodes would be siblings,
not comparable.  This is direct/nested incidence.

Now cut in original vertices.  Let `c` be the parent articulation of `T_o`.
Delete exactly the three edges of `T_o`.  By Lemma 4.1 the resulting
components are `C_x`, one for each original vertex `x in V(T_o)`, and `C_x`
meets `T_o` exactly at `x`.  Define

\[
 A=V(C_c),
 \qquad
 W=\bigcup_{x\in V(T_o)\setminus\{c\}}V(C_x).          \tag{5.2}
\]

These are disjoint and exhaustive sets of original vertices.  The induced
graph `H[A]` is connected.  The induced graph `H[W]` is connected because
the edge of `T_o` joining its two vertices different from `c` joins the two
private owner components.  The only crossing edges are the two triangle
edges incident with `c`.  The physical vertex `c`, every sibling block at
`c`, and every branch rooted at `c` belong only to `A`; branches rooted at a
private triangle vertex belong only to `W`.

The root diamond and both selected triangles lie in `A`, because no selected
triangle is below `T_o`.  No positive block lies in `W`: the complete positive
list was `D,T_a,T_b,T_o`, and opening `T_o` leaves in `W` only its private
edge.  Thus `H[W]` is a nonempty connected rank-zero graph, hence a tree, and

\[
 \sigma(H[W])=-1.                                     \tag{5.3}
\]

Inside `H[A]`, take the cut closure of the incidence subtree `S`.  Every
remaining block is a `K2`, and each remaining component attaches once by
Lemma 4.2.  This remains true if `T_o` shares an articulation with a retained
block: that one original cut vertex belongs to `A` only.  Hence `H[A]` is
exactly an allowed direct/direct or direct/nested `D+T+T` packet, so

\[
 \sigma(H[A])>3.                                      \tag{5.4}
\]

Induced superadditivity on the original-vertex partition (5.2) gives

\[
 \sigma(H)\ge\sigma(H[A])+\sigma(H[W])>3-1=2>1.
\]

This is a narrow structural cut proof.  It does not prove
`\sigma(D+T^3)>4`, does not extend the lower-half-plane formula for
`D+T+T`, and is not an imported `D+T^3` phase theorem. ∎

## 6. Simultaneous first-`K2` antichain separation

Choose either physical diamond and name it `D_0`; no favorable root is
assumed.  Root `BC(G)` at its block node.  For each other positive block

\[
 X\in\{D_1,T_1,T_2,T_3\},
\]

inspect the unique root-to-`X` route.  If it contains a `K2` block node,
select the first such node from the root and hence its unique physical bridge
edge.  Deduplicate equal selections before deleting anything.  Let `F` be
the resulting set of physical edges.

### Lemma 6.1 (first-`K2` antichain)

The selected `K2` block nodes are pairwise incomparable in the rooted
block-cut tree.

**Proof.**  If distinct selected nodes `e,f` had `e` strictly above `f`, then
every root route reaching `f` would encounter `e` first.  The node `f` could
therefore not have been selected as the first `K2` on any target route. ∎

Delete all edges in `F` simultaneously.  Each is a physical bridge.  By the
antichain property, the components are exactly

* one root component `R` containing `D_0`; and
* one complete away component `A_e` beyond each `e in F`.

Their original-vertex sets are pairwise disjoint and exhaustive.  Every
`R` and `A_e` is connected and is the induced graph on its vertex set: after
bridge deletion there is no undeleted edge between two components.  A shared
connector prefix is cut once, not once for each positive label.  No selected
edge lies inside another selected away side, so `A_e` contains the positive
block whose route selected `e`.  Every later connector vertex, branch point,
nested block, and rooted payload stays in that one complete side.  Thus

\[
 V(G)=V(R)\mathbin{\dot\cup}
       \bigdotcup_{e\in F}V(A_e)                       \tag{6.1}
\]

is an induced exhaustive partition of original vertices.

No away side contains `D_0`.  Its intact positive inventory is therefore
exactly one of the following:

* `q` literal triangles and no diamond, where `1<=q<=3`; or
* `D_1` and `q` literal triangles, where `0<=q<=3`.

In the first case every cyclic block is a literal triangle, and (3.2) gives

\[
 \sigma(A_e)>0.                                       \tag{6.2}
\]

In the second case block-rank additivity gives

\[
 \beta(A_e)=2+q\in\{2,3,4,5\},
\]

so (3.3) gives

\[
 \sigma(A_e)\ge0.                                    \tag{6.3}
\]

This is packet-specific dispatch.  It does not use the false generic rule
that every rank-one bridge side is nonnegative; for example
`\sigma(C_5)=2-\sqrt5<0`.  Here every rank-one away side is physically forced
to be a literal triangle.

Finally, every positive block retained in `R` has a `K2`-free route from
`D_0`.  Otherwise its first `K2` would have been selected and the block would
lie in an away component.

## 7. Four diamond fibres and induced `U/W` ownership

There are two cases.

### 7.1 The second diamond is away

Suppose `D_1` is not in `R`.  The positive blocks of `R` are exactly `D_0`
and `k` retained triangles for some `0<=k<=3`.  Their root routes are
`K2`-free by §6, so Lemma 5.1 gives

\[
 \sigma(R)>1.                                         \tag{7.1}
\]

Equations (3.1), (6.1), (6.2), and (6.3) already imply `sigma(G)>0`.

### 7.2 The second diamond is retained

Suppose `D_1` lies in `R`.  Let `c` be its parent articulation on the route
from `D_0` in the rooted physical block-cut tree.  Work inside the induced
root graph `R` and delete exactly the five edges of `D_1`.  The block `D_1`
remains maximal in `R`: any path in `R` outside `D_1` between two of its
vertices would also be such a path in `G` and would contradict maximality in
`G`.

Lemma 4.1 now gives **exactly four diamond fibres**.  For each original
vertex `x in V(D_1)`, let `C_x` be the component of `R-E(D_1)` containing
`x`.  Then the four `C_x` are distinct, exhaustive, and each meets `D_1`
exactly at its indexing vertex.  Define original-vertex sets

\[
 U=V(C_c),
 \qquad
 W=\bigcup_{x\in V(D_1)\setminus\{c\}}V(C_x).         \tag{7.2}
\]

The sets `U,W` are disjoint and exhaust `V(R)`; no copy of `c` is placed in
`W`.  The graphs charged below are the induced graphs `R[U]` and `R[W]`.
The graph `R[U]` is connected.  The graph `R[W]` is connected because the
physical remnant on the other three diamond vertices is

\[
 D_1-c=
 \begin{cases}
  P_3,&\deg_{D_1}(c)=3,\\
  K_3,&\deg_{D_1}(c)=2.
 \end{cases}                                          \tag{7.3}
\]

This remnant joins the three owner fibres.  The only edges crossing `U/W`
are the diamond edges incident with `c`; every other diamond edge lies in
`R[W]`, and no edge outside `D_1` joins two owner components.

Ownership is now literal:

* `D_0`, the route from `D_0` to `c`, every sibling block at `c`, and every
  payload rooted at `c` lie in `U`;
* a descendant route leaving `D_1` through `x!=c` lies wholly in `C_x` and
  hence in `W`;
* every original triangle in `R` is intact and lies wholly in exactly one
  fibre, because none of its edges was deleted and its vertices remain
  connected in `R-E(D_1)`;
* every nested block and every tree payload follows its first owner fibre and
  is charged once.

#### The upstream induced graph

Let

\[
 a=\#\{T_i:T_i\text{ lies in a first-`K2` away side}\},
 \qquad
 \delta=\#\{T_i:T_i\subseteq R[W]\},
 \qquad
 k=3-a-\delta.                                      \tag{7.4}
\]

Thus `delta` is the number of downstream triangles in `W`, and the positive
blocks of `R[U]` are exactly `D_0` and the `k` intact original triangles not
owned away or by `W`.  In the no-triangle-away subledger, `a=0` and hence
`k=3-delta`; formula (7.4) is the exact general ownership count when first-
`K2` sides have already removed triangles.  The opened block `D_1` contributes
no edge to `R[U]`, because
`U` meets it only at `c`.  A triangle in `U` cannot have a root route that
traverses `D_1` and exits through another diamond vertex: that would place it
in the corresponding component of `W`.  Its route from `D_0` therefore
survives in `U` and is `K2`-free.

Lemma 5.1 and its sharper low-`k` inputs give the exact anchor floor needed
here:

\[
 \sigma(R[U])>
 \begin{cases}
  1,&k=0,\\
  2,&1\le k\le3.
 \end{cases}                                          \tag{7.5}
\]

For `k=1` this is the exact `D+T` packet; for `k=2` it is the exact
`D+T+T` packet; for `k=3` the cut proof of Lemma 5.1 gives `>2`.

#### Connectivity and exact rank of the opened side

Put

\[
 \eta=\mathbf1_{\{\deg_{D_1}(c)=2\}}.
\]

Owner fibres are joined only by the remnant (7.3), so block-rank additivity
gives the exact formula

\[
 \boxed{\beta(R[W])=\delta+\eta}.                   \tag{7.6}
\]

Indeed, the `P3` remnant adds no cycle, whereas the `K3` remnant adds exactly
one literal triangular block.  All other cyclic blocks of `R[W]` are the
`delta` intact original triangles.

If `delta+eta=0`, then `R[W]` is a nonempty connected rank-zero graph and is
a tree, so its exact credit is `-1`.  If `delta+eta=1`, it is a connected
unicyclic triangular block graph and (3.2) gives strict positive credit; the
weaker floor `-1` would already suffice.  If `delta+eta>=2`, the connected
fixed-rank floor (3.3), or (3.2) directly, gives nonnegative (indeed strict)
credit.  In the integer ledger we may therefore record

\[
 \sigma(R[W])\ge
 \begin{cases}
  -1,&\delta+\eta\in\{0,1\},\\
  0,&\delta+\eta\ge2,
 \end{cases}                                          \tag{7.7}
\]

while remembering that the rank-one triangular case is actually `>0` and
that equality `-1` can occur only at rank zero.

The two floors already close every case.  If `k>=1`, the anchor has credit
`>2`; if `k=0`, it still has credit `>1`.  In either case (7.7) charges at
worst `-1`, so induced superadditivity on (7.2) gives

\[
 \sigma(R)\ge\sigma(R[U])+\sigma(R[W])>1-1=0.         \tag{7.8}
\]

The sharper `>2` floor leaves more than one unit whenever an upstream
triangle exists; the `k=0` floor is nevertheless already strict enough to pay
the single tree debit.  Adding the nonnegative first-`K2` away sides from
(6.2)–(6.3) proves `\sigma(G)>0` in the retained-diamond case.

## 8. Both-root symmetry and exact ledger

The root `D_0` in §§6–7 was an arbitrary one of the two physical diamonds.
No step uses a label-specific property.  Interchanging `D_0,D_1` and
rerooting the same physical block-cut tree gives the same proof scheme.  The
actual selected bridges, entry degree, and owner territories need not be the
same after rerooting; each orientation is proved independently by the same
original-vertex argument.

Only one arbitrary-root proof is logically needed.  A finite adjacency
verifier may replay both roots to detect orientation mistakes, but that replay
is corroborative only and is neither a premise nor a replacement for the
universal topology proof.

The complete charge ledger is:

| Territory | Possible number | Exact physical inventory | Floor used |
|---|---:|---|---:|
| first-`K2` away, no diamond | any | `T^q`, `1<=q<=3` | `>0` |
| first-`K2` away containing `D_1` | at most one | rank `2+q`, `0<=q<=3` | `>=0` |
| root when `D_1` is away | one | `D_0+T^k`, `0<=k<=3`, `K2`-free hull | `>1` |
| upstream `U` when `D_1` is retained | one | `D_0+T^k`, `0<=k<=3`, `K2`-free hull | `>1` if `k=0`; `>2` if `k>=1` |
| opened `W` with `beta(W)=delta+eta in {0,1}` | at most one | tree at rank zero; triangular unicycle at rank one | ledger `>=-1` (exactly `-1` only at rank zero) |
| opened `W` with `beta(W)=delta+eta>=2` | at most one | connected triangular block graph | ledger `>=0` (actually `>0`) |

Thus, if `D_1` is away,

\[
 \sigma(G)\ge (>1)+(\ge0)+\sum(>0)>0.                 \tag{8.1}
\]

If `D_1` is retained, there is no diamond-containing away side, and the
exact integer ledger is

\[
 \sigma(G)>
 \begin{cases}
  2-1+0,&k\ge1,\\
  1-1+0,&k=0,
 \end{cases}
 =0,                                                   \tag{8.2}
\]

where `0` denotes the sum of the nonnegative first-`K2` away credits (strict
triangle-away credits, if present, only improve the line).  Empty sums are
allowed.  There is at most one `-1` debit, and even the `k=0` strict anchor
pays it.  Equations (8.1)–(8.2) complete the proof of Theorem 1.1. ∎

## 9. Exact nonclaims and hostile-topology coverage

The proof covers long bridge connectors, shared connector prefixes,
connector branching, repeated articulation vertices, nested triangles,
nested diamonds, both diamond entry-degree orbits, and arbitrary finite tree
payloads.  It does so by assigning complete components of physical edge cuts,
not by assigning names or copies of articulation vertices.  Every charged set
in (5.2), (6.1), and (7.2) is first defined as a disjoint set of original
vertices and only then replaced by its induced graph.

The following boundaries are explicit.

1. This is no generic hull-bridge theorem.  Packet-specific typing is
   essential; `sigma(C5)=2-sqrt(5)<0` disproves the naive claim that every
   rank-one away side is nonnegative.
2. This note makes no standalone determinant-phase claim for `D+T^3`, no
   estimate `sigma(D+T^3)>4`, and no monotonic extension from the exact
   `D+T+T` phase theorem.  The `k=3` statement in Lemma 5.1 is an induced-cut
   consequence and only its floor `>1` is consumed by the final ledger.
3. The invalid old nested `R221` paragraph and its synthetic threshold
   verifier are excluded, not repaired in place and not treated as a
   dependency.
4. This note proves neither the full rank-seven multiblock theorem nor any
   single-block case, other residual key, `R21`, `R322`, or source manuscript.
5. DNN-boundary profiles are asserted only to meet the non-strict target
   supplied by (2.1); no strict surplus on the boundary is claimed.
6. Hashes authenticate exact source bytes, not mathematical truth,
   publication, promotion, or independent review.
7. Finite semantic fixtures may corroborate the physical construction but do
   not establish its universal quantifiers.
8. Subdivided diamonds or triangles are outside the literal theorem even if a
   coarser profile label would look similar.

## 10. Exact dependency and exclusion ledger

The following SHA-256 values pin the exact bytes supplying the imported
analytic statements.  The DNN residual arithmetic itself is written out in
§2; no rank-seven residual table is substituted for that arithmetic.

| Role | Exact source | SHA-256 | Exact scope consumed |
|---|---|---|---|
| DNN dual, induced superadditivity, connected rank-three theorem, and primary theta/cycle classification | `all-tricyclic-graphs/paper.tex` | `4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02` | DNN dual/additivity; lines 289–417 for (2.2)–(2.9), including the unique diamond maximum, nonmaximum `<4/3`, and exact cycle excesses; rank-three away floor |
| primary `D` and `D+T` packet provenance; connected rank-five theorem | `all-pentacyclic-graphs/paper.tex` | `8ce140b07dc1428656b4ffd914305f2b14b49a0555cd13a6fc87be0fd4246a18` | lines 239–290 for the packet scope and weighted-state/one-sum proofs of `>1` and `>2`; rank-five away floor |
| exact `D+T+T` packet | `positive-square-energy/pentacyclic-general/diamond-two-triangle-exact-packet.md` | `9107ef2821d441da401079982ae8d0b6c98cee17ae7e52268a9b6ad895b8e11b` | all direct/direct owner multisets, including repeated cuts, and direct/nested incidence; arbitrary one-root trees; `>3` |
| triangular block graphs | `packing-two-square-energy/paper.tex` | `9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791` | strict positivity for connected all-triangle block graphs with bridges and trees |
| connected rank two | `all-bicyclic-graphs/paper.tex` | `56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da` | rank-two complete-away-side floor |
| connected rank four | `all-tetracyclic-graphs/paper.tex` | `70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f` | rank-four complete-away-side floor |

The rank-five source is already the pinned all-pentacyclic manuscript in the
second row.  The tree identity (3.6), first-`K2` antichain, four-fibre owner
lemma, `U/W` rank calculation, and narrow `k=3` cut are proved inside this
note and have no external packet dependency.

For avoidance of doubt, the historical file

`positive-square-energy/heptacyclic-general/nested-induced-piece-packet-theorem.md`

has SHA-256

`79b44180ff2d3ca44b5537e2913709fa6c2334b2e475990b34508475592a000b`.

It is recorded solely to identify the excluded artifact.  It is **not** in
the dependency closure.  Likewise,
`positive-square-energy/heptacyclic-general/r21-complete-physical-closure.md`
is not imported for Lemma 5.1; the needed `k=3` argument is proved directly
in §5.

## 11. Dependency closure in one sentence

Exact DNN arithmetic leaves only literal `D+D+T^3`; the simultaneous
first-physical-`K2` antichain gives disjoint complete away territories; the
fixed-rank and triangular theorems make those territories nonnegative; four
original-vertex fibres of a retained second diamond give an induced
`D+T^k` upstream anchor of credit `>1` and a connected opened side of credit
at least `-1`; induced superadditivity then gives `sigma(G)>0`.
