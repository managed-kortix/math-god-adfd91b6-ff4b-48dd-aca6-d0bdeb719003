# Missing proof-artifact Git forensics — 2026-11-11

## Verdict

**The missing historical proof bytes are not recoverable from the current local Git object database.** This is an object-database conclusion, not a claim that no other clone, staging disk, backup, deleted remote ref, or hosting-provider retention copy has them.

The frozen target remains Seymour's Second Neighborhood Conjecture and the lane remains `active`. I inspected only this assignment and repository-level Git metadata needed to locate same-target objects. I made no state change, fetch, checkout, commit, push, publication, contact, or session action.

| frozen missing set | historical bytes recoverable from this ODB? | exact result |
|---|---:|---|
| `m=8`, `rho=0..3`, 18 aggregate LRATs | **No** | All 18 LRAT SHA-256 identities, and all 18 corresponding CNF SHA-256 identities, have zero matches among every Git blob and every decompressed XZ Git blob. No commit ever added the files. Deterministic CNF generators and hash reports survive, so the CNFs can be reproduced and the proofs can be regenerated, but that is replacement/regeneration rather than recovery of Git objects. |
| B7-l2 leaves `488..651` / packages `44..51` | **No** | Exactly 164 compressed artifacts are absent: leaf 488 plus all 163 profile-03 leaves. None of their 164 compressed SHA-256 or 164 raw-LRAT SHA-256 identities matches any Git blob, decompressed XZ Git blob, or nested retained campaign-archive member. No package-44-through-51 commit or child of the visible tip is in the ODB. Frozen generators, CNF hashes, proof hashes, sizes, package hashes, and verifiers survive, so exact regeneration is possible in principle. |

The positive custody boundary is exact: source tip `cc61b3dc4d46a0330253bac31c0d598421850864` contains B7-l2 leaves `000..487`, all contiguous, and no later leaf. All 488 retained compressed objects exactly match their frozen ledger rows. It contains no one of the 18 aggregate rho 0–3 LRATs.

## Frozen inputs read

I read the required control files and both requested 2026-11-11 recovery reports:

- `BREAKTHROUGH_STATE.md` — `status: active`; exact assignment remains frozen; no announcement.
- `breakthrough/PROGRAM.md` — no target switch; proof artifacts must be exact and independently checkable.
- `breakthrough/assignments/seymour-second-neighborhood/prompt.md` — finite-order and restricted-model checks are non-wins; an UNSAT result without a sound reduction and checkable certificate is not a solution.
- `agents/2026-11-11-frontier-audit.md`.
- `agents/2026-11-11-integration-plan.md`.

For provenance context I also read the same-target `agents/2026-11-10-recovery.md`. The working control blobs equal the September source-ref blobs:

```text
BREAKTHROUGH_STATE.md                                      90e4dad0404d393aa002144fad77ef6290ad917d
breakthrough/PROGRAM.md                                    07517250775a060f406e90b3663a3151dd8a79ae
breakthrough/assignments/seymour-second-neighborhood/prompt.md d2efd5acf4a430ee2300afba61e005cfb1117faf
```

The latest research notebook is not the checked-out notebook. Its recovered identity is:

```text
source ref       refs/remotes/origin/45a63659-bb8c-4524-86d8-c52dde0362b5
source tip       cc61b3dc4d46a0330253bac31c0d598421850864
notebook blob    f21ec257b829e3c50d900ca6b390945393dd85cd
assignment tree  901a22dada2940368e1dc0fb14a3aeff4876191b
assignment size  1,786 files / 6,151,429,116 bytes
```

## Repository/object-store scope

Audit timestamp: 2026-11-11 UTC. Git is 2.43.0, SHA-1 object format. The repository is a full, non-shallow, non-partial clone:

```text
.git is both git-dir and common-dir
shallow=false
extensions.partialClone unset
remote.origin.promisor unset
GIT_ALTERNATE_OBJECT_DIRECTORIES unset
no objects/info/alternates
no linked worktree metadata
no submodule object stores
```

The local ODB consists of one valid pack plus seven loose objects:

```text
pack     .git/objects/pack/pack-1b70c762cb6edcd8ef8e2ee881e59a0756864372.pack
pack bytes 6,698,702,755
packed objects 15,394
loose objects 7
all objects 15,401
objects by type: 9,988 blobs; 1,039 commits; 4,374 trees
logical blob bytes 7,257,571,058
```

