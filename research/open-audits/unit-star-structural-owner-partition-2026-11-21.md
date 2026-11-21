# Unit-star structural owner partition: exact cactus closure and the noncactus obstruction

Date: 2026-11-21. Status: **PROVED SUBFAMILY / SHARP STRUCTURAL OBSTRUCTION / NONPROMOTIONAL**.

## 1. Scope and reconstructed hypotheses

Let `G` be a finite simple connected graph with cyclomatic rank `beta(G)=7`.
Delete every physical bridge.  Suppose the positive hull of the resulting
bridge-free-component quotient is in the unresolved alternative of the exact
physical-hull reduction: after suppressing zero-rank degree-two hull vertices,
it is a star with `k` unit-rank leaves and center rank

```text
c=7-k,             1<=k<=7.
```

Assume every leaf component is hostile: it is connected unicyclic and its
unique cycle has length `1 mod 4`; arbitrary finite rooted trees and arbitrary
physical bridge-chain lengths are allowed.  The center is the actual complete
bridge-free component of rank `c`, not owner metadata supplied by a packet.

The following is a literal subfamily theorem.  It neither closes arbitrary
centers of ranks `2,...,6` nor the full rank-`(1,6)` marked bridge theorem.

## 2. Exact structural theorem

### Theorem (cactus-center unit stars)

If the actual bridge-free center component is a cactus, then `G` is a cactus
of cyclomatic rank seven and

```text
sigma(G)=s+(G)-|V(G)|>0.
```

This covers every center rank `c=0,...,6` subject to the literal cactus-center
hypothesis.  It includes arbitrary hostile cycle lengths `1 mod 4`, arbitrary
rooted-tree payloads, arbitrary bridge-chain lengths, arbitrary arm ports and
arbitrary center ports.  For the rank-`(1,6)` complement obtained by cutting
any arm, the conclusion is the instance-exact coupled inequality

```text
sigma(R)+Gamma(R,x;U,y) > -sigma(U).
```

### Proof

Every unit leaf side is unicyclic.  Every off-cycle edge of that side is a
physical bridge of `G`: deleting it separates an off-cycle tree, and the sole
external connection of the leaf side lies on the other side of that edge.
Thus its sole positive bridge-free component is its unique cycle; all of its
other blocks are bridges.  The same is true of every suppressed hull chain and
every off-hull tree branch.

By hypothesis every positive block inside the center is a cycle and, because
the center is a component obtained after deleting all physical bridges, the
center itself contains no bridge block.  Reattaching the arm components and
all zero-rank material only adds bridge blocks.  Hence every maximal block of
`G` is a cycle or a bridge: `G` is a cactus.  Its cyclomatic rank is
`c+k=7>=2`.  The established all-rank nonunicyclic-cactus theorem then gives
`sigma(G)>0`.

For any selected arm `U`, let `R` be the complete induced complement and let
`Gamma=s+(G)-s+(R)-s+(U)`.  The exact identity

```text
sigma(G)=sigma(R)+sigma(U)+Gamma
```

turns strict positivity into the displayed coupled inequality. `QED`

### Corollary (all centers of rank at most one)

Every hostile unit-star state with `c<=1` (equivalently `k>=6`) satisfies the
theorem.  A bridge-free connected rank-zero component is a single vertex: a
nontrivial connected rank-zero graph is a tree and has a bridge.  A
bridge-free connected rank-one component is a cycle: a connected rank-one
graph is unicyclic and every off-cycle edge is a bridge.  Thus either center is
a cactus, and the theorem applies.

### Exact scope consequence

The hostile unit-star remainder therefore has no noncactus `c=0` or `c=1`
state, and all cactus-center states are closed at every center rank.  The only
potentially noncactus center ranks are

```text
2<=c<=6,           1<=k=7-c<=5.
```

So "at least two hostile arms" alone does **not** finish the structural route:
that condition still permits every center rank `2,...,5`.

## 3. Why a bridge-opening owner partition cannot exploit arm multiplicity alone

