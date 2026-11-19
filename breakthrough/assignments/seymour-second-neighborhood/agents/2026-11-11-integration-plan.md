# Seymour history integration plan — 2026-11-11

## Recommendation

Integrate the September Seymour branch by **merging its exact commit tip**, not
by cherry-picking 146 commits and not by copying only its final files.  The safe
operation, after committing the three current same-target recovery/audit reports,
is a no-edit, no-fast-forward merge of frozen commit
`cc61b3dc4d46a0330253bac31c0d598421850864` into the current recovery branch.
The integration branch should first contain current `main` plus the three
November recovery/audit reports, but those report commits must not be rewritten.
This preserves:

- all 146 original research commits and their commit/tree identities;
- all 198 later `origin/main` commits, which are unrelated by path;
- the current recovery report and the two 2026-11-11 audit/plan reports; and
- the exact 6.151 GB Seymour assignment tree at the source tip, including its
  limitations and missing proof objects.

Do **not** call the merge a certificate recovery or a mathematical closure.  It
recovers only the bytes that are actually in the fetched source ref.  In
particular, the 18 historical `m=8` aggregate LRATs and B7-l2 leaves 488--651
remain absent.

This file is a procedure only.  Nothing in the integration was executed while
writing it.

## Frozen identities and observed state

Run all commands from `/workspace/math-god`.  The audited identities are:

```text
current branch              recovery/breakthrough-a13aca7c
current HEAD                2e0441e3aac1f9437ba3863f58e0dd5d938f1631
origin/main                 964faf4b97f9a93809dbb4bc54b400dbcf04104a
local main                  964faf4b97f9a93809dbb4bc54b400dbcf04104a
source ref                  origin/45a63659-bb8c-4524-86d8-c52dde0362b5
source tip                  cc61b3dc4d46a0330253bac31c0d598421850864
merge base                  0ee816763890ec5d75ae80f2ec626b0bd78fa570
origin/main...source         198 left / 146 right
current HEAD...source        199 left / 146 right
synthetic main+source tree  f5e670e506195b7d84fb9ce9e17b238e826f7507
source assignment tree      901a22dada2940368e1dc0fb14a3aeff4876191b
source certificate tree     2fd540f09568ac789c4a22826c1555a53ef36737
source notebook blob        f21ec257b829e3c50d900ca6b390945393dd85cd
source notebook bytes       142183
B7-l2 frozen base commit    721249ac550ad173333643d4658e23325af56187
B7-l2 frozen base tree      03f893673ca672c84c6341d48f1c922a23923d44
```

The fetched refs were refreshed at 2026-11-11 07:12:07 UTC.  Before any later
execution, fetch again and re-run the identity gates below; do not assume these
names still denote the audited objects.

At audit time the working tree had one tracked current-branch report and one
untracked report:

- tracked by `HEAD`:
  `agents/2026-11-10-recovery.md`;
- untracked, SHA-256
  `0b622e2dcbfd85b94297b5217470c3bf2342260b198f8b96d6a4bc34fd920303`:
  `agents/2026-11-11-frontier-audit.md`;
- this plan is the third same-target artifact that must be preserved before the
  merge.

No source commit contains any of those three report paths.  Nevertheless, the
two untracked files must be committed before merging: aborting or switching
with untracked audit evidence present is an avoidable preservation risk.

## What the history contains

`origin/main..origin/45a63659-bb8c-4524-86d8-c52dde0362b5` is a linear,
merge-free series of 146 nonempty commits, from
`2fbec879e5b09f227157ee81fcfd8fb06812bdde` through `cc61b3dc...`.  Every path
touched by the series lies under:

```text
breakthrough/assignments/seymour-second-neighborhood/
```

Across the final endpoint it changes 1,714 paths: 1,710 additions and four
modifications, with no deletions.  The four pre-existing files modified from the
common base are:

```text
breakthrough/assignments/seymour-second-neighborhood/notebook.md
breakthrough/assignments/seymour-second-neighborhood/experiments/README.md
breakthrough/assignments/seymour-second-neighborhood/experiments/m9-final-certificates.md
breakthrough/assignments/seymour-second-neighborhood/experiments/m9_k4_placements.py
```

