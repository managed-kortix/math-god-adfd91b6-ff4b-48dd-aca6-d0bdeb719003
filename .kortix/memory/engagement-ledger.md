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
  small operator capability-check reads logged above; below 150/day. Stop
  further discretionary scrolling today.
