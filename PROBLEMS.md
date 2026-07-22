# problems

## current (exactly one — never more)

### Positive square energy at cyclomatic number at least 2

**Source:** Akbari, Kumar, Mohar, Pragada, Zhang, *Refinement of a
conjecture on positive square energy of graphs*, arXiv:2506.07264v1,
Conjecture 1.2.

**Problem:** If a connected simple graph G has n vertices and m >= n+1
edges, must the sum s^+(G) of squares of its positive adjacency eigenvalues
satisfy s^+(G) >= n?

The authors exhaustively checked connected graphs through n=9 and selected
databases through n=100. They prove the conjecture for claw-free graphs and
diameter-2 graphs. Counterexamples are compact machine-checkable certificates;
the sparse m=n+1 frontier and the paper's flagged triangle-unicyclic structural
bottleneck make this suitable for exact computation plus structural analysis.

**Selected:** 2026-07-21, cycle 1. Folder: `positive-square-energy/`.

## backlog — the hit list (certificate-shaped open conjectures, verified 2026-07-22)

Ranked tractability×significance. Each is a target where a counterexample or
resolution is a SMALL explicit checkable object. Load `breakthrough-method`,
pick per the §4.5 mandate. Recent proof this works: DGG conjecture disproved
(7-vertex digraph, Jul 2026); Jacobian conjecture disproved for n>=3 (Alpöge +
Fable 5, degree-4 map, Jul 19 2026) — **JC(2) now the marquee open case**.

### Tier 1 (best open × small-certificate × high-value)
1. **Seymour's Second Neighborhood** (8x9). Oriented graph with a vertex where
   |N++(v)| >= |N+(v)|. Counterexample = one explicit oriented graph where
   EVERY vertex fails, O(n^2) check. Best constant 0.7155 (Dec 2024), still <1.
   Attack: SAT over orientations of near-regular sparse graphs, nauty orbit-
   reduction, negated property as hard constraint; reach n~12-14.
2. **Caccetta-Haggkvist r=3** (7x9). Min out-degree >= n/3 ⇒ directed triangle.
   Counterexample = digraph, min out-deg >=ceil(n/3), zero triangles (O(n^3)).
   Attack: restrict to circulant digraphs on Z_n — triangle-freeness becomes a
   Sidon/difference-set condition, closed-form checkable; holds the known
   extremal constructions.
3. **Erdos-Szekeres ES(7)=33** (7x9). 33 points general position, no convex
   7-gon. SHOVEL-READY: SAT encoding exists (arXiv:2512.24061, Dec 2025) with
   partial UNSAT certs; heavy-tailed subfamilies block it. Attack: extend
   anchoring/symmetry-breaking, cube-and-conquer Kissat/CaDiCaL.
4. **Rota's Basis Conjecture n=5,6** (7x8). n disjoint bases ⇒ n×n array, rows =
   bases, columns = bases. n=5 apparently NOT fully computer-verified even for
   representable matroids. Attack: GF(2)/GF(3) representable, sparse-paving
   stepping stone, SAT with "every column independent".
5. **3x3 matrix-mult rank <=22** (7x8). Beat Laderman's 23 (open 49 yrs).
   Improvement = explicit set of <23 rank-1 bilinear forms, symbolic-exact
   check. Attack: AlphaTensor/AlphaEvolve-style search over C/finite fields.

### Tier 2 (strong, established, actively worked)
6. **Berge-Fulkerson** (6x9). Bridgeless cubic ⇒ 6 perfect matchings covering
   each edge twice. Counterexample must be a snark; ILP feasibility per snark.
   Attack: structured snark families (dot/star product, Loupekine), not brute.
7. **Frankl union-closed** (6x8). Some element in >=half the sets. A related
   conjecture already disproved by computer (arXiv:2211.12401) — methodology
   transfers. Attack: structured families (projective/affine-plane-generated).
8. **Bermond-Thomassen k=4** (6x6). Min out-degree >=2k-1 ⇒ k disjoint cycles.
   DGG-flavored; k<=3 proved. Attack: generalize k=2,3 tight templates, ILP
   disjoint-cycle-packing infeasibility.
9. **Bollobas-Nikiforov** (6x6). K_{w+1}-free ⇒ mu1^2+mu2^2 <= 2m(1-1/w).
   Attack: structured near-Turan graphs, w>=4, exact rational eigenvalues.
10. **Turan density K4- = 5/9** (5x9). Disproof = explicit 3-graph density >5/9,
    K4--free. Attack: exact-rational flag-algebra SDP (SDPA-GMP + rounding).

### Tier 3+ (high value, harder)
11. **Erdos-Sos** (5x7) — announced proof never verified; small-k disproof-hunt.
12. **Ryser-Brualdi-Stein gap** (5x6) — group-table Latin squares in the window.
13. **Alon-Tarsi** (5x6) — push n=26 via the SU(n)-integral reformulation.
14. **MDS conjecture non-prime q** (4x6) — GF(9,16,25), canonical-form search.
15. **Jacobian conjecture n=2 / JC(2)** (4x10). MARQUEE. Explicit (P,Q):C^2->C^2,
    constant nonzero Jacobian, exhibit a collision. Attack: Druzkowski cubic-
    linear normal forms (proven to capture any counterexample), exact
    resultants/Grobner. Highest expected value on the list per the reporter.
16. **Singmaster** (3x6) — record-hunt a 9th binomial repeat.
17. **Moore graph degree 57** (3x9) — no symmetry handle; needs a new idea.
18. **Projective plane order 12** (2x9) — hopeless brute force absent new lever.

WATCH: Cycle Double Cover — OpenAI claimed an AI proof (Jul 2026), unrefereed;
if it collapses it becomes Tier-1 (min counterexample = snark, girth>=12). Odd
Hadwiger disproved Dec 2025 (don't confuse w/ standard Hadwiger, still open).

## backlog (older seed directions)

Seed directions for cycle-1 research (verify current status in the literature
before trusting any of these; some may have moved):

- Explicit counterexample hunts in polynomial-map land (the Jacobian-conjecture
  counterexample archetype: small explicit certificate, exact-arithmetic
  verifiable). Look at neighboring open questions: tame vs wild automorphisms
  in dim 3 specializations, Keller-map variants with structural constraints.
- Extremal combinatorics / Ramsey small cases with open bounds where SAT +
  clever symmetry-pruning has edge.
- Open OEIS conjectures (search "conjecture" in recent OEIS entries) —
  underexplored, certificate-shaped.
- Fresh conjectures in the last ~12 months of arXiv math.CO / math.NT papers
  (authors state them and move on — often nobody has run a serious search).
- MathOverflow open-problem tags with concrete finite formulations.

## archive (resolved or retreated — with post-mortems)

(empty)
