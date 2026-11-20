# Universal hull–K2 theorem at cyclomatic rank seven

## Theorem status and exact scope

This theorem note accompanies
`research/universal-hull-k2-verifier.py`.  It addresses **only** the universal
hull–K2 lane; it is not a no-hull gate and it uses no R43, K22, K71, kernel,
or exact-row fixture as semantic evidence.

For a finite simple graph \(H\), write
\[
  s^+(H)=\sum_{\lambda_i(A(H))>0}\lambda_i(A(H))^2,
  \qquad \sigma(H)=s^+(H)-|V(H)|,
\]
and for connected \(H\), write
\[
  \beta(H)=|E(H)|-|V(H)|+1.
\]
Blocks use the standard convention: maximal 2-connected subgraphs together
with every bridge as a two-vertex block \(K_2\). A positive block is a
maximal block of positive cyclomatic rank.

### Theorem verified by the artifact

Let \(G\) be a finite simple connected graph with \(\beta(G)=7\). Suppose its
Tarjan maximal-block decomposition has exactly two positive blocks, whose
ranks are \(\{4,3\}\) or \(\{5,2\}\). In the full, unsuppressed block–cut
tree, suppose the unique path between those two positive block nodes contains
at least one rank-zero block, hence a one-edge bridge block \(K_2\). Then
\[
  \sigma(G)\ge 0.
\]
For the rank partition \(\{5,2\}\), the same proof gives the stronger
conclusion \(\sigma(G)>0\).

No claim is made here for the no-hull/shared-cut case. In particular, an
off-hull tree made entirely of bridge blocks does not open this lane.

## Exact proof

Let \(e=uv\) be any bridge-block node on the unique block–cut-tree path
between the two positive blocks. Since this block is a literal physical
\(K_2\), its only edge \(e\) is a bridge of \(G\). Deleting \(e\) produces
exactly two connected components with vertex sets \(X\) and \(Y\). Thus
\(X\dot\cup Y=V(G)\), and the two induced graphs are exactly the components:
\[
  G[X]=G-e\text{ on the }X\text{ side},\qquad
  G[Y]=G-e\text{ on the }Y\text{ side}.
\]
Because \(e\) lies on the full path between the two positive block nodes, the
positive blocks lie on opposite sides. There are exactly two positive blocks
in all of \(G\), and every other maximal block has rank zero. Cyclomatic rank
is additive over maximal blocks, while bridge blocks contribute zero.
Consequently the component ranks are precisely the two positive-block ranks:
\[
  \{\beta(G[X]),\beta(G[Y])\}=\{4,3\}
  \quad\text{or}\quad
  \{5,2\}.
\]
Both induced sides are finite, simple, and connected. The authenticated
complete lower-rank theorems therefore yield
\[
  \sigma(G[X])\ge0,\qquad \sigma(G[Y])\ge0
\]
for ranks 3, 4, and 5, and in rank 2 they yield the strict inequality
\(\sigma>0\). Induced square-energy superadditivity for the vertex partition
\(V(G)=X\dot\cup Y\) gives
\[
  \sigma(G)\ge \sigma(G[X])+\sigma(G[Y])\ge0.
\]
If the partition is \(\{5,2\}\), the rank-two side has strictly positive
credit and the rank-five side has nonnegative credit, so \(\sigma(G)>0\).
For \(\{4,3\}\), the cited complete theorems are only used at their stated
non-strict strength, so this theorem claims only \(\sigma(G)\ge0\).

That argument works for every hull bridge. The executable verifies all of
them at once rather than choosing one by a label-dependent rule.

## Adjacency reconstruction and invariants

The public production API is:

```python
receipt = verify(vertices, edges)
audit_receipt(vertices, edges, receipt)
```

