# Seymour second-neighborhood frontier audit — 2026-11-11

## Audit result

The lane is still **active** and has **no solution claim**.  The newest
same-target history available in the repository is the unmerged remote ref
`origin/45a63659-bb8c-4524-86d8-c52dde0362b5`, whose visible tip is
`cc61b3dc4d46a0330253bac31c0d598421850864` (2026-09-02 21:22:08 UTC).
Its latest notebook-changing commit is
`b1acaa76600180044292b82ba703f7c8b38f8e99` (2026-09-02 21:02:44 UTC), and
its notebook blob is `f21ec257b829e3c50d900ca6b390945393dd85cd`, 142,183 bytes.  The tip
then adds only B7-l2 proof-object packages 00--43.

The latest sound mathematical scope is therefore a collection of restricted
order-18 branch eliminations, not Seymour's conjecture.  The strongest clean
frontier statement supported by the branch is:

> In the vertex-minimal-then-arc-minimal order-18 normal form, `m=9` has a
> written complete reduction plus durable reduced-campaign archives.  The
> notebook also calls `m=8` eliminated, but the 18 aggregate LRAT files behind
> rho 0--3 are absent; only hashes/generators and partial human replacements are
> retained.  Within `m=6`, the forced regimes and seven of the eight final
> clean-sink groups have durable packages.  B7-l2 has a complete 652-leaf ledger
> but only leaves 000--487 are present.  Therefore neither the notebook's full
> `m=8` closure nor its complete B7-l2 closure is presently certificate-supported
> by the fetched repository bytes.

The immediate recovery boundary is not a new search.  It is to restore and
replay the September branch exactly, recover or regenerate the missing `m=8`
aggregate proofs, and recover or regenerate B7-l2 leaves 488--651.  If those
closures replay and the top-level covers compose, the genuinely mathematical
order-18 frontier is `m in {5,7}`; until then, the sound recovered frontier also
contains the artifact-gapped portions of `m=8` and `m=6`.

## Repository facts checked directly

### Frozen control state

- `BREAKTHROUGH_STATE.md` says `status: active`, names only
  `breakthrough/assignments/seymour-second-neighborhood/prompt.md`, records no
  announcements, and directs continuation of the exact notebook frontier.
- `breakthrough/PROGRAM.md` forbids target switching and requires exact,
  independently checkable artifacts; finite/restricted-class results are not
  wins.
- `prompt.md` states the universal oriented-graph conjecture with exact-distance
  second neighborhoods.  A win is either one explicit counterexample passing
  two independent verifiers and hostile audit, or a complete universal proof
  with sound reductions and checkable terminal computation.
- The working copies of `BREAKTHROUGH_STATE.md`, `breakthrough/PROGRAM.md`, and
  `prompt.md` have the same Git blob IDs as the target remote ref.  No lane-state
  discrepancy was found in those files.
- The current working branch is not the research tip: current `HEAD` is
  `2e0441e3aac1f9437ba3863f58e0dd5d938f1631`; its merge base with the target
  ref is `0ee816763890ec5d75ae80f2ec626b0bd78fa570`, and
  `git rev-list --left-right --count HEAD...origin/45a63659-...` reports
  `199 146`.  The current checked-out notebook ends at tick 34; the remote
  notebook continues through the September certificate campaigns.
- Among fetched remote refs containing this assignment notebook, only
  `origin/45a63659-bb8c-4524-86d8-c52dde0362b5` has a notebook update later
  than 2026-07-26.  No fetched ref contains its tip.

### Artifact presence and integrity

At the target ref the assignment tree has 1,786 files and 6,151,429,116 bytes:
54 attempt reports, 418 experiment files, and 1,302 certificate-path files.
The certificate tree occupies 6,134,610,080 bytes.

I checked repository-object availability rather than trusting filenames:

- `git fsck --no-dangling` passed.
- All 1,299 `.xz` files actually present under the certificate tree were
  streamed from Git objects through `xz --test`: 6,014,412,800 bytes tested,
  zero malformed streams.
