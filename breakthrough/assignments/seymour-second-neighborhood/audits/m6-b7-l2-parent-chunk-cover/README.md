# Frozen B7-l2 parent-chunk full-replay audit

## Exact scope

This audit records the post-integration verification of the exact clean Frozen
Seymour `B7-l2` parent campaign only.  The 652 ledger leaves form four ordered,
disjoint, exhaustive profile covers of exactly 8,119 parents (32,476
profile/parent incidences).  This is not a claim about another residual group,
all `m=6`, order 18, or Seymour's conjecture.

The verified repository object was:

```text
HEAD                  27d4a46f9d2d36c93aa18ae4c5cdaaab2dd5222a
tree                  22e6ce3ff7589f392bb3e6a85ffc44a266b6c910
artifact subtree      9b1de10c5e17b0b941033b1ccb40387aeae4528e
certificate ledger    8c4f35b7ae6524154bc862ba707f277e67645e68
package ledger        5172afa52ee3e23ff16938fe5b80b18d6edc47db
CNF hash ledger       b57061a00b7899cff1a297534defcab8f2b1828a
certificate verifier  7345442e0fc3ad8392b5cc2bf3ae32fb65e9c015
closure verifier      70ecd03f5705fbb4af90afce57b461c3fc87f1e8
```

The pinned checker was `/tmp/drat-trim/lrat-check`, SHA-256
`e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8`.
All runs used the reciprocal-pinned verifier and immutable ledgers above.

## Identity and replay evidence

The initial official invocation was:

```sh
python3 verify_m6_b7_l2_parent_chunk_certificates.py \
  --checker /tmp/drat-trim/lrat-check
```

It authenticated all 652 compressed artifacts and all 652 decompressed raw
LRAT identities.  It then structurally regenerated CNFs `000..419` and emitted
post-checker `PASS replay` records for `000..418` before the enclosing execution
limit interrupted the process.  Its unmodified output is retained as
`replay-000-419-interrupted.log`; the lack of a trailing newline and of a
`PASS replay` line for leaf 419 is intentional evidence of that interruption,
not a successful replay claim for 419.

The remainder was checked with the same verifier module and checker by calling
`replay(rows, checker, range(420, 652))`.  Its output is
`replay-420-651.log`.  Leaf 419 was then replayed separately, with the same
binding and artifact-set gates, in `replay-419-bridge.log`.

A strict parser required the semantic replay sequences to be exactly:

```text
replay-000-419-interrupted.log  000..418
replay-419-bridge.log           419
replay-420-651.log              420..651
```

Their ordered union is exactly `000..651`, with no duplicate or missing leaf.
The final independent composition check is retained as `closure.log`.

## Retained log identities

```text
22ed2c1832e78d83478985357779edb344d19dc23c3ad54cb9fe1e0ac01820aa  replay-000-419-interrupted.log
1af5a0656ec0660d5018dd2aad9bc3d3147378f45a5544559c0871d1e414ae3f  replay-419-bridge.log
e6a74d8483116a24f7e63670394a7184d8c372e4598c7a5bbc81ed86f5406d20  replay-420-651.log
d045296dcaddcba53b70e253a8773da9056dd6fd4413c7d66f5148831573e821  closure.log
```

Consequently, all 652 exact frozen CNFs were regenerated and structurally
checked, every ledger-bound LRAT was authenticated and accepted by the pinned
checker, and the 652 leaves independently compose to the complete clean
`B7-l2` parent campaign.  The frozen ledger's solver/compressor provenance is
not inferred from the later byte-restoration run; certificate validity rests on
exact CNF reconstruction and pinned-checker replay.
