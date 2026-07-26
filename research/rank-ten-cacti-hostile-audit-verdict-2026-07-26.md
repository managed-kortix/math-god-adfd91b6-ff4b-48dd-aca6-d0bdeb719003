# Hostile audit verdict: connected rank-ten cacti

**Date:** 2026-07-26

## Verdict

**ACCEPT.** The current artifact set is acceptable as a fail-closed proof
that every connected cactus of cyclomatic rank ten satisfies

```text
s+(G)>|V(G)|.
```

The mathematical synthesis and all principal endpoint certificates reproduce,
including under `python -O`. The previously blocking defect at the global
exhaustion gate has been repaired: the malformed expected `T^9Q` tuple in
`research/rank-ten-cactus-residual-partition-audit.py` now agrees with the
generated row

```text
Q+T+T+A_7.
```

The corrected verifier passes in ordinary and optimized modes and certifies
`97/96/92/4` and `181/180/170/10`. No mathematical counterexample or further
blocker was found in the marked or fully shared families.

## 1. Reproduction

The following endpoint and replacement certificates passed in both ordinary
Python and `python -O`:

```bash
python3 research/rank-ten-a9-one-interface-census.py
python3 -O research/rank-ten-a9-one-interface-census.py
python3 research/rank-ten-t8p-entry-locked-census.py
python3 -O research/rank-ten-t8p-entry-locked-census.py
python3 research/rank-ten-a8-two-interface-census.py
python3 -O research/rank-ten-a8-two-interface-census.py
python3 research/rank-ten-t9q-template-closure-verifier.py
python3 -O research/rank-ten-t9q-template-closure-verifier.py
python3 research/rank-ten-t8pp-nine-exceptions-resolution.py
python3 -O research/rank-ten-t8pp-nine-exceptions-resolution.py
```

They reproduce:

1. `A_9|Q`: `3624=3618+6`, with the frozen row and residual digests;
2. entry-locked `T^8P|P`: `11689=11586+100+3`;
3. `P|A_8|P`: `11689=11674+15`, including every residual repair;
4. hostile fully shared `T^9Q`: all three exceptions at capacities five and
   nine; and
5. fully shared `T^8PP`: `30386=30377+9`, with all nine replacements.

The standalone fully shared census also produced the claimed totals before the
combined long run timed out while repeating later commands. The dedicated
`T^9Q` and `T^8PP` closure verifiers completed separately, so this timeout is
not itself a blocker.

The designated global commands pass:

```bash
python3 research/rank-ten-cactus-residual-partition-audit.py
python3 -O research/rank-ten-cactus-residual-partition-audit.py
```

Both print the four frozen `T^9Q` structural rows, the ten frozen `T^8PP`
structural rows, and the three endpoint normal forms.

## 2. Census and normal-form attack

The sharp-DNN normal form is exact. With ten cyclic blocks the residual failure
set is precisely

```text
T^9Q, q>=3,
T^8PP.
```

The symbolic comparisons in the frontier note correctly separate every other
cycle multiset. `Q=T` is included in `T^9Q`, and the two residual families are
disjoint because `T^8PP` has exactly eight triangles.

For a residual cactus, maximal shared-cut cyclic clusters joined by actual
bridges form a reduced tree. The one-node/multiple-node dichotomy is exhaustive:
one node is handled by the fully shared incidence census; multiple nodes are
handled by colored cluster profiles followed by tree topology. The integer
partition generator returns the stated cardinalities and the expected four and
ten structural rows. The corrected frozen expected table agrees exactly and
passes under `python -O`.

The marked incidence universes cover
every shared cut and every actual private triangle vertex; ordered interfaces
may coincide. Color-preserving canonicalization, capacity stabilization for
`Q`, score distributions, exception signatures, and row digests reproduce.

## 3. Root and interface completeness

The three disconnected kernels are the correct endpoint targets once the
reduced-tree pruning is accepted:

```text
A_9|Q,
T^8P|P,
P|A_8|P.
```

For `A_9|Q`, projection to the first cyclic-hull entry is complete: an entry is
either a shared cut or an actual private triangle vertex, and an entry through
an off-hull tree projects to its unique hull attachment. The marked universe has
355 unmarked incidence trees, 6745 labelled placements, and 3624 canonical
rows.

For `P|A_8|P`, both labels range independently over the same complete interface
universe, including coincidence. The 36414 ordered placements quotient to
11689 canonical rows. The accepted plans have exact score at least one; all 15
zero-score rows are materialized separately.

For `T^8P|P`, the proof explicitly separates the ordinary internal-pentagon and
privately entered leaf-pentagon interval cases from the entry-locked family.
The latter enumerates all 1105 incidence-leaf `T^8P` shapes and every shared-cut
or private-triangle entry orbit, giving 11689 rows. This matches the rank-nine
normal form and does not omit a locked cut entry.

## 4. Packet scopes, strictness, and ledgers

