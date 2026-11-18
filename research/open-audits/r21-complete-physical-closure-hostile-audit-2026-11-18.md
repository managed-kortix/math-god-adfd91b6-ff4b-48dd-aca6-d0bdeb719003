# Hostile audit of `r21-complete-physical-closure.md`

Date: 2026-11-18. Status: **BLOCK on the audited bytes / NONPROMOTIONAL**.

Audited target: the untracked file
`positive-square-energy/heptacyclic-general/r21-complete-physical-closure.md`
as present on branch `main-read` on 2026-11-18. Line numbers below refer to
those bytes. This note does not edit or promote that target, `STATE`, any
master theorem, or any publication artifact.

## Verdict

The proposed theorem is **not proved by the current text**. I found no graph
violating the claimed spectral inequality, but I found a concrete
original-vertex ownership failure in the retained-pentagon proof. The repair is
small and local: perform the pentagon owner-fibre opening inside the induced
root group left after the simultaneous first-bridge deletion, not in the full
graph. Until that change is made, Sections 3 and 5 do not compose.

The two requested subverdicts are:

* **Section 1 (six-triangle lemma): ACCEPT, but only with the physical
  block-cut-tree reading recorded below.** The theorem follows from existing
  exact-scope packet statements. The numerical/exact scout is corroborating
  evidence, not the proof.
* **Section 5 (retained pentagon): BLOCK on current bytes.** Lines 233--245
  define owner components in full `G`, although the object being partitioned is
  the root group after lines 178--188. A legal first-bridge away group can then
  be swallowed by the parent C5 fibre and also retained as a separate away
  group at line 264.

There is also one exact inequality repair: line 190 must use

```text
sigma(P-only) >= -(sqrt(5)-2) > -1,
```

not strict inequality at the first comparison. Bare `C5` has equality.

## 1. Six-triangle lemma: accepted scope, not executable provenance

### 1.1 Correct physical object

At lines 65--80, the labelled sources must be understood as the **full,
pairwise vertex-disjoint incidence subtrees of maximal shared-cut clusters in
the physical block-cut tree**, before contraction. Labeling only six abstract
marked nodes is insufficient to own articulation vertices. With the full
subtrees retained, contract them and assign every remaining physical
block/cut-tree node by multi-source distance with a fixed tie-break. The usual
predecessor argument in a tree proves that every label class is connected.
Every edge between classes lies on a K2-only connector route; cut one actual
bridge on that route. Shared articulation vertices are never duplicated.

An off-hull component has exactly one attachment to the hull. Two distinct
attachments would give a second path in the block-cut object and hence a cycle
outside the listed cyclic blocks. Therefore each rooted branch follows the
unique label containing its attachment. At a connector Steiner node, the node
and every incident acyclic branch follow the one label assigned to that node;
only actual bridge edges between differently labelled classes are discarded.
This gives original-vertex sets that are connected, induced after restriction,
pairwise disjoint, and exhaustive. It also prevents the forbidden operation of
cutting every bridge incident with a selected path and leaving an uncharged
acyclic middle component.

This clarification is essential to lines 77--80 and 110--111. With it, their
claims about connector remnants, Steiner branches, entry vertices, and
arbitrary rooted payloads are correct.

### 1.2 Exact packet scopes

The invoked floors have matching existing scope:

1. `all-heptacyclic-cacti/paper.tex`, lines 96--108 and 174--205, proves for
   one shared-cut triangle cluster with arbitrary attached trees

   ```text
   A1>0, A2>1, A3>2, A4>3, A5>2, A6>1.
   ```

   Its private-vertex leaf opening owns one nonempty tree of credit exactly
   `-1`; it does not use monotonicity or silently delete both private vertices.
2. `all-bicyclic-graphs/paper.tex`, Theorem `thm:main`, has the broader exact
   statement that every connected bicyclic graph, including a two-triangle
   cactus with arbitrary connector and arbitrary rooted trees, has `sigma>0`.
   More sharply, because such a graph has `|E|=|V|+1` and the two triangle Sachs
   phase gives `s+>s-`, it has `sigma>1`. The same attached two-triangle scope is
   stated in the cited cactus/packet sources.
