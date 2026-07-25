# Tick 2 audit of arXiv:2501.00614v14

This May 2026 manuscript claims a complete proof, but later primary papers still
treat SNC as open. A same-target hostile read found concrete fatal gaps:

1. Lemma 2.2 (p. 4) infers a pointwise internal outdegree lower bound from the
   existence of disjoint cycles in a BFS layer. Cycle packing does not imply
   that every layer vertex has the asserted degree; the proof selects a vertex
   with the desired property without deriving its existence.
2. Lemma 3.1 (p. 6) gives a purported partition of a child's outneighborhood
   that omits same-layer outneighbors not also children of the chosen parent.
   Exact witness: arcs
   `r->u,r->x,u->v,x->y,v->y`. With BFS layers `{u,x}` and `{v,y}`, the
   outneighbor `y` of `v` belongs to none of the three stated partition classes.
3. Theorem 3.2 assumes its set-cover conclusion in its first step and claims an
   arc swap lowers density `|E|/(|V|(|V|-1))`; an arc swap leaves that quantity
   unchanged.

The later regularity/layer bounds and final supply-demand contradiction depend
on these steps. Therefore v14 is not a valid resolution and does not change the
frozen assignment's open-status assessment. This is a correctness audit, not a
priority or announcement claim.
