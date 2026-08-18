# Frozen B7-l6 ordered C-to-B `(3,1)` elimination

## Scope

This campaign concerns only Frozen Seymour's `m=6`, `B7-l6` base, with ordered
`C=(16,17)`, internal arc `17 -> 16`, high mask `10`, exact ordered C-to-B
row sizes `(3,1)`, and the two simultaneous `S7(B)` intersection orbits
`t=0,1`. It neither imports nor assumes any state, witness, coordinate, or gain
campaign unit.

The immutable base generator is invoked with `robust_witness=True` and
`arc_minimal=True`, so the base includes the global robust-witness and
arc-minimal clause families. The campaign adds no selected witness literals or
witness units. The structural checker independently regenerates those global
families; it does not treat a producer-built CNF as an oracle.

## Exact parent exhaustion

The producer and independent checker begin from the committed placement cover,
placement filter, clean remaining stream, and clean parent manifest. They
reconstruct all 42 committed `B7-l6` parents. For each parent they directly
count the forced outgoing arcs from each C vertex to `R union A`, include only
the fixed internal contribution of `17 -> 16`, impose high mask `10`, and test
whether the remaining available B arcs have ordered counts `(3,1)`.

Exactly ten parents pass, with `(accepted ordinal, cover index)`:

```
(23728,112443) (23737,112460) (24899,114188) (24952,114264)
(24958,114275) (29966,121458) (30098,121657) (30101,121663)
(41947,138180) (42075,138397)
```

The other 32 committed parents fail the direct profile test. Thus the ten-way
selector ALO in each grouped CNF is the exact support disjunction for this
profile, not a selected subset of a larger compatible family. The canonical
ten-parent payload SHA-256 is
`0062dc3e08d197650e7f1e23e07e98746901c62786327c7521c2a5b458d83dc2`.

Independently, the checker enumerates all 245 ordered pairs `(X,Y)` with
`X subset B`, `|X|=3`, and `Y subset B`, `|Y|=1`, then applies all 5,040
permutations of `S7(B)`. This gives exactly two disjoint exhaustive orbits, of
sizes 140 and 105, distinguished by `|X intersect Y|=0,1`. The checked
representatives are respectively `({9,10,11},{12})` and
`({9,10,11},{9})`; these are derived rather than assumed as an orbit census.

## CNFs and certificates

For `t=0`, the representative rows are `{9,10,11}` and `{12}`. For `t=1`,
they are `{9,10,11}` and `{9}`. Each grouped CNF consists only of the immutable
B7 base, three profile units, all 14 signed C-to-B arc units, the exact ten-way
parent ALO, and 153 guarded hole-projection clauses per parent. Each has 23,626
variables and 144,277 clauses. There are no state counters, robust-witness
units, witness-coordinate clauses, or gain/no-gain clauses.

Pinned CaDiCaL 1.7.3 produced textual LRAT for both grouped CNFs with
`--lrat --no-binary`; pinned `lrat-check` accepted both with `c VERIFIED`.
The compressed proofs total 36,404,128 bytes, strictly below the exclusive
250,000,000-byte limit.

The canonical certificate ledger binds the manifest, CNF hash ledger,
producer, independent checker, hostile tests, certificate producer, and the
exact transitive local Python runtime closure. It also pins the CaDiCaL and
`lrat-check` binary SHA-256 values and mutually pins the canonical ledger and
verifier. Replay validates exact artifact paths, identities, clause families,
selector block/ALO, all guarded projections, and the required `c VERIFIED`
checker output.

| t | CNF SHA-256 | raw LRAT SHA-256 | xz bytes | xz SHA-256 |
|---:|---|---|---:|---|
| 0 | `0c06a73c9308bae4eee1b309362485d24ed6508c7de8e64bf87c647805048b5f` | `5ea2cb24af68ab9bfd8ad208da63277a2647c4cca50031244e8ef0fce22071c0` | 22,000,348 | `9d136d538658ad44326dba02c554fec6cf13ee845e3c8c0d6a0baacc9bab9282` |
| 1 | `d6bc88cf265db8aaaf5ff6f93160c0ca24bb7c1ba9341ad5704c9f29795eae2a` | `d40c40103b31cd9798768992f6eaaf09caecf34809adf7d7f7697b45256ad20f` | 14,403,780 | `db833fb632b84917217ebd68d98ee7381f8a9332c5620bded2d1c6b928972be3` |

## Result

Both exact intersection orbits are UNSAT. Therefore no orientation satisfying
the frozen B7 base and the exact committed ten-parent support disjunction has
the stated ordered C-to-B profile `(3,1)`, internal arc `17 -> 16`, and high
mask `10`, for either `t=0` or `t=1`. This is a profile elimination only; it is
not a full `B7-l6`, `m=6`, or Seymour conjecture result. No commit was made.
