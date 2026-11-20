# Exact physical-hull bridge reduction at cyclomatic rank seven

**Status.** Candidate theorem note; nonpromotional; no claim that the remaining
marked rank-`(1,6)` states are closed.

For a finite graph `H`, write

```text
beta(H)=|E(H)|-|V(H)|+c(H),
sigma(H)=s+(H)-|V(H)|,
s+(H)=sum_{lambda_i(A_H)>0} lambda_i(A_H)^2.
```

All graphs in the theorem statements are finite and simple; `c(H)` is the
number of connected components.

All cuts below are cuts of actual bridge edges.  Every territory is a set of
original vertices, and all uses of superadditivity are uses of induced
subgraphs on pairwise disjoint original-vertex sets.  In particular, no
articulation vertex is silently assigned to two owners.

## 1. Dependencies and the exact claim boundary

The combinatorial statements in Sections 2--4 are proved here from first
principles.  The spectral dispatch in Section 5 is conditional only on the
following established receipts.

* **(S)** Induced-subgraph superadditivity:
  `s+(G)>=sum_i s+(G[V_i])` for every vertex partition.
* **(L2--L6)** Every connected graph of cyclomatic rank `r`, `2<=r<=6`,
  satisfies `sigma>=0`; the rank-two result is strict.  These are used only at
  their stated connected ranks, not as quantified credit at ranks `3,...,6`.
  The exact local sources and current SHA-256 locks are

  ```text
  r=2  all-bicyclic-graphs/paper.tex
       56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da
  r=3  all-tricyclic-graphs/paper.tex
       4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02
  r=4  all-tetracyclic-graphs/paper.tex
       70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f
  r=5  all-pentacyclic-graphs/paper.tex
       8ce140b07dc1428656b4ffd914305f2b14b49a0555cd13a6fc87be0fd4246a18
  r=6  all-hexacyclic-graphs/paper.tex
       0e7a2db2932d38a4b4909831c34050553afc0973869fe937eb510cb59421bda7
  ```

  The rank-three source also contains receipt (S).  Hashes authenticate the
  cited local bytes, not external review or mathematical truth.
* **(U)** The attachment-uniform unicyclic receipts in Theorem 2 below.

Receipt (U) is already proved, with arbitrary attached trees, in

* `all-tricyclic-cacti/paper.tex`, Lemma `lem:packets`, item 2 and its proof
  (current SHA-256
  `d928a56b0257936fcc326ddc2c85e40593117a7749b55502bb42379c805e71e8`),
  and independently restated in
* `all-tetracyclic-cacti/paper.tex`, Lemma `lem:packets`, item 2 and its proof
  (current SHA-256
  `196a7cab1125404114de0cf94430919441f01cac9c72cbf4f5576bcd1daf2180`).

The qualitative favorable sign used below is Theorem `thm:main(i)` of
`packing-two-square-energy/paper.tex` (current SHA-256
`9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791`),
whose proof is self-contained there; it specializes to a unicyclic graph.
That theorem records the odd-unicyclic result of Ning--Zeng as prior work, but
no external paper is needed for the displayed repository proof.

The present note reconstructs the short matching-message argument in Theorem 2
so that its use is explicit.  It does **not** independently re-prove the full
signed Coulson identity; that identity is a dependency of the cited proofs.
Consequently, if the cited repository theorems are treated as unauthenticated,
all spectral conclusions below are conditional, while the weighted-tree
classification remains unconditional.

## 2. Rank-one sides: exact structure and sharp uniform receipt

### Lemma 1 (rank-one induced side)

Let `U` be a finite connected **simple** graph with `beta(U)=1`.  Then `U` has
a unique cycle `C_q`, and every edge outside this cycle belongs to a tree that
meets `C_q` in exactly one root vertex.  Equivalently, `U` is `C_q` with an
arbitrary finite rooted tree identified at each cycle vertex.  The root trees
may be trivial and may branch.  If `U` is one side of a bridge cut in a larger
graph, its marked bridge port may be any vertex of `U`, including an interior
vertex of an attached tree.

**Proof.** A connected graph has a spanning tree with `|V(U)|-1` edges.  Since
`beta(U)=1`, exactly one edge remains, and adjoining it creates one cycle.
Every edge not on that cycle is a bridge: a second nonbridge edge would lie on
a second cycle and give cycle-space dimension at least two.  Removing the
cycle edges therefore leaves a forest.  Any forest component meets the cycle
vertex set in at most one vertex, since its unique path between two such
vertices together with either cycle arc would create an additional cycle.
Equivalently, each off-cycle tree is identified with the cycle at one root.
This is precisely the rooted-tree description. `QED`

