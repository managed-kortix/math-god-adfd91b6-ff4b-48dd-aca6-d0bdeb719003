# Rank-eleven `P|A_9|P` marked frontier and certificate obstruction

**Date:** 2026-07-28

## Status

This note records the historical frontier and the audit failure that forced a
theorem-aware redesign. The completed fail-closed endpoint certificate is now
`research/rank-eleven-a9-two-interface-verifier.py`, documented in
`research/rank-eleven-a9-two-interface-fail-closed-note-2026-07-28.md`. The
rejection below remains important: a pure triangular margin cannot also be used
after a remote hostile cycle has entered that packet unless a theorem for the
resulting mixed packet is supplied.

## Exact finite frontier

Extending the established `A_8` two-interface generator to nine triangles
reproduces

```text
355 unmarked A_9 incidence trees,
128155 ordered labelled interface placements,
43151 canonical marked rows,
43116 rows accepted by the provisional pure-triangle router score,
35 zero-score rows.
```

The exact score distribution is

```text
0:       35
1:       59
2:      262
3:     3136
4:    10813
5:    18339
6:    10507
```

and the provisional router-count distribution is

```text
0:       26
1:    35215
2:     7855
3:       55.
```

The independently observed diagnostic digests were

```text
all rows: 0bf53914ae760002386b4b94e4de2d0cccbe61725063b4a46435bcd49c70403b
residual: d90c43d8edfa06e0795625d77cfe3c5ed88a731fe96d109a49876981e9e5fce1
```

These values remain diagnostic until an independent fail-closed generator is
committed.

## Residual geometry

The 35 zero-score rows have exactly three unmarked incidence shapes:

```text
6  common-cut nine-triangle bouquets,
28 two-cut saturated extensions with branch profiles A_7 and T,
1  double-leaf hub with five ordinary petals and two router petals.
```

There are plausible uniform repairs. The saturated rows split according to
whether each demand enters the private router port, the singleton side, or the
seven-fan side. The bouquet rows use openings, one-pivot packets, or demand
coalescence. The double-leaf row has a candidate nested branch-demand
coalescence into `A_5PP` plus two strict triangular packets. These are proof
targets, not accepted certificates.

## Hostile audit of the attempted closure

The attempted verifier failed for four independent reasons.

1. **Ordinary mixed-packet double counting.** Of the 43116 provisionally
   accepted rows, 41863 put at least one external pentagon in a positively
   credited triangular packet, and 32443 put both in credited packets. The
   provisional score still counted the pure `A_k` margin. For example, a
   score-one row sends both demands into an `A_6` packet; the actual packet is
   `A_6PP`, not `A_6+P+P`. No theorem used by the verifier justified the pure
   credit after this absorption.
2. **Declarative packet bounds.** Repair records stored theorem names and a
   claimed bound, but the executable did not derive the bound from a finite
   whitelist of proved packet theorems and checked hypotheses.
3. **Underchecked intervals.** The checker did not require the number of
   interval sizes to equal the number of owners or their sum to equal three.
4. **Manufactured nested owners.** In the double-leaf row, a provisional
   refinement owner was reassigned to `A_5PP` without proving through the
   second split that the inherited adhesion position reached that descendant.

Consequently neither `43151=43116+35` nor the attractive 35 repair templates
is an endpoint theorem. The equality is an exact provisional-router census;
the word `accepted` refers only to that score.

## Exact next certificate

A correct verifier must first materialize final owners for every row, then
replace each pure `A_k` bound by a theorem for the packet after its zero, one,
or two remote pentagons are attached. It may use only:

```text
P, TP, PP, TPP,
connected rank 2 or 3 nonnegative packets,
connected rank 4 through 10 strict packets,
proved common-cut and packing-one packets,
explicit opening costs.
```

It must reject an unrecognized mixed profile rather than retaining the old
pure triangular credit. Every repair must carry concrete proper intervals,
unique cut and connector owners, recursive adhesion ownership, packet
hypotheses, and a theorem-derived exact ledger. This theorem-aware
reclassification of all 43151 rows is the next endpoint task.

## Theorem-aware search refinement

After this frontier was written, the rooted shared-cut two-pentagon hinge
theorem was proved. It is a valid terminal only when the two pentagons
themselves share a cut and the triangular packet has one complete interface to
their lobe. A pair of labelled connector demands on `A_9` does not imply those
hypotheses, so the hinge theorem closes **zero** marked rows merely by profile
recognition.

An exhaustive theorem-aware search using only bounded-rank connected packets,
`P,TP,PP,TPP`, one-hostile packets, and complete-profile demand coalescence
finds coverage for every marked row through eight triangles. At nine triangles
it finds plans for `43145` of `43151` rows. The six conservative residuals are:

```text
4 common-cut A_9 bouquet mark types:
  both marks at the locked hub;
  hub/private, in both label orders;
  private marks on two distinct petals;

2 saturated two-cut extensions:
  one private-router mark and one mark locked on the A_7 fan cut.
```

The smallest is the double-locked bouquet

```text
X[AB](T()^9).
```

Both remote pentagons enter through connectors at the triangular hub; they are
not cyclic blocks sharing that hub. Hence neither the common-cut `T^9PP`
theorem nor the rooted hinge theorem applies. The committed theorem-aware
verifier now reproduces this `43145+6` refinement and closes the six rows by two
explicit router repairs and four pentagon openings. Thus the finite
`P|A_9|P` endpoint is proved; the separated-pentagon analytic obstruction below
remains relevant only to broader all-rank targets.

The six rows identify the true analytic target: a packing-one triangular cactus
with two separated rooted pentagons. Its grouped Sachs polynomial contains the
joint-cycle package

```text
-4D+8iE,
```

absent from the shared-cut hinge. This second-quadrant correction prevents the
coefficientwise phase comparison used in the hinge proof.
