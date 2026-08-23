# Frozen B7-l6 remaining early C-profile certificates

## Scope

This package is restricted to Frozen Seymour's five early C-profile census
cells `04,05,31,32,33`. They are exactly the `SCOUT-UNSAT` cells omitted from
the separate 26-cell fast campaign. It imports no timeout cell and makes no
broader `B7-l6`, `m=6`, or Seymour claim.

## Checked certificates

Pinned CaDiCaL 1.7.3 generated one textual LRAT per cell, and pinned
`lrat-check` accepted all five. The new `xz -3` artifacts total 76,286,284
bytes. Together with the fast campaign's 13,906,564 bytes, the complete 31-cell
SCOUT-UNSAT package is 90,192,848 bytes, strictly below 250,000,000 bytes.

A separate strict ledger and verifier bind the prior ledger, frozen census
inputs, certificate producer, transitive local runtime sources, regenerated
CNFs, raw LRATs, and compressed artifacts. Fresh replay regenerates and
structurally checks every CNF, authenticates and decompresses every artifact,
checks every raw LRAT identity, and invokes the pinned checker. Failed staging
is removed atomically by the producer; no failed certificate is retained.

Production compression invokes exactly `/usr/bin/xz`, authenticated by SHA-256
`b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0`.
Replay requires an explicit canonical path to the checker binary and verifies
its pinned SHA-256 before use. Together with the 26-cell package and existing
certified cells 34/35, this gives 33/60 retained certificates, 27 unresolved
scout-TIMEOUT cells, and zero uncertified scout-UNSAT cells.
