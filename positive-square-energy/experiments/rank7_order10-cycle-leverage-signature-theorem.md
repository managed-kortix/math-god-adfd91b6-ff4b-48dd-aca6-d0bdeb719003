# Order-ten cycle-leverage signature theorem

## Exact setup

For the physical-path endpoint multigraph, let `B` be an oriented incidence
matrix and let

`P = B^T (B B^T)^+ B`, `C = I-P`.

Thus `P` and `C` are the orthogonal cut and cycle projectors. For a path `e`,
its unit-conductance effective resistance and cycle leverage are

`R_e=P_ee`, `lambda_e=C_ee=1-R_e`.

Let `A` be the signed endpoint matrix: the column of a path of length `L_e`
has entries `1` and `(-1)^{L_e}` at its endpoints. Let `D` have entry `1` at
cubic vertices and a prescribed rational defect scale at noncubic vertices.
For nonnegative rational `a,b` and nonnegative weights `q_e`, define

`H = D [a A P A^T + b A C diag(q_e) C A^T] D`,

`M = max(1,max_v H_vv)` and

`G = H/M + diag(1-diag(H)/M)`.

The exact predicate scan uses the historical winner choices

- `q_e=lambda_e`;
- `q_e=lambda_e/R_e`;
- `q_e=1/L_e`;
- `q_e=lambda_e/L_e`;
- `q_e=1/L_e^2`;
- `q_e=lambda_e^2`;
- `q_e=lambda_e/(R_e L_e)`;
- `q_e=lambda_e/(R_e L_e^2)`.

Every quantity is rational because the endpoint graph and all path lengths are
finite and integral.

## Sufficient inequality

**Theorem (cycle-leverage predicate).** With the definitions above, put

`t_e = (-1)^{L_e} H_uv/M`

for the endpoints `u,v` of path `e`. If every `t_e>-1` and

`Phi(H) = sum_e (1-t_e)/(L_e(1+t_e)) <= 6`,

then the rank-seven canonical row is owned by the displayed Gram. The same
certificate owns every subdivision obtained by increasing any `L_e` by an even
amount, and the established one-vertex DNN lift allows arbitrary rooted-tree
attachments.

**Proof.** Since `P=P^2=P^T`, the cut term is

`A P A^T=(A P)(A P)^T`.

Likewise,

`A C diag(q_e) C A^T=(A C diag(sqrt(q_e)))(...)^T`

is positive semidefinite for `q_e>=0`. Congruence by `D`, positive scaling by
`1/M`, and addition of the nonnegative diagonal completion preserve positive
semidefiniteness, while the completion gives `G_vv=1`. Its endpoint
correlation is `H_uv/M`, so the canonical path atom contributes exactly
`(1-t_e)/(L_e(1+t_e))`. Summing gives exact excess `Phi(H)`, and the rank-seven
budget is six. At fixed endpoint Gram and parity, replacing `L_e` by `L_e+2`
only decreases its positive summand. This proves the all-length assertion. The
rooted-tree statement is the existing affine/DNN lift. QED.

The useful point is that this is a direct algebraic inequality, not a grid
selection rule. Once a finite set of rational winners has been learned for a
coarse signature, every row in that signature is decided by exact evaluation
of `Phi`; a signature is a whole-signature theorem exactly when all its rows
pass at least one of those fixed predicates.

## Exact full-remainder result

`rank7_order10_cycle_leverage_signature_predicate.py` authenticates all 7,807
prior weighted-cycle owners, extracts 32 distinct rational winners on 28 exact
coarse signatures, and then scans all 8,184,653 rows of the authenticated
post-weighted remainder. It performs no parameter-grid search.

The exact result is:

- 3,709 remainder rows have one of the 28 winner-bearing signatures;
- 124 additional orbits (146 physical rows, 2,108 canonical-plus-coordinate
  targets) satisfy the inequality;
- all 124 new owners use the single predicate
  `b=1/16`, defect scale `3/4`, and `q_e=lambda_e`;
- combined weighted-cycle ownership rises from 7,807 to 7,931 orbits;
- 19 of the 28 signatures are certified whole, totaling 5,006 owned orbits;
- 8,184,529 unowned rows remain byte-for-byte in the new remainder.

The canonical report digest is
`eb50949007f9351585d72da697942c4cde585b020da1ee51c2c55e787fa31019`.
This is additional exact finite ownership, not an order-ten or rank-seven
theorem.
