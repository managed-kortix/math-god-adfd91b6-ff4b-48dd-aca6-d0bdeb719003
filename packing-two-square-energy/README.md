# Packing Two Square Energy

This directory contains a self-contained LaTeX manuscript proving a
square-energy sign theorem for graphs whose maximum collection of pairwise
vertex-disjoint cycles has size at most two.

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

- Every connected bicyclic block graph has exactly two triangular blocks
  and satisfies `s+(G) > |E(G)| = n + 1 > s-(G)`. This settles AKMPZ
  Conjecture 1.2 strictly for this class.
- Every connected tricyclic block graph satisfies `s+(G) > n`.  The only
  block structures are one `K4`, or three triangles; the packing-three case
  is split into three induced triangular unicyclic pieces by deleting two
  bridges.
- Triangular cacti whose triangles are covered by at most two bouquets have
  `s+ > s-`, including friendship and double friendship constructions.
- The manuscript proves the structural theta-obstruction lemma rather than
  assuming a classification of triangle intersections.

## Files

- `paper.tex` - manuscript and bibliography

Build from the repository root with:

```sh
bash scripts/build-paper.sh packing-two-square-energy
```

No claim of novelty or priority is made from a negative literature search;
the reverse `1 mod 4` theorem is presented as the phase-reversed companion
to the main argument.
