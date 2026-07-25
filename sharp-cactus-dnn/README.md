# Sharp Cactus DNN Constant

This directory contains a LaTeX manuscript computing the exact optimized
Liu--Tang--Zhang doubly nonnegative constant for every connected cactus.

## Main result

For a connected cactus `G` with `b` bridges and cyclic blocks of lengths
`l_1,...,l_r`, the manuscript proves

```text
kappa(G) = b + sum_j kappa(C_{l_j}),

kappa(C_l) = l                         if l is even,
             l sec^2(pi/(2l))          if l is odd.
```

Here

```text
kappa(G) = sup 4(sum_{uv in E(G)} sqrt(M_uv))^2 / (1^T M 1),
```

where the supremum is over nonzero doubly nonnegative matrices with positive
denominator.

The proof includes:

- the exact cycle upper correlation certificate from the LTZ functional;
- the sharp primal cycle matrix `M = x(2cI + A)`;
- exact one-vertex-sum additivity, with folding and Gram splitting for the
  upper bound and orthogonal gluing at the scaling `T_i/kappa_i = constant`
  for the lower bound;
- the spectral chain from `B = A_-` and `M = B o B`, yielding
  `s-(G) <= kappa(G)`.

## Bicyclic consequence

For a bicyclic cactus whose cyclic block lengths are `p,q`, define

```text
epsilon_l = 0                         if l is even,
            l tan^2(pi/(2l))          if l is odd.
```

The DNN bound proves `s+(G) >= n` whenever `epsilon_p + epsilon_q <= 1`.
The manuscript proves the exact comparisons

```text
epsilon_3 = 1,
epsilon_5 = 5 - 2 sqrt(5),
epsilon_5 + epsilon_7 < 1,
```

and monotonicity through odd lengths. Combined with the packing-two theorem
in `../packing-two-square-energy/paper.tex`, this proves the AKMPZ conjecture
for every bicyclic cactus except possibly the cyclic-length pairs

```text
{5,5} and {3,4k+1}, k >= 1.
```

These families are explicitly recorded as unresolved by the combined
methods, not as exceptions or counterexamples. In particular, all cases with
an even cycle are covered, while pairs with both lengths `3 mod 4` satisfy the
stronger inequality `s+(G) > |E(G)| = n+1`.

## Files

- `paper.tex` - self-contained manuscript and bibliography
- `../packing-two-square-energy/paper.tex` - companion packing-two theorem

No build artifacts are included.
