# Conservative last-bridge rerun: all sixteen failed classes

**Date:** 2026-07-26

## 1. Verdict

Write

```text
sigma(H)=s+(H)-|V(H)|,  T=C3,  P=C5,
delta=sqrt(5)-2.
```

The hostile conservative rerun of the disconnected row

```text
T^6P_0 | P_1
```

is reproduced exactly. It first cuts the last actual connector bridge before
the remote pentagon `P_1`, never silently moves the remaining connector across
that cut, and charges a separate acyclic territory when a subsequently split
router contains the private entry. Of the 877 canonical marked-entry classes,
861 pass the restricted one-router ledger and exactly 16 fail:

```text
c=1,2,3,4,5,6:  2,5,5,4,0,0.
```

Thus the rerun has the stated 13 additional failures beyond its original three,
for 16 total. All 16 admit the explicit packetizations below. Two classes need
no router split, five need one split, and nine need two simultaneous or
successive router splits. The weakest exact final margin is

```text
1-2delta = 5-2sqrt(5) > 0.                         (1.1)
```

No rooted hostile-cycle guard or numerical eigensolver is used.

## 2. What the conservative rerun charges

Cut the last actual bridge before `P_1`. The remote component, including the
remote side of that bridge and every branch attached there, is a pentagonal
unicyclic territory and contributes at least `-delta`. The connector remnant on
the clustered side remains rooted at its first cyclic-hull entry.

Now split a triangle router into nonempty proper cyclic intervals, one for each
incidence side. If the entry is private on that router, it is an additional
mark. Under the conservative convention the bridge has already been cut, so
the entry-owning interval cannot be reassigned to `P_1`. If that interval owns
no retained cycle, it is a connected induced acyclic territory. The sharp
universal accounting is

```text
sigma(tree) >= -1.                                  (2.1)
```

This is the private-entry interval acyclic cost omitted by the nonconservative
implementation. Charging (2.1) produces the 16 failures. In the explicit
repairs, it occurs only in L7 and L11. Every other private entry lies on an
unsplit triangle or on a split router interval that already belongs to a cyclic
packet, so it is merely an attached tree and incurs no separate cost.

The verifier uses these established packet bounds:

```text
sigma(A_1)>0;
sigma(common-cut T^kP_0)>k-delta;
sigma(shared-cut TTP_0)>2-delta;
sigma(P_1)>=-delta;
sigma(acyclic private-entry interval)>=-1.          (2.2)
```

All connector remnants, Steiner branches, and off-core trees follow the unique
interval owning their attachment.

## 3. Canonical failed classes

Cycle labels are `0,...,5=T`, `6=P_0`, and cut labels begin at `7`. In a
canonical root code, `R(...)` marks a cut and `TR(...)` marks a private vertex
of a triangle. `positions` records the labelled cyclic positions represented by
the rooted orbit.

| class | `c` | root | positions | canonical rooted code |
|---|---:|---|---:|---|
| L1 | 1 | `cut:7` | 1 | `R(P()T()T()T()T()T()T())` |
| L2 | 1 | `private:0` | 12 | `X(P()T()T()T()T()T()TR())` |
| L3 | 2 | `cut:7` | 1 | `T(R(P()T()T()T()T())X(T()))` |
| L4 | 2 | `cut:8` | 1 | `T(R(T())X(P()T()T()T()T()))` |
| L5 | 2 | `private:2` | 2 | `T(X(P()T()T()T()T())X(TR()))` |
| L6 | 2 | `private:1` | 8 | `T(X(P()T()T()T()TR())X(T()))` |
| L7 | 2 | `private:0` | 1 | `TR(X(P()T()T()T()T())X(T()))` |
| L8 | 3 | `cut:7` | 1 | `R(P()T()T()T(X(T()))T(X(T())))` |
| L9 | 3 | `cut:8` | 2 | `X(P()T()T()T(R(T()))T(X(T())))` |
| L10 | 3 | `private:2` | 4 | `X(P()T()T()T(X(T()))T(X(TR())))` |
| L11 | 3 | `private:0` | 2 | `X(P()T()T()T(X(T()))TR(X(T())))` |
| L12 | 3 | `private:3` | 4 | `X(P()T()T(X(T()))T(X(T()))TR())` |
| L13 | 4 | `cut:7` | 1 | `R(P()T(X(T()))T(X(T()))T(X(T())))` |
| L14 | 4 | `cut:8` | 3 | `X(P()T(R(T()))T(X(T()))T(X(T())))` |
| L15 | 4 | `private:2` | 6 | `X(P()T(X(T()))T(X(T()))T(X(TR())))` |
| L16 | 4 | `private:0` | 3 | `X(P()T(X(T()))T(X(T()))TR(X(T())))` |

