# Tick 54: checked clean-sink B6-l5 H_CC=2 shards

## Audited scope

This report is restricted to shard ordinals 02 and 05 of the frozen balanced
clean-sink manifest. They are exactly the `B6-l5` cells with `H_CC=2`:

| shard | q | parents | variables | clauses |
|---|---:|---:|---:|---:|
| `B6-l5-q0-c2-s00` | 0 | 78 | 23,694 | 154,671 |
| `B6-l5-q1-c2-s00` | 1 | 26 | 23,642 | 146,715 |

The complete partition manifest is 8,414 bytes with SHA-256
`20f6d04a9e8ca0662efd011ead7804402d3c0dd21e025311cb4485fae8403fdb`.
The partition theorem is 2,490 bytes with SHA-256
`a6aa643ae2cad46349a8a1aee88f837e112532aef2858913c9e19289e8200a87`.
The independent structural checker regenerated the cover and accepted both
canonical CNFs at their hashes recorded in the complete 57-shard hash ledger.

## Checked certificates

Pinned CaDiCaL 1.7.3 from source commit
`38e073b389a877b0a0d3c91136d2443ab95fdeba` (binary SHA-256
`108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292`)
returned exit 20 for both CNFs using textual LRAT mode. Pinned `lrat-check`
from source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` (binary SHA-256
`e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8`)
then independently returned `c VERIFIED` for each proof.

| shard | CNF SHA-256 | LRAT SHA-256 | xz bytes | xz SHA-256 |
|---|---|---|---:|---|
| `B6-l5-q0-c2-s00` | `60cdb0f2bc29c77a2d63e77ed903e2ce9fb8395fac6896b98e25aa103f21874a` | `622f9ac6b4a63e6277da7dbcfb0dc329ec1b218deb3cb13207f0b723d2f24b83` | 476,276 | `b4993470899149a8e9d706fe78e80253b3dfecfc9d9c47870cdd57ad44ffca49` |
| `B6-l5-q1-c2-s00` | `677fcbf44934cbf873edb042a544d3a39cae5b1213a24d970a375836d268f0dd` | `b871095c6085ff9c93a43b493a36268e921540ac2b642334701cf1561247d77a` | 466,772 | `1b4f74e20f549841b79d4610835425aa70424dd9c21040a7ac0a73cce780ff49` |

The two `xz -3` artifacts total 943,048 bytes, below the ledger's strict
2,000,000-byte compactness limit. The strict verifier binds the exact shard
manifest, partition theorem, complete CNF hash ledger, producer, structural
checker, tool binaries, CNFs, raw LRATs, compressed artifacts, and safe artifact
paths. It regenerates and structurally audits each CNF, decompresses and hashes
each proof, and freshly replays both proofs with the pinned checker.

## Consequence and limitation

The 104 canonical parents in these two exact shards admit no realization of the
frozen clean-sink selector CNF. Together with the rooted clean-sink theorem and
the balanced partition theorem bound by the shard manifest, this closes only
the `B6-l5`, `H_CC=2`, `q in {0,1}` portion of the restricted order-18 `m=6`
campaign. It does not certify any other balanced shard and is not a proof of the
full restricted campaign or Seymour's Second Neighborhood Conjecture.
