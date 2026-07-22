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

## 2026-07-21 — complete exact n=10,m=11 certificate

**Experiment.** Ran `exact_certify.py` on all 2,678 graph6 records from
`nauty-geng -cq 10 11:11`. Every characteristic polynomial was computed over
the integers and every real root was enclosed in a disjoint rational interval
of width below 10^-30. Summing squared positive-root interval bounds gave a
strictly positive lower bound for every graph.

**Independent engine.** `pari_verify.py` reconstructed every adjacency matrix,
computed `charpoly(A,x)` and `polrootsreal` in PARI/GP at 80-digit precision.
All 2,678 PARI characteristic polynomials exactly matched SymPy coefficient by
coefficient, and all PARI slacks were positive.

**Certified result.** Every connected simple graph with n=10 and m=11 satisfies
`s^+(G) >= 10.593873751236949401... > 10`. Equality in this finite census is
attained by graph6 `I?`D@POd?`, which is two disjoint 5-cycles joined by a
single bridge (the `(5,5)` dumbbell). The exact lower endpoint from rational
root isolation is positive; the displayed decimal is only a readable summary.

This extends the conjecture's exact computational frontier specifically on the
minimum-edge slice m=n+1 from the paper's n<=9 census to n=10. Novelty and a
compact stranger-verifiable aggregate certificate remain necessary before any
public claim.

## 2026-07-21 — n=10,m=12 screen

Screened all 8,548 connected nonisomorphic graphs. The observed minimum slack
was `1.498439554674811...` at graph6 `I?`DA_wIO`. The lowest 20 were certified
positive by exact SymPy root isolation, and PARI exactly matched all 20
characteristic polynomials and numerical slacks.

**Full exact follow-up.** All 8,548 graphs were subsequently certified by
exact SymPy rational root isolation. PARI independently produced an exactly
matching characteristic polynomial for every graph and positive 80-digit
slack. Hence every connected n=10,m=12 graph has
`s^+(G) >= 11.498439554674811... > 10`.

## 2026-07-21 — n=10,m=13 and m=14

All 22,950 connected n=10,m=13 graphs were certified using exact rational
SymPy root isolation, with exact PARI characteristic-polynomial agreement for
all 22,950. The finite-slice minimum is
`s^+(G)=12.400133863581128... > 10`, at graph6 `I?`DA`gJO`.

The n=10,m=14 slice contains 53,863 graphs. Floating screening found minimum
slack `3.258887081526075...` at graph6 `I?`acgwg_`; exact SymPy and independent
PARI checks certify the low 20. Full exact certification was launched and is
still running across a heartbeat boundary; do not launch a duplicate process.

## 2026-07-21 — complete exact n=10,m=14 certificate

**Experiment.** Regenerated all 53,863 connected nonisomorphic graphs with
`nauty-geng -cq 10 14:14` in a fresh sandbox process. `exact_certify.py`
computed each integer adjacency characteristic polynomial, exactly isolated
all real roots in rational intervals of width below `10^-30`, and obtained a
strictly positive lower bound for `s^+(G)-10` in all 53,863 cases. There were
no errors or nonpositive lower endpoints.

**Independent engine.** `pari_verify.py` independently reconstructed all
53,863 matrices. PARI's exact `charpoly` agreed coefficient-for-coefficient
with SymPy in every case, and 80-digit `polrootsreal` evaluation gave positive
slack in every case.

**Certified result.** The minimum is attained at graph6 `I?`acgwg_`, with
`s^+(G)-10 = 3.2588870815260757547073475364...`. Thus every connected simple
graph with 10 vertices and 14 edges satisfies the conjectured inequality.
Together with the previous slices, all 88,039 connected n=10 graphs with
11 through 14 edges are now exact-certified. This remains a finite census,
not a proof of Conjecture 1.2.

## 2026-07-21 — n=10,m=15 screen and low-tail certificate

