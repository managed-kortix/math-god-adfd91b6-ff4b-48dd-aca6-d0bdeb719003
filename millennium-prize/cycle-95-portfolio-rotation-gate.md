# Cycle 95: second structural portfolio gate

## RH: canonical systems

Riemann's cosine kernel is positive, but positivity of an even Schwartz kernel
does not imply real zeros of its Fourier transform.  For example,
\[
 \phi(u)=e^{-u^2}+\epsilon(e^{-(u-L)^2}+e^{-(u+L)^2}),
 \qquad 0<\epsilon<1/2,
\]
is strictly positive while
\[
 \widehat\phi(z)=\sqrt\pi e^{-z^2/4}(1+2\epsilon\cos Lz)
\]
has nonreal zeros.  In the Suzuki--Burnol construction, contraction of every
explicit finite Hankel section would produce positive canonical Hamiltonians,
but doing so for every positive shift is RH-equivalent.  Direct total
positivity of the multiplicative kernel also fails by a `2x2` support minor.

## BSD: derived Bockstein heights

Derived Bockstein regulators give exact determinant-line descent identities
and remain injective when the first height degenerates.  They identify Iwasawa
orders and `p`-adic Selmer structure, not the complex derivative index.  The
missing identity compares the derived `p`-adic determinant with
\[
 L^*(E,\chi,1)/(\Omega_\chi R_{NT,\chi}).
\]
Character variation and repetition over many primes do not construct this
archimedean comparison; postulating one prime-independent scalar identified
with the displayed term assumes the leading-term bridge.

## Hodge: Tate specialization and lifting

Assuming a finite-field Tate class is represented by a cycle `Z`, embedded
lifting across a square-zero thickening is obstructed in
\[
 H^1(Z,N_{Z/X})\otimes I.
\]
Frobenius invariance controls only the semiregularity image; a residual class
may survive in
\[
 \operatorname{im}\alpha_Z\cap\ker\sigma_Z.
\]
Derived Hilbert geometry records rather than kills this obstruction.  A valid
conditional production lemma requires selecting a Tate representative with all
successive obstructions zero, proving formal effectivity, and matching the
horizontal class.  Tate plus properness alone does not lift cycles.

## Navier--Stokes: suitability and enstrophy

For divergence-free fields,
\[
 \int_0^T\|\omega\|_2^2dt=\int_0^T\|\nabla u\|_2^2dt
\]
is already the Leray--Hopf budget.  The local energy inequality does not turn
it into scale-uniform control.  The normalized quantity
\[
 r^{-1}\int_{Q_r}|\omega|^2
\]
can remain order one along geometrically shrinking cylinders while the total
cost is summable.  Uniform-in-time enstrophy gives regularity by Prodi--Serrin,
but is itself a strong continuation hypothesis.  The missing input is
equation-produced critical tightness or epsilon-smallness, not suitability.

## P versus NP: incompressible errors

If an error set has size `M`, counting gives an error with time-bounded
Kolmogorov complexity at least `floor(log_2 M)` relative to the candidate.
Boundary-layer query hardness therefore produces nearly incompressible errors.
But a polylogtime-uniform `AC0` output sequence has an `O_A(1)` conditional
description once its uniformity machine is fixed.  Thus incompressibility points
in the opposite direction from the CJSW requirement: query hardness produces
high-complexity errors, while the constructive theorem demands a low-complexity
error sequence.

## Yang--Mills: Balaban RG

Balaban proved major cutoff-uniform ultraviolet stability and effective-action
results, including four-dimensional small-field RG with associated large-field
bounds.  These do not construct all continuum gauge-invariant Schwinger
functions, preserve limiting OS positivity through the RG machinery, take the
infinite-volume limit, or prove uniform infrared clustering.  The RG state is
an infinite-dimensional polymer Banach object with finitely many relevant or
marginal directions; finite codimension is not a finite-dimensional stable
manifold.  Even a complete ultraviolet trajectory theorem would leave the
nonperturbative infrared mass gap.

All six mechanisms met explicit rotation gates.  No Millennium result is
claimed.
