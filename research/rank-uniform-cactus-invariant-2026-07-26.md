# A rank-uniform cactus proof: residual theorem, guarded-hostility invariant, and the remaining obstruction

## 1. Scope and status

For a graph `G`, put

`sigma(G)=s+(G)-|V(G)|`.

This note isolates a possible rank-uniform proof of `sigma(G)>0` for every
connected cactus of cyclomatic number at least two. It distinguishes proved
reductions from candidate lemmas. No all-rank theorem is claimed here.

The main conclusions are:

1. the sharp DNN argument has the same two residual patterns at every rank;
2. the rank-by-rank incidence censuses can be replaced, if one proves one
   guarded-decomposition lemma and one common-cut absorption lemma;
3. the useful invariant is not a numerical lower bound depending on rank, but
   a rank-free assignment of one triangular guard to every negative
   distinguished cycle;
4. the existing shared-triangle opening recurrence is intrinsically a
   rank-seven method: from its four-triangle base it cannot prove rank eight;
5. the exact obstruction to a purely combinatorial interval decomposition is
   a multiway cut shared by a distinguished hostile cycle and arbitrarily many
   triangles. Every retained cycle needs the same vertex, so induced
   territories cannot separate them.

Theorems already established elsewhere give the desired strict conclusion for
cyclomatic ranks `2,...,7`. Thus rank seven is the exact maximal range of the
current four-triangle-reserve recurrence, not a proposed maximal range of the
truth of the cactus theorem.

## 2. Rank-uniform DNN residual classification (proved)

Let `G` be a connected cactus of cyclomatic number `r`. Let its cycle lengths
be `ell_1,...,ell_r`, and let `b` be its number of bridge blocks. Block
counting gives

`b+sum_i ell_i=|V(G)|+r-1`.

Define

`epsilon_ell=0` for even `ell`,

`epsilon_ell=ell tan^2(pi/(2ell))` for odd `ell`.

The sharp cactus DNN estimate gives

`sigma(G) >= r-1-sum_i epsilon_(ell_i)`.                    (2.1)

The odd sequence is strictly decreasing, with

`epsilon_3=1`, `epsilon_5=a=5-2sqrt(5)`,

`2a>1`, `3a<2`, and `epsilon_5+epsilon_7<1`.                (2.2)

Write `T=C3` and `P=C5`.

**Lemma 2.1 (all-rank residual classification).** If the right side of (2.1)
is not strictly positive, then the cycle multiset is in one of the two
families

`T^(r-1) Q`, where `Q` is an arbitrary cycle (and may itself be `T`), or

`T^(r-2) P P`.

Conversely, the DNN estimate alone does not prove strict positivity uniformly
on either displayed family.

**Proof.** Let `k` be the number of nontriangular cycles. Since every such
cycle has epsilon at most `a`,

`sum epsilon_i <= (r-k)+ka = r-k(1-a)`.

Failure of strict positivity in (2.1) requires

`k(1-a)<=1`.                                                  (2.3)

Now `3a<2` implies `3(1-a)>1`, so `k<=2`. If `k=0` or `k=1`, the multiset is
`T^(r-1)Q`, allowing `Q=T`. If `k=2`, (2.1) can fail only if the two
nontriangular epsilon values have sum at least one. An even cycle contributes
zero. For two odd cycles, (2.2) shows that any pair other than `5,5` has sum at
most `epsilon_5+epsilon_7<1`; the pair `5,5` survives because `2a>1`. This is
`T^(r-2)PP`. The all-triangle member has DNN lower bound `-1`, and the other
displayed families include zero or negative DNN lower bounds, proving the last
assertion. QED.

This lemma is the first census-free invariant: independently of `r`, at most
two cycles need special treatment.

## 3. Rank-free packet ledger (proved inputs)

Call an odd cycle `C_q` **hostile** when `q=1 mod 4`. Its unicyclic packet has

`sigma(C_q with arbitrary trees) >= -delta_q`,

where `delta_q=sec(pi/q)-1<1`. A pentagon has
`delta_5=sqrt(5)-2<1/4`. Even cycles and cycles of length `3 mod 4` are
nonnegative or strict in the established unicyclic ledger.