3. `packing-two-square-energy/paper.tex`, Corollary
   `cor:triangular-block`, explicitly allows bridge blocks and arbitrary
   attached trees and gives strict positive credit to every connected
   triangular block graph containing a triangle.

Now consider the two cases at lines 97--111.

* If a maximal shared-cut cluster has size at least two, label **every** cluster
  subtree, not just the selected one. The selected territory has exactly that
  cluster's cycles and thus credit `>1`; every other territory contains its
  cluster and is a connected triangular block graph, so its credit is `>0`.
* If all clusters are singletons, choose two marked nodes at minimum distance.
  Their unique reduced-tree path has no third marked node. Label the full
  expanded connector path as one source and the other four triangle subtrees
  separately. The first territory is an arbitrary-connector two-triangle
  cactus and has credit `>1`; each other territory is triangular and positive.

Thus the Section 1 conclusion is mathematically supported. The finite
`research/six-triangle-margin-scout.py` census checks selected bare incidence
models and characteristic polynomials; it cannot prove arbitrary connector,
Steiner, or rooted-tree scope. Those quantifiers come from the physical
partition and the cited attachment-uniform analytic theorems.

### 1.3 Line-level clarification requested

Lines 68--76 should say explicitly that the sources are expanded full cluster
subtrees in the **physical** block-cut tree, and that contraction is undone
before cutting one actual bridge on each inter-class route. Lines 77--80 should
add the unique-attachment argument for every off-hull component. No theorem
change is needed; this is a proof-domain clarification.

## 2. Simultaneous first-actual-bridge split: accepted

Lines 178--188 correctly use the deduplicated set of first/rootmost K2 blocks
on all routes from the `D` cluster to an external cyclic block. In the rooted
block-cut tree, two distinct first bridges cannot be ancestor and descendant:
if the ancestor lies on a route, the descendant is not first on that route.
Deleting the antichain simultaneously therefore makes one root component and
one complete descendant component per first bridge. A later bridge or nested
cycle remains in that complete away component; no second cut is licensed.

The split is on physical bridge **edges**. Hence its components partition the
original vertices, are connected, and become induced territories by taking the
induced graph on each vertex set. A bridge not on a root-to-external-cycle
route is payload and must not be cut. These observations cover repeated cuts,
nested triangles, positive-length K2 chains, connector branch points, and
Steiner topology. An away group containing a triangle is a connected
triangular block graph. At most one away group can contain the unique pentagon
and no triangle; its exact floor is the non-strict radical inequality discussed
in Section 5 below.

The counts at lines 192--202 are irrelevant to this proof. They may be useful
regression checks, but neither Bell counts nor a reduced quotient proves the
original-vertex ownership asserted at lines 184--188.

## 3. Narrow bridge-free `D+T^k`: accepted with corrected derivation

### 3.1 Selector

In a rooted bridge-free shared-cut incidence tree with `k>=2`, choose the two
triangle block nodes of least depth from `D`, not merely an unspecified pair.
If a third triangle lay in the union of their two root paths, it would be a
proper ancestor of one selected triangle and hence have smaller depth. Thus the
minimal hull contains exactly `D` and the selected two triangles and no K2
block. It is within the exact scope of
`positive-square-energy/pentacyclic-general/diamond-two-triangle-exact-packet.md`:
direct/direct or direct/nested shared-cut incidence, arbitrary one-root tree
branches, no positive bridge connector, and `sigma>3`.

The 307-state selector executable confirms this combinatorial fact only for
its canonical incidence quotient. The least-depth argument is the proof and
covers repeated owners and nested triangles without relying on that census.

### 3.2 Boundary cuts on original vertices

Take the cut closure of the selected incidence hull: every represented cut
incident with a retained `D`/triangle block remains upstream. At each frontier
`c -> unselected triangle`, keep `c` upstream and take the complete component
of the physical block-cut tree beyond that incidence, with `c` removed, as one
set `W`. If two unselected triangles leave the same cut, they are different
block-cut branches and yield disjoint `W` sets. If another triangle is nested
below the first, it remains in that same `W`; do not cut it again.

