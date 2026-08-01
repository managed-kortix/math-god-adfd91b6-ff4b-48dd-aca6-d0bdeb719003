# Cycle 205: corrected exact reduced certificate

## Result

The sign-corrected 514-equation Cycle 204 system is infeasible over `Q`, `R`,
and `C`. The former two-terminal constant-2 certificate is invalid and is not
used. Under the corrected Fourier-reality sign, `e0509` and `e0513` have the
same reduced image rather than complementary images.

The next exact contradiction found has 22 source equations: the 19 linear rows
below and `e0089`, `e0436`, `e0509`. Exhaustive subset checks of the 22 distinct
nonzero equations obtained after reducing by all 44 linear rows find no
contradictory one- or two-equation subset; the first contradictory reduced
subset has three equations, precisely the three forms used here. This proves
minimality only in that fully linearly reduced ledger. Separately, deleting any
one of the 19 displayed linear rows from this 22-row original subsystem makes
that subsystem consistent over `C`, as does deleting any nonlinear row. It
does not prove that no different original subsystem with fewer than 22 rows
exists among all 514 equations.

## Linear substitution

The same 19 independent exterior-closure equations used in the earlier audit
give, with

\[
 a=q1\_o9\_planar\_im,\qquad
 b=q1\_o10\_planar\_im,\qquad
 c=q1\_o10\_planar\_re,
\]

the planar zero relations and

\[
 q1\_o9\_planar\_re=c/2,
\]

\[
 q1\_o4\_vertical=(-c/2,-a),\quad
 q1\_o5\_vertical=(0,2a-b),\quad
 q1\_o6\_vertical=(c/2,-a).
\]

The 19 rows are

```text
e0042 e0043 e0068 e0069 e0084 e0085 e0090 e0091
e0092 e0093 e0094 e0095 e0096 e0097 e0101 e0102
e0103 e0104 e0105
```

## Unit ideal

Substitution into three nonlinear source equations gives

\[
 \bar e_{0089}=-a^2+c^2/4,
\]

\[
 \bar e_{0436}=242905(1-a^2+2ab-3c^2/4),
\]

\[
 \bar e_{0509}=2a^2-2ab+c^2/2.
\]

The corrected opposite terminal row satisfies

\[
 \bar e_{0513}=\bar e_{0509}=Q,
\]

so the terminal pair alone is consistent, not contradictory.

Direct addition yields

\[
 \bar e_{0089}+\frac{1}{242905}\bar e_{0436}+\bar e_{0509}=1.
\]

This is a unit-ideal certificate after exact substitution, with no division by
a variable and no numerical step. The full RREF artifact additionally records
the complete `44 x 44` rational left transform, and the independent Singular
run verifies a lifted certificate against all original generators.

## Reproduction

```sh
python3 millennium-prize/navier-stokes/verify_cycle205_terminal_contradiction.py
python3 millennium-prize/navier-stokes/verify_cycle205_exact_reduction.py
python3 millennium-prize/navier-stokes/run_cycle205_singular.py
```

This is only an obstruction to the declared pinned-seed, frozen-support,
quadratic-order tangency ansatz, not a Navier--Stokes regularity result.