Neither `origin/main` nor current `HEAD` changed any of those 1,714 source paths
since the merge base.  More strongly, the complete set of paths touched by all
146 source commits has zero overlap with the paths changed on the main/current
side.  The three frozen control files have identical blobs at the merge base,
`origin/main`, current `HEAD`, and the source tip:

```text
BREAKTHROUGH_STATE.md                                      90e4dad0404d393aa002144fad77ef6290ad917d
breakthrough/PROGRAM.md                                    07517250775a060f406e90b3663a3151dd8a79ae
breakthrough/assignments/seymour-second-neighborhood/prompt.md d2efd5acf4a430ee2300afba61e005cfb1117faf
```

A Git 2.43.0 in-core trial merge succeeded without conflict:

```sh
git merge-tree --write-tree origin/main \
  origin/45a63659-bb8c-4524-86d8-c52dde0362b5
# f5e670e506195b7d84fb9ce9e17b238e826f7507
```

The synthetic tree differed from `origin/main` on exactly the source's 1,714
endpoint paths; all 1,714 entries were byte-identical to the source tip, and all
4,310 paths changed only on the main side were byte-identical to `origin/main`.
Each of the four small source modifications also passed `git apply --check`
against current `HEAD`.

## Repository and blob risk

At audit time:

```text
Git object store / pack     6.23 GiB (one 6,698,702,755-byte pack)
whole repository on disk   about 7.3 GB
current worktree excluding .git about 1.1 GB
free /workspace space      about 97.25 GB
source assignment files    1,786 files, 6,151,429,116 logical bytes
source certificate tree    1,302 files, 6,134,610,080 logical bytes
new worktree materialization estimated about 6,150,557,729 bytes
```

The endpoint contains 1,299 `.xz` proof files totalling 6,014,412,800 bytes
and 184 files of at least 10 MiB (2,990,932,708 logical bytes).  The five files
larger than 50,000,000 bytes are:

```text
103486540  certificates/k6-exact-campaign.tar.xz
 90435048  certificates/m6-b7-l3-profile-root-cardinality-profile-07.lrat.xz
 82686636  certificates/m6-b7-l3-profile-root-cardinality-profile-08.lrat.xz
 60000000  certificates/k5-reduced-campaign.tar.xz.part-00
 60000000  certificates/k5-reduced-campaign.tar.xz.part-01
```

The first file is a 103,486,540-byte (98.69 MiB) ordinary Git blob
`bbecf648ff78f3d1e5e044e3eaadf798e6baa664`, introduced by commit
`3db52e133d6207d9610d629e12ad6663c610c6a8`.  It exceeds GitHub's documented
50 MiB warning threshold but remains 1,371,060 bytes below the documented
100 MiB (104,857,600-byte) hard block. It is still a material hosting/policy
risk because server-side limits can differ.  It is already present on the remote
source branch, so a merge should reuse the existing remote object rather than
upload it as a new object; nevertheless, **the push dry-run below is mandatory**.
If the server rejects the merge because of that object or repository policy,
do not rewrite, split, delete, or LFS-convert the historical object in place.
Stop and preserve the source ref while a separate storage/migration plan is
audited.

There is no `.gitattributes` at the source tip and these objects are not Git LFS
pointers.  No active repository hooks were found.  `git fsck --full
--connectivity-only --no-dangling` passed, and all 1,299 retained `.xz` objects
were already stream-tested in the frontier audit.  Do not run `git gc`,
`repack`, `prune`, `filter-repo`, BFG, LFS migration, or history rewriting as
part of this integration.

## Missing bytes that integration must not conceal

### `m=8` aggregate LRATs

The source retains deterministic generators and hash records for 18 aggregate
proofs:

- rho 3: 3 rows (`k=0..2`);
- rho 2: 4 rows (`k=0..3`);
- rho 1: 5 rows (`k=0..4`);
- rho 0: 6 rows (`k=0..5`).

No corresponding aggregate CNF/LRAT artifact files are in the source tree.
The only `m=8` CNF/LRAT bytes present are the much earlier pilot pair
`m8pilot.cnf.xz` and `m8pilot.lrat.xz`; those do not close the 18 rows.

### B7-l2 packages 44--51

The frozen ledger names 652 leaves, but only leaves 000--487 exist in any
fetched ref.  Exact totals are:

```text
present leaves 000--487: 488 files
  compressed: 3,735,127,652 bytes
  raw LRAT:  21,882,614,492 bytes

missing leaves 488--651: 164 files
  compressed:   674,234,424 bytes
  raw LRAT:    4,605,372,237 bytes
```

The missing set is profile 02's final leaf plus all 163 profile-03 leaves.  It
is exactly package rows 44--51:

```text
44  488-507   89,634,588 bytes
45  508-527   88,135,348 bytes
46  528-548   88,563,896 bytes
47  549-570   87,557,220 bytes
48  571-591   89,154,328 bytes
49  592-614   85,488,684 bytes
50  615-635   85,557,652 bytes
51  636-651   60,142,708 bytes
```

No fetched ref, reflog, or reachable-object path contains leaf 488 or leaf 651.
The complete ledger blob is
`8c4f35b7ae6524154bc862ba707f277e67645e68`; the package-ledger blob is
`5172afa52ee3e23ff16938fe5b80b18d6edc47db`.  The strict verifier is designed
to require all 652 artifacts, so it **must fail** after integration until the
missing bytes are recovered or replaced under a new, truthful ledger.  Do not
edit that verifier merely to make it green.

## Method decision

| Method | Decision | Reason |
|---|---|---|
| Two-parent merge of frozen tip | **Use** | Preserves all 146 source commits and provenance, reuses existing blobs, and Git's in-core merge is conflict-free while retaining all later main-side paths. |
| Cherry-pick all 146 commits | Do not use | Rewrites every commit ID, creates 146 new commits, repeats handling of multi-gigabyte additions, is harder to abort/audit, and adds no conflict advantage because path overlap is zero. |
| Squash merge | Do not use | Collapses provenance and makes package-by-package archaeology harder; a single large rewritten commit is inferior for proof custody. |
| Full assignment-tree content transplant | Fallback only | It can preserve final bytes but discards source commit ancestry and obscures when ledgers, generators, and proof packages entered. Use only if repository governance forbids merge commits, and record an exact subtree-tree comparison. |
| Merge source branch first, then reports | Do not use | Leaves current untracked audit evidence exposed during a 6.15 GB checkout and makes abort/recovery less safe. |
| Rewrite/LFS-convert large history | Prohibited here | Changes historical object identities and risks breaking proof ledgers and external references. |

## Exact integration procedure

The following procedure deliberately separates ref validation, report
preservation, history integration, byte-level verification, semantic replay,
and publication.  Stop at the first failed gate.  Commands that mutate history
or the worktree begin only in Phase 2.

### Phase 0 — prerequisites and capacity

```sh
set -euo pipefail
cd /workspace/math-god

SRC_REF=refs/remotes/origin/45a63659-bb8c-4524-86d8-c52dde0362b5
SRC=cc61b3dc4d46a0330253bac31c0d598421850864
AUDITED_MAIN=964faf4b97f9a93809dbb4bc54b400dbcf04104a
AUDITED_HEAD=2e0441e3aac1f9437ba3863f58e0dd5d938f1631
BASE=0ee816763890ec5d75ae80f2ec626b0bd78fa570
ASSIGN=breakthrough/assignments/seymour-second-neighborhood
```

Require at least 20 GiB free before materialization.  The expected checkout
increase is about 6.15 GB, and full LRAT replay may need much more temporary
space for decompressed proofs and regenerated CNFs.

```sh
avail=$(df -B1 --output=avail /workspace | tail -1 | tr -d ' ')
test "$avail" -ge 21474836480

git fsck --full --connectivity-only --no-dangling
test "$(git rev-parse --show-object-format)" = sha1
test -z "$(git config --get extensions.partialClone || true)"
test -z "$(git config --get remote.origin.promisor || true)"
```

**Gate 0:** all commands exit zero; no partial-clone/promisor configuration is
present; at least 20 GiB is free.

### Phase 1 — refresh and freeze the input refs

Fetching is intentionally explicit and forced only for the two audited remote
tracking refs.  It does not merge or check anything out.