The executable also prints the complete canonical unrooted incidence code and
edge list for each row, so this table is not dependent on a drawing.

## 4. Explicit packetizations

`E` denotes the acyclic private-entry interval in (2.1). The separate `P_1`
packet is included in every displayed ledger.

| classes | split routers | final packets | exact ledger |
|---|---|---|---:|
| L1--L2 | none | common-cut `T^6P_0 + P_1` | `>6-2delta` |
| L3--L6 | `T_0` | `T_2 +` common-cut `T_1T_3T_4T_5P_0 + P_1` | `>4-2delta` |
| L7 | `T_0` | `T_2 +` common-cut `T_1T_3T_4T_5P_0 + P_1 + E` | `>3-2delta` |
| L8--L10, L12 | `T_0,T_1` | `T_2+T_5+` common-cut `T_3T_4P_0 + P_1` | `>2-2delta` |
| L11 | `T_0,T_1` | `T_2+T_5+` common-cut `T_3T_4P_0 + P_1 + E` | `>1-2delta` |
| L13 | `T_0,T_1` | `T_2+T_4+` shared-cut `T_3T_5P_0 + P_1` | `>2-2delta` |
| L14--L16 | `T_1,T_3` | `T_4+T_5+` shared-cut `T_0T_2P_0 + P_1` | `>2-2delta` |

For L3--L7, `T_0` has the two incidence marks `7,8`; a private entry on `T_0`
is the third mark only in L7. For L8--L13, the two binary routers meet the
retained hub owner; splitting either first and then refining that owner gives
the displayed territories. For L14--L16, the same construction uses routers
`T_1,T_3`. Each binary split assigns one marked vertex to one incidence side
and the complementary edge to the other side. When a private mark is present
on a split router, the three singleton intervals are forced.

The shared-cut packets in L13--L16 are not common-cut three-cycle bouquets and
are not generic rank-three packets: their two triangles share an actual cut,
so the established strict `TTP>2-delta` bound applies. Every retained cut has
exactly one packet owner. Split-router remnants
are paths and retain no cycle. Hence the table gives connected, induced,
disjoint, exhaustive territories for every cyclic ordering and every attached
tree realization.

## 5. Exact weakest margin

The six ledger values occurring are

```text
6-2delta, 4-2delta, 3-2delta, 2-2delta,
1-2delta.
```

Since `delta=sqrt(5)-2`, their unique minimum is

```text
1-2delta = 5-2sqrt(5).
```

It is positive exactly because `25>20`. This is stronger and more precise than
the convenient estimate `delta<1/4`; no decimal approximation is used.

## 6. Reproduction

Run from the repository root:

```bash
python research/octacyclic-t6p-last-bridge-conservative.py
python research/octacyclic-t6p-last-bridge-sixteen-resolution.py
```

The first executable regenerates the `877=861+16` hostile rerun, prints all
canonical codes and incidence edge sets, and includes the private-entry
acyclic `-1` charge. The second independently asserts the 16 canonical rows,
checks every retained-cycle ownership set, every split-router mark owner,
packet connectedness, common-cut or shared-cut hypotheses, all symbolic
ledgers, and exact positivity. Its terminal result is

```text
closed conservative failures: 16/16
weakest exact margin: 1-2delta = 5-2sqrt(5) > 0
```

Therefore `877=861+16` is the authoritative complete `(G6PP)` proof. It has
`16/16` closure and no residual; no connector reassignment is used.
