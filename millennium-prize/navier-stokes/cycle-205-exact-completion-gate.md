# Cycle 205: corrected exact completion gate

## Result

After correcting the positive terminal derivative at `(8,-1,0)` to `+i e3`,
the regenerated 514-equation Cycle 204 completion system still has no rational,
real, or complex point. This conclusion does not use the invalid former
`e0509+e0513=2` identity: the corrected terminal rows reduce to the same
quadratic.

Exact row reduction of the 44 linear equations has rank 27 and leaves nine free
coordinates. Put

\[
 a=q1\_o9\_planar\_im,\qquad
 b=q1\_o10\_planar\_im,\qquad
 c=q1\_o10\_planar\_re.
\]

Three independently sourced nonlinear equations reduce to

\[
 f=-a^2+\frac14c^2 \quad (e0089),
\]

\[
 g=242905\left(1-a^2+2ab-\frac34c^2\right) \quad (e0436),
\]

\[
 h=2a^2-2ab+\frac12c^2 \quad (e0509).
\]

They satisfy the exact unit-ideal identity

\[
 f+\frac{1}{242905}g+h=1.
\]

The affine substitutions come from the linear ideal, so the verifier lifts this
identity back through the exact row-operation provenance and checks a polynomial
identity in the original 36 variables. Singular independently computes the
corrected 22-generator reduced ideal and the full 514-generator ideal as `(1)`
over `Q`, with zero certificate remainder.

## Verification

Run

```sh
python3 millennium-prize/navier-stokes/generate_cycle204_s2_system.py --check
python3 millennium-prize/navier-stokes/generate_cycle205_exact_reduction.py --check
python3 millennium-prize/navier-stokes/verify_cycle205_exact_reduction.py
python3 millennium-prize/navier-stokes/verify_cycle205_exact_infeasibility.py
python3 millennium-prize/navier-stokes/verify_cycle205_terminal_contradiction.py
python3 millennium-prize/navier-stokes/run_cycle205_singular.py
```

This retires only the pinned Cycle 177 seed with its frozen `S2` completion
support through second time order. It is not an obstruction to other supports,
seeds, leakage-controlled or infinite-mode constructions, and it has no
Navier--Stokes regularity consequence.