Each nonempty `W` is connected; distinct sets cannot share a vertex other than
the upstream cut, which was excluded from all of them. Every connector remnant,
Steiner branch, and rooted acyclic component follows its unique physical root.
After taking induced subgraphs, upstream plus the `W` sets are disjoint and
exhaustive. There is at most one `W` per nonempty group of unselected
triangles, so `m<=k-2`.

The only floor needed is `sigma(W)>=-1`. Its cases have exact scope:

* rank zero: a nonempty connected acyclic `W` is a tree, so `sigma=-1`;
* rank one: `W` is unicyclic with arbitrary attached trees, and the established
  unicyclic floor is strictly greater than `-1` (including hostile lengths);
* rank at least two: `W` is a cactus whose cyclic blocks are triangles, because
  the root cluster contains only `D` and literal triangles and `D` remains in
  the anchor. The rank-uniform nonunicyclic cactus theorem, or more narrowly
  the triangular-block theorem, gives strict positive credit, hence certainly
  nonnegative.

Thus

```text
sigma(D+T^k) > 3-m >= 3-(k-2).
```

For `k=3` this is `>2`; for `k=4` it is `>1`. This proves exactly the narrow
line-206 scope. It does **not** prove a free-standing spectral theorem for an
arbitrary graph merely described symbolically as `D+T^k`; the physical
bridge-free shared-cut and unique-root-branch hypotheses are indispensable.

### 3.3 Line-level repair requested

Lines 214--218 should replace “select two triangles” with the least-depth
selection and should spell out the cut closure and original-vertex frontier
sets before quoting their floors. The current compact wording states the right
result but leaves the crucial no-third-triangle and no-duplicated-cut arguments
implicit. This is not the fatal blocker; the longer conditional proof already
exists in `research/r21-hostile-p-complement-reduction-2026-11-14.md`, lines
130--186.

## 4. Retained pentagon: concrete ownership blocker

### 4.1 The defect

Section 3 first deletes `E_0` and creates disjoint root and away groups. But
lines 233--237 then say, without restricting the ambient graph:

```text
Delete the five pentagon edges. For each w in V(P), let F_w be the
component of G-E(P) containing w.
```

If the retained `P` shares an articulation `c` with the root group while a
triangle lies beyond a first bridge elsewhere in that root group, the full-`G`
component `F_c` includes that already separated triangle-away group through its
bridge route. Consequently `A=G[V(F_c)]` at line 244 contains an away group,
while line 264 says all first-bridge away groups remain disjoint. Both cannot
be true as an original-vertex partition.

This is a logical gap, not a spectral counterexample. The bounded checker
`research/r21-retained-pentagon-owner-fibre-checker.py` constructs exactly this
legal rank-seven graph:

* `D`, three triangles, and `C5` share `x` in the root group;
* the fourth triangle is attached beyond the actual bridge `x--b`;
* deleting `x--b` gives a 14-vertex root group and a 3-vertex away group;
* deleting C5 edges in full `G` gives a 13-vertex parent fibre, which includes
  the 3 away vertices;
* deleting C5 edges in the induced root group gives the correct 10-vertex
  parent fibre.

Both operations produce five formal C5 owner components, so merely counting
fibres cannot catch the mistake. The ambient vertex set is the issue.

### 4.2 Exact repair

Immediately after Section 3, name the root territory

```text
R = G[V_R],
```

where `V_R` is the component containing `D` after simultaneous deletion of the
first bridges `E_0`, and regard `R` as the induced graph on that vertex set.
Then replace lines 233--251 by the following scoped construction:

```text
Suppose P remains in R. Let c be the parent articulation of its block node in
the block-cut tree of R. Delete E_R(P), the five P-edges, from R. For each
w in V(P), let F_w be the component of R-E_R(P) containing w. Maximality of
the P block implies these are five distinct components, each meeting P exactly
at w, and they partition V(R).

Set
A  = R[V(F_c)],
B' = R[ union_(w != c) V(F_w) ].
```

