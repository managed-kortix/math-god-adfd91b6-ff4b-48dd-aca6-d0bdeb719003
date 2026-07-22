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

**Fresh reproduction completed.** A newly generated graph6 file had the same
211,866 records and SHA-256. Fresh SymPy and PARI processes reproduced the
exact same pass counts, minimizer, rational lower endpoint, 80-digit slack, and
PARI worker characteristic-polynomial hashes. The m=16 aggregate certificate
has therefore passed the fresh-process gate.

## 2026-07-22 — n=10,m=17 screen and low-tail certificate

Screened all 361,342 connected nonisomorphic graphs. The observed minimum is
at graph6 `I?`FBqsF_`, with slack `5.911281165531542...`. Its characteristic
polynomial factors as

`(x-1)^4 (x+2) (x^2+3x+1) (x^3-x^2-9x+2)`.

Exact SymPy rational root isolation certifies positive slack for the lowest 50
screened graphs. PARI independently matched every one of their exact integer
characteristic polynomials and gives minimizer slack
`5.9112811655315422682710710157956986343169838260335...`. This certifies only
the low tail; a full-slice exact pass remains required.

**Full SymPy pass.** The compact verifier was generalized to accept a rational
root-isolation precision. Width below `10^-6` is ample because the numerical
minimum is nearly 6, while avoiding unnecessary 30-decimal algebraic work.
All 361,342 graphs were exact-certified. The least rigorous lower endpoint is
`20940707161630/3542499915409 = 5.911279509293167... > 0` at the same minimizer.
The ordered input SHA-256 is
`179562801fb7a60d29da2c6a6ed03909c27660ef57fe6ddaf94490005ce4729e`.
Independent full PARI verification remains next.

**Full PARI pass.** Independent GP workers completed all 361,342 records,
produced and parsed exact integer characteristic polynomials throughout, and
found every 80-digit slack positive. The input hash matched SymPy exactly.
PARI reproduced minimizer `I?`FBqsF_` with
`s^+-10 = 5.9112811655315422682710710157956986343169838260335...`.
Thus m=17 is certified by both engines; the cumulative exact two-engine census
for m=11 through 17 contains 773,865 connected graphs. Fresh reproduction is
the remaining aggregate verification gate.

**Fresh reproduction completed.** Newly generated m=17 input and fresh SymPy
and PARI processes reproduced the same input hash, pass count, minimizer,
rational lower endpoint, 80-digit slack, and PARI exact-charpoly worker hashes.

## 2026-07-22 — n=10,m=18 screen and low-tail certificate

