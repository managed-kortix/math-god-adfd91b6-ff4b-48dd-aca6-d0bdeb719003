---
name: x-operator
description: Complete X (Twitter) operations skill — identity, credentials, x-cli usage, posting, threading, reading, deleting, error handling, compliance. Persona-agnostic mechanics for ANY Kortix X agent; what/when to post belongs to the calling agent's own doctrine.
---

# x-operator — how a Kortix agent runs an X account

This skill is pure mechanics. It says nothing about WHAT to post or WHEN —
that policy lives in your own agent doctrine (e.g. math-god-operator §8).
Load this alongside your doctrine whenever you touch X.

## 1. Identity & credential model

- One shared **"Kortix" X app** (consumer key/secret) is used by the whole
  agent fleet. Each agent's X account authorizes that app once (3-legged
  OAuth, done by the operator), producing a per-account **access token +
  secret** that never expires.
- Your project injects five env vars at sandbox boot:
  `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET` (the app),
  `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET` (YOUR account),
  `TWITTER_BEARER_TOKEN` (app-level, read-only endpoints).
- **You are whoever the access token says you are.** Verify at session start,
  never assume (see §3). Secrets have no read API; if they're absent or dead
  (401), report to the operator — you cannot fix credentials yourself.
- NEVER print, echo, log, or commit any credential value. Ever.

## 2. Setup (idempotent, every resurrection)

The harness bootstrap (`scripts/setup-harness.sh`) installs `x-cli`
(`uv tool install x-cli`) and writes `~/.config/x-cli/.env`:

```
X_API_KEY=$TWITTER_CONSUMER_KEY
X_API_SECRET=$TWITTER_CONSUMER_SECRET
X_BEARER_TOKEN=$TWITTER_BEARER_TOKEN
X_ACCESS_TOKEN=$TWITTER_ACCESS_TOKEN
X_ACCESS_TOKEN_SECRET=$TWITTER_ACCESS_TOKEN_SECRET
```

If x-cli misbehaves after a credential rotation, rewrite that file from the
current env (re-run the harness script) — a stale config is the usual cause.

## 3. Identity check (do this before your first post of a session)

x-cli has NO identity subcommand — verify with an OAuth1-signed
`GET https://api.twitter.com/2/users/me` (python `requests_oauthlib`
one-liner using the TWITTER_* env).

Confirm the handle matches the account your doctrine says you operate. On
401: credentials are dead/rotated — stop all X work, surface it to the
operator in your state/ledger, continue non-X work.

## 4. Posting, threading, deleting (x-cli reference)

Field-verified syntax (2026-07-21): the binary lands at `~/.local/bin/x-cli`
(ensure it's on PATH — the harness script handles this), and `--json` is a
GLOBAL flag that goes BEFORE the subcommand.

```
x-cli --json tweet post "text"           # new post → returns tweet id
x-cli --json tweet reply <id> "text"     # reply — THIS is how threads work
x-cli --json tweet quote <id> "text"     # quote-post
x-cli --json tweet delete <id>           # remove a post
x-cli --json tweet get <id>              # read one post back (NOT "show")
x-cli --json search "query"              # recent search
x-cli --json user get <handle>           # user info (NOT "lookup")
x-cli --json timeline [<handle>]         # timelines
```

- Always `--json` and parse ids programmatically; never eyeball-copy.
- Unsure of syntax? `x-cli --help` / `x-cli tweet --help` before guessing.
- **Threading protocol**: a thread is a chain of replies to your own last
  post. Keep the chain: reply to the LATEST id in the thread, not the root.
  Record every id in your ledger immediately (see §6).
- 280-char limit (URLs count ~23). If it doesn't fit, thread it — don't
  compress into unreadability.
- x-cli gaps: anything it can't do, use the raw v2 API with OAuth1 signing
  (python `requests_oauthlib` one-liner from `~/mathenv` or equivalent) for
  writes, bearer token for reads.

## 5. Error handling

| symptom | meaning | action |
|---|---|---|
| 401 | dead/rotated credentials | stop X work, flag operator, carry on elsewhere |
| 403 duplicate | identical text posted recently | rewrite the text, don't retry verbatim |
| 403 permission | app lost Read+Write | flag operator (portal fix needed) |
| 429 | rate limited | exponential backoff, retry after the reset header; NEVER hammer |
| 5xx | X hiccup | one retry after 60s, then park it and try next tick |

A failed post is never an emergency. Park it, log it, move on — your ledger
means you can retry next tick.

## 6. Ledger discipline

Every write action (post/reply/quote/delete) is recorded IMMEDIATELY in your
project's tweet ledger (`.kortix/memory/tweet-ledger.md` or your project's
equivalent): UTC timestamp, action, tweet id + url, text (or text hash for
long), parent id if reply, and what evidence/certificate backs it (if your
doctrine requires evidence). Append-only. The ledger is the source of truth
for "what have I said publicly" — consult it before posting to avoid
duplicates and to find thread parents.

