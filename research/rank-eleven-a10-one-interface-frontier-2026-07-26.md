# Exact marked frontier for the rank-eleven endpoint `A_10 | Q`

**Date:** 2026-07-26

## Scope

This note records an exact first-stage census for the disconnected rank-eleven
cactus endpoint consisting of a shared-cut cluster `A_10` of ten triangles and
one hostile cycle `Q` joined through an arbitrary actual connector.  The first
cyclic-hull entry of that connector is marked.  It may be a shared cut or an
actual private triangle vertex.

This is an exact closure of one rank-eleven endpoint, not a proof of the full
rank-eleven cactus theorem. The ordinary router ledger closes all but ten
marked classes. Unique final owners are now resolved for every ordinary row,
and the ten residuals are closed by invariant structural repair templates.

## Exact result

The fail-closed verifier

```text
research/rank-eleven-a10-one-interface-census.py
```

regenerates

```text
1037 unmarked A_10 incidence trees,
21777 labelled interface placements before automorphisms,
12099 canonical marked rows,
12089 rows with router-ledger credit at least one,
10 zero-credit residual rows, all explicitly repaired.
```

Thus the exact marked frontier is

```text
12099 = 12089 + 10.                                      (1)
```

The complete credit distribution is

```text
credit 0:    10
credit 1:    15
credit 2:    26
credit 3:   161
credit 4:  1561
credit 5:  6190
credit 6:  4136
```

and the number of routers in the selected provisional plan is

```text
0 routers:    10
1 router:   7859
2 routers:  4192
3 routers:    38.
```

The residual cut-count distribution is `2,5,3` at one, two, and three shared
cuts.  The frozen digests are

```text
all rows: 8db6255acb0e663ea2d2c16ec4ffc0c329dae1cc8d7bb396eebd69aaa6b50402
residual: cb3daea744bf96c12f60b0a2028c4353c4b239a5cd36029cb75b7d16dff6d325.
```

## Final-owner resolution

For every ledger-accepted row the script checks the established proper-interval
triangle-router realization. Retained cycles are disjoint and exhaustive, each
retained shared cut has at most one retained-packet owner, later splits refine
an earlier branch, and a private marked connector on a destroyed router appears
in an actual router interval. A private mark on a retained triangle or a cut
mark touches a provisional retained owner.

The verifier interprets every router plan as a refinement tree. It pushes every
original cut, private hull vertex, router interval, and the marked connector
through the unique descendant branch to a terminal packet. For a two-interval
triangle split, the unlisted third triangle vertex follows the unique interval
of size two. It checks that terminal cycle packets are disjoint and exhaustive,
the intervals of one router remain distinct, every cut agrees with its retained
packet when one exists, fully deleted cuts have interval owners, and the marked
connector has exactly one terminal owner. The complete owner ledger has digest

```text
9600bb00f1f1fbf6e4cc74141fa2a4a27be9c781b785076492dff35021077479.
```

Since the hostile unicyclic deficit is strictly less than one, the `12089`
ordinary rows have strict positive surplus.

## Residual geometry and proof firewall

The ten residuals consist of the two marked orbits on the common-cut bouquet,
five marked orbits on a two-cut saturated extension, and three marked orbits on
a three-cut ladder extension. The repair classifier derives these shapes from
incidence neighborhoods, never from hard-coded row signatures.

The exact repair distribution is

```text
2  packing-one A10Q,
2  TQ + A8,
2  packing-one A8Q + T,
1  open one leaf + packing-one A9Q,
2  A7 + TQ + T,
1  open two leaves + packing-one A8Q.
```

The hostile ledgers are respectively `>10-delta_q`, strict zero sums,
`>8-delta_q` plus a strict triangle, `>8-delta_q` after one exact tree cost,
strict zero sums, and `>6-delta_q` after two exact tree costs. Here
`0<delta_q<1`. Each opened leaf contributes exactly one nonempty induced tree
of surplus `-1`; each router split uses proper triangle intervals. The verifier
checks exact cycle coverage, every cut owner, the unique Q/connector owner,
common-hub packing-one hypotheses, terminal profiles, and symbolic ledgers. The
repair digest is

```text
5c0f91e0d8953425521030928b282e64f2e91be7140344613e30e67b236e7df3.
```

The proof firewall remains:

* qualitative positivity of an `A_r` packet cannot pay a hostile deficit or an
  opening cost of one;
* triangles incident at different locked cuts cannot be assigned to separate
  retained packets when they need the same cut vertex;
* resemblance to a rank-ten residual signature does not prove that its repair
  inherits compatible marked intervals and final owners;
* neither the false global separator nor an unproved two-pivot phase theorem is
  used.

Thus every `A_10|Q` endpoint closes. The full rank-eleven theorem still requires
the marked `T^9P|P` and `P|A_9|P` endpoints and both fully shared residual
families.

## Reproduction

From the repository root, with Python 3.10 or newer, run

```bash
python3 research/rank-eleven-a10-one-interface-census.py
python3 -O research/rank-eleven-a10-one-interface-census.py
```

Both modes reproduce all counts, distributions, signatures, and digests. The
wrapper explicitly validates canonical incidence trees and freezes the
incidence, row, residual, final-owner, and repair digests using `require`, so
optimized execution is fail-closed for the stated endpoint closure.
