# Disconnected rank-nine `T^7PP`: exact marked-interface reduction

**Date:** 2026-07-26

## Verdict

Write `sigma(G)=s+(G)-|V(G)|`, `T=C3`, `P=C5`, and
`delta=sqrt(5)-2<1/4`.  This note sharpens the disconnected rank-nine
`T^7PP` frontier.  It proves the entry-locked family

```text
T^7P_0 | P_1
```

completely by an exact marked-entry census.  It also reduces the two-entry
middle-cluster family

```text
P_0 | A_7 | P_1
```

to one explicit locked bouquet packet, and closes that packet by opening one
remote pentagon and applying the established one-hostile-cycle packing-one
theorem to the other arm.  Thus every disconnected `T^7PP` configuration is
proved.

The two executable certificates are

```bash
python research/nonacyclic-t7p-last-bridge-conservative.py
python research/nonacyclic-t7-two-interface-census.py
```

They use only exact integer and `Fraction` arithmetic.

## Territory and packet rules

Every external connector is projected to its first cyclic-hull vertex.  A
triangle of incidence degree `d` has exactly `3-d` private cyclic vertices.
Splitting a triangle with two marks assigns one marked vertex as a singleton
and the complementary edge to the other owner; with three marks the three
singleton intervals are forced.  Successive splits refine one induced owner.
Thus every incidence branch, connector remnant, shared cut, and hanging tree
has one owner.

The certificates use only established bounds, all valid with arbitrary
attached trees:

```text
sigma(P)>-delta,
sigma(A_r)>b_r, (b_1,...,b_7)=(0,1,2,3,2,1,0),
sigma(common-cut T^kP)>k-delta,
sigma(shared-cut TTP)>2-delta,
sigma(H)>=0 in ranks two and three,
sigma(H)>0 in ranks four through eight.
```

If a connector is cut before its remote pentagon, a private entry interval on
a subsequently split router is charged by `sigma(E)=-1`.  Alternatively, the
connector may remain uncut and its remote pentagon travels with that private
entry interval; then the interval is a pentagonal unicyclic packet and no
separate `E` is charged.  The scripts distinguish these alternatives.

## Entry-locked `T^7P|P`: complete census

The clustered incidence tree has seven triangle nodes and one pentagon node;
the clustered pentagon is required to be an incidence leaf.  Private vertices
of that pentagon are absent because those entries are already settled by the
ordinary pentagon interval argument.  Every cut and every private triangular
vertex orbit is marked.

The exact counts are:

| cut count | 1 | 2 | 3 | 4 | 5 | 6 | 7 | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| all `T^7P` incidence trees | 1 | 9 | 49 | 145 | 245 | 205 | 69 | 723 |
| `P`-leaf trees | 1 | 6 | 30 | 79 | 120 | 86 | 23 | 345 |
| marked-entry orbits | 2 | 29 | 195 | 661 | 1144 | 909 | 248 | 3188 |
| direct one-router certificates | 0 | 24 | 186 | 649 | 1134 | 909 | 248 | 3150 |
| replacement certificates | 2 | 5 | 9 | 12 | 10 | 0 | 0 | 38 |

The 38 replacements use no split in two common-cut rows, one router in nine
rows, two routers in 22 rows, and three routers in five rows.  For every one of
the `3150+38=3188` certificates, the executable now materializes the sequential
router steps, proper interval sizes, interval owners, connector/root owner,
remote-`P_1` owner, unique cut owners, and the correspondence sending arbitrary
off-hull tree attachments to those owners.  It checks connected retained
incidence packets and the common-cut or shared-cut hypothesis whenever that
credit is used.  Sequential refinement is carried through to final owners: an
early interval that contains several provisional packet territories is replaced
by the unique packet owner exposed by the later router splits.  In particular,
the two-router regression class
`X(P()T()T()T()T(X(T()))T(X(T())))` with root cut `8` assigns the first
router's cut-`8` interval, cut `8`, and the root to `packet:1`.  The executable
checks this class explicitly and checks all 38 replacements have only final
packet owners (or the explicit `naked-tree:entry` owner), with no surviving
`territory:*` label.  Thus the certificate no longer relies on an implicit
simultaneous split, synthetic territory owner, or unstated attachment
convention.  These checks use a fail-closed helper rather than Python `assert`,
so they remain active under `python -O`.

