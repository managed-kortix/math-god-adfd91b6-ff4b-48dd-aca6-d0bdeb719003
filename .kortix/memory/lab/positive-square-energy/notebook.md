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

The cycle baseline simplifies much further. Since
`sin(4a)=4 sin(a) cos(a) cos(2a)` and
`cos(3a)=cos(a)(2cos(2a)-1)`, the formulas above reduce exactly to

- `s^+(C_n)-n = 1-sec(pi/n)` for `n=1 mod 4`;
- `s^+(C_n)-n = sec(pi/n)-1` for `n=3 mod 4`.

This immediately proves the equal-cycle dumbbell inequality for every odd
`n=3 mod 4`: its two vertex-disjoint cycles are induced subgraphs, so square-
energy superadditivity gives
`s^+(D_n) >= 2s^+(C_n) = 2n+2(sec(pi/n)-1) > 2n`.
Consequently the analytic family problem is now rigorously reduced to
`n=1 mod 4`, where superadditivity misses by only
`2(sec(pi/n)-1)=O(n^-2)` and the bridge perturbation must repay that deficit.

The remaining congruence class also yields to the paper's gluing lemma. View
`D_n` as base `K_2`, with one rooted `C_n` glued to each endpoint. Vertex-
transitivity gives the negative spectral diagonal
`d=tr(A^-(C_n))/n=E(C_n)/(2n)=csc(pi/(2n))/n`. The sine Taylor bound together
with `333/106<pi<22/7` gives `d<2/3` for n>=13, so the gluing correction
`s^+([[-d,1],[1,-d]])=(1-d)^2>1/9`. Meanwhile
`cos x >= 1-x^2/2` and `pi<22/7` give
`sec(pi/n)-1 < 1/9` for `n>=9`. The preliminary comparison

`s^+(D_n) >= 2s^+(C_n)+(1-d)^2 > 2n-2/9+1/9` is insufficient.

The factor of two means the crude correction must exceed
`2(sec(pi/n)-1)`. It does for every `n>=13`: monotonicity reduces the check to
n=13, and `cos x>=1-x^2/2`, `pi<22/7` give the rational certificate
`sec(pi/13)-1<1/18`. The only remaining lengths n=5,9 were exact-isolated by
the standalone certificate. D_5 has slack `0.5938737512369494019...`; D_9 is
also strictly positive. Together with the n=3 mod 4 argument, this proves the
equal odd-cycle dumbbell lemma for every odd n>=3. Fresh PARI verification of
D_9 remains before treating this as fully gated progress.

Fresh PARI independently reproduced the exact integer characteristic
polynomials for D_5 and D_9 and found 80-digit positive slacks
`0.5938737512369494019308...` and `0.8926085469026702207213...`. Thus the
all-odd lemma is now two-engine checked. Full proof statement: if D_n is formed
from two C_n's by a bridge and odd n>=3, then `s^+(D_n)>2n`. For n=3 mod 4,
induced-subgraph superadditivity and `s^+(C_n)-n=sec(pi/n)-1` suffice. For
n=1 mod 4, n>=13, the gluing lemma gives correction `(1-d)^2>1/9`, whereas
the two-cycle deficit is `<1/9`; D_5,D_9 are the exact finite exceptions.

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

**Full m=19 pass launched.** Regenerated all 795,630 records, ordered SHA-256
`2178cc8ac8ce524cc43ab6671573c0830e2b57df387b8b95c7d275e93d62e041`,
and split them into 32 atomic chunks. The full exact SymPy pass uses width
below `10^-6`, ample against the screened slack above 8, and remains active.
`count_known_classes.py` is separately counting exact diameter-two and induced-
claw predicates over m=18,19 so the genuinely new portion of the computation
can be stated rather than conflated with classes already proved in the paper.

