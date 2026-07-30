# All cyclomatic-rank-thirteen cacti

This manuscript proves that every connected cactus `G` of cyclomatic rank 13
on `n` vertices satisfies

```text
s+(G) > n.
```

## Proof map

- Sharp cactus DNN gives `sigma(G) >= 12-sum_i epsilon_(l_i)`.
- Exact monotonicity and `3 epsilon_5<2`, `2 epsilon_5>1`, and
  `epsilon_5+epsilon_7<1` leave exactly `T^12Q` and `T^11PP`.
- Existing complementary all-rank one-cycle theorems close `T^12Q` for every
  `q>=3`, including even `q` and `q=3`.
- The existing all-rank two-pentagon theorem closes `T^11PP` at `r=11`.

The exact dependencies are:

```text
sharp-cactus-dnn/paper.tex
research/rank-thirteen-cactus-dnn-residual-frontier-2026-07-30.md
research/rank-thirteen-cactus-dnn-residual-frontier-verifier.py
all-rank-triangle-hostile-cacti/paper.tex
research/all-rank-nonhostile-one-cycle-theorem-2026-07-30.md
all-rank-triangle-two-pentagon-cacti/paper.tex
```

## Exact reproduction

Python 3.10 or newer is required. From the repository root run:

```bash
python3 research/rank-thirteen-cactus-dnn-residual-frontier-verifier.py
python3 -O research/rank-thirteen-cactus-dnn-residual-frontier-verifier.py
```

Expected output is byte-identical and includes:

```text
rank-thirteen sharp-DNN residual frontier: exact audit passed
frontier: T^12Q, T^11PP
certificate_sha256: afed9ecb78b7def1cf0daf14655730e64f52fe59a1e8a38f1b9f115b5aecce76
rejected_hostile_mutations: 4
status: DNN frontier only; no rank-thirteen cactus theorem claim
```

The verifier file SHA-256 is:

```text
7da0684ff251c57a6832c5ce5077c76105af3d116eb30532f54007c2a5ec7fa9
```

## Build

```bash
bash scripts/build-paper.sh all-rank-thirteen-cacti
```

The resulting PDF is `all-rank-thirteen-cacti/paper.pdf`.

## Scope and disclosure

The theorem is scoped to finite simple connected cyclomatic-rank-13 cacti. It
does not prove the conjecture for all graphs, an all-rank cactus theorem, a
result for non-cactus block intersections, or a three-pentagon theorem.

The manuscript is AI-generated and claims no human authorship, review, or
verification. No artifact is published externally by these instructions.
