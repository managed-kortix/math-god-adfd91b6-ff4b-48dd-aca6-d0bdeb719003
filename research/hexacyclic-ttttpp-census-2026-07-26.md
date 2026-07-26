# Fully shared hexacyclic `{T,T,T,T,P,P}` incidence census

## Scope and status

This is an exact color-preserving census of the incidence trees for one
fully shared six-cycle cluster with four triangles and two pentagons. It is a
proof-search object, not a hexacyclic theorem. Its SAFE ledger accepts a split
only when the resulting induced branch territories have a positive total from
already proved lower-rank or pentacyclic estimates, with every needed incidence
hypothesis checked directly in the retained branch.

Write a branch as `(t,p)`. Splitting a cycle node partitions the other five
cycle nodes into branch multisets. The split cycle is distributed as proper
consecutive path intervals, so this operation itself incurs no separate tree
cost.

## Exact enumeration

The incidence graph has six cycle nodes and `c` shared-cut nodes. It is a tree,
so it has `c+5` edges and

`sum_x (deg(x)-1)=5`.

Every cut has degree at least two; hence `1<=c<=5`. Triangle degrees are at
most three and pentagon degrees at most five. Quotienting by
`S4 x S2 x S_c` gives:

| cut count `c` | colored incidence trees | SAFE-resolved | unresolved |
|---:|---:|---:|---:|
| 1 | 1 | 0 | 1 |
| 2 | 9 | 9 | 0 |
| 3 | 40 | 40 | 0 |
| 4 | 62 | 62 | 0 |
| 5 | 38 | 37 | 1 |
| **total** | **150** | **148** | **2** |

The script also records all `900=6*150` cycle splits. There are 26 distinct
triples `(split color, branch multiset, SAFE status)`. The same raw branch
multiset can occur with both statuses because retained incidence matters: for
example, a `TTP` branch is assigned the stronger `>2-delta` estimate only when
its two triangles share a cut inside that branch; otherwise the conservative
generic tricyclic bound is only `>=0`.

## SAFE positive acceptance ledger

The executable ledger uses only these estimates:

| retained branch | required incidence | bound used |
|---|---|---:|
| `T` | unicyclic triangle | `>0` |
| `P` | unicyclic pentagon | `>=-delta` |
| `TT` | arbitrary connector/incidence | `>1` |
| `TP` | arbitrary connector/incidence | `>1-delta` |
| `PP` | one retained shared-cut component | `>=1-4/(3sqrt(13))` |
| `TTT` | one retained shared-cut cluster | `>2` |
| `TPP` | one retained shared-cut cluster | `>6-2sqrt(5)` |
| `TTP` | its two triangles share a retained cut | `>2-delta` |
| any other tricyclic branch | no stronger checked hypothesis | `>=0` |
| `TTTT` | one retained shared-cut cluster | `>3` |
| `TTTP` | some two triangles share a retained cut | `>1` |
| any other tetracyclic branch | qualitative tetracyclic theorem | `>0` |
| any pentacyclic branch | qualitative pentacyclic theorem | `>0` |

Here `delta=sqrt(5)-2`. Bounds are added only across actual components after a
cycle-node split. A split is accepted exactly when the numerical sum is
positive, or equals zero with at least one strict summand. In particular:

- qualitative tetracyclic and pentacyclic positivity is never used to cancel a
  negative singleton pentagon;
- a formal `TTP`, `TTT`, `TTTT`, or `TTTP` cycle multiset does not receive a
  concentrated estimate unless its retained shared-cut hypothesis holds;
- no entry-sensitive disconnected-cluster row is inferred from cycle colors;
- no external opening cost is charged in this census.

This is intentionally narrower than all potentially valid packet arguments.

## Canonical exceptions

Cycle nodes are `0,1,2,3=T` and `4,5=P`; cut nodes start at `6`.

1. **Six-cycle bouquet (`c=1`).**

   `((0,6),(1,6),(2,6),(3,6),(4,6),(5,6))`.

   Every cycle split leaves one pentacyclic branch, so there is no multi-branch
   packet sum. Proposed structural class: **two-pentagon sacrifice at a common
   cut**. Opening private vertices on both pentagons should leave a connected
   four-triangle bouquet with known surplus `>3`, against two tree costs. This
   is the proposed H6/H10 mechanism and still requires its induced-territory
   statement to be cited or proved in the eventual argument.

2. **Saturated pentagon hub (`c=5`).**

   `((0,6),(4,6),(1,7),(4,7),(2,8),(4,8),(3,9),(4,9),(4,10),(5,10))`.

   Pentagon `4` uses five distinct degree-two cuts and has four triangular
   petals and one pentagonal petal. Splitting the hub into five separate
   branches gives `P+T+T+T+T`, whose conservative total is only `>-delta`.
   Proposed structural class: **pentagon five-mark interval merge**. In cyclic
   order, merge the pentagonal mark with an adjacent triangular mark and use
   four intervals, producing `TP+T+T+T` with total `>1-delta>0`. This is the
   proposed H7P structural lemma; the raw census does not mark it SAFE because
   it is not an ordinary one-branch-per-mark split.

No double-hub or hybrid incidence remains exceptional under the stated SAFE
one-cycle ledger. This computational fact does not establish either proposed
structural lemma and does not claim a theorem.

## Reproduction

Run:

```bash
python research/hexacyclic-ttttpp-incidence-census.py
```

The executable contains assertions for the 150-tree total, per-`c` counts,
148 resolved trees, both canonical exceptions, all 26 split profiles, and all
900 recorded cycle splits.
