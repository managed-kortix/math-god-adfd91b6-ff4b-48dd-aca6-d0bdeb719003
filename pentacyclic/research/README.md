# Order-five rank-five experiment

`order5-tetra-census-experiment.py` independently extracts the 24 order-five
kernels from the digest-locked rank-five classification, reconstructs all 6282
physical rows and 4238 genuine automorphism orbits, and exactly recomputes the
regular-tetrahedron sieve. It leaves 208 residual orbits.

Exactly one residual key is separated from the requested search ledger: the
all-odd simple complete-minus-one-edge target. The artifact makes no claim for
that target. The remaining search ledger therefore has 207 canonical targets.
For an all-length proof, each canonical target would additionally require all
nine one-coordinate length-plus-two frontier targets, because every order-five
rank-five kernel has nine paths. The complete all-length covering set would
therefore contain `207 * (1+9) = 2070` exact targets.

No rational Gram certificate fixture is frozen here. The exploratory planar
search did not complete exact certificates for every canonical target, much
less every required coordinate frontier. The generated JSON therefore carries
`certificate_fixture_frozen=false`, and the verifier rejects promotion of that
field.

`order5-dim4-rational-gram-search.py` replaces that planar experiment by
Riemannian optimization of five unit vectors in dimension four, followed by
rational stereographic reconstruction of every branch and internal path vector.
The complete 2070-target run in `order5-dim4-rational-gram-results.json` gives
2062 strict exact certificates. The eight remaining optimized obstructions are
four targets of kernel 22 and four equality-limit targets of kernel 35. They
form eight labeled length archetypes under unrestricted vertex relabeling.
The completed theorem artifact now closes those eight targets separately:
kernel 35 has four exact symbolic equality certificates and kernel 22 has four
structural attached-`K4` closures. For K22 the verifier reconstructs the
physical paths, deletes the induced tree at branch 0 with every rooted tree
owned there or at an ear internal vertex, and checks that the complement is an
actual attached `K4`. The source-locked deterministic fixture and
standalone verifier are `order5-kernel-family-theorem.json` and
`order5-kernel-family-theorem-verifier.py`. They prove every order-five
kernel/parity family except the explicitly separated all-odd `K5-e` orbit.

The separated orbit is closed by the disjunctive DNN-or-structural theorem in
`all-odd-k5e-theorem.json` and `all-odd-k5e-theorem-verifier.py`. Its 142
residual states form 16 orbits under the full `S_3 x S_2` automorphism group
and have exact rational certificates; the remaining states close by either the
simplex DNN certificate or an induced actual-`K4`/favorable-theta territory
packet. The paper records all stereographic parameters and reduced costs. No
universal DNN excess-four claim is made for all-odd `K5-e`.

Run:

```text
python3 pentacyclic/research/order5-tetra-census-experiment.py
python3 -O pentacyclic/research/order5-tetra-census-experiment.py
python3 pentacyclic/research/order5-dim4-rational-gram-search.py --progress
python3 pentacyclic/research/order5-kernel-family-theorem-verifier.py
python3 -O pentacyclic/research/order5-kernel-family-theorem-verifier.py
python3 pentacyclic/research/all-odd-k5e-theorem-verifier.py
python3 -O pentacyclic/research/all-odd-k5e-theorem-verifier.py
```

## Complete order-six theorem

`order6-tetra-census-experiment.py` independently reconstructs the 38
order-six kernels, 23,208 physical rows, and 12,810 automorphism orbits. The
exact regular-tetrahedron sieve certifies 11,312 orbits and leaves 1,498
residuals. Every kernel has ten paths, so the canonical-plus-ten-coordinate
frontier has 16,478 targets.

`order6-dim6-rational-gram-experiment.py` deterministically optimizes six unit
vectors in dimension six and exactifies accepted witnesses with rational
stereographic parameters and `Fraction` arithmetic. Its frozen raw output
contains 16,451 strict exact certificates. The 27 raw-search failures split
exactly into 18 symbolic equality certificates in kernels 55 and 61 and nine
structural triangle-plus-attached-`K4` closures in kernel 71. Thus all 16,478
frontier targets, and by fixed-parity monotonicity every longer subdivision,
are proved.

The experiment artifacts remain honestly labeled `full_theorem=false`; theorem
promotion occurs only in `order6-kernel-family-theorem.json`. The standalone
`order6-kernel-family-theorem-verifier.py` locks the raw result SHA-256,
independently rebuilds all 16,478 target keys from the 1,498 census residuals,
rejects duplicates, omissions, and extras, checks the exact nine-key missing
sets in each of K55/K61/K71, and verifies every certificate. It checks symbolic
Gram PSD and exact path costs, and reconstructs each K71 physical graph,
favorable triangle, actual `K4`, owner-exact rooted-tree partition, and rooted
descendants. The paper note is
`positive-square-energy/pentacyclic-general/order-six-kernel-family-theorem.md`.