- A scan of 39 certificate-oriented ledger/report files found 1,462 unique
  *explicitly path-referenced* certificate objects.  Exactly 164 of those paths
  are absent, all and only B7-l2 `leaf-488.lrat.xz` through
  `leaf-651.lrat.xz`.  The older rho certificate reports record only LRAT
  hashes, not artifact paths, so their 18 absent proof files are a separate
  recovery gap and are not included in this 1,462-path count.
- The retained `m=9,k=5` split archive concatenates to exactly 120,197,280
  bytes with SHA-256
  `d3f845d980390cac63930b8b7228eba295dbb598f6d261148aab22cf137c0f1d`.
- The retained `m=9,k=6` archive is exactly 103,486,540 bytes with SHA-256
  `e44f8ff81d272a9f9e4b060d37aa51cdbd560552fd3ced2a1d5f98d94bb80402`.
  Both archive streams pass `xz --test` and are listable as tar archives.
- For the **present** B7-l2 objects 000--487, every compressed byte count and
  SHA-256 and every decompressed LRAT byte count and SHA-256 matches the frozen
  652-row ledger: 488 rows, 3,735,127,652 compressed bytes and 21,882,614,492
  raw LRAT bytes, zero identity mismatches.

This audit did **not** rerun `lrat-check` over all proofs or regenerate all
CNFs.  It establishes exact object presence, stream integrity, and (for the
present B7-l2 rows) ledger identity.  The branch's own strict verifiers and
notebook record prior `lrat-check` acceptance; that is separated below as a
notebook/campaign claim until clean replay is recovered.

## Checked claims

These are claims for which the exact statement/reduction and durable artifacts
are present at the target ref, with repository-object existence and compressed
integrity checked here.  “Checked” below does not enlarge the stated scope.

1. **Basic exact oracle, not a theorem of SNC.**  The repository contains the
   independent Python/set and Node/Boolean-matrix neighborhood verifiers and
   the recorded exhaustive differential census through order five: 59,809
   labelled oriented graphs, zero counterexamples.  This is regression evidence
   only.

2. **Minimal order-18 normalization.**  The recorded arc-deletion repair
   supports deficits one or two and root second-layer size six or seven for a
   vertex-minimal then arc-minimal counterexample.  Orders at most 17 are
   excluded in the notebook's exact capacity/tournament argument.  The later
   campaigns all depend on this restricted normalization; they are not direct
   searches over every oriented graph.

3. **Order-18 `m=8` proved subscopes, not recovered full closure.**  Rho 5 and
   rho 4 have retained written human contradictions.  Rho 3 has retained human
   proofs for the zero-/one-internal-hole cases and for the two-hole case when
   neither hole meets the root, but its root-incident residual was discharged
   computationally.  The rho 2, 1, and 0 rows likewise have human low-`k`
   subcases but rely on aggregate computation for the remaining cases.  The
   exact generators and CNF/LRAT hashes are retained in
   `rho3-certificates.md` (3 rows), `rho2-certificates.md` (4 rows), and
   `rho-low-certificates.md` (11 rows), but none of those 18 LRAT files is in
   the tree.  Thus the written human subscopes are checked claims; full `m=8`
   closure is a notebook/checked-run claim below, not a recovered certificate
   claim.

4. **Order-18 `m=9` branch.**  `attempts/tick48-complete-m9-closure.md` gives
   the coverage argument: a nine-edge missing graph with no isolate is `9K2`;
   otherwise root at an isolate and cover 28 `(rho,k)` cells.  Rows `k<=4` are
   backed by the written human arguments; the final `k=5` and `k=6` reduced
   campaigns have the exact durable archives and hashes checked above.  The
   supported consequence is precisely that `m=9` is impossible in the
   order-18 minimal normal form.

