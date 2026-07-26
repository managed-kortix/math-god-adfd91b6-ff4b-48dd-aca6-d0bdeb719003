# Cycle 35: dyadic telescoping of endpoint-safe Abel shells

Fix an even integer `N`, let

\[
 X_j=2^jN\qquad(0\leq j\leq J+1),
\]

and use the normalized shell weights at every scale.  For even `X`, define

\[
 T^{(X)}_r=rA_X-\frac{\psi(r)}{\log X},
 \qquad X/2\leq r<X,
\]

and

\[
 E_X=\sum_{r=X/2}^{X-1}\frac{X}{r(r+1)}
       \bigl(T^{(X)}_r\bigr)^2.
\tag{35.1}
\]

Thus the weight is always `X/[r(r+1)]`; it is not replaced by an
unnormalized common weight when scales are summed.

## One-scale Abel energy

Put

\[
 d^{(X)}_r=T^{(X)}_r-T^{(X)}_{r-1}
 =A_X-\frac{\Lambda(r)}{\log X}.
\tag{35.2}
\]

The endpoint-safe Abel identity gives the exact decomposition

\[
 \boxed{E_X=H_X+P_X,}
\tag{35.3}
\]

where

\[
 H_X=2\bigl(T^{(X)}_{X/2}\bigr)^2
       -\bigl(T^{(X)}_{X-1}\bigr)^2
\tag{35.4}
\]

is the two-square boundary packet and

\[
 P_X=X\sum_{r=X/2+1}^{X-1}\frac1r
 \left(A_X-\frac{\Lambda(r)}{\log X}\right)
 \left(T^{(X)}_r+T^{(X)}_{r-1}\right)
\tag{35.5}
\]

is the complete normalized increment packet.  Both terms in (35.4), including
the negative right endpoint with denominator already absorbed into its exact
coefficient, are required.

For adjacent scales, (35.3) is precisely the Cycle 34 formula in the compact
form

\[
 E_X-E_{2X}=(H_X-H_{2X})+(P_X-P_{2X}).
\tag{35.6}
\]

Opening (35.6) displays the four boundary squares:

\[
\begin{aligned}
 E_X-E_{2X}={}&
 2\left[\bigl(T^{(X)}_{X/2}\bigr)^2
       -\bigl(T^{(2X)}_X\bigr)^2\right]\\
 &+\left[\bigl(T^{(2X)}_{2X-1}\bigr)^2
       -\bigl(T^{(X)}_{X-1}\bigr)^2\right]
 +P_X-P_{2X}.
\end{aligned}
\tag{35.7}
\]

## Exact sum over dyadic scales

Sum the decrements for `X_0,X_1,...,X_J`.  Since `2X_j=X_(j+1)`, the
boundary packets and increment packets telescope separately:

\[
\begin{aligned}
 \sum_{j=0}^{J}(H_{X_j}-H_{X_{j+1}})&=H_N-H_{X_{J+1}},\\
 \sum_{j=0}^{J}(P_{X_j}-P_{X_{j+1}})&=P_N-P_{X_{J+1}}.
\end{aligned}
\tag{35.8}
\]

Consequently

\[
 \boxed{
 \sum_{j=0}^{J}\bigl(E_{2^jN}-E_{2^{j+1}N}\bigr)
 =H_N-H_{2^{J+1}N}+P_N-P_{2^{J+1}N}
 =E_N-E_{2^{J+1}N}.}
\tag{35.9}
\]

In fully opened endpoint-safe form, with `M=2^(J+1)N`, this is

\[
\boxed{\begin{aligned}
 \sum_{j=0}^{J}(E_{2^jN}-E_{2^{j+1}N})={}&
 2\bigl(T^{(N)}_{N/2}\bigr)^2
 -\bigl(T^{(N)}_{N-1}\bigr)^2\\
 &-2\bigl(T^{(M)}_{M/2}\bigr)^2
 +\bigl(T^{(M)}_{M-1}\bigr)^2\\
 &+N\sum_{r=N/2+1}^{N-1}\frac{d^{(N)}_r}{r}
       \bigl(T^{(N)}_r+T^{(N)}_{r-1}\bigr)\\
 &-M\sum_{r=M/2+1}^{M-1}\frac{d^{(M)}_r}{r}
       \bigl(T^{(M)}_r+T^{(M)}_{r-1}\bigr).
\end{aligned}}
\tag{35.10}
\]

Every square and every packet belonging to an intermediate scale cancels
exactly.  This cancellation is between two identical copies of the complete
one-scale Abel decomposition: the scale `X_j` fine contribution in decrement
`j-1` and its coarse contribution in decrement `j`.  It is not a new
pointwise pairing between the right endpoint of one shell and the left endpoint
of the next.

## Obstruction

The dyadic sum gives no new favorable boundary structure.  Equation (35.9) is
the defining telescoping of endpoint energies, refined only by the fact that
the Abel boundary and interior packets telescope separately.  After all exact
cancellations, both outer scales still contain:

1. an indefinite boundary difference `H_N-H_M`, with two squares of opposite
   signs at each outer scale; and
2. an indefinite packet difference `P_N-P_M`, whose factors
   `A_X-Lambda(r)/log X` and `T_r^(X)+T_(r-1)^(X)` have no common sign.

Taking absolute values before (35.8) destroys the exact cancellation.  Taking
them after (35.8) still requires control of the two outer complete packets and
does not yield monotonicity.  Letting `J` grow would help only after an
independent theorem controlling the terminal energy or the correlated terminal
pair `H_M+P_M=E_M`; proving the needed decay or sign is the original
RH-strength obstruction for this approximant.  Thus Cycle 35 supplies an exact
bookkeeping result, not a contraction, a favorable residual boundary, or a new
RH implication.

## Certified analyzer and observed signs

`analyze_dyadic_abel_packets.py` evaluates (35.3) independently at every
requested scale, forms each adjacent difference as boundary and cumulative
packets, and checks packetwise and endpoint telescoping.  Its accepted domain
is a dyadic `base_N`, positive `depth`, and final shell scale at most `8192`.
At 192-bit Arb precision, the maximal run

```text
uv run --with python-flint python analyze_dyadic_abel_packets.py \
  --bits 192 --base-N 2 --depth 13
```

certifies all thirteen shell scales from `2` through `8192`.  The direct sum,
packet sum, and outer endpoint difference all overlap at

\[
 -5.26027807136.
\]

The separately telescoped interior boundary and cumulative residuals contain
zero, with radii below `2.1e-50` and `7.8e-47`, respectively.  The surviving
outer packets are approximately

\[
 H_2-H_{16384}=+2.77948999734,
 \qquad P_2-P_{16384}=-8.03976806870.
\]

The analyzer records maximal certified sign runs rather than inferring a trend.
For the thirteen decrements the sign word is

```text
++++--+-----
```

corresponding to `+` on scales `2..32`, `-` on `64..128`, `+` at `256`, and
`-` on `512..8192`.  The boundary and cumulative packet words are
`+++-+-+-++--+` and `++-+-+-+---+-`, respectively.  Their frequent sign
changes certify that neither separated packet has a stable finite sign pattern.
The test suite includes an exact rational Abel identity, sign-run detection,
input bounds, and the complete Arb telescope through shell scale `8192`:

```text
uv run --with python-flint python -m unittest -v \
  test_dyadic_abel_packets.py
```
