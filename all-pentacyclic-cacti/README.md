# All pentacyclic cacti

This manuscript proves that every connected pentacyclic cactus satisfies
`s+(G) > |V(G)|`, allowing arbitrary bridge connectors and arbitrary trees
attached at arbitrary vertices.

The proof contains:

- the exact DNN reduction to `TTTTQ` and `TTTPP`;
- all 11 disconnected `TTTTQ` cluster partitions and all 15 disconnected
  `TTTPP` cluster partitions;
- reduced-tree leaf proofs for both all-singleton partitions;
- entry-sensitive interval repairs for `TTTP|P` and `TTP|T|P`;
- the complete fully shared `TTTTQ` incidence proof;
- the exact 40-tree fully shared `TTTPP` census and its four exceptions.

Reproduce the exact colored incidence census from the repository root:

```bash
python research/pentacyclic-tttpp-incidence-census.py
```

Expected tree counts by cut-node count are `{1: 1, 2: 7, 3: 18, 4: 14}`;
the script also asserts the 36 one-cycle-split certificates and the exact four
unresolved canonical trees handled in the manuscript.

Build command (not run while creating this manuscript):

```bash
scripts/build-paper.sh all-pentacyclic-cacti
```