The exact class count completed. At m=18, only 4,225 of 561,106 graphs lie in
the union of the diameter-two (3,418) and claw-free (807) classes, leaving
556,881 not covered by either theorem. At m=19, the union contains 15,685 of
795,630 (14,794 diameter-two, 892 claw-free; one graph lies in both), leaving
779,945 uncovered. Thus the exhaustive certificates are not mostly redundant:
over 98% of each of these slices lies beyond those two published sufficient
conditions. `count_known_classes.py` computes diameter two from exact Boolean
walk existence and claw-freeness by enumerating triples in every neighborhood.

**Full m=19 paired certificate.** SymPy completed all 32 chunks. The standalone
aggregator validated each raw chunk's count and SHA-256 against both engine
outputs and obtained exactly 795,630 graphs, global hash
`2178cc8ac8ce524cc43ab6671573c0830e2b57df387b8b95c7d275e93d62e041`.
Every exact SymPy slack lower endpoint is positive. Both engines select
`I?bF`xw{?`; the least rigorous lower endpoint is
`1480358217260351809395815033389/183604253579963139078852096400`,
approximately `8.0627654`, and PARI gives
`8.062769428154473509087996169435736543...`. Thus m=19 is two-engine
certified, bringing the cumulative m=11..19 census to 2,130,601 graphs.
Fresh reproduction remains.

## 2026-07-22 — m=20 screen and low-tail certificate

Screened all 1,032,754 connected n=10,m=20 graphs. The observed minimizer is
graph6 `I?rFf_{N?`, with slack
`9.055728090000841214363305325074895058...`. Exact SymPy rational isolation
certifies the lowest 50 and PARI independently matches all their integer
characteristic polynomials and slacks. The minimizer factors especially cleanly:

`chi(x)=x^5(x-4)(x^2+2x-4)^2`.

It is the 4-regular circulant `Cay(Z_10,{+/-1,+/-4})`, has automorphism group
size 320, diameter two, girth four, and no triangles. Its positive eigenvalues
are `4` and `sqrt(5)-1` with multiplicity two, so exactly
`s^+=16+2(sqrt(5)-1)^2=28-4sqrt(5)` and slack `18-4sqrt(5)`.
This low-tail result is exact in both engines, but the full m=20 slice remains.

Across the exact slice minimizers, the m=11 through m=17 graphs all have
inertia `(6,0,4)`, followed by `(5,2,3)` at m=18,19 and `(3,5,2)` at m=20.
The m=20 circulant is 4-regular, diameter two, triangle-free of girth four,
biconnected, and contains an induced claw. Thus it is covered by the paper's
diameter-two theorem despite not being claw-free. This is a structural
fingerprint only, not evidence about the uncaught remainder of the slice.

The m=20 low-50 structural census sharpens this. All 50 contain induced claws;
only 19 have diameter two, while 30 have diameter three and one has diameter
four. Hence 31/50 are outside both the diameter-two and claw-free theorems.
There are 26 triangle-free members and 24 with triangles (13 with one, nine
with two, two with three), and ten distinct inertia triples. The low tail is
therefore structurally heterogeneous and mostly not explained by those two
published sufficient conditions, even though its exact minimizer is.

The complete m=20 theorem-coverage count confirms this at full scale. Of all
1,032,754 connected graphs, 52,476 have diameter two and 942 are claw-free;
the union has 53,414 graphs, leaving 979,340 outside both classes. The overlap
is four graphs. Thus 94.83% of this slice is not covered by either of the two
headline sufficient conditions in the target paper.

**Fresh m=19 gate completed.** All 32 regenerated chunks passed exact SymPy
and independent PARI verification. The strengthened aggregator also checked
that the chunks form exactly the same graph6 multiset as the regenerated whole
file. It reproduced 795,630 graphs, whole SHA-256 `2178cc8a...`, minimizer
`I?bF`xw{?`, rational lower bound, and 80-digit PARI slack. The m=19 finite
slice has now passed every computational verification gate.

**Unequal odd-cycle probe.** Float-screened every bridge `C_p--C_q` for odd
`3<=p,q<=101`; the least slack was still the equal `(5,5)` case at
`0.5938737512...`, and no counterexample appeared. The same gluing setup has
correction equal to the square of the positive eigenvalue of
`[[-d_p,1],[1,-d_q]]`, where `d_r=csc(pi/(2r))/r`. Crude rational bounds prove
the unequal family whenever both p,q>=13: each d is below 2/3, so correction
exceeds 1/9, while the sum of both possible cycle deficits is below 1/9.
Small-fixed/large-variable pairs remain; do not claim the unequal extension.

The exact gluing lower bound was then mapped for odd p,q through 100,001.
Its only persistent failure mechanism is a `C_5` side: for `(5,q)` with
q>=9 the bound remains negative and tends to about `-0.1078342693`, although
the actual spectral slack stays positive in the direct q<=101 scan. Outside
the C5 pairs, the gluing bound's isolated small failure is `(5,5)` itself.
Thus extending the lemma to unequal cycles reduces naturally to proving the
one-parameter family `C_5--C_q`; brute force alone will not close it.

The C5-fixed characteristic polynomial has an exact uniform factor. The
rank-one bridge identity for unequal cycles is
`chi(C_5--C_q)=p_5 p_q-q_5 q_q`, and symbolic division shows
`x^2+x-1` divides it for every odd q (checked by the Chebyshev recurrence and
symbolically for q<=101). In fact the proof is immediate: `x^2+x-1` divides
both `p_5` and the rooted minor `q_5`, so it divides the bridge polynomial for
every q, without a parity restriction. These are the two C5 eigenvalues that persist under
the bridge because their eigenvectors vanish at the attachment vertex. This
reduces the moving spectrum by degree two and suggests treating C5--Cq as a
fixed finite-rank perturbation of Cq rather than through the coarse gluing
bound.

Explicitly,
`p_5=(x-2)(x^2+x-1)^2` and
`q_5=(x^2-x-1)(x^2+x-1)`, so after removing the persistent factor the moving
polynomial is

`(x-2)(x^2+x-1)p_q-(x^2-x-1)q_q`.

Numerically, the gain relative to `s^+(C_q)` tends to
`5.80092867...`, leaving an asymptotic surplus near `0.80092867` over the
required five new vertices. This suggests a direct phase-shift proof with a
large safety margin; the gluing lower bound loses that margin by treating the
C5 side only through one spectral diagonal.

Exact Sturm counts for q=5,7,...,29 show the reduced degree-(q+3) moving
polynomial has exactly q+1 roots in [-2,2] and precisely two simple outliers,
one below -2 and one above 2. Together with the persistent golden-ratio pair,
the entire C5--Cq spectrum is therefore a band phase shift plus two bound
states. This is the right decomposition for an analytic energy comparison:
control the squared positive bound state and the displacement of the positive
band roots against Cq.

For a band root `x=2cos(theta)`, substituting
`p_q=2(cos(q theta)-1)` and `q_q=sin(q theta)/sin(theta)` into the reduced
polynomial yields, after removing the roots with `sin(q theta/2)=0`, the phase
equation

`tan(q theta/2)=-(x^2-x-1)/(2(x-2)(x^2+x-1)sin(theta))`.

The removed roots are exactly one copy of each nontrivial double eigenvalue of
Cq, represented by the eigenvector vanishing at its bridge vertex. Hence much
of both cycles' spectra persists unchanged; only the rooted symmetric sector
obeys this phase shift. This equation is now the analytic target for C5--Cq.

The positive outlier has a clean infinite-q algebraic limit. Put
`x=r+r^{-1}` with r>1. The exact finite equation below shows the limit is the
unique real root r>1 of

`r^8-r^7-2r^6+2r^5-r^4+r-1=0`,

namely `r=1.67560406152636...`, giving
`x=2.27240376078769...` and square `5.163818852042...`. Eliminating r gives
the degree-eight equation
`x^8-2x^7-9x^6+18x^5+24x^4-50x^3-15x^2+46x-17=0`.
An earlier scratch simplification to `r^5=3` was false despite producing the
same displayed x to available digits; adversarial substitution exposed it.
The full C5--Cq slack tends to `0.80092867...`, so a proof still needs a
global phase-sum estimate, not just control of the bound state.

For finite odd q, the positive outlier equation also becomes algebraic after
`x=r+r^{-1}`. Removing the trivial `r^q-1` factor gives a relation linear in
`r^q`, equivalently

`r^q=(r^8-r^7+r^4-2r^3+2r^2+r-1)/`
`(r^8-r^7-2r^6+2r^5-r^4+r-1)`.

This supplies a route to rigorous monotonicity of the outlier toward
`r=3^(1/5)`: prove the rational function's sign/monotonicity for r>1 and
compare intersections with r^q. It also gives a compact exact certificate for
the bound state without constructing a degree-(q+5) characteristic polynomial.

The required monotonicity is unusually clean: differentiating that rational
function gives numerator

`-4r(r-1)^2(r^10+2r^8+2r^6+5r^5+2r^4+2r^2+1)`,

strictly negative for r>1 wherever the denominator is nonzero. Thus the right
side decreases while r^q increases, proving uniqueness of the positive bound
state on each admissible branch. This should make comparison with the limiting
root r=3^(1/5) a sign check rather than a root-isolation problem.

Correction to that last comparison target: the limiting r is the pole of the
rational function, i.e. the >1 zero of A(r), not `3^(1/5)`. Exact signs
`A(5/3)<0<A(17/10)` bracket it in `(5/3,17/10)`. For finite q the solution is
to the right of this pole and decreases toward it, matching q=3,5,... data.
The monotonicity calculation remains valid; only the mistakenly identified
limit was replaced.

Moreover the finite positive outliers decrease strictly with odd q. On the
right of the pole, `R(r)=B(r)/A(r)` decreases from infinity while `r^q`
increases. If `r_q^q=R(r_q)`, then
`r_q^(q+2)>R(r_q)`, whereas immediately right of the pole R dominates;
uniqueness forces `r_{q+2}<r_q`. Therefore their eigenvalues
`r_q+r_q^{-1}` also decrease to the certified algebraic limit.

The total C5--Cq slack itself is not monotone: it oscillates by q mod 4 around
its limit. For q=1 mod 4 it increases from q=5 toward the limit; for q=3 mod 4
it decreases from q=7 toward it. The global minimum in q<=33 is q=5. This
mirrors the alternating cycle baseline exactly and suggests proving two
separate monotone subsequences after subtracting the explicit
`+/- (sec(pi/q)-1)` cycle term.

After subtracting that cycle term, define the bridge gain
`g_q=s^+(C5--Cq)-s^+(Cq)-5`. Numerically `g_q` still alternates but is already
bounded between 0.7822 and 0.8300 for q=5..33 and converges to 0.80092867.
Thus a considerably weaker uniform estimate `g_q>0` proves the family; exact
monotonicity is unnecessary. A possible route is to lower-bound the positive
outlier by its algebraic limit and show the positive band sector contributes
more than `5-x_infinity^2`, about -0.16382 relative to its retained roots.

Recomputing this decomposition carefully gives something stronger. Remove the
persistent positive golden-ratio root from the band spectrum. Relative to all
positive roots of Cq, the remaining positive band roots contribute a *positive*
square gain: 0.1452 at q=5 and between 0.185 and 0.256 through q=33. The
positive outlier alone contributes `x_q^2-5>0.1638188`. Thus the bridge gain
above was understated because the second persistent golden root also supplies
`((sqrt(5)-1)/2)^2=(3-sqrt(5))/2=0.381966...`. A proof can aim at the simpler
statement that the moving positive band square sum does not decrease relative
to Cq; together with the persistent root and outlier this gives a margin over
five immediately.

Exact inertia of the reduced polynomial follows a stable pattern: for
q=1 mod 4 it is `(q+5)/2` positive and `(q+1)/2` negative; for q=3 mod 4 the
counts are equal `(q+3)/2`. Restoring the persistent factor adds one positive
and one negative root. In particular, the moving band contains exactly one
more positive root than Cq after the persistent positive root is removed.
That extra root explains why coordinatewise interlacing is the wrong target;
a majorization or phase-sum inequality should use the additional positive
degree of freedom.

At x=0 the reduced polynomial is exactly -3 for q=1 mod 4 and -5 for
q=3 mod 4 (verified symbolically through q=21 and immediate from the
Chebyshev values at zero). Combined with the one-positive/one-negative
outliers and simple-root interlacing in the band, this gives a promising
elementary route to formalizing the inertia pattern without full Sturm chains.

Root-by-root comparison reveals a stronger persistence pattern. Besides the
C5 golden root, one copy of every double Cq eigenvalue survives unchanged
(the antisymmetric eigenvector vanishing at the root). After removing those,
the moving positive sector has one extra root and interlaces the retained Cq
positive roots. Examples show the perturbation losses occur only near the top
of each interlacing interval, while inserted roots repay them. The natural
unit is therefore each adjacent pair, not global majorization: prove that the
sum of squares of the inserted root and shifted root exceeds the two copies of
the corresponding Cq root. Direct values support this except that endpoint
pairs must be grouped with their neighbor.

Factoring out the retained Cq sector produces a degree `(q+7)/2` symmetric-
sector polynomial S_q. Newton sums are strikingly rigid:
`sum roots(S_q)=2` and `sum roots(S_q)^2=q+11` exactly (checked symbolically
for q=5..17 and derivable from the first two coefficients). Hence its total
square energy is already explicit; proving the positive-sector comparison is
equivalent to an upper bound on the negative square energy of S_q. Since S_q
has one positive outlier and one negative outlier, the problem may be cleaner
on the negative side via the analogous monotone bound-state equation.

That negative bound state increases in magnitude with q and tends to
`-2.189273...`. Writing the limiting eigenvalue as `x=-(r+r^{-1})`, r>1,
its exact equation is

`r^8+r^7-2r^6-2r^5-r^4-r-1=0`.

The positive and negative outliers therefore move in opposite monotone
directions. Since the symmetric sector has fixed total square sum q+11, an
upper bound on its negative band plus this negative outlier is exactly a lower
bound on the desired positive band plus positive outlier. The next step is to
derive the negative-band phase equation and compare it to the retained Cq
negative roots.

Two more exact Newton sums emerge from the leading coefficients of S_q:

`sum lambda^3=8`, and `sum lambda^4=3q+49`.

So the first four spectral moments of the moving symmetric sector are affine
or constant in q: `(2, q+11, 8, 3q+49)`. These equal closed-walk counts of a
fixed C5 defect attached to the rooted symmetric cycle sector. The constant
odd moments quantify spectral asymmetry and may bound the positive/negative
square split through a moment optimization problem with support constraints
[-x_-,x_+].

A discretized linear program for a quartic polynomial minorant of
`max(x,0)^2` on the certified spectral support gives strong bounds using only
these four moments: for q=5 the optimized moment lower bound is 9.608 versus
the actual symmetric-sector s+ of 9.830, and for q=101 it gives 55.027. This
is enough in scale to prove the desired family if converted to a rational
polynomial whose two nonnegativity conditions factor or admit Sturm
certificates. This moment-dual route avoids summing phase shifts root by root.

Higher Newton sums continue the pattern through degree eight:
`p5=37`, `p6=10q+236`, `p7=177`, `p8=35q+1169` (here pk means the kth
power sum, not a cycle polynomial). Every even moment is affine in q and every
odd moment is constant. A degree-eight polynomial minorant therefore has enough
freedom to produce a q-uniform coefficient above the roughly q/2 threshold;
the first quartic trial had slope 0.469 and eventually fails, so the next LP
must optimize worst-case slope and intercept jointly rather than at q=5.

The degree-eight dual optimized directly for asymptotic slope reaches
`0.4963995`, still below the required coefficient 1/2, although its intercept
is generous. This is informative failure: fixed low-degree moment bounds lose
a small amount to approximating the kink of `max(x,0)^2` at zero. Increasing
degree should converge to slope 1/2, but a finite rational certificate must
balance the slope deficit against its intercept and then exact-check only the
remaining finite q range.

Using the safe cycle bound `s^+(Cq)>=q-1/4`, the symmetric-sector target is
only `S_q^+ >= q/2+sqrt(5)/2+45/8`. The numerical degree-eight dual has bound
`0.4963995q+7.3069`, which beats this target through about q=156 despite its
slight slope deficit. Therefore one rational degree-eight minorant plus exact
finite certificates up to q=157 would already prove a substantial infinite
range only if supplemented by a higher-degree asymptotic certificate; or,
conversely, a degree around 16 may push the crossover far enough that an
analytic tail estimate becomes easy.

Moments through degree 16 are now explicit:
`p9=872`, `p10=126q+5861`, `p11=4413`,
`p12=462q+29548`, `p13=22817`, `p14=1716q+149349`,
`p15=119788`, `p16=6435q+755809`.
The even-moment slopes are `1,3,10,35,126,462,1716,6435`, namely
`binomial(2k-1,k-1)` for moment 2k. LP minorant slopes converge rapidly:
degree 8,10,12,14,16 give 0.4963995, 0.4978230, 0.4988487, 0.4991809,
0.4994902. This confirms the moment measure's bulk limit and makes a
high-degree finite-range certificate practical, though exact rationalization
and interval nonnegativity remain.

The slope sequence is exactly half the central binomial coefficient:
`binomial(2k,k)/2`. These are the positive-half moments of the arcsine spectral
measure of the infinite path. Hence the coefficient 1/2 is not merely an LP
limit: it is exactly the bulk positive square energy per cycle vertex. The
whole C5--Cq problem is a finite defect term. A cleaner proof should subtract
the cycle bulk measure first and bound only the q-independent moment intercepts,
rather than approximate the kink uniformly with a polynomial whose slope is
necessarily below 1/2.

An extraction pass initially subtracted the Cq Perron root as retained, but
the retained factor R has `p_q=(x-2)R^2` and does not contain x=2. Correcting
that exact factor-of-four error gives the symmetric-sector defect
`D_q=S_q^+-q/2` as 7.41421, 7.41764, 7.41861, 7.41887, 7.41894,
7.41896 for q=21,41,81,161,321,641. It converges from below to about
7.418962..., safely above the required constant
`sqrt(5)/2+45/8=6.743...`. The target formula is therefore consistent; the
moment route has asymptotic margin about 0.676.

The exact decomposition is now clean. If
`s^+(Cq)=q+delta_q`, then the retained R-sector contributes
`(q+delta_q-4)/2`, the persistent C5 factor contributes
`g=(3-sqrt(5))/2`, and S_q contributes `q/2+D_q`. Therefore the desired
inequality is precisely

`D_q >= 7-g-delta_q/2`.

The worst cycle deficit occurs at q=5, giving the uniform sufficient target
`D_q >= sqrt(5)+9/2 = 6.7360679...`. Numerically D_5 itself is about 7.32994
and the limit is 7.41896, leaving a robust margin. This is the correct defect
constant for rational moment certification.

The degree-16 dual has the form
`S_q^+ >= 0.49949017 q+7.11173`, so after subtracting q/2 its defect bound
stays above the uniform target through approximately q=736. This is already a
finite exact-certification strategy for every odd q<=735 once the numerical
polynomial is rationalized and its minorant property Sturm-certified. It does
not settle the infinite tail; that requires either increasing degree with q or
an analytic defect-limit error bound. The latter is preferable because the
observed D_q approaches its limit at O(q^-2), with margin about 0.68.

Separate large-q fits confirm the congruence oscillation explicitly:

- q=1 mod 4: `D_q = D_inf - 2.41049/q^2 + O(q^-4)`;
- q=3 mod 4: `D_q = D_inf + 1.95710/q^2 + O(q^-4)`;

with `D_inf=7.4189626...`. Thus the lower subsequence is q=1 mod 4 and rises
toward the limit; proving a coarse error bound such as
`D_q>D_inf-3/q^2` for q>=737 would finish the tail with enormous margin.
This points back to Euler-Maclaurin on the phase-shifted band sum, but now only
a crude remainder is needed.

The uniform target itself is exact: for q=1 mod 4,
`-delta_q=sec(pi/q)-1` decreases with q and is maximized at q=5, where it is
`sqrt(5)-2`; for q=3 mod 4, delta_q is positive and only lowers the target.
Thus no slack was lost in replacing the cycle term by
`D_q>=sqrt(5)+9/2`. Any valid defect lower bound above 6.737 closes all q at
once.

Since `p2(S_q)=q+11`, the defect has the exact imbalance form

`D_q=11/2 + (1/2) sum_{lambda in S_q} lambda|lambda|`.

Therefore the entire C5--Cq theorem reduces to the q-independent inequality

`sum lambda|lambda| >= 2sqrt(5)-2 = 2.4721359...`.

Numerically this signed-square imbalance tends to about 3.837925. This is a
much cleaner statement than the positive-energy target and aligns with the
constant odd moments `p1=2,p3=8,p5=37,...`; a direct inequality between
`sum lambda|lambda|` and the first few odd moments may finish the proof.

A naive global odd-polynomial minorant cannot work: near zero,
`x|x|` has opposite quadratic signs on the two sides, while any nonzero odd
polynomial has a linear or odd leading term and violates one side. Numerical
LPs correctly report infeasibility even through degree seven. Any moment proof
must therefore include an even polynomial component (the earlier positive-part
minorant), exclude a certified zero-free gap, or split positive and negative
supports using the inertia/interlacing information.

There is no q-uniform spectral gap at zero: the smallest absolute S_q root is
positive and about `2/q` for q=1 mod 4, while for q=3 mod 4 it is negative and
about `4/q`. Exact constant/linear coefficients show the local Newton estimate:
S_q(0) cycles through `3,5,-3,-5`, and for q=1 mod 4 the tangent root estimate
is exactly `3/(q+10)` (examples 3/14,3/18,3/22,... after indexing), matching
the observed O(1/q) root. Therefore a gap-based polynomial certificate cannot
be uniform; the near-zero root must be treated explicitly or absorbed into an
O(q^-2) tail remainder.

More precisely the local coefficients split by q mod 8. For q=1 mod 8,
`S(0)=-3, S'(0)=(5q-7)/4`; for q=5 mod 8,
`S(0)=3, S'(0)=-(5q+31)/4`. The other two classes have S(0)=+/-5 and
linear derivatives of smaller magnitude. These exact formulas provide the
leading near-zero root and explain the two different q^-2 defect corrections.
They are also the data needed to subtract one explicit local root before using
a gap-based polynomial minorant on the remainder.

A direct high-precision scan of the correctly normalized defect through every
odd q<=301 finds the global minimum `D_5=7.3299417287...`; all later values
remain above it. Since the exact uniform target is 6.7361, even proving the
coarse universal bound `D_q>=7` would suffice. This suggests simplifying the
moment dual objective to a constant defect 7 rather than approximating the
optimal 7.42 limit.
