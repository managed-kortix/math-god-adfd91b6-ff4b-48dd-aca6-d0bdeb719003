# Order-ten structural Gram sieve

## Exact construction

For a cubic order-ten kernel and a residual parity row, let `m_uv` be the
path multiplicity and `o_uv` its number of odd paths.  Define the rational
correlation matrix

`G_uu = 1`, and `G_uv = (m_uv - 2 o_uv)/3` on the support (zero elsewhere).

This is a signed normalized-adjacency construction.  It can also be read as a
signed signless-Laplacian Gram: every vertex has weighted degree three and

`sum_(v != u) |m_uv - 2 o_uv| <= sum_(v != u) m_uv = 3`.

Thus `G` is symmetric diagonally dominant with nonnegative diagonal, hence
positive semidefinite.  This proof is exact and uniform; it needs neither an
eigendecomposition nor numerical optimization.  The factor `1/3` is the
largest uniform factor justified by diagonal dominance.  Equivalently, `G`
is a sum of rational rank-one signed-edge matrices and nonnegative diagonal
slack matrices.

For a path of length `L`, put `t=(-1)^L G_uv`.  Convexity of `tan` gives the
standard path bound

`L tan^2(arccos(t)/(2L)) <= (1-t)/(L(1+t))`.

The right side is rational.  Increasing `L` by two preserves `t` and decreases
this bound, so one Gram certifies the canonical row and all fifteen
canonical-plus-two frontiers whenever the canonical rational sum is below
five.  Strict inequality also permits a nearby exact rational-vector witness
by density, if a physical chain rather than a Gram certificate is required.

## Complete residual audit

Run from the repository root:

```sh
python3 positive-square-energy/experiments/rank6_order10_structural_gram_sieve.py
```

The exact all-residual census is:

- residual parity-orbit representatives: `125457`;
- representatives certified at most five: `824` (`822` strictly below five);
- frontier targets certified by the same Gram: `13184 = 824 * 16`;
- largest structural bound: exactly `10`.

Therefore this simple signless-Laplacian/diagonal-dominance formula is a useful
fast pre-sieve, but it is not a uniform theorem for all residuals.  Its exact
worst value `10 > 5` is a direct obstruction to that proposed formula, not a
failure of rational rounding.

## Simplex comparison and conclusion

The existing exhaustive no-optimization simplex search is reproduced by

```sh
python3 positive-square-energy/experiments/rank6_orders8_10_atom_ledger_search.py --orders 10
```

It finds only `178` order-ten decompositions: eight five-mixed ledgers, 152
two-mixed/tetrahedron ledgers, and 18 mixed/triangle/tetrahedron ledgers.
These decompositions cover `108` distinct residual representatives.  They are
disjoint from the 824 diagonal-dominance rows, so the combined exact fast lane
covers `932` representatives and `14912` frontier targets.
Consequently the regular-simplex atom model is also sparse rather than
uniform.  The final 18 are valid one-sum spectral embeddings, so allowing the
standard cut-vertex product completion repairs the apparent overlap between
the triangle and tetrahedron blocks; it does not broaden the census.

For the remaining search lane `[70000,125457)`, the exact fast-lane coverage is
65 rows, hence 1040 targets:

- `[70000,100000)`: 47 structural rows and no atom rows;
- `[100000,125457)`: 4 structural rows and 14 atom rows;
- structural indices in the second interval: `118149`, `118756`, `118758`,
  and `124259`;
- atom indices in the second interval: `105465`, `105470`, `105483`, `105492`,
  `105515`, `105521`, `124181`, `124188`, `124191`, `124200`, `124203`,
  `124209`, `124212`, and `124218`.

The 47 structural indices in `[70000,100000)` are `70002`, `70004`, `70045`,
`70049`, `70056`, `70058`, `70060`, `70104`, `70114`, `70119`, `70123`,
`70223`, `70228`, `70232`, `70255`, `70259`, `70266`, `70268`, `70270`,
`71042`, `71094`, `71141`, `71323`, `71545`, `71594`, `71663`, `71700`,
`71712`, `71714`, `71717`, `71742`, `71771`, `71830`, `71842`, `71844`,
`71847`, `71872`, `71985`, `72198`, `72257`, `72269`, `72271`, `72274`,
`72299`, `73947`, `74151`, and `74840`. Thus exact pre-ownership reduces the
55,457-row tail to 55,392 expensive searches. The atom and structural sets are
disjoint, so no tie-breaking is required.

The tested structural families therefore do not replace the current general
search.  The durable gain is an exact, linear-time first lane: apply the
diagonally dominant Gram test, then the finite simplex ledger, and reserve
optimization/rationalization for the remaining rows.  The two equality rows
need their exact Gram realization rather than the rational-density argument.
A stronger uniform
formula must use correlations not determined solely by the local signed
imbalance `m-2o`; the exact value-ten rows rule out the most natural shared
normalized signless-Laplacian choice.
