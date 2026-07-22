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

It remains to combine the two fractional endpoint integrals
`[-1/2,0]` and `[m,u(pi/2)]` with `(F(0)+F(m))/2`. Direct expansion shows
their total is the congruence-dependent O(q^-2) term seen numerically. A crude
absolute bound below 0.38 is enough. This endpoint lemma is the sole remaining
gap in the C5--Cq proof.
