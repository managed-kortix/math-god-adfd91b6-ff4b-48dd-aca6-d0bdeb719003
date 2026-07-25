# Two-C5 Bouquet with Arbitrary Trees

This directory contains a self-contained LaTeX manuscript proving a positive
square-energy bound for one specific bicyclic cactus family.

## Result

Let `G` be a connected cactus whose only cyclic blocks are two copies of
`C5` that share exactly one vertex. Arbitrary trees may be attached at any of
the nine core vertices. If `n = |V(G)|`, the manuscript proves

```text
s+(G) >= n + 1 - 4/(3 sqrt(13)) > n.
```

This is the shared-vertex bouquet case only. It does not include two cycles
joined by a bridge or path, and it does not claim a theorem for every
bicyclic cactus. The constant is an explicit proved lower bound, not a claimed
optimal spectral constant: although the coefficient inequality is an equality
for bare-core activities, the later estimate `atan(u) <= u` is strict.

## Proof structure

- The signless matching partition and grouped Sachs expansion normalize the
  characteristic polynomial on the imaginary axis.
- Exact rooted-tree belief propagation gives messages
  `q = t + sum 1/q_child >= t`, effective core activities `a_v >= t`, and a
  common positive factor that remains valid when a full cycle is deleted.
- Weighted `P4` and root-matched formulas give
  `R = a0 A1 A2 + B1 A2 + A1 B2` and
  `Psi = K [R + 2i(A1 + A2)]`. There is no double-cycle Sachs term because
  the two cycles share their root.
- An exact coefficientwise certificate proves
  `2R >= t(t^4 + 7t^2 + 9)(A1 + A2)` for all effective activities.
- The first-quadrant phase, `atan(u) <= u`, the exact integral
  `2 pi/(3 sqrt(13))`, and the signed Coulson identity yield the result.

## Files and verification

- `paper.tex` - manuscript, bibliography, and reproducibility appendix
- `../positive-square-energy/experiments/c5_bouquet_matching_certificate.py`
  - exact SymPy certificate over the integers

Run the certificate from `/workspace`:

```bash
python positive-square-energy/experiments/c5_bouquet_matching_certificate.py
```

Expected summary:

```text
PASS two-C5 bouquet matching coefficient certificate
terms=1290 min_coefficient=1 max_coefficient=22
y_constant=0 all_coefficients_nonnegative=True
sha256=4c436cac772395d2a8edfdd81408ffe426759d3e94d66df2e4ab0235a3343110
```

The digest is for the canonical ordered coefficient stream. The certificate
script used by the manuscript has file SHA-256
`b3936c0d08ae252bdc11689ab55eb60331f0c54481f4544e442a98e5002fe6cf`.

No build artifacts are included.