`git verify-pack` reported the pack `ok`. The seven loose objects are only the 2026-11-10 recovery commit, its trees, and its 730-byte report blob; none is a lost proof object.

All 15,401 objects are reachable from current refs:

```text
objects from git cat-file --batch-all-objects  15,401
objects from git rev-list --objects --all      15,401
difference                                          0
```

Accordingly, there is no unreachable/dangling object reservoir in this clone. These all exited zero and printed no object findings:

```sh
git fsck --full --strict
git fsck --full --unreachable --no-reflogs
git fsck --full --dangling --no-reflogs
git fsck --full --connectivity-only --no-dangling
```

`git fsck --full --unreachable --no-reflogs --lost-found` likewise found nothing; `.git/lost-found` is absent.

## Ref, remote, and reflog findings

There are 24 local refs: two local heads, 21 origin branch-tracking refs, and `origin/HEAD`. The configured fetch refspec is exhaustive for heads:

```text
+refs/heads/*:refs/remotes/origin/*
```

A read-only `git ls-remote --heads --tags origin` showed exactly the same 21 remote heads and zero tags. The Seymour source head still points to `cc61b3dc...`; there is no remote head or tag for packages 44–51. This was a ref listing only, not a fetch, so the report does not claim knowledge of deleted/unadvertised server refs.

Only one fetched ref has post-2026-07-26 notebook work for this assignment: `origin/45a63659-bb8c-4524-86d8-c52dde0362b5`. Its post-base history is 146 linear, merge-free commits. The visible source tip is literally:

```text
cc61b3dc... parent 1aad1906...  add B7 l2 proof package 43
1aad1906... parent 5b888ce9...  add B7 l2 proof package 42
...
d1ed2bcc... parent b1acaa76...  add B7 l2 proof package 00
b1acaa76... parent 721249ac...  add final B7 l2 closure verifiers
```

There is no commit object in the ODB with parent `cc61b3dc...`. There is no commit subject for `add B7 l2 proof package 44` through `51`, and no commit path delta containing leaves 488–651. The package sequence ends at 43, exactly where the artifacts end.

The clone is recent and its reflogs are correspondingly sparse. `git reflog show --all` and raw `.git/logs/**` contain only:

- clone of `main` at `964faf4b...` on 2026-11-10;
- checkout/create of `recovery/breakthrough-a13aca7c`;
- commit `2e0441e3...` for the 2026-11-10 recovery report.

No source-branch tip, package commit, missing-object ID, or deleted ref appears in any reflog. `ORIG_HEAD` is `964faf4b...`; `FETCH_HEAD` contains only the currently fetched advertised heads, including source tip `cc61b3dc...`.

## `m=8`, rho 0–3 forensics

### What history actually committed

The three historical certificate commits added only reports, deterministic generators, human-attempt text where applicable, and notebook updates:

```text
34f8a4a2f72b03d2de8a941a83d1dd47ed07f1e8  certify rho three shards
4797faace794fc90ca8e7cc531b559573a2e8683  certify rho two row
9d3bdced523c9486ea96cd801640150d7f558818  complete eight-hole row campaign
```

`git diff-tree` shows no `.cnf`, `.lrat`, `.xz`, archive, or proof-object addition in any of these commits. Across all refs/history, each rho report/generator path has only that one introducing commit; there is no later revision that added the artifacts.

The retained generator/provenance objects are:

```text
rho3_shards.py      blob 6f38e51805212d822d9dc6ccefd82c01602cfc79
rho2_shards.py      blob dc03b32b3331a5f10de1f14116b425ef21a52ae9
rho_low_shards.py   blob 155cc47fcec3129145dd3e72bd45b793d4c1f1d6
snc_cnf.py          blob 170cddb7075aa4cbd6e288949110deb762da23b8
rho3 report         blob 624799207a161e1bc60de6cbe541f1f179f41002
rho2 report         blob 40cdc800f7e501caac6039e1eb3bf8344cfb2cfd
rho-low report      blob effaabed7c30b94d3b8ff434bf942ccf99de1b2e
```

The exact target identities frozen in those reports are:

