# Exact long-path phase limits for the two dangerous theta channels

This note records exact limiting phase carriers for the empirically dangerous
families.  The finite-to-limit comparison is now supplied by
`theta-phase-monotonicity.md`; together with the finite Sturm gates in
`theta_short_base_gates.py`, it proves the complete short-base theorem in
`../theta-short-base-four-fifths.md`.

Let `I_c=int_0^1 (z^-2-1) alpha_c(z) dz`, where `alpha_c` is the principal
phase from `theta-imaginary-phase.md`.  Then

`s^+(Theta)-n = 1-I_c/pi`.

For fixed short paths, every term involving the long path tends to zero at
each fixed `0<z<1`, independently of `c mod 4`.  The four residue classes have
the same limit.

## The `(2,3,c)` channel

The limiting carrier factors into positive real factors times

`1+2z-z^2+2i z^(5/2)`.

Therefore

`alpha_23(z)=atan(2z^(5/2)/(1+2z-z^2))`.                       (1)

## The `(1,4,c)` channel

The limiting carrier factors into positive real factors times

`1+2z-z^2+z^3-z^4+2i z^(5/2)`.

Therefore

`alpha_14(z)=atan(2z^(5/2)/(1+2z-z^2+z^3-z^4))`.               (2)

Both denominators dominate `1+z` on `[0,1]`:

`1+2z-z^2-(1+z)=z(1-z)>=0`,

`1+2z-z^2+z^3-z^4-(1+z)=z(1-z)(1+z^2)>=0`.

Using `atan(t)<t` for `t>0`, either limiting area satisfies

`I_inf < integral_0^1 (z^-2-1) 2z^(5/2)/(1+z) dz`

`      = integral_0^1 2z^(1/2)(1-z) dz = 8/15`.                (3)

Since `pi>3`,

`8/15 < 3/5 < pi/5`.                                           (4)

Thus both dangerous channels have a rigorously safe long-path phase limit,
with a substantial rational margin.  The obstruction is finite-to-limit
control, not the limiting graph.

The exact pointwise monotonicity under `c -> c+4` in every residue class is
packaged in `theta_phase_monotonicity_certificate.py`.  Classes approaching
from below inherit (3) immediately; classes approaching from above reduce to
the finite gates certified by `theta_short_base_gates.py`.