```sh
git fetch origin \
  +refs/heads/main:refs/remotes/origin/main \
  +refs/heads/45a63659-bb8c-4524-86d8-c52dde0362b5:"$SRC_REF"

# The source must not have moved silently.  If it did, stop and re-audit.
test "$(git rev-parse "$SRC_REF^{commit}")" = "$SRC"

# Main may legitimately have advanced after this report.  Record it; do not
# reset it to AUDITED_MAIN.
MAIN_NOW=$(git rev-parse refs/remotes/origin/main^{commit})
printf 'MAIN_NOW=%s\nSRC=%s\n' "$MAIN_NOW" "$SRC"

git merge-base --is-ancestor "$AUDITED_MAIN" "$MAIN_NOW"
test "$(git merge-base "$MAIN_NOW" "$SRC")" = "$BASE"
```

Re-run the no-overlap and in-core merge gates against `MAIN_NOW`:

```sh
tmp=$(mktemp -d /workspace/seymour-integration-audit.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

git diff --name-only "$BASE" "$MAIN_NOW" | LC_ALL=C sort -u >"$tmp/main.paths"
git log --format= --name-only "$BASE..$SRC" | sed '/^$/d' | \
  LC_ALL=C sort -u >"$tmp/source.paths"
test ! -s <(comm -12 "$tmp/main.paths" "$tmp/source.paths")

MERGE_TREE=$(git merge-tree --write-tree "$MAIN_NOW" "$SRC")
printf 'trial merge tree: %s\n' "$MERGE_TREE"
git cat-file -e "$MERGE_TREE^{tree}"

git diff --check "$BASE" "$SRC"
test "$(git rev-list --count "$BASE..$SRC")" = 146
test "$(git rev-list --min-parents=2 --count "$BASE..$SRC")" = 0
```

Create local custody refs only after all identity tests pass.  These refs do not
alter commits or the worktree:

```sh
git update-ref refs/tags/recovery/seymour-source-cc61b3d "$SRC" \
  0000000000000000000000000000000000000000
git update-ref refs/tags/recovery/main-before-seymour-"${MAIN_NOW:0:12}" "$MAIN_NOW" \
  0000000000000000000000000000000000000000
```

If either tag already exists, inspect it; do not force-move it.

**Gate 1:** source ref still equals `cc61b3dc...`; current main descends from
`964faf4b...`; merge base remains `0ee8167...`; overlap is empty; `merge-tree`
returns exactly one tree ID and no conflict messages; source topology remains
146 linear non-merge commits; custody tags point to the exact commits.

### Phase 2 — preserve current same-target reports first

Do not use `git stash --include-untracked`: the reports are custody evidence,
not disposable working state.  Require the current branch and HEAD to be the
audited recovery branch.  If the branch has legitimately advanced, stop and
review those commits rather than resetting them.

```sh
test "$(git symbolic-ref --short HEAD)" = recovery/breakthrough-a13aca7c
test "$(git rev-parse HEAD)" = "$AUDITED_HEAD"

git status --porcelain=v1
```

The status must show exactly the two untracked 2026-11-11 reports (this file and
the frontier audit). Enforce that exact set:

```sh
expected=$(printf '?? %s\n?? %s\n' \
  "$ASSIGN/agents/2026-11-11-frontier-audit.md" \
  "$ASSIGN/agents/2026-11-11-integration-plan.md")
test "$(git status --porcelain=v1)" = "$expected"
```

The 2026-11-10 recovery report is already in `HEAD`.
Verify that none of the three paths exists in the source tip:

```sh
for f in \
  agents/2026-11-10-recovery.md \
  agents/2026-11-11-frontier-audit.md \
  agents/2026-11-11-integration-plan.md
do
  test -z "$(git ls-tree "$SRC" -- "$ASSIGN/$f")"
done

sha256sum "$ASSIGN/agents/2026-11-11-frontier-audit.md"
# Expected frontier audit:
# 0b622e2dcbfd85b94297b5217470c3bf2342260b198f8b96d6a4bc34fd920303
```

Commit only the two untracked reports; do not use `git add -A`:

```sh
git add -- \
  "$ASSIGN/agents/2026-11-11-frontier-audit.md" \
  "$ASSIGN/agents/2026-11-11-integration-plan.md"

git diff --cached --check
git diff --cached --name-status
# Require exactly the two A records above.

git commit -m "Audit Seymour frontier and integration recovery"
REPORTS_COMMIT=$(git rev-parse HEAD)

git diff-tree --no-commit-id --name-only -r "$REPORTS_COMMIT" | LC_ALL=C sort
# Require exactly the two 2026-11-11 report paths.

test -z "$(git status --porcelain=v1)"
git update-ref refs/tags/recovery/seymour-reports-"${REPORTS_COMMIT:0:12}" \
  "$REPORTS_COMMIT" 0000000000000000000000000000000000000000
```

