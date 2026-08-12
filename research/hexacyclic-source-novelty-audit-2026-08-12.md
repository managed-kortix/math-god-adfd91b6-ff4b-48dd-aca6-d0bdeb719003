# Hexacyclic positive square-energy source and novelty audit (2026-08-12)

## Scope and decision

This audit implements the source-and-novelty gate in
`research/procedural/PUBLICATION.md` for the repository result whose exact
scope is:

> Every finite simple connected graph `G` with
> `|E(G)| = |V(G)| + 5` satisfies `s+(G) >= |V(G)|`.

Equivalently, this is the cyclomatic-rank-six (hexacyclic) specialization of
AKMPZ Conjecture 1.2. It is not the conjecture for all connected graphs with
at least `n+1` edges, and this audit does not assess any stronger claim such as
strict inequality, equality classification, edge-addition monotonicity,
subdivision monotonicity, or nonsimple graphs.

**Audit conclusion (current through 2026-08-12):** no prior paper proving the
full connected hexacyclic statement above was located in the documented
search. The closest papers prove different statements or different graph
classes. This is negative search evidence, not proof of novelty or priority.
Publication wording should therefore say only that no prior proof was located
in this search, and should describe the result as a complete hexacyclic-class
theorem and partial progress on AKMPZ Conjecture 1.2.

No author contact, submission, resolution report, social-media post, or other
external write action was performed as part of this audit.

## Exact AKMPZ source readback

Primary source:

- S. Akbari, H. Kumar, B. Mohar, S. Pragada, and S. Zhang, *Refinement of a
  conjecture on positive square energy of graphs*, arXiv:2506.07264v1,
  submitted 8 June 2025, 19:58:29 UTC.
- Versioned abstract: <https://arxiv.org/abs/2506.07264v1>
- Versioned PDF: <https://arxiv.org/pdf/2506.07264v1>
- arXiv API readback on 2026-08-12 returned exactly one version, v1, with no
  later revision in the version history:
  <https://export.arxiv.org/api/query?id_list=2506.07264>
- PDF SHA-256 downloaded on 2026-08-12:
  `35e43a7ef70a52c79df2a40df802e7139a39d5c8e29625bbf23ceedfbbeecfbc`.

The source paper defines graphs as finite and simple in its introduction and
states Conjecture 1.2 verbatim as follows:

> Let G be a connected graph of order n and size m. If m >= n + 1, then
> s+(G) >= n.

Here `s+(G)` is the sum of the squares of the positive adjacency eigenvalues.
The source abstract and discussion say that AKMPZ prove this conjecture for
claw-free graphs and graphs of diameter two; they do not claim the class of
all graphs with `m=n+5`. The repository statement is a literal specialization:
`m=n+5` implies `m>=n+1`, while connectedness and simplicity agree with the
source conventions.

The arXiv HTML and extracted PDF text agree on the conjecture. The arXiv API
also confirms the five authors, title, submission time, category `math.CO`,
and v1-only status. OpenAlex record `W4417128720` matches the title, authors,
date, arXiv location, and DOI-form identifier
<https://doi.org/10.48550/arXiv.2506.07264>.

## Search record

Searches were run on 2026-08-12 and interpreted through that date. Exact
phrases were supplemented by terminology variants because `hexacyclic` can
mean either cyclomatic number six in graph theory or an unrelated chemical
structure.

### Exact-scope queries

- arXiv API, `"hexacyclic" AND "square energy"`: zero results.
- arXiv API, `"s^+(G)" AND hexacyclic`: zero results.
- arXiv API, exact phrase `"positive square energy"`: two records, AKMPZ and
  the 2026 positive square-energy Turan paper; neither is a hexacyclic theorem.
- arXiv API, `"square energies"` in `math.CO`: nine records were returned and
  their titles and abstracts were reviewed. None claims the full connected
  `m=n+5` class.
- OpenAlex full-text search, `"hexacyclic" "positive square energy"`: zero
  results.
- OpenAlex full-text search, `"cyclomatic rank six" graph energy`: zero
  results.
- Google Scholar, `"hexacyclic" "positive square energy"`: no matching
  articles.
- Google Scholar, `"positive square energy" hexacyclic graph`: no matching
  articles.