### Lemma (physical bridge-cut rigidity)

Let `T` be the all-physical-bridge component quotient of one of these unit-star
states.  Any vertex partition obtained solely by deleting physical bridges has
connected induced owners whose positive-rank profiles are the weight multisets
of connected components of `T-F`, for some `F subset E(T)`.  In particular,
if an owner contains positive material from two distinct arms, it contains the
center component in full.  Hence at most one owner can contain positive
material from two or more arms.

### Proof

Deleting physical bridges is exactly deleting quotient-tree edges.  Components
of `T-F` expand to pairwise disjoint, exhaustive connected induced original-
vertex territories.  The unique quotient path between any two arm leaves runs
through the center.  A connected quotient component containing both leaves
must therefore contain the center.  Since quotient components are disjoint,
only one can do so. `QED`

This proves a method limitation: an induced owner partition using only
physical bridge openings cannot pair each of several hostile arms with a
separate piece of center reserve.  It has only two possibilities:

1. retain the center with any chosen subset of arms in one owner and detach
   every other arm as a complete unicyclic owner; or
2. retain all arms in the same center owner.

Every detached hostile arm has only the weak receipt
`sigma(U)>=-delta_q<0`.  Qualitative strictness elsewhere is not spendable.
Therefore multiplicity of hostile arms gives no new nonnegative ledger under
the existing lower-rank and unicyclic receipts.  A successful noncactus
partition must open **inside the actual center component** and prove a new
packet-specific owner theorem; the inherited star topology alone does not
supply one.

## 4. Exact obstruction to the tempting `c<=5` center-opening lemma

A natural proposed structural lemma is:

> If the center has rank at most five and at least two hostile arms, one can
> split the center into disjoint induced territories, each retaining the full
> center cycle/rank needed to guard a different hostile arm.

This is false even topologically.  For each `c in {2,3,4,5}`, take the
bridge-free center

```text
C=K_(2,c+1),
```

which has `beta(C)=c`, and attach `7-c>=2` disjoint hostile `C5` arms by
physical bridges (or arbitrary bridge chains) at arbitrary center vertices.
The inherited positive hull is the required unit-star.

The center `K_(2,c+1)` is 2-connected.  More generally, in any 2-connected
center, no vertex partition can put a **complete** center positive block in
more than one territory: retaining that block literally requires every center
vertex.  Distinct induced territories cannot duplicate those vertices.  Thus
there is no topology-only operation that manufactures one intact center guard
for each arm.  For the displayed family the arm ports may all coincide or may
be distinct; the obstruction is unchanged.

This does **not** show `sigma(G)<0`, and in fact these graphs are not offered as
spectral counterexamples.  It refutes only the proposed center-rank/arm-count
owner lemma.  Any valid route for `2<=c<=5` must use one of the following extra
inputs:

* a proved mixed packet on one center owner carrying several hostile arms;
* a center-specific structural opening that destroys part of the center but
  leaves separately certified lower-rank owners, with exact debit accounting;
* or the marked reserve--bridge-gain inequality.

Center rank by itself does not authenticate any of these.

## 5. Boundary relative to the graph theorem

Proved here:

* complete closure of actual unit-star hostile states with a cactus center,
  including all `c<=1` states (`k>=6`);
* exact reduction of the remaining noncactus star schemas to `2<=c<=6` and
  at most five hostile arms;
* physical-bridge owner rigidity; and
* an explicit rank-`2,...,5` family refuting a topology-only claim that
  multiple arms or `c<=5` creates multiple intact center guards.

Not proved here:

* any universal theorem for centers of ranks `2,...,6`;
* any theorem for all marked connected rank-six complements;
* any negative spectral counterexample;
* closure of the full actual-hull-bridge lane or the connected rank-seven
  theorem.

The cactus theorem used above is
`all-nonunicyclic-cacti/paper.tex`; the structural starting point and exact
rank/ownership conventions are
`positive-square-energy/heptacyclic-general/physical-hull-bridge-reduction/theorem-note.md`.
