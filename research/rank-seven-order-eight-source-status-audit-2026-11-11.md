# Rank-seven order-eight kernel source and status audit (2026-11-11)

## Scope and release decision

This audit supplies the source-and-current-status gate in
`research/procedural/PUBLICATION.md` for the exact statement:

> If `G` is finite, simple, and connected, has cyclomatic rank seven and exactly
> one positive-rank cyclic block, and suppressing the degree-two vertices of
> that block gives a loopless 2-connected multigraph kernel on eight vertices,
> then `s+(G) >= |V(G)|`.

Equivalently, the result permits every simple subdivision of every such kernel
and arbitrary finite rooted trees attached at branch or subdivision vertices.
It does **not** cover suppressed kernel orders 9--12, rank-seven graphs with
several positive-rank cyclic blocks, or all connected heptacyclic graphs.

**Bounded-search conclusion (current through 2026-11-11):** no public theorem
with this full combined scope, in particular the allowance of arbitrary
leaf-bearing rooted-tree attachments, was located in the sources searched.
This negative search is not proof of novelty or priority. Two September 2026
preprints already subsume every tree-free instance of the stated class. Any
public description must say so and must make no firstness claim.

This audit performs no external write: no post, email, author contact,
conjecture-registry action, preprint submission, or journal submission.

## Exact conjecture source

The target is a restricted case of Conjecture 1.2 in:

- S. Akbari, H. Kumar, B. Mohar, S. Pragada, and S. Zhang, *Refinement
  of a conjecture on positive square energy of graphs*, arXiv:2506.07264v1,
  submitted 8 June 2025.
- Versioned record: <https://arxiv.org/abs/2506.07264v1>
- Versioned HTML: <https://arxiv.org/html/2506.07264v1>

That conjecture states that every connected graph of order `n` and size
`m >= n+1` satisfies `s+(G) >= n`. The source uses finite simple graphs. Since
cyclomatic rank seven gives `m=n+6`, the repository theorem is a special case,
not a resolution of the universal conjecture. The source abstract records that
AKMPZ prove their conjecture for claw-free graphs and graphs of diameter two;
those are additional already-known subfamilies inside the present scope.

The versioned arXiv record and API readback on 2026-11-11 confirmed the title,
the five authors, v1 submission timestamp, `math.CO` classification, and no
later version in the displayed submission history.

## Decisive prior-work boundary

### Every tree-free instance is already covered

Akbari, Hu, and Liu prove that every 2-connected noncycle `H` satisfies
`s+(H) >= |V(H)|`:

- S. Akbari, F.-T. Hu, and Y.-Y. Liu, *Positive and Negative Square Energies
  of 2-Connected Graphs*, arXiv:2609.04069v1, submitted 3 September 2026.
- <https://arxiv.org/abs/2609.04069v1>

If the repository theorem has no nontrivial rooted-tree attachment, then
`G` is its unique cyclic block. It is 2-connected and has cyclomatic rank
seven, hence is not a cycle. Thus the whole tree-free subfamily follows
immediately from this broader theorem; neither the order-eight restriction nor
the finite certificate census is needed for that subfamily.

The same authors subsequently prove that every connected noncycle of order
`n` and minimum degree at least two satisfies `s+(H) >= n`:

- S. Akbari, F.-T. Hu, and Y.-Y. Liu, *Positive Square Energy of Graphs with
  Minimum Degree at Least Two*, arXiv:2609.06778v1, submitted 6 September 2026.
- <https://arxiv.org/abs/2609.06778v1>

Within the repository's one-cyclic-block class, `delta(G) >= 2` holds exactly
when every rooted-tree attachment is trivial. Any nontrivial finite rooted tree
has a non-root leaf, which remains a degree-one vertex after attachment.
Therefore this second broad theorem again covers all and only the tree-free
members of the scoped class.

### What remains beyond those broad theorems

The repository theorem additionally covers arbitrary rooted-tree attachments
inside its restricted rank-seven/order-eight-kernel frontier. Such graphs may
have minimum degree one and are not 2-connected, so neither September theorem
subsumes them.

This distinction is substantive. If one separates an attached forest `F` and
uses only induced superadditivity, then `s+(F)=|E(F)|=|V(F)|-c(F)`; one loses
one unit for each forest component. A core inequality `s+(B) >= |V(B)|` does
not by itself recover the full `|V(G)|` target. The repository certificates
instead carry a rooted-tree extension in their DNN budget, while the unique
last orbit is partitioned into two complete induced tricyclic territories that
retain the assigned trees.

The safe comparative description is therefore:

> Recent general theorems already cover every tree-free instance. Relative to
> those results, this theorem additionally permits arbitrary rooted-tree
> attachments within the stated rank-seven, order-eight-kernel class.