### Theorem 2 (sharp attachment-uniform unicyclic receipt)

Let `U` be as in Lemma 1, with unique cycle length `q`.  Put

```text
delta_q=sec(pi/q)-1            when q=1 (mod 4).
```

Then:

1. if `q` is even, `sigma(U)=0`;
2. if `q=3 (mod 4)`, `sigma(U)>0`;
3. if `q=1 (mod 4)`,
   `sigma(U)>=-delta_q=1-sec(pi/q)`.

The third bound is best possible over all rooted-tree data and over every
choice of marked bridge port: the bare cycle `U=C_q` has equality and may be
marked at any vertex.  Moreover,

```text
0<delta_q<=delta_5=sqrt(5)-2,
```

because `q>=5` and `sec(pi/q)` decreases with `q` on this range.

There is no positive attachment-uniform constant in item 2.  Indeed, let
`U_t` be a triangle with `t` pendant leaves at each cycle vertex.  Leaf
differences give `3(t-1)` zero eigenvalues.  For each triangle eigenvalue
`mu in {2,-1,-1}`, the two remaining eigenvalues are the roots of
`x^2-mu*x-t`; hence the positive root is
`(mu+sqrt(mu^2+4t))/2`.  Squaring and summing gives the exact surplus

```text
sigma(U_t)=2 sqrt(t+1)-sqrt(4t+1)>0,
```

which tends to zero.  Thus item 2 supplies strict positivity but no spendable
quantified token.

**Proof.** If `q` is even, `U` is bipartite.  Its spectrum is symmetric about
zero and `|E(U)|=|V(U)|`, so

```text
s+(U)=|E(U)|=|V(U)|,
```

which proves item 1.

For odd `q`, orient every off-cycle tree toward its cycle attachment.  For any
forest `F`, define its matching partition function by

```text
Z_F(t)=sum_{M matching in F} t^(|V(F)|-2|M|).
```

For vertex activities `a=(a_v)`, use the multivariate form

```text
Z_F(a)=sum_{M matching in F} product_{v unmatched by M} a_v.
```

For an oriented branch `T_{u->p}`, put

```text
Q_{u->p}(t)=Z_{T_{u->p}}(t)/Z_{T_{u->p}-u}(t).
```

Splitting a matching according as `u` is unmatched or matched to one child
gives the exact recursion

```text
Q_{u->p}(t)=t+sum_{w child of u} 1/Q_{w->u}(t) >= t.          (2.1)
```

Let `B=T_{u->v}` range over the top-level branches attached to cycle vertices
and set

```text
K(t)=product_B Z_B(t),
a_v(t)=t+sum_{B=T_{u->v}} Z_{B-u}(t)/Z_B(t)
      =t+sum_{B=T_{u->v}} 1/Q_{u->v}(t) >= t.                 (2.2)
```

Splitting matchings according to each attachment edge gives the two exact
identities

```text
Z_U(t)=K(t) Z_{C_q}(a(t)),
Z_{U-V(C_q)}(t)=K(t).                                        (2.3)
```

Thus the same positive factor occurs in the matching term and in the Sachs
term deleting the cycle.  With the signed imaginary-axis convention of the
cited proofs,

```text
Psi_U(t)/K(t)=Z_{C_q}(a(t))+2i       if q=1 (mod 4),
Psi_U(t)/K(t)=Z_{C_q}(a(t))-2i       if q=3 (mod 4).           (2.4)
```

The multivariate matching polynomial has nonnegative coefficients, so (2.2)
gives

```text
Z_{C_q}(a(t))>=Z_{C_q}(t)>0.                                 (2.5)
```

Consequently the phase in (2.4) lies between zero and the bare-cycle phase
`arg(Z_{C_q}(t)+2i)`.  The signed Coulson identity, with the sign and continuous
branch fixed in the cited proofs, therefore bounds the asymmetry of `U` below
by that of `C_q`.  Since `|E(U)|=|V(U)|`, asymmetry divided by two is exactly
`sigma(U)`.  The exact cycle spectrum `2 cos(2 pi j/q)` gives

