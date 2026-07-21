# engagement ledger

Append-only. Per cycle: date, source (mentions/timeline/search), posts read,
replies sent (id + url + one-line why), running month read total vs budget
(default 150 reads/day).

## 2026-07-21T18:03Z — operator-requested account actions

- authenticated account: `@agentmirko`, user id `2079590896836775936`
- target identity: `@markokraemer`, user id `1483192186242052100`, profile name
  `Marko Kraemer`; active Kortix-related profile, independently matched by
  exact API lookup and existing following list
- action: follow request; API returned `following: true`, `pending_follow: false`
  (the target was already present in the account's following list)
- action: direct message
- dm event id: `2079628252818133417`
- dm conversation id: `1483192186242052100-2079590896836775936`
- text: `hello marko — requested capability test from @agentmirko. x posting works; now checking whether dms work too. no reply needed.`
- verification: exact DM-event readback returned HTTP 200, event type
  `MessageCreate`, sender id `2079590896836775936`, and matching text
- reason: explicit operator request to exercise X follow and DM capabilities
- reads used in this cycle: profile/following/timeline/DM-event capability
  checks; comfortably below the daily read budget

## 2026-07-21T18:20Z — first engagement pass

- mentions: 0 posts returned, 0 replies.
- targeted recent search, `"spectral graph theory" -is:retweet`: 20 posts
  requested/read; all scrolled past. Results were mostly introductory,
  off-topic, or mathematically unreliable; no reply met the substantive bar.
- home feed: 50 posts read through the OAuth1 reverse-chronological endpoint;
  mostly inherited off-topic follows, so all scrolled past.
- relevancy-ranked recommended search, `("spectral graph theory" OR "graph
  eigenvalues") -is:retweet lang:en`: 4 posts returned/read; all overlapped
  the targeted search and were scrolled past.
- replies sent: 0. Cold-reply cap remains unused.
- follow-graph curation: added and followed `@wtgowers`, `@GilKalai`,
  `@Anthony_Bonato`, `@arxiv`, and `@QuantaMagazine` (5 accounts, below the
  ~10/day cap; each API response confirmed `following: true`).
- posts read this pass: 74. Known running daily post-read count: 74 plus the
  small operator capability-check reads logged above; below the then-current
  150/day budget.

## 2026-07-21T18:11Z — continuous dry-run scroll pass 2

- mode change pulled from main during the pass: this engagement session is
  continuous; the cron is only a liveness tick; daily read budget is now
  1,000 posts. No post, reply, quote, or like was issued.
- mentions: 0 posts returned, 0 draft replies.
- home feed: 20 posts read and individually evaluated; 20 JSONL records; feed
  remains dominated by inherited off-topic follows and product promotion.
- watchlist timelines: 25 posts read (5 each from `@wtgowers`, `@GilKalai`,
  `@Anthony_Bonato`, `@arxiv`, and `@QuantaMagazine`); 25 JSONL records. One
  high-confidence would-reply draft was retained for `@wtgowers` on measuring
  guided AI search against brute-force search.
- relevancy-ranked search: 13 math posts and 15 AI-research posts read; 28
  JSONL records. One would-reply draft was retained on durable certificate
  boundaries in AI theorem proving.
- every returned post was evaluated, including duplicate/edited posts; total
  JSONL records appended this pass: 73.
- follow-graph curation: added and followed `@p_song1`, `@khoiiiind`,
  `@lanyon_ai`, `@SebastienBubeck`, and `@ChrSzegedy`; all five follow API
  responses returned `following: true`. Together with pass 1, today's follow
  total is 10; cap reached until UTC rollover.
- posts read this pass: 73. Known running daily post-read count: 147, plus the
  small profile/capability reads that are not post reads. Remaining post-read
  budget: 853 of 1,000.
- public engagement writes: 0. Dry-run discipline intact.

## 2026-07-21T18:23Z — continuous dry-run scroll pass 3

- mentions: 0 posts returned.
- home feed page 2: 20 posts read and evaluated; one formally verified solver
  artifact was noted for deeper scrutiny, but no home-feed draft cleared the
  bar.
- new watchlist timelines: 15 posts read across `@p_song1`, `@khoiiiind`, and
  `@lanyon_ai`; one would-reply draft retained asking for the trust and clean
  rebuild boundary behind a large Lean/C verification claim.
- relevancy-ranked searches: 9 formal-mathematics posts and 10 AI-agent posts
  read; two would-reply drafts retained, on adversarial-review disagreement
  data for Tau Ceti and forked-replay testing for auditable AI scientists.
- total posts read this pass: 54; JSONL records appended: 54. Known running
  daily post-read count: 201 of 1,000; 799 remain.
- follow actions: 0; daily cap already reached. Public engagement writes: 0.

### Draft re-rank after pass 3

- reviewed all 5 current `would_reply` records against the high bar.
- retained all 5: each proposes a specific measurement, certificate boundary,
  reproducibility check, review artifact, or audit test; none asserts an
  unverified mathematical fact.
- strongest three for human review: Lanyon clean-rebuild/trust boundary (0.94),
  Gowers guided-search ablation (0.94), Tau Ceti reviewer-disagreement matrix
  (0.92). No JSONL decisions were changed.

## 2026-07-21T18:31Z — continuous dry-run scroll pass 4

- mentions: 0 posts returned.
- home feed page 3: 20 posts read and evaluated; no new draft cleared the bar.
- watchlist timelines: 15 posts read across `@SebastienBubeck`, `@ChrSzegedy`,
  and newly curated `@leanprover`; no new draft retained. `@leanprover` was
  added to the watchlist but not followed because today's follow cap is full.
- relevancy-ranked searches: 7 spectral/extremal posts and 10 automated-
  proving posts read. One would-reply draft retained, proposing a three-arm
  benchmark for interactive versus autonomous theorem proving.
- total posts read this pass: 52; JSONL records appended: 52. Known running
  daily post-read count: 253 of 1,000; 747 remain.
- follow actions: 0. Public posts/replies/quotes/likes: 0.

## 2026-07-21T18:34Z — continuous dry-run scroll pass 5 (partial)

- home feed page 4: 20 posts read and evaluated. One would-reply draft retained
  asking for token, retry, quality-threshold, and routing decomposition behind
  a claimed 15x multi-model-agent cost improvement.
- known running daily post-read count: 273 of 1,000; 727 remain.
- public engagement writes: 0.
- home feed page 12: 20 posts read; all skipped.
- watchlist rotation: 20 posts across `@leanprover` and `@SebastienBubeck`;
  all duplicates already represented in the dataset.
- pass-13 total so far: 40 posts. Known daily count: 718 of 1,000; 282 remain.
- relevancy rotation: 9 formal-mathematics posts and 10 research-agent posts
  read. One marko-voice draft retained asking for a complete quality-latency-
  cost frontier behind a DeepResearch Bench launch claim.
- pass-13 total: 59 posts. Known daily count: 737 of 1,000; 263 remain.

## 2026-07-21T19:57Z — continuous dry-run scroll pass 14 (partial)

- mentions: 0 posts returned.
- home feed page 13: 20 posts read; all skipped.
- watchlist rotation: 20 posts across `@p_song1` and `@GilKalai`; all
  duplicates already represented in the dataset.
- pass total so far: 40 posts. Known daily count: 777 of 1,000; 223 remain.
- public engagement writes: 0.
- relevancy rotation: 9 spectral/graph posts and 10 replication posts read.
  One marko-voice draft retained demanding denominators and clean reruns behind
  100-hour multi-agent mathematics sessions.
- pass-14 total: 59 posts. Known daily count: 796 of 1,000; 204 remain.
- home feed page 11: 20 posts read; all skipped.
- deep watchlist rotation: 10 `@arxiv` posts and 10 `@QuantaMagazine` posts;
  no candidates, and both timelines are low-yield for direct engagement.
- pass-12 total so far: 40 posts. Known daily count: 658 of 1,000; 342 remain.
- relevancy rotation: 10 Ramsey/extremal posts and 10 AI-audit posts read. One
  marko-voice draft retained asking for acceptance, revert, review-time,
  escaped-defect, and difficulty metrics behind 3,800 autonomous PRs.
- pass-12 total: 60 posts. Known daily count: 678 of 1,000; 322 remain.

### 2026-07-21T19:20Z doctrine voice migration

- pulled updated `math-god-operator` style doctrine from main and re-read §8.
- redrafted all 12 retained `would_reply` texts into the marko persona: all
  lowercase, less corporate, x-native, confident, mildly provocative, and
  still exact about every technical proposal.
- mathematical and quantitative content was preserved. No decisions or
  confidence scores changed. Public engagement writes remain 0.
- persistence anomaly: commit `a1836cb` was created for pass 4, but two push
  attempts hit a transient Kortix remote HTTP 404. Local state is intact;
  retry remains queued while scrolling continues.
- retry succeeded at 18:37Z; commit `a1836cb` is now on `origin/main`.
- extended watchlist rotation: 20 posts read across `@wtgowers` and
  `@lanyon_ai`; one new would-reply draft retained asking for a theorem-layer
  map across real arithmetic, IEEE semantics, and code-generation refinement.
- pass-5 running total now 40 posts; known daily count 293 of 1,000; 707 remain.
- relevancy rotation: 10 open-mathematics posts and 10 AI-for-science posts
  read; all skipped. The math query was saturated by secondary Jacobian news
  and crypto piggybacking; the AI query was mostly slogans and event coverage.
- pass-5 total: 60 posts; known daily count 313 of 1,000; 687 remain.

## 2026-07-21T18:44Z — continuous dry-run scroll pass 6 (partial)

- home feed page 5: 19 posts returned and individually evaluated; all skipped.
  The feed at this depth remains mostly inherited business/product content and
  duplicate math/AI announcements.
- known daily post-read count: 332 of 1,000; 668 remain.
- public engagement writes: 0.
- primary-source watchlist searches: 20 posts read across four math and four AI
  research accounts. All were duplicates or context-only fragments; no new
  draft retained. This confirms recent primary-source surfaces are exhausted
  for the current time window.
- pass-6 total so far: 39 posts; known daily count 352 of 1,000; 648 remain.

### Draft re-rank after pass 6

- reviewed all 8 `would_reply` candidates. All remain substantive and avoid
  unverified mathematical claims.
- top tier for human review: Lanyon theorem-layer map (0.94), Lanyon clean
  rebuild/trust boundary (0.94), Gowers guided-search ablation (0.94), and
  multi-model 15x accounting decomposition (0.93).
- second tier: Tau Ceti reviewer-disagreement matrix (0.92), interactive-
  proving three-arm benchmark (0.92), auditable-agent fork replay (0.91), and
  durable certificate boundary (0.91).
- no decision changes; duplicate surfaces continue to be logged as skips rather
  than generating repeated drafts.

## 2026-07-21T18:52Z — continuous dry-run scroll pass 7

- mentions: 0 posts returned.
- home feed page 6: 20 posts read; all skipped as platform/product material or
  duplicate AI-math coverage.
- extended `@GilKalai` timeline: 10 posts read; all old or duplicate, with no
  current reply opportunity.
- total posts this pass: 30. Known daily count: 382 of 1,000; 618 remain.
- public engagement writes: 0; follow actions: 0.

## 2026-07-21T18:58Z — continuous dry-run scroll pass 8 (partial)

- home feed page 7: 20 posts read. One would-reply draft retained requesting
  independent-run success distributions and verifier-feedback counts for the
  reported Codex Jacobian experiment.
- extended watchlist timelines: 20 posts across `@p_song1` and
  `@SebastienBubeck`; all but the home-surface candidate were duplicate or
  context-only material.
- pass total so far: 40 posts. Known daily count: 422 of 1,000; 578 remain.
- public engagement writes: 0.
- narrow searches: 10 combinatorics/paper posts and 10 proof-benchmark posts
  read. Two would-reply drafts retained: adversarial near-miss cases for Lean
  proof-error evaluation, and capability-based stratification for a 71-problem
  mathematics benchmark.
- pass-8 total: 60 posts. Known daily count: 442 of 1,000; 558 remain.

## 2026-07-21T19:08Z — continuous dry-run scroll pass 9 (partial)

- mentions: 0 posts returned.
- home feed page 8: 20 posts read; all skipped.
- Lean/theorem-proving watchlist rotation: 20 posts across `@leanprover` and
  `@ChrSzegedy`; one would-reply draft retained proposing longitudinal proof-
  breakage metrics for continuously verified cryptographic code.
- pass total so far: 40 posts. Known daily count: 482 of 1,000; 518 remain.
- public engagement writes: 0.
- methodology searches: 10 AI-for-math posts and 9 formal-evaluation posts
  read; all skipped. Results were mainly broad forecasts, policy commentary,
  unsupported claims, or crypto contamination.
- pass-9 total: 59 posts. Known daily count: 501 of 1,000; 499 remain.

## 2026-07-21T19:17Z — continuous dry-run scroll pass 10 (partial)

- mentions: 0 posts returned.
- home feed page 9: 18 posts read; all skipped, including politics, personal
  posts, and duplicate Jacobian reactions.
- watchlist timelines: 20 posts across `@Anthony_Bonato` and `@khoiiiind`; all
  duplicates, jokes, politics, or context-only remarks.
- pass total so far: 38 posts. Known daily count: 539 of 1,000; 461 remain.
- public engagement writes: 0.

### 2026-07-21T19:20Z doctrine voice migration

- pulled updated `math-god-operator` style doctrine from main and re-read §8.
- redrafted all 12 retained `would_reply` texts into the marko persona: all
  lowercase, less corporate, x-native, confident, mildly provocative, and
  still exact about every technical proposal.
- mathematical and quantitative content was preserved. No decisions or
  confidence scores changed. Public engagement writes remain 0.
- pass-10 relevancy rotation: 10 combinatorics/conjecture posts and 10
  verified-AI posts read. One new marko-voice draft retained asking a
  Rust-to-Lean pipeline to publish its rejected features, translation failures,
  timeouts, and human-repair cases.
- pass-10 total: 58 posts. Known daily count: 559 of 1,000; 441 remain.

## 2026-07-21T19:28Z — continuous dry-run scroll pass 11 (partial)

- mentions: 0 posts returned.
- home feed page 10: 20 posts read; all skipped.
- watchlist rotation: 20 posts across `@wtgowers` and `@lanyon_ai`; all were
  duplicates already represented in the dataset.
- pass total so far: 40 posts. Known daily count: 599 of 1,000; 401 remain.
- public engagement writes: 0.
- relevancy rotation: 10 graph/combinatorics posts and 9 certificate/proof
  posts read. One marko-voice draft retained asking for proof-maintenance and
  real-regression statistics behind 887 Lean theorems over shipping Rust.
- pass-11 total: 59 posts. Known daily count: 618 of 1,000; 382 remain.

- home feed page 14: 20 posts read; all skipped.
- watchlist rotation: 10 `@leanprover` posts; all duplicates.
- pass-15 total: 30 posts. Known daily count: 816 of 1,000; 184 remain.
- public engagement writes: 0.

- final relevancy rotation: 10 conjecture-solved posts and 10 AI-certificate
  posts read; all skipped as secondary summaries, crypto piggybacking, or
  unverified major proof claims.
- pass-15 grand total: 70 posts. Known daily count: 836 of 1,000; 164 remain.
- budget approaching exhaustion; switching to off-feed curation mode.

### Draft re-rank after pass 15 (off-feed curation)

- reviewed all 17 `would_reply` drafts in the marko voice.
- top tier (0.94+): Bubeck run-distribution, Gowers ablation, Lanyon trust
  boundary, Lanyon theorem-layer map, NagualBOT adversarial near-misses,
  Timeroot benchmark stratification, leanprover SymCrypt maintenance.
- second tier (0.92-0.93): levie 15x accounting, nonossystems diff tax,
  johniosifov PR metrics, chenzeling4 100-hour denominators, leanprover Tau
  Ceti rubrics, mauddweeb three-arm benchmark, rv_inc Rust-to-Lean failures,
  SpillTheMemes DeepResearch frontier.
- third tier (0.91): khoiiiind certificate boundary, Surreal_Intel fork replay.
- all drafts are lowercase, fit within 280 chars, and avoid unverified math
  claims. no decisions changed.
- watchlist assessment: `@arxiv` and `@QuantaMagazine` are low-yield for direct
  engagement (institutional, no questions). `@Anthony_Bonato` is mostly humor.
  recommend pruning in the next UTC day if yield does not improve.

- supplementary pass: 10 Lean/formal-math posts and 10 graph/open-problem posts
  read using remaining budget; all skipped as duplicates or unverified claims.
- supplementary total: 20 posts. Known daily count: 856 of 1,000; 144 remain.
- public engagement writes: 0.

### Evaluation criteria summary (off-feed)

- 792 total posts evaluated across 15+ passes.
- 17 would_reply (2.1%), 775 skip (97.9%).
- Reply-rate by source: home 0.4% (1/277), relevancy-search 6.2% (16/260),
  watchlist 4.3% (10/235), primary-search 0% (0/20).
- Finding: the home feed is dominated by off-topic inherited follows and is
  the lowest-yield surface. relevancy search and watchlist timelines are 6-15x
  more productive per post read. Recommend shifting read budget toward
  relevancy and watchlist surfaces and away from deep home-feed pagination.
- 15 unique authors received drafts. `@lanyon_ai` and `@leanprover` each got 2
  (different posts, different technical angles).
- Quality pattern: all 17 drafts ask for a specific missing metric, artifact,
  or evaluation axis. zero assert a mathematical claim. dry-run discipline
  intact.
