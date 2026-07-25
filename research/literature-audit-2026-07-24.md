# Literature audit: positive square energy (2026-07-24)

## Verified new result

Liu, Tang, and Zhang, *The positive and negative square-energy conjecture*,
arXiv:2607.18031v1, submitted 2026-07-20 14:59:44 UTC, proves that every
finite connected simple graph on `n` vertices satisfies

`min{s+(G),s-(G)} >= n-1`.

Primary sources checked:

- arXiv abstract, HTML manuscript, and metadata API;
- OpenAlex work `W7169887649`;
- Semantic Scholar record `53f61bcf68be70e5afbf9b1d4a268bb7ae570247`;
- formalization repository `ShengtongZhang-alt/Sq`;
- successful GitHub Actions run `29665815401` at commit
  `aab7dd701f042195377b1855619550e5c5aee0b0`;
- formalization and verification audits in `FORMALIZATION.md` and
  `VERIFICATION.md`.

The exact Lean theorem is
`SquareEnergy.card_sub_one_le_min_squareEnergy`.  The audit reports no
`sorry`, `admit`, project axiom, or `native_decide`; its printed axioms are
only Mathlib's standard `propext`, `Classical.choice`, and `Quot.sound`.

## Proof mechanism

The central result is the DNN inequality: for connected `G`,
`q(G)=2m-n+1`, and every doubly nonnegative matrix `M`,

`4 (sum_{uv in E} sqrt(M_uv))^2 <= q(G) 1^T M 1`.

The proof folds nonedge entries onto the diagonal, splits at cut vertices via
a Gram representation, and handles graphs with no cut vertex by averaging
the induction hypothesis over all vertex deletions and combining an averaged
estimate with a flat Cauchy--Schwarz estimate.  Applying it to
`A_+ o A_+` and `A_- o A_-` proves `s+,s- <= 2m-n+1`, hence the lower bounds.

The paper is 12 pages.  Calling it merely “two pages of actual mathematics”
is misleading: the argument is concise and elegant, but Theorem 2.1 contains
a substantive multi-case induction.

## Precise overlap with this repository

This paper settles the original EFGW `n-1` conjecture.  It does **not** settle
AKMPZ Conjecture 1.2 (arXiv:2506.07264):

`connected, m>=n+1 => s+(G)>=n`.

Therefore our exact theta theorem and one-tree theta extension remain
stronger class-specific results toward the surviving refinement.  They are
not duplicated by arXiv:2607.18031 or its companion arXiv:2607.18044.

Our disconnected edge-threshold counterexample is also compatible with the
new theorem.  Liu--Tang--Zhang prove `s± >= n-kappa(G)` for a graph with
`kappa(G)` components, not preservation of `s+>=n` under edge addition.

## Other simultaneous result

The same authors posted arXiv:2607.18044 thirteen minutes later.  It proves

`sqrt(s+(G)) <= (1-1/omega(G)) n`,

settling the positive square-energy strengthening of Turan's theorem.  This
also uses the DNN relaxation, with a Caro--Wei random partition and a local
harmonic estimate.  It does not settle AKMPZ Conjecture 1.2.

## Open targets checked

AKMPZ Section 9 explicitly proposes:

1. `s+(G)=n-1` iff connected `G` is a tree;
2. `s-(G)=n-1` iff connected `G` is a tree or complete;
3. if `s+(G)=n`, then `G` is bipartite unicyclic;
4. connected `omega(G)>=3 => s+(G)>=n`;
5. the full `m>=n+1 => s+(G)>=n` refinement.

Searches of arXiv, OpenAlex, Crossref, Semantic Scholar, and GitHub found no
later paper claiming the equality characterization as of this audit.  This
is negative search evidence, not a proof of priority.  Equality analysis in
the new DNN theorem is therefore a legitimate immediate target.

## Workflow correction

Use a funnel rather than an indiscriminate swarm:

1. **Literature gate:** arXiv API/HTML, OpenAlex, Crossref, Semantic Scholar,
   citation graph, and associated code/formalization repositories.
2. **One shared proof object:** a single `prompt.md` and notebook containing
   exact statement, victory conditions, definitions, and current lemmas.
3. **Small role-separated team:** normally one proof agent and one hostile
   auditor; add a computation agent only when a concrete certificate is
   needed.  Agents receive the same current proof object.
4. **Merge after each lemma:** no parallel branches that depend on unstated
   discoveries.  Subsequent work starts from the merged lemma.
5. **Large swarms only for separable searches:** finite case splits,
   independent construction families, or adversarial falsification.  Do not
   swarm a tightly coupled proof whose later steps need all earlier context.
