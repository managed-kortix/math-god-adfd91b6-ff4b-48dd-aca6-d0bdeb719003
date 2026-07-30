# Cycle 137: shrinking temporal blocks do not repair the local square

Temporal averaging before forming the electric-energy square can suppress the
Cycle 131 alias divergence only by retaining nonzero physical temporal
resolution.  If the block shrinks to recover a local composite, the divergence
returns.  Exact preservation of the target two-leg vertex forces the filter to
be trivial.

For the normalized `m`-slice box multiplier

\[
B_m(\theta)=\frac1m\sum_{r=0}^{m-1}e^{ir\theta},
\]

orthogonality gives the exact fourth moment

\[
\boxed{
\frac1{2\pi}\int_{-\pi}^{\pi}|B_m(\theta)|^4d\theta
=\frac{2}{3m}+\frac{1}{3m^3}.
}
\]

Indeed, this counts quadruples with `r_1+r_2=r_3+r_4`.  On an `N`-frequency
temporal lattice, when `N>=2m-1`,

\[
\sum_{k=0}^{N-1}|B_m(2\pi k/N)|^4
=N\left(\frac{2}{3m}+\frac{1}{3m^3}\right).
\]

Thus a Wick loop with four filtered legs has alias multiplicity of order
`N/m`.  Writing temporal spacing `a_tau`, period `T=N a_tau`, and physical block
width `ell=m a_tau`:

- fixed `m` leaves the `a_tau^(-1)` divergence;
- fixed `ell>0` gives a finite limit of order `1/ell`, but the observable stays
  temporally pre-smoothed and bilocal;
- `ell -> 0` restores divergence of order `1/ell`.

More generally, for a temporal approximate identity with multiplier
`b_epsilon(omega)->1`, the free Maxwell centered-square spectral density at
fixed external frequency contains a nonnegative integral whose integrand tends
to

\[
\frac12\operatorname{Tr}(Q_\infty^2)
=\frac1{96\pi^3\sigma^3}>0.
\]

Fatou's lemma therefore forces divergence as the temporal resolution is
removed.  This mass remains at fixed external frequency, so negative Sobolev
weights cannot hide it.  Deterministic mean subtraction does not affect the
connected covariance.

There is a second exact rigidity.  If filtering each elementary leg changes a
two-leg composite vertex by `b(p)b(q)`, and exact target retention requires

\[
b(p)b(q)=1
\]

for independently variable `p,q`, then `b` is constant; with `b(0)=1`,

\[
b\equiv1.
\]

On a finite cyclic lattice, the corresponding all-pass statement says that a
normalized finite impulse response with unit modulus at every cyclic root must
be a unit-phase delta translation.  Such a filter supplies no ultraviolet
suppression.

One-sided or collar temporal blocks can remain inside the positive-time
observable algebra and thereby preserve reflection positivity on that restricted
algebra.  A centered block crossing the reflection plane does not automatically
preserve it.  In either case the free-limit dichotomy above remains: fixed
physical width changes the observable, while shrinking width recreates the
local-square divergence.

This theorem rules out only constructions based on linear temporal blocking of
the elementary electric field, pointwise squaring, and deterministic centering.
It does not rule out fixed-resolution bilocal observables, a separately
renormalized composite smeared after formation, operator mixing, or a genuine
composite-field extension.

Reproduce the exact finite identities with

```sh
python3 millennium-prize/yang-mills/verify_cycle137_temporal_block_no_go.py
```

No Yang--Mills or Millennium solution is claimed.
