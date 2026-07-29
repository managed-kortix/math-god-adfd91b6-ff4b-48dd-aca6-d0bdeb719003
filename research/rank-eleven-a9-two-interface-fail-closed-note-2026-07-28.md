# Rank-eleven `P|A_9|P` fail-closed verification note

**Date:** 2026-07-28

## Scope

`research/rank-eleven-a9-two-interface-verifier.py` is restricted to the
rank-eleven `P|A_9|P` endpoint. It does not claim a rank-eleven cactus theorem,
an all-rank separator theorem, or a theorem for two arbitrary separated hostile
cycles.

The executable independently generates the 355 unmarked nine-triangle
incidence trees, all 128155 ordered labelled placements, and 43151 canonical
marked rows. It verifies the canonical-row digest

```text
0bf53914ae760002386b4b94e4de2d0cccbe61725063b4a46435bcd49c70403b.
```

Its concrete cyclic interval checks now use
`research/geometry_router_owner_core.py`, shared with the T9P frontier
verifier. This extraction does not alter any A9 count, record, digest, or
printed output.

It searches standard recursive triangle routers, checks proper interval sizes,
resolves retained cuts and marked demands, assigns each pentagon exactly once,
and classifies terminal packets from a closed theorem whitelist. Unknown mixed
profiles raise an error. The whitelist contains pure triangular strictness,
the `P`, `TP`, `PP`, and `TPP` bounds, connected rank 2/3 nonnegativity,
connected rank 4 through 10 strictness, and one-hostile common-cut or
packing-one quantitative bounds after their incidence hypotheses are checked.
The complete-profile coalescence transition is available only inside the
current active territory and only for two complete singleton pentagon demands.

## Exact theorem-aware census

The independent generator reproduces exactly six specified residual signatures
with digest

```text
248a595dfebef2cdb2caaa0c0f9d0d729ff0e1be71d3345bfc4cb2869072b26d.
```

The hardened search now proves exactly

```text
43145 / 43151 rows,
```

and its search residuals are exactly the six specified signatures. Frozen
digests are

```text
ordinary accepted signatures:
  8d170ef9af714c6288214e5933826fcbfe2d006dc0e70c7277a393fc2d18239c
ordinary theorem/owner records:
  d59ea6b38bef5f5bcdd2d6dbf2ebcb40db7096059c573c53c49122785de904c2
```

The previous `43135` implementation omitted fifteen explicit two-arm plans;
five of those rows happened to have alternative standard plans, so the count
deficit was ten. The corrected plans split the first marked router with the
private connector and outer-arm cut in one concrete size-two interval and the
common-hub cut in the singleton interval. The second marked router remains in
that hub child and is split recursively with the same ownership rule. Thus no
closed sibling is retrieved. Their fifteen arm-size pairs are exactly all
positive pairs `(a,b)` with `a+b<=6`; the retained pure hub has `7-a-b`
triangles. Each plan has profile

```text
A_a P_A + A_b P_B + A_(7-a-b),
```

where `A_1P` is the quantitative `TP` theorem and larger arms use the checked
common-cut one-hostile theorem. Every plan is positive; the smallest is
`TP+TP+A5 > 2-2*(sqrt(5)-2)`. The frozen two-arm owner-plan digest is

```text
c609dbaec9d7c8abe4e66c5f01375e88b28e56b77110c2be17e026eb46f48f5c.
```

The verifier independently rederives every terminal packet from its concrete
cycle and demand sets and compares the packet name, theorem, hypothesis, and
exact bound. It checks branch exhaustion and disjointness; partitions the three
actual router positions into cyclically consecutive intervals; binds ordered
interval sizes to those position owners (so `(2,1)` cannot be changed to
`(1,2)`); verifies nesting by active cycle sets; recursively resolves every cut
and connector to its final packet; and checks connected terminal carriers and
theorem-derived radical ledgers. An unrecognized or mutated profile fails
closed.

## Safe residual repairs

For audit purposes the executable materializes the reported repairs for the
specified six signatures before reaching the fail-closed count gate:

```text
R1-R2: split the saturated router into TP plus packing-one A7P;
R3-R6: open PA at a named nonconnector pentagon vertex and retain
       packing-one A9P through the connector interval.
```

For `R1-R2` it checks the `(2,1)` triangle intervals, TP/A7P owners, both
connector labels, both cuts, seven pairwise-intersecting retained triangles,
and the exact symbolic ledger `8-2*(sqrt(5)-2)>0`. For `R3-R6` it checks the
named opening vertex role, `(1,4)` pentagon intervals, exact opening cost `-1`,
connector and hub ownership, nine pairwise-intersecting retained triangles,
and `8-(sqrt(5)-2)>0`. The frozen repair digest is

```text
9b8631b8d1b92970584156e2e444fedf78c2394e0867d43c1204aa09c4f49e0e.
```

The opening certificate now contains five distinct abstract pentagon vertices
in cyclic order. The connector root is the singleton retained owner; deleting
it leaves the other four vertices as one path owned by the opening territory.
The attachment-owner map is required to equal the vertex-owner map, so every
off-cycle attachment follows its actual pentagon vertex. Repair packet
theorems and bounds are rederived, cycles and demands are distinct and
exhaustive, cut owners must agree with incident retained packets, connector
owner names must exist and be reachable, and the opening ledger is recomputed
as the retained packet bound plus cost `-1`.

Seven built-in mutation tests must all be rejected: a forged ordinary bound,
swapped ordinary interval sizes, broken recursive active ownership, a forged
repair theorem, swapped repair intervals, a corrupted pentagon vertex owner,
and an unreachable opening connector owner. The swapped interval gate now runs
through the shared geometry-aware core.

These checks establish the finite `P|A_9|P` endpoint certificate only. They do
not prove a generic separated-two-pentagon theorem, the complete rank-eleven
cactus induction, or an all-rank router theorem.

## Reproduction

Run both modes:

```sh
python research/rank-eleven-a9-two-interface-verifier.py
python -O research/rank-eleven-a9-two-interface-verifier.py
```

Both modes complete successfully and print byte-identical census, theorem-use,
owner-plan, residual, and repair diagnostics. All count and digest gates use
explicit `RuntimeError` checks and therefore remain active under `python -O`.
