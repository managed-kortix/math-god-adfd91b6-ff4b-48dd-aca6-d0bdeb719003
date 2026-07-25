# Triangle--One-Mod-Four Bicyclic Cacti

This directory contains a self-contained LaTeX proof for the full mixed
residual family of the sharp cactus DNN analysis.

## Result

Let `G` be a connected bicyclic cactus whose cyclic blocks are `C3` and
`Cq`, where `q = 4k + 1 >= 5`. The cycles may share an arbitrary cut vertex,
or they may be vertex-disjoint and joined by a path of arbitrary length.
Arbitrary trees may be attached at arbitrary vertices. If `n = |V(G)|`, then

```text
s+(G) > n + 2 - sec(pi/q) > n.
```

The first inequality is strict, not merely non-strict. The proof obtains a
strict pointwise phase comparison for every `t > 0`. Also,
`sec(pi/q) <= sec(pi/5) < 2`, which proves the second strict inequality.

## Proof structure

- The spine `H` consists of the two cycles and, in the disjoint case, their
  unique joining path.
- Exact matching belief propagation removes every off-spine tree. It gives
  activities `a_v = t + y_v >= t` and one common positive factor `K`, even
  when a Sachs cycle deletes the core root of an attached tree.
- With
  `A = Z_{H-V(C3)}`, `B = Z_{H-V(Cq)}`, and, only in the disjoint case,
  `D = Z_{H-(V(C3) union V(Cq))}`, the two Sachs formulas are kept separate:

```text
shared cut vertex:  Psi/K = Z_H + 2i(B-A)
vertex-disjoint:    Psi/K = Z_H + 4D + 2i(B-A)
```

  There is no `+4D` term in the shared case. In the disjoint case its sign is
  positive because `(-2i)(2i) = +4`.
- Set `R = Z_H` in the shared case and `R = Z_H + 4D` in the disjoint case.
  Partitioning matchings by whether they use an edge leaving `V(Cq)` gives
  `Z_H = Z_Cq(weighted) B + E`, where `E >= 0`.
- Since `Z_Cq(weighted) >= Z_Cq(t)`, writing their difference as `L >= 0`
  gives

```text
R - Z_Cq(t)(B-A) = E + LB + Z_Cq(t)A (+4D) > 0.
```

  This proves the uniform pointwise comparison
  `Theta_G(t) < atan(2/Z_Cq(t))`, regardless of the sign of `B-A` and without
  any continuant or bounded-connector argument.
- The comparison phase is exactly that of the isolated `Cq`. Its eigenvalues
  give
  `s+(Cq)-s-(Cq) = -2(sec(pi/q)-1)`, so the signed Coulson identity gives the
  exact phase integral. Since a connected bicyclic graph has `m = n + 1`,
  averaging the strict signed-energy bound with `s+ + s- = 2n + 2` proves the
  theorem.

No symbolic certificate is needed. A symbolic `C3`--`C5` check could
corroborate the smallest instance, but it is not part of the proof.

## File

- `paper.tex` - complete manuscript with the theorem, uniform proof, cycle
  calculation, Coulson step, and AKMPZ/LTZ references

No build artifacts are included.