| rho | k | CNF SHA-256 | LRAT SHA-256 |
|---:|---:|---|---|
| 3 | 0 | `2a232c2478c3c609241ed2d2c47b755127d95100ac57e39acee2a4a8e7339a5f` | `4d0c419d993ab28fffb9bba622977e85bb27916838a67aae7ce96776ca2497ef` |
| 3 | 1 | `329489edf5c75fd194a171d8b60341ac587720f838cb189d4cb85cf0172c4202` | `e8109fe5adfcf81a558e973dfd6b5d7182ebf736f78fea4bd6c191c9cee14620` |
| 3 | 2 | `55e88baba98fb79dc22562fa7e0205e8d0b33600aa1c7574fdc7236875cdfe31` | `060c19a3b412550d4cebcff78280c5e3e00c92a32fac7aa79e52af2d9d2b335a` |
| 2 | 0 | `965155d8cf5b4d1f709ae32aa03ca5ff1428f9439734308b2a8a07420fba3356` | `4b5c0d8a348362a6119a0779e2a0f1829fbd305b7036ff06e4ffb713dfa03de7` |
| 2 | 1 | `7668b01c3b44af56944c54e5547d4165e697a7e994c10f9d3cbdbb65fa1e1cf4` | `ffc49229e5d412849763ecd52f82f3cd9e4fab10c2ee850ff11f2f8d0948618d` |
| 2 | 2 | `ea398e47f6080e20c6d7a92afce731186a73b0af1b84274ce24804959e250ba4` | `963c4800207a69cf725215024470ce167eb8112cb6387ce22bf5b3cc7c146e5d` |
| 2 | 3 | `6ae22517d92e7d3bd2bcec3faf6d7f18ef020cd6934ffd8dd71f218f825a665e` | `604653aaf40bf4f49aefe6a32f51bebe820c378babf869c2393aaccc51f24e20` |
| 1 | 0 | `5575e7ac8a1b581c903b0de201678e92cad89ba5c474c1d9aa63dc1834d735b1` | `9fb8804705e768adc4f19e6c76cca889db5ac2e7783e14688a2565195286439c` |
| 1 | 1 | `a4e32a35d451511b30c08a843c7ee20cbdcd5c2d3d9f097d79ab86816a4eade6` | `6bae77afbdc60ff6f050f90b78d4d9aaf18697292c86008f2c8326940c601729` |
| 1 | 2 | `df79c9d341a6099a333746ed2c0b287dfbfdaafb6b252f511915ec8e34f1793e` | `37c97b15b549985139df3bdbe3e0922c6c519668708e7f3cffbe40393c4b7330` |
| 1 | 3 | `96609557ab05c2611b8d8d2503002f685a8468444a83ab8ecf83b9d329eb9fa4` | `54fbe724b1646a861cef4e6b6be0eb00b9f6c9944dc23d43e7f9097c63501adc` |
| 1 | 4 | `931d6ba85afb32e36dc428549dfc0e40b9f6c2ac5f0af08967a8d61b630bbd98` | `62301e906f97be1f668bcefe0c2707b632643905d2e1a9d1317e995a80b1d95f` |
| 0 | 0 | `8f7810e49cf1e1b159cb2af40adbb01b6e03d5b0c060fe5c552214cb3a7989cc` | `32b8df9a1093c73c806d8ba6e7b5d8846bdfd903e88bc41bfe748b35a2465a58` |
| 0 | 1 | `917c78e08bb9206788bd0e2febe8bcd13597841671651c1a4f6b81b37af0fb5e` | `cb05379ca96a417bf4e2efecb102f9a74077aa41ec156e433e720e6900c2af68` |
| 0 | 2 | `b8edf2118dbe28e6ad5f97d667dd165a78a294016e3cd3e15d85a56673182f9c` | `e49ce46c19cb029c41d213ee1c6ffaae1b7336de6e5b5e97cb57d2701f03ff85` |
| 0 | 3 | `6672088b2a17c7ad21a21416a70e7f1e406596d848453ec3efddd51d33de2743` | `e7c036a9934b975765d21192059226b0062b86fcca679c4dc4868f6959b3d169` |
| 0 | 4 | `280c770eda43770a39d53b545eb045f0dc2a6d9a960052e7823b60db345712f1` | `a632bb2c3b5b6dc35626d0988d895ccdd194677582eff78e216eb1e6e8617347` |
| 0 | 5 | `228780d9a7de83905fded0a38603f0bf1610f9e90b05e1f4aaf16a185362bd44` | `725a692dfeeb63adeb45f515f106cee212c55f88e8f11652858318d472d66e22` |