The accepted router rows use only packet bounds within their stated scope:
proved lower-rank cacti, triangular margins, `TP`, `PP`, `TPP`, scalar
common-cut packets, and one-hostile-cycle packing one. The finite programs do
not purport to prove those analytic inputs; they check that each selected
packet has the required color profile and incidence hypothesis.

Strictness is retained correctly. Zero numerical ledgers are accepted only
with a strict summand. In particular, the coincident-private `A_7+PP` repair is
strict because `A_7` is strict, while `PP` need only be nonnegative. The hostile
`Q` ledgers distinguish strict `TQ`, nonnegative `TTQ`, and strict lower-rank
packets. All displayed radical margins are positive by exact comparisons; no
floating-point sign decision is used.

The fully shared exception verifier checks packet connectivity, common-cut or
packing-one hypotheses, cycle coverage, and strictness. The weakest
two-pentagon router margin is

```text
1-2delta=5-2sqrt(5)>0.
```

The N4 pentagon-router case checks all 60 placements of its three marks and
uses the established `TP>3/4` packet rather than an unproved cyclic-order
shortcut.

## 5. Router and final ownership

The local triangle-router theorem is sufficient for every router actually used:
two marks produce proper intervals of sizes `1+2`; three marks produce three
singletons; later splits refine one existing induced territory. The marked
verifiers check branch disjointness and exhaustiveness, router activity,
interval sizes, nesting, and final cut owners.

The entry-locked certificate resolves provisional `territory:*` labels through
later refinements and rejects any unresolved synthetic owner. The two-interface
certificate assigns both remote pentagons and both connectors exactly once,
checks that each marked entry belongs to its declared packet, and prevents a
destroyed router triangle from reappearing in a terminal packet. The fully
shared replacement verifier likewise rejects packet overlap and multiple cut
owners.

The three new locked `T^8P|P` repairs are less richly materialized than the 100
inherited finite replacements, but their graph operation is unambiguous: open
the remote pentagon, assign its four private vertices to one nonempty tree, and
retain both connector remnants with the eight-hub-triangle plus clustered-
pentagon packet. The checked incidence shape and common hub make the cited
packing-one theorem applicable.

## 6. Arbitrary connectors and attachments

No accepted global move contracts a connector and forgets its vertices.
Reduced-tree cuts occur at actual bridges. Connector remnants follow the entry
interval or retained endpoint packet. Off-hull trees have one first hull
attachment and follow that attachment's final owner.

The scalar common-cut estimates are uniform over arbitrary rooted trees. The
packing-one theorem is uniform over arbitrary joining paths and trees attached
to the cycles or path. Explicit cycle openings assign every private opened
vertex and every tree rooted there to the opened tree territory while retaining
the shared cut and connector side with the cyclic packet. Therefore connector
length, branching along connectors, coincident entries, and arbitrary finite
attachments introduce no uncharged territory in the audited finite closures.

## 7. Fail-closed `-O` attack

The hardened endpoint and replacement scripts use explicit `require`/`check`
exceptions and pass under `python -O`. Their imported marked-router dependencies
are also hardened.

The base incidence generator still contains Python `assert` statements, so the
standalone compressed census is not independently fail-closed at every internal
invariant. The dedicated closure verifiers compensate for the theorem-critical
totals, signatures, ownership, and replacement checks with explicit failures,
and ordinary/optimized outputs agree in the audited runs. This residual design
weakness is not promoted to a second blocker because the controlling endpoint
verifiers recheck the theorem-critical conclusions explicitly.

The partition audit is fail-closed and now passes its corrected frozen
expectations in both execution modes.

## 8. Separator and two-pivot firewall

The proof does not invoke candidate Lemma S. It enumerates the rank-ten
incidence universes and supplies explicit finite replacements where the router
automaton does not accept. No step infers that an arbitrary triangular
incidence tree must contain a good separator.

The proof also does not invoke the open two-pivot winding inequality. Every
two-interface endpoint is resolved by proper-interval routers, a proved bounded
`TP`/`PP` terminal, a scalar common-cut packet, packing one, or an explicit
pentagon opening with its exact tree charge. The direct two-pivot Schur state is
never converted into an integrated phase bound.

The use of `TPP` in the ordinary finite ledger is only the already proved
bounded rank-three packet. It is not the proposed arbitrary-rank separator and
not a hidden two-pivot theorem. The known separator counterexamples therefore
remain excluded rather than silently assumed away.

## Final finding

The hostile audit finds no remaining blocker. The previous blocker was:

```text
B1. RESOLVED: expected_t9q contained one extra singleton triangle in the
    Q+T+T+A_7 row. The tuple was corrected and both execution modes pass.
```

The current marked censuses, normal forms, interface completeness, packet
scopes, final ownership, arbitrary-tree coverage, strict ledgers, and
two-pivot/separator firewall withstand the audit. The verdict is unconditional
`ACCEPT` relative to the proved analytic inputs cited by the synthesis.
