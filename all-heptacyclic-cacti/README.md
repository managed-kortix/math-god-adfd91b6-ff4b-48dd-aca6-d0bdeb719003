# All heptacyclic cacti

This manuscript proves that every connected heptacyclic cactus satisfies
`s+(G) > |V(G)|`. The result allows arbitrary bridge connectors, arbitrary
connector entries and Steiner branches, and arbitrary finite trees attached at
arbitrary vertices.

The proof contains:

- the exact sharp-DNN reduction to `T^6Q` and `T^5PP`;
- induced connector-territory, cycle-interval, and private-opening lemmas;
- the shared-triangle recurrence with exact strict margins
  `b_1,...,b_7 = 0,1,2,3,2,1,0`;
- the disconnected `T^6Q` structural leaf-cluster proof;
- all 46 proper disconnected `T^5PP` colored partitions: 41 direct packet
  rows and five structural rows, including the `T^5P|P` degree dichotomy;
- the fully shared `T^6Q` leaf-`Q`/internal-`Q` split, including the bouquet;
- the fully shared `T^5PP` two-pentagon-leaf/internal-pentagon split;
- current exact census certificates with corrected totals only.

Reproduce the exact finite certificates from the repository root:

```bash
python research/heptacyclic-t5pp-disconnected-partition-audit.py
python research/heptacyclic-t6q-incidence-census.py
python research/heptacyclic-tttttpp-incidence-census.py
```

The scripts use the Python standard library and exact `fractions.Fraction`
comparisons. Their asserted headline outputs are:

```text
Disconnected T^5PP partitions:
  all colored partitions:                  47
  proper partitions:                       46
  direct packet rows:                      41
  structural topology/entry rows:           5

Fully shared T^6Q totals by c=1,...,6:
  q=3:                    1, 8, 33, 71, 74, 29 = 216
  q=4:                    1, 8, 33, 73, 77, 32 = 224
  q=5:                    1, 8, 33, 73, 78, 33 = 226
  q=6:                    1, 8, 33, 73, 78, 34 = 227
  q>=7:                   1, 8, 33, 73, 78, 34 = 227
  SAFE split totals:                   215, 223, 225, 226, 226
  unique exception per regime:         seven-cycle bouquet

Fully shared T^5PP:
  colored trees:          1, 12, 68, 177, 211, 91 = 560
  SAFE ordinary splits:   0, 11, 67, 177, 211, 91 = 557
  structural exceptions:                                3
```

The three `T^5PP` census exceptions are the seven-cycle bouquet, a common-cut
`T^5P` core with a `TP` tail, and a five-triangle common-cut core with two
pentagon tails. The manuscript closes all three by the two-pentagon-leaf
opening argument. The censuses are independent certificates; inducedness,
cyclic interval realization, entry ownership, costs, and arbitrary attached
trees are proved structurally in `paper.tex`.

Build from the repository root with:

```bash
scripts/build-paper.sh all-heptacyclic-cacti
```
