# Victory contract: all connected bicyclic graphs

## Target

Prove that every finite simple connected graph `G` with `|E(G)|=|V(G)|+1`
satisfies `s+(G)>=|V(G)|` (preferably strictly outside a precisely identified
equality class).

The cactus-kernel cases are already complete. The only live family is a simple
theta 2-core with arbitrary finite rooted forests attached at any number of
core vertices.

## What counts as victory

A proof uniform in all three theta path lengths and all attached forests, with
physical ownership or exact tree-message elimination and no floating-point
step. The exact signed target is `D(G)=s+(G)-s-(G)>=-2`.

## What does not count

- the bare-theta theorem;
- one attachment site;
- the bipartite theta subfamily;
- a finite attachment census;
- the false multi-diagonal weighted-core reduction;
- attachment monotonicity (false even for one leaf);
- a pointwise comparison with the corresponding bare theta (false);
- merely rewriting the target as an unevaluated Coulson integral.

## Exact current kernel

Tree-message elimination gives a positive factor times
`W=pq-(u+iv)^2`, with `Re W=pq-u^2+v^2>0`. Hence there is no winding and

```text
D(G)=-(4/pi) integral_0^infinity t atan(-2uv/(pq-u^2+v^2)) dt.
```

Four mod-four channels are pointwise harmless, four are pointwise favorable,
and four have a single continuant cancellation. Victory is an integrated bound
of at most `pi/2` in the adverse channels, using the realizable recursion
`q=t+sum 1/q_child` rather than arbitrary independent activities.

## Search plan

1. Derive path-transfer differential identities and seek an integral charging
   each adverse phase interval to attachment matching energy.
2. Search for a stronger general packing-one mixed-cycle Coulson lemma whose
   threshold is `-2` and whose hypotheses theta graphs satisfy.
3. In parallel, seek a block-DNN-plus-spectral correction or coupled
   core/branch PSD witness; do not reuse separable diagonal penalties.
4. Hostile-test every proposed pointwise monotonicity on leaf messages at
   `t=1/4` and on `Theta(2,2,3)` and `Theta(2,3,3)`.