### Exhaustive content test

I streamed every one of the 9,988 Git blobs (7,257,571,058 logical bytes), computed its SHA-256, detected every XZ payload, decompressed all 2,656 XZ blobs (52,821,949,115 decoded bytes; zero XZ errors), and computed every decoded payload's SHA-256. Results against the 36 rho target hashes:

```text
raw Git-blob matches                0 / 36
SHA-256 matches after XZ decoding   0 / 36
```

This closes common false-negative routes: a proof under another filename, a raw proof blob, a compressed proof blob, or an XZ artifact whose raw LRAT matches the ledger. Full 64-hex target strings also have no accidental Git-OID prefix disambiguation match.

The only retained `m=8` proof pair is the earlier `m8pilot.cnf.xz` / `m8pilot.lrat.xz`; neither raw nor compressed identities match any aggregate rho 0–3 target.

### Recoverability

- **Historical-object recovery from current ODB:** impossible; no matching object exists.
- **Exact CNF reconstruction:** available. The reports specify 30,981 variables and 171,942–171,944 clauses, and the committed deterministic generators emit each row. First require the regenerated CNF SHA-256 to equal the table.
- **Historical LRAT byte-for-byte regeneration:** not guaranteed. The reports give CaDiCaL 1.7.3 and `--lrat --no-binary`, but unlike the later B7 ledger they do not freeze solver binary SHA-256, all solver controls, raw byte counts, or compression identity. A regenerated LRAT that differs but checks the same frozen CNF is a valid replacement certificate, not recovery of the old bytes.

Safe read-only materialization/regeneration procedure (run in a disposable directory; do not write into this report's branch unless separately authorized):

```sh
set -euo pipefail
cd /workspace/math-god
SRC=cc61b3dc4d46a0330253bac31c0d598421850864
A=breakthrough/assignments/seymour-second-neighborhood
W=$(mktemp -d /workspace/seymour-m8-regenerate.XXXXXX)
git archive "$SRC" "$A/experiments" | tar -x -C "$W"
cd "$W/$A/experiments"

# Examples; repeat the complete 3+4+5+6 row matrix.
python3 rho3_shards.py 0 rho3-k0.cnf
sha256sum rho3-k0.cnf   # must equal 2a232c...7339a5f

python3 rho2_shards.py 3 rho2-k3.cnf
sha256sum rho2-k3.cnf   # must equal 6ae225...5a665e

python3 rho_low_shards.py 1 4 rho1-k4.cnf
sha256sum rho1-k4.cnf   # must equal 931d6b...0bbd98
python3 rho_low_shards.py 0 5 rho0-k5.cnf
sha256sum rho0-k5.cnf   # must equal 228780...62bd44

# With an authenticated CaDiCaL 1.7.3 and lrat-check:
cadical --lrat --no-binary -q rho3-k0.cnf rho3-k0.lrat
lrat-check rho3-k0.cnf rho3-k0.lrat
sha256sum rho3-k0.lrat
# Equality to 4d0c41...2497ef would recover the historical identity;
# inequality plus VERIFIED is a new replacement proof and needs a new ledger.
```

## B7-l2 leaves 488–651 / packages 44–51 forensics

### Exact present/missing boundary

At source tip `cc61b3dc...`:

```text
present leaves     000..487, exactly 488 contiguous files
present xz bytes   3,735,127,652
present raw bytes 21,882,614,492 (ledger total)
missing leaves     488..651, exactly 164 files
missing xz bytes     674,234,424
missing raw bytes  4,605,372,237
missing CNF bytes  1,768,539,203 (regenerable, not retained)
```

The missing profile split is exact: profile 02 final chunk `p02-c162` (leaf 488), then all 163 profile-03 chunks `p03-c000..p03-c162` (leaves 489–651).

The missing package rows are:

| package | leaves | count | xz bytes | artifact-set SHA-256 |
|---:|---:|---:|---:|---|
| 44 | 488–507 | 20 | 89,634,588 | `49a0478c2aecb7bdd60afa5839c17e5360dcd8fe2cfe47724d5fca933fed36a6` |
| 45 | 508–527 | 20 | 88,135,348 | `0347276e6a19866c29ad02d154777aaa18e873f2bc9e7112361a642a97a65ea9` |
| 46 | 528–548 | 21 | 88,563,896 | `10c848def8b90056c23c913078263a903f31199300bae6e799e0084d231838dc` |
| 47 | 549–570 | 22 | 87,557,220 | `9efa4286549b08eb543dd32a254611cb39bd359e077f884e18c6d05c81a19cf0` |
| 48 | 571–591 | 21 | 89,154,328 | `413a8446bd4f04308d424e634e34f21454f0b74e3c86a1bd0ce235f83777d28d` |
| 49 | 592–614 | 23 | 85,488,684 | `4cff8d000b3211fdc6889888f922e340cb16b793d8a9f9965f83ddc8bd7691b8` |
| 50 | 615–635 | 21 | 85,557,652 | `b9a24271eb0cfe28b3d68eff8d02733ecb7aab9a26c56d119edbd807ebadcb59` |
| 51 | 636–651 | 16 | 60,142,708 | `d039a83d8d3feb51e1e33047acdbec09cb2d978207e7eec818d6669c9168a392` |

The complete proof ledger and package ledger exist and are intact:

```text
certificate ledger blob  8c4f35b7ae6524154bc862ba707f277e67645e68
package ledger blob      5172afa52ee3e23ff16938fe5b80b18d6edc47db
CNF hash ledger blob     b57061a00b7899cff1a297534defcab8f2b1828a
cover manifest blob      704607a81452db164ed03362fac718e054c42e6d
frozen base commit       721249ac550ad173333643d4658e23325af56187
frozen base tree         03f893673ca672c84c6341d48f1c922a23923d44
```

All 488 present compressed artifacts match the ledger's exact byte count and SHA-256. For the 164 missing rows, only one unrelated Git blob shares even a compressed byte count (leaf 641's 484,932 bytes); its SHA-256 differs. No Git blob shares any missing raw LRAT byte count. Size is not the primary proof—the exhaustive digest scan is.

