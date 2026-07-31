# Cycle 177: the terminal receiver quartet reopens the filter

The Cycle 176 source field has complete quadratic convolution supported on its
terminal boundary quartet. Those four output frequencies cannot also be
populated as nonzero receiver modes while retaining the same closed filter.
Exact source--receiver and receiver--receiver terms create new outputs, and no
choice of divergence-free receiver polarizations cancels all of them. The
obstruction already occurs at the four outermost receiver--pump sums and is
independent of depth.

Fix the Cycle 176 data, write its terminal radius as `T=R_D`, and let

\[
 G(z)=\sum_s g_sz^s
\]

be the pump polynomial. It is nonconstant, reciprocal, and has an extreme
positive exponent `S` with coefficient one, where `0<S<T`. The source-only
convolution is the terminal quartet `(+-T,+-Y,0)`.

Populate these frequencies by a real receiver field. The most general real
divergence-free polarization on the positive `Y` layer is

\[
 v_-=(Ya_-,Ta_-,b_-),\qquad v_+=(Ya_+,-Ta_+,b_+)
\tag{1}
\]

at `(-T,Y,0)` and `(T,Y,0)`, respectively; reality assigns the same vectors to
the opposite frequencies. Thus (1) searches the entire real receiver-
polarization space, not only coordinate-axis choices. The endpoint argument
below is complex-linear and therefore also applies to complex receiver
polarizations, with conjugate data imposed on the opposite reality layer.

## Full convolution

For `u=u_src+u_rec`, the exact ordered Leray convolution splits as

\[
 B(u,u)=B(u_{src},u_{src})
 +B(u_{src},u_{rec})+B(u_{rec},u_{src})
 +B(u_{rec},u_{rec}).
\tag{2}
\]

The first term is the Cycle 176 quartet. The middle terms include every
receiver--rail and receiver--pump interaction. The last term includes all
sixteen ordered receiver pairs. These terms are retained in the exact
certificate; none is discarded by a support convention.

For `R=3`, `Y=5`, and representative small/depth families, the nonzero symbolic
support counts are

| multipliers; rail factors | source modes | source--source | source--receiver | receiver--receiver | full |
|---|---:|---:|---:|---:|---:|
| `(2); empty` | 6 | 4 | 20 | 4 | 28 |
| `(2,4); {0}` | 8 | 4 | 28 | 4 | 36 |
| `(2,4,2); {0,2}` | 12 | 4 | 40 | 4 | 48 |
| `(4,2,6,2); {1,3}` | 40 | 4 | 144 | 4 | 152 |

Counts are over vector-valued polynomials in the four receiver parameters: a
frequency is counted when its symbolic coefficient is not identically zero.

## Unique endpoint obstruction

Consider the receiver `(T,Y,0)` and extreme pump `(S,0,0)`. Their sum
`q=(T+S,Y,0)` has a unique source--receiver representation. Indeed, `S` is the
largest pump exponent, while rail horizontal exponents have absolute value
strictly below `T`; no other receiver plus pump or receiver plus rail reaches
this horizontal coordinate. Receiver--receiver sums have horizontal coordinate
only `-2T,0,2T`, so they do not reach `q` either.

Before Leray projection, the symmetrized interaction at `q` is

\[
 w_+=\bigl(a_+Y^2,\ a_+Y(S-T),\ b_+Y\bigr).
\tag{3}
\]

For `P_qw_+=0`, the vector `w_+` must be parallel to `q`. Its third component
first forces `b_+=0`. If `a_+` is nonzero, comparing the first two components
then gives

\[
 Y^2=(S-T)(S+T)=S^2-T^2,
\tag{4}
\]

which is impossible because `Y` is nonzero and `0<S<T`. Hence
`a_+=b_+=0`. The extreme negative pump applied to `(-T,Y,0)` similarly gives
`a_-=b_-=0`. Reality supplies the conclusions on the `-Y` layer. The same
argument holds for complex `a` and `b`, since (4) remains the necessary scalar
identity.

Therefore

\[
 \boxed{\text{all newly generated outputs vanish only for }u_{rec}=0.}
\]

Receiver--receiver cancellation cannot repair this: its support misses the
unique frequencies `(+- (T+S),+-Y,0)`. Nor can the original source--source
quartet repair it, because that term remains at horizontal radius `T`.

## Decision

The Cycle 176 field is an exact forcing-output filter only while its terminal
quartet is left unpopulated. Turning those outputs into physical receivers for
cubic energy flux destroys the filter before any receiver-flux normalization is
considered. Within the fixed Cycle 176 source support, arbitrary divergence-
free polarization choices do not close the new channels. A viable cubic
cascade adversary would need additional completion modes or a different
frequency architecture; the receiver quartet cannot simply be inserted into
the existing Laurent construction.

This is a finite Fourier-algebra obstruction, not a Navier--Stokes regularity
result. Run the exact symbolic certificate with

```sh
python3 millennium-prize/navier-stokes/verify_cycle177_receiver_quartet.py
```
