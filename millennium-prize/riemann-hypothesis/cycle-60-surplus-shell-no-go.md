# Cycle 60: surplus-shell optimization and boundary nonvanishing

## The matched-shell boundary never degenerates

Put

\[
m_n=\sum_{a\le n}{\mu(a)\over a},\qquad
L_n=\operatorname{lcm}(1,\ldots,n).
\]

Then

\[
\boxed{m_n\ne0\quad(n\ge1).}                       \tag{60.1}
\]

For `n>1`, Bertrand's postulate gives a prime `n/2<p<=n`. In the integer

\[
L_nm_n=\sum_{a\le n}\mu(a)L_n/a,
\]

every term except `a=p` is divisible by `p`: no other `a<=n` is divisible by
`p`. The surviving term is `-L_n/p`, nonzero modulo `p` because `p^2>n`.
The case `n=1` is immediate.

Consequently the Cycle 59 matched-shell equation `m_(B-1)A=0` always forces
`A=0`, after which the triangular floor equations kill every detectable cell
mass. There is no exceptional integer endpoint.

## Eliminating the cell-linear moments

For a cell set `K`, put

\[
p_k={\lambda_k\over\tau_k},\qquad
d_k={\Delta_k\over\tau_k},\qquad S_K=\sum_{k\in K}d_k.
\]

For fixed total `A` and masses `B_k`, minimization over the individual `A_k`
in the Cycle 59 metric gives

\[
\boxed{A_k^*=p_kB_k+{d_k\over S_K}
\left(A-\sum_jp_jB_j\right),}                     \tag{60.2}
\]

and

\[
\boxed{\mathcal E_K(A,B)=
\sum_k{B_k^2\over\tau_k}
+{(A-\sum_kp_kB_k)^2\over S_K}.}                  \tag{60.3}
\]

Thus surplus-shell optimization is a rational floor-nullspace calculation
followed by one positive-definite logarithmic quadratic solve. For one surplus
cell `j`, if `n_j` is the forced null vector, the exact score is

\[
\boxed{\Omega_j={(w^Tn_j)^2\over n_j^TQ_Kn_j}.}   \tag{60.4}
\]

For two cells the gain is the corresponding two-by-two Schur quotient. These
formulas show that the next cell should be chosen by residual correlation after
metric projection, not merely by distance from the cutoff. Floor-signature
jumps near `j=2q` are natural sparse candidates.

## Certified consecutive-surplus experiment

For each critical window below, optimize the full Cycle 59 quotient over

\[
K_s=\{M,M+1,\ldots,B+s-1\},\qquad1\le s\le24.
\]

The floor constraints and nullspaces are exact over the rationals; logarithms
and the final positive-definite solve use 256-bit Arb balls. The best member is
always `s=24`:

| window | `Omega_(K_24)` | fraction of `beta_2+delta` |
|---|---:|---:|
| `[98,99)` | `0.00276877263226352708` | `0.0342131` |
| `[219,231)` | `0.00108445069951682313` | `0.0225748` |
| `[220,231)` | `0.00108172461837439381` | `0.0580412` |
| `[222,226)` | `0.00137405221940718224` | `0.0344793` |

None pays the required residual target. For `[98,99)`, one and two consecutive
surplus cells have identically zero arithmetic numerator; the first nonzero
correlation appears at three cells. Growing nullity alone is therefore not the
missing mechanism.

The finite no-go redirects the search from consecutive local shells to sparse
cells selected at arithmetic or floor-signature jumps, or to a genuinely
global correlation theorem. It proves no additive-12 theorem or RH result.