Run:

```text
python3 pentacyclic/research/order6-tetra-census-experiment.py
python3 pentacyclic/research/order6-dim6-rational-gram-experiment.py --verify pentacyclic/research/order6-dim6-rational-gram-results.json
python3 pentacyclic/research/order6-experiment-verifier.py
python3 pentacyclic/research/order6-kernel-family-theorem-verifier.py
python3 -O pentacyclic/research/order6-kernel-family-theorem-verifier.py
```

## Complete order-seven theorem

`order7-tetra-census-experiment.py` independently reconstructs the exact 23
order-seven kernels. It finds 31,112 physical rows and 18,026 automorphism
orbits; the regular-tetrahedron sieve certifies 14,306 and leaves 3,720
residuals. Every kernel has eleven paths, so canonical plus all eleven
one-coordinate length-plus-two frontiers gives 44,640 exact targets.

`order7-dim7-rational-gram-experiment.py` accepts witnesses only after rational
stereographic reconstruction and exact `Fraction` verification. Its frozen raw
output certifies 44,616 targets and leaves 24 equality limits, all in K80: six
parity rows at each of canonical and path coordinates 0, 3, and 6.

`order7-kernel-family-theorem.json` closes those 24 keys with exact
cycle-support Gram certificates. The sign-switch construction covers all six
parity rows, and lengthening coordinates 0, 3, or 6 preserves their zero path
cost. The theorem verifier reconstructs all 44,640 keys, checks every rational
certificate, every principal minor and path cost in all 24 symbolic records,
and the complete one-coordinate descendant cover. It digest-locks the raw
kernel, census, results, and theorem fixture, and rejects normal and `-O`
hostile mutations. The paper note is
`positive-square-energy/pentacyclic-general/order-seven-kernel-family-theorem.md`.

The raw artifacts remain honestly labeled `full_theorem=false`; theorem
promotion occurs only in the separate theorem fixture and verifier.

Run:

```text
python3 pentacyclic/research/order7-tetra-census-experiment.py
python3 pentacyclic/research/order7-dim7-rational-gram-experiment.py --verify pentacyclic/research/order7-dim7-rational-gram-results.json
python3 pentacyclic/research/order7-experiment-verifier.py
python3 -O pentacyclic/research/order7-experiment-verifier.py
python3 pentacyclic/research/order7-kernel-family-theorem-verifier.py
python3 -O pentacyclic/research/order7-kernel-family-theorem-verifier.py
```

## Complete order-eight theorem

`order8-cubic-tetra-census-experiment.py` extracts exactly the 16 order-eight
cubic kernels (fixture rows 103--118), reconstructs 46,736 physical parity
rows and 11,188 automorphism orbits, and applies the exact tetrahedral sieve.
It certifies 7,705 orbits and leaves 3,483 residuals. Each cubic kernel has 12
paths, so the canonical-plus-twelve-coordinate ledger has 45,279 targets. The
artifact also marks the unique row-118 all-support cycle equality residual.

`order8-dim8-rational-canonical-frontiers-experiment.py` searched those targets
with eight-dimensional branch vectors and accepted only exact rational
stereographic reconstructions. Four source-locked chunks contain 45,249 strict
rational certificates and 30 unresolved keys. The unresolved set is exactly
six K118 rows at canonical and path frontiers `0,5,6,11`.

`order8-kernel-family-theorem.json` is a compact theorem fixture: it does not
duplicate the roughly 67 MB of rational records, but stores the 30 exact signed
cycle closures and locks all four chunks. Its verifier derives all 45,279 keys
from the census, checks each chunk slice, verifies every rational `Fraction`
witness, checks every principal minor and path cost for all 30 K118 records,
and audits all-length coverage and arbitrary rooted-tree attachments. It also
rejects ten hostile mutations and enforces identical normal and `-O` output.

The raw census and chunks remain honestly labeled `full_theorem=false`;
promotion occurs only in the separate deterministic theorem fixture. The paper
note is `positive-square-energy/pentacyclic-general/order-eight-kernel-family-theorem.md`.

Run the exact census and a bounded search slice with:

```text
python3 pentacyclic/research/order8-cubic-tetra-census-experiment.py
python3 -O pentacyclic/research/order8-cubic-tetra-census-experiment.py
python3 pentacyclic/research/order8-kernel-family-theorem-verifier.py
python3 -O pentacyclic/research/order8-kernel-family-theorem-verifier.py
python3 research/rank-five-order2-8-master-verifier.py
python3 -O research/rank-five-order2-8-master-verifier.py
```

The implication master composes the independently regenerated exact census
with every order-two-through-eight theorem owner. Its theorem note is
`positive-square-energy/pentacyclic-general/rank-five-order2-8-master-theorem.md`.
This closes all 118 single rank-five suppressed-kernel families after arbitrary
simple subdivisions and rooted-tree attachments; it does not claim the
connected pentacyclic multiblock cases.
