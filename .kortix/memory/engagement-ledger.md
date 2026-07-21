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
