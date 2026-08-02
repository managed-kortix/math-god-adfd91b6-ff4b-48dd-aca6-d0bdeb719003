# Cycle 263: frozen invariant-preserving Galerkin architecture

## Pre-compute freeze

This document freezes `C263-MG1` before its validation computation. It defines
a new integrator test and does not reuse, evolve, refine, or tune any member of
the retired Cycle 258 family. The test is numerical finite-dimensional
validation only; a finite Galerkin trajectory is not a full Euler PDE
certificate and is not an `ND251` crossing.

Let

\[
 \Lambda_K=\{k\in\mathbb Z^2:0<\lVert k\rVert_\infty\leq K\},
 \qquad \omega_{-k}=\overline{\omega_k},
\]

and let `P_K` be the orthogonal Fourier projection onto this symmetric square.
The frozen semidiscrete equation is the exact convolution Galerkin system

\[
 \dot\omega=P_K[-u(\omega)\mathbin\cdot\nabla\omega]=F_K(\omega),
 \qquad u=\nabla^\perp\Delta^{-1}\omega.
\]

The production right-hand side is evaluated by direct retained-mode
convolution, not by an unqualified native-grid two-thirds rule. An independent
padded replay uses a grid of side at least `4K+1`, multiplies in physical
space, and projects back to `Lambda_K`. This padding prevents every quadratic
wraparound into a retained mode, including cutoff-boundary aliases.

For a signed step `h`, define `omega_1` by implicit midpoint:

\[
 m={\omega_0+\omega_1\over2},\qquad
 R=\omega_1-\omega_0-hF_K(m)=0.
\]

Solve this finite real system by full Newton iteration with the analytic
Jacobian. Freeze maximum 12 Newton iterations and the fail-closed acceptance
test

\[
 \lVert R\rVert_2\leq 5\times10^{-13}
   (1+\lVert\omega_0\rVert_2+|h|\lVert F_K(m)\rVert_2).
\]

No unconverged step is accepted. The implementation records the actual
nonlinear residual rather than treating Newton convergence as exact.

## Invariant statement

Use normalized finite-mode quadratic forms

\[
 Z(\omega)={1\over2}\sum_{k\in\Lambda_K}|\omega_k|^2,
 \qquad
 E(\omega)={1\over2}\sum_{k\in\Lambda_K}{|\omega_k|^2\over |k|^2}.
\]

Orthogonality of `P_K`, incompressibility, and periodic integration by parts
give, for every real retained field,

\[
 \operatorname{Re}\sum_k\overline{\omega_k}F_K(\omega)_k=0,
 \qquad
 \operatorname{Re}\sum_k{|k|^{-2}}\overline{\omega_k}F_K(\omega)_k=0.
\]

Both invariants are quadratic. Therefore implicit midpoint preserves both when
`R=0`; this is not merely a small-step consistency claim. For a computed step,
the exact algebraic defect identities are

\[
 Z(\omega_1)-Z(\omega_0)
 =h\langle m,F_K(m)\rangle_Z+\langle m,R\rangle_Z,
\]

\[
 E(\omega_1)-E(\omega_0)
 =h\langle m,F_K(m)\rangle_E+\langle m,R\rangle_E.
\]

Thus any observed defect is split into a semidiscrete tangency defect and the
nonlinear-solve residual, up to roundoff in evaluating the displayed identity.
In addition, replay the Cauchy--Schwarz bound
`|<m,R>_Q| <= ||m||_Q ||R||_Q` for each quadratic form `Q`. Reporting only
endpoint relative drift is insufficient.

## Frozen validation

Validation uses deterministic synthetic real Fourier states, not Cycle 258
data.

1. At `K=2` and `K=3`, compare direct convolution with the independent padded
   replay and test both invariant tangencies.
2. At `K=3`, run 32 midpoint steps with `h=1/64` from a formula-defined state
   `omega_k=(cos(0.37 k_x+0.19 k_y)+i sin(0.23 k_x-0.41 k_y)) /
   (1+|k|^2)^2`, imposing conjugate symmetry.
3. At every step require the frozen nonlinear residual gate and replay both
   invariant defect identities. Report maximum absolute and relative invariant
   defects; do not relax the solve gate after seeing results.
4. Reverse the final state with 32 steps of `-h` and report the relative state
   return error. This checks the symmetric update but is not a substitute for
   the residual identities.
5. Fail if the direct/padded relative RHS discrepancy exceeds `2e-13`, either
   normalized tangency exceeds `2e-13`, either defect-identity closure exceeds
   `2e-13` times its natural scale, or the reversal error exceeds `2e-11`.

Passing these tests establishes that the implemented finite-mode update
preserves Galerkin energy and enstrophy to its recorded nonlinear-solve and
roundoff residuals. It establishes neither convergence to the full Euler flow
nor a directed velocity-`L3` amplification. A later production architecture
must separately freeze a new deterministic family, horizon, refinement and
cubature matrix, analytic-tail interface, and strict directed endpoint target
greater than `2+eta` before trajectory selection.
