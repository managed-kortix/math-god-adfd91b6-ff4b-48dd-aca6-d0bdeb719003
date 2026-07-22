# C5--Cq analytic tail, proof draft

This note records the exact logical correspondence needed to close odd
`q>=727`. It is deliberately not yet a claimed theorem: the spectral root
parametrization itself still needs to be derived cleanly from the moving
factor `S_q` in the standalone certificate.

Let the band roots be `x=2 cos(theta)` and choose the continuous phase branch
with

`u(theta)=(q theta/2-delta(theta))/pi`,

`delta(0)=pi/2`, `delta(pi/2)=-pi+atan(1/4)`.

The root equation says precisely that band roots in `[0,2]` occur at the
integer values of `u`. Since

`u(0)=-1/2`,

`b:=u(pi/2)=q/4+1-beta`, `beta=atan(1/4)/pi`,

and `1/13<beta<1/12`, these integers are `0,...,l+1` for both
`q=4l+1` and `q=4l+3`.

Put `F(u)=4cos^2(theta(u))`. The union of unit midpoint cells centered at
those integers begins exactly at `-1/2` and ends at `l+3/2`. Its endpoint
differs from `b` by less than `1/3`: it overshoots by `1/4+beta<1/3` in the
first residue class and undershoots by `1/4-beta<1/3` in the second.

The exact Sturm certificates give `|delta'|<10`, `|delta''|<60`. Therefore,
for `a=q/2-10`,

`|F''| <= 8 pi^2/a^2 + 240 pi^2/a^3 =: M`.

Midpoint error on all full cells is at most `(q+7)M/96`. At the terminal
discrepancy, `F(b)=F'(b)=0`, so Taylor's theorem bounds its integral by
`M/(6*3^3)`. The script `c5_tail_certificate.py`, using `pi<22/7`, proves
their sum is below `1/100` for q=727 and decreases for larger q.

On the exact interval `[u(0),u(pi/2)]`, change variables back to theta:

`integral F du = q/2 - (1/pi) integral_0^(pi/2) 4cos^2(theta)delta'(theta)dtheta`.

The independent polynomial-majorant certificate proves

`I_phase := -2-(1/pi) integral 4cos^2(theta)delta'(theta)dtheta > 0`.

Consequently the sum of squares of the positive band roots is greater than
`q/2+2-1/100`.

For the positive outlier, write `x_q=r_q+r_q^-1`. Its finite equation is
`r_q^q A(r_q)=B(r_q)`. The polynomial `B(1+t)` has strictly positive
coefficients, while `A` has a unique root greater than one and that root is
greater than `5/3`; hence `r_q>5/3` and `x_q>34/15`. Thus

`D_q=S_q^+-q/2 > 2+(34/15)^2-1/100`.

Using `sqrt(5)<161/72`, the right side exceeds the required
`sqrt(5)+9/2` by more than `0.39`.

## Remaining adversarial gate

`c5_phase_equation.py` now derives `z^q=B/A`, the trigonometric phase equation,
the exact rational derivative used by the bounds, the continuous branch
endpoints, the integer count in each residue class, and uniqueness/sign of the
positive outlier. Since `u'>0`, all band roots are simple and exhausted by the
integer count. The remaining publication gate is independent reproduction in
PARI/GP and a final statement-level audit of the factor decomposition.