```text
s+(C_q)=q+1-sec(pi/q),
sigma(C_q)=1-sec(pi/q)=-delta_q.                              (2.6)
```

This proves item 3 and sharpness.

For `q=3 (mod 4)`, the Sachs cycle multiplier is `-2i`.  The normalized curve
lies strictly in the lower half-plane for every `t>0`; its continuous argument
is strictly negative, so the signed Coulson identity gives positive
asymmetry.  Again `|E(U)|=|V(U)|`, hence `sigma(U)>0`.  This is also the
unicyclic specialization of the cited favorable-cycle theorem. `QED`

**Root-data interpretation.** The exact instance-specific value of
`sigma(U)` is determined by all messages in (2.1), hence by the rooted-tree
shapes, their locations on the cycle, and the marked port only when the later
bridge interaction is considered.  It is generally not one of finitely many
numbers.  What is finite is the universal receipt type

```text
EVEN: 0;       FAVOURABLE_ODD: strict 0;       HOSTILE(q): -delta_q.
```

For universal hostile dispatch, the single worst cap is `delta_5`.

## 3. The full physical bridge tree

Let `G` be a finite connected graph with `beta(G)=7`.  Delete **all actual
bridge edges**.  Let the resulting connected components be `X_v`, and let `T`
have one vertex `v` for each `X_v` and one edge for each deleted bridge.
Assign weight

```text
rho(v)=beta(X_v).
```

### Lemma 3 (physical bridge quotient)

If `G` has at least one bridge, `T` is a tree; if it has no bridge, `T`
is the one-vertex tree.  Every `rho(v)` is a nonnegative integer, and

```text
sum_{v in V(T)} rho(v)=7.                                    (3.1)
```

For every edge `e=uv` of `T`, deleting the corresponding physical bridge of
`G` gives two connected, induced, disjoint, exhaustive original-vertex sides.
Their cyclomatic ranks are the two component weight sums of `T-e`.

**Proof.** Contracting the components of `G` after all bridges are deleted
preserves connectedness.  A cycle in the quotient would make each of its
physical bridge edges lie on a cycle in `G`, impossible; hence the quotient is
a tree.  For a bridge joining connected graphs `A,B`,

```text
beta(A + bridge + B)=beta(A)+beta(B).
```

Induction over the quotient tree proves (3.1) and the edge-side rank formula.
A bridge deletion in a connected graph has exactly two connected components;
the subgraphs induced by their vertex sets contain all noncrossing edges, and
the bridge is the sole crossing edge.  Thus the sides are induced and form an
original-vertex partition. `QED`

We use this direct all-bridge-component quotient throughout.  We do **not**
identify it with the ordinary block--cut incidence tree: deleting a leaf
bridge-block node there can discard its non-articulation endpoint.  An
incidence-tree reformulation would have to augment the block--cut tree with
all original vertices, including non-articulation bridge endpoints.  The
direct quotient above already retains every original vertex exactly once.

Let `K` be the minimal subtree of `T` containing every positive-weight vertex.
Call it the **positive hull**.  A zero-weight component outside `K` has a unique
first attachment to `K` and stays whole with that owner.  Within `K`, suppress
every zero-weight degree-two vertex, recording the corresponding full physical
bridge chain.  Call the resulting weighted tree `K_red`.  No zero-weight leaf
can occur in `K`; every zero-weight vertex of `K_red` therefore has degree at
least three.

### Lemma 4 (finite reduced size)

If `p` is the number of positive-weight vertices, then `2<=p<=7` whenever a
hull edge exists, and

```text
|V(K_red)|<=2p-2<=12.                                         (3.2)
```

**Proof.** There are at most seven positive vertices because their positive
integer weights sum to seven.  Let `z` be the number of zero-weight vertices
of `K_red`.  Each such vertex has degree at least three, while every leaf is
positive.  In any tree, the number of degree-at-least-three vertices is at most
the number of leaves minus two.  Hence `z<=p-2`, proving (3.2). `QED`

### Theorem 5 (balanced edge or unit-star obstruction)

Let a finite tree have nonnegative integer vertex weights summing to seven.
Assume its positive hull `K` has an edge, equivalently that at least two
vertices have positive weight.  Then exactly one of the following holds.

1. Some edge of `K` has side-weight split `r | (7-r)` with
   `r in {2,3,4,5}`.
