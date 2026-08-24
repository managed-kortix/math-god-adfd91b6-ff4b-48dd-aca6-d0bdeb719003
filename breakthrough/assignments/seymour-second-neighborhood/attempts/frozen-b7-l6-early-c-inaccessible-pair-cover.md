# Frozen B7-l6 early C inaccessible-pair cover

## Scope

This layer covers only the eight unresolved one-high early C profiles
`03,11,23,25,28,47,49,54`. It creates no certificate and makes no claim about
the other early profiles or the full Frozen Seymour instance.

## Exact-distance lemma

Fix one of these profiles and let `c` be its unique low C vertex. The profile
unit for `cnt_d1_c_17_9` is false, while the base requires outdegree at least
eight, so `d+(c)=8`. Among the other 17 vertices there are therefore exactly
nine nonoutneighbors of `c`.

The CNF variable `q_c_v` is true exactly when there is a directed two-walk
`c -> k -> v` and no arc `c -> v`. Thus on a nonoutneighbor it is precisely
exact-distance-two accessibility, not mere existence of a walk and not
distance at most two. First and exact second neighborhoods are disjoint.

If at most one of the nine nonoutneighbors were inaccessible, at least eight
would be exact second neighbors. Hence `d++(c) >= 8 = d+(c)`, contradicting the
base badness condition. Therefore every model has at least two inaccessible
vertices among those nine. Adding `-q_c_t` and `-q_c_u` for a selected pair is
therefore an exhaustive existential cover.

This is an overlapping cover, not a partition: a model with three or more
inaccessible nonoutneighbors can satisfy several labelled pair children. The
argument needs only that every model lies in at least one child. No
at-most-one claim is made for pair children.

## Safe quotient and parent support

For each profile and each frozen parent support, the pair universe is derived
from the 2-subsets of that parent's exact nine-element nonoutneighbor set. The
full stabilizer in `S7(B)` of the fixed ordered C-to-B rows acts on this union.
Pairs are quotiented only under that stabilizer. A canonical pair child carries
exactly the parent selectors for which both endpoints are nonoutneighbors; all
incompatible selectors receive negative unit clauses. This avoids the unsound
step of quotienting a pair while forgetting which parent supports it.

The independent checker enumerates all 5,040 B permutations, filters each
profile stabilizer, derives the parent supports and pair universe separately,
checks parent-family invariance together with transformed compatibility, and
checks disjoint complete pair-orbit coverage. It then reconstructs the frozen
base, profile and guarded-parent clauses, the two `-q` units, and every selector
restriction without importing the producer's cover routine.

"Independent" is layer-local here. The checker independently derives this
pair universe, stabilizer quotient, compatibility relation, and child CNFs, but
it deliberately reuses the frozen base generator and the checked early-profile
census interface. It is not an implementation-independent rederivation of the
entire Frozen Seymour ancestry.

The result is exactly 192 children and 746 compatible parent-pair memberships.
A pinned CaDiCaL 1.7.3 one-second scout reports 172 UNSAT and 20 TIMEOUT, with
zero SAT. Scout UNSAT is observational only: no proof artifact is retained and
no row is promoted to a certified claim.

## Reproduction and identities

```sh
python3 m6_b7_l6_early_c_inaccessible_pair_orbits.py \
  --manifest-output m6-b7-l6-early-c-inaccessible-pair-orbits.tsv \
  --hash-output m6-b7-l6-early-c-inaccessible-pair-hashes.tsv --populate-hashes
python3 test_m6_b7_l6_early_c_inaccessible_pair_orbits.py
python3 m6_b7_l6_early_c_inaccessible_pair_scout.py \
  --solver /path/to/pinned/cadical --seconds 1 \
  --output m6-b7-l6-early-c-inaccessible-pair-scout-1s.json
python3 check_m6_b7_l6_early_c_inaccessible_pair_orbits.py --exhaustion
```

The 8,714-byte manifest has SHA-256
`b9488ecb3cd8f734d213ef891ccd5e3695b3415319806f7e5190fa26f3f45c11`.
The complete 19,648-byte CNF hash ledger has SHA-256
`150b7a86960078f78d64cb82f499403bf8e9359ec24c936838f99dc6b299a358`.
The 47,594-byte scout has SHA-256
`1c324d6ce3b73ebdb9abdc8bafcaed1a3373541b208c7ef22002d1556bd3a480`.
Its exact 192-entry status sequence has SHA-256
`07e6e6e189544bede5004996a7bcb70db3ad4ed99bd20de5b1632e86388d2434`.
Its pinned solver is the 1,002,216-byte binary with SHA-256
`108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292`,
at path `/tmp/opencode/cadical-1.7.3/build/cadical`, version `1.7.3`.
