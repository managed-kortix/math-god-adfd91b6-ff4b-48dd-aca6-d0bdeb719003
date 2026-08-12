# Rank-six all-connected final hostile audit (2026-08-12)

## Verdict

PASS under the repository's authenticated committed-execution-evidence convention.
Commit `3ac4e68d2ef30b28925d5c30563b5e66ebfae4c0` (tree
`abb041ffb6e0dba4e47491d4f7c73d7b008f8f65`) was checked from a worktree with
no tracked modifications. Fresh normal and optimized executions of both theorem
masters succeeded, wrote no stderr, and were byte-identical by mode. Independent
hostile calls rejected every tested scope widening and owner/dependency omission.

This verdict does not strengthen committed execution attestations into fresh
replays of every underlying exact segment. It confirms that the committed theorem
owners authenticate the frozen sources and evidence, enforce the stated narrow
scopes, and compose fail-closed into the nonstrict all-connected conclusion
`s+(G)>=|V(G)|`.

No publication artifact or `STATE` file was read, modified, or promoted by this
audit.

## Fresh master executions

The commands were run from the repository root with `--emit --print-manifest`:

| master | mode | bytes | stdout SHA-256 | stderr |
|:--|:--|--:|:--|:--|
| rank-six orders 2--10 | normal | 4,218 | `e32149c665638e1d9cd08f8050cd4a7c7cae9f76c51b49f9cda3e0cfb2645834` | empty |
| rank-six orders 2--10 | `python3 -O` | 4,218 | `e32149c665638e1d9cd08f8050cd4a7c7cae9f76c51b49f9cda3e0cfb2645834` | empty |
| hexacyclic all-connected | normal | 2,015 | `de4f7ff814530bd0a69c4d6a1407cf5583bff8dee3aeab41600b3e971afd127e` | empty |
| hexacyclic all-connected | `python3 -O` | 2,015 | `de4f7ff814530bd0a69c4d6a1407cf5583bff8dee3aeab41600b3e971afd127e` | empty |

`cmp` confirmed normal/optimized byte identity separately for each master. The
rank-six output digest also equals the all-connected master's pinned single-block
owner-output digest. The all-connected output contains exactly the two mandatory
branches, the exhaustive rank-six block partition, and the nonstrict conclusion.

## Frozen source and evidence identities

Fresh SHA-256 measurements were:

| artifact | SHA-256 |
|:--|:--|
| `research/hexacyclic-all-connected-master-verifier.py` | `cd22798e32c1f51bf5a1646eb063215731c30ee14b4570c60b9fb1faf8584379` |
| `research/hexacyclic-multiblock-ledger-verifier.py` | `3052fe48c2f80115259a344523d8ef7a556bea07039e405493108ffd67a37c24` |
| `research/rank-six-order2-10-master-verifier.py` | `21aabed4eee24f36dc9ddf0460423d0fdd6d20a56e80a60ffed69c796c163bf1` |
| `research/rank-six-order2-10-child-execution-evidence.json` | `bbbb8eff45f8009dfb49e926c4952ae0b231ed6e02e708bddfb13b4aac17bb5d` |
| `research/rank-six-kernel-census-verifier.py` | `325b78066b626a00deaceb6a026377dd7f898a906c63c597f77831548585e1ee` |
| `research/rank-six-conditional-analytic-lift-verifier.py` | `97c49fa7d1c9c162f4592e0954d63271eb98416fbab59605a9e58a0ada1043df` |
| `research/rank-six-conditional-analytic-lift-manifest.json` | `b6ab90a895fcd7d6ebcf3b32b69676847c35dd7d070e9b8c6c4c13150bda94f6` |
| `research/rank-six-order2-7-master-verifier.py` | `a84d100a61433eae1944db1036693a0eec136c53343192d6c238392335cf742f` |
| `research/rank-six-order-eight-kernel-theorem-verifier.py` | `247fc797251f19ce1fde2824f24543e2eaa7d3d3dfe4411bcc6eb829aa3e9703` |
| `research/rank-six-order-nine-kernel-theorem-verifier.py` | `d11b6da30ccff5905cf851d33fc6a5d0cfc6650f3e8317224ddc0d8a2e4cd3d9` |
| `research/rank-six-order-ten-kernel-theorem-verifier.py` | `4cb22611448755d1eea984271251b542ab96f519cc052f3aeda8d56c04c61819` |
| `research/fixtures/rank-six-kernels.json` | `5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476` |

Every dependency digest equals the corresponding pin consumed by the master
chain. The multiblock canonical output pin is
`c391247907833695586eac184379a8bd34800bc76d26a851d20dcf9903f85611`.

## Hostile mutations

An external import-based harness made 18 independent mutations against the
committed validators. All 18 were rejected:

1. Omitted each of the four finite rank-six owners in turn.
2. Omitted each of the six rank-six dependencies in turn: census, analytic lift,
   and each of the four finite owners.
3. Widened each finite owner's scope to `all connected hexacyclic graphs`.
4. Omitted each all-connected branch in turn.
5. Widened the multiblock and single-block branch scopes to
   `all-positive-rank-block-configurations`.

The harness transcript had 19 lines including its final PASS marker and SHA-256
`039ecbdba2037a2e2bb8a9021b6e127f9c57c5289243a1accc832b459d00e9bf`.
These checks supplement the masters' built-in 10 rank-six and 16 all-connected
hostile self-checks, which also ran during every fresh execution above.

## Diff inspection

`git diff --check 3ac4e68^ 3ac4e68` passed. The audited commit changes exactly
four paths: two verifier modifications, the committed child-execution evidence,
and the integration referee report. Its diff is 292 insertions and 52 deletions.
No tracked post-commit source change was present before this report was written.

During final report verification, a concurrent tracked modification appeared in
`all-hexacyclic-graphs/paper.tex` (18 insertions, 30 deletions). It was not made,
read, reverted, staged, or included in this audit. The final worktree diff is
therefore not attributable solely to this report; theorem-source and evidence
paths remained unchanged.

Pre-existing untracked LaTeX auxiliaries and rank-ten search fragment directories
were present and were not read, changed, staged, or treated as theorem evidence.
The earlier integration report's lines describing a pending, moving worktree are
historical review context superseded by this post-commit audit; its receipt versus
fresh-replay caveat remains applicable.
