# Packing Two Square Energy

This directory contains a self-contained LaTeX manuscript proving a
square-energy sign theorem for graphs whose maximum collection of pairwise
vertex-disjoint cycles has size at most two, together with a cycle-territory
and packet proof for all connected non-tree block graphs.

## Main result

For a finite simple graph `G` containing a cycle:

- if every cycle has length `3 mod 4` and the cycle packing number is at
  most two, then `s+(G) > s-(G)`;
- if every cycle has length `1 mod 4` under the same packing hypothesis,
  then `s+(G) < s-(G)`.

The proof groups Sachs terms by vertex-disjoint cycle collections. After
normalization on the imaginary axis, each cycle of length `l` contributes
`q_l = -2 i^{-l}`, and each residual graph contributes its positive
signless matching polynomial `Z_H(t)`. Collections of two cycles contribute
only to the real part, so all one-cycle terms force the normalized
characteristic polynomial into one open half-plane. A carefully tracked
continuous argument and a Coulson identity then determine the sign of
`s+ - s-`.

## Consequences

- A fixed-priority nearest-cycle partition around any maximum cycle packing
  produces connected induced territories, each containing its chosen cycle
  and having cycle packing number exactly one. The proof tracks integer
  distances separately for earlier and later priority indices.
- Every connected triangular block graph containing a triangle satisfies
  `s+(G) > n`, with no bound on the number or packing of its triangles. This
  follows territory by territory from `s+ > s-`, `s+ > m_i >= n_i`, and
  induced-subgraph superadditivity; it does not claim `s+(G) > m(G)`.
- Every connected non-tree block graph satisfies `s+(G) > n`, with no bound
  on cyclomatic number, clique size globally, or cycle packing number. This
  is the manuscript's principal block-graph theorem and supersedes the
  rank-two-through-five results as a qualitative statement.
- Each induced cycle territory has packing number one. Its cyclic blocks are
  necessarily `K3`, `K4`, or `K5`; if there are at least two, they share one
  common cut vertex. Components off the cyclic bouquet have a unique root,
  so their tree branches can be assigned exactly once to induced packets.
- The packet estimates are explicit: a unique `K4` with rooted trees has
  `s+ > m = n+2` by the grouped Sachs expansion, and a unique `K5` with
  rooted trees has `s+ > n+1` by splitting one rooted tree from the remaining
  `K4` packet. No arbitrary `K_r` packet lemma is assumed.
- Bouquet territories split by deleting the common cut vertex from noncentral
  blocks: `K4-c=K3` routes to the triangular theorem and `K5-c=K4` routes to
  the standalone `K4` packet lemma. The proof separately treats one cyclic
  block, multiple blocks with a triangle, and multiple blocks without one.
- Consequently AKMPZ Conjecture 1.2 holds for every connected block graph with
  `m >= n+1`; the stronger theorem applies to every connected non-tree block
  graph, including `m=n`. It does not assert `s+(G) > m(G)` globally.
- Every connected bicyclic block graph has exactly two triangular blocks
  and satisfies `s+(G) > |E(G)| = n + 1 > s-(G)`. This settles AKMPZ
  Conjecture 1.2 strictly for this class.
- Every connected tricyclic block graph satisfies `s+(G) > n`.  The only
  block structures are one `K4`, or three triangles; the packing-three case
  is split into three induced triangular unicyclic pieces by deleting two
  bridges.
- Every connected tetracyclic block graph satisfies `s+(G) > n`. For a
  `K4` plus a triangle, the proof either splits vertex-disjoint blocks at a
  bridge or handles a shared cut vertex directly by Sachs phases. For four
  triangles, the packing-three obstruction is classified as a single
  `K1,3` cyclic cluster and resolved by explicit matching injections that
  force the normalized characteristic polynomial into the lower half-plane.
  The triangular-block corollary now subsumes the all-triangle conclusion,
  while the matching argument retains the stronger asymmetry statement.
- Every connected block graph of cyclomatic number five satisfies `s+(G)>n`.
  Its cyclic blocks are either five triangles, handled by the triangular
  corollary, or `K4+2K3`. Multiple cyclic clusters split over bridges into
  cyclic pieces of ranks at most four. In one cluster, deleting a private
  `K4` vertex and its bridge-only branches leaves a connected triangular
  rank-three piece with packing at most two, yielding the stronger `s+>n+1`.
- Triangular cacti whose triangles are covered by at most two bouquets have
  `s+ > s-`, including friendship and double friendship constructions.
- The manuscript proves the structural theta-obstruction lemma rather than
  assuming a classification of triangle intersections.

## Files

- `paper.tex` - manuscript and bibliography
- `../STATE.md` - current research-state summary
- `../positive-square-energy/notebook.md` - detailed research notebook

Build from the repository root with:

```sh
bash scripts/build-paper.sh packing-two-square-energy
```

No claim of novelty or priority is made from a negative literature search;
the reverse `1 mod 4` theorem is presented as the phase-reversed companion
to the main argument.
