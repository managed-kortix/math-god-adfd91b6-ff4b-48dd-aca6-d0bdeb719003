# Positive square energy of all tetracyclic cacti

`paper.tex` proves that every connected tetracyclic cactus `G` on `n` vertices
satisfies

```text
s+(G) >= n.
```

The theorem permits arbitrary cycle-block incidence, arbitrary bridge and
connector trees, and arbitrary trees attached at every core vertex.

## Proof map

- The exact block-additive DNN bound leaves precisely `{3,3,3,q}` for odd `q`
  and `{3,3,5,5}`.
- For `C333q` with `q = 3 mod 4`, maximum-cycle-packing territories reduce to
  packets of packing number at most two. For `q = 1 mod 4`, a formal
  shared-cut-cluster partition handles both disconnected clusters and every
  connected incidence, including the common-root case; the bouquet phase
  theorem remains as an independent stronger bound.
- For `C3355`, bridge cuts exhaust disconnected shared-cut clusters. In the
  hostile `{3,3,5}|{5}` split, the strong tricyclic bound is used only when the
  internal triangles meet; when they are disjoint, an explicit induced
  `{3,5}|{3}` partition absorbs the full external connector.
- A connected `C3355` cluster has exactly twenty core types. An exhaustive
  induced-packet DP certifies types 2--20; the common-root type 1 uses the
  bouquet phase formula `s+ >= n + 7 - 2 sqrt(5)`.

No cycle-closure or edge-addition monotonicity is used. The paper also records
why the raw shared-`C333q` polynomial certificate `Phi = 2R - Zq I` is false
and does not use it.

## Build

From this directory run:

```sh
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

## Exact supplements

From the repository root, reproduce the `C3355` core census and packet DP:

```sh
python positive-square-energy/experiments/c3_c3_c5_c5_induced_packet_partitions.py
```

Expected final line:

```text
SUMMARY exact_positive=18/20 strict_target=19/20 minimum_score=-1 minimum_decimal=-1.000000000000
```

The missing type is the common-root bouquet proved analytically in the paper.
Audit the deliberately rejected raw `C3335` coefficient certificate with:

```sh
python positive-square-energy/experiments/c3_c3_c3_c5_shared_cluster_certificate.py
```

Supporting proof objects are at:

```text
research/c3-c3-c5-c5-tetracyclic-proof-2026-07-26.md
research/c3-c3-c5-c5-induced-packet-partition-audit-2026-07-26.md
research/common-root-cycle-bouquet-phase-2026-07-26.md
sharp-cactus-dnn/paper.tex
all-bicyclic-cacti/paper.tex
all-tricyclic-cacti/paper.tex
```