5. **Order-18 `m=6` setup and forced part.**  The repository freezes an exact
   68-type six-hole support census; 187,324 rooted placements; a necessary
   placement filter leaving 76,361 parents (23,578 B6 and 52,783 B7); and the
   deterministic full parent-CNF gate.  The forced regimes contain 40,415
   parents (B6 `lambda=3`, B7 `lambda=1`).  The B7 `q=0` cell has a human
   arc-minimality contradiction; nine retained grouped LRAT objects cover the
   other 31,568 forced parents.  The forced frontier is therefore closed only
   in this exact order-18 model.

6. **Rooted clean-sink theorem and exact clean residual partition.**  The human
   theorem in `attempts/tick52-rooted-clean-sink-theorem.md` is explicit: a
   degree-nine C vertex with no internal-C or C-to-B outarc has
   `N+(c)=R union A`, `N++(c)=B`, and remains bad after deleting its root arc,
   contradicting arc minimality.  Its audited application leaves 18,862 clean
   parents in eight groups:
   B6-l4 2,470; B6-l5 1,024; B6-l6 220; B7-l2 8,119; B7-l3 5,016; B7-l4
   1,649; B7-l5 322; B7-l6 42.

7. **Durable clean-group closures other than B7-l2.**  Exact ledgers, proof
   objects, and replay entrypoints are present for:
   - B6-l4, B6-l5, and B6-l6 (one complete grouped proof each; the earlier two
     H_CC=2 B6-l5 shards are subsumed by the complete B6-l5 proof);
   - B7-l3 (18 profile proofs plus a disjoint/exhaustive 60-leaf refinement of
     profile position 14, covering all 5,016 parents);
   - B7-l4 (40 profiles, all 1,649 parents);
   - B7-l5 (53 profiles, all 322 parents);
   - B7-l6 (composition of 33 original certified profile cells, eight one-high
     closures, and 19 two-high closures, exhausting 60 profile orbits over all
     42 parents).

8. **B7-l2 partial durable scope only.**  The frozen cover itself is exact:
   four profiles, 8,119 parents, 163 disjoint chunks per profile, 652 leaves,
   and 32,476 profile/parent incidences.  At the visible remote tip, however,
   only leaves 000--487 are present.  These are all of profiles 00 and 01 and
   all of profile 02 except its final chunk 162; no profile-03 object is present.
   Consequently only these 488 profile-chunk UNSAT certificates are currently
   certificate-supported by repository bytes.  Because all four profiles are
   needed to compose the parent campaign, this does not close any claimed
   complete B7-l2 parent scope.  A complete B7-l2 closure is **not** supported
   by this ref as fetched.

9. **What the retained `m=6` pieces would compose to.**  The exact placement
   filter leaves 76,361 parents.  The forced cover has 40,415 parents.  The
   residual has 35,946 distinct parents, split with no mixed parent into 17,084
   eliminated by the clean-sink theorem and 18,862 final parents in the eight
   groups listed above.  These counts sum exactly: `40,415+17,084+18,862 =
   76,361`.  The seven fully retained final groups contain 10,743 parents and
   B7-l2 contains the remaining 8,119.  Therefore restoring and replaying
   B7-l2, followed by an explicit top-level composition audit, would close the
   whole frozen `m=6` parent universe; there is no separately identified
   “non-clean m=6” search family beyond that final group decomposition.

## Notebook/campaign claims not promoted by this audit

These statements are recorded by the latest notebook and campaign ledgers, but
this audit does not treat them as presently recovered closure beyond the exact
qualifications given.

1. **The notebook says all of `m=8` is eliminated.**  It records all 18 rho
   0--3 aggregate shards as accepted by pinned `lrat-check` and combines them
   with the rho 4/5 human proofs.  The repository retains deterministic
   generators and exact CNF/LRAT hashes, but not those LRAT bytes.  The same
   notebook later applied the correct durability rule to old `m=9` hashes:
   absent proof bytes are not presently checkable certificates.  Applying that
   rule consistently, full `m=8` closure must be replayed/regenerated or
   replaced by complete human proofs before promotion.