- Google Scholar, `"cyclomatic rank six" "square energy"`: no matching
  articles.
- Google Scholar, `"m=n+5" "square energy" graph`: two irrelevant records
  caused by text fragmentation; neither concerns spectral graph theory.
- Crossref title/topic searches for `hexacyclic positive square energy` and
  the AKMPZ title found no exact-scope publication. The conspicuous
  `hexacyclic` hits concerned Sombor energy or Laplacian indices of chemical
  hexacyclic systems, not positive adjacency square energy.

### Source-paper citation and author-neighborhood queries

- Google Scholar's AKMPZ record showed four citing records: Ning--Zeng on odd
  unicyclic graphs, Liu--Tang on positive p-energy/path minimality,
  Liu--Tang--Zhang on the EFGW square-energy conjecture, and
  Liu--Tang--Zhang on a Turan strengthening. All four plausible hits were read
  at abstract/manuscript level and are separated below.
- OpenAlex title search found the AKMPZ source and five nearby citing/textual
  matches, but its citation linkage was incomplete (`cited_by_count` zero and
  no works under the `cites:W4417128720` filter). It was used for discovery,
  not as proof that the citation graph is empty.
- arXiv author search for Saieed Akbari returned 49 records through the audit
  date. The recent square-energy-related records were AKMPZ, *A Linear Lower
  Bound for the Square Energy of Graphs*, and *Vertex Partitioning and
  p-Energy of Graphs*; none states the all-connected hexacyclic theorem.
- Crossref confirmed the journal publication of Akbari--Kumar--Mohar--Pragada,
  *A Linear Lower Bound for the Square Energy of Graphs*, Electron. J. Combin.
  32 (2025), P3.53, DOI <https://doi.org/10.37236/13467>.

### Coverage limitations

- MathSciNet's public endpoint redirected to institutional/individual login,
  so no authenticated MathSciNet result list was available in this session.
- The zbMATH Open API endpoint was reachable, but the broad search response
  was not a dependable narrow bibliographic result set for this phrase and is
  not counted as an affirmative database check.
- Semantic Scholar returned HTTP 429 for the direct AKMPZ lookup.
- Google Scholar and general indexes can omit, merge, or delay records;
  OpenAlex demonstrably had incomplete citation linkage for this recent
  preprint.
- Theses, manuscripts not indexed on the searched services, non-English work,
  and results described under substantially different terminology may have
  been missed.

These limitations are why the conclusion is phrased as "no prior proof was
located," never "first," "novel," or "previously unknown."

## Plausible nearby literature and non-overlap

### AKMPZ itself (2025)

Akbari--Kumar--Mohar--Pragada--Zhang, arXiv:2506.07264v1, is the conjecture
source. It proves Conjecture 1.2 for claw-free graphs and diameter-two graphs,
plus related domination-number results. Neither class contains every
connected hexacyclic graph, and the manuscript does not state a theorem for
all graphs of fixed cyclomatic rank six.

### General EFGW theorem and DNN method (2026)

Y. Liu, Q. Tang, and S. Zhang, *The positive and negative square-energy
conjecture*, arXiv:2607.18031v1, proves for every connected `n`-vertex graph

`min{s+(G),s-(G)} >= n-1`.

Its consequence for a connected hexacyclic graph is only `s+(G)>=n-1`, not
the AKMPZ threshold `s+(G)>=n`. The paper introduces the important nearby
method of relaxing Hadamard squares to the doubly nonnegative cone and proves
a universal DNN matrix inequality. It cites AKMPZ as a refinement and does not
claim to settle AKMPZ Conjecture 1.2 or its `m=n+5` specialization.

This is genuine methodological overlap: the repository proof also uses DNN
witnesses/optimization. The repository's additional fixed-rank contribution
is its block split, suppressed rank-six kernels, path/parity reductions, and
exact finite certificate architecture. Any manuscript should cite
arXiv:2607.18031 prominently and avoid presenting "use of DNN methods for
square energy" as novel.

### DNN/conic precursors

G. Coutinho, T. Jung Spier, and S. Zhang, *Conic programming to understand
sums of squares of eigenvalues of graphs*, arXiv:2411.08184v1 (dated 11 August
2026 in the current manuscript), studies doubly nonnegative/conic programs for
positive and negative square energies and vector-chromatic bounds. It does not
state the connected `m=n+5` lower bound. It is prior/nearby methodological
literature and should be cited for the conic framework rather than treated as
an exact-scope predecessor.