**Gate 2:** reports are committed in one narrow commit; the working tree is
clean; the report custody tag exists; no research, state, announcement, or
unrelated path entered the report commit.

### Phase 3 — bring current main forward without rewriting reports

If `MAIN_NOW` still equals `AUDITED_MAIN`, it is already an ancestor and no
main integration is needed.  If main advanced, **merge** it into the recovery
line; do not rebase or cherry-pick the recovery/report commits, because that
would rewrite the very custody history being preserved.

First preserve the report-bearing head:

```sh
REPORTS_HEAD=$(git rev-parse HEAD)
git update-ref refs/tags/recovery/seymour-reports-head-"${REPORTS_HEAD:0:12}" \
  "$REPORTS_HEAD" 0000000000000000000000000000000000000000
```

Then, only if current main is not already an ancestor, perform an inspectable
main merge:

```sh
if ! git merge-base --is-ancestor "$MAIN_NOW" HEAD; then
  GIT_MERGE_AUTOEDIT=no git merge --no-ff --no-edit --no-commit "$MAIN_NOW"
  test -z "$(git ls-files -u)"
  git diff --cached --check
  git diff --cached --name-status
  git commit -m "Merge current main before Seymour recovery"
fi

git merge-base --is-ancestor "$MAIN_NOW" HEAD
test -z "$(git status --porcelain=v1)"
PREMERGE=$(git rev-parse HEAD)
git update-ref refs/tags/recovery/seymour-premerge-"${PREMERGE:0:12}" \
  "$PREMERGE" 0000000000000000000000000000000000000000
```

If the main merge conflicts or its staged path set is unexpected, run
`git merge --abort` and re-audit the new main commits.  Do not resolve the
conflict automatically.  No existing recovery/report commit is rewritten.

**Gate 3:** `MAIN_NOW` is an ancestor of current `HEAD`; all original recovery
and report commits remain ancestors; the working tree is clean; the report-head
and pre-source-merge custody refs exist.

### Phase 4 — merge the exact source commit

Use the immutable commit ID, not the branch name, and forbid an editor:

```sh
GIT_MERGE_AUTOEDIT=no git merge --no-ff --no-edit --no-commit "$SRC"
```

This materializes about 6.15 GB.  Before committing, require a clean merge index
with no unmerged entries and inspect exactly what is staged:

```sh
test -z "$(git ls-files -u)"
git diff --cached --check
git diff --cached --shortstat
# Expected source delta at the audited base: 1714 files changed,
# 385096 insertions(+), 3 deletions(-).

git diff --cached --name-only | grep -v \
  '^breakthrough/assignments/seymour-second-neighborhood/' && exit 1 || true

test -z "$(git diff --cached --diff-filter=D --name-only)"
```

If any check fails:

```sh
git merge --abort
```

Do not resolve a surprise conflict automatically.  Re-run Phase 1 against the
new refs and update this plan.

If the index passes:

```sh
git commit -m "Merge recovered Seymour proof-artifact history"
MERGE=$(git rev-parse HEAD)

test "$(git rev-list --parents -n1 "$MERGE" | awk '{print NF}')" = 3
test "$(git rev-parse "$MERGE^1")" = "$PREMERGE"
test "$(git rev-parse "$MERGE^2")" = "$SRC"
test "$(git merge-base "$MERGE^1" "$MERGE^2")" = "$BASE"
```

**Gate 4:** merge has exactly two parents, in order `PREMERGE` then
`cc61b3dc...`; there are no unmerged paths or deletions; all staged source paths
are inside the frozen assignment; source history remains reachable unchanged.

### Phase 5 — exact tree-preservation checks

The merge result must preserve both sides, not merely avoid textual conflicts.

