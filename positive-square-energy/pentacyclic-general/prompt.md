# Victory contract: all connected pentacyclic graphs

## Target

Prove that every finite simple connected graph `G` with
`|E(G)|=|V(G)|+4` satisfies `s^+(G)>=|V(G)|`.

## Structural routes

The positive block-rank partitions of five are

`1^5`, `2+1^3`, `2+2+1`, `3+1+1`, `3+2`, `4+1`, and `5`.

The single rank-five block suppresses to one of 118 loopless no-cut-vertex
multigraph kernels (preliminary independent census; must be certified before
use). A universal DNN excess-four theorem is false already for all-odd
`K5-e`, whose optimized excess is `2sqrt(7)-1>4`.

The high-variance alternative is marked edge promotion. If a tetracyclic DNN
certificate has excess `E<=3`, margin `mu=3-E`, and endpoint correlation r for
a proposed new edge, reusing it proves the pentacyclic target whenever

`(1+r)/(1-r) <= 1+mu`, equivalently `r<=mu/(2+mu)`.

## What counts

- a complete marked-pair/margin theorem for every tetracyclic graph and
  nonedge, or
- complete multiblock packets plus an exact 118-kernel rank-five program.

## What does not count

- unrestricted edge monotonicity;
- a finite graph census;
- assigning universal DNN excess at most four to rank-five blocks;
- switching physical canonical path lengths;
- treating strict tetracyclic DNN margins as uniform spectral surplus.
