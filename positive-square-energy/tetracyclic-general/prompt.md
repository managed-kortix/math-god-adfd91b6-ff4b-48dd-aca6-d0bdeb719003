# Victory contract: all connected tetracyclic graphs

## Target

Prove that every finite simple connected graph `G` with
`|E(G)|=|V(G)|+3` satisfies `s^+(G)>=|V(G)|`.

## Exact structure

The positive cyclic-block ranks partition four as

`1+1+1+1`, `2+1+1`, `2+2`, `3+1`, or `4`.

The cactus case is complete. DNN block additivity closes almost all remaining
multi-block rows; retain exact root/cut ownership in every structural repair.
For one rank-four block, suppress degree-two paths. The kernel is loopless,
2-connected, has minimum degree at least three, and
`sum_v(deg(v)-2)=6`; an independently verified kernel census is required.

## What counts

- a complete multi-block residual packet library;
- an exact rank-four kernel classification;
- all-length path/tree arguments, not finite graph sampling;
- exact rational/symbolic certificates and hostile audits.

## What does not count

- assuming edge addition preserves `s^+`;
- using the tricyclic theorem to pay a deleted tree without a quantified unit
  of surplus;
- treating switching as changing physical canonical path lengths;
- a kernel or parity census without independent regeneration;
- numerical SDP evidence.

## Current bottleneck

For a rank-four block with `L` edges and `L-3` vertices, DNN closes it if
`kappa<=L+3`. Exact path elimination reduces this to excess at most three on
each signed suppressed kernel. Weighted frustration alone is insufficient;
canonical even paths cost two and direct paths cannot be frustrated by a
collinear certificate.
