# Two C5 Blocks Joined by a Bridge, with Arbitrary Trees

This directory contains a self-contained LaTeX proof for the bicyclic cactus
whose core is two vertex-disjoint copies of `C5` joined by exactly one bridge
edge. Arbitrary rooted trees may be attached at any of the ten core vertices.

## Result

If `H` is the bare ten-vertex bridge core and `n = |V(G)|`, then

```text
s+(G) >= n + s+(H) - 10 > n,
s+(H) = (31 + sqrt(13))/2 - sqrt(5) - rho^2,
```

where `rho` is the unique root in `(2, sqrt(5))` of

```text
rho^3 - 4 rho - 1 = 0.
```

The minus sign before `1` is necessary. The characteristic polynomial has
the factor `x^3 - 4x + 1`; its negative root is `-rho`, so substituting
`x = -rho` gives `rho^3 - 4rho - 1 = 0`. The cubic factor itself has no root
in `(2, sqrt(5))`. This resolves the sign inconsistency in the source note.

## Proof outline

- Rooted-tree matching messages satisfy `m = t + sum(1/m_child) >= t`.
  Eliminating all branches leaves core activities `a_v = t + y_v`, with
  `y_v >= 0`, and a common positive factor `K` in every Sachs carrier.
- For the two rooted pentagons, let `p,s` be the deleted-root matching
  partitions and `q,r` the full partitions. The exact normalized formula is
  `Psi/K = (qr + ps - 4) + 2i(q + r)`.
- For the bare core, `P0 = t^4 + 3t^2 + 1` and
  `Q0 = t^5 + 5t^3 + 5t`. Its phase is the upper-half-plane value
  `atan2(4Q0, Q0^2 + P0^2 - 4)`, not an ordinary one-argument arctangent.
- Exact integer expansion proves the angular cross product
  `Y0 X - Y X0 >= 0`. It has 4891 positive nonconstant terms and vanishes at
  the bare specialization, hence `Theta_G(t) <= Theta_H(t)` pointwise.
- The signed Coulson identity converts phase comparison into square-energy
  comparison. Factoring the bare characteristic polynomial gives the exact
  value of `s+(H)`, and the exact interval `2 < rho < sqrt(5)` proves the
  strict slack without relying on decimals.

## Files and verification

- `paper.tex` - complete manuscript and reproducibility appendix
- `../positive-square-energy/experiments/c5_bridge_phase_certificate.py` -
  exact SymPy certificate and bare-core factorization check

From the repository root, run:

```bash
python positive-square-energy/experiments/c5_bridge_phase_certificate.py
```

Expected coefficient-certificate summary:

```text
PASS two-C5 bridge phase coefficient certificate
terms=4891 min_coefficient=1 max_coefficient=289
y_constant=0 all_nonconstant_coefficients_positive=True
sha256=365e18dedf9032fbcdb88af83d033f0651f02412c796b4f1dfde04152a478af1
```

The SHA-256 value is the digest of the canonical ordered coefficient stream.
The generated manuscript is included as `paper.pdf`.
