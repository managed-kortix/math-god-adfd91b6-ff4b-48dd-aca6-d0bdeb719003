# Fully shared rank-eleven `T^9PP`: physical closure verifier

**Date:** 2026-07-29

## Scope and verdict

The companion executable independently regenerates the complete fully shared
`T^9PP` incidence universe and the ordinary one-cycle split frontier. It then
materializes every ordinary SAFE row on named `C3` and `C5` vertices, partitions
the sacrificed cycle into concrete consecutive intervals, assigns every
physical vertex and arbitrary-tree attachment site exactly one final owner, and
reclassifies every complete owned terminal packet.

The exact result is

```text
115512 = 115502 ordinary physical-owner SAFE + 10 physical repairs.
```

The verifier now closes the exact ten ordinary residual signatures through the
same independently reconstructed graph, exhaustive final-owner, complete-cycle,
theorem-reclassification, and exact-ledger pipeline. This proves the fully
shared incidence family only; it does not assert the global rank-eleven cactus
theorem or router reachability R11.

## Reproduction

```bash
python3 research/rank-eleven-t9pp-fully-shared-first-phase-verifier.py
python3 -O research/rank-eleven-t9pp-fully-shared-first-phase-verifier.py
```

Both modes must produce byte-identical output. The program uses explicit
`RuntimeError` guards rather than `assert`, so optimization does not remove its
checks.

## Frozen census

| shared cuts | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all | 1 | 22 | 264 | 1790 | 7560 | 20080 | 33154 | 32369 | 16775 | 3497 | 115512 |
| ordinary SAFE | 0 | 20 | 260 | 1788 | 7559 | 20080 | 33154 | 32369 | 16775 | 3497 | 115502 |
| residual | 1 | 2 | 4 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 10 |

Frozen SHA-256 values are:

```text
canonical rows       65f4d845ff0ef17ce7880992810de149fd2108927e2ef03b8fac57032ac72ce2
ordinary signatures f9c743de601ca11eb03bf687ad020475f8a087a4f62af56e58726a3510b30c2b
physical proofs      5d134b875d7ff369c74f361f4fd58a2ee7262c8bfdaba0453987f46f3391b70e
residual signatures  37da45267e16a5c98610ff3a733dbcaeee000c3b089dc16de253e2fbf2feb25c
```

## Physical and theorem gates

For each accepted row the verifier:

1. independently checks the canonical colored incidence tree and capacities;
2. creates distinct named cyclic positions for all nine triangles and both
   pentagons, identifying only positions carrying the same shared cut;
3. binds the sacrificed cycle's occupied ports to ordinary consecutive
   intervals and their final component owners;
4. reconstructs the expected physical vertex, edge, and attachment domains;
5. checks exhaustive, disjoint, connected induced owner territories with the
   shared `geometry_router_owner_core.py` routines; and
6. derives complete owned cycles and selects a theorem from a closed whitelist.

The attachment domain is not copied from submitted physical vertices. For each
independently reconstructed physical anchor the verifier creates a distinct
symbolic arbitrary-forest site and requires it to follow the anchor owner.
Every private position of a sacrificed router has a separate remnant leaf with
an independently reconstructed anchor and edge. Each remnant-bearing
owner-induced graph is checked to be connected and to have cyclomatic number
exactly equal to its complete owned cycle count. Thus it is a cactus with the
derived complete profile plus forest attachments, inside the tree-uniform scope
of the selected theorem.

The generalized physical `C5` statement and proof are in
`research/physical-c5-interval-router-lemma-2026-07-29.md`. The shared core
keeps its old `(2,3)` default and exposes an explicit `C5` entry point for
`d=2,...,5`; `d=4` is forced `1+1+1+2`, and `d=5` is forced singleton.

The whitelist contains exact triangular rank margins, `P`, `PP`, `TP`, `TPP`,
common-cut `TTP`, shared-pair `T^3P`, the rooted common-cut/packing-one
one-hostile theorem, and the proved connected rank-at-most-ten cactus inputs.
An unknown owned profile raises an error. The accepted ledger must be the exact
sum of these post-ownership bounds and must be strictly positive.

The selected-router census is

```text
d=2: 65586, d=3: 43202, d=4: 5334, d=5: 1380.
degree-4 signature sha256 1724a7155021b740373957fbcc81eee7dea4d9bc8892d4e9e2ccd6fa9a887af4
degree-5 signature sha256 e9049b58c3212b15fb3892367822ed1051aa0663e58828b771658fa8544f020c
```

The abstract search has `517923` SAFE cycle choices across the `115502` SAFE
rows. The hardened run constructs and verifies a complete physical theorem
certificate for every one, not only for the first selected witness. Their
ordered certificate stream has SHA-256
`071df2e10153eb21a8153cc3e45de6768e350a2257a692b0b03979227bc37a0f`.

The executable prints the first complete degree-five canonical signature and
freezes the entire 1380-signature stream by digest. Eight hostile mutations
verify rejection of interval overlap, vertex-owner drift, coordinated private
interval/attachment drift, forged theorem, missing attachment domain,
unsupported old-default arity, fifth-interval omission, and coordinated
remnant/domain deletion.

## Physical repair closure

The ten rows are matched by exact canonical signature, not residual order. For
each one the executable reconstructs all `C3`/`C5` positions, physical shared
cuts, sacrificed-router remnants, opening paths, nested refinement order,
attachment domains, and final owners. It then derives complete cycles from the
owner map and reclassifies the terminal theorem before summing the ledger.

| row | physical operation | derived terminal profile | exact ledger |
|---|---|---|---:|
| `U1` | no split; common cut predicate | common-cut `T^9PP` | `>10-4/(3sqrt(13))` |
| `U2` | rooted leaf-`P` opening `1+4` | common-cut `T^9P` + tree | `>8-delta` |
| `U3` | triangle `1+2` router | `P` + common-cut `T^8P` | `>8-2delta` |
| `U4` | `C5` singleton/complement | `A_8+TP` | `>3/4` |
| `U5` | rooted leaf-`P` opening `1+4` | packing-one `T^9P` + tree | `>8-delta` |
| `U6` | forced triangle singletons | `P+T+` common-cut `T^7P` | `>7-2delta` |
| `U7` | corrected one-router `1+2` split | `P+` packing-one `T^8P` | `>8-2delta` |
| `U8` | degree-four `C5` singleton/complement | `T+` rank-nine `T^8P` | `>0` |
| `U9` | two nested triangle refinements | `P+P+T+A_6` | `>1-2delta` |
| `U10` | two nested triangle refinements | `P+P+T+T+A_5` | `>2-2delta` |

The radical predicates are exact rational comparisons after squaring; no
floating-point approximation or qualitative strictness is used as credit.
Twenty-five hostile mutations are rejected (eight ordinary and seventeen repair
mutations), including coordinated U4/U7/U8 owner-domain swaps with rederived
packets and ledgers, forged packet hypotheses and bounds, closed-sibling
retrieval in both nested repairs, and the invalid literal
`U7` extension, a wrong `C5` singleton, reversed nesting/opening, and a forged
common-cut radical charge. Both normal and `-O` runs report `115512/115512`.
