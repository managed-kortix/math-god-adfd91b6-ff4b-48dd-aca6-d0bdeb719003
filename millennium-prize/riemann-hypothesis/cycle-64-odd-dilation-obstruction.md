# Cycle 64: exact odd-dilation obstruction

## Three-level physical completion

On `H_(2M)=L^2([2M,infinity),dt/t^2)`, let

\[
(J_Mf)(t)=\sqrt2 f(t/2),
\]

so `J_M rho_q=sqrt(2) rho_(2q)`. Define

\[
e_U=\sqrt2U_{2M-1}-J_MU_{M-1},\qquad
e_D=\sqrt2D_{2M-1}-J_MD_{M-1}.
\]

The affine `chi` term cancels exactly. Splitting every squarefree even index as
twice an odd index gives

\[
\boxed{
{e_U\over\sqrt2}=
\sum_{\substack{r<2M\\r\ odd}}\mu(r)\rho_r
-2\sum_{\substack{r<M\\r\ odd}}\mu(r)\rho_{2r}
+\sum_{\substack{2r<M\\r\ odd}}\mu(r)\rho_{4r}.}                 \tag{64.1}
\]

Similarly,

\[
\boxed{
\begin{aligned}
{e_D\over\sqrt2}={}&
\sum_{\substack{r<2M\\r\ odd}}\mu(r)\log r\,\rho_r\\
&-\sum_{\substack{r<M\\r\ odd}}
\mu(r)(\log(2r)+\log r)\rho_{2r}\\
&+\sum_{\substack{2r<M\\r\ odd}}
\mu(r)\log(2r)\rho_{4r}.
\end{aligned}}                                                   \tag{64.2}
\]

An independent symbolic audit checked the coefficient dictionaries exactly for
every `2<=M<=64`. The strict ranges and all logarithmic factors matter.

## Exact affine and odd-row Schur identity

First replace the transported affine row and score by their physical completed
versions, but do not add new odd reciprocal constraints. If `G_0,b_0,d_0` are
the transported Gram data and `Delta G,delta b,delta d` their completion
perturbations, put

\[
x_0=G_0^{-1}b_0,\qquad h=\delta b-\Delta Gx_0.
\]

Then

\[
\boxed{
\Omega_E-\Omega_{M,B}
=\delta d-2\Re(x_0^*\delta b)+x_0^*\Delta Gx_0
-h^*G_E^{-1}h.}                                    \tag{64.3}
\]

Now let `O` be the genuinely new odd rows `sqrt(2)rho_j`,
`2M<=j<2B`. With

\[
S_{odd}=\langle(I-P_E)O,(I-P_E)O\rangle,
\]

\[
g_{odd}=\langle(I-P_E)O,(I-P_E)s\rangle,
\]

the complete physical dilation identity is

\[
\boxed{
2\Omega_{2M,2B}=\Omega_E-g_{odd}^*S_{odd}^{+}g_{odd}.}           \tag{64.4}
\]

The last term is exactly the positive amount of transported/completed
innovation erased by the residualized odd rows. Thus a fixed-fraction survival
theorem is precisely an arithmetic angle estimate

\[
g_{odd}^*S_{odd}^{+}g_{odd}\le(1-\kappa)\Omega_E.                 \tag{64.5}
\]

Positivity, interlacing, dilation, and rank do not imply (64.5).

## Finite diagnostic: separate norms are too lossy

Exact rational floor constraints and 192-bit Arb were used to compare the two
successive scale innovations and a triangle-inequality remainder. On historical
stress windows, the common-kernel score remainder has norm about `0.135--0.151`,
while the first innovation square root is about `0.114--0.132`. The resulting
criterion is vacuous. Near the certified frontier the ratio of this remainder
to the innovation square root is about `1.36`.

Constraint-kernel mismatch itself is much smaller; physical score
noncovariance dominates. Successive innovation ratios also move both below and
above one. Hence neither monotone contraction nor a norm-small odd remainder is
supported by finite data. A useful proof must retain signed covariance in
(64.3)--(64.4), not estimate the defects separately.

## Square-wave simplification

Define the exact square wave

\[
J_r(t)=2\rho_{2r}(t)-\rho_r(t)
=\mathbf1_{\{\lfloor t/r\rfloor\ odd\}}.
\]

Every packet `A rho_r+B rho_(2r)+C rho_(4r)` is one affine reciprocal row plus
two nested square-wave rows. The affine part disappears exactly when
`4A+2B+C=0`. This reveals the jump structure, but jumps from different odd
indices overlap by divisibility and do not become orthogonal or low rank.

Polarizing the odd Schur kernel gives

\[
\boxed{
\mathcal S_N(a,b)={1\over2}
\sum_{\substack{N<r<2N\\r\ odd}}{1\over r^2}
\left(\sum_{d\mid r}a_d\right)
\left(\sum_{e\mid r}b_e\right).}                  \tag{64.6}
\]

For Möbius logarithmic tapers the divisor sums are von Mangoldt values, so the
positive diagonal becomes

\[
{1\over2\log X\log Y}
\sum_{\substack{N<r<2N\\r\ odd}}{\Lambda(r)^2\over r^2}.         \tag{64.7}
\]

Weighted PNT controls (64.7), but not the signed cross-window rectangle in the
full centered Chebyshev covariance. The exact unresolved channel can be written

\[
\boxed{
\left|C_N- {\log(2N)\over\log N}A_N\right|
\le \log N\log(2N)B_N,}                            \tag{64.8}
\]

where `A_N` is the centered Chebyshev diagonal energy and `C_N` is its signed
two-scale covariance including the odd von Mangoldt endpoint. PNT-level
one-point information does not imply (64.8); even an RH-scale pointwise error
used through absolute values is insufficient in exact block countermodels.

Cycle 64 therefore sharpens the active target from an unspecified dilation
remainder to the signed covariance (64.8), equivalently the physical odd-row
angle (64.5). No additive-12 theorem or RH result is claimed.