2. **The notebook says B7-l2 is completely closed.**  It records all 652 proofs
   accepted by pinned `lrat-check`, 4,409,362,076 retained compressed bytes, 52
   packages, complete identity authentication, representative replay, and an
   exhaustive composition check.  The 652-row ledger agrees.  But the ref ends
   after package commit 43, while the package ledger requires packages 00--51.
   Missing packages 44--51 correspond exactly to leaves 488--651: 164 files,
   674,234,424 compressed bytes and 4,605,372,237 raw LRAT bytes.  No fetched
   ref contains `leaf-651`, and no unreachable local commit/object recovery was
   found.  Thus the notebook describes a completed local/staging campaign whose
   final eight packages were not preserved on the visible remote history.

3. **Prior checker acceptance.**  The notebook and strict ledgers state that
   pinned CaDiCaL 1.7.3 generated the LRATs and pinned `lrat-check` accepted
   them, often followed by fresh replay.  I checked object/ledger integrity, not
   every semantic replay in this bounded audit.  These claims become fully
   recovered operational evidence only after the exact checker binary is
   rebuilt/authenticated and the relevant strict replay entrypoints pass from a
   clean materialization.

4. **The direct `m=5` B6 run.**  The notebook records all 4,355 placement-parent
   CNFs locally UNSAT with independently checked LRATs, but also records that
   the 7,655,223,816-byte compressed object set was never made durable.  The
   hostile audit then found the proposed compact two-high witness hierarchy
   incomplete (three genuine orbits omitted and one contradictory orbit added).
   Therefore no five-hole branch closure is recovered from this work.

5. **Exploratory scouts and TIMEOUT/UNSAT statuses without retained proofs.**  A
   scout UNSAT line, a solver timeout, an old hash-only ledger, or a local proof
   later discarded is not included in checked scope.  This applies throughout
   the early m=5/m=6 campaigns and to any superseded B7-l6 refinement that was
   later replaced by an authoritative complete composition.

## Non-wins and rejected overclaims

- No explicit oriented counterexample exists in the recovered work.
- No universal proof of Seymour's conjecture exists in the recovered work.
- Eliminating orders through 18, even if completed, would still be a finite-order
  non-win under `prompt.md`.
- The exact recovered order-18 frontier is not empty: `m=5` and `m=7` are
  mathematically open; `m=8` has unrecovered computational proof dependencies;
  and `m=6` has the B7-l2 artifact gap and still needs top-level composition.
- `m=5` is not closed.  B6 has five uncovered missing-support shapes and the
  corrected broader 4,355-parent cover, but durable proof bytes are absent;
  B7 retains broad incidence freedom and was not covered by that B6 campaign.
- `m=7` is not closed.  The latest durable work is only the two-high robust-
  witness normal form and simultaneous-zone/support identities in ticks 11--12;
  no complete support cover, CNF campaign, or certificate package follows.
- `m=6` is not presently certificate-closed in the fetched ref.  Its exact
  cover does exhaust the forced plus residual parent universe, but the final
  B7-l2 profile composition lacks 164 proof objects.  A full branch statement
  also requires explicit composition from the placement filter through forced,
  clean-sink-eliminated, and all eight final groups.
- Full `m=8` closure is not presently certificate-supported: hash records and
  deterministic regeneration instructions are not retained proof bytes.
- The branch's complete B7-l2 assertion cannot be quoted as certificate-
  supported until the absent 164 proof files are recovered or regenerated and
  replayed.
- Historical claims based only on solver status, unavailable local bytes,
  incomplete hierarchy, or a restricted local projection remain non-wins.
- The assignment's literature ledger is still effectively unpopulated, and the
  prompt's full current-literature/novelty gate was never closed.  That blocks
  any priority/publication claim even if a mathematical closure were later
  obtained.

## Exact unresolved frontier

### Recovery frontier (must precede new mathematics)

1. Materialize the research tree from
   `origin/45a63659-bb8c-4524-86d8-c52dde0362b5`, not from the current stale
   working tree.  Preserve the remote commit and tree identities; do not
   silently merge its 6.1 GB assignment tree into a divergent branch and assume
   equivalence.
