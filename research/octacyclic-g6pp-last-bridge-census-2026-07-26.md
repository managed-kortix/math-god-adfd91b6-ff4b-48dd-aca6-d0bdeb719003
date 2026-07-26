# Independent exact last-bridge `G6PP` marked-root census

**Date:** 2026-07-26

## Verdict

The strict last-bridge convention cuts immediately before the remote pentagon
`P_1`. Thus `P_1` is always a separate unicyclic packet. If a subsequently
split router contains the marked private entry, its entry interval is an
acyclic territory with exact conservative surplus `-1`; the connector is not
moved back into the `P_1` packet.

An independent generator, canonicalizer, rooted-orbit enumerator, and packet
search gives

```text
all T^6P_0 incidence trees:        226,
P_0-leaf incidence trees:          111,
marked cyclic-entry root classes:  877,
labelled cyclic positions:         1443.

strict last bridge, at most one router:  861 resolved, 16 unresolved;
the 16-class shared-cut/common-cut search: 16 resolved, 0 unresolved.
```

The 16 classes have cut-count distribution

```text
c=1,2,3,4,5,6: 2,5,5,4,0,0.
```

Hence the exact strict-last-bridge certificate is `877=861+16`, with no
residual. This is the sole authoritative complete certificate for `(G6PP)`.

## Established packet ledger

Write `delta=sqrt(5)-2<1/4`. The two-router search uses only

```text
P >= -delta,
A_r > 0,1,2,3,2,1 for r=1,...,6,
common-cut T^kP > k-delta,
shared-cut TTP > 2-delta when the two triangles share a cut,
generic rank 2 or 3 >= 0,
generic rank 4 through 7 > 0,
acyclic entry interval >= -1.
```

Every accepted row is an induced partition obtained by removing zero, one, or
two triangle routers. Each router has two or three distinct owners. Retained
components are generated directly from the incidence tree, and each unsplit cut
has one component owner. The remote `P_1` packet contributes the second
`-delta` in every listed ledger.

## The 16 exact classes

Labels `0,...,5` are triangles, `6=P_0`, and cuts start at `7`. `R` marks a cut
or a private triangle position. Positional multiplicity records symmetric
private positions represented by the rooted code.

| class | `c` | root code | positions | routers | final packets | ledger | status |
|---|---:|---|---:|---|---|---:|---|
| L1 | 1 | `R(P()T()T()T()T()T()T())` | 1 | none | common-cut `T^6P_0 + P_1` | `>6-2delta` | resolved |
| L2 | 1 | `X(P()T()T()T()T()T()TR())` | 12 | none | common-cut `T^6P_0 + P_1` | `>6-2delta` | resolved |
| L3 | 2 | `T(R(P()T()T()T()T())X(T()))` | 1 | `0` | common-cut `T^4P_0 + T + P_1` | `>4-2delta` | resolved |
| L4 | 2 | `T(R(T())X(P()T()T()T()T()))` | 1 | `0` | common-cut `T^4P_0 + T + P_1` | `>4-2delta` | resolved |
| L5 | 2 | `T(X(P()T()T()T()T())X(TR()))` | 2 | `0` | common-cut `T^4P_0 + T + P_1` | `>4-2delta` | resolved |
| L6 | 2 | `T(X(P()T()T()T()TR())X(T()))` | 8 | `0` | common-cut `T^4P_0 + T + P_1` | `>4-2delta` | resolved |
| L7 | 2 | `TR(X(P()T()T()T()T())X(T()))` | 1 | `0` | common-cut `T^4P_0 + T + P_1 + tree` | `>3-2delta` | resolved |
| L8 | 3 | `R(P()T()T()T(X(T()))T(X(T())))` | 1 | `0,1` | common-cut `T^2P_0 + T + T + P_1` | `>2-2delta` | resolved |
| L9 | 3 | `X(P()T()T()T(R(T()))T(X(T())))` | 2 | `0,1` | common-cut `T^2P_0 + T + T + P_1` | `>2-2delta` | resolved |
| L10 | 3 | `X(P()T()T()T(X(T()))T(X(TR())))` | 4 | `0,1` | common-cut `T^2P_0 + T + T + P_1` | `>2-2delta` | resolved |
| L11 | 3 | `X(P()T()T()T(X(T()))TR(X(T())))` | 2 | `0,1` | common-cut `T^2P_0 + T + T + P_1 + tree` | `>1-2delta` | resolved |
| L12 | 3 | `X(P()T()T(X(T()))T(X(T()))TR())` | 4 | `0,1` | common-cut `T^2P_0 + T + T + P_1` | `>2-2delta` | resolved |
| L13 | 4 | `R(P()T(X(T()))T(X(T()))T(X(T())))` | 1 | `0,1` | `T+T+` shared-cut `TTP_0+P_1` | `>2-2delta` | resolved |
| L14 | 4 | `X(P()T(R(T()))T(X(T()))T(X(T())))` | 3 | `1,3` | `T+T+` shared-cut `TTP_0+P_1` | `>2-2delta` | resolved |
| L15 | 4 | `X(P()T(X(T()))T(X(T()))T(X(TR())))` | 6 | `1,3` | `T+T+` shared-cut `TTP_0+P_1` | `>2-2delta` | resolved |
| L16 | 4 | `X(P()T(X(T()))T(X(T()))TR(X(T())))` | 3 | `1,3` | `T+T+` shared-cut `TTP_0+P_1` | `>2-2delta` | resolved |

The weakest accepted row is L11:

```text
sigma(G)>1-2delta=5-2sqrt(5)>0.
```

## Final four classes

L13--L16 are four roots of one unrooted incidence tree:

```text
incidence: X(P()T(X(T()))T(X(T()))T(X(T())))
edges: ((0,7),(0,8),(1,7),(1,9),(2,8),(3,7),(3,10),
        (4,9),(5,10),(6,7)).
```

This is a pentagon hub with three binary triangle arms. The four root orbits are
the hub cut, an arm cut, a terminal private position, and a router private
position. Exhaustive testing of all `1+6+15=22` subsets of zero, one, or two
triangle routers closes every root once the classifier recognizes the
established shared-cut `TTP` packet.

## Shared-cut resolution

The four-row crosscheck is recorded in
`research/octacyclic-g6pp-last-bridge-four-resolution-2026-07-26.md`. Its
packetizations use the same two-router cuts as the 16-row verifier and the
established special packet theorem

```text
sigma(TTP)>2-delta
```

when the two retained triangles share an actual cut. It yields the uniform exact margin

```text
sigma(G)>2-2delta=6-2sqrt(5)>0
```

for L13--L16, with arbitrary attached trees. The independent verifier is
`research/octacyclic-g6pp-last-bridge-four-resolution.py`.

## Reproduction

Run

```bash
python research/octacyclic-g6pp-last-bridge-census.py
```

The script imports no other project census. Generation and canonicalization are
implemented locally; all finite counts are asserted. Positivity uses integer or
`Fraction` arithmetic, with `delta<1/4` as the only algebraic comparison.

The defective uncut-connector `877=868+9` construction is superseded. It proves
neither E1--E9 completeness nor `(G6PP)`: several displayed packets separate a
root owner from the uncut connector. The strict-last-bridge convention instead
cuts before `P_1`, charges a private split-router entry interval by `-1`, and
closes all 16 first-stage failures without connector reassignment.
