# Fully shared heptacyclic `T^5PP`: exact incidence census

## Scope and status

This note records an exact color-preserving census and a conservative ordinary
one-cycle split ledger for a fully shared cluster with five triangles and two
pentagons. It is a proof-search artifact, not a theorem and not a claim that the
heptacyclic case is complete. The three types left unresolved by the stated
ledger require separate induced-territory arguments before they can be used in
any proof.

The executable is

```bash
python research/heptacyclic-tttttpp-incidence-census.py
```

It uses `fractions.Fraction` for every numerical SAFE comparison. No floating
point arithmetic occurs.

## Exact quotient census

Cycle nodes are `0,...,4=T` and `5,6=P`. Cut nodes start at `7`. If there are
`c` cut nodes, the bipartite incidence tree has `c+6` edges and

```text
sum_x (deg(x)-1)=6.
```

Every cut has degree at least two, triangle degree is at most three, and
pentagon degree is at most five. Quotienting by `S5 x S2 x S_c` gives:

| cut count `c` | colored incidence trees | SAFE-resolved | unresolved |
|---:|---:|---:|---:|
| 1 | 1 | 0 | 1 |
| 2 | 12 | 11 | 1 |
| 3 | 68 | 67 | 1 |
| 4 | 177 | 177 | 0 |
| 5 | 211 | 211 | 0 |
| 6 | 91 | 91 | 0 |
| **total** | **560** | **557** | **3** |

The independent tree canonical key is the center-rooted colored-tree code. The
script also computes a lexicographically least edge representative under the
same quotient for every unresolved type.

Across all `3920=7*560` cycle choices, the distribution of the number of SAFE
choices per tree is:

| SAFE cycle choices | 0 | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|---:|
| trees | 3 | 67 | 211 | 206 | 67 | 6 |

Thus the ordinary ledger leaves exactly three canonical incidence types. This
is only a statement about the finite acceptance test below.

## SAFE split ledger

Deleting one cycle node gives retained incidence components. A legal ordinary
split assigns the attachment marks to proper consecutive intervals of that
cycle; no additional opening cost is charged. For each retained component, the
script checks its actual incidence before selecting a bound. A split is SAFE
exactly when the rational lower-bound sum is positive, or is zero with at least
one strict summand.

The exact rational proxies are deliberately weaker than the established
irrational estimates:

| retained branch | checked hypothesis | rational bound used |
|---|---|---:|
| `T` | singleton triangle | `>0` |
| `P` | singleton pentagon | `>-1/4` |
| `TT` | arbitrary bicyclic incidence | `>1` |
| `TP` | arbitrary bicyclic incidence | `>3/4` |
| `PP` | one retained shared-cut component | `>0` |
| `TTT` | one retained shared-cut cluster | `>2` |
| `TTP` | its two triangles share a retained cut | `>7/4` |
| `TPP` | one retained shared-cut cluster | `>3/2` |
| any other tricyclic branch | no stronger hypothesis checked | `>=0` |
| `TTTT` | one retained shared-cut cluster | `>3` |
| `TTTP` | some two triangles share a retained cut | `>1` |
| any other tetracyclic branch | established theorem | `>0` |
| `TTTTT` | one retained shared-cut cluster | `>2` |
| any other pentacyclic branch | established theorem | `>0` |
| any hexacyclic branch | established theorem | `>0` |

Here `P>-1/4` and `TP>3/4` follow from
`delta=sqrt(5)-2<1/4`; `TTP>7/4` follows from
`2-delta>7/4`; and `TPP>3/2` is weaker than the established
`6-2sqrt(5)` estimate. These dyadic weakenings let every acceptance decision be
made in exact `Fraction` arithmetic.

The ledger is intentionally conservative:

- qualitative tetra-, penta-, and hexacyclic positivity never pays a negative
  singleton pentagon;
- `TTP` and `TTTP` receive stronger bounds only after their retained shared-cut
  condition is checked;
- concentrated all-triangle bounds are used only for a retained incidence
  component, not for triangles dispersed across components;
- the census tests ordinary one-branch-per-mark cycle splits only; merged-mark
  intervals and private openings are outside its acceptance rule.

The script prints all distinct `(split color, branch multiset, SAFE)` profiles
with multiplicities and asserts that their multiplicities sum to all `3920`
cycle choices.

## Canonical unresolved types

### U1. Seven-cycle bouquet

```text
c=1
((0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7))
```

All seven cycles use one common cut. Every cycle deletion leaves one rank-six
branch, so the ordinary multi-branch ledger has no split to add. Structural
class: **seven-cycle bouquet**.

A previously proposed repair is to open private vertices of both pentagons and
retain the five-triangle bouquet, formally giving `>2-2=0`. The exact
five-triangle margin is established, but this census does not certify the two
induced tree territories; U1 therefore remains unresolved here.

### U2. Six-cycle common-cut core with a `TP` tail

```text
c=2
((0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(0,8),(6,8))
```

Cut `7` supports `T^5P`; triangle `0` continues through cut `8` to the second
pentagon. The cut-color degrees are `(5,1)` and `(1,1)`. Structural class:
**six-cycle common-cut core with `TP` tail**.

Ordinary splitting at the tail triangle returns singleton `P` plus a
qualitatively positive rank-five branch, which is not a safe quantitative sum.
Splitting elsewhere leaves one rank-six branch or another ledger failure. A
candidate repair must preserve one owner for triangle `0` and both cuts while
extracting a quantitative pentagon partner or a valid concentrated sacrifice.
No such induced partition is asserted by the census.

### U3. Five-triangle common-cut core with two `P` tails

```text
c=3
((0,7),(1,7),(2,7),(3,7),(4,7),
 (0,8),(5,8),(1,9),(6,9))
```

The five triangles share cut `7`; triangles `0` and `1` continue through
separate cuts to the two pentagons. The cut-color degrees are `(5,0)`, `(1,1)`,
and `(1,1)`. Structural class: **five-triangle common-cut core with two `P`
tails**.

The ordinary ledger cannot simultaneously turn both pentagons into quantitative
mixed packets without splitting ownership of the central triangular core.
Opening both pentagons is a plausible concentrated-sacrifice route because the
five triangles remain at cut `7`, but admissible private vertices and the exact
induced ownership construction are not part of this abstract census. U3 is
therefore retained as unresolved.

## Structural-class ledger

The unresolved output consists of exactly:

| structural class | count |
|---|---:|
| seven-cycle bouquet | 1 |
| six-cycle common-cut core with `TP` tail | 1 |
| five-triangle common-cut core with two `P` tails | 1 |

In particular, no saturated pentagon hub, pentagon-ended incidence path,
pentagon double hub, saturated triangle router, or generic hybrid two-hub tree
survives this ordinary SAFE ledger. That exclusion is a computational census
result under the stated packet rules, not a replacement for interval-realization
lemmas and not a heptacyclic theorem.

## Reproducibility boundary

The executable asserts the six per-cut totals, the six per-cut SAFE totals, the
SAFE-choice distribution, all three canonical unresolved edge sets and labels,
and the global split count. It enumerates abstract incidence trees and checks
retained incidence hypotheses. It does not enumerate cyclic orders of marks on
a split cycle, external connector entries, attached trees, private opening
vertices, or spectra. Those geometric and spectral inputs must come from the
established territory lemmas and separate structural arguments.

No theorem claim is made.
