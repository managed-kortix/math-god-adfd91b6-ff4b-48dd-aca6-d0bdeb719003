# Exact rank-(1,6) bridge-gain finite scout — corrected final packet

This packet is **FINITE_ONLY**: a finite computational scout, not a universal
theorem.  For a one-bridge join `G=U--R`, it studies

- `sigma(X)=s+(X)-|V(X)|`;
- `Gamma=s+(G)-s+(U)-s+(R)`;
- `F=Gamma+sigma(R)-(sqrt(5)-2)`.

A negative `F` would refute only the sufficient worst-`C5` payment route.  A
negative `sigma(G)` would be a rank-seven counterexample.  The exact Atlas
census has positive exact lower enclosures for every stored per-profile
extremum.  The kernel and filtered unit-star scans persist
numerical no-negative counts, with exact receipts for selected/extremal rows.
The structured slice persists only a numerical no-negative `sigma(G)` count
and does not compute `F`.

## Authoritative replay

Install the pinned Python dependencies from `requirements.txt`, then run:

```bash
python final_verify.py
python -O final_verify.py
```

The two outputs are required to be byte-identical.  `final_verify.py`
re-enumerates the Atlas rooted-side census and eligibility, then exactly
replays the nine stored Atlas extremal graphs.  It reconstructs physical-bridge
eligibility for persisted unit-star extrema/certificate graphs, authenticates
the kernel fixture and its persisted extrema, and exact-replays the listed
characteristic-polynomial/Sturm receipts.  It does **not** independently
evaluate all 14,916 Atlas joins, regenerate and evaluate all 100,401 unit-star
rows, or numerically recompute or Sturm-replay all 515,070 kernel joins.  Those
full-slice no-negative counts remain outputs of the pinned numerical census
scripts; only the stated selected/extremal records are independently exact-
certified here.  `FINAL-MANIFEST.sha256` covers every nonempty top-level final
artifact except itself (avoiding a self-hash paradox).

## Search result

The persisted numerical census reports nonnegative `sigma(G)` in all four
slices and nonnegative `F` in the Atlas, kernel, and unit-star slices; the
structured scan does not compute `F`.  These broad all-row statements are
numerical census data; exact Sturm receipts cover only the stated
selected/extremal rows.  This is finite discovery, not a universal theorem,
and `final_verify.py` does not independently replay all-row spectral
comparisons in any slice.

## Four scopes — do not merge them

### A. Exhaustive Graph Atlas slice

`atlas-exact-exhaustive-minima.json` covers exactly:

- every connected hostile unicyclic `U` in the NetworkX Graph Atlas (therefore
  order at most seven) and every vertex-automorphism orbit: **22 rooted U**;
- every connected rank-six `R` in the Atlas and every vertex-automorphism
  orbit: **678 rooted R**;
- all **22 x 678 = 14,916** one-bridge joins.

Only profiles `(6)`, `(5,1)`, and `(3,3)` occur.  The verifier independently
enumerates the complete side/root census and checks exact hostility and that
all 678 rooted complements become actual unit-star hulls after the external
rank-one arm is attached: every physical bridge induces only `0|7` or `1|6`.
These are minima selected by the exhaustive finite Atlas scan, with the nine
stored extremal values exact-replayed using integer characteristic polynomials
and rational Sturm enclosures.  The verifier does not exactly compare every one
of the 14,916 joins, so the receipts prove the named values and signs, while
their within-Atlas minimality remains a persisted exhaustive numerical-census
result.

### B. Authenticated canonical-shortest kernel slice

`kernel-results.json` covers the authenticated fixture of **1,198** loopless
2-connected rank-six multigraph kernels (orders 2--10, fixture SHA-256
`5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476`).
For each kernel it uses only its canonical shortest simple realization (one
direct path in each parallel class, all other paths of length two), every
labelled complement port, and the 45 listed rooted hostile `C5` star/path arms:
**515,070 joins**.  This is not exhaustive over path lengths/parities or all
tree payloads.  The JSON records persisted numerical minimum candidates.
`exact-scan-certificates.json` directly certifies the named kernel `sigma(G)`
and `F` candidates.  The named kernel `Gamma` candidate is the same graph up
to isomorphism as the graph certified by the `Gamma` record in
`correct-global-unit-star-gamma-sigmaG-certificates.json`; `final_verify.py`
does not directly bind that isomorphism.  These receipts prove the named
values and signs, not minimality against every scanned row.

### C. Generated common-center unit-star slice

The corrected `unit_star_scan.py` generates **100,401** rows, then reconstructs
the bridge-free-component quotient from adjacency and retains exactly
**90,013** rows whose every physical bridge cut is `0|7` or `1|6`.
`unit-star-results.json` is the corrected filtered result.

The original scout incorrectly marked all generated rows eligible even when an
Atlas center contained an internal bridge producing (for example) a `2|5`
cut.  That statement is retracted.  In particular, merely attaching a hostile
arm to an arbitrary rank-six graph does **not** make an actual unit-star hull.
The corrected exact per-profile `F` receipts are in
`unit-star-exact-certificates.json`; the old ineligible `(2,1,1,1,1)` receipt
has been replaced.  `correct-global-unit-star-gamma-sigmaG-certificates.json`
contains exact receipts for the corrected `sigma(G)` and `Gamma` persisted
numerical minimum candidates **within this stated generated family**.  The
receipts prove the named graphs' values and signs, not minimality against every
generated row; the numerical census reports that within-family minimality
only.

Nine profiles occur here: `(1^6)`, `(2,1^4)`, `(2,2,1,1)`, `(3,1,1,1)`,
`(3,2,1)`, `(3,3)`, `(4,1,1)`, `(5,1)`, `(6)`.  Absence of `(4,2)` and
`(2,2,2)` is only a center/order limitation, not a mathematical exclusion.

### D. Sparse structured discovery slice

`structured_scan.py` is deliberately nonexhaustive.  It uses selected
cycle/star/path payloads, four named rank-six cores, and exactly **12 random
`tree + 6 non-tree edges` samples at each of n=6,7,8,10,12** (two sampled
ports where possible).  The earlier phrase “100k/order through n=13” was
false and is retracted.  Its persisted scope and counts are in
`structured-results.json`.  Numerical values in this slice are discovery data,
not exact global minima.

## Legacy discovery files

`search.py`, `profile_scan.py`, and their JSON outputs are retained to make the
search trajectory reproducible.  They are nonexhaustive outside their explicit
Atlas portions and are not theorem evidence.  `certify.py` and the `*_certify`
scripts generate exact receipts for selected candidates only.  The
`final_verify.py` report is authoritative for all claims made by this README.

## Exact-certificate boundary

Floating-point eigensolvers perform and order the broad numerical scans; their
aggregate no-negative counts are numerical census evidence.  Atlas hostile-
side membership is decided by exact Sturm intervals.  Exact receipts use
integer adjacency matrices, exact characteristic polynomials, square-free
factorization, exact Sturm root counts, and outward rational interval
arithmetic; decimal fields are renderings of rational endpoints.  They certify
only the listed selected/extremal graphs and inequalities.  `final_verify.py`
does not turn the complete numerical census into an all-row exact proof.  Even
for the complete Atlas input slice, it does not exactly compare all 14,916
spectral rows, so within-slice minimality remains persisted exhaustive
numerical-census data.
