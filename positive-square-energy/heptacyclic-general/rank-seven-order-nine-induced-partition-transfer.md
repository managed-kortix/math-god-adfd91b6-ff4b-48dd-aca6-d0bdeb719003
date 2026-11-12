# Rank-seven/order-nine transfer by induced lower-rank territories

## Scope and conclusion

Write

```text
sigma(X) = s+(X) - |V(X)|.
```

Let `G` be obtained from a loopless 2-connected rank-seven multigraph kernel
`K` on nine branch vertices by replacing every physical edge with a positive-
length path whose interiors are mutually disjoint, and then attaching arbitrary
finite rooted trees at branch or path vertices.  The result is simple.

The following criterion gives a uniform theorem owner.

**Induced-partition transfer theorem.**  Suppose there is a nontrivial
partition

```text
V(K) = S disjoint_union T
```

such that both induced multigraphs `K[S]` and `K[T]` are connected and have
cyclomatic ranks at least two.  Then

```text
s+(G) >= |V(G)|.                                      (1)
```

This applies to every path length and parity and every allowed rooted-tree
attachment.  It is independent of the order-eight rank-seven finite package:
the actual theorem inputs are the completed connected rank-at-most-six
results.  In the order-nine census the two territory ranks can only be

```text
(4,2), (3,3), (3,2), or (2,2),
```

with respectively `2,2,3,4` crossing physical edges.  Thus no territory has
rank seven; every positive-rank territory is covered by an already-proved
rank-two through rank-four theorem (and hence also by the stated rank-at-most-
six package).

## Sharp transfer inequality

The spectral step is the exact inequality

```text
sigma(G) >= sigma(G[U]) + sigma(G[W]).               (2)
```

Here `U,W` are induced vertex territories constructed below.  Since each
territory is connected, has cyclomatic rank between two and six, and contains
all trees assigned to it, the completed lower-rank theorem gives

```text
sigma(G[U]) >= 0,    sigma(G[W]) >= 0.                (3)
```

Equations (2)--(3) prove (1).  This is sharp at the level of the imported
nonstrict theorems: neither territory supplies a uniformly asserted positive
margin, and none is needed.  The crossing edges are simply omitted by the
principal-block pinching; no edge-addition monotonicity is asserted.

For completeness, (2) follows from the variational identity

```text
tr(A_+^2) = max_(X psd) {2 tr(AX) - tr(X^2)}.
```

Test it on the block diagonal matrix with blocks
`A(G[U])_+` and `A(G[W])_+`.  Cross-territory adjacency entries make zero
trace contribution.  This proves induced square-energy superadditivity with no
hypothesis on the crossing edges.

## Construction and exact rank accounting

For every replacement path whose kernel endpoints lie on the same side, put
the entire path on that side.  Orient each crossing path from `S` to `T`, put
all its internal vertices on the `S` side, and put its `T` endpoint on the
`T` side.  A unit crossing path has no internal vertices and contributes its
sole edge as a crossing edge.  Every rooted tree follows its root.  This gives
a genuine disjoint vertex partition

```text
V(G) = U disjoint_union W.
```

The induced graph `G[U]` is a subdivision of `K[S]`, with crossing-path stubs
and attached trees as rooted forest edges.  It is connected and has exactly
the same cyclomatic rank as `K[S]`.  The graph `G[W]` is a subdivision of
`K[T]` with its attached rooted trees and has the rank of `K[T]`.

If `c` is the total multiplicity of kernel edges crossing `S,T`, then
connectivity of `K[S]` and `K[T]` gives the exact identity

```text
beta(K[S]) + beta(K[T]) + c - 1 = beta(K) = 7.       (4)
```

Because both ranks are at least two, (4) forces the four types listed above.
Conversely, the proof uses exactly connectedness and the two rank inequalities;
those are the criterion's complete combinatorial hypotheses.

The same construction shows why arbitrary subdivisions and rooted trees cause
no hidden debit: subdivision preserves rank, and every connector remnant or
attached-tree edge belongs to a forest meeting one territory core at one root.

## Exact order-nine census

`research/rank-seven-order-nine-induced-partition-transfer-verifier.py`
regenerates the order-nine kernels from the pinned rank-seven census, enumerates
every unordered nontrivial branch-vertex bipartition, and checks connectedness
and cyclomatic rank using integer arithmetic.  Of the `4,495` order-nine
kernels, exactly

```text
4,022 satisfy the transfer criterion,
  473 do not.
```

A deterministic witness selection (maximize the smaller territory rank, then
the rank sum, then minimize the crossing multiplicity, vertex imbalance, and
bit mask) has this exact kernel distribution:

