# Rank-seven orders 8--12: structural main-lane roadmap

## Decision

Do not make completion of orders 8--12 depend on a corpus of independent
rational Grams.  Keep the order-eight search as a bounded fallback and source
of conjectures, but put the main lane through the marked rank-six edge-opening
reduction, a cubic order-twelve theorem, and transport of that theorem through
the degree-excess strata at orders eleven down to eight.

The preferred order of mathematical attack is

```text
all-order marked-owner interface -> order 12 -> order 11 -> order 10
                                  -> order 9 -> order 8 exceptional packets.
```

This is not the order of smallest raw residual count.  It is the order in which
the kernels have the least structural entropy and in which one theorem has the
largest downward reuse.  Order eight remains the best finite-certificate
fallback, not the best theorem-discovery lane.

## Exact snapshot

The census counts below are complete exact orbit counts.  A frontier target is
the canonical row plus every one-coordinate length-plus-two row.

| order | kernels | parity orbits | coarse residual orbits | targets per residual | coarse residual targets |
|:--:|--:|--:|--:|--:|--:|
| 8 | 4,015 | 26,426,026 | 493,417 | 15 | 7,401,255 |
| 9 | 4,495 | 65,167,570 | 2,835,895 | 16 | 45,374,320 |
| 10 | 3,396 | 98,342,348 | 8,208,285 | 17 | 139,540,845 |
| 11 | 1,391 | 82,561,174 | 11,424,569 | 18 | 205,642,242 |
| 12 | 365 | 29,747,798 | 6,138,723 | 19 | 116,635,737 |

The exact coarse residual total over orders 8--12 is `29,100,889` orbits and
`514,594,399` frontier targets.  This arithmetic is the main reason not to use
one unrelated rational payload per target.

### Owner coverage at the snapshot

| order | exact completed owner statement | exact remainder | status boundary |
|:--:|:--|--:|:--|
| 8 | 605 elementary payload-free rows plus 204,766 rows from the rational one-parameter SOS family; disjoint union 205,371 | 288,046 rows / 4,320,690 targets | complete scan; 41.62% of coarse residual rows owned by these lanes |
| 9 | first 2,110,183 residual rows scanned; 1,817,460 owned | 292,723 among the scanned prefix | scan is incomplete (74.41% of the universe scanned), so there is deliberately no full owner percentage |
| 10 | no persisted completed owner manifest | 8,208,285 before the in-progress owner scan | exact census complete; owner aggregation in progress |
| 11 | no persisted completed owner manifest | 11,424,569 before owner scan | exact census complete; scan code exists but no authenticated result |
| 12 | switched three-ray owner: 1,430,594 | 4,708,129 rows / 89,454,451 targets | complete exact classification of this owner only; 23.30% owned |

For order eight, exact rational packs currently persist rows `0--12,999` of the
492,812-row rational-search stream, with rows `13,000--16,999` running at the
snapshot.  Those packs are useful insurance but do not change the structural
owner count in the table: their witnesses overlap the parametric lane and have
not been merged into a disjoint theorem ledger.

For orders nine through eleven, owner coverage must not be inferred from a
prefix, a running process, or the order-twelve percentage.  Publish the exact
numbers only after canonical manifests have been written and replayed.

## Structural lanes

### Lane A: marked rank-six owner interface (highest leverage)

Materialize, for every DNN-owned rank-six deletion state, a checked tuple

```text
(typed owner, exact excess E_e, marked endpoints, correlation r_e).
```

Then apply the proved restoration gate

```text
E_e + f_q(r_e) <= 6.
```

Every restored path of length at least three closes automatically when
`E_e<=5`.  Consequently only canonical short signed supports and one-ear
extensions of typed structural rank-six owners survive.  The output needed from
this lane is an exact support-family manifest for each order, not a Gram pack.

This lane precedes order-specific work because it can delete most rows at every
order and supplies the transport mechanism from order twelve downward.

**Blocker A1.**  The completed rank-six theorem is unmarked: most owner records
do not persist endpoint correlation and slack.  Structural rank-six owners have
no Gram at all.  A new fail-closed marked-owner API is required; merely invoking
the rank-six theorem is invalid.

**Blocker A2.**  There is no universal good-edge/minimax argument on the short
class.  The doubled-edge `K5` support proves that every edge-opening test can
fail although a separate structural packet closes the graph.  The short
manifest therefore needs explicit direct-obstruction tags.

**Estimate.**  Two to four research days for the marked schema, replay checks,
and a first all-order support manifest; another two to five days to classify
the typed non-DNN one-ear extensions.  Runtime should be streaming-census scale,
not witness-search scale.

### Lane B: order-twelve cubic cycle/cut theorem

Order twelve has only cubic kernels: 365 supports and eighteen physical edges.
Use the exact switched three-ray criterion as the first member of a finite
family of nonlocal cycle/cut Grams.  Mine the 4,708,129 failures by switching
class and cycle-space signature, then seek one of:

1. a four-ray or small spherical-code extension of the six-state owner;
2. a cycle-space projection Gram with an exact PSD factorization;
3. a signed-adjacency polynomial with type-dependent diagonal scaling; or
4. a finite exceptional switching theorem reduced to induced packets.

The deliverable is a theorem saying that every cubic signed support is owned by
one of finitely many checked geometries, followed by a complete owner manifest.
The present three-ray failure count is training data, not evidence that
4.7 million exceptional proofs are needed.

