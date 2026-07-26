# Rank-ten `T^9Q`: exact finite certificate and closure

**Date:** 2026-07-26

## Verdict

Every connected rank-ten cactus with cyclic multiset `T^9Q` satisfies
`s+(G)>|V(G)|`. The disconnected marked endpoint and the fully shared frontier
are both exhausted by exact finite certificates. The new hostile three-cut
obstruction closes by opening its leaf triangle and applying packing one only
to the retained eight-triangle common hub. No all-rank Voronoi or census-free
separator assertion is used.

## Inputs

Write `sigma(G)=s+(G)-|V(G)|`, `T=C3`, and
`delta_q=sec(pi/q)-1<1` for hostile `q=1 mod 4`. We use:

1. induced-partition superadditivity of `s+`;
2. the proved rank-nine cactus theorem, including arbitrary attached trees;
3. `TQ>0`, `TTQ>=0`, and the established connected lower-rank bounds;
4. the common-cut `T^kQ` Schur--Sachs bound; and
5. the one-hostile-cycle packing-one theorem, only when the retained triangles
   are directly certified to contain one common hub.

## Disconnected shared-cut graph

Contract maximal shared-cut cyclic clusters and retain every bridge connector.
The result is a tree. If the cluster containing `Q` contains `k<=8` triangles,
cut all outward bridge branches from that cluster. Its induced territory has
rank `k+1<=9`: it is strict for `k>=3`, is `TQ>0` for `k=1`, and is
`TTQ>=0` for `k=2`. Every remaining nonempty territory contains only triangles;
one is strict whenever the `TTQ` row needs strictness. The case `k=0` is handled
by adjoining the first neighboring triangular cluster; unless it contains all
nine triangles this gives the same lower-rank ledger. Thus the only endpoint
not discharged directly by rank at most nine is

```text
A_9 | Q
```

remains.

The executable `research/decacyclic-t9q-marked-entry-certificate.py` projects
the connector to every possible shared cut or private triangle port, quotients
by marked incidence automorphisms, and runs every legal one-router split. It
certifies

```text
355 unmarked A_9 incidence trees,
3624 canonical marked-entry classes,
6745 physical marked positions before quotienting,
3621 direct one-router certificates,
3 common-hub repairs.
```

The direct ledger uses `TQ>0`, `TTQ>=0`, the strict rank-three-through-nine
theorems, and the exact triangular credits. If the entry is a private vertex of
the sacrificed router, its interval stays with the actual connector and `Q`;
it is not charged as a naked tree.

The executable freezes the three marked signatures and their orbit
multiplicities `1,1,18`; their sum is 20 physical positions. It also checks the
full multiplicity histogram, `6725+20=6745`, and the canonical-class identity
`3621+3=3624`. The three residuals are exact. Two are the common-cut nine-triangle bouquet,
with the entry respectively at the hub and at a private triangle vertex. They
are common-cut or rooted packing-one `T^9Q` packets and have
`sigma>9-delta_q`. The third has a triangle router between a seven-petal hub and
one leaf triangle, with the entry at the router's private vertex. Keeping the
connector with the router retains eight triangles sharing the real hub and the
rooted `Q`; packing one gives `sigma>8-delta_q>0`. Thus all 3624 marked classes
close, including the former `j=0` branch without the false claim that any
four-or-more triangle branch has surplus greater than three.

## Fully shared exact frontier

The executable `research/decacyclic-t9q-incidence-certificate.py` enumerates
all color-preserving bipartite cycle-cut incidence trees, checks degree
capacities, and applies every ordinary one-cycle split with exact `Fraction`
ledgers. The totals by shared-cut count are:

| `Q` capacity | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 12 | 91 | 406 | 1178 | 2115 | 2250 | 1246 | 275 | 7574 |
| 4 | 1 | 12 | 91 | 412 | 1203 | 2187 | 2361 | 1340 | 306 | 7913 |
| 5 | 1 | 12 | 91 | 412 | 1208 | 2201 | 2393 | 1372 | 321 | 8011 |
| 6 | 1 | 12 | 91 | 412 | 1208 | 2204 | 2400 | 1383 | 327 | 8038 |
| 7 | 1 | 12 | 91 | 412 | 1208 | 2204 | 2402 | 1386 | 330 | 8046 |
| 8 | 1 | 12 | 91 | 412 | 1208 | 2204 | 2402 | 1387 | 331 | 8048 |
| >=9 | 1 | 12 | 91 | 412 | 1208 | 2204 | 2402 | 1387 | 332 | 8049 |

For nonhostile `Q`, ordinary splits leave only the common-cut bouquet. Actual
hostility means `q=1 mod 4`; thus `q=7` is nonhostile. For every regime audited
with the weaker hostile ledger (actual hostile capacity five, conservative
capacity seven, and the stabilized capacity-nine universe containing every
actual hostile `q>=9`), the exact frontier has the same three frozen classes:

```text
X(Q()T()T()T()T()T()T()T()T()T())
T(X(Q())X(T()T()T()T()T()T()T()T()))
T(X(Q())X(T())X(T()T()T()T()T()T()T()))
```

The first is a real common-cut `T^9Q` bouquet and has
`sigma>9-delta_q` by the scalar theorem. In the second, all nine triangles
contain one hub and `Q` meets the triangle router at its other cut. It has
packing one and again `sigma>9-delta_q`.

The third is the new three-cut hostile obstruction. A saturated triangle router
meets `Q`, a leaf triangle, and a common-hub branch of seven triangles. The nine
triangles do **not** have packing one, so applying a global packing-one or
Voronoi guard here would be false. Open the leaf triangle instead: its two
private vertices, their edge, and every tree rooted there form one nonempty
induced tree `E`, hence `sigma(E)=-1`. The retained packet has the router and
seven other triangles, all containing the real hub, while `Q` is rooted at the
router's other cut. The packing-one theorem applies to exactly those eight
triangles and gives

```text
sigma(G) >= sigma(H)+sigma(E)
         > (8-delta_q)-1
          = 7-delta_q
          > 0.
```

The certificate materializes final induced territories and gives every router
cut and every cycle attachment a concrete packet or opened-tree owner. It
checks the exact three signatures in each hostile regime, canonical orbit sums,
the real common cuts, router degrees, the openable leaf triangle, and the
eight-triangle common hub. Exact integer-versus-`delta_q` checks certify the
strict margins `9-delta_q`, `9-delta_q`, and `7-delta_q`; no floating-point
comparison is used. Thus the fully shared frontier is finite and every row
closes. Both certificates fail closed under normal Python and `python -O`.

## Remaining gap

There is no remaining gap for `T^9Q`. A full rank-ten theorem still requires
the global cluster-partition synthesis for the other sharp-DNN residual family
`T^8PP`; finite endpoint and fully shared certificates for that family exist in
the separate decacyclic router artifacts.