The ear argument is now applied inside `R`. The four nonparent owners are
joined by `P-c`, a four-vertex path. Therefore `A,B'` are connected induced,
vertex-disjoint, and exhaustive **in `R`**, and the only `R`-edges crossing are
the two P-edges at `c`. Every first-bridge away group lies in `G-V(R)` and is
therefore automatically disjoint from both.

With this correction, the `q=0/q>=1` ledger is valid:

* `A` has exactly `D+T^(t-q)` as its positive-rank shared-cut cluster and all
  other material is a one-root branch, so the narrow bound gives `sigma(A)>1`;
* if `q=0`, `B'` is connected and acyclic: removing all P edges leaves four
  owner trees, while restoring the three edges of `P-c` connects them without
  a cycle. It is nonempty, hence `sigma(B')=-1`;
* if `q>=1`, every surviving positive-rank block of `B'` is a literal triangle;
  `P-c` and all connector material are bridges/trees. Thus `B'` is a connected
  triangular block graph and has `sigma(B')>0`.

So the desired strict sum follows after the scoping repair. Repeated owner cuts,
nested triangles, and branches at `c` are handled because the complete owner
component follows its owner; no owner vertex is copied.

### 4.3 Exact C5 floor

Line 190 currently says that a P-only away group has credit “strictly greater
than `-(sqrt(5)-2)`.” This is false for bare `C5`. Its eigenvalues give

```text
s+(C5)=7-sqrt(5),
sigma(C5)=s+(C5)-5=2-sqrt(5)=-(sqrt(5)-2).
```

The cited arbitrary-tree unicyclic theorem supplies

```text
sigma(P-only) >= -(sqrt(5)-2) > -1.
```

The second inequality is strict because `2<sqrt(5)<3`. That is all the ledger
needs. Make the same non-strict-first-comparison correction anywhere the draft
calls the general P-only packet strictly greater than the exact radical.

## 5. Executable evidence and trust boundary

Run:

```text
python3 research/r21-retained-pentagon-owner-fibre-checker.py
python3 -O research/r21-retained-pentagon-owner-fibre-checker.py
```

The checker uses no Python `assert`, compares normal and optimized output,
runs a Tarjan edge-stack decomposition, authenticates the exact block profile
`D+T^4+C5`, checks original-vertex C5 fibres, computes exact integer
characteristic polynomials, and exhibits the full-`G` versus root-`R` fibre
size difference above. It also materializes the bridge-isolated and all-shared
profiles to show that an isolating-bridge-only gate is not exhaustive.

Its floating-point `sigma` values are explicitly nonproof counterexample-search
evidence. Its exact characteristic polynomials certify the materialized finite
fixtures, not arbitrary attachment or connector quantifiers. The general
owner-fibre theorem is the maximal-block ear argument; the general spectral
floors are the separately cited analytic theorems.

## 6. Final line-level decision

**ACCEPT after clarification:**

* lines 55--111, provided lines 68--80 explicitly operate on expanded physical
  cluster subtrees and state unique ownership of off-hull branches;
* lines 178--188, simultaneous first-bridge antichain split;
* lines 206--226, provided lines 214--218 name least-depth selection, cut
  closure, and original-vertex first-boundary territories;
* lines 253--263 (`q=0/q>=1`) after the ambient root-group repair.

**BLOCK on current bytes:**

* line 190: wrong strictness at the exact C5 radical; change `>` to `>=` at the
  first comparison;
* lines 233--245: `F_w` and `A,B'` are formed in full `G`; replace their ambient
  graph by induced root group `R`;
* line 264: “away groups remain disjoint” is unjustified until that replacement
  is made;
* lines 264--266 and 270: the `D+T^4+P` row and complete `R21` theorem cannot be
  declared closed on the current bytes.

Accordingly the precise audit status is **BLOCK**, with no known spectral
counterexample and with a local proof repair identified and finitely witnessed.
