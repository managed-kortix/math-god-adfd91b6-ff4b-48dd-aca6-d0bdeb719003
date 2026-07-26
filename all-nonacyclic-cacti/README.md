# All nonacyclic cacti

This manuscript proves that every connected cactus `G` of cyclomatic rank nine
satisfies

```text
s+(G) > |V(G)|.
```

It covers arbitrary bridge lengths, connector entries, Steiner branches,
coincident interfaces, and finite trees attached at arbitrary vertices.

## Proof contents

- Exact sharp-DNN reduction to the two residual cycle multisets `T^8Q` and
  `T^7PP`.
- Disconnected colored-partition audits `66=63+3` and `117=109+8` (from totals
  `67` and `118`, after excluding the one-cluster partition).
- A complete `A_8|Q` proof using legal triangle routers and the directly checked
  one-hostile-cycle packing-one theorem.
- Entry-locked `T^7P|P` census `3188=3150+38`, including sequential
  final-owner refinement and exact connector/private-entry accounting.
- Two-interface `P|A_7|P` census `3188=3182+6`, with all six bouquet residuals
  explicitly repaired.
- The complete fully shared `T^8Q` census in every `Q`-capacity regime, with
  its common-cut and packing-one closures.
- Fully shared `T^7PP` census `8004=7997+7`, all seven residual signatures and
  replacements, and the F9 leaf-pentagon opening.
- Exact induced-territory ownership for every bridge remnant, router interval,
  shared cut, incidence branch, and attached tree.

The proof explicitly does **not** use the open two-pivot winding/phase
assertion in
`research/two-pivot-schur-sachs-triangular-cactus-2026-07-26.md`. It also does
not use candidate separator Lemma S in
`research/rank-uniform-triangular-router-interface-theorem-2026-07-26.md`.
Every two-interface rank-nine kernel is resolved by finite checked router
splits or an explicit pentagon opening.

The authoritative global proof boundary is
`research/nonacyclic-cactus-complete-synthesis-2026-07-26.md`; the corrected
lower-rank infrastructure is `all-octacyclic-cacti/paper.tex`, and the hostile
dependency audit is
`research/rank-nine-cacti-hostile-audit-verdict-2026-07-26.md`.

## Dependencies

The first five certificate programs require Python 3.10 or newer and use only
the standard library, including exact `fractions.Fraction` arithmetic. The
common-cut two-pentagon coefficient certificate requires SymPy 1.14.0. The PDF
build requires TeX Live with `pdflatex`, `latexmk`, `amsmath`, `amsthm`,
`mathtools`, `booktabs`, and `hyperref`.

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

Create a repository-local isolated environment.  The version check fails before
the census if the interpreter is older than Python 3.10, and no pre-existing
`/tmp` path is assumed:

```bash
python3 -c 'import sys; sys.exit("Python 3.10+ required") if sys.version_info < (3, 10) else None'
python3 -m venv .venv-nonacyclic
.venv-nonacyclic/bin/python -m pip install sympy==1.14.0
```

No network service, secret, numerical eigensolver, or repository environment
file is required.

## Exact reproduction

Run from the repository root, in this order:

```bash
.venv-nonacyclic/bin/python research/rank-nine-cactus-residual-census.py
.venv-nonacyclic/bin/python \
  research/nonacyclic-fully-shared-incidence-census.py
.venv-nonacyclic/bin/python \
  research/nonacyclic-t7p-last-bridge-conservative.py
.venv-nonacyclic/bin/python \
  research/nonacyclic-t7-two-interface-census.py
.venv-nonacyclic/bin/python \
  research/nonacyclic-t7pp-seven-exceptions-resolution.py
.venv-nonacyclic/bin/python \
  positive-square-energy/experiments/c5_bouquet_matching_certificate.py
```

The expected headline results are:

```text
Sharp-DNN residuals:
  T^8Q
  T^7PP

Disconnected T^8Q:
  all colored partitions:       67
  proper partitions:            66
  direct packet rows:           63
  structural rows:               3

Disconnected T^7PP:
  all colored partitions:      118
  proper partitions:           117
  direct packet rows:          109
  structural rows:               8

Entry-locked T^7P|P:
  marked classes:              3188
  direct one-router:           3150
  finite replacements:          38
  failures:                       0
  weakest margin: 1-2delta = 5-2sqrt(5) > 0

Two-interface P|A_7|P:
  unmarked incidence trees:      48
  ordered placements:         10800
  canonical classes:           3188
  ordinary router accepts:     3182
  best plans by router count:  2 zero, 3134 one, 52 two
  accepted by router count:    0 zero, 3131 one, 51 two
  explicit residual repairs:      6
  residuals:                    2 zero-router, 4 routed
  failures:                       0

Fully shared T^8Q totals by c=1,...,8:
  q=3:   1,11,68,253,572,742,493,127 = 2267
  q=4:   1,11,68,258,586,774,525,142 = 2365
  q=5:   1,11,68,258,589,781,536,148 = 2392
  q=6:   1,11,68,258,589,783,539,151 = 2400
  q=7:   1,11,68,258,589,783,540,152 = 2402
  q>=8:  1,11,68,258,589,783,540,153 = 2403

Fully shared T^7PP:
  all:        1,17,150,699,1856,2714,1998,569 = 8004
  SAFE:       0,15,148,698,1855,2714,1998,569 = 7997
  exceptions: 1, 2,  2,  1,   1,   0,   0,  0 = 7
  replacement closure: 7/7, including F9

Common-cut coefficient certificate:
  1290 nonnegative-coefficient terms
```

The hardened `T^7P|P`, two-interface, seven-exception, and coefficient
executables use explicit checks and fail closed even under `python -O`. The
residual partition and fully shared census generators still use Python
`assert`; run those two exactly as shown, without `-O`. The finite scripts
certify enumeration, canonicalization, exact packet ledgers, router recipes,
interval sizes, sequential refinement, and ownership data. They do not replace
the analytic packet proofs or graph-level exhaustion; those are supplied in
`paper.tex` and the cited packet manuscripts.

The `T^7P|P` verifier specifically checks that no provisional
`territory:*` owner survives a completed replacement: every cut, root, branch,
and attachment resolves to a final packet owner or the explicit
`naked-tree:entry` owner. The seven-row verifier regenerates all `8004` fully
shared types, checks the exact N1/F9/N2--N6 signatures and edge sets, and
verifies F9's exact `-1` nonempty-tree charge.

## Build

Build and verify the PDF from the repository root:

```bash
bash scripts/build-paper.sh all-nonacyclic-cacti
```

Or invoke `latexmk` directly:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -cd all-nonacyclic-cacti/paper.tex
```

The resulting manuscript is `all-nonacyclic-cacti/paper.pdf`.