### Exhaustive content and container tests

The same full ODB scan compared all 328 missing B7 identities (164 compressed plus 164 raw) against:

1. every Git blob as stored;
2. every decoded XZ Git blob;
3. every regular member of retained `k6-exact-campaign.tar.xz`;
4. every regular member of the reconstructed three-part `k5-reduced-campaign.tar.xz`;
5. every decoded nested `.xz` member inside those archives.

Results:

```text
Git blob target matches                         0 / 328
Git XZ-decoded target matches                   0 / 328
k6 archive: 1,761 regular members               0 payload / 0 decoded matches
k5 archive: 1,784 regular members               0 payload / 0 decoded matches
```

The archive pass read 651 nested XZ members in k6 and 853 in k5, decoding 1,489,026,617 bytes total with no XZ error. Thus the missing leaves are not hidden under content-addressed member names in the two large retained campaign archives.

A direct object-wide text scan found `leaf-488.lrat.xz` and `leaf-651.lrat.xz` only in certificate-ledger blob `8c4f35b...`; no other object names those files. There is no package-44/51 commit message anywhere in the ODB.

### Why the ledger can be complete while Git is incomplete

The latest notebook and `attempts/frozen-b7-l2-parent-chunk-certificates.md` explicitly say all 652 proofs were generated, checked, identity-authenticated, and staged, and that no commit was made at that stage. Commit `b1acaa76...` then froze the complete ledger/verifiers. Separate linear commits added packages 00 through 43 only. The visible remote branch stopped after package 43. Therefore the complete ledger is evidence that the bytes existed in the campaign staging area, but not evidence that packages 44–51 ever became Git objects.

### Recoverability and exact regeneration commands

