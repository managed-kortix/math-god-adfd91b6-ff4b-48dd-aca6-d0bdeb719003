# Strict positive square energy of every bicyclic graph

`paper.tex` proves that every finite simple connected graph `G` with `n`
vertices and `n + 1` edges satisfies

```text
s+(G) > n.
```

## Proof map

- The 2-core classification is exhaustive: a bicyclic cactus
  (figure-eight or handcuff/dumbbell) or a theta, with arbitrary rooted-tree
  attachments.
- The cactus branch invokes the strict all-nonunicyclic-cacti theorem.
- The theta branch is proved in the paper using tree messages, an open
  right-half-plane Sachs expansion, exact omitted-path packets, and zero-,
  one-, and two-hostile phase channels.
- The delicate `0 mod 4` channels use explicit monotone and endpoint
  factorizations rather than changing the negative Sachs sign.
- A nonbipartite attached theta satisfies the quantitative bound
  `D >= -4(sqrt(5)-2)`, hence `s+(G)-n >= 5-2sqrt(5) > 0`; a bipartite theta
  has `s+(G)=n+1`.

The research note and verifier are supporting dependencies. The manuscript
reproduces the uniform proof and does not infer completeness from finite path
lengths.

## Verify

From the repository root, with Python 3.10 or newer:

```sh
python3 positive-square-energy/experiments/arbitrary_attached_theta_phase_verifier.py
python3 -O positive-square-energy/experiments/arbitrary_attached_theta_phase_verifier.py
```

Expected output in both modes:

```text
arbitrary attached theta phase verifier: PASS (packets=5, monotone-packets=2, even-factors=4, mutations=7/7)
```

The verifier checks canonical packet identities, low-length conventions,
one- and two-hostile `0 mod 4` repairs, the phase ledger, and seven hostile
mutations. It is corroborative, not a finite census proof.

## Build

From the repository root:

```sh
bash scripts/build-paper.sh all-bicyclic-graphs
```

Or from this directory:

```sh
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

The committed `paper.pdf` is the built manuscript. The paper includes an AI
disclosure and a scoped nonclaim.