The following established packet facts are the only numerical facts needed by
the proposed rank-uniform invariant:

* a triangular unicyclic packet has `sigma>0`;
* a mixed `T C_q` packet has `sigma>1-delta_q>0` when `C_q` is hostile;
* a mixed `TP` packet has `sigma>1-delta_5>0`;
* a `PP` packet in one shared-cut cluster is nonnegative;
* every connected triangular cactus containing a triangle has `sigma>0`.

All packets permit arbitrary attached trees; connector territories are cut
only on actual bridge edges. Therefore induced-subgraph superadditivity adds
their surpluses without any edge-monotonicity assumption.

## 4. The proposed invariant: guarded hostility

A **guarded territory decomposition** of a residual cactus is a vertex
partition into connected induced subgraphs satisfying the following rules.

1. Every hostile distinguished cycle belongs either to a territory certified
   as a positive mixed packet (in particular, an exact `TQ` or `TP` packet),
   or (only for the two-pentagon residual) both pentagons belong to one
   certified nonnegative `PP` territory.
2. A triangle used to guard one hostile territory is not used in another.
3. Every remaining cyclic territory is triangular.
4. At least one territory is strict. This is automatic if a guarded mixed
   territory exists, or if a triangle remains outside a nonnegative `PP`
   territory.

**Lemma 4.1 (guarded ledger, proved).** Every residual cactus admitting a
guarded territory decomposition has `sigma(G)>0`.

**Proof.** A guarded hostile territory is positive by its required packet
certificate; merely containing a triangle is not enough. Every unguarded
triangular territory has positive surplus. The only allowed weak territory is
`PP`, and in that case a remaining triangular territory is strict. Add the
bounds by induced-subgraph superadditivity. QED.

This is the desired rank-independent invariant. It records a matching between
negative demands and triangular guards, not a surplus that deteriorates with
the total number of cycles. Lemma 2.1 bounds the number of demands by two at
every rank.

One may encode it numerically by assigning demand `delta_q<1` to a hostile
distinguished cycle and one unit of guard credit to a triangle in the same
mixed packet. The strict residual credit is `1-delta_q`; pure triangular
packets need only retain a strict Boolean flag, since their positive surplus
has no known uniform lower bound.

## 5. Reduced trees and interval splits

Contract each shared-cut cluster to a marked node in the block-cut tree, take
the minimal subtree spanning all marked nodes, and suppress unmarked degree-two
nodes. This is the reduced cluster tree `R`. A connected subtree of `R` lifts
to a connected induced territory after cuts on actual bridge blocks. Thus the
following reduction is rigorous.

**Lemma 5.1 (reduced-tree pruning).** Assume the all-rank theorem below rank
`r`. If a residual rank-`r` cactus has a leaf cluster containing no
distinguished cycle, cutting its first actual bridge gives a strict triangular
territory and a connected lower-rank cactus. If the complement has rank at
least two, induction proves the original cactus strict.

**Proof.** The leaf cluster and its connector remnant form a connected induced
triangular territory. The complementary territory is connected and contains
all distinguished cycles. Its cyclomatic number is smaller. Apply the
triangular theorem to the leaf and induction to the complement, then add. QED.

Consequently a minimal counterexample can have no all-triangle leaf cluster
whose deletion leaves rank at least two. There is one important exception: a
leaf may contain *all* triangles while its complement is one hostile
unicyclic distinguished cycle. Qualitative strictness of the triangular side
does not pay the fixed hostile deficit. Apart from this concentrated-leaf
exception, for `T^(r-1)Q` a nontrivial reduced tree would have all leaves
containing the single distinguished `Q`, impossible. For `T^(r-2)PP`, after
the same pruning, the reduced core is a path between the two
pentagon-containing ends, unless one end contains all triangles and deletion
leaves only a single pentagon. Thus the reduced-tree analysis removes the
colored partition census but exposes a rooted quantitative endpoint problem.

