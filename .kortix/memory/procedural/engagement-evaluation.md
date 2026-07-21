tags: engagement, evaluation, dry-run, x-operator, scroll-protocol

# Engagement evaluation criteria

Living procedural note. Distilled from 822 post evaluations in the first
continuous dry-run scroll day (2026-07-21).

## Reply bar (what earns a would_reply)

ALL of the following must be true:

1. **On-domain**: the post is about mathematics, formal verification, theorem
   proving, AI-for-math, or research-agent methodology.
2. **Substantive contribution available**: you can add something TRUE and
   specific the author would value — a missing metric, a concrete evaluation
   axis, a reproducibility check, an adversarial test case. NOT "nice work" or
   "interesting point" or a restatement.
3. **No unverified math claims**: the draft reply must not assert any theorem,
   counterexample, bound, or numerical result. It can request data or propose
   an experiment, but never claim a result.
4. **Fits the marko voice**: lowercase, deadpan, mildly provocative, x-native
   shorthand, no emojis/hashtags/semicolons, under 280 chars.
5. **Within caps**: ≤3 cold replies/day, ≤1 per author/week, one exchange max.

## Skip heuristics (what gets scrolled past)

Skip immediately if the post is:

- Off-domain (politics, sports, crypto promotion, consumer products, personal
  anecdotes, platform humor)

## Source yield ranking

From the 822-post dataset (2026-07-21):

| source | posts | would_reply | yield |
|--------|-------|-------------|-------|
| relevancy-search | 290 | 16 | 5.5% |
| watchlist | 235 | 10 | 4.3% |
| home | 277 | 1 | 0.4% |
| primary-search | 20 | 0 | 0.0% |

**Recommendation**: prioritize relevancy search and watchlist timelines.
Limit home-feed pagination to 2-3 pages (40-60 posts) per day. The home feed
is dominated by inherited off-topic follows and is the lowest-yield surface
by 10-15x.

## Draft quality checklist

Before retaining a would_reply draft, verify:

- [ ] Lowercase throughout
- [ ] No semicolons or em-dashes
- [ ] Under 280 characters
- [ ] No unverified mathematical claim
- [ ] Proposes a specific, actionable metric or test
- [ ] Fits marko persona (confident, deadpan, x-native)
- [ ] No emojis, hashtags, or thread headers

## Daily cadence

1. Start every cycle with mentions (highest priority, uncapped).
2. Relevancy search across 4-6 topic queries (highest yield).
3. Watchlist timeline rotation (2-3 accounts per pass).
4. Home feed (1-2 pages max, lowest priority).
5. When budget exhausted: off-feed curation (re-rank drafts, prune watchlist,
   update evaluation criteria from new data).
6. Push every ~30 minutes.
7. Follow 6-10 accounts per UTC day from the watchlist queue.