| ranks | crossing edges | kernels |
|:--:|--:|--:|
| `(4,2)` | 2 | 811 |
| `(3,3)` | 2 | 400 |
| `(3,2)` | 3 | 1,689 |
| `(2,2)` | 4 | 1,122 |
| **total** |  | **4,022** |

The criterion is a kernel property, so it owns every physical parity row and
every canonical-plus-coordinate target on those kernels, not merely the
currently persisted residue.

For a direct test against the exact residual frontier, the verifier authenticates
`rank7_order9_after_sos_remainder.jsonl.xz` and the three persisted Gram-owner
streams (`dominant`, `third`, and `fourth` family), checks that all `2,795`
stream records are disjoint exact source rows, and removes their union.  The
resulting exact population is

```text
269,725 orbit rows, 304,122 physical rows.
```

The transfer criterion owns

```text
268,110 orbit rows, 302,177 physical rows,
```

leaving only

```text
1,615 orbit rows, 1,945 physical rows,
```

on `115` represented obstruction kernels.  Thus it owns the exact fraction

```text
268110/269725 = 53622/53945
```

of these orbit rows (approximately `99.4012%`; the decimal is descriptive only
and is not used in any formal claim).  By deterministic witness type the owned
rows are:

| ranks / crossing | orbit rows | physical rows |
|:--|--:|--:|
| `(4,2)` / 2 | 88,722 | 101,324 |
| `(3,3)` / 2 | 51,251 | 57,095 |
| `(3,2)` / 3 | 104,224 | 115,955 |
| `(2,2)` / 4 | 23,913 | 27,803 |
| **total** | **268,110** | **302,177** |

These row counts classify only the currently committed post-SOS stream after
the three named persisted lanes.  They do not claim that those three streams
form every Gram lane ever intended by historical ordinal names.

## Exact obstruction to this transfer route

The induced-partition theorem is exact for the stated criterion, but its
failure is only a failure of this particular owner: a kernel outside the
criterion may still satisfy the desired spectral inequality for other reasons.
After removing the three named persisted Gram lanes, the obstruction population
is exactly

```text
1,615 orbit rows, 1,945 physical rows,
25,840 orbit targets, 31,120 physical targets,
```

on `115` represented kernels (among `473` obstruction kernels globally).
Every such row is canonically short: no parallel bundle has more than one odd
physical path, so every canonical physical path has length one or two.  Thus
all `1,615` canonical targets are a rigorous obstruction to the automatic
`q>=3` clause of the marked edge-opening lemma.  Each of the fifteen coordinate
frontiers does contain a length-at-least-three path, but ordinary rank-six
ownership is still insufficient: the opening lemma needs a marked rank-six DNN
owner carrying its exact excess `E_e` and endpoint correlation `r_e`, with

```text
E_e + f_q(r_e) <= 6.
```

A structural rank-six owner provides no Gram, and an unmarked theorem
conclusion records neither `E_e` nor `r_e`.  Consequently no deletion or
edge-opening ownership beyond the induced-partition class is claimed here.

The verifier also records a narrower exploratory incidence statistic for the
cubic-vertex deletion route: `22,742` orbit targets (`27,402` physical targets)
have a long path incident with at least one cubic vertex whose branch-vertex
deletion leaves a connected rank-five graph, while `3,098` orbit targets
(`3,718` physical targets) do not.  These numbers are **not** a theorem owner.
Deleting a branch vertex is not the marked physical-edge deletion of
`rank-seven-edge-opening-averaging-reduction.md`; the latter deletes one path
and leaves rank six, not rank five.  The unproved rank-five reinsertion step
must not be used to promote the `22,742` targets.  The `3,098` count is only an
incidence obstruction to that exploratory branch-vertex route.

### Recommended next experiment

For the `1,615` obstruction rows, enumerate all fifteen physical-edge
deletions into the completed rank-six owner library.  Retain only DNN owners,
extract the exact marked pair `(E_e,r_e)`, and test
`E_e+f_q(r_e)<=6` on each canonical-plus-coordinate target.  Report structural
owners and failed marked inequalities separately.  This directly tests the
proved rank-six edge-opening theorem and avoids the invalid rank-five
branch-vertex shortcut.

## Reproduction and claim boundary

Run from the repository root:

```text
python3 research/rank-seven-order-nine-induced-partition-transfer-verifier.py
python3 -O research/rank-seven-order-nine-induced-partition-transfer-verifier.py
```

Both runs use exact integer combinatorics and authenticated canonical JSONL
bytes; no floating-point arithmetic enters any accepted count or theorem
claim.  The verifier is not an order-nine theorem gate.  It proves the induced-
partition owner's exact scope and the stated finite obstruction/incidence
classification only.  It does not replay or validate the mathematical Gram
payloads of the three excluded owner streams, promote any deletion class,
close the residual targets, cover multiblock graphs, or claim an all-
heptacyclic theorem.
