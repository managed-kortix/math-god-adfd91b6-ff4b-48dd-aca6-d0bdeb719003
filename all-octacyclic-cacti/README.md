# All octacyclic cacti

This manuscript proves that every connected octacyclic cactus `G` satisfies
`s+(G) > |V(G)|`. It permits arbitrary bridge connectors, arbitrary connector
entries and Steiner branches, and arbitrary finite trees attached at arbitrary
vertices.

The corrected proof contains:

- the exact sharp-DNN reduction to `T^7Q` and `T^6PP`;
- the shared-triangle margins `b_1,...,b_7 = 0,1,2,3,2,1,0`;
- disconnected colored-partition audits `44=42+2` and `76=70+6`;
- the `G7Q` structural reduction and standalone packing-one Sachs lemma, with
  packing one verified directly for the seven-triangle common-cut bouquet;
- the strict-last-bridge `G6PP` certificate `877=861+16`, including all sixteen
  L1--L16 marked profiles, conservative private-entry costs, and the distinction
  between shared-cut `TTP` and a common-cut bouquet;
- the fully shared `T^7Q` census and its unique common-cut bouquet exception;
- the fully shared `T^6PP` census `2116=2110+6` and all six U1--U6 router
  resolutions;
- the scalar common-cut Schur--Sachs theorem for `T^kQ` and `T^kPP`;
- its explicit `Q=P` specialization `sigma(T^kP)>k-delta`;
- an induced-territory audit assigning every connector remnant, shared cut,
  router interval, incidence branch, and hanging tree exactly once.

The proof explicitly does **not** use the then-retracted, now restored, all-rank
rooted hostile-cycle guard, including its valid Voronoi packing assertion. It also does
not use the superseded uncut `877=868+9` / E1--E9 certificate. The authoritative
proof boundary is
`research/octacyclic-cactus-complete-synthesis-2026-07-26.md`.

## Dependencies

The census and router scripts require Python 3.10 or newer and use only the
Python standard library, including exact `fractions.Fraction` arithmetic. The
common-cut two-pentagon coefficient certificate
requires SymPy 1.14.0. The paper build requires a TeX Live installation
containing `pdflatex`, `latexmk`, `amsmath`, `amsthm`, `mathtools`, `booktabs`,
and `hyperref`.

On Debian or Ubuntu, install the complete dependency set with:

```bash
sudo apt-get update
sudo apt-get install -y \
  python3 \
  python3-venv \
  texlive-latex-base \
  texlive-latex-recommended \
  texlive-latex-extra \
  texlive-science \
  latexmk
```

Create an isolated certificate environment and install the pinned symbolic
dependency:

```bash
python3 -m venv /tmp/opencode/octacyclic-cacti-venv
/tmp/opencode/octacyclic-cacti-venv/bin/python -m pip install --upgrade pip
/tmp/opencode/octacyclic-cacti-venv/bin/python -m pip install sympy==1.14.0
```

No repository environment file, network service, secret, or numerical
eigensolver is required.

## Exact reproduction

Run these commands from the repository root, in this order:

```bash
/tmp/opencode/octacyclic-cacti-venv/bin/python \
  research/octacyclic-disconnected-partition-census.py
/tmp/opencode/octacyclic-cacti-venv/bin/python \
  research/octacyclic-t6p-last-bridge-conservative.py
/tmp/opencode/octacyclic-cacti-venv/bin/python \
  research/octacyclic-g6pp-last-bridge-census.py
/tmp/opencode/octacyclic-cacti-venv/bin/python \
  research/octacyclic-t6p-last-bridge-sixteen-resolution.py
/tmp/opencode/octacyclic-cacti-venv/bin/python \
  research/octacyclic-g6pp-last-bridge-four-resolution.py
/tmp/opencode/octacyclic-cacti-venv/bin/python \
  research/octacyclic-fully-shared-incidence-census.py
/tmp/opencode/octacyclic-cacti-venv/bin/python \
  research/octacyclic-t6pp-six-exceptions-resolution.py
/tmp/opencode/octacyclic-cacti-venv/bin/python \
  positive-square-energy/experiments/c5_bouquet_matching_certificate.py
```

The asserted headline results are:

```text
Disconnected T^7Q:
  all colored partitions:       45
  proper partitions:            44
  direct packet rows:           42
  structural rows:               2

Disconnected T^6PP:
  all colored partitions:       77
  proper partitions:            76
  direct packet rows:           70
  structural rows:               6

Strict-last-bridge G6PP:
  marked root classes:         877
  conservative direct passes:  861
  replacement profiles:         16
  failures by c=1,...,6:  2, 5, 5, 4, 0, 0
  replacement closure:       16/16
  weakest margin: 1-2delta = 5-2sqrt(5) > 0

Fully shared T^7Q totals by c=1,...,7:
  q=3:     1, 9, 49, 142, 236, 191, 60 = 688
  q=4:     1, 9, 49, 145, 243, 202, 66 = 715
  q=5:     1, 9, 49, 145, 245, 205, 69 = 723
  q=6:     1, 9, 49, 145, 245, 206, 70 = 725
  q>=7:    1, 9, 49, 145, 245, 206, 71 = 726
  unique exception in each regime: common-cut bouquet

Fully shared T^6PP:
  all:       1, 14, 106, 377, 728, 657, 233 = 2116
  SAFE:      0, 13, 104, 376, 727, 657, 233 = 2110
  exceptions:1,  1,   2,   1,   1,   0,   0 = 6
  replacement closure: 6/6
  weakest margin: 1-2delta = 5-2sqrt(5) > 0
```

All finite comparisons use exact integer or `fractions.Fraction` arithmetic.
The U1--U6 verifier regenerates the six rows from the imported fully shared
census, checks their signatures and edge sets, router interval sizes,
sequential refinements, retained packet sets, common-cut conditions, cyclic-cut
ownership, and exact ledgers. It deliberately imports that census's generator
and SAFE classifier, so it is not an independent re-enumeration. It does not
prove the analytic packet inequalities or arbitrary-tree realization. Those
are proved in `paper.tex`; the final command checks only the 1290-term
positive-coefficient polynomial inequality for the common-cut two-pentagon
theorem.

The conservative last-bridge script imports the marked-census module for the
finite incidence generator, root-orbit construction, and encoded packet-bound
ledger. The separate L1--L16 resolution script checks ownership and exact
positivity, while `octacyclic-g6pp-last-bridge-census.py` independently
regenerates the marked universe without importing a project census. No script
is claimed to establish the whole-cluster or one-cycle interval realization
lemmas for arbitrary connectors, coincident entries, or attached trees.

## Build

Build and verify the PDF from the repository root with:

```bash
bash scripts/build-paper.sh all-octacyclic-cacti
```

For a direct reproducible build after dependency installation, run:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -cd all-octacyclic-cacti/paper.tex
```

The resulting manuscript is `all-octacyclic-cacti/paper.pdf`.