Y. Liu, Q. Tang, and S. Zhang, *A positive square-energy strengthening of
Turan's theorem*, arXiv:2607.18044v1, uses the same DNN relaxation to prove an
upper bound in terms of clique number. Its direction and conclusion differ
from the AKMPZ lower bound and from fixed cyclomatic rank.

### Other graph-class and structural results

- B. Ning and J. Zeng, *A Proof of a Conjecture on Positive and Negative
  Square Energies of Unicyclic Graphs*, arXiv:2605.24668v1, proves the AKMPZ
  odd-unicyclic sign conjecture. Its graphs have `m=n`, not `m=n+5`.
- A. Abiad et al., *Positive and Negative Square Energies of Graphs*, Electron.
  J. Linear Algebra 39 (2023), 307--326, proves the older EFGW `n-1` bound for
  several classes, including unicyclic graphs. It neither reaches the AKMPZ
  `n` threshold for all rank-six graphs nor treats the full hexacyclic class.
- S. Akbari et al., *A Linear Lower Bound for the Square Energy of Graphs*,
  Electron. J. Combin. 32 (2025), P3.53, proves superadditivity over disjoint
  induced subgraphs and the general `3n/4` lower bound. It is an important
  ingredient/precursor but does not imply `s+(G)>=n` for all hexacyclic graphs.
- S. Zhang, *Extremal values for the square energies of graphs*,
  arXiv:2409.15504v2, develops semidefinite and graph-operation methods and
  proves `min{s+,s-}>=n-gamma(G)`. It does not give the exact hexacyclic claim.
- Q. Tang, Y. Liu, and W. Wang, *On the Positive and Negative p-Energies of
  Graphs under Edge Addition*, arXiv:2410.09830v4 / Discrete Appl. Math. 388
  (2026), 25--33, shows in particular why edge-addition monotonicity cannot be
  assumed. It does not settle the rank-six class.
- The repository's cactus and lower-rank manuscripts concern proper
  subclasses or smaller cyclomatic ranks. They are internal related work, not
  prior external literature establishing the all-connected rank-six scope.

## Method-specific comparison

No searched external source combined all of the following elements:

1. a decomposition exhaustive for all connected cyclomatic-rank-six simple
   graphs;
2. a multiblock theorem plus a single-positive-rank-block reduction;
3. enumeration of the `1198` suppressed rank-six multigraph kernels on two
   through ten branch vertices;
4. exact path elimination into physical parity orbits and
   canonical-plus-coordinate frontiers; and
5. machine-replayed exact DNN certificates closing every resulting target.

Items involving DNN optimization are not independently new in view of
Coutinho--Spier--Zhang and Liu--Tang--Zhang. Kernel suppression, finite
enumeration, and computer-assisted certification are standard broad
techniques in graph theory and optimization. The defensible potential
contribution is therefore the particular exhaustive rank-six synthesis and
its exact certificate system, not any isolated generic technique.

## Publication wording

Acceptable, subject to the remaining proof, manuscript, reproduction, and
package gates in `research/procedural/PUBLICATION.md`:

> We prove that every finite simple connected graph G with
> |E(G)|=|V(G)|+5 satisfies s+(G)>=|V(G)|. This establishes the hexacyclic
> specialization of AKMPZ Conjecture 1.2. We located no prior proof of this
> full class in the literature search documented on 12 August 2026.

Do not write:

- "we prove the AKMPZ conjecture" without the hexacyclic qualifier;
- "the first proof," "a novel method," or an unconditional priority claim;
- that the 2026 EFGW theorem already implies the `n` bound;
- that cactus, claw-free, diameter-two, unicyclic, or lower-rank results cover
  every connected hexacyclic graph; or
- that a negative database search establishes novelty.

## Gate result

The source-and-novelty audit required by Section B of the specialized
publication checklist is complete as a dated internal audit. Its result is
**cautiously favorable but non-certifying**: the AKMPZ source and exact
specialization are verified, no exact-scope predecessor was located, and the
known DNN and graph-class overlap is identified. This report does not close
any other acceptance gate and does not authorize contact or dissemination.
