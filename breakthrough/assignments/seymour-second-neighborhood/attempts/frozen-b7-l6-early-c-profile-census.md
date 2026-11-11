# Frozen B7-l6 early C-profile census

## Scope

This is the authoritative early C-profile partition of Frozen Seymour's exact
`m=6`, `B7-l6` clean-parent frontier. It refines all 30 exact C states and all
260 parent/state incidences over the complete set of 42 committed parents. It
does not import witness, coordinate, gain, no-gain, or residual units.

## Exact census

The canonical ordering is
`(internal-C, high-mask, (cb16,cb17), (h16,h17), intersection-t)`. For each
state, the ordered C-to-B subsets are partitioned under the full `S7(B)` action
by their intersection size. This gives exactly 60 orbits and 544
parent/orbit incidences.

The producer applies all 5,040 permutations to every encountered ordered row
size. The checker is independently derived at this layer: it reconstructs the
42 parents from lower-layer checker routines, independently derives all 30
states, and separately exhausts every labelled ordered subset-pair universe
under all 5,040 permutations. It is not fully implementation-independent
because it shares the frozen base CNF generator and audited lower-layer
parsing/checking code. The layer-level derivations agree on representatives,
orbit sizes, parent compatibility, dimensions, manifest, and CNF stream.

For every one of the 30 states, the checker also applies all 5,040 permutations
of `B` to every guarded parent hole support and verifies that the complete
parent-support disjunction is invariant and closed. This checks the grouped CNF
symmetry needed to use one C-row representative, not only closure of the C-row
subset pair itself.

Under this ordering, orbits 34 and 35 have status `CERTIFIED` and are exactly
the certified ordered `(3,1)`
orbits with `t=0,1`. Their existing checked LRAT campaign is bound into the
census. Orbit 31 is the `(2,2),t=0` orbit in state `h24-cr-m10-b22`; it remains
uncertified.

## Scout and status

The reproducible scout covers exactly the other 58 orbits, whose manifest
statuses are explicitly `SCOUT-UNSAT` or `SCOUT-TIMEOUT`. It projects the
already frozen 30-second state scout for states proved UNSAT there, and the
already frozen 20-second hard-orbit scout for unresolved state children. This
is a deterministic provenance projection, not a new solver run. It reports 31
UNSAT, 27 TIMEOUT, and zero SAT rows. The 18 projected state UNSAT outcomes all
finished in under 20 seconds; the other 40 rows use the exact frozen 20-second
hard-orbit sequence. Together with the two existing certified cells, this is 33
eliminated cells, of which only two had retained certificates at census commit
`3e176b4675a4d4676cae9eeab8399a74ef19f265`. A later campaign promotes exactly
the 26 fast cells
`00,01,02,06,07,08,09,10,18,19,20,21,22,24,26,27,29,30,44,45,46,48,50,51,52,53`.
The second package certifies the other scout-UNSAT cells `04,05,31,32,33`.

The census itself records exactly two certified orbits, 34 and 35. With both
later packages, exactly 33 of the 60 profile cells have retained certificates:
those two plus all 31 scout-UNSAT cells. The unresolved set is exactly the 27
scout-TIMEOUT cells, and no scout-UNSAT cell remains uncertified. This remains a
profile-level partition, not a complete `B7-l6`, `m=6`, or Seymour result.

The existing certificate CNFs and census CNFs for orbits 34 and 35 are
serialization-equivalent in the proof-relevant sense: they have the identical
numbered variable map and identical ordered DIMACS clause stream. Their comment
metadata intentionally differs, so their whole-file SHA-256 identities do not.

Exhaustion independently regenerates and compares every one of the 60 complete
CNF file hashes. A strict self-pinned provenance ledger binds the producer,
layer checker, regression test, scout, census, hash ledger, documentation, and
the full transitive local Python runtime-source closure. This is a census and
integrity gate only; it creates no certificate and makes no additional
certification claim.

## Selected scout-UNSAT certificates

Pinned CaDiCaL 1.7.3 generated textual LRAT for exactly the listed 26 cells,
and pinned `lrat-check` accepted every proof. The retained `xz -3` artifacts
total 13,906,564 bytes, below the 250,000,000-byte cap. The strict canonical
certificate ledger and verifier bind each CNF, raw LRAT, compressed artifact,
the committed census provenance chain, the complete transitive local Python
runtime closure, documentation, and pinned producer/checker binaries. Fresh
replay regenerates and structurally checks each CNF, authenticates and
decompresses each artifact, checks the raw LRAT identity, and invokes the
pinned checker. No orbit outside the exact 26-cell scope is certified by this
campaign. The separate five-cell package covers `04,05,31,32,33`; together the
packages cover all 31 scout-UNSAT cells. Their combined compressed size is
90,192,848 bytes.
