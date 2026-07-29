# Rank-eleven `T^9P|P` geometry-aware exact frontier

**Date:** 2026-07-28

## Verdict

The executable `research/rank-eleven-t9p-p-endpoint-frontier-verifier.py` is
downgraded to an exact geometry-aware census. It certifies no endpoint row and
always fails closed after checking the complete 50399-row universe.

The requested K1 coalescence, K2 opening, and K3--K17 two-router recipes are
now persisted in
`research/rank-eleven-t9p-p-seventeen-repair-blueprint-2026-07-28.md`.
The verifier pins that file at SHA-256
`c56b1830ada29d5b6887d9ddb95a12ddd950052a23854e39e7a4cd92664ecf5d`.
They remain explicitly labelled a proof blueprint rather than a certificate:
they have not been integrated with one uniform graph-level final-owner checker
for all ordinary and private-pentagon rows. Promoting only the 17 recipes while
retaining under-materialized ordinary records would regress the hostile audit.

The former `50382/50399` claim is withdrawn. Its records represented demands
as strings, used an ambiguous synthetic triangle slack position, and did not
materialize complete pentagon and connector geometry. Those records are not
proof certificates.

## Certified census

```text
8011  colored T^9P incidence trees,
3624  trees with the clustered P as an incidence leaf,
43151 triangular-hull rows from 68856 physical placements,
 7248 private clustered-P rows from 14496 physical vertices,
50399 total rows.
```

Both pentagons are now explicit rooted five-cycles with five named vertices
and five cyclic edges. Every connector has a named pentagon root, concrete hull
position, unique symbolic path vertices, and a distinct connector-remnant
attachment object. Every triangle has exactly three named cyclic positions;
incidence cuts occupy actual positions and the remaining positions are private.
The checker enumerates and validates ordered consecutive `(1,2)` and
`(1,1,1)` interval partitions without synthetic slack vertices.

The private clustered-pentagon orbits are derived rather than asserted. The
program constructs all ten actions of `D5`, takes the stabilizer of root `v0`,
and computes its two private orbits:

```text
distance 1: {v1,v4},
distance 2: {v2,v3}.
```

Owner-like incidence ledgers are checked for duplicate keys and exact domains
before conversion to dictionaries. Nine hostile geometry mutations must be
rejected, including malformed pentagon edges, duplicate vertices, moved roots,
aliased remnants, nonconsecutive or incomplete triangle intervals, duplicate
or incomplete owner domains, and an incomplete rooted-C5 orbit.

## Theorem frontier

No one-router, opening, or K-repair record is accepted as a theorem
certificate. Therefore the exact certified theorem frontier is all 50399 rows.
The previously printed 17 identifiers remain only a reported candidate repair
frontier, with diagnostic digest

```text
fcf002bb4150db6dc4c5b19f2e9d76b05de066898413b28ee11c4e0a9619747c.
```

That digest is not a closure claim. A future theorem verifier must integrate
the persisted blueprint, materialize every refinement inside its current active
territory, prove complete terminal connectivity including both actual
pentagons and connector paths, and independently rederive every theorem
hypothesis and exact ledger. Until the same checker covers all 50399 rows, the
exact theorem-certified subset remains empty and the executable fails closed.

## Reproduction

```sh
python research/rank-eleven-t9p-p-endpoint-frontier-verifier.py
python -O research/rank-eleven-t9p-p-endpoint-frontier-verifier.py
```

Both modes must print byte-identical census and geometry diagnostics and then
raise the same explicit `RuntimeError`. No invariant uses `assert`.

The frozen geometry digests are:

```text
incidence geometry:      f1db45b36e04eb68ddf6d549e1daf75c0cdae65b22052505e98abf5d4e9ca530
triangular connectors:   e59ff052f88b00bbfaed46ad8d0fd4a6d6cb42302ad53bf321202066c2d76e8b
private-P connectors:    df3437148c879d78c0595331f3e9d5966e9edf037ea8a12fb5cd64d6df77b90f
combined geometry:       82387e52ea2ab4878de670377d9003c5a66297637abcf28778d223a2b3d39398
```
