# Victory contract: all connected tricyclic graphs

## Target

Prove that every finite simple connected graph `G` with
`|E(G)|=|V(G)|+2` satisfies `s+(G)>=|V(G)|` (preferably strictly).

## What counts

A complete block/kernel classification with uniform path and rooted-tree
arguments, or a valid edge-promotion theorem from every connected bicyclic
base. Every infinite subdivision/message family must be proved, not sampled.

## What does not count

- exhaustive graphs only through a fixed order;
- the unproved bicyclic edge-monotonicity conjecture;
- a finite suppressed-kernel list without a theorem for arbitrary path/tree
  messages;
- DNN alone when the total block saving is below one;
- treating tree impedances as arbitrary edge weights;
- asserting a generic SOS remainder without displaying and verifying it.

## Current routes

1. Block ranks `1+1+1` are cacti and complete.
2. Block ranks `2+1`: theta block plus a cycle. Bridge-separated clusters close
   from the theta margin and the worst unicyclic deficit; direct one-vertex sums
   need a rooted theta-cycle phase packet.
3. One rank-three block: suppress degree-two paths to four tricyclic multigraph
   kernels. Use block DNN as a sieve, then coarse hostile-cycle phase charging;
   the signed target is `D(G)>=-4`.
4. Parallel high-variance route: prove bicyclic edge monotonicity, but its exact
   rank-two phase-area inequality remains open and must not be assumed.