```sh
# Every source-side path changed from BASE must have the exact source entry.
git diff --name-only "$BASE" "$SRC" | while IFS= read -r p; do
  test "$(git ls-tree "$MERGE" -- "$p")" = "$(git ls-tree "$SRC" -- "$p")" || {
    echo "source entry mismatch: $p" >&2; exit 1;
  }
done

# Every path changed only on main must retain the exact main entry.
git diff --name-only "$BASE" "$MAIN_NOW" | while IFS= read -r p; do
  test "$(git ls-tree "$MERGE" -- "$p")" = "$(git ls-tree "$MAIN_NOW" -- "$p")" || {
    echo "main entry mismatch: $p" >&2; exit 1;
  }
done

# Frozen control identities must remain unchanged.
test "$(git rev-parse "${MERGE}:BREAKTHROUGH_STATE.md")" = \
  90e4dad0404d393aa002144fad77ef6290ad917d
test "$(git rev-parse "${MERGE}:breakthrough/PROGRAM.md")" = \
  07517250775a060f406e90b3663a3151dd8a79ae
test "$(git rev-parse "${MERGE}:${ASSIGN}/prompt.md")" = \
  d2efd5acf4a430ee2300afba61e005cfb1117faf
test "$(git rev-parse "${MERGE}:${ASSIGN}/notebook.md")" = \
  f21ec257b829e3c50d900ca6b390945393dd85cd

# Current same-target reports must all remain present.
for f in \
  agents/2026-11-10-recovery.md \
  agents/2026-11-11-frontier-audit.md \
  agents/2026-11-11-integration-plan.md
do
  git cat-file -e "${MERGE}:${ASSIGN}/$f"
done

test -z "$(git status --porcelain=v1)"
git fsck --full --connectivity-only --no-dangling
```

Record a machine-readable tree inventory outside the assignment only as a
verification log if policy permits a later dedicated audit commit; do not mix
new generated files into the merge itself.  At minimum capture:

```sh
git ls-tree -r -l "$MERGE" -- "$ASSIGN" > \
  /workspace/seymour-integrated-ls-tree.txt
sha256sum /workspace/seymour-integrated-ls-tree.txt
```

**Gate 5:** all source-delta entries equal the source; all main-delta entries
equal current main; frozen control blobs and notebook blob match; all three
recovery/audit reports survive; repository connectivity passes.

### Phase 6 — artifact-presence and stream-integrity gates

First verify the integrated endpoint inventory without pretending the absent
files exist:

```sh
python3 - <<'PY'
from pathlib import Path
root = Path('breakthrough/assignments/seymour-second-neighborhood')
leaves = root / 'certificates/m6-b7-l2-parent-chunk-cover-artifacts'
present = sorted(p.name for p in leaves.glob('leaf-*.lrat.xz'))
assert len(present) == 488
assert present[0] == 'leaf-000.lrat.xz'
assert present[-1] == 'leaf-487.lrat.xz'
for i in range(488, 652):
    assert not (leaves / f'leaf-{i:03d}.lrat.xz').exists()
print('PASS retained B7-l2 objects=488 missing=164')
PY
```

Test every retained compressed stream.  This reads about 6.0 GB and can take
time, but does not decompress to disk:

```sh
find "$ASSIGN/certificates" -type f -name '*.xz' -print0 | \
  LC_ALL=C sort -z | xargs -0 -n1 xz --test --
xz --test -- "$ASSIGN/experiments/m8pilot.cnf.xz"
xz --test -- "$ASSIGN/experiments/m8pilot.lrat.xz"
```

Authenticate the two retained m9 archives before extracting:

```sh
cat "$ASSIGN"/certificates/k5-reduced-campaign.tar.xz.part-* | \
  tee /workspace/k5-reduced-campaign.tar.xz | sha256sum
# d3f845d980390cac63930b8b7228eba295dbb598f6d261148aab22cf137c0f1d

test "$(stat -c %s /workspace/k5-reduced-campaign.tar.xz)" = 120197280
xz --test -- /workspace/k5-reduced-campaign.tar.xz
tar -tJf /workspace/k5-reduced-campaign.tar.xz >/dev/null

sha256sum "$ASSIGN/certificates/k6-exact-campaign.tar.xz"
# e44f8ff81d272a9f9e4b060d37aa51cdbd560552fd3ced2a1d5f98d94bb80402
test "$(stat -c %s "$ASSIGN/certificates/k6-exact-campaign.tar.xz")" = 103486540
xz --test -- "$ASSIGN/certificates/k6-exact-campaign.tar.xz"
tar -tJf "$ASSIGN/certificates/k6-exact-campaign.tar.xz" >/dev/null
```