2. Every edge of `K` has split `1|6`.  After pruning zero-weight off-hull
   branches and suppressing zero-weight degree-two hull vertices, `K_red` is a
   star.  Every leaf has weight one.  If it has `k` leaves, its center has
   weight `7-k`; hence `1<=k<=7`.  The center may have weight zero only in the
   `k=7` case.  (When `k=1`, both endpoints are positive, with weights `1,6`.)

Conversely, every weighted star described in item 2 has only `1|6` splits.
Arbitrary lengths of the suppressed physical bridge chains do not change the
classification.  No assertion is made for a one-vertex positive hull of
weight seven: that case has no hull bridge, for example a rank-seven
bridge-free core with an arbitrary pendant tree.

**Proof.** The alternatives are disjoint because an item-2 edge has no side
weight in `{2,3,4,5}`.  Suppose item 1 fails.  Every hull edge has two positive
side weights summing to seven, so every split is `1|6`.

Choose a weighted centroid `c`: orient an edge toward a side of weight greater
than `7/2` whenever such a side exists.  At most one incident side can have
weight greater than `7/2`; each step strictly advances along a finite tree, so
this process stops at a vertex for which every component of `K-c` has weight
at most `3`.  Each such component is an edge side and is nonempty in the
positive hull.  Because every edge split is `1|6`, its weight must therefore
be exactly one.

Now take a component `C` of `K-c`.  If `C` had two positive-weight vertices,
its total weight would be at least two.  If it had one positive vertex of
weight at least two, the same would hold.  Thus `C` has exactly one positive
vertex, of weight one.  Every other vertex of `C` is zero-weight.  In the
reduced tree, a zero-weight vertex cannot be a leaf or have degree two.  A
zero-weight vertex inside `C` of reduced degree at least three would have at
least two branches away from `c`, each containing a positive hull vertex, so
`C` would have weight at least two.  Therefore suppression reduces `C` to one
weight-one leaf adjacent to `c`.  This proves the star form.  The center weight
is the remaining `7-k` and is nonnegative, so `k<=7`.

Conversely, cutting any star arm isolates its unit leaf, giving `1|6`.
Subdividing an edge by any number of zero-weight degree-two vertices repeats
the same side split along that physical chain and creates no new side weight.
`QED`

The dependency-free verifier at
`research/physical-hull-weighted-tree-verifier.py` exhausts every unlabelled
reduced tree allowed by
(3.2), every legal zero-weight branching support, and
every positive integer weighting of total seven.  It separately expands and
resuppresses zero-weight bridge chains.  It is corroboration only; Theorem 5
has the preceding proof.

## 4. Reselection of a hull bridge cannot always help

### Proposition 6 (sharp failure of repeated bridge choice)

For each number `p in {2,...,7}` of positive bridge-free components, there is a
rank-seven connected graph whose positive hull has no edge split in
`{2,...,5}`.  For each `p in {3,...,7}`, this remains true despite having at
least three positive components, and every detachable rank-one side can be
chosen hostile.

**Construction and proof.** A concrete simple bridge-free graph of every rank
`r in {1,...,6}` is `K_{2,r+1}`, whose cyclomatic rank is `r` (for `r=1` one
may instead take `C_5`).  For `p=2`, join a rank-six such graph to one `C_5` by
a bridge.  For `3<=p<=7`, take a bridge-free connected central graph of rank
`8-p` and attach `p-1` disjoint copies of `C_5` to it by independent bridge
arms.  For `p=7`, choose `C_5` also as the rank-one center if one wants every
positive component hostile.  The weights are

```text
central weight 8-p;     p-1 leaf weights 1.
```

They sum to seven.  Every hull edge isolates exactly one `C_5`, so every split
is `1|6`, and every available rank-one leaf has cycle length `1 mod 4`.
Subdividing any arm by an arbitrary bridge chain changes nothing.  Thus neither
choosing a different hull bridge nor requiring at least three positive blocks
forces a favorable rank-one side or a rank split `2,...,5`. `QED`

After cutting one arm, the remainder has rank six.  Repeating the operation
inside that remainder is not a new rank-seven split.  Plainly summing separate
rank-one receipts would accumulate hostile debits, and the known theorem for
the complete rank-six remainder supplies only `sigma>=0`; therefore this
sequential bookkeeping cannot pay the already detached debit.  Nor can one
generally pair several arms as disjoint induced territories: paths between
arms run through the same central original component, which cannot be owned by
two territories.