- **Historical-object recovery from current ODB:** impossible; none of the raw or compressed content identities is present.
- **Exact historical-byte regeneration:** unusually plausible, but must be proved by hashes. The ledger freezes CaDiCaL 1.7.3, solver source commit `38e073b389a877b0a0d3c91136d2443ab95fdeba`, solver binary SHA-256 `108d1042...3d3a8292`, command options including restart/phase/seed, checker identity, `xz -3`, every CNF/raw/compressed hash and byte count, and package hashes.
- **Semantic replacement:** if a proof verifies the exact frozen CNF but differs from the historical LRAT/xz hashes, it is not recovered package 44–51. Record it under a new replacement ledger; do not edit the old ledger to pretend identity.

The needed committed producer/verifier identities are present:

```text
m6_b7_l2_profile_root_cardinality.py  blob 8bcd29ae950f4cc22ec1ec2d46373a55be16f8e7
m6_b7_l2_parent_chunk_cover.py        blob a430dbb8f41c26683ad839d21b5f16c8e480a452
check_m6_b7_l2_parent_chunk_cover.py  blob 64d74fd523aff94179bfd583f91f5e62e830379d
verify_m6_b7_l2_parent_chunk_certificates.py blob 7345442e0fc3ad8392b5cc2bf3ae32fb65e9c015
verify_m6_b7_l2_parent_chunk_closure.py      blob 70ecd03f5705fbb4af90afce57b461c3fc87f1e8
```

Read-only recovery test for a candidate object already obtained elsewhere:

```sh
# For a candidate compressed leaf 488:
test "$(stat -c %s candidate-leaf-488.lrat.xz)" = 9097380
printf '%s  %s\n' \
  cea716c418dfca593141549d5e0a282e2d3a6c7f9c0916538a46239d228d2f06 \
  candidate-leaf-488.lrat.xz | sha256sum -c -
xz -dc candidate-leaf-488.lrat.xz | tee /dev/null | sha256sum
# Required raw result:
# 0eb73d1141da0e3a8c0b1722023742dd0d58fd72a930572a7c4f481aabc530fc
# Required raw byte count: 49,446,991
```

Exact deterministic regeneration pattern, in a disposable materialization of base commit `721249ac...`:

```sh
set -euo pipefail
cd /workspace/math-god
BASE=721249ac550ad173333643d4658e23325af56187
A=breakthrough/assignments/seymour-second-neighborhood
W=$(mktemp -d /workspace/seymour-b7-l2-regenerate.XXXXXX)
git archive "$BASE" "$A" | tar -x -C "$W"
cd "$W/$A/experiments"

# First prove the frozen cover and all 652 CNF identities still reconstruct.
python3 check_m6_b7_l2_parent_chunk_cover.py --cover --regenerate

# Example leaf 488; repeat 488..651.
python3 m6_b7_l2_parent_chunk_cover.py --leaf 488 --output "$W/leaf-488.cnf"
python3 check_m6_b7_l2_parent_chunk_cover.py "$W/leaf-488.cnf"
sha256sum "$W/leaf-488.cnf"
# Required: 73aec08bea37b86d396310d0db0dc292913632f824d79ce1a4e56ff5b6f7cae5
# Required bytes: 10,707,683

# Require authenticated solver/checker hashes before running. The companion scout
# additionally pins the CaDiCaL binary length to 1,002,216 bytes.
test "$(sha256sum "$CADICAL" | awk '{print $1}')" = \
  108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292
test "$(sha256sum "$LRAT_CHECK" | awk '{print $1}')" = \
  e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8

"$CADICAL" --lrat --no-binary -q --restart=false --phase=false --seed=3 \
  "$W/leaf-488.cnf" "$W/leaf-488.lrat"
"$LRAT_CHECK" "$W/leaf-488.cnf" "$W/leaf-488.lrat"
sha256sum "$W/leaf-488.lrat"
test "$(stat -c %s "$W/leaf-488.lrat")" = 49446991
# Historical raw SHA-256 required:
# 0eb73d1141da0e3a8c0b1722023742dd0d58fd72a930572a7c4f481aabc530fc

test "$(sha256sum /usr/bin/xz | awk '{print $1}')" = \
  b5b163eb273291934556377ab883b4b2a5d4da50bd0dc0a91774ecc234ccd8d0
xz -3 -c "$W/leaf-488.lrat" > "$W/leaf-488.lrat.xz"
sha256sum "$W/leaf-488.lrat.xz"
test "$(stat -c %s "$W/leaf-488.lrat.xz")" = 9097380
# Historical compressed SHA-256 required:
# cea716c418dfca593141549d5e0a282e2d3a6c7f9c0916538a46239d228d2f06
```