Screened all 561,106 connected nonisomorphic graphs. The observed minimum is
at graph6 `I?q`qjo{?`, with slack
`6.9242077361381927285404716806637992814001351189310...`. Its exact
characteristic polynomial factors as

`x^2 (x-1)^3 (x+2)^2 (x^3-x^2-12x+8)`.

Exact 30-decimal SymPy rational root isolation certifies all lowest 50 positive,
and PARI independently matches all 50 exact characteristic polynomials and
positive slacks. A full-slice pass remains required.

## 2026-07-22 — full m=18 pass launched; dumbbell identity

Regenerated the complete 561,106-record slice. Its ordered graph6 SHA-256 is
`b47af8111f2d07caf6fa2d09bba7351d9fa5969bbac63ea0ae3669e2cfe8bdc2`.
Split it into 24 line-balanced chunks and launched 12 outer jobs with two
SymPy workers each. Each chunk is written atomically only after all its exact
rational root-isolation checks pass, so interruption loses at most one chunk
per active job. Width below `10^-6` is sufficient against the screened minimum
slack `6.924...`. This job remains active and is not yet a certificate.

In parallel, let `D_n` be two copies of `C_n`, joined by one edge between
distinguished vertices. If `p_n(x)=chi(C_n,x)` and
`q_n(x)=chi(P_{n-1},x)` (the principal minor at that vertex), the block
determinant/rank-one bridge formula gives

`chi(D_n,x)=p_n(x)^2-q_n(x)^2=(p_n-q_n)(p_n+q_n)`.

Equivalently the two factors are the characteristic polynomials of
`C_n+e_0e_0^T` and `C_n-e_0e_0^T`, corresponding to symmetric and
antisymmetric vectors under interchange of the cycles. SymPy independently
constructed the adjacency matrices and verified the identity exactly for
`n=3,5,7,9`. In Chebyshev notation,
`p_n=2(T_n(x/2)-1)` and `q_n=U_{n-1}(x/2)`. This reduces analysis of the
whole dumbbell family from degree `2n` to two rank-one perturbations of a
cycle.

The further Chebyshev identity
`p_n=(x-2)(U_k+U_{k-1})` and
`q_n=U_k-U_{k-1}` for `n=2k+1` shows that

`chi(D_n)=(U_k+U_{k-1})^2 ((x-2)(U_k+U_{k-1})-(U_k-U_{k-1}))
((x-2)(U_k+U_{k-1})+(U_k-U_{k-1}))`.

Thus all nontrivial spectral movement is confined to two degree-`k+1`
polynomials; the other `k` cycle eigenvalues retain multiplicity two. The
standalone `dumbbell_family.py` exactly isolates these factors and certifies
strict positive slack for every odd `n<=31`; the least certified lower bound
in that range occurs at `n=5` and exceeds `0.5938737271`. The attempted
`n<=101` run exceeded the short foreground window and is not counted.

`minimizer_fingerprints.py` reproduced the structural census for m=11..18.
All eight minimizers are triangle-free and contain an induced claw, so neither
the paper's claw-free theorem nor triangle-specific mechanisms explain them.
The m=11..17 minimizers all have inertia `(6,0,4)`; m=18 changes to `(5,2,3)`.
Bridges disappear at m=14, and diameter drops to two at m=15,17,18 (so those
slices are already covered by the paper's diameter-two theorem, despite being
useful verifier checks).

For later comparison with the bridge perturbation, the positive square-energy
of the underlying odd cycle itself has a closed trigonometric form. Writing
`a=pi/(2n)` and summing the positive eigenvalues `2 cos(2 pi j/n)` gives

- if `n=4l+1`, `s^+(C_n)-n = 3-4 cos(a) sin(3a)/sin(4a)`;
- if `n=4l+3`, `s^+(C_n)-n = 1-4 cos(3a) sin(a)/sin(4a)`.

These identities follow directly from the finite cosine sum after replacing
`cos^2(theta)` by `(1+cos(2theta))/2`. They explain the alternating sign of
the odd-cycle slack and provide an explicit baseline for proving that the
rank-one symmetric/antisymmetric bridge perturbations together contribute
enough to make the dumbbell slack positive.

The m=18 low-50 structural scan found 14 diameter-two and 36 diameter-three
graphs; 40 are triangle-free of girth four and 10 have one triangle; all 50
contain an induced claw. Their inertia is not constant (seven distinct
triples), with `(4,3,3)` most frequent (18/50). Therefore the exact exhaustive
slice adds genuinely uncovered diameter-three cases, while the extremal graph
itself has diameter two and lies in a previously proved class.

**Independent full m=18 PARI pass.** The 24 checkpointed GP chunks completed
all 561,106 graphs. Each graph's exact integer characteristic polynomial was
generated and parsed, and every 80-digit real-root slack was strictly positive.
PARI's global minimum is graph6 `I?q`qjo{?`, with
`s^+-10 = 6.9242077361381927285404716806637992814001351189309953...`,
agreeing with the earlier low-tail result. The exact SymPy pass has completed
12 of 24 atomic chunks; no full two-engine claim is made until the remainder
finishes and aggregate hashes/counts are checked.

**Full m=18 two-engine aggregate.** SymPy completed the remaining chunks.
`aggregate_chunk_certificates.py` independently reread all 24 input chunks and
paired output files, checked each engine's count and SHA-256 against raw input,
and aggregated exactly 561,106 records with global ordered SHA-256
`b47af8111f2d07caf6fa2d09bba7351d9fa5969bbac63ea0ae3669e2cfe8bdc2`.
Every exact rational SymPy lower endpoint is positive. Both engines select
`I?q`qjo{?`; the global rigorous SymPy lower bound is
`17510320956417/2528856896644 = 6.9242039672...`, while PARI gives the
high-precision value `6.924207736138192728540471680663799...`. Therefore m=18
is internally certified in both engines, bringing m=11..18 to 1,334,971
graphs. A newly generated fresh reproduction remains before publicity.

**Fresh m=18 reproduction completed.** From a newly generated graph6 stream,
fresh SymPy and GP processes completed all 24 chunks. The standalone aggregate
reproduced count 561,106, global SHA-256
`b47af8111f2d07caf6fa2d09bba7351d9fa5969bbac63ea0ae3669e2cfe8bdc2`,
minimizer `I?q`qjo{?`, exact lower endpoint
`17510320956417/2528856896644`, and the prior 80-digit PARI slack. The finite
m=18 slice has now passed the fresh-process gate in both engines.

The background exact dumbbell certificate also completed every odd cycle
length `3<=n<=101`: all 50 equal-cycle dumbbells have positive slack, and the
least exact lower endpoint remains the n=5 case (`>0.5938737271`). This is a
finite family certificate, not yet the desired analytic all-n lemma.

For an analytic route, put a non-retained eigenvalue in the spectral band as
`x=2 cos(theta)`. The Chebyshev equations `p_n(x) +/- q_n(x)=0` become

`2(cos(n theta)-1) +/- sin(n theta)/sin(theta)=0`.

After removing the retained roots `sin(n theta/2)=0`, the two moving branches
satisfy the simple phase equations

`tan(n theta/2)=+1/(2 sin(theta))` and
`tan(n theta/2)=-1/(2 sin(theta))`,

with the out-of-band Perron root handled by the hyperbolic continuation. Also,
because `s^++s^-=2|E|=4n+2`, the desired dumbbell inequality is equivalent to
the signed-square imbalance `sum lambda|lambda| >= -2`. Numerically this
imbalance alternates in sign and tends to zero; the only apparent difficult
congruence class is `n=1 mod 4`, where the minimum observed value is the n=5
case `-0.81225249...`, already well above -2. The phase equations are the next
route to a uniform bound rather than further polynomial root isolation.

## 2026-07-22 — m=19 screen and exact low tail

Screened all 795,630 connected n=10,m=19 graphs. The numerical minimum is
`8.0627694281544735...` at graph6 `I?bF`xw{?`. Fresh exact SymPy rational
root isolation certifies each of the lowest 50 positive; PARI independently
matches all 50 exact integer characteristic polynomials and slacks. For the
minimizer,

`chi(x)=x^2(x^4-3x^3-7x^2+16x-6)(x^4+3x^3-3x^2-4x+2)`

and PARI gives slack
`8.0627694281544735090879961694357365431607856405603...`. This remains a
low-tail certificate, not a full-slice proof. The fresh m=18 input meanwhile
reproduced the previous SHA-256 exactly; 12/24 fresh SymPy chunks have passed.