## 5. Exact dispatch theorem and rooted deficit DP

### Theorem 7 (physical-hull dispatch)

Assume receipts (S), (L2--L6), and (U).  Let `G` be connected with
`beta(G)=7` and with a nontrivial positive hull.

1. If Theorem 5(1) holds, then `sigma(G)>=0`; indeed a `2|5` split is strict.
2. If Theorem 5(2) holds and some unit leaf side is even, then
   `sigma(G)>=0`.
3. If Theorem 5(2) holds and some unit leaf side has cycle length `3 mod 4`,
   then `sigma(G)>0`.
4. Otherwise every detachable unit leaf is a hostile unicyclic side with
   cycle length `1 mod 4`.  Choosing any one such side `U` leaves a connected
   induced rank-six complement `R`.  The plain induced-partition argument
   closes this cut **whenever** one has a proved receipt

   ```text
   sigma(R) >= d(U),                                           (5.1)
   ```

   where any certified `d(U)` satisfying `sigma(U)>=-d(U)` may be used.  The
   sharp cycle-only uniform choice is `d(U)=delta_q`; a single bound uniform
   in all hostile cycle lengths and rooted-tree data is

   ```text
   sigma(R) >= delta_5=sqrt(5)-2.                              (5.2)
   ```

**Proof.** In case 1, delete the physical bridge supplied by Theorem 5.  Its
two original-vertex sides have connected ranks in `{2,...,5}`.  Receipts
(L2--L6) give nonnegative surplus on both, with strictness on a rank-two side;
(S) sums the receipts.  In cases 2 and 3, cut the indicated unit arm.  The
complement has rank six and hence nonnegative surplus; Theorem 2 supplies,
respectively, zero or strict positive surplus for the arm.  In case 4,

```text
sigma(G)>=sigma(R)+sigma(U)>=sigma(R)-d(U),                    (5.3)
```

so (5.1) suffices.  Theorem 2 gives `d(U)=delta_q<=delta_5`, proving (5.2).
`QED`

A weak inequality in (5.1) suffices: the hostile receipt itself is weak.  A
qualitative statement `sigma(R)>0` with no numerical lower bound does **not**
suffice.  Strictness may be propagated only as a Boolean fact after the
numeric ledger has reached zero; it cannot be spent against `delta_q`.

### Coupled bridge gain

For marked ports `x in V(R)`, `y in V(U)`, define the actual one-edge gain

```text
Gamma(R,x;U,y)
 =s+(R + xy + U)-s+(R)-s+(U).                                 (5.4)
```

Because `|V(R+xy+U)|=|V(R)|+|V(U)|`, the exact identity is

```text
sigma(G)=sigma(R)+sigma(U)+Gamma(R,x;U,y).                     (5.5)
```

Thus a coupled marked-port theorem may replace (5.1) by

```text
Gamma(R,x;U,y) >= d(U)-sigma(R).                               (5.6)
```

This is a genuinely new analytic obligation.  Superadditivity yields only
`Gamma>=0`.  No universal gain of size `2/3` may be assumed: the exact
counterfamily in
`research/open-audits/rank-one-six-bridge-gain-obstruction-2026-11-18.md`
(current SHA-256
`62c255e495f10c128e1adbfd4b124e00f3a92ff084b09730c81ed81d400ef685`)
has a finite member with `Gamma<2/3`.  That source gives an upper-bound
obstruction, not a lower bound and not closure of (5.6).

### Exact bridge-cut partitions and exhaustive recursion

Fix a graph `G` and its direct all-bridge-component quotient tree `T` from
Lemma 3.  A **bridge cut set** is a subset `F of E(T)`.  Its terminal owners
are the original-vertex graphs obtained from the components of `T-F`: for a
component `C`, its owner vertex set is

```text
W_C = union_{v in V(C)} V(X_v),
```

and its owner is `G[W_C]`.  Let a **receipt library** assign a proved numerical
surplus floor and strictness bit to specified connected induced owner graphs.
An unquantified conclusion `sigma>0` is represented by numeric floor zero and
a strictness bit; it is never spent as positive credit.

### Lemma 8 (cut sets are exactly connected-subtree partitions)

The map

```text
F  ->  components of T-F
```

