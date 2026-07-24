# Parity-uniform imaginary-axis phase formula for theta graphs

This note records an exact phase representation for the signed square trace of
every theta graph. It reduces the remaining bare `4/5` theorem to a weighted
phase-area inequality. The determinant algebra, positivity, trace identity,
and endpoint integration by parts have been independently audited; the final
phase-area bound remains open.

Let `G=Theta(a,b,c)`, `L=a+b+c`, and `n=L-1`. For `u>0`, set
`z=e^(-2u)` and `x=2i sinh(u)=i(1-z)/sqrt(z)`. Define

`f_l(z)=1-(-z)^l`, `F=f_a f_b f_c`.

Every quotient `F/f_l` below means the polynomial product of the other two
factors. The path Chebyshev polynomial satisfies exactly

`U_(l-1)(x/2)=i^(l-1) z^(-(l-1)/2) f_l/(1+z)`.                 (1)

Put

`N=(1-z)F+z sum_l f_(l-1) F/f_l`,

`M=sum_l i^(1-l) z^((l-1)/2) F/f_l`,

where the sum runs over `l=a,b,c`, and put

`H=N^2+z(1+z)^2 M^2`.                                          (2)

Schur complementation along the three path interiors gives

`chi_G(x)=-i^(L-3) z^(-(L-1)/2) H / ((1+z)^3 F)`.              (3)

On `0<z<1`, every factor outside `H` has constant phase. Thus all phase
variation of `chi_G(i(1-z)/sqrt(z))` is carried by `H`.

## Real polynomial decomposition

Write `M=P+i sqrt(z) Q`, where

`P=sum_(l=2k+1) (-1)^k z^k F/f_l`,

`Q=sum_(l=2k) (-1)^k z^(k-1) F/f_l`.

Then `P,Q` are real polynomials and `H=R+i sqrt(z) S`, with

`R=N^2+z(1+z)^2(P^2-zQ^2)`,

`S=2z(1+z)^2 P Q`.                                             (4)

For an even length `l=2k`,

`f_(l-1)-(1+z)z^(k-1)=(1-z^(k-1))(1-z^k)>=0`.

All `F/f_l` are nonnegative on `[0,1]`, so the triangle inequality gives

`N>=z(1+z)|Q|`.                                                 (5)

Consequently

`R=(N^2-z^2(1+z)^2Q^2)+z(1+z)^2P^2>=0`.                       (6)

For `0<z<1`, `H` cannot vanish because (3) would give a nonreal eigenvalue of
a real symmetric matrix. Hence `H` remains in the closed right half-plane,
avoids zero, and has a canonical continuous principal phase
`alpha(z)=Arg H(z) in [-pi/2,pi/2]`.

## Signed-square trace

For any loopless real symmetric matrix,

`tr(A|A|)=(2/pi) integral_0^infinity t^2 d/dt arg chi_A(it) dt`.

Using (3) and `t=(1-z)/sqrt(z)` gives

`tr(A|A|)=-(2/pi) integral_0^1 ((1-z)^2/z) Im(H'/H) dz`.        (7)

Here `H'=dH/dz`. Integrating by parts yields

`tr(A|A|)=-(2/pi) integral_0^1 (z^(-2)-1) alpha(z) dz`.         (8)

There is no endpoint term. At `z=1`, `(1-z)^2/z` vanishes and `alpha` is
bounded. At `z=0`, `N(0)=H(0)=1` and
`Im H=2z^(3/2)(1+z)^2PQ`, so `alpha(z)=O(z^(3/2))`; multiplication by the
`O(z^-1)` boundary weight still tends to zero.

Because a theta has `m=n+1`, the desired bare surplus inequality
`s^+(G)-n>=4/5` is equivalent to `tr(A|A|)>=-2/5`, or

`integral_0^1 (z^(-2)-1) alpha(z) dz <= pi/5`.                 (9)

The weight in (9) has infinite total mass near zero, so the coarse bound
`alpha<=pi/2` cannot prove (9). The usable structure is the exact vanishing
`alpha=O(z^(3/2))`, together with the path-dependent powers in `P,Q` and the
positive lower bound (5) for `N`. Establishing (9) outside
`Theta(2,2,3)`, `Theta(2,3,3)`, and `Theta(1,4,4)` is the active obstruction.
