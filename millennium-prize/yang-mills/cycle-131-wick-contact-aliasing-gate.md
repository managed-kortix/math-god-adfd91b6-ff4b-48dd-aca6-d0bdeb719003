# Cycle 131: naive lattice action density is not distributionally tight

Negative temporal Sobolev topology does not rescue the naive centered square of
a spatially smoothed electric field.  In the free Gaussian calibration, the
unsuppressed temporal contact covariance is squared by Wick contraction and
aliases into every external lattice frequency with strength proportional to
`a_tau^(-1)`.  The family is not tight even as a distribution.

Let `sigma>0` be the combined spatial heat time.  At temporal frequencies of
order the lattice cutoff, the spatially smoothed transverse electric covariance
tends to

\[
Q_\infty=\frac23G_\sigma I_3,
\qquad
G_\sigma=(4\pi\sigma)^{-3/2}.
\]

For the centered electric energy

\[
e_a=\frac12\left(|E_a|^2-\mathbf E|E_a|^2\right),
\]

Wick contraction gives the internal-loop coefficient

\[
\frac12\operatorname{Tr}(Q_\infty^2)
=\frac23G_\sigma^2
=\frac1{96\pi^3\sigma^3}.
\]

There are `N=T/a_tau` internal temporal-frequency decompositions for every
fixed external lattice frequency.  Consequently, locally uniformly at bounded
external frequency,

\[
S_a(\nu)
=\frac1{96\pi^3\sigma^3a_\tau}+O_\nu(1).
\]

For every nonzero smooth temporal test function `phi`,

\[
\operatorname{Var}\langle e_a,\phi\rangle
=\frac{\|\phi\|_2^2}
{96\pi^3\sigma^3a_\tau}+O_\phi(1).
\]

Thus no negative-Sobolev exponent can produce a cutoff-uniform bound: the
divergence occurs at every fixed external frequency, including the zero mode,
rather than escaping only to high frequencies.

Subtracting the mean cannot alter this connected covariance.  Multiplication
by a factor tending to a nonzero constant also fails.  Scaling by
`sqrt(a_tau)` produces temporal white noise, not the intended local action
density.  Formally subtracting the positive divergent contact covariance is not
an observable-level deterministic counterterm and need not preserve positivity.

This does not contradict the standard continuum two-photon computation for a
renormalized composite smeared *after* it is formed.  That object has exact
spectral polynomial

\[
15\omega^4-30\omega^2|p|^2+23|p|^4,
\]

which is positive for `|p|<=omega` because, with
`x=|p|^2/omega^2`,

\[
15-30x+23x^2
=23\left(x-\frac{15}{23}\right)^2+\frac{120}{23}>0.
\]

Its external frequency tail is proportional to `omega^4`, giving the sharp
local temporal threshold `H^{-s}` for `s>5/2`, modulo the usual contact-
polynomial choice.  The naive lattice square is not a regulator approximation
to that composite: nonlinear product formation does not commute with temporal
sampling, and cutoff frequencies alias into a divergent white component.

The surviving objects are temporally mollified composites at fixed physical
resolution or genuinely bilocal two-time Wick products.  Collapsing a bilocal
product to a one-time diagonal recreates the forbidden product of temporal
contact distributions.

This free obstruction invalidates the proposed Yang--Mills compactness target
for the naively centered plaquette/action density.  Any interacting revival
must first specify a reflection-compatible composite renormalization whose free
limit passes this gate.

Reproduce the exact constants with

```sh
python3 millennium-prize/yang-mills/verify_cycle131_wick_contact_aliasing.py
```

No Yang--Mills or Millennium solution is claimed.
