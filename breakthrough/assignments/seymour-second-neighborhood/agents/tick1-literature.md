# Tick 1 literature audit (2026-07-25)

Independent same-target agent report, condensed and checked against the frozen
prompt. This is a research ledger, not a novelty certification.

## Exact reusable claims

| claim | source / scope |
|---|---|
| SNC holds when `delta+(D) <= 7` | Sadhukhan--Sandeep--Sen, arXiv:2606.30588v1, Theorem 1.1 |
| For a minimum-degree root `s`, `A=N+(s)`, `B=N++(s)`, `a1` minimizing `d_A+(a)`: `|B|>=delta` makes `s` Seymour; `|B|<=ceil(delta/2)` yields a local Seymour vertex | ibid., Proposition 2.6 (attributed to Kaneko--Locke) |
| `|N_A+(a1)| <= ceil(delta/2)-1` | ibid., Lemma 2.4 |
| Deleting arcs with tails outside a witness set preserves those witnesses' non-Seymour status | ibid., Lemma 5.6 / 6.2 |
| In an edge-minimal 1-counterexample, successive layers decrease; in particular `d+++(u)<=d++(u)<d+(u)` | Seacrest, arXiv:1808.06293v3, Lemma 4; Huang--Peng Lemma 2.1 is a special case |
| A counterexample of minimum outdegree `delta` implies one on at most `binom(delta+1,2)` vertices | Seacrest, Corollary 5; the reduced graph is not asserted to retain minimum degree exactly `delta` |
| A vertex-minimal counterexample is strongly connected and has `delta+ > sqrt(n)` | Espuny Díaz--Girão--Granet--Kronenberg, arXiv:2403.02842v2, Proposition 4 and preceding reduction |
| For the special global arc-then-vertex minimality notion, every deficit is 1 or 2 | Brantner--Brockman--Kay--Snively, arXiv:0808.0946, Definition 2.2 and Theorem 4.1 |

## Degree-eight funnel without minimality

If `delta+=8`, then `|A|=8`, `5<=|B|<=7`, and
`8-|B| <= |A1| <= 3`. Writing `r=|N_B+(a1)|`, the ten branches are

```
(|B|,|A1|,r) =
(5,3,5),
(6,2,6), (6,3,5), (6,3,6),
(7,1,7), (7,2,6), (7,2,7),
(7,3,5), (7,3,6), (7,3,7).
```

The preferred first branch is `(5,3,5)`: it has no missed vertex of `B` and
isolates exactly the loss of the odd regular-tournament argument used at degree
seven.

## Scope and chronology hazards

- Vertex-minimal, edge-minimal, globally arc-then-vertex-minimal, and a local
  witness obstruction are different notions. Conclusions may not be mixed.
- The public `rbsandeep/Seymour-Vertex-delta7` repository supplies reproducible
  OR-Tools models/logs but its formal-certificate layer is marked draft/future;
  solver logs are not independent UNSAT certificates.
- arXiv:2501.00614 has a claimed full proof, but later July 2026 primary papers
  still describe SNC as open. Treat it as an unvalidated claimed proof requiring
  a separate hostile audit.
- arXiv:2601.21563 was withdrawn after counterexamples to claims in that paper;
  this is not evidence of a counterexample to SNC.

## Next exact need

Prove a boundary-signature model in the forward direction only: every genuine
degree-eight obstruction induces a feasible finite model. No bound on outside
signature multiplicity is sound unless derived from the out-edge budgets of the
boundary vertices. A feasible local model may merely fail global completion.
