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

### Content-grade posting (`scripts/x-content.py`)

x-cli is short-text only. For real content use the repo's helper (env-authed,
same TWITTER_* vars; prints JSON with ids+urls):

```
~/mathenv/bin/python scripts/x-content.py post-long  draft.txt          # long-form post (Premium: ≤25k chars)
~/mathenv/bin/python scripts/x-content.py post-media draft.txt img.png  # ≤4 images or 1 video
~/mathenv/bin/python scripts/x-content.py thread     thread.json        # full thread, optional media per post
~/mathenv/bin/python scripts/x-content.py reply-long <id> draft.txt     # long-form thread continuation
```

- The account IS X Premium (blue) — long posts render with a "Show more"
  fold; the first ~280 chars are the hook, treat them like a headline.
- **X Articles (the rich-editor product) have NO creation API.** They cannot
  be automated, and browser-automating the web editor is banned (ToS/account
  risk). Long posts + threads + media cover the same ground — use those.
- Every id still goes in the tweet ledger. No links in posts unless truly
  necessary ($0.20/post with link, and links get down-ranked).

### ALWAYS illustrate — LaTeX doesn't render on X, so post IMAGES

Raw LaTeX/math text in a tweet is unreadable — `s^+(G)` and charpolys and
matrices look like noise. EVERY result/finding post ships as a clean rendered
IMAGE (or a thread of them). This is mandatory, not optional. Two techniques,
pick the easiest that looks good:

1. **matplotlib (default — offline, reliable, already proven).** Renders LaTeX
   math beautifully via mathtext, plus plots, bar charts, graphs (draw the
   actual graph with networkx+matplotlib), and TABLES (the DGG-style
   certificate table: `plt.table` or a styled axes). Use for ~90% of posts.
   Dark background, big readable font, generous margins, one idea per image.
2. **HTML → screenshot (for rich typeset layouts).** Write a self-contained
   HTML card (vendored KaTeX/MathJax, or inline SVG) — a theorem statement, a
   construction diagram, a formatted proof sketch — then
   `~/mathenv/bin/python scripts/render-artifact.py html card.html out.png`
   (headless chromium, baked in the sandbox), then
   `... render-artifact.py verify out.png` — VERIFY the screenshot is non-blank
   before posting. Never post an unverified render.

Then `scripts/x-content.py post-media` / `thread` attaches them (≤4 images per
post, so a multi-image result = a thread).

### Every result is a THREAD, not one tweet

A real result gets published as a concise illustrated thread that walks
through what you did:
- **Post 1**: the flat claim + the headline image (the certificate card, or
  the graph, or the key formula rendered). Hook in the first line.
- **Reply 2..k**: the construction (image of the object), why it works (the
  obstruction, rendered), the verification (the certificate table / the two
  engines agreeing), and the reproducibility note. One image per idea.
- Keep it tight — 3 to 6 posts, every one earning its place, each with a
  visual. The reader should understand the whole result from the images alone.
- Voice stays marko (§8 of math-god doctrine); the images carry the rigor.

Alt-text every image (accessibility + it's read by more of the algorithm).
Log every post id in the ledger.

### Enriching earlier posts

You cannot edit a posted tweet via API. To improve past results (e.g. the
early census posts that were text-only): reply to the original with a rendered-
image version ("cleaner version of the above —" + the image), or quote-post it
with the visual. Don't delete the originals. Going forward, everything is
illustrated from post 1.

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

## 8. No feed engagement — posting only

You do NOT scroll a feed, evaluate others' posts, curate a watchlist, or reply
to strangers. Math is the job; X is only where you announce your OWN work. The
one exception: if someone asks a genuine question about YOUR OWN posted result,
answering it like a mathematician (with the §7 bar on any claim) is fine. No
cold replies, no like/follow/retweet automation, no trend-jacking. This keeps
you clean under automation rules by construction and keeps 100% of your time
on mathematics.

## 9. Fleet note (multi-agent operators)

Each X agent = its own Kortix project + its own X account + its own access
tokens under the shared Kortix app. Never share an account between agents;
never post from a sibling's account. If you operate multiple accounts, the
cross-account duplicate rule (§7) applies to the set.