The integrated B7-l2 strict verifier is expected to fail because it requires
all 652 artifacts.  Do not use its failure as evidence that present leaves are
corrupt; authenticate leaves 000--487 against their ledger with the independent
stream/hash audit described in the frontier report, or run a separate
read-only partial-ledger checker that does not modify the frozen verifier.

**Gate 6:** all retained streams pass `xz --test`; archive lengths and hashes
match; exactly 488/652 B7-l2 objects are present; no report says 652/652.

### Phase 7 — checker reconstruction and replay matrix

Build `lrat-check` from source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` in a disposable directory on
`/workspace` (not `/tmp`, whose capacity may be smaller).  The expected binary
SHA-256 frozen by the ledgers is:

```text
e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8
```

Set an absolute checker path only after authenticating it:

```sh
CHECKER=/workspace/tools/drat-trim/lrat-check
sha256sum "$CHECKER"
test "$(sha256sum "$CHECKER" | awk '{print $1}')" = \
  e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8
```

Run structural and semantic regression first:

```sh
cd "/workspace/math-god/$ASSIGN/experiments"
python3 test_verifiers.py
python3 exhaustive_crosscheck.py --max-n 5
python3 test_cnf_semantics.py
python3 check_m8_rho5_cover.py
python3 check_m8_rho5_groups.py
python3 test_m9_k3_shapes.py
python3 test_m9_k4_shapes.py
python3 test_m9_k4_placements.py
python3 check_m9_k4_cover.py
```

Then replay the retained m9 archives exactly as their reports prescribe:

```sh
mkdir -p /workspace/replay/k5-reduced /workspace/replay/k6-exact

tar -xJf /workspace/k5-reduced-campaign.tar.xz \
  -C /workspace/replay/k5-reduced --strip-components=1
mkdir -p /workspace/replay/k5-reduced/work
python3 check_k5_reduced_cuts.py
python3 k5_reduced_verify.py \
  --root /workspace/replay/k5-reduced --checker "$CHECKER"
# Expected: PASS leaves=931 labelled=758181

tar -xJf ../certificates/k6-exact-campaign.tar.xz \
  -C /workspace/replay/k6-exact --strip-components=1
mkdir -p /workspace/replay/k6-exact/work
python3 k6_exact_verify.py \
  --root /workspace/replay/k6-exact --checker "$CHECKER"
# Expected: PASS leaves=1110 labelled=3171168
```

Replay retained m6 campaigns using their committed strict entrypoints.  At
minimum:

```sh
python3 verify_m6_forced_group_certificates.py --checker "$CHECKER"
python3 verify_m6_clean_sink_B6_l4_certificate.py --checker "$CHECKER"
python3 verify_m6_clean_sink_B6_l5_root_cardinality_certificate.py --checker "$CHECKER"
python3 verify_m6_clean_sink_B6_l6_root_cardinality_certificate.py --checker "$CHECKER"

python3 verify_m6_b7_l3_profile_root_cardinality_all19_closure.py \
  --checker "$CHECKER"
python3 verify_m6_b7_l4_profile_root_cardinality_closure.py \
  --replay --checker "$CHECKER"
python3 verify_m6_b7_l5_profile_root_cardinality_closure.py \
  --replay --checker "$CHECKER"
python3 verify_m6_b7_l6_early_c_profile_all60_closure.py \
  --replay --checker "$CHECKER"
```

Also run the source's lower-level m6 cover/filter/parent tests and any strict
residual certificate verifiers named in `experiments/README.md`; capture command,
exit status, stdout/stderr hashes, wall time, checker hash, and commit ID in a
new replay matrix.  Do not edit historical ledgers to record new runs.

For B7-l2, record:

```text
leaves 000--487   ARTIFACT_PRESENT; identity checked; replay status separately recorded
leaves 488--651   ARTIFACT_MISSING
closure           NOT ESTABLISHED
```

For `m=8`, record all 18 rho 0--3 aggregate rows as `ARTIFACT_MISSING` until
proof bytes are recovered/regenerated and checked.  Human-only subcases can be
recorded separately as `HUMAN_PROOF_CHECKED` after an actual proof audit.

**Gate 7:** every retained scope has a truthful status in
`HUMAN_PROOF_CHECKED`, `CERTIFICATE_REPLAYED`, `ARTIFACT_MISSING`, or `OPEN`.
No aggregate row is promoted from a hash or old log alone.

### Phase 8 — dry-run publication before any push

Do not push until all history/tree/inventory gates above pass.  First test what
the remote will accept:

```sh
git status --short --branch
git log --graph --decorate --oneline --boundary \
  "${MAIN_NOW}..HEAD" "${SRC}^..${SRC}"

