# All rank-ten cacti

This manuscript proves that every connected cactus `G` of cyclomatic rank ten
satisfies

```text
s+(G) > |V(G)|.
```

It covers arbitrary bridge and connector lengths, branching connectors,
coincident interfaces, all cyclic entry positions, and arbitrary finite trees
attached at any core or connector vertex.

## Proof contents

- Exact sharp-DNN reduction to the two residual cycle multisets `T^9Q` and
  `T^8PP`.
- Disconnected colored-partition audits `96=92+4` and `180=170+10` (from
  totals `97` and `181` after excluding the one-cluster partition).
- Marked `A_9|Q` closure `3624=3618+6`, including the common-cut and
  saturated-router entry orbits.
- Entry-locked `T^8P|P` closure `11689=11586+100+3`, with sequential
  final-owner refinement and three explicit remote-pentagon openings.
- Two-interface `P|A_8|P` closure `11689=11674+15`, with all bouquet and
  saturated-router residuals explicitly repaired.
- Complete fully shared `T^9Q` census in every `Q`-capacity regime: `8011`
  types at `q=5`, `8049` stabilized types, and all three hostile exceptions.
- Fully shared `T^8PP` census `30386=30377+9`, all nine signatures and
  replacements, and all 60 N4 pentagon placements.
- Formal proper-interval and final-owner lemmas assigning every bridge remnant,
  shared cut, router interval, incidence branch, opened vertex, and attached
  tree exactly once.

The proof does **not** use the open two-pivot phase/winding assertion in
`research/two-pivot-schur-sachs-triangular-cactus-2026-07-26.md`, and it does
not use candidate separator Lemma S in
`research/rank-uniform-triangular-router-interface-theorem-2026-07-26.md`.
Every global split is at an actual bridge; every local split is a checked
proper cycle interval.

The authoritative proof boundary is
`research/rank-ten-cactus-complete-synthesis-2026-07-26.md`; the corrected
lower-rank infrastructure is `all-octacyclic-cacti/paper.tex` and
`all-nonacyclic-cacti/paper.tex`; the acceptance audit is
`research/rank-ten-cacti-hostile-audit-verdict-2026-07-26.md`.

## Dependencies

The census and closure scripts require Python 3.10 or newer and use only the
standard library, with exact integer or `fractions.Fraction` classifications.
The separate common-cut coefficient certificate requires `sympy==1.14.0`.
The PDF build requires TeX Live with `pdflatex`, `latexmk`, `amsmath`,
`amsthm`, `mathtools`, `booktabs`, `hyperref`, and `xurl`.

On Debian or Ubuntu:

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

No network service, secret, numerical eigensolver, or repository environment
file is required after the Python package is installed.

## Exact reproduction

Run from the repository root:

```bash
python3 -m venv .venv-rank-ten
. .venv-rank-ten/bin/activate
python -m pip install --upgrade pip
python -m pip install sympy==1.14.0
python -c 'import sys; sys.exit("Python 3.10+ required") if sys.version_info < (3, 10) else None'

python research/rank-ten-cactus-residual-partition-audit.py
python -O research/rank-ten-cactus-residual-partition-audit.py

python research/rank-ten-a9-one-interface-census.py
python -O research/rank-ten-a9-one-interface-census.py

python research/rank-ten-t9q-template-closure-verifier.py
python -O research/rank-ten-t9q-template-closure-verifier.py

python research/rank-ten-t8p-entry-locked-census.py
python -O research/rank-ten-t8p-entry-locked-census.py

python research/rank-ten-a8-two-interface-census.py
python -O research/rank-ten-a8-two-interface-census.py

python research/rank-ten-fully-shared-incidence-census.py

python research/rank-ten-t8pp-nine-exceptions-resolution.py
python -O research/rank-ten-t8pp-nine-exceptions-resolution.py

python positive-square-energy/experiments/c5_bouquet_matching_certificate.py
```

Expected headline results:

```text
Sharp-DNN residuals:
  T^9Q
  T^8PP

Disconnected T^9Q:
  all colored partitions:       97
  proper partitions:            96
  direct packet rows:            92
  structural rows:                4

Disconnected T^8PP:
  all colored partitions:      181
  proper partitions:           180
  direct packet rows:           170
  structural rows:               10

A_9|Q:
  unmarked incidence trees:     355
  labelled placements:         6745
  canonical marked rows:       3624
  finite-router rows:           3618
  explicit repairs:                6

Entry-locked T^8P|P:
  canonical marked rows:       11689
  direct final-owner rows:      11586
  finite replacements:           100
  locked openings:                  3

P|A_8|P:
  unmarked incidence trees:       126
  ordered placements:           36414
  canonical marked rows:        11689
  ordinary router accepts:      11674
  explicit residual repairs:       15

Fully shared T^9Q at stabilized capacity:
  c=1,...,9: 1,12,91,412,1208,2204,2402,1387,332
  total: 8049
  hostile exceptions: 3

Fully shared T^8PP:
  all:        1,19,204,1155,3990,8135,9615,5843,1424 = 30386
  SAFE:       0,17,200,1154,3989,8135,9615,5843,1424 = 30377
  exceptions: 1, 2,  4,   1,   1,   0,   0,   0,   0 = 9
  replacement closure: 9/9
  N4 cyclic placements: 60/60
```

All commands above except the final coefficient command are standard-library
scripts. The coefficient certificate alone imports the pinned SymPy package.
The partition, marked-endpoint, `T^9Q` closure, and nine-exception programs use
explicit exception-raising checks and are fail-closed under `python -O`. The
standalone compressed shared-incidence generator still contains Python
`assert`, so run that command only without `-O`. The dedicated closure
verifiers recheck their stated totals, signatures, ownership conditions, and
replacements in optimized mode, but they reuse census modules and recurrence
code; they are not an independent all-row implementation. Until such a
verifier exists, no stronger implementation-independence claim is intended.
The scripts certify finite enumeration and packetization; the analytic packet
bounds and global exhaustion are proved and cited in `paper.tex`.

## Build

Build and verify the PDF from the repository root:

```bash
bash scripts/build-paper.sh all-rank-ten-cacti
```

Or invoke `latexmk` directly:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -cd all-rank-ten-cacti/paper.tex
```

The resulting manuscript is `all-rank-ten-cacti/paper.pdf`.
