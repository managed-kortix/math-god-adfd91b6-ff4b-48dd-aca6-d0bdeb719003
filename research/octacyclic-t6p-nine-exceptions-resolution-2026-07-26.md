# SUPERSEDED: nine marked-root `T^6P | P` packet attempt

**Date:** 2026-07-26

## 1. Verdict

> **SUPERSEDED -- NOT A PROOF DEPENDENCY.** The uncut `877=868+9` / E1--E9
> construction is defective. It is retained as audit history. Use only the
> strict-last-bridge `877=861+16` proof in
> `research/octacyclic-t6p-last-bridge-conservative-resolution-2026-07-26.md`.

**Connector erratum.** The claimed `9/9` verdict below is not valid. With the
connector left uncut, its marked-root interval must lie in the same packet as
`P_1`. The displayed separate-`P_1` profile is therefore legal only when the
mark is private on a router sacrificed by the recipe. The exact verifier now
finds precisely E5, E8, and E9 valid and reports E1--E4 and E6--E7 invalid.
Those six rows require a bound for the joined root-side-plus-`P_1` packet or a
different legal split. Statements below asserting closure of all nine are
retained only as the audited former claim and must not be cited as proof.

Write

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5,
delta=sqrt(5)-2<1/4.
```

**Historical withdrawn claim (do not cite):** The nine exceptions E1--E9 in
`research/octacyclic-t6p-marked-root-incidence-census-2026-07-26.md` all admit
induced packetizations using the common-cut theorem and at most two successive
triangle-router splits. No rooted hostile-cycle guard, rooted quantitative
estimate, numerical eigensolver, or direct spectral comparison is used.

The exact result is:

| exceptions | closed | residual |
|---:|---:|---:|
| 9 | 3 | 6 |

The weakest ledger is E9:

```text
sigma(G)>1-2delta=5-2sqrt(5)>0.                 (1.1)
```

The preceding consequence is withdrawn: only E5, E8, and E9 survive the
connector audit in this uncut formulation.

## 2. Inputs and legal operations

Only the following established estimates are used:

```text
sigma(P)>=-delta;
sigma(A_r)>r-1                    for 1<=r<=4;
sigma(A_5)>2,  sigma(A_6)>1;
sigma(common-cut T^kP)>k-delta.                 (2.1)
```

Here `A_r` is a connected shared-cut cluster of `r` triangles. Every estimate
allows arbitrary attached trees. Positive square energy is superadditive over
induced vertex partitions, so the displayed packet surpluses add.

The corrected rule is never to cut the connector before `P_1`. Its entire
territory belongs to the marked-root interval's packet. A one-pentagon profile
survives exactly when that interval lies on a sacrificed private-root router,
because a proper triangle interval is a tree. Otherwise the owner retains core
cycles and the joined packet has those cycles together with `P_1`.

A degree-two router triangle is then split into the two proper consecutive
intervals owning its two cyclic cuts. A degree-three router is split into the
three singleton intervals owning its three cuts. If the marked entry is a
private vertex of a router, it is a third interval mark; retaining the
uncut connector through that interval instead gives the same pentagonal
unicyclic `P_1` packet. Every cyclic cut has one owner, and each incidence
branch follows the interval at its cut.

Some rows split a second router inside a territory produced by the first
split. Refinement of an induced partition by an induced partition remains an
induced partition. The remnants of split routers are trees in their owning
packets and retain no cyclic block. Thus the final packet lists below are
disjoint, exhaustive, induced, and valid with arbitrary attached trees.

## 3. Exact resolutions

Cycle labels in the executable representatives are `0,...,5=T`, `6=P_0`, with
cut labels starting at `7`; write `T_i` for triangle node `i`. Symmetry permits
the representative router and petal labels used below.

### E1--E2: common-cut bouquet

Do not split a triangle. Cut before `P_1`; the clustered packet is the
common-cut `T^6P_0` bouquet and the other packet is `P_1`. For both marked
entry orbits,

```text
sigma(G)> (6-delta)-delta = 6-2delta.            (3.1)
```

The entry connector remnant is merely an attached tree on the bouquet side,
whether it enters at cut `7` (E1) or privately on a triangle (E2).

### E3--E4: hub-tail form

Split router `T_0` between hub cut `7` and the `P_0`-tail cut `8`. The tail
packet is `P_0`; the hub owner retains `T_1,...,T_5=A_5`; and `P_1` is the
external packet. Hence, for both the hub-cut and hub-leaf entry orbits,

```text
sigma(G)> -delta+2-delta = 2-2delta.             (3.2)
```

### E5: pentagon-hub form

Split router `T_0` between cut `8`, which owns `T_2`, and hub cut `7`. The final
packets are

```text
T_2 + common-cut (T_1 T_3 T_4 T_5 P_0) + P_1.
```

The second packet is a common-cut `T^4P` packet at cut `7`; the remnant of
`T_0` is an attached tree. Therefore

```text
sigma(G)>0+(4-delta)-delta = 4-2delta.           (3.3)
```

### E6--E7: saturated router form

Split `T_0` at cuts `7,8,9`. The cut-`8` packet is `T_2`, the cut-`9` packet is
`P_0`, and the cut-`7` packet is `T_1,T_3,T_4,T_5=A_4`; `P_1` is external. This
works for both the hub-cut entry E6 and the hub-leaf entry E7:

```text
sigma(G)>0-delta+3-delta = 3-2delta.             (3.4)
```

### E8: two binary routers

First split `T_0` between its terminal cut `8` and hub cut `7`, and then split
`T_1` between the `P_0` cut `9` and hub cut `7`. The exact final list is

```text
T_2 + P_0 + A_3(T_3,T_4,T_5) + P_1,
```

so

```text
sigma(G)>0-delta+2-delta = 2-2delta.             (3.5)
```

### E9: saturated router followed by a binary router

Split `T_0` at cuts `7,8,10`, and inside the cut-`7` territory split `T_1`
between cuts `7,9`. The cut-`8`, cut-`9`, and cut-`10` sides own `T_2`, `T_5`,
and `P_0`, respectively. The common cut `7` retains `T_3,T_4=A_2`, while `P_1`
is external. Thus

```text
sigma(G)>0+0-delta+1-delta
        =1-2delta
        =5-2sqrt(5)>0.                            (3.6)
```

The final inequality is exact since `sqrt(5)<5/2`.

## 4. Comparison with the four rooted residual kernels

For each E-row, delete the incidence-leaf `P_0`, suppress its now-private cut
when appropriate, and retain the marked external entry root. Canonical rooted
color-preserving coding was compared with R1--R4 from
`research/octacyclic-rooted-six-triangle-finite-reduction-2026-07-26.md`.

```text
{triangular marked kernels underlying E1,...,E9}
    intersect {R1,R2,R3,R4} = empty.              (4.1)
```

This empty overlap is expected to be stated narrowly. It says that none of the
nine one-triangle-ledger exceptions is one of the four residual marked
six-triangle kernels. It does not close R1--R4 and does not invoke their rooted
packet target. Conversely, resolving E1--E9 by the unrooted packetizations in
Section 3 supplies no new rooted estimate for R1--R4.

## 5. Exact verifier

Run from the repository root:

```bash
python research/octacyclic-t6p-nine-exceptions-resolution.py
```

The verifier reruns the 877-class census, checks the listed abstract ownership
and symbolic ledgers, and separately checks connector realizability. It now
asserts that E5, E8, and E9 are the only displayed rows whose private marked
root lies on a sacrificed router; it reports the other six as invalid.
