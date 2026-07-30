# All cyclomatic-rank-twelve cacti

This manuscript proves that every connected cactus `G` of cyclomatic rank 12
on `n` vertices satisfies

```text
s+(G) > n.
```

## Proof map

- The sharp cactus DNN formula gives
  `sigma(G) >= 11 - sum_i epsilon_(l_i)`.
- Exact monotonicity and the inequalities `0<a<1`, `3a<2`, `2a>1`, and
  `a+epsilon_7<1`, where `a=5-2sqrt(5)`, leave exactly `T^11Q` and
  `T^10PP`.
- The public-repository hostile manuscript closes `T^11Q` for
  `q=1 mod 4`; the nonhostile note closes even `q` and `q=3 mod 4`, including
  `q=3`.
- The new public-repository all-rank two-pentagon manuscript closes `T^10PP`
  by specializing its theorem to ten triangles.

The short proof cites the rank-uniform structural arguments rather than
duplicating them. Its exact dependencies are:

```text
sharp-cactus-dnn/paper.tex
research/rank-twelve-cactus-dnn-residual-frontier-2026-07-30.md
research/rank-twelve-cactus-dnn-residual-frontier-verifier.py
all-rank-triangle-hostile-cacti/paper.tex
research/all-rank-nonhostile-one-cycle-theorem-2026-07-30.md
all-rank-triangle-two-pentagon-cacti/paper.tex
```

## Exact reproduction

Python 3.10 or newer is required. From the repository root run:

```bash
python3 research/rank-twelve-cactus-dnn-residual-frontier-verifier.py
python3 -O research/rank-twelve-cactus-dnn-residual-frontier-verifier.py
```

Expected output includes:

```text
rank-twelve sharp-DNN residual frontier: exact audit passed
frontier: T^11Q, T^10PP
certificate_sha256: 96d20340187cd0b2c01ca5d89d1f2c06cb0ecd321d035d73b53d94a706edd663
status: DNN frontier only; no rank-twelve cactus theorem claim
```

The verifier file SHA-256 is:

```text
d94364685251afb9a1045085f6cd4b85774d37329bbf359a1c35dd738c3baae6
```

## Build

```bash
bash scripts/build-paper.sh all-rank-twelve-cacti
```

The resulting PDF is `all-rank-twelve-cacti/paper.pdf`.

## Scope and disclosure

The theorem is scoped to finite simple connected cyclomatic-rank-12 cacti. It
does not prove the positive-square-energy conjecture for all graphs, an
all-rank cactus theorem, a result for non-cactus block intersections, or a
three-pentagon theorem.

The manuscript is AI-generated and claims no human authorship, review, or
verification. Its authority is the displayed reduction and the cited public,
reproducible proof objects.
