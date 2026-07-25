# Two C5 Blocks Joined by Any Positive-Length Path

This directory contains a self-contained proof for connected cacti whose only
cyclic blocks are two vertex-disjoint copies of `C5`. The cycles may be joined
by a bridge or by any longer path, and arbitrary trees may be attached at any
cycle or connector vertex.

## Result

For `n = |V(G)|`, the paper proves

```text
s+(G) > n + 5 - 2 sqrt(5) > n.
```

The shared-vertex bouquet is excluded: it is a separate theorem, not the
zero-length instance of this result.

## Proof strategy

- Normalize the characteristic polynomial as
  `Psi_H(t) = i^(-|V(H)|) det(itI - A(H))` and use the grouped Sachs expansion.
- Keep the two actual `C5`-unicyclic lobes `X1` and `X2`, including every tree
  attached at their cycle vertices. Belief propagation eliminates only the
  connector-internal branches, producing positive activities `a_j` and a
  common positive factor `B0`.
- Set `z_i = Psi_Xi`, `w_i = Psi_(Xi-root)`, and `r_i = w_i/z_i`. Then `z_i`
  is in the first quadrant, `w_i > 0`, and `r_i` is in the fourth quadrant.
- The exact normalized connector factor is

  ```text
  m = 0:  F = 1 + r1 r2
  m = 1:  F = a1 + r1 + r2
  m >= 2: F = K(a1+r1, a2, ..., am+r2),
  ```

  where `m` is the number of internal connector vertices and `K` is the path
  continuant. Expanding `F = A + B r1 + C r2 + D r1 r2` proves `Im F < 0`.
- The whole grouped Sachs expansion lies in the upper half-plane. A branch
  argument therefore gives
  `0 < Theta_G < Theta_X1 + Theta_X2`, and signed Coulson integration yields
  `D(G) > D(X1) + D(X2)` for `D = s+ - s-`.
- A weighted-cycle/product-subpartition argument proves
  `D(X_i) >= D(C5) = 4 - 2 sqrt(5)`. Since the graph has `n + 1` edges, the
  claimed bound follows.

## Important distinction

The proof does **not** compare the attached graph pointwise with the bare
two-pentagon core. Attachments can increase the bare-core phase. The valid
comparison is between the joined phase and the sum of the phases of its actual
two unicyclic lobes.

## Files

- `paper.tex` - complete proof
- `../positive-square-energy/experiments/connector_factor_audit.py` - finite exact
  corroborative audit of the connector identities (not needed by the proof)

The generated manuscript is included as `paper.pdf`. The paper proves the
strict lower bound for each finite graph.