is a bijection from edge subsets of `T` to partitions of `V(T)` into nonempty
connected vertex sets.  Under expansion `C -> W_C`, it is a bijection to the
partitions of `V(G)` obtained by simultaneously deleting physical bridges.
Every expanded part induces one connected graph, and the expanded parts are
pairwise disjoint and exhaustive on original vertices.

**Proof.** Deleting `F` from a tree gives connected components.  Conversely,
if `P` is a partition of `V(T)` into connected parts, let `F_P` be the edges
whose endpoints lie in different parts.  Each part remains connected in
`T-F_P`, while no edge joins two parts, so the components are exactly `P`.
Thus the constructions are inverse.  Lemma 3 says quotient edges are exactly
physical bridges and quotient vertices are disjoint exhaustive original-vertex
components.  Expanding a connected quotient subtree therefore gives a
connected induced original-vertex graph, with no duplicated endpoint or
articulation. `QED`

Root `T`.  The following recursion enumerates all bridge cut sets without any
schematic owner equivalence.  At every child edge choose exactly one bit:

* `0` (keep): retain the edge in the current connected subtree;
* `1` (cut): put the edge in `F`, thereby starting a new terminal subtree on
  the child side.

After all edges are processed, reconstruct the components of `T-F`, expand
each by Lemma 8, and accept this leaf of the recursion exactly when the fixed
receipt library authenticates every expanded owner and the sum of its numeric
floors is nonnegative.  Strictness changes a zero total from weak to strict;
it never cancels a negative numeric total.

### Corollary 9 (exact exhaustive full-tree search)

For a fixed finite `G`, the recursion has exactly `2^{|E(T)|}` leaves and is
sound and complete for simultaneous physical-bridge cut-partition
certificates using the fixed receipt library.

**Proof.** Binary choices give every subset `F` exactly once.  Lemma 8 gives
exactly its connected induced original-vertex owners.  Induced
superadditivity makes every accepted summed receipt sound.  Conversely, every
certificate in the stated class has one bridge cut set and hence occurs at its
unique recursion leaf. `QED`

This is deliberately a cut-set theorem, not a claim about arbitrary nested or
entry-sensitive packet openings inside a retained owner.  Such an opening
requires its own ownership theorem and cannot be inferred from Lemma 8.

The full-tree recursion is finite for each finite graph but is not bounded by
rank: an actual K2 chain can be arbitrarily long.  A bounded reduced recursion
therefore needs a stronger receipt hypothesis.

Call a receipt library **iterated zero-rank absorption stable for a proposed
reduction** if every receipt on an allowed connected owner remains valid, with
the same numeric floor and strictness, after attaching any finite family of
finite trees at any finite multiset of owner vertices that can occur as
endpoints of bridge edges restored by that reduction.  Every such endpoint
must be an allowed absorption port; repeated attachments at the same port are
permitted.  The statement must hold after every finite sequence of such
attachments, not merely for one tree at one port.  If port data matter, the
library must also provide a finite equivalence typing of their configurations;
an unbounded length or port list stored verbatim is an analytic parameter, not
a finite state.

### Lemma 10 (safe reduction of simultaneous cut partitions)

For a receipt library iterated zero-rank absorption stable for the reduction
below, every successful simultaneous bridge-cut partition is dominated by one
in which

1. every zero-weight branch outside the positive hull is absorbed whole into
   its unique adjacent hull owner; and
2. no maximal zero-weight degree-two hull chain is cut more than once.

Here `dominated` means that the new partition is another successful
certificate using the same library, its numerical ledger is no smaller, and
its strictness is not weakened when the old and new numerical ledgers both
vanish.  Consequently every resulting cut topology projects to a subset of
`E(K_red)`, which has at most eleven edges and hence at most `2^11` projected
outer topologies.  Cut position along a suppressed chain and owner, port, or
message data remain parameters unless the stated finite equivalence typing
identifies them.  With such a finite receipt/port alphabet this is a genuinely
finite reduced recursion; otherwise it is only a finite collection of
parametric outer schemas.

**Proof.** Every component of `T-K` is a zero-rank tree attached to `K` at one
first quotient vertex.  Restore all cuts in such a component and absorb its
entire original-vertex tree into the adjacent hull owner.  Distinct off-hull
components, and several components at the same owner, require repeated and
multi-port absorption; the stated hypothesis preserves that owner's receipt.
Every separate zero-rank terminal owner removed this way was a nonempty tree
with exact surplus `-1`, so the numeric ledger cannot decrease.