2. Recover or regenerate the 18 historical `m=8` aggregate proofs named by
   `rho3-certificates.md`, `rho2-certificates.md`, and
   `rho-low-certificates.md`.  At minimum, complete human proof audits must
   replace every certificate-dependent subcase; otherwise regenerate each
   frozen CNF, emit LRAT, and retain/replay the exact proof.  Do not promote
   hashes alone.
3. Recover B7-l2 package commits/objects 44--51 if they exist outside the fetched
   repository.  Required exact scope is leaves 488--651, with identities already
   frozen in `m6-b7-l2-parent-chunk-cover-certificates.tsv` and package ranges
   frozen in `m6-b7-l2-parent-chunk-cover-packages.tsv`.
4. If those B7-l2 bytes cannot be recovered, deterministically regenerate
   exactly leaves 488--651 from base commit
   `721249ac550ad173333643d4658e23325af56187`, require the frozen CNF hashes,
   pinned solver/checker provenance, exact raw/compressed hashes from the ledger,
   and strict replay.  Any differing proof is acceptable only through a new,
   explicit replacement ledger after validating the same frozen CNFs; it must
   not be passed off as the missing historical object set.
5. Run the target branch's structural tests and closure verifiers from a clean
   materialization, then run strict proof replay.  At minimum this includes the
   m9 k5/k6 verifiers; forced m6 verifier; clean B6 l4/l5/l6 verifiers; B7
   l3/l4/l5/l6 composition verifiers; and, only after restoration, the B7-l2
   certificate and closure verifiers.  Authenticate the exact pinned
   `lrat-check` binary or rebuild it from commit
   `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` and record the resulting identity.
6. Reconcile the notebook with actual durable bytes.  Until the recovery steps
   pass, the truthful statements are “m8 checked-run hashes retained, aggregate
   LRATs absent” and “B7-l2 ledger complete, 488/652 proof objects present,” not
   “m8 closed” or “B7-l2 closed.”

### Mathematical frontier after recovery

1. **`m=5`:** this is a full open branch, not merely the old 170-ledger P6
   shard.  Preserve the corrected five-support census.  For B6, either recover
   the complete direct 4,355-parent proof archive and perform hardened full
   readback, or build a corrected compact/selector-batched cover that includes
   all five two-high witness orbits from tick 49.  Independently construct the
   B7 completion cover; the B6 parent campaign does not cover it.
2. **`m=6`:** do not invent a new non-clean search family.  Restore B7-l2,
   then mechanically compose the exact 76,361-parent partition: 40,415 forced,
   17,084 clean-sink-theorem eliminations, and 18,862 final-group parents.  Only
   if that composition fails should a new m6 mathematical frontier be opened.
3. **`m=7`:** resume from ticks 11--12.  There are exactly two high vertices;
   use the simultaneous robust-witness zones and the high-high three-target
   support gadget to freeze a complete finite location/overlap cover for both
   B6/B7 root branches.  The current identities are necessary constraints only.
4. **Beyond order 18:** even complete recovery of `m=8`, completion of `m=5`
   and `m=7`, and composition of `m=6` would establish only
   the order-18 theorem.  The universal assignment would still require a sound
   reduction from every counterexample order to the checked terminal range, or
   a different universal proof/counterexample route.  No such reduction is
   recovered here.

## Sound resumption checkpoint

Resume only after recording a clean replay matrix with one row per exact closed
scope and an explicit status among `HUMAN_PROOF_CHECKED`,
`CERTIFICATE_REPLAYED`, `ARTIFACT_MISSING`, and `OPEN`.  The first rows that must
be marked `ARTIFACT_MISSING` today are the 18 rho 0--3 aggregate LRATs for `m=8`
and B7-l2 leaves 488--651.  After those are recovered and m6 is composed, the
first genuine mathematical research rows are `m=5` and `m=7`; no work should
restart at tick 34, resurvey another problem, claim order-18 closure, or alter
lane state.
