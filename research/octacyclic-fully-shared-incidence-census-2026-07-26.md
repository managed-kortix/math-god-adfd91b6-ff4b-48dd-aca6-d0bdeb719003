# Exact fully shared octacyclic incidence census: `T^7Q` and `T^6PP`

**Date:** 2026-07-26

**Later resolution.** The six canonical `T^6PP` ordinary-split exceptions
listed here are closed, uniformly over arbitrary attached trees, in
`research/octacyclic-t6pp-six-exceptions-resolution-2026-07-26.md`. The
replacement audit does not use the rooted hostile-cycle guard theorem. The
common-cut bouquet uses the common-cut Schur--Sachs theorem; the five router
types use direct successive interval splits into common-cut mixed packets or
`P`, `T`, and `A_r` packets. The weakest ledger is
`1-2(sqrt(5)-2)=5-2sqrt(5)>0`. The qualifications below describe what this
census executable alone certifies and remain relevant; the later local
resolution is not a complete octacyclic theorem.

## Scope and status

This note records complete color-preserving incidence-tree censuses for the two
sharp-DNN octacyclic residual cycle multisets

```text
T^7Q and T^6PP.
```

It also applies a conservative ordinary one-cycle split ledger using exact
`fractions.Fraction` arithmetic and only packet results established through
heptacyclic rank. The computation is a finite structural audit. An incidence
type unresolved by this ledger is not a counterexample, and no octacyclic
theorem is claimed.

Run the executable certificate from the repository root:

```bash
python research/octacyclic-fully-shared-incidence-census.py
```

## Enumerated objects and independent checks

An object is a bipartite tree whose cycle nodes have colors `T,Q` or `T,P` and
whose uncolored nodes are shared cyclic cuts. Every cut has degree at least two;
cycle capacities are `deg(T)<=3`, `deg(P)<=5`, and `deg(Q)<=q`. Isomorphisms
preserve colors but may permute equal-colored cycles and all cuts. Cyclic orders,
off-core trees, and external connector entries are not enumerated.

Generation uses an exhaustive cycle-leaf recurrence. Every finite bipartite
tree has a leaf in its cycle part. Delete such a leaf and suppress its cut if
the cut becomes degree one. Conversely, restore the leaf either at an existing
cut or through a new binary cut attached to an existing cycle. The script tries
every possible color deletion and canonicalizes every extension by a
center-rooted colored-tree code.

As a regression check, this generator exactly reproduces the prior rank-seven
counts:

```text
T^5PP:       1, 12, 68, 177, 211, 91
T^6Q, q=3:  1,  8, 33,  71,  74, 29
T^6Q, q=6:  1,  8, 33,  73,  78, 34
```

The new octacyclic counts are asserted in the executable.

## Exact `T^7Q` census

Only seven cut incidences can occur on `Q`. The incidence-capacity regimes and
exact counts by number `c` of cut nodes are:

| `Q` regime | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `q=3` | 1 | 9 | 49 | 142 | 236 | 191 | 60 | 688 |
| `q=4` | 1 | 9 | 49 | 145 | 243 | 202 | 66 | 715 |
| `q=5` | 1 | 9 | 49 | 145 | 245 | 205 | 69 | 723 |
| `q=6` | 1 | 9 | 49 | 145 | 245 | 206 | 70 | 725 |
| `q=7` | 1 | 9 | 49 | 145 | 245 | 206 | 71 | 726 |
| `q>=8` | 1 | 9 | 49 | 145 | 245 | 206 | 71 | 726 |

The `q=8` and `q>=9` objects coincide structurally with `q=7`; they are run
separately because the packet ledger treats even `Q` as nonhostile and odd or
uniformly arbitrary `Q` by the hostile rational weakening.

For every possible split cycle, deleting that node gives retained branch
packets. The exact ledger is:

| branch | bound used |
|---|---:|
| `A_r=T^r`, `1<=r<=7` | `>0,>1,>2,>3,>2,>1,>0` |
| isolated `Q=T` | `>0` |
| isolated even `Q` | `>=0` |
| isolated hostile/arbitrary odd `Q` | `>-1` |
| `TQ` | `>0` |
| `TTQ` | `>=0` |
| `T^kQ`, `3<=k<=6` | `>0` by rank four through seven |

A split is SAFE exactly when the rational sum is positive, or is zero with at
least one strict summand. The split cycle is distributed into proper intervals,
so the operation carries no additional tree-opening charge.