After regenerating all 164, validate each row against `m6-b7-l2-parent-chunk-cover-certificates.tsv`, recompute each package artifact-set hash against package rows 44–51, and run strict proof replay. The historical verifier currently requires all 652 artifacts, so a full clean materialization must combine retained leaves 000–487 with recovered/regenerated 488–651 before:

```sh
python3 verify_m6_b7_l2_parent_chunk_certificates.py \
  --checker /absolute/path/to/authenticated/lrat-check
python3 verify_m6_b7_l2_parent_chunk_closure.py \
  --checker /absolute/path/to/authenticated/lrat-check \
  --representative-replay
```

Do not weaken the verifier to accept 488/652.

## Object names/hashes mentioned in ledgers and notebook

The same-target ledgers/notebook contain these relevant 40-hex provenance IDs:

```text
PRESENT in this ODB
03f893673ca672c84c6341d48f1c922a23923d44  frozen B7 base tree
721249ac550ad173333643d4658e23325af56187  frozen B7 base commit
3e176b4675a4d4676cae9eeab8399a74ef19f265  historical same-target commit
6068e283fc21fadc73c1317db1b5625886904cad  historical same-target commit
b7cdeff6816fd29eedc9633aea7d7adb949d55a5  historical same-target commit

ABSENT from this ODB (external upstream-tool provenance, not missing proof blobs)
38e073b389a877b0a0d3c91136d2443ab95fdeba  CaDiCaL source commit
2e3b2dc0ecf938addbd779d42877b6ed69d9a985  drat-trim/lrat-check source commit
```

The two absent tool commits are references to external upstream repositories. Their absence here does not suggest dangling Seymour objects, and `git fsck` cannot recover them from this repository.

## Exact absence claim and limits

The strongest justified statement is:

> In the current `/workspace/math-god/.git` ODB, as of this audit, none of the 18 frozen aggregate rho 0–3 LRAT identities, none of their 18 CNF identities, and none of the 164 missing B7-l2 raw or compressed proof identities occurs as a Git blob, an XZ-decoded Git blob, or a nested retained campaign-archive payload. All ODB objects are reachable from refs; no dangling/unreachable commit, tree, or blob exists; no reflog names a later source tip; no commit is a child of package-43 tip `cc61b3dc...`; and advertised origin refs contain no later target ref.

What this does **not** prove:

- that the bytes never existed—the frozen ledgers/notebook say they did;
- that no other clone, old sandbox, staging directory, filesystem snapshot, backup, object quarantine, deleted server ref, or hosting-provider retention store contains them;
- that a SHA-256 preimage cannot be regenerated from the pinned generators/toolchain;
- that a different but valid LRAT cannot replace a missing historical proof.

No SHA-1 Git object IDs for the missing proofs were ever recorded. The frozen identities are SHA-256 content hashes, so `git cat-file -e <hash>` is not a valid direct lookup. The exhaustive byte/digest scan above is the relevant test.

## Recommended recovery order

1. Preserve source tip `cc61b3dc...`, base `721249ac...`, ledger blobs `8c4f35b...` / `5172afa...` / `b57061a...` / `704607a...`, and this report before any history integration. Do not run `gc`, `prune`, repack, or rewrite as a recovery step.
2. Search copies outside this current ODB first: the original campaign sandbox/stage, other clones, backups/snapshots, and any authorized deleted-ref/object-retention mechanism. A candidate is recovered only if both byte count and frozen SHA-256 match.
3. If external recovery fails, regenerate the 18 rho CNFs and B7 leaves 488–651 from the frozen sources. Keep historical recovery and replacement proof status distinct.
4. For B7, try the exact pinned binary/options/compressor path first; byte-for-byte matches can truthfully restore packages 44–51. If hashes differ but checks pass, create a new replacement ledger.
5. Replay every restored/replacement proof and only then run the full 652-leaf closure composition. Until then record `m=8 rho 0–3: ARTIFACT_MISSING` and `B7-l2: 488/652 present; closure NOT ESTABLISHED`.

This audit does not promote any finite-order closure and makes no Seymour solution claim.