If a maximal zero-weight degree-two hull chain is cut at least twice, every
terminal component between two consecutive cuts expands to a nonempty tree of
surplus `-1`.  Restore one boundary bridge and absorb that complete middle
tree into either adjacent owner.  This may occur repeatedly and at ports
already used by earlier absorptions, so again the full iterated hypothesis is
needed.  Its receipt is unchanged and the separate `-1` disappears.  Iterate
until the chain has at most one cut.  Side ranks and the order of all positive
owners are unchanged.  Every surviving cut set projects to a subset of
`E(K_red)`; hence Lemma 4 gives at most `2^11` projected outer topologies.
The physical cut position and receipt data are retained as parameters unless
the stated equivalence typing identifies them. `QED`

The universal receipts used in Theorem 7 satisfy this absorption requirement
for the moves just made: (L2--L6) covers every connected graph of the stated
rank after arbitrary tree attachments, and Theorem 2 already covers arbitrary
rooted-tree families.  A packet-specific structural receipt does not inherit
this property; repeated/multi-port attachment stability and ownership must be
proved for that receipt.

Combining Theorems 5 and 7 with Lemmas 8 and 10 yields the following **relative
structural reduction** for graphs with nontrivial positive hull, within the
simultaneous physical-bridge cut-partition class and under the fixed receipts
(S), (L2--L6), and (U).  A balanced edge dispatches immediately.  In the
unit-star alternative, an even or favorable unit arm dispatches.  If neither
occurs, every detachable arm is hostile; choosing any one gives a marked
rank-`(1,6)` deficit state governed by (5.1) or (5.6).  There are at most seven
arm choices.  This is a finite family of outer state schemas, not a finite
classification of the rank-six graphs, marked ports, cycle lengths, or
rooted-tree message functions.

## 6. Relative hostile residual schemas

Among connected rank-seven graphs whose positive hull has an edge, and within
the simultaneous physical-bridge cut-partition method using only the fixed
receipts (S), (L2--L6), and (U), every graph not dispatched by Theorem 7 has
the following hostile **outer state schema**.

1. `K_red` is a weighted star with `k in {1,...,7}` unit leaves and center
   weight `7-k`.
2. Every detachable leaf side is a connected unicyclic graph whose unique
   cycle has length `q=1 mod 4`; each may carry arbitrary rooted trees, and its
   physical bridge port may lie anywhere in that side.
3. For every leaf choice tried by this fixed receipt method, the complete
   induced complement `R=G-V(U)` is connected of rank six.  It inherits the
   same center and all other unit hostile arms of the reduced star (or has a
   one-vertex positive hull of weight six when `k=1`), together with the
   retained zero-rank trees and chains.  Closure would require an additional
   receipt supplying either

   ```text
   sigma(R)>=delta_q,
   ```

   or the marked coupled inequality (5.6), or a stronger induced packet
   partition paying the same deficit.

The center may itself contain positive blocks and may absorb the other hostile
arms; it must not be replaced by a bare single-block rank-six object unless a
separate theorem proves that replacement.  Thus the complement is arbitrary
within this inherited unit-star residue, not literally arbitrary among all
rank-six bridge topologies.  A theorem for every marked connected rank-six
complement would be sufficient but stronger than necessary.  Marked
attachment orbits, physical chain lengths, path parities, rank-six owner types,
and the rooted-tree message data may remain analytic parameters.

One important closed subfamily illustrates the distinction.  If the rank-six
complement is a nonempty triangular cactus and the hostile arm is attached
through exactly one interface, the rooted all-rank guard in
`all-rank-triangle-hostile-cacti/paper.tex`, Theorem `thm:rooted` (current
SHA-256
`caa2c85d0416bd12bbbfd179f04bef9fe3293b83bca025acc6a2e83e53037230`),
gives `sigma>1-delta_q>0`.  It is a coupled owner theorem; it does not imply a
standalone reserve for an arbitrary rank-six complement or cover multiple
interfaces without a new ownership proof.

Accordingly, purely combinatorial reselection of a hull bridge does not
universally eliminate the hostile unit-star schemas.  Closing those schemas by
this method requires quantified rank-six marked reserve, marked bridge
interaction, or packet-specific original-vertex ownership.  This note makes no
exhaustive claim about all receipts already available elsewhere in the
repository, no claim about a one-vertex positive hull, and no claim that a
non-bridge or nested packet method cannot close additional cases.
