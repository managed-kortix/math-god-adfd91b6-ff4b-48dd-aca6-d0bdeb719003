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
