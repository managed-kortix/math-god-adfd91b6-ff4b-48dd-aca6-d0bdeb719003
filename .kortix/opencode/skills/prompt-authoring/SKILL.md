---
name: prompt-authoring
description: How to author a problem-specific prompt.md that dissects an open problem for a rigorous multiagent attack — the exact structure that solved 6 Erdős problems (ShouqiaoW/erdos) and disproved DGG, lineage of the OpenAI cycle-double-cover prompt. Load whenever you START a new problem — the FIRST artifact is always prompt.md.
---

# prompt-authoring — the proven attack-prompt structure

Every problem you attack begins with a `prompt.md` in its top-level problem
folder, written in THIS exact structure before any search starts. This is the workflow that
solved 6 open Erdős problems in 5 days with GPT-5.6 Sol (ShouqiaoW/erdos) and
found the DGG counterexample. The prompt IS the method: it defines exactly
what counts as solving, closes every escape hatch, and manages the search.

## Why it works
- It makes "solved" a precise, non-negotiable predicate — the model can't
  declare a partial result a win.
- It enumerates every WEAKER result that does NOT count — killing the failure
  mode where the model reduces the problem to an equally-hard lemma and stops.
- It hard-codes adversarial self-audit and diverse multiagent search into the
  goal itself.

## The template — fill every section for the specific problem

### 1. Exact statement + notation
Define all notation precisely (LaTeX). Restate the problem VERBATIM in the
strongest standard form. Quote the source (problem id, who posed it). Never
paraphrase away a quantifier, a strictness (`m>n`), or an edge condition.

### 2. The ask
> Resolve the following [problem] completely[, at least to the level of its
> principal explicit question].

### 3. Neutrality clause
> Assume for purposes of this task that a complete resolution exists, but do
> not assume in advance that the answer is affirmative or negative. A complete
> solution must prove exactly one of the following two statements.

### 4. The two exact resolutions
Spell out **Affirmative resolution** and **Negative resolution** as precise
mathematical statements — exactly what each must establish, with all
quantifiers. For a disproof, state that it must construct ONE fixed explicit
object and rigorously prove the failure — not a family that varies with the
parameter, not finite-stage approximations.

### 5. What is sufficient
State the minimal thing that settles it (e.g. "any unconditional bound of the
form … with η→0 suffices for affirmative; any positive-density construction
for infinitely many N suffices for negative, even along a sparse sequence").

### 6. Reformulations
Give the useful equivalent framings (prime-valuation form, complement/union
form, generating-function form) — and flag the traps in each (e.g. "each C_n
is eventually periodic, but their infinite union need NOT be treated as
periodic without proof").

### 7. "Partial progress does not count unless…" — THE KILL LIST
The most important section. Enumerate, as an explicit bulleted list, every
insufficient/partial result specific to THIS problem — every escape hatch the
model might mistake for a solution. Draw from: proving only finite/special
cases; only under coprimality/divisibility/lacunarity/summability; only for
special parameter values; proving finite-truncation versions; convergence only
along a subsequence; upper and lower quantity without proving equality; a
DIFFERENT notion (natural vs logarithmic density, etc.); numerics through a
fixed range; heuristic independence; changing the object as the parameter
grows; ignoring a strict inequality/edge case; **reducing the problem to
another unproved statement of comparable strength.** This list is what forces
completeness. Be exhaustive and problem-specific.

### 8. Allowed tools
> Standard proved theorems from [relevant areas] may be used, but they must be
> stated accurately and applied with all necessary hypotheses and uniformity.

### 9. Multiagent search management (the engine)
> Use multiagent aggressively and dynamically. You have up to N concurrent
> agents. Do not use a fixed assignment.

Then the heuristics, verbatim-in-spirit (see `breakthrough-method`):
- Begin with a genuinely DIVERSE portfolio of substantially different
  approaches (list the specific ones for this problem — the reformulations,
  invariants, reductions, constructions, computational checks).
- Keep several INCOMPATIBLE routes alive across rounds — both proof and
  counterexample routes — until one side is rigorously ruled out.
- Maintain a registry of approach FAMILIES (by idea, not wording); redirect
  agents away from over-crowded families toward underexplored ones.
- Preserve independence early — don't tell most agents the favored approach.
- **Mark a route BLOCKED when it stalls at a theorem-strength missing lemma**
  or only reduces to a statement of comparable strength; reopen only on a
  genuinely new mechanism.
- Computational agents throughout: finite cases, exact periodic densities,
  counterexamples to intermediate lemmas, certificate verification. Computation
  is evidence, never a proof, until converted to a rigorous general argument or
  an exact certificate.
- Adversarial agents throughout: list the problem-specific things EVERY
  candidate proof must be checked against (each quantifier, each edge case,
  each easy-to-confuse notion, each unjustified limit interchange, each
  independence/continuity assumption, circular use of an equivalent principle).
- Require agents to return CONCRETE artifacts (lemmas, constructions,
  estimates, code outputs, exact densities, counterexamples) — reject status
  reports, vague optimism, "routine".

### 10. Return condition
> Return only when [the exact question] has been completely resolved and the
> argument survives adversarial audit. Do not return a reduction, partial
> result, isolated missing lemma, finite computation, numerical guess, "best
> effort" summary, or explanation of why it's hard. Do not stop or give up
> until a complete and rigorous solution is found; keep launching rounds,
> repairing failed arguments, and developing new ones.
> Public search only for standard background/named theorems — never to look up
> whether this problem is open or to find its solution.

## Authoring procedure
1. Read the source statement; verify it in the literature (state accurately,
   don't look up a solution).
2. Draft `prompt.md` filling all 10 sections. The kill-list (§7) and the
   adversarial checklist (§9) are where you spend the most effort — brainstorm
   every way a partial result could masquerade as a solution FOR THIS PROBLEM.
3. Self-check: does prompt.md preserve the original statement EXACTLY? (a
   silently weakened statement invalidates everything). Re-derive the two
   resolutions from the source.
4. Commit prompt.md, then run the attack against it (math-god-operator §6),
   the swarm executing its multiagent-search section.

Reference lineage: OpenAI cycle-double-cover prompt
(cdn.openai.com/pdf/…/cdc_prompt.pdf) → ShouqiaoW/erdos per-problem prompt.md.