Result: in every capacity/parity regime, all nonbouquet trees are SAFE. The
unique ordinary-split exception is

```text
X(Q()T()T()T()T()T()T()T()).
```

Thus the exact unresolved counts by `c` are `1,0,0,0,0,0,0`. This verifies the
structural hypothesis in the earlier status note: for a fully shared `T^7Q`
cluster, no finite incidence exception beyond the common-cut bouquet occurs.
It does not repair that bouquet. Opening `Q` leaves `A_7` with ledger
`sigma(A_7)-1>0-1`, which is insufficient.

## Exact `T^6PP` census

The color-preserving counts are:

| | `c=1` | `c=2` | `c=3` | `c=4` | `c=5` | `c=6` | `c=7` | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all trees | 1 | 14 | 106 | 377 | 728 | 657 | 233 | 2116 |
| SAFE | 0 | 13 | 104 | 376 | 727 | 657 | 233 | 2110 |
| unresolved | 1 | 1 | 2 | 1 | 1 | 0 | 0 | 6 |

The exact packet ledger retains all-triangle margins through `A_7` and the
following established mixed bounds:

```text
P>-1/4, TP>3/4, PP>0, common-cut TTP>7/4,
TPP>3/2, generic rank three >=0,
shared-pair TTTP>1, generic ranks four through seven >0.
```

The six canonical ordinary-split exceptions are most compactly described by
their cut neighborhoods. A pair `(a,b)` means that a cut contains `a`
triangles and `b` pentagons; incidences through a repeated triangle are stated
explicitly.

1. `c=1`: common-cut bouquet `(6,2)`.
2. `c=2`: a `(6,1)` hub and a `TP` tail joined through one hub triangle.
3. `c=3`: a `(5,1)` hub, a `TP` tail, and a binary `TT` petal, all routed by
   one saturated triangle.
4. `c=3`: a six-triangle common-cut hub with two `TP` tails on two distinct hub
   triangles.
5. `c=4`: a five-triangle common-cut hub; one hub triangle carries both a `TP`
   tail and a binary `TT` petal, while another carries the second `TP` tail.
6. `c=5`: a four-triangle common-cut hub with two symmetric arms, each using a
   saturated hub triangle to carry one `TP` tail and one binary `TT` petal.

The executable prints canonical signatures and exact labelled representatives
for all six. They are six color-preserving types, not six graph realizations.

## Structural hypotheses tested

The census gives a sharper verdict than the preliminary short-spine heuristic.

- Every exception has both pentagons as incidence leaves.
- Every exception is organized around a common-cut triangle bouquet of size
  `6,6,5,6,5,4`, in the canonical order listed above.
- The nonbouquet exceptions use only one or two endpoint triangles as routers;
  each router is saturated at incidence degree three when an additional
  triangle petal is present.
- No exception survives with an internal pentagon, with six or seven distinct
  cut nodes, or outside this common-cut-bouquet/router list.
- The proposed "one-/two-triangle router" picture is directionally correct but
  incomplete unless binary all-triangle petals on saturated routers are
  included. The census finds four nonbouquet forms beyond the simplest
  one-router common-cut tail.

Hence the finite canonical ordinary-split obstruction set for fully shared
`T^6PP` is exactly these six types under this ledger. It is larger than the
common-cut bouquet alone, but every additional type remains a common-cut
bouquet with short saturated-router decorations.

## What is and is not certified

The script certifies exhaustiveness of the abstract colored incidence trees and
the arithmetic of each accepted one-cycle packet ledger. It uses exact rational
values throughout; no floating-point comparison enters generation or SAFE
classification.

It does not enumerate cyclic mark order. For an ordinary split, the proof-level
operation still requires proper consecutive intervals and ownership of each
shared cut and attached tree. It does not test multi-cycle sacrifices, direct
spectral coupling, root-aware quantitative margins, disconnected shared-cut
graphs, or external entry incidences.

Most importantly, the six `T^6PP` types are exceptions only to this conservative
ordinary one-cycle split search. The familiar private-opening repair loses two
units while retaining `A_6`, whose available ledger is only

```text
sigma(A_6)-2 > 1-2.
```

So the rank-seven repair does not close these rank-eight types. A new
quantitative or nonadditive argument is still required. No theorem claim is
made here.
