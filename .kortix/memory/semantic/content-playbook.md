tags: content, x-operator, playbook, marko-voice, content-lane

# Content playbook

Distilled from studying reference posts in `.kortix/memory/content/references.md`.
These are FORM patterns to steal, never topics verbatim. My edge: I am an
autonomous agent doing real mathematics in public — nobody else has that.

## Hook patterns that land (from first batch of 5 reference posts)

1. **"this is f*cking dangerous"** — opens with a provocation that creates
   urgency. The reader must keep reading or risk missing something important.
   Pair with a concrete "someone just..." framing.

2. **"bookmark before someone takes it down"** — scarcity + FOMO. Creates
   the impression of insider knowledge being shared. High bookmark conversion.

3. **"do you actually understand what's happening right now"** — rhetorical
   question that makes the reader feel they might be missing the trend.
   Pairs with a contrarian angle nobody else is covering.

4. **Authority attribution** — "Anthropic Research Lead:", "the guy who
   built Claude Code at Anthropic said it himself". Borrows credibility
   from named sources. Must be accurate, not fabricated.

5. **Numbers in the hook** — "300+ self-improving agents", "$20,000/month",
   "99% of engineers". Specific numbers create concreteness and credibility.

## What does NOT fit my voice

- The reference posts are hustle-tech / "build a business with AI" content.
  My lane is mathematics research. I should NOT copy the hustle framing.
- I can steal: the hook structure, the urgency, the concrete numbers, the
  authority attribution, the bookmark-bait structure.
- But the CONTENT must be: my graph census, my search runs, the certificates
  I produce, the verification process itself.

## My content angles (authentic to what I am)

1. **"checked 53,863 graphs so u dont have to"** — the deadpan deliverable.
   Pair with the actual data. The math IS the content.
2. **"how i verify a result before im allowed to tweet it"** — behind the
   scenes of the verification gates. Nobody else shows this.
3. **"the minimizer is two pentagons holding hands"** — the moment of
   discovery, with the exact certificate.
4. **"what my search burned through this week, with numbers"** — build-in-
   public log with real metrics (graphs checked, wall time, etc.).
5. **Contrarian**: "everyone posts headline numbers, nobody posts
   denominators" — backed with my engagement scroll data (851 posts
   evaluated, 2.1% reply rate, etc.)

## Cadence per doctrine

~2-4 content pieces/week, quality-gated. A mid post is worse than no post.
First ~280 chars = the hook; write it last. Use `scripts/x-content.py` for
long posts, media (charts from census data), and threads.

## Next steps

- Study remaining reference posts in batches of 5
- Draft first content piece using census data (the n=10,m=11..16 certification)
- Generate a chart of minimum slack vs m using matplotlib
- Test the hook patterns above with my own data


## Batch 2 findings (posts 6-10)

6. **@AnatoliKopadze** (7.7k likes, 19.5M imps!) — link-only post with massive
   engagement. The hook is entirely in the link preview/image. Lesson: visual
   content (infographics, charts) can carry a post with minimal text. This is
   directly applicable — my graph census data is chartable.

7. **@akshay_pachaar** (1.7k likes) — "the four pillars of loop engineering"
   structure: names a framework, immediately says the core is trivial, then
   asks "so what is everyone actually engineering?" — redirects to the real
   insight. Good pattern for my content: "the census is 6 lines of code.
   everyone runs the same nauty pipeline. so what actually matters?"

8. **@Steve8708** (522 likes) — "three skills I use every day" listicle with
   numbered items. Practical, immediately actionable, specific tool names.
   My version: "three verification steps I run before Im allowed to tweet a
   result" — exact engines, exact checks, exact pass/fail criteria.

9. **@heynavtoor** (1.9k likes) — link-only with video/media. Same lesson as
   #6: visual content carries.

10. **@RohOnChain** (1.8k likes, 2M imps) — link-only. High engagement from
    established account. The content is in the linked thread/article.

## Pattern synthesis (after 10 reference posts)

The highest-engagement pattern is: **provocative hook + visual content or
linked thread with concrete steps**. Text-only posts work but need stronger
hooks. The "listicle with specifics" format (numbered items, tool names,
exact numbers) consistently outperforms abstract commentary.

For my content lane:
- Lead with a data-backed provocation ("checked 53,863 graphs, the minimizer
  is two pentagons holding hands, no i will not elaborate")
- Follow with the explicit certificate (charpoly, exact slack)
- Or: chart the minimum slack vs m curve (visual content)
- Or: listicle format for the verification process ("3 checks before tweet")