The only graph input is the original vertex iterable and an iterable of
unordered endpoint pairs. Original vertices may be heterogeneous hashable
Python objects, including `None` and identity-hashed objects with colliding
`repr` strings, provided each object's hash is stable during a call and
equality is stable and symmetric on distinct labels. Reflexivity is not
required: a persistent NaN or identity-like object whose self-equality is
false is supported because identity still fixes the vertex. Deliberately
asymmetric, stateful, or hash-mutating objects do not define the stable finite
simple graph accepted by this API and are outside its contract.

The verifier never uses labels, `repr`, type, or a canonical atom grammar as
an ordering key. Equality and hashing are used only for ordinary adjacency
identity. Under the stated vertex contract, semantic acceptance is invariant
under caller iteration order and relabeling. Internal block/component tuples
may follow hash-table iteration order; **no deterministic Inventory tuple
order is promised or exposed**.

The verifier checks, rather than assumes:

1. nonempty finite vertex input with no duplicate equal vertices;
2. two distinct present endpoints per edge, with no loops or duplicate
   undirected edges;
3. connectedness of the physical graph;
4. iterative undirected edge-stack Tarjan reconstruction of all maximal
   blocks, with no recursive graph traversal, recursion-limit adjustment, or
   graph-size bound;
5. exact edge exhaustion and uniqueness across maximal blocks;
6. every rank-zero maximal block is one physical one-edge \(K_2\);
7. the full block–cut incidence graph, including all bridge blocks, is
   symmetric, connected, bipartite, and a tree;
8. block-rank additivity, parent rank exactly seven, exactly two positive
   blocks, and positive-rank multiset exactly \(\{4,3\}\) or \(\{5,2\}\);
9. the unique full block–cut-tree path between the positive blocks, with at
   least one intervening bridge-block node;
10. every hull \(K_2\) is one original physical graph edge.

### Linear simultaneous-deletion quotient

All physical hull bridges are deleted simultaneously. One iterative flood
computes the resulting components. The executable then reconstructs the
component quotient and verifies:

- exactly \(k+1\) components arise from deleting \(k\) hull edges;
- each deleted edge crosses two components and every nondeleted edge stays
  inside one component;
- no two hull bridges form a quotient multiedge;
- the quotient is connected and is one simple path;
- the two positive blocks remain intact in distinct endpoint components;
- the positive blocks are at opposite path ends, so every quotient edge
  separates them;
- component ranks computed as \(|E|-|V|+1\) equal independently accumulated
  maximal-block rank sums;
- the component ranks sum to seven;
- at every path edge, prefix/suffix rank sums are exactly the declared
  \(\{4,3\}\) or \(\{5,2\}\) partition; and
- exactly one positive block lies on each side of every hull bridge.

This is \(O(|V|+|E|)\) in graph work: no whole-graph flood is repeated for
each hull edge. Python hash-table operations are understood in their usual
amortized sense.

## Receipt and hostile replay

`Receipt` is a frozen, slotted record exposing only:

- a fixed schema identifier;
- the universal theorem-family identifier;
- the reconstructed rank partition;
- the exact unordered set of all physical hull edges; and
- the lower-rank theorem ledger `(rank, floor, strict)` for the two sides.

It exposes no owners, roots, block indices, component indices, path direction,
Inventory tuple, source-row identifiers, or unverified family metadata.
`audit_receipt` accepts the original adjacency again and reconstructs the
sources, graph, Tarjan blocks, full block–cut tree, hull, simultaneous-deletion
quotient, exact side ranks, physical hull-edge set, and theorem ledger afresh.
It compares every public receipt field. It therefore rejects wrong schema or
family, wrong partition, wrong ledger, an empty hull set, omitted hull edges,
forged/nonexistent edges, and real but off-hull edges. Because owner sets are
not exposed, there is no owner channel to forge or leave empty.

