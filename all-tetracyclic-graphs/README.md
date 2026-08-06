# Positive square energy of every tetracyclic graph

`paper.tex` proves that every finite simple connected graph `G` with `n`
vertices and `n + 3` edges satisfies

```text
s+(G) >= n.
```

This is the weak bound `s+(G) >= n`, not a strict theorem: several exact DNN
certificates meet the auxiliary excess budget three, and spectral equality is
not classified. It settles the connected `m = n + 3` frontier only; no
edge-addition monotonicity or conclusion for denser graphs is claimed.

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

## Dependencies and citations

- The theorem is the `m = n + 3` case of the edge-surplus conjecture in Akbari,
  Kumar, Mohar, Pragada, and Zhang, *Refinement of a conjecture on positive
  square energy of graphs*, arXiv:2506.07264 (2025).
- It uses the general `s+(G) >= n - 1` theorem of Liu, Tang, and Zhang, *The
  positive and negative square-energy conjecture*, arXiv:2607.18031 (2026), as
  historical context rather than as a substitute for the proof.
- Its lower-rank and rank-`3+1` inputs use the current companion manuscript
  `all-tricyclic-graphs/paper.tex`, dated 5 August 2026, plus its exact local
  certificate audits. The bibliography in `paper.tex` identifies every other
  companion manuscript and proof note by repository path.

## Verify

Run from the repository root:

```sh
python3 research/tricyclic-finite-rational-certificates-verifier.py
python3 -O research/tricyclic-finite-rational-certificates-verifier.py
python3 positive-square-energy/experiments/k4_all_odd_exact_verify.py
python3 -O positive-square-energy/experiments/k4_all_odd_exact_verify.py

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
The current transitive rank-four master manifest digest is
`9fa7bdf4a4a296a69f818bf78d5fe1a3aba5bddb38639ea784593d0291dfe19f`;
it pins seven direct verifier outputs, eleven transitive files, and three nested
verifier outputs.
The tricyclic finite-ledger and all-odd-`K4` digests are
`795f7772618d4f0280da914a85042970492f641909cd093abe9e30b434aa279c` and
`85ccff4a03791e2a5a455a7c350b804982f6ee3fb426233cd5e92c67431466c2`.
The appendix states each verifier's exact scope and what remains mathematical
rather than executable.

## Build

```sh
bash scripts/build-paper.sh all-tetracyclic-graphs
```

This produces `all-tetracyclic-graphs/paper.pdf` (15 pages in the current
build). The manuscript and proof-object synthesis are AI-generated. No human
authorship, human review, independent verification, conventional peer review,
or external publication is claimed; scripts audit finite proof objects but do
not replace the analytic and structural arguments.
