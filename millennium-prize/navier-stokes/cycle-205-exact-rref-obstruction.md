# Cycle 205: exact RREF and reduced obstruction

## Linear reduction

The 44 degree-one equations in the frozen Cycle 204 JSON form a `44 x 36`
rational matrix. Exact Gauss--Jordan elimination has rank 27 and no inconsistent
augmented row. Its solution set is therefore a nine-dimensional linear (hence
affine) space. In the Cycle 204 active-variable order, the free coordinates are

```text
q1_o8_vertical_re   q1_o8_vertical_im   q1_o9_planar_im
q1_o9_vertical_re   q1_o9_vertical_im   q1_o10_planar_re
q1_o10_planar_im    q1_o10_vertical_re  q1_o10_vertical_im
```

The exact parameterization and a `44 x 44` rational row-operation matrix are
stored in `cycle205_exact_reduction.json`. The certificate identity is

```text
left_transform * input_augmented_matrix = rref_augmented_matrix.
```

The verifier also checks that `left_transform` is invertible, so the displayed
RREF is row-equivalent to all 44 input equations rather than merely implied by
them.

## Nonlinear reduction

Substitution into all 514 Cycle 204 equations makes 478 source equations
identically zero. After primitive integer normalization and merging 14 duplicate
nonzero images, 22 distinct equations remain: 14 quadratic and 8 cubic.

The reduced system is inconsistent. Three of its quadratic equations are

\[
 r_{0001}=4t_2^2-t_5^2,
\]

\[
 r_{0006}=4-4t_2^2+8t_2t_6-3t_5^2,
\]

\[
 r_{0021}=4t_2^2-4t_2t_6+t_5^2.
\]

They give the exact degree-zero ideal certificate

\[
 -\frac14r_{0001}+\frac14r_{0006}+\frac12r_{0021}=1.
\]

The corrected terminal rows `e0509` and `e0513` both map to `r0021`. The
certificate also needs exterior images `r0001` and `r0006`; it does not preserve
the invalid former two-terminal solve claim.

Thus the full frozen Cycle 204 polynomial system has no solution over any
field of characteristic zero, and in particular no Fourier-real completion.
This is a bounded obstruction to the declared pinned-seed, fixed-support,
quadratic-order tangency ansatz only; it is not a Navier--Stokes regularity or
blowup result.

## Reproduction

```sh
python3 millennium-prize/navier-stokes/generate_cycle205_exact_reduction.py --check
python3 millennium-prize/navier-stokes/verify_cycle205_exact_reduction.py
```

The generator reparses `cycle204_s2_equations.json`, recomputes the exact RREF,
performs every affine polynomial substitution, and regenerates the reduced
system byte for byte. The independent verifier checks the source hash, RREF
row-equivalence certificate, affine replay, artifact hash, and the final
unit-ideal identity.