git push --dry-run origin \
  HEAD:refs/heads/recovery/breakthrough-a13aca7c-integrated
```

A dry run does not upload the branch.  If it reports authentication failure,
large-file rejection, non-fast-forward policy failure, or any unexpected
objects, stop.  Do not force-push and do not rewrite proof history.

Only after an authorized review should publication occur, first to a recovery
branch and then through the normal change-request/merge process.  Updating
`main` directly is not part of this plan.

**Gate 8:** dry run names only the intended recovery ref and reports no policy
or large-blob rejection.  Publication remains a separate authorized action.

## Abort and rollback rules

- Before the merge commit: `git merge --abort` returns to the pre-merge custody
  ref.
- After the merge commit but before publication: do not reset destructively.
  Switch to or branch from
  `refs/tags/recovery/seymour-premerge-<prefix>`; retain the merge commit for
  diagnosis.
- After publication: revert through a reviewed change; never force-rewrite a
  public proof-artifact branch.
- Never delete the remote source ref or local source custody tag until a second
  clone has verified the integrated merge and all reachable objects.
- Never use `git clean -fdx` in this repository.  It could destroy regenerated
  certificates, replay logs, or untracked audit evidence.

## Fallback content transplant (only if merge commits are forbidden)

A transplant is technically safe at the endpoint because source/main path
changes are disjoint, but it is provenance-inferior.  If governance forbids a
merge commit, preserve the source ref/tag and transplant the exact source delta
with Git plumbing, not `cp`/`rsync`, then verify every entry against `$SRC`.
The conceptual operation is:

```sh
# Start from a clean branch descending from MAIN_NOW and the report commits.
git restore --source="$SRC" --staged --worktree -- \
  breakthrough/assignments/seymour-second-neighborhood/notebook.md \
  breakthrough/assignments/seymour-second-neighborhood/experiments/README.md \
  breakthrough/assignments/seymour-second-neighborhood/experiments/m9-final-certificates.md \
  breakthrough/assignments/seymour-second-neighborhood/experiments/m9_k4_placements.py

# For additions, generate the NUL-delimited list from `git diff --diff-filter=A
# --name-only -z "$BASE" "$SRC"` and restore those exact paths from `$SRC`.
# Do not pass such a list through whitespace-delimited shell expansion.
```

Then require the same 1,714 source-entry equality loop from Gate 5 and commit
one transplant commit whose message records `$SRC`, `$BASE`, and the source
subtree identity.  This fallback loses original ancestry in the integrated
line, so it is not preferred while a clean two-parent merge is available.

## Final acceptance checklist

- [ ] Source ref still resolves to `cc61b3dc4d46a0330253bac31c0d598421850864`.
- [ ] Current main descends from audited `964faf4b...`; any advance was re-audited.
- [ ] Source/main changed-path intersection is empty.
- [ ] Three current recovery/audit reports are committed and preserved.
- [ ] Merge has exact parents `PREMERGE` and `cc61b3dc...`.
- [ ] Every source-delta entry equals the source tip; every main-delta entry
      equals current main.
- [ ] Frozen state/program/prompt blobs are unchanged and state remains active.
- [ ] Source assignment inventory is 1,786 files / 6,151,429,116 bytes before
      adding the three current reports.
- [ ] All retained `.xz` streams pass integrity checks.
- [ ] k5/k6 archive hashes and sizes match and archives list successfully.
- [ ] Exactly 488 B7-l2 proof objects are present; 164 remain explicitly missing.
- [ ] All 18 rho 0--3 aggregate `m=8` LRATs remain explicitly missing.
- [ ] Replay matrix separates checked human proofs, replayed certificates,
      missing artifacts, and open mathematics.
- [ ] Push dry-run succeeds without rewriting or force.
- [ ] No solution, order-18 closure, B7-l2 closure, `m=8` durable closure,
      announcement, or publication claim is made by the integration itself.
