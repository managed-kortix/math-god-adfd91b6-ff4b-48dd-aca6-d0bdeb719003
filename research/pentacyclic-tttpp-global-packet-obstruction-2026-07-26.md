# Obstruction to a cluster-free `TTTPP` packet lemma

## Question

Can every pentacyclic cactus with residual cycle multiset

`{T,T,T,P,P}`, where `T=C3` and `P=C5`,

be handled by one global induced-territory construction which opens one or two
pentagons and leaves only packets of types `T`, `TT`, and `TP`?

The answer is no. The obstruction already occurs in the smallest possible
shared-cut incidence tree.

## The general obstruction

Call a cyclic block *retained* by a territory if all vertices of that block
belong to the territory, so that it remains a cyclic block of the induced
subgraph.

**Common-cut lemma.** Let `B1,...,Br` be cyclic blocks of a cactus containing
one common cut vertex `x`. In every vertex partition into induced territories,
all retained blocks among `B1,...,Br` belong to one territory.

Indeed, a territory retaining `Bi` contains every vertex of `Bi`, and hence
contains `x`. Since a vertex partition assigns `x` to exactly one territory,
no other territory can retain any `Bj`.

There is a slightly more general formulation which identifies why shared-cut
clusters cannot simply be omitted from a packet proof.

**Intersection-component lemma.** Form the graph on the retained cyclic blocks
in which two blocks are adjacent when they share a cut vertex. Every connected
component of this graph lies in one territory.

For adjacent blocks this follows because their common vertex can belong to only
one part. Propagation along a path proves the assertion. Consequently, a
territory theorem whose allowed packets contain at most two retained cycles
requires every retained shared-cut component to have order at most two.

## The `TTTPP` counterexample

Take three triangles and two pentagons and identify one vertex from every cycle
to a single vertex `x`, making no other identifications. This is a cactus. Its
cycle/cut incidence tree is the star

`{T1,T2,T3,P1,P2} -- x`,

with one cut node of degree five. It is the unique incidence type with one cut
node in the exact `TTTPP` incidence census.

Open or sacrifice either one or both pentagons, but retain the three triangles,
as required by the proposed `T`/`TT`/`TP` accounting. The three triangles still
share `x`. By the common-cut lemma they must all lie in one territory. None of
the proposed packet types contains three triangles:

- three `T` packets are impossible;
- a `TT` packet and a `T` packet are impossible;
- adding a retained pentagon only makes the unique cyclic territory larger,
  rather than producing a separate `TP` packet.

Splitting the pentagons into path fragments does not change the obstruction,
because it does not split the vertex `x`. Thus no partition into triangular
unicyclic, `TT`, and `TP` packets exists for this cactus after sacrificing at
most the two pentagons.

Allowing a triangle also to be opened avoids the literal combinatorial
obstruction, but not the intended surplus proof: it removes one of the three
positive triangular cycles and creates an additional tree cost. It is therefore
not the proposed lemma and does not yield the advertised packet ledger.

## The necessary replacement packet

The same example has a short induced-territory proof once a `TTT` packet is
allowed. Choose a private vertex `vi` of each pentagon `Pi`. Let `Fi` consist
of `vi` and every hanging tree rooted there, and put all remaining vertices in
`H`. Then:

- each `Fi` is a tree and has surplus `sigma(Fi)=-1`;
- each `Pi-vi` is a path containing `x`, so `H` is connected;
- the only cycles of `H` are the three triangles, all sharing `x`;
- their cycle-packing number is one, so the favorable-cycle estimate gives
  `sigma(H)>2`.

Induced-subgraph superadditivity therefore gives

`sigma(G) >= sigma(H)+sigma(F1)+sigma(F2) > 2-1-1=0`.

This is exactly the two-pentagon sacrifice, but its surviving packet is `TTT`,
not a collection of `T` and `TT` packets.

## Conclusion

There is no universal cluster-free partition lemma with only `T`, `TT`, and
`TP` packets. The one-cut five-cycle bouquet is a minimal counterexample, and
the intersection-component lemma explains the structural reason. Any valid
global proof must do at least one of the following:

1. admit a three-triangle packet with enough surplus to pay two tree costs;
2. split a triangle and establish a new quantitative estimate paying the extra
   loss; or
3. retain a shared-cut bottleneck alternative, which is cluster analysis under
   a different name.

The first option is already sharp for the bouquet: `sigma(TTT)>2` pays exactly
the two opened-pentagon tree costs, with strictness left over.
