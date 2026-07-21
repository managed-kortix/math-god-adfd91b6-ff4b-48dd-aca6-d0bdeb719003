# notebook — positive square energy

## 2026-07-21 — selection

**Hypothesis.** The sparse frontier m=n+1 is the highest-yield place to test
Conjecture 1.2 beyond the published exhaustive range n <= 9.

**Rationale.** The conjectured threshold is constant in m, known classes remove
dense/diameter-2 and claw-free graphs, and any counterexample is likely sparse
and structurally exceptional. Nonisomorphic connected n=10, m=11 graphs are a
finite census accessible to nauty.

**Status.** Infrastructure setup next; no mathematical result yet.

## 2026-07-21 — first sparse census

**Hypothesis.** A counterexample or exceptionally low-slack graph may first
appear among connected graphs with n=10 and the minimum allowed m=11.

**Code.** `search_geng.py` streams `nauty-geng -cq 10 11:11`, decodes graph6,
and ranks graphs by NumPy's floating-point estimate of s^+(G)-10.

**Result (screening only).** The census contained 2,678 nonisomorphic connected
graphs. The smallest observed slack was approximately
`0.593873751236952`, at graph6 `I?`D@POd?` (backticks escaped conceptually;
the literal graph6 string is stored in the search output and code invocation).
Its degree sequence is `(2,2,2,2,2,2,2,2,3,3)`. NetworkX independently
confirmed 10 vertices, 11 edges, connectivity, and agreement with our graph6
decoder. SymPy factors its exact adjacency characteristic polynomial as

`(x-1)(x^2-x-3)(x^2+x-1)^2(x^3-4x+1)`.

**Conclusion.** No numerical counterexample at n=10,m=11. This is not yet a
certified exhaustive bound: exact root-isolation certificates for the low
candidates and a second-engine pass remain required. The factorized minimizer
is highly structured and is the first object for exact analysis.

**First exact check.** `exact_certify.py` was run in a fresh Python process on
graph6 `I?`D@POd?`. SymPy exact rational root isolation (width < 10^-30)
certified five positive roots counting multiplicity and

`0.593873751236949402 < s^+(G)-10 < 0.593873751236949403`.

Thus this particular observed minimizer rigorously satisfies the conjectured
bound. This is only the first-engine certificate for one graph; exact checks
of the remaining low tail and PARI independence are still queued.