What remains is local to the one or two endpoint clusters. If an internal
cycle has distinct attachment marks, delete its incidence node and split the
cycle into proper consecutive intervals, assigning each incidence branch to
one interval. The cycle is destroyed, every branch has one owner, and the
resulting territories are induced. This is the mechanism that should create a
`TQ`, `TP`, or `PP` endpoint packet and leave triangular territories behind.

## 6. Candidate structural lemmas

The following two statements would complete the all-rank proof. They are
formulated to make the remaining burden precise; they are not proved here.

**Candidate Lemma A (endpoint guard extraction).** Let `K` be a shared-cut
cluster whose cycles consist of triangles and at most two distinguished
cycles. Suppose its cycle-cut incidence tree has no cut node incident with
every cycle of `K`. Given at most two labelled external connector entries, one
can split one or more internal cycles into consecutive intervals and obtain a
guarded territory decomposition of `K` together with those connector arms.
Every distinguished hostile cycle is in a `TQ` or `TP` territory, or the two
pentagons are together in a nonnegative `PP` territory; all other cyclic
territories are triangular.

The quantifiers concerning labelled entries are essential. An entry through a
triangle must travel with that triangle; an entry at a shared cut is owned by
the unique interval containing that cut; coincident entries are allowed.

**Candidate Lemma B (locked-cluster absorption and guard export).** Let `A` be
a nonempty shared-cut cluster of triangles with arbitrary attached trees and a
labelled connector root `z`. Then either of the following augmented cacti has
positive surplus:

1. a distinguished cycle `Q` is joined to `z` through an arbitrary nonempty
   bridge connector, with arbitrary trees on the resulting cactus;
2. one or two distinguished cycles meet the triangular cluster at a common
   cyclic cut, so that no triangle can be separated while retained.

In case 1 it is enough to assert the lemma for hostile `Q`; in case 2 the
cycle multiset is `T^kQ` or `T^kPP`, `k>=1`, and is one of the DNN residual
patterns.

Lemma B is deliberately analytic rather than a territory assertion. Its first
clause is forced by the exceptional reduced-tree leaf: a large locked
triangular cluster can be bridge-separated from a singleton hostile `Q`, and
its merely qualitative positive surplus is insufficient. A rooted matching-BP
or Coulson-phase inequality is a plausible route: compress every rooted tree
to its activity and prove that a nonempty triangular cluster exports one
hostile-cycle guard through the connector. In the common-cut clause, factor
the common root and prove absorption inside the locked packet. The needed
estimate is rank-free because extra triangular lobes must preserve a favorable
phase inequality rather than contribute a fixed additive margin.

**Candidate Lemma C (two-ended reduced-path split).** In the `T^(r-2)PP`
residual, suppose the reduced cluster tree is a path and each endpoint cluster
contains one distinguished pentagon. If neither endpoint is a common-cut
configuration covered only by Lemma B, then interval splits in the endpoint
clusters produce either

`TP + (lower-rank cactus) + TP`,

or

`PP + (nonempty triangular cactus)`.

Lemma C is expected to be a consequence of Lemma A plus ordinary connector
territories, but it is useful to state separately because it carries the exact
strictness condition in the `PP` alternative.

## 7. Conditional all-rank theorem

**Proposition 7.1.** Candidate Lemmas A and B imply that every connected cactus
of cyclomatic number at least two satisfies `s+(G)>|V(G)|`.

**Proof.** Induct on the cyclomatic number `r`, using the established ranks as
the base. Lemma 2.1 disposes of every nonresidual cycle multiset by the strict
DNN estimate.

Consider `T^(r-1)Q`. If `Q` is nonhostile, the same decomposition below needs
no negative payment. Repeatedly apply Lemma 5.1 to all-triangle leaf clusters
whose complement has rank at least two. If the process reaches an
all-triangular leaf opposite a singleton hostile `Q`, Candidate Lemma B(1)
finishes. Otherwise a nontrivial reduced core would have an all-triangle leaf
because only one marked cluster contains `Q`, a contradiction. Hence the
unresolved core is one shared-cut cluster. Candidate Lemma A gives a guarded
decomposition unless the core has the common-cut obstruction; Candidate Lemma
B(2) handles that obstruction. Lemma 4.1 finishes.