**Blocker B1.**  Three rays leave 76.70% of coarse residual orbits.  Local
signed imbalance is known to cost nine on the all-odd simple cubic row, so any
uniform local formula is impossible; cycle or cut information is mandatory.

**Blocker B2.**  The current signed-adjacency-square candidate owns zero rows in
the completed order-twelve manifest.  Coefficient-grid expansion without a new
PSD mechanism is low value.

**Estimate.**  Three to seven research days to obtain a decisive finite-family
experiment and exact conjecture; one to three weeks for proof and hostile audit
if the failure classes collapse.  Stop after one week if no family covers at
least 90% of the three-ray remainder or produces a sharply characterized
exceptional class.

### Lane C: defect transport, orders eleven to eight

For a rank-seven kernel of order `n`, the total degree excess over cubic is
`24-2n`.  Thus orders 11, 10, 9, and 8 have excess `2, 4, 6, 8`: respectively
one small defect, two, three, and four.  Treat them as cubic cores with bounded
vertex-splitting/contraction defects rather than as unrelated kernel lists.

Prove a local replacement lemma that transports a cubic owner across one
degree-excess operation while spending explicit slack.  Where slack is zero,
record a finite interface state and compose these states for at most four
defects.  Apply in this order:

```text
order 11: one defect -> order 10: two defects -> order 9: three defects
          -> order 8: four defects.
```

The order-eight payload-free union, dominated by the one-parameter SOS family,
already owns 41.62% and can serve as the terminal fallback for defect states
not handled by transport.  Its next useful generalization is typed diagonal
scaling keyed to local defect type, not more scalar coefficient grids.

**Blocker C1.**  A cubic theorem must expose slack and interface correlations;
a Boolean owner label cannot be transported.

**Blocker C2.**  Suppression, splitting, and parallel-bundle changes must
preserve the canonical-plus-coordinate frontier.  A proof only for canonical
lengths is insufficient.

**Estimate.**  After Lane B, two to four days for the one-defect lemma and
order eleven; one to two additional weeks for the bounded-state composition
through order eight.  If the number of interface states grows beyond a few
hundred, switch to exact automaton minimization rather than hand packets.

### Lane D: exceptional structural packets

Collect failures of Lanes A--C by typed support, dual stress, and induced
subgraph.  Prove packets for families, never individual parity rows.  Likely
owners include exposed simplex stresses (`K5`, `K4+K4`, mixed-pair assemblies),
induced favorable lower-rank pieces, and one-ear extensions of the finite
non-DNN rank-six owner list.

**Estimate.**  One to three days per genuinely new packet family.  A residual
with thousands of signatures is evidence that the preceding structural state
space is missing an invariant, not a request for thousands of packet proofs.

## Execution order and gates

1. **Freeze census truth.**  Finish and replay the order-nine and order-ten
   owner scans; build and replay order eleven.  This is bookkeeping, not the
   main proof lane.  Gate: one canonical disjoint owner/remainder manifest per
   order, all with `full_theorem=false`.
2. **Build the marked deletion ledger.**  Start with a stratified sample from
   each order, then stream all exact censuses.  Gate: every accepted row replays
   `(E_e,r_e,q_e)` exactly and every structural deletion is typed rather than
   discarded.
3. **Solve the cubic owner problem.**  Work on switching/signature classes of
   the exact 4,708,129 order-twelve remainder.  Gate: a proved finite geometry
   family with an independently checked PSD/cost reconstruction.
4. **Transport by degree excess.**  Close order eleven, then ten, nine, and
   eight.  Gate at each order: exact manifest partition into transported,
   marked-edge, direct packet, and unresolved owners; no overlap and no omitted
   frontier targets.
5. **Use rational search only on the final bounded remainder.**  Continue the
   durable order-eight jobs while idle resources exist, but do not launch
   order-nine through order-twelve rational corpora.  Promote a rational result
   only if it reveals a reusable formula or if the final structural remainder
   is small enough for a compact audited appendix.

## Feasibility and stop rules

- **Order 12: highest theorem value, medium risk.**  Low kernel entropy and
  exact owner failures make it the best discovery lane despite 4.7 million
  rows.  Continue while each experiment is signature-level and payload-free.
- **Order 11: high feasibility after cubic closure.**  Only two units of degree
  excess; this is the clean test of the transport lemma.  Do not attack its
  11.4 million rows independently.
- **Orders 10 and 9: medium feasibility by bounded composition.**  Their raw
  residual growth is hostile to certificates but their defect depth remains
  two and three.  Require state reuse across kernels before scaling a scan.
- **Order 8: high finite feasibility, lower structural priority.**  Existing
  exact search indicates that brute closure is practical, but 4.32 million
  targets remain outside current payload-free lanes.  Keep it as insurance and
  the final four-defect test, not as the template for higher orders.
- **Global stop rule.**  Do not generate a new rational witness corpus above
  one million targets unless a structural scan has first proved that the
  remainder has fewer than 1,000 support/interface classes and no plausible
  common owner.  Store formulas and class witnesses in preference to row
  payloads.

The optimistic structural schedule is two to four weeks to decide whether a
cubic-plus-defect theorem closes the branch, followed by one to two weeks of
exact manifests and hostile audit.  The pessimistic outcome is still valuable:
within one week Lane B should either expose a finite cubic obstruction list or
demonstrate that a different global inequality, rather than more Gram search,
is required.