It is not safe to call the full theorem "new" or "first" on the basis of this
audit.

## Broader baseline and methodological prior art

The following public results are relevant but do not prove the full exact
scope above:

1. Y. Liu, Q. Tang, and S. Zhang, *The positive and negative square-energy
   conjecture*, arXiv:2607.18031v1, prove for every connected `n`-vertex graph
   `min{s+(G),s-(G)} >= n-1`. This general theorem misses the present threshold
   by one.
2. S. Akbari, H. Kumar, B. Mohar, and S. Pragada, *Vertex Partitioning and
   p-Energy of Graphs*, Linear Algebra Appl. 724 (2025), 96--107,
   doi:10.1016/j.laa.2025.06.009; arXiv:2503.16882v2, prove the relevant
   induced-block superadditivity for positive and negative `p`-energy.
3. The same four authors, *A Linear Lower Bound for the Square Energy of
   Graphs*, Electron. J. Combin. 32(3) (2025), P3.53,
   doi:10.37236/13467, establish induced-subgraph superadditivity and the
   general `3n/4` lower bound.
4. A. Abiad, L. de Lima, D. N. Desai, K. Guo, L. Hogben, and J. Madrid,
   *Positive and Negative Square Energies of Graphs*, Electron. J. Linear
   Algebra 39 (2023), 307--326, prove the older `n-1` conjecture for several
   classes and study graph operations; this does not give the present `n`
   threshold for the scoped rank-seven class.
5. C. Elphick, M. Farber, F. Goldberg, and P. Wocjan, *Conjectured bounds for
   the sum of squares of positive eigenvalues of a graph*, Discrete Math. 339
   (2016), 2215--2223, doi:10.1016/j.disc.2016.01.021, is the source of the
   original `n-1` square-energy conjecture.

The cited literature supplies clear prior art for induced-superadditivity and
DNN/conic methods. This audit makes no priority determination about kernel
suppression, enumeration, or computer-assisted exact certification.

## Search record

Searches were run and public records read on 2026-11-11. Queries combined:

- `positive square energy`, `s+(G)`, and the AKMPZ inequality;
- `cyclomatic rank seven`, `cyclomatic number seven`, `heptacyclic`;
- `suppressed kernel`, `order eight kernel`, `rank-seven kernel`;
- `one cyclic block`, `single cyclic block`, `block decomposition`;
- `rooted tree attachment`, `tree attachment`, `pendant tree`, `leaf`;
- `subdivision`, `2-connected`, and `minimum degree at least two`.

The search covered the versioned arXiv records and HTML for 2506.07264,
2609.04069, 2609.06778, 2607.18031, and 2503.16882; the published Linear
Algebra and its Applications record for volume 724 (2025), pages 96--107,
doi:10.1016/j.laa.2025.06.009; general web searches for exact-scope terminology
and pendant/rooted-tree variants; the Electronic Journal of Combinatorics
record for P3.53; the Electronic Journal of Linear Algebra record for the 2023
paper; and DOI/title records for the 2016 paper.
No exact-scope predecessor or broad theorem plainly covering arbitrary rooted
trees was located.

This search has strict limitations. Public indexing can lag or omit results;
equivalent theorems may use different terminology; MathSciNet, zbMATH, closed
publisher databases, theses, accepted manuscripts, and non-English sources
were not exhaustively searched; and very recent work may not yet be indexed.
Absence from this search does not establish novelty, priority, or firstness.

## Required publication language

Acceptable:

> Akbari, Kumar, Mohar, Pragada, and Zhang conjectured the `n` bound for every
> connected graph with at least `n+1` edges. The theorem verifies only the
> stated rank-seven, single-block, order-eight-kernel class. Recent theorems
> already cover the tree-free instances; the certificate argument additionally
> permits arbitrary rooted-tree attachments within this restricted class. No
> previous theorem with the full combined scope was located in the search of
> 11 November 2026, but this negative search does not establish priority.

Forbidden or unsupported:

- "we prove the AKMPZ conjecture" without the restricted-class qualifier;
- "first proof", "novel", "previously open", or an unconditional priority
  claim;
- any implication that the order-eight census is needed for tree-free graphs;
- any claim that arXiv:2609.06778 already covers a graph with a nontrivial
  attached rooted tree;
- any all-heptacyclic, multiblock, or kernel-orders-9--12 claim;
- any claim that all historical producer searches were freshly recomputed.

## Gate result

The source/status gate is complete as a dated, bounded internal audit. Its
conclusion is cautiously favorable for the exact leaf-bearing extension, but
non-certifying as to novelty: no full-scope prior theorem was found, while the
tree-free subfamily is explicitly known already. This audit alone authorizes
no external action. All remaining acceptance, evidence, immutable-link,
idempotency, and destination gates remain mandatory.
