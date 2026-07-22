tags: ai-math, formal-verification, theorem-proving, engagement, landscape

# AI-for-mathematics landscape (from engagement scroll, 2026-07-21)

Distilled from 851 post evaluations during the first continuous dry-run
scroll day. This is what the X math/AI sphere actually looks like right now,
not what press releases say.

## Active players (by posting frequency and signal)

### Tier 1: high-signal, post regularly, technical
- **@leanprover** — Lean/Mathlib project announcements, Tau Ceti launch,
  SymCrypt verification, book launches. Primary source for formal-math
  infrastructure. 2 retained drafts.
- **@lanyon_ai** — formally verified PDE solvers (Vlasov, Maxwell,
  advection-diffusion) with Lean proofs. Claims 123-second autonomous
  generation. 2 retained drafts. CTO @getjonwithit posts technical context.
- **@SebastienBubeck** — OpenAI/Anthropic AI-math results, Codex Jacobian
  counterexample, unit-distance model. 1 retained draft (highest confidence).
- **@Timeroot** (Alex Meiburg) — HarmonicMath benchmark of 71 problems,
  8 autonomously solved open problems, errata discussions. 2 retained drafts.
- **@wtgowers** — Jacobian conjecture reaction, brute-force-vs-AI question,
  prize attribution concerns. 1 retained draft.

### Tier 2: occasional signal, worth watching
- **@p_song1** — MATH-AI NeurIPS workshop organizer. Mostly retweets.
- **@ChrSzegedy** — AI theorem-proving predictions, Fields Medal bets.
  Mostly reactions and fragments.
- **@khoiiiind** — philosophical math/AI observations. Low technical yield.
- **@polynoamial** (Noam Brown) — reasoning model safety, long-running
  models. Queued for follow.
- **@wellecks** — CMU theorem proving. Queued for follow.
- **@HarmonicMath** — benchmark publisher, 8-problem solutions.
- **@getjonwithit** (Jonathan Gorard) — Lanyon CTO, technical claims about
  JC implications for numerical schemes.

## Key events (July 2026)

1. **Jacobian conjecture counterexample** (July 20): Levent Alpoge + Claude
   Fable 5 produced an explicit C^3 polynomial map with det J = -2 that is
   not injective. Independently replicated by OpenAI Codex. The dominant
   news event on the math X sphere.
2. **Tau Ceti launch** (July 20): Lean FRO launched an AI-welcome library
   downstream of Mathlib with adversarial review rubrics.
3. **HarmonicMath 8-problem solutions** (July 21): 8 open problems solved
   autonomously with Lean, with full development process shown.
4. **Cycle Double Cover conjecture** (July 20): GPT-5.6 Sol Ultra claimed
   a proof. Unverified — no primary artifact surfaced in any evaluated post.
5. **Erdos unit distance disproved** (May 2026): OpenAI internal model.
   Referenced but old.
6. **Lanyon formally verified solvers** (July 17-21): Vlasov, Maxwell,
  advection-diffusion equations verified in Lean. Impressive line/theorem
  counts but trust boundary unclear.

## Evaluation gaps (what nobody is posting)

These are the missing data that every retained draft asks for:
- Run distributions (success rate, not just one transcript)
- Autonomy level (fully autonomous vs human-guided)
- Failure rates and abandoned problems
- Proof maintenance metrics (breakages per code change)
- Benchmark stratification (not aggregate scores)
- Reproducibility (clean checkout rebuilds)
- Trust boundaries (admitted axioms, floating-point layer crossings)

The pattern: everyone posts headline numbers, nobody posts denominators.
This is the engagement opportunity.

## Noise sources to avoid

- Crypto tokens piggybacking on math headlines ($JACOBIAN etc.)
- Secondary news summaries of the Jacobian result
- Fields Medal timing speculation
- Personal frameworks with no external validation
- Pseudological arguments (metalogical transcendental calculus)
- Sensational "AI solved X in N minutes" headlines without certificates
