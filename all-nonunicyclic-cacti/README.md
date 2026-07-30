# All nonunicyclic cacti

This directory contains an AI-generated synthesis proving:

```text
Every finite simple connected cactus G of cyclomatic rank k>=2 satisfies
s+(G)>|V(G)|.
```

Rank one is excluded and cannot be added with strict inequality: `C4` has
spectrum `2,0,0,-2`, hence `s+(C4)=4=|V(C4)|`.

## Proof map

- Sharp cactus DNN gives `sigma(G)>=k-1-sum epsilon_l`.
- A rank-independent three-case calculation leaves exactly
  `T^(k-1)Q` and `T^(k-2)PP`, where `T=C3`, `P=C5`, and `Q` is any cycle.
- Hostile (`q=1 mod 4`) and nonhostile (even or `q=3 mod 4`) all-rank
  one-cycle theorems close `T^(k-1)Q`, including `Q=T`.
- The all-rank two-pentagon theorem closes `T^(k-2)PP` for `k>=3`.
- At `k=2`, the pure `PP` family is split exactly into the shared-cut bouquet
  theorem and the positive-length connector theorem.

Exact dependencies, in logical order:

```text
sharp-cactus-dnn/paper.tex
research/rank-uniform-cactus-dnn-frontier-verifier.py
all-rank-triangle-hostile-cacti/paper.tex
research/all-rank-nonhostile-one-cycle-theorem-2026-07-30.md
all-rank-triangle-two-pentagon-cacti/paper.tex
two-c5-bouquet-trees/paper.tex
two-c5-all-connectors/paper.tex
research/rank-uniform-cactus-theorem-proof-note-2026-07-30.md
```

The rank-two through rank-thirteen synthesis papers are not dependencies.

## Reproduce

Python 3.10 or newer is required. From the repository root:

```bash
python3 research/rank-uniform-cactus-dnn-frontier-verifier.py
python3 -O research/rank-uniform-cactus-dnn-frontier-verifier.py
bash scripts/build-paper.sh all-nonunicyclic-cacti
sha256sum all-nonunicyclic-cacti/paper.tex \
  all-nonunicyclic-cacti/README.md \
  all-nonunicyclic-cacti/paper.pdf \
  research/rank-uniform-cactus-dnn-frontier-verifier.py \
  research/rank-uniform-cactus-theorem-proof-note-2026-07-30.md
```

The normal and `-O` verifier outputs must be byte-identical. The verifier uses
exact affine `Q(sqrt(5))[K]` arithmetic. It proves symbolic cancellation and
constant signs for arbitrary integer `K>=2`; no finite-rank frontier calls are
trusted. Substitutions at `2,3,4,5,7,13,64` semantically test every generated
template identity. The canonical symbolic expression records determine the
digest, and seven mutations of coefficients, radicals, case bounds, or
survivor families are rejected. It certifies the DNN frontier only; residual
closure remains dependency-based.

Expected verifier output:

```text
rank-uniform sharp-DNN cactus frontier: symbolic exact audit passed
frontier display (not a trusted function): T^(K-1)Q, T^(K-2)PP
symbolic_variable: K (integer K>=2); no representative-rank proof calls
semantic_substitutions: 2,3,4,5,7,13,64
certificate_sha256: 1b549165c84ab20bdaebfec9329c37fb3e808ef435bda7a3586c8285c2d075ca
rejected_hostile_mutations: 7
status: DNN frontier only; structural closure is dependency-based
```

## Scope and disclosure

This is a cactus theorem, not a proof for all graphs. It assumes finite,
simple, connected graphs and does not cover disconnected cacti, non-cactus
block intersections, or cyclomatic rank one. It makes no universal
positive-square-energy claim for arbitrary graphs.

The manuscript and proof note are AI-generated; no human authorship, review,
or verification is claimed. No external publication was performed.
