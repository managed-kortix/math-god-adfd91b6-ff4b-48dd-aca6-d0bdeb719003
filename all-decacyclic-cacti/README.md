# All decacyclic cacti

This manuscript proves that every connected cactus `G` of cyclomatic rank ten
satisfies

```text
s+(G) > |V(G)|.
```

It covers arbitrary bridge lengths, connector entries, coincident interfaces,
Steiner branches, and finite trees attached at arbitrary vertices.

## Proof contents

- Exact sharp-DNN reduction to `T^9Q` and `T^8PP`.
- Complete colored cluster audits `96=92+4` and `180=170+10`, followed by a
  graph-level reduced-tree synthesis retaining all actual bridge connectors.
- The marked `A_9|Q` endpoint: `3624=3621+3` canonical entry classes.
- The `T^8P|P` last bridge: `11689=11586+100+3` classes.
- The two-interface `P|A_8|P` theorem: `11689=11674+15`, including all nine
  two-hub and six bouquet replacements.
- The complete fully shared `T^9Q` census in every `Q`-capacity regime, with
  an exact three-row hostile frontier.
- The fully shared `T^8PP` census `30386=30377+9`, with all nine exceptions
  explicitly repaired.
- General cycle-order and final-ownership lemmas for bridge remnants, router
  intervals, shared cuts, incidence branches, and attached trees.

The proof explicitly rejects a false packing-one/Voronoi guard on the new
three-cut kernels. It opens a leaf triangle or pentagon at exact tree cost `-1`
and applies packing one only to the retained common-hub packet. It does **not**
use the open two-pivot winding assertion in
`research/two-pivot-schur-sachs-triangular-cactus-2026-07-26.md`.

## Dependencies

The rank-ten certificate programs require Python 3.10 or newer and use only
the standard library, including exact `fractions.Fraction` arithmetic. The PDF
build requires TeX Live with `pdflatex`, `latexmk`, `amsmath`, `amsthm`,
`mathtools`, `booktabs`, and `hyperref`.

On Debian or Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y \
  python3 \
  texlive-latex-base \
  texlive-latex-recommended \
  texlive-latex-extra \
  texlive-science \
  latexmk
```

No network service, secret, numerical eigensolver, or repository environment
file is required.

## Exact reproduction

Run from the repository root:

```bash
python3 -c 'import sys; sys.exit("Python 3.10+ required") if sys.version_info < (3, 10) else None'
python3 research/rank-ten-cactus-frontier-census.py
python3 -O research/rank-ten-cactus-frontier-census.py
python3 research/decacyclic-t9q-marked-entry-certificate.py
python3 -O research/decacyclic-t9q-marked-entry-certificate.py
python3 research/decacyclic-t9q-incidence-certificate.py
python3 -O research/decacyclic-t9q-incidence-certificate.py
python3 research/decacyclic-t8p-last-bridge-census.py
python3 -O research/decacyclic-t8p-last-bridge-census.py
python3 research/decacyclic-t8-two-interface-census.py
python3 -O research/decacyclic-t8-two-interface-census.py
python3 research/decacyclic-fully-shared-nine-exceptions.py
python3 -O research/decacyclic-fully-shared-nine-exceptions.py
python3 research/decacyclic-t8pp-reduced-tree-topology.py
python3 -O research/decacyclic-t8pp-reduced-tree-topology.py
```

Expected headline results:

```text
Sharp-DNN residuals:
  T^9Q
  T^8PP

Colored cluster partitions:
  T^9Q:   all 97, proper 96, direct 92, structural 4
  T^8PP:  all 181, proper 180, direct 170, structural 10

A_9|Q marked entries:
  unmarked A_9 incidence trees: 355
  canonical marked classes:    3624
  physical marked positions:   6745
  direct one-router:            3621
  explicit common-hub repairs:    3

T^8P|P last bridge:
  T^8P incidence trees:          2392
  P-leaf incidence trees:        1105
  canonical marked classes:     11689
  direct one-router:             11586
  finite replacements:            100
  explicit repairs/openings:         3

P|A_8|P two-interface:
  unmarked incidence trees:       126
  ordered labelled placements:  36414
  canonical classes:            11689
  ordinary-router accepts:      11674
  explicit replacements:          15

Fully shared T^9Q totals by c=1,...,9:
  q=3:   1,12,91,406,1178,2115,2250,1246,275 = 7574
  q=4:   1,12,91,412,1203,2187,2361,1340,306 = 7913
  q=5:   1,12,91,412,1208,2201,2393,1372,321 = 8011
  q=6:   1,12,91,412,1208,2204,2400,1383,327 = 8038
  q=7:   1,12,91,412,1208,2204,2402,1386,330 = 8046
  q=8:   1,12,91,412,1208,2204,2402,1387,331 = 8048
  q>=9:  1,12,91,412,1208,2204,2402,1387,332 = 8049
  actual hostile q=5 and q>=9: 3 frozen classes each, all closed
  conservative hostile weakening at nonhostile q=7: same 3 classes, all closed

Fully shared T^8PP:
  all:         1,19,204,1155,3990,8135,9615,5843,1424 = 30386
  SAFE:        0,17,200,1154,3989,8135,9615,5843,1424 = 30377
  exceptions:  1, 2,  4,   1,   1,   0,   0,   0,   0 = 9
  replacement closure: 9/9
```

The frontier, `T^9Q`, strengthened `P|A_8|P`, and fully shared nine-exception
executables use explicit fail-closed checks and are run normally and under
`python -O`. They freeze exact signatures/digests and check concrete incidence
edges, router marks and intervals, connected disjoint retained packets,
displayed common hubs and packing one, exact `-1` opening costs, ledgers,
connector owners, and final ownership of every incidence cut. The imported
leaf-extension generator still contains assertions, but strengthened outputs
and acceptance decisions are identical under `-O`. The analytic packet proofs
and global graph-level exhaustion are in `paper.tex`.

## Build

Build and verify the PDF from the repository root:

```bash
bash scripts/build-paper.sh all-decacyclic-cacti
```

Or invoke `latexmk` directly:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -cd all-decacyclic-cacti/paper.tex
```

The resulting manuscript is `all-decacyclic-cacti/paper.pdf`.
