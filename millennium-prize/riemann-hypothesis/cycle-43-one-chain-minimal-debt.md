# Cycle 43: one-chain minimal-debt renewal theorem

## 1. Exact residual

Retain the physical weights

\[
 w_n={\log(1+1/n)\over\log(n+1)},\qquad
 \beta_n={\log(1+1/n)\over\log n\,\log^2(n+1)},
\]

and the exact identity

\[
 P_a-P_b-\sum_{a\le n<b}w_nP_n
 =R(a,b):=\sum_{a\le n<b}\beta_nH_n.                     \tag{43.16}
\]

The following theorem is deterministic. It distinguishes one recursively
generated chain from the stronger every-start stopping property.

## 2. Minimal-debt theorem

Fix one initial index `a_0`. At the current endpoint `a_j`, choose a finite
provisional episode endpoint `q_j>a_j` and put

\[
 Z_j=R(a_j,q_j),\qquad D_j=(-Z_j)_+.
\]

If `D_j=0`, set `a_(j+1)=q_j`. Otherwise choose the first finite `t>=q_j`
such that

\[
 R(q_j,t)\ge D_j,                                        \tag{43.17}
\]

and set `a_(j+1)=t`.

**Theorem.** If every requested crossing (43.17) is attained at a finite
index, then

\[
 R(a_j,a_{j+1})\ge0                                      \tag{43.18}
\]

for every `j`, the intervals form a consecutive partition of the tail, and

\[
 \sum_{n\ge a_0}w_nP_n\le P_{a_0}.                       \tag{43.19}
\]

Consequently `liminf P_n=0`.

**Proof.** Equation (43.17) gives

\[
 R(a_j,a_{j+1})=Z_j+R(q_j,a_{j+1})\ge0.
\]

Substitute this into (43.16):

\[
 P_{a_j}-P_{a_{j+1}}
 \ge\sum_{a_j\le n<a_{j+1}}w_nP_n.
\]

Summing consecutive blocks telescopes all endpoints and counts every interior
index once. Nonnegativity of `P` gives (43.19). Since `sum w_n` diverges, a
positive eventual lower bound for `P_n` would contradict (43.19). QED.

When `Z_j<0`, `D_j=-Z_j` is the exact extension debt: a later endpoint recovers
the current start exactly when its signed gain is at least this quantity. When
`Z_j>=0`, no extension is needed and the algorithm stops the block at `q_j`;
if one nevertheless extends farther, the exact threshold is `-Z_j`, not zero.
The larger maximal-suffix debt from Cycle 42 is needed only when one common
window must recover every interior start. It is not needed for a single
generated chain. Positive terms inside the episode must remain in the signed
sum; replacing `D_j` by the sum of negative parts is a strictly stronger
demand.

## 3. Sharp incomplete-payment variants

For any consecutive chain put

\[
 R_j=R(a_j,a_{j+1}),\qquad
 B_j=\sum_{a_j\le n<a_{j+1}}w_nP_n.
\]

Summing (43.16) shows that the weaker condition

\[
 \sup_J\left(-\sum_{j<J}R_j\right)<\infty                \tag{43.20}
\]

already implies bounded total weighted energy and hence `liminf P_n=0`.
This sufficient additive condition allows earlier positive residual credit to
pay later deficits. The convenient condition `sum_j(-R_j)_+<infinity` is a
stronger sufficient condition; neither is asserted necessary without further
control of endpoint energies.

There is also a multiplicative version. If numbers `0<=c_j<=1` satisfy

\[
 R_j\ge-(1-c_j)B_j,                                      \tag{43.21}
\]

then

\[
 P_{a_j}-P_{a_{j+1}}\ge c_jB_j.
\]

Thus the variable-block argument works whenever the **post-loss** effective
mass diverges:

\[
 \sum_jc_j\sum_{a_j\le n<a_{j+1}}w_n=\infty.             \tag{43.22}
\]

Nominal divergence before the factors `c_j` are applied is insufficient.

## 4. Quantifier and scope audit

One-chain recovery is strictly weaker than every-start recovery. A signed
sequence can have `R(2,4)=0` while `R(3,b)<0` for every `b>=4`; the chain may
take the first block `[2,4)` and then continue through zero-residual cells,
although the skipped start `3` never recovers. Likewise, compensation that
approaches the debt only in the infinite limit is insufficient: (43.17)
requires finite attainment.

The theorem does not prove the needed Mobius compensation. It sharpens its
quantifier: it is enough to pay debts encountered along one consecutive,
recursively generated chain. If this is proved with full payment, no
scale-dependent dissipation is lost. If only proportional payment is proved,
(43.22) must be checked after every arithmetic, projection, and block-selection
loss. No RH result is claimed.
