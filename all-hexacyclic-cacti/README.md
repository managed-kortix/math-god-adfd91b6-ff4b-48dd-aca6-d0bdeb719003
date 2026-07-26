# All hexacyclic cacti

This manuscript proves that every connected hexacyclic cactus satisfies
`s+(G) > |V(G)|`, allowing arbitrary bridge connectors and arbitrary trees
attached at arbitrary vertices.

The proof contains:

- the exact sharp-DNN reduction to `TTTTTQ` and `TTTTPP`;
- arbitrary connector-territory, cycle-interval, and private-opening lemmas;
- the disconnected `TTTTTQ` proof, including the uniform five-triangle shared
  cluster bound `sigma > 2` and its packing-three case;
- all 28 proper disconnected `TTTTPP` colored cluster partitions;
- the six-row E1 proof for `TTTTP|P` and the exact E2 census of eight `TTTP`
  incidences and 26 ordered labelled-entry orbits;
- the fully shared `TTTTTQ` census totals 68, 70, and 71, with the unique
  bouquet handled directly;
- the fully shared `TTTTPP` census of 150 trees, its 148 SAFE ordinary splits,
  and direct proofs for the bouquet and saturated pentagon hub.

Reproduce the exact finite certificates from the repository root:

```bash
python research/hexacyclic-e2-tttp-entry-census.py
python research/hexacyclic-tttttq-incidence-census.py
python research/hexacyclic-ttttpp-incidence-census.py
```

The asserted headline outputs are:

```text
E2 TTTP incidences by cut count:         1, 3, 4
E2 ordered hub-entry orbits:             26 = 20 TP+TTT + 6 TTP+TT

TTTTTQ totals:
q=3:                                     1, 6, 20, 27, 14 = 68
q=4:                                     1, 6, 20, 28, 15 = 70
q>=5:                                    1, 6, 20, 28, 16 = 71
ordinary-split exception:                one six-cycle bouquet per regime

TTTTPP totals:                           1, 9, 40, 62, 38 = 150
SAFE ordinary-split resolutions:         0, 9, 40, 62, 37 = 148
canonical exceptions:                    bouquet, saturated pentagon hub
recorded cycle choices:                  900
```

Canonical exception edge sets and the symbolic repairs are recorded in
`paper.tex`; the scripts may print larger local ledgers, including all 26 E2
interval certificates, but those enormous outputs are not duplicated in the
manuscript.

Build from the repository root with:

```bash
scripts/build-paper.sh all-hexacyclic-cacti
```