## 7. Compliance (X automation rules — non-negotiable)

- The account is **labeled as automated** in X settings (operator does this
  once; if you notice it missing, flag it).
- Allowed: posting original content, threading your own posts, replying when
  someone engages YOUR content (if your doctrine permits).
- Forbidden: duplicate/near-duplicate posts (per account or across the
  fleet), unsolicited mentions/replies to strangers, mass
  like/follow/retweet automation, engagement bait, trend-jacking, anything
  that pattern-matches spam. One thoughtful post beats five mediocre ones —
  the ranking algorithm rewards engagement quality, not volume, and posting
  via API carries no penalty vs the official app.
- Politics, drama, harassment: never, regardless of doctrine.

## 8. Feed engagement protocol (scrolling, evaluating, replying)

Reads are METERED (X pay-per-use, ~$0.005/post read; posts $0.015, $0.20 if
the post contains a link). Your doctrine sets a daily read budget — default
150 posts/day unless it says otherwise. Track reads in your engagement ledger
and STOP at budget.

Sources, in priority order (field-verified x-cli syntax):
1. **Mentions**: `x-cli --json me mentions --max 20` — people engaging YOU.
   Always safe to reply per automation rules; check every cycle.
2. **Replies to your own posts** — same as above; keep threads alive.
3. **Watchlist scroll**: `x-cli --json user timeline <handle> --max 10` over
   your curated watchlist (`.kortix/memory/x-watchlist.md` — accounts worth
   reading in your domain; curate it yourself, keep it 30–100 handles, note
   why each earns its spot, prune duds).
4. **Targeted search**: `x-cli --json tweet search "<query>" --max 20` on
   your doctrine's topics/queries.

Note: x-cli has NO home-feed command, and the algorithmic "For You" feed has
no public API at all. The reverse-chron home timeline endpoint
(`GET /2/users/:id/timelines/reverse_chronological`, OAuth1) exists as a raw
API fallback once the account follows people — but the watchlist scroll is
better anyway: deterministic, budget-exact, and independent of follow state.
Following accounts on the watchlist is fine and good for the account's
legitimacy — add follows gradually (a few/day max, never bulk).

Evaluation, per post (the scroll loop): decide reply / no-reply with a HIGH
bar. Reply only when ALL true: (a) genuinely on your domain, (b) you can add
something TRUE and substantive the author would value (a fact, a
computation, a correction offered kindly, an answer), (c) it fits your voice
and doctrine, (d) caps below not exhausted. Otherwise scroll on — most posts
deserve silence. When your verification gates apply to a claim (§ your
doctrine), they apply in replies too.

Hard caps + rules (automation-rules compliance):
- ≤ 3 outbound replies/day to non-engagers ("cold" replies); mentions-replies
  are uncapped within reason. ≤ 1 cold reply per author per week.
- Never argue past one exchange; never dunk; never politics/drama; never
  reply-guy a thread that didn't ask.
- No automated likes/follows/retweets in bulk. An occasional like of
  something genuinely good is fine.
- Every read batch + every reply decision goes in the engagement ledger
  (`.kortix/memory/engagement-ledger.md`): date, source, posts read count,
  replies sent (id, url, why), running month read total.

## 9. Fleet note (multi-agent operators)

Each X agent = its own Kortix project + its own X account + its own access
tokens under the shared Kortix app. Never share an account between agents;
never post from a sibling's account. If you operate multiple accounts, the
cross-account duplicate rule (§7) applies to the set.
