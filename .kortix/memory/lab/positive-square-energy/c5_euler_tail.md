# C5--Cq Euler tail bookkeeping

Let `delta(0)=pi/2` be the continuous phase and

`u(theta)=(q theta/2-delta(theta))/pi`.

Then `u(0)=-1/2`,
`u(pi/2)=q/4+1-atan(1/4)/pi`, and the positive band roots are
`theta(k)` for consecutive integers `k=0,...,m`, where
`m=floor(u(pi/2))=(q+3)/4` if q=1 mod 4 and `(q+1)/4` if q=3 mod 4.

Put `F(u)=4cos(theta(u))^2`. For q>=727,

`|F''| <= 8pi^2/(q/2-10)^2+240pi^2/(q/2-10)^3 < 0.000686`.

The composite trapezoid inequality on `[0,m]` gives

`|sum_{k=0}^m F(k)-int_0^m F(u)du-(F(0)+F(m))/2|`
`<=m sup|F''|/12 <0.011`.

For uniformity in q, use `m<=(q+3)/4`. After inserting `pi<22/7`, the
derivative of this upper envelope is exactly
`-968(q^2+126q+1220)/(147(q-20)^4)<0`; hence q=727 is the worst tail case.

It remains to combine the two fractional endpoint integrals
`[-1/2,0]` and `[m,u(pi/2)]` with `(F(0)+F(m))/2`. Direct expansion shows
their total is the congruence-dependent O(q^-2) term seen numerically. A crude
absolute bound below 0.38 is enough. This endpoint lemma is the sole remaining
gap in the C5--Cq proof.

This gap closes by Lipschitz bounds. Since `|f'|<=4` and
`theta'<=pi/(q/2-10)`,

`L:=sup|F'|<=4pi/(q/2-10)<0.03555` at q>=727.

On the left half-cell, the difference between `F(0)/2` and the integral over
`[-1/2,0]` has magnitude at most `L/4<0.00889`. On the right, write
`rho=u(pi/2)-m`. We have `0<rho<3/4` in both congruence classes and
`F(u(pi/2))=0`; hence `F(m)<=rho L` and

`|F(m)/2-int_m^(m+rho)F| <= rho L/2+rho^2 L/2 <15L/32<0.01667`.

Together with the interior error <0.011, the complete finite-band quadrature
error is <0.037. This is below the available defect margin
`2+(34/15)^2-(sqrt(5)+9/2)>0.401`. The q>=727 tail is therefore proved once
the limiting density identity is stated with these endpoint orientations.
