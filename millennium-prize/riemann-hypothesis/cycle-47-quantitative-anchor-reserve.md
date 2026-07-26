# Cycle 47: quantitative anchor reserve and exact cell obstruction

## A scale-correct reserve identity

Retain the Cycle 45 packets

\[
X_b=\sum_{r=M}^{b-1}W_{M,r}h_rD_r,
\qquad
\alpha_b={w_b\over W_{M,b}W_{M,b-1}},
\]

and put `A_(M,r)=-<F_M,D_r>`. The aggregate weighted anchor reserve is

\[
S_{M,B}=\sum_{b=M+1}^B\alpha_b[-\langle F_M,X_b\rangle].
\]

Since

\[
\alpha_b={1\over W_{M,b-1}}-{1\over W_{M,b}},
\]

finite reversal of sums gives

\[
\boxed{
S_{M,B}=\sum_{r=M}^{B-1}h_rA_{M,r}
\left(1-{W_{M,r}\over W_{M,B}}\right).}          \tag{47.1}
\]

The online weighted-mean identity also gives the simpler geometric form

\[
\boxed{S_{M,B}=P_M-\langle F_M,\bar F_{M,B}\rangle.}     \tag{47.2}
\]

These formulas put the reserve on the same quadratic scale as the physical
dispersion `V_(M,B)=sum alpha_b||X_b||^2`.

A tempting packet target is

\[
-\langle F_M,X_b\rangle\ge\|X_b\|^2.             \tag{47.3}
\]

It would imply `V_(M,B)<=S_(M,B)`, but not `V_(M,B)<=P_M`: by (47.2) one
still needs a sign or lower bound for `<F_M,bar F>`. For the truncated terminal
budget its strongest immediate consequence is only

\[
Q_{M,B}\ge\langle F_M,\bar F_{M,B}\rangle
-W_{M,B}\|\bar F_{M,B}\|^2,                     \tag{47.4}
\]

whose right side is sign-indefinite. Thus even the stronger packet inequality
would not close the terminal problem by itself.

## Finite quantitative diagnostics

Complete 192-bit restricted Vasyunin computations through endpoint `512`
certify the following minima:

\[
\min_{2\le M\le r\le512}
{-\langle F_M,D_r\rangle\over h_r\|D_r\|^2}
=5.91424402312137610159579574084282\ldots,        \tag{47.5}
\]

attained at `(M,r)=(2,2)`, and

\[
\min_{2\le M<b\le512}
{-\langle F_M,X_b\rangle\over\|X_b\|^2}
=1.25580212023797953527552387329982\ldots,        \tag{47.6}
\]

attained at `(M,b)=(2,512)`. The aggregate ratio has minimum

\[
\min_{2\le M<B\le512}{S_{M,B}\over V_{M,B}}
=2.58341091294259266393361730361488\ldots,        \tag{47.7}
\]

again at `(2,512)`. These certify finite margins only. In particular `(2,2)`
rules out an atomic constant `6`, `(2,512)` rules out packet constant `2`, and
the endpoint drift prevents extrapolating constant `1` from this box.

The atomic sign itself was extended independently: every one of the `523776`
correlations `<F_M,D_r>` with `2<=M<=r<=1024` is certified negative at 160-bit
precision. Selected adversarial rows, including every known negative-`H`
episode, remain negative through `r=2304`. This remains finite evidence, not an
asymptotic theorem.

## Exact unit-cell expansion

In reciprocal coordinates `t=1/x`, write

\[
m_M=\sum_{a\le M}{\mu(a)\over a},\quad
\ell_r=\sum_{q\le r}{\mu(q)\log q\over q},\quad
A_M=m_M-{\ell_M\over\log M},
\]

and on the cell `k<t<k+1` put

\[
b_{M,k}=1-\sum_{a\le M}\mu(a)
\left(1-{\log a\over\log M}\right)\lfloor k/a\rfloor,
\]

\[
v_{r,k}=-\sum_{q\le r}\mu(q)\log q\,\lfloor k/q\rfloor.
\]

Then `F_M=A_Mt+b_(M,k)` and `D_r=ell_r t+v_(r,k)`, so

\[
\boxed{
\langle F_M,D_r\rangle=\sum_{k\ge1}\left[
A_M\ell_r+(A_Mv_{r,k}+\ell_rb_{M,k})\log(1+1/k)
+{b_{M,k}v_{r,k}\over k(k+1)}\right].}           \tag{47.8}
\]

The sum is taken in complete cells; its individually nonsummable channels must
not be separated at infinity. For `k<=M`, divisor convolution gives

\[
b_{M,k}=-{\psi(k)\over\log M},\qquad v_{r,k}=\psi(k),
\]

and the cell becomes

\[
A_M\ell_r+\psi(k)\left(A_M-{\ell_r\over\log M}\right)
\log(1+1/k)-{\psi(k)^2\over\log M\,k(k+1)}.       \tag{47.9}
\]

On `M<k<=r`, only `v_(r,k)=psi(k)` remains valid; replacing `b_(M,k)` by its
Chebyshev expression there is false. Beyond `r`, both coordinates are truncated
divisor-floor transforms. Therefore elementary Chebyshev bounds determine only
the initial packet and cannot sign (47.8). Absolute values destroy the internal
cancellation, while square-root Mertens input would import RH-strength
information rather than prove it.

The exact obstruction is a two-cutoff signed Mobius divisor-floor correlation.
The next target is a coupled estimate in which its negative anchor reserve pays
both the packet squares and the coherent weighted-mean channel. No terminal
sign theorem or RH result is claimed.