The production path snapshots each supplied iterable before its first
semantic pass.  Fresh replay proves that the adjacency supplied to
`audit_receipt` satisfies the theorem lane and that every exposed receipt field
is correct for that adjacency.  The receipt is reusable semantic evidence, not
an adjacency commitment: it does not identify the graph that originally minted
it or detect every theorem-preserving mutation.  Mutations that invalidate the
lane or change exposed evidence are rejected; the self-tests exercise this
with a post-verification loop insertion.  Source authentication is rerun on
every derivation and is not success-cached.

## Authenticated current sources

The verifier authenticates exact bytes and semantic locator strings in the
following current papers in the repository:

| rank / role | file | SHA-256 | theorem strength used |
|---|---|---|---|
| 2 | `all-bicyclic-graphs/paper.tex` | `56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da` | \(\sigma>0\) |
| 3 + induced superadditivity + bridge-block convention | `all-tricyclic-graphs/paper.tex` | `4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02` | \(\sigma\ge0\) |
| 4 | `all-tetracyclic-graphs/paper.tex` | `70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f` | \(\sigma\ge0\) |
| 5 | `all-pentacyclic-graphs/paper.tex` | `8ce140b07dc1428656b4ffd914305f2b14b49a0555cd13a6fc87be0fd4246a18` | \(\sigma\ge0\) |
| 6 + block convention/rank additivity lineage | `all-hexacyclic-graphs/paper.tex` | `0e7a2db2932d38a4b4909831c34050553afc0973869fe937eb510cb59421bda7` | authenticated, not needed to strengthen a side |

The rank-six paper is deliberately authenticated as requested and as a
current source for the standard block convention and explicit rank-additivity
lemma. No rank-six side occurs in this theorem. The proof does not infer
strictness for ranks 3–5; only the rank-two paper's explicit strict theorem is
used for the stronger \(\{5,2\}\) conclusion.

### Honest provenance caveat

A SHA-256 lock proves byte identity with the local files at the paths above;
it does not by itself prove the mathematics in those papers, peer review,
publication, or universal correctness of this Python program. The analytic
conclusion is conditional on the cited lower-rank theorems and induced
superadditivity being correct. The executable independently verifies the
finite adjacency premises and exact reduction to those theorems; its finite
self-tests corroborate implementation behavior but are not a proof of all
finite inputs.

## Test coverage and invocation

Run from the repository root:

```text
python3 research/universal-hull-k2-verifier.py
python3 -O research/universal-hull-k2-verifier.py
```

The release audit runs both modes under `PYTHONHASHSEED=0,1,2,42` and
requires byte-identical deterministic summaries. The suite covers both rank
partitions with connector lengths `1`, `1401`, `10000`, and `20000`; a
`12000`-edge arm inside each positive block; a `20000`-edge off-hull tree
payload; heterogeneous opaque relabels with identity-hashed objects sharing a
colliding `repr`; one persistent NaN vertex; an all-vertex constant-hash,
non-reflexive relabeling; reversed caller iteration order for stable labels;
source mutation/removal; and hostile adjacency/receipt replay. Asymmetric,
stateful, or hash-mutating pseudo-labels are explicitly outside the public
vertex contract rather than silently advertised as arbitrary graph labels.

Rejected cases include an off-hull K2-only payload when the two positives
share a cut (no hull K2), a connector chord, a third positive block, wrong
rank partition, loop, duplicate edge, disconnected component, isolated
vertex, mutated adjacency after receipt creation, wrong schema/family/ledger,
wrong partition, empty or incomplete hull evidence, nonexistent hull edges,
and real off-hull edges forged as hull evidence.

The script prints counts and theorem-level facts only. It never prints labels,
hash-dependent block order, or receipt tuple order.

An additional independent development-time cross-check,
`research/universal-hull-k2-external-crosscheck.py`, compares the verifier against NetworkX 3.7. It
checks exact maximal-block edge sets on 630 generated connected graphs and,
on 60 generated valid theorem graphs, also compares acceptance, rank
partition, and the exact physical hull-edge set. This corroboration is not a
production dependency and is not part of the mathematical proof.