Now consider `T^(r-2)PP`. Prune every all-triangle reduced leaf whose complement
has rank at least two. If a concentrated endpoint leaves a singleton pentagon,
Candidate Lemma B(1) applies with `Q=P`. Otherwise a nontrivial reduced core
has only pentagon-containing leaves and is a path. Candidate Lemma C, hence
Lemma A, gives guarded endpoint packets and a lower-rank or triangular middle.
Common-cut endpoint obstructions are absorbed by Lemma B(2). If the reduced
tree has collapsed to one cluster, apply Lemma A or B directly. In every case
Lemma 4.1 gives strict positivity. QED conditionally.

## 8. The exact obstruction to interval-only proofs

Let `B_k` be the cactus consisting of one distinguished cycle `Q` and `k`
triangles, all sharing the same cut vertex `x`, with otherwise disjoint vertex
sets. Attach arbitrary rooted trees anywhere.

**Obstruction 8.1 (common-cut ownership).** No vertex partition into induced
territories can retain `Q` in one cyclic territory and retain any triangle in
a different cyclic territory.

**Proof.** Every one of these cycles contains `x`. A retained cycle requires
all of its vertices, hence requires `x`. Distinct territories in a vertex
partition cannot both contain `x`. QED.

Therefore no rank-uniform proof can rely only on pairing the hostile `Q` with
one triangle and sending the other triangles to separate cyclic territories.
At a multiway common cut, all retained cycles are locked into one packet. One
must either prove an analytic absorption inequality for that whole packet or
destroy cycles by private openings. The bridge-separated concentrated leaf is
the quantitative companion obstruction: it can be separated, but only into a
hostile singleton and a triangular packet whose known strict surplus has no
uniform positive lower bound. This is why Candidate Lemma B needs both common-
cut absorption and rooted guard export.

Private openings explain the current rank barrier. For a shared triangular
cluster `A_t`, the proved recurrence is

`sigma(A_t)>t-1` for `1<=t<=4`,

`sigma(A_t)>7-t` for `t>=4`.                                  (8.1)

The second line follows by opening an incidence-leaf triangle at exact tree
cost one until four triangles remain. If a leaf distinguished cycle is also
opened, the resulting bound at total rank `r` is

`sigma(G)>[7-(r-1)]-1=7-r`.                                  (8.2)

It is strict and positive through `r=7`, but at `r=8` it yields only `>-1`.
This is not a loose endpoint in the bookkeeping: every opened nonempty tree
has exactly `sigma=-1`. Improving (8.2) requires either a stronger
rank-uniform estimate for shared triangular clusters or avoiding repeated
openings through common-cut absorption.

There is a second obstruction to a naive numerical induction. Triangular
unicyclic packets with arbitrary trees are known to be strict, but no uniform
positive constant is available. Hence arbitrarily many qualitative strict
triangle terms cannot be asserted to pay one fixed hostile deficit. The guard
must be placed in the same certified mixed packet as the hostile cycle; merely
counting triangles is invalid.

## 9. Recommended next proof target

The most economical next target is Candidate Lemma B in the one-distinguished-
cycle form. It is the only configuration where the guarded-decomposition
invariant fails for a fundamental vertex-ownership reason. A successful lemma
should be stated for arbitrary rooted-tree activities and should prove a
pointwise matching-polynomial or Coulson-phase domination, not an additive
surplus per triangular lobe. After that, Candidate Lemma A is a finite-type
local topology theorem with unbounded numbers of triangle branches but only
three marks on each split triangle and at most two distinguished cycles; it
should admit a direct tree-pruning proof rather than a rank census.

Until those lemmas are proved, the rigorous result is:

* exact all-rank DNN residual families `T^(r-1)Q` and `T^(r-2)PP`;
* a rank-free guarded-hostility invariant sufficient for every decomposable
  residual;
* reduction of minimal counterexamples to one shared cluster or a two-ended
  reduced path;
* an exact common-cut obstruction to interval-only decomposition;
* and exact maximal range `2<=r<=7` for the present shared-triangle reserve
  method.
