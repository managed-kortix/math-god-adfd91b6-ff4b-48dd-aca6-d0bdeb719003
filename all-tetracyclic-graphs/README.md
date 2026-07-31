# Positive square energy of every tetracyclic graph

`paper.tex` proves that every finite simple connected graph `G` with `n`
vertices and `n + 3` edges satisfies

```text
s+(G) >= n.
```

The manuscript deliberately makes no strict global claim. Several exact DNN
certificates meet the auxiliary excess budget three, and spectral equality is
not classified.

## Proof map

- Positive cyclic-block ranks split as `1+1+1+1`, `2+1+1`, `2+2`, `3+1`, or
  `4`.
- The multiblock proof gives the sharp DNN residual list and explicit packet
  repairs, including every cut incidence, bridge connector, and rooted tree.
- A single rank-four block suppresses to exactly 17 loopless 2-connected
  multigraph kernels: `1,2,5,4,5` types on `2,3,4,5,6` branch vertices.
- The paper proves the DNN correlation dual and exact path-elimination lemma.
  Fixed-parity monotonicity promotes finite physical-row frontiers to all path
  lengths.
- Exact ledger totals include `342=270+70+2` for four-vertex kernels,
  `378=370+8` for five-vertex orbits, and `376=359+17` followed by
  `160=148+12` for cubic kernels 13--15 and 17.
- Kernel 16 checks all 512 physical rows; kernel 17 is covered by seven exact
  templates with first-cover gains `284,123,56,24,13,8,4`.

The detailed proof objects are in
`positive-square-energy/tetracyclic-general/` and the exact verifiers are in
`research/`.

## Verify

Run from the repository root:

```sh
python3 research/rank-four-kernel-census-verifier.py
python3 -O research/rank-four-kernel-census-verifier.py

python3 research/rank-four-three-vertex-tables-verifier.py
python3 -O research/rank-four-three-vertex-tables-verifier.py

python3 research/rank-four-four-vertex-theorem-verifier.py
python3 -O research/rank-four-four-vertex-theorem-verifier.py

python3 research/rank-four-five-vertex-three-color-verifier.py
python3 -O research/rank-four-five-vertex-three-color-verifier.py
python3 research/rank-four-five-vertex-residual-closure-verifier.py
python3 -O research/rank-four-five-vertex-residual-closure-verifier.py

python3 research/rank-four-kernel16-three-color-verifier.py
python3 -O research/rank-four-kernel16-three-color-verifier.py
python3 research/rank-four-cubic-kernels-final-verifier.py
python3 -O research/rank-four-cubic-kernels-final-verifier.py

python3 research/tetracyclic-master-verifier.py
python3 -O research/tetracyclic-master-verifier.py
```

The kernel census checksum is
`d89e6e60c66e480ba89e662ab90b5ace211cbcff7292f92ad1614bb0937eb8e9`.
The four-vertex payload digest is
`f381b2b28bd3f45d7c96d90bce824a308bc340c9d6ebd098e5da116b89648d5a`.
The appendix states each verifier's exact scope and what remains mathematical
rather than executable.

## Build

```sh
bash scripts/build-paper.sh all-tetracyclic-graphs
```

This produces `all-tetracyclic-graphs/paper.pdf`. The paper includes a scoped
nonclaim, verifier appendix, AI disclosure, and no publication step.