The ledger also records the exact strictness of every packet; in particular it
does not force strictness after summation.  It separately computes the sign of
`a-b*delta` by positive-side squaring and accepts equality only when an actual
strict packet is present.  Both pentagonal deficits and every private-entry
tree cost are owned and charged exactly once.  The recomputed census has zero
failures, and the weakest accepted state has

```text
sigma(G)>1-2delta=5-2sqrt(5)>0.
```

There are no failed marked-entry rows.  Together with the prior internal-`P_0`
and private-`P_0` interval cases, this proves every disconnected
`T^7P_0|P_1` configuration.

## Two arbitrary entries on `A_7`: exact reduction

There are 48 unmarked incidence trees of one seven-triangle shared-cut cluster.
The two connectors are labelled and may coincide.  Exhaustive placement on all
cut and private triangle vertices gives 10800 labelled placements before
automorphisms and 3188 canonical marked classes.  The exact router automaton
accepts 3182; 3134 best certificates use one router and 52 use two successive
routers.  The retained triangular incidence components have certified credit
at least one after every naked private interval is charged, so each accepted
ledger is positive after the two pentagonal deficits:

```text
sigma(G)>1-2delta>0.
```

Private connector entries on the split triangle remain joined to their remote
pentagons and are pentagonal unicyclic territories, not naked tree intervals.
This is why no unrecorded `-1` opening cost occurs.

The six ordinary-router residual orbits all occur on the common-cut bouquet.
They are: both entries at the common cut; one cut and one private entry in
either label order; coincident private entries; distinct private vertices on
one triangle; and private entries on two triangles.  Five close by explicit
one- or two-router packetizations:

```text
P + common-cut T^6P,  A_6+PP,  A_6+P+P,  or A_5+P+P.
```

Their weakest ledger is `1-2delta>0`.  The only non-router shape is exact:

```text
seven triangles form a common-cut bouquet at x,
and both bridge connectors enter the bouquet at x.             (B9)
```

In canonical form it has one cut, incidence code
`X(T()T()T()T()T()T()T())`, and marked pair `(x,x)`.  Every bouquet triangle
then has only one mark, so no proper two-owner router split exists.  The
common-cut `T^kPP` theorem does not apply because the remote pentagons do not
contain `x`, and additive separation gives only
`sigma(A_7)-2delta>-2delta`.

Open one remote pentagon, say `P_0`, by placing its four vertices other than
its connector entry, together with every tree branch rooted there, in one
induced territory `E`.  This is a nonempty tree, so `sigma(E)=-1`.  The
complementary induced territory `H` consists of the seven-triangle common-cut
bouquet, the entire other pentagon `P_1`, both joining paths up to the retained
entry of `P_0`, and arbitrary attached trees.  The first joining-path remnant
is acyclic and is merely an attached tree at `x`; the only cyclic blocks of
`H` are the seven triangles and `P_1`.  All seven triangles contain `x`, so
their vertex-packing number is one.  The rooted packing-one hostile-cycle
lemma therefore applies, including an arbitrary joining path to `P_1`, and
gives

```text
sigma(H)>7-delta.
```

Consequently

```text
sigma(G)>=sigma(H)+sigma(E)>6-delta=8-sqrt(5)>0.
```

The opening vertex set excludes the connector entry, so this ownership remains
valid for arbitrary connector length and arbitrary trees on either connector.

## Exact status

Proved here:

1. all 3188 marked-entry classes in the entry-locked `T^7P|P` family;
2. all 3188 canonical labelled two-interface `P|A_7|P` classes, with 3182
   accepted by the uniform router ledger;
3. all six canonical ordinary-router residual orbits, five by explicit
   interface-aware router packets;
4. `(B9)` itself by one remote-pentagon opening and the packing-one theorem.

Not proved in this note: the fully shared census replacements and the global
rank-nine exhaustion, which are separate artifacts.

Thus the disconnected `T^7PP` problem has no remaining row.  In particular,
no new two-hostile-arm analytic theorem is needed: opening either remote
pentagon converts the unique locked row to the already proved one-hostile-arm
packing-one packet with a margin of more than `6-delta` after the exact tree
cost.