Screened all 112,618 connected nonisomorphic graphs. The observed minimum is
exactly `s^+(G)-10=4` at graph6 `ICOf@pSb?`; its six positive adjacency
eigenvalues are numerically `1,1,1,1,1,3`, so `s^+=14`. Exact SymPy rational
root isolation certified the lowest 20, and PARI independently matched all 20
integer characteristic polynomials and gave positive slack. Full-slice exact
certification remains next; the floating screen alone is not exhaustive proof.

**Full exact follow-up.** A fresh SymPy process exact-certified all 112,618
graphs: integer characteristic polynomials, rational real-root isolation at
width below `10^-30`, no errors, and no nonpositive slack lower endpoint.
A separate PARI process reconstructed all 112,618 adjacency matrices, matched
every characteristic polynomial coefficient-for-coefficient, and found no
nonpositive 80-digit slack. The exact minimum lower bound is 4 at graph6
`ICOf@pSb?`. Hence every connected n=10,m=15 graph satisfies `s^+(G)>=14>10`.
The cumulative exact-certified total for m=11 through 15 is 200,657 graphs.

## 2026-07-21 — n=10,m=16 screen and low-tail certificate

Screened all 211,866 connected nonisomorphic graphs. The observed minimum
slack is `5.06187147279694...` at graph6 `I?`DF`YN?`. Exact SymPy rational
root isolation certified the lowest 20 positive, and PARI independently
matched all 20 integer characteristic polynomials and slacks. Full-slice exact
certification remains next; the screen is not itself an exhaustive proof.

## 2026-07-21 — full m=16 certification attempt

Regenerated the complete 211,866-record graph6 slice. A serial exact SymPy run
and then a 32-way split run both exceeded the shell's 20-minute process window;
the latter produced 247,185 output lines before termination, but outputs are
not accepted as a certificate because chunks were incomplete. No `ERROR` or
nonpositive slack was observed in completed records. This is an infrastructure
result only, not mathematical progress. The next run will use bounded
parallelism, one atomic output and completion marker per chunk, so completed
chunks survive interruption and can be checked exactly once.

**Successful compact certificate.** `batch_exact_certify.py` used 16 bounded
workers and completed exact rational root isolation for all 211,866 records.
Every lower bound for `s^+-10` was strictly positive. The least exact lower
endpoint was attained at `I?`DF`YN?` and equals

`14734185568792384654654323644651704256129128122371442382501185586836113407590319046813515369840747272878357699092186381 / 2910817796930549421169163740037535324261740806692831225688955715483886074316306918159490034385198707635063716544264100`,

approximately `5.0618714727969403`. The ordered graph6 input SHA-256 was
`b51f7340afeb301878dc93ba894d89ac85572d23a8b5a39096a21930ecf0efe0`.
A first persistent-worker PARI pass exceeded one hour before producing an
atomic aggregate output, so it is rejected as incomplete. Independent PARI
verification remains required before the slice is fully certified.

## 2026-07-22 — complete independent PARI m=16 certificate

The first PARI design was slow because it launched an interactive round trip
for every graph and redundantly recomputed each characteristic polynomial in
SymPy. `batch_pari_verify.py` now sends one batch program to each GP worker.
With 64 workers it completed all 211,866 records. For every graph PARI produced
an exact integer characteristic-polynomial coefficient vector, which the
driver parsed and hashed, and an 80-digit real-root slack; every slack was
strictly positive. The ordered input hash matched the SymPy run exactly:
`b51f7340afeb301878dc93ba894d89ac85572d23a8b5a39096a21930ecf0efe0`.
PARI independently found the same minimizer `I?`DF`YN?`, with
`s^+-10 = 5.06187147279694008219895763296165025385192302815164949...`.

Therefore all 211,866 connected n=10,m=16 graphs pass both engines, and the
cumulative exact-certified n=10 census for m=11 through 16 is 412,523 graphs.
One fresh-process reproduction of the compact scripts remains before treating
the aggregate certificate as public-ready.
