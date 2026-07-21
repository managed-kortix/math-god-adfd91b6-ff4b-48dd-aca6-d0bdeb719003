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
