# Exact obstruction to adaptive favorable-cycle frontier promotion

## Verdict and scope

The favorable-cycle induced-partition transfer is valid for each individual
finite graph to which its hypotheses apply.  It does **not** provide an
all-length lift from the canonical and one-coordinate frontier.

For an actual finite simple realization, suppose the branch vertices split
into two nonempty parts whose induced kernel sides are connected, of ranks
`h in {2,3,4,5}` and `1`, and the unique physical cycle on the rank-one side
is even or has length `3 mod 4`.  Put every same-side replacement path wholly
on its side.  Orient each crossing path, put all its internal vertices on one
endpoint side, and send every attached tree wholesale with its root.  The two
induced territories are connected, retain ranks `h` and `1`, and crossing
remnants are forests.  Induced square-energy superadditivity, the completed
rank-two through rank-five connected theorems, and the favorable unicyclic
theorem then give `sigma(G) >= 0`.

This target-level implication is not attacked here.  The obstruction is to the
tempting promotion

```text
canonical and every one-coordinate +2 target has some favorable partition
  ==> every same-parity descendant has some favorable partition.
```

That implication is false.  Favorability is not fixed-parity monotone: adding
two edges to a cycle changes its length from `3 mod 4` to `1 mod 4`.
Coordinate-specific witnesses do not repair simultaneous coordinate changes.

## Pinned source record

The counterexample route starts from this exact row of
`positive-square-energy/experiments/rank7_order9_after_sos_remainder.jsonl.xz`:

```text
[source index, global kernel, local order-nine kernel, odd-count row, orbit]
[78714, 7662, 176, [1,1,1,1,0,1,0,1,1,0,1,1,1], 1]
```

The source bytes and kernel fixture used to locate that row have SHA-256
values

```text
rank7_order9_after_sos_remainder.jsonl.xz
  2a45b69d495e65c47d4b3c668572b0b7922e808c905c501c97e513df47d05089
uncompressed canonical JSONL source
  fb28f9f36cafad170995f7dff43fb0d8cd1effa08765dd283461fb011d4cba7b
rank-seven-kernel-frontier-census.json
  a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5
```

The standalone verifier below does not depend on these files: it embeds the
small source certificate and checks it from first principles.

## Physical-occurrence certificate

The suppressed kernel has these physical occurrences, numbered in canonical
support order:

| occurrence | endpoints | canonical length | descendant length |
|---:|:---:|---:|---:|
| 0 | `0--7` | 1 | 1 |
| 1 | `0--8` | 1 | 3 |
| 2 | `0--8` | 2 | 2 |
| 3 | `1--6` | 1 | 1 |
| 4 | `1--7` | 1 | 1 |
| 5 | `1--8` | 2 | 2 |
| 6 | `2--4` | 1 | 1 |
| 7 | `2--7` | 2 | 2 |
| 8 | `2--8` | 1 | 1 |
| 9 | `3--4` | 1 | 1 |
| 10 | `3--5` | 2 | 2 |
| 11 | `3--8` | 1 | 1 |
| 12 | `4--8` | 1 | 1 |
| 13 | `5--6` | 1 | 3 |
| 14 | `5--6` | 2 | 2 |

Thus the increment-parity support is exactly `z={1,13}` and the descendant
length vector is

```text
(1,3,2,1,1,2,1,2,1,1,2,1,1,3,2).
```

It is a legitimate same-parity descendant.  Expansion gives a connected
simple graph with `(n,m,beta)=(18,24,7)`.  In particular, each parallel class
still has at most one unit path; lengthening cannot create a duplicate unit
edge.

## Exhaustive eligible-partition table

Enumerate every unordered nontrivial branch partition exactly once by taking
representative masks `1,...,255`, so the representative side omits branch
vertex `8`.  Test both orientations: either the representative or its
complement may be the rank-one side.  The complete list for which both induced
kernel sides are connected, the low side has rank one, and the other side has
rank two through five is:

| low-side mask | high rank | low-cycle physical occurrences |
|---:|---:|:---:|
| 96 | 5 | `{13,14}` |
| 98 | 4 | `{13,14}` |
| 104 | 4 | `{13,14}` |
| 106 | 3 | `{13,14}` |
| 120 | 3 | `{13,14}` |
| 122 | 2 | `{13,14}` |
| 124 | 2 | `{13,14}` |
| 226 | 3 | `{13,14}` |
| 227 | 2 | `{13,14}` |
| 230 | 2 | `{13,14}` |
| 234 | 2 | `{13,14}` |
| 257 | 2 | `{1,2}` |

Mask `257` is the complement-low orientation of representative mask `254`.
This convention prevents silently losing the only cycle of the second type.

At the canonical lengths every listed cycle has length `1+2=3`, so every row
of the table is favorable.  In the descendant, occurrence `13` is lengthened
for the first eleven masks and occurrence `1` for the final mask.  Every
listed cycle consequently has length `3+2=5`, which is odd and `1 mod 4`.
The exhaustive table proves that no alternate connected rank-`(2..5)`/rank-one
branch partition survives.

This is a route-level obstruction, **not** a graph counterexample to
`s^+(G) >= |V(G)|`.  It proves only that the favorable-cycle partition route
cannot infer all same-parity descendants from its finite frontier ownership.
A different owner may still prove the spectral inequality for this graph.

## Exact replay

Run from the repository root:

```text
python3 research/rank-seven-order-nine-favorable-cycle-adaptive-blocker-verifier.py
python3 -O research/rank-seven-order-nine-favorable-cycle-adaptive-blocker-verifier.py
```

The dependency-free verifier uses integer arithmetic only.  It checks the
expanded occurrence ledger, connectivity and cyclomatic ranks of every side,
leaf-prunes the expanded rank-one side while preserving parallel physical-edge
identities, requires exact equality with the twelve-row table, audits full
graph simplicity/connectivity/rank, and rejects any surviving favorable
partition.

No aggregate `1,501/1,615` census is claimed by this note.  That exploratory
count is intentionally omitted until a source- and fixture-digest-locked
full-census verifier is persisted and independently reviewed.
