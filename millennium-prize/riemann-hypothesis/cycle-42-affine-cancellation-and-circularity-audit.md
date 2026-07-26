# Cycle 42: exact affine cancellation and circularity audit

## 1. Contract the finite-zero block before taking limits

Keep the notation of Cycle 41 and put

\[
 g_{T,k}=\sum_{\rho\in Z(T)}Z_{\rho,k}
         =\left(0,\sum_{\rho\in Z(T)}{k^\rho\over\rho}\right).
\]

For the complete-cell prefix define

\[
 \|W\|_K^2=\sum_{k\leq K}{\cal I}_k(W_k,W_k),
 \qquad
 G_{T,K}=\|g_T\|_K^2.
\]

The positive zero Gram is therefore

\[
 \boxed{
 G_{T,K}=\sum_{\rho,\sigma\in Z(T)}
 {1\over\bar\rho\sigma}\sum_{k\leq K}
 {k^{\bar\rho+\sigma}\over k(k+1)}\geq0.}                 \tag{42.1}
\]

It is independent of `n`.  The exact endpoint formula says

\[
 X_{n,T,k}-g_{T,k}=(\ell_n,v_{n,k}),
\]

not merely that the two sides are asymptotic.  Write the affine-row
contraction, excluding the zero-zero block, as

\[
 A_{n,T,K}:={\cal K}_{\star\star}^{(n,T,K)}
 +2\Re\sum_{\rho\in Z(T)}{
        \cal K}_{\star\rho}^{(n,T,K)}.                    \tag{42.2}
\]

Expanding `||X-g||_K^2` once, and only once, gives the required cancellation
identity

\[
 \boxed{A_{n,T,K}=H_{n,K}-G_{T,K},\qquad
        H_{n,K}=A_{n,T,K}+G_{T,K}.}                        \tag{42.3}
\]

Here

\[
 H_{n,K}=\sum_{k\leq K}
 \{\mathcal I_k((\ell_n,v_{n,k}),(\ell_n,v_{n,k}))
       -L_nL_{n+1}\mathcal I_k((m_n,u_{n,k}),(m_n,u_{n,k}))\}
\]

is the actual arithmetic prefix and is independent of `T`.  Thus (42.3) is
also a direct audit of all signs: the affine-zero cross terms occur with a
minus sign, and the pure zero Gram occurs with a plus sign.

For a scale block `[A,B)`, let

\[
 s_{A,B}=\sum_{n=A}^{B-1}\beta_n,
 \qquad
 A_{A,B;T,K}=\sum_{n=A}^{B-1}\beta_nA_{n,T,K}.
\]

Since the same finite zero wave occurs for every `n`, (42.3) sums to

\[
 \boxed{
 \mathfrak R_{1/2}(A,B;K)
 =A_{A,B;T,K}+s_{A,B}G_{T,K},}                             \tag{42.4}
\]

where `mathfrak R_(1/2)(A,B;K)=sum beta_n H_(n,K)`.  Consequently the exact
finite-prefix criterion is

\[
 \boxed{
 \mathfrak R_{1/2}(A,B;K)\geq0
 \quad\Longleftrightarrow\quad
 A_{A,B;T,K}\geq-s_{A,B}G_{T,K}.}                         \tag{42.5}
\]

This is the affine cancellation estimate that would be needed for block
positivity.  It is an exact reformulation, not an available bound.

## 2. Why positivity of the zero Gram does not give a lower bound

At fixed finite `T`, the separate terms on the right of (42.4) generally do
not have limits as `K` tends to infinity.  On RH, under simplicity, the
Hermitian diagonal gives

\[
 \sum_{\rho\in Z(T)}{H_{K+1}-1\over|\rho|^2},              \tag{42.6}
\]

and every off-diagonal sum has a nonzero frequency and is `O_T(1)`.  Hence

\[
 G_{T,K}=(H_{K+1}-1)\sum_{\rho\in Z(T)}|\rho|^{-2}+O_T(1),
                                                               \tag{42.6a}
\]

with equal ordinates grouped if multiplicities are allowed.  Thus the complete
arithmetic prefix tending to the finite `H_n` forces the affine row to contain
the opposite logarithmic contribution.  Equation (42.3) identifies that
cancellation exactly.  The finite-cutoff remainder
`r_T`, the endpoint packet, and the affine-zero cross terms cannot be dropped
or estimated independently and then sent to infinity.

In particular, retaining `G_(T,K)>=0` while discarding the affine row is not a
valid lower bound for `H_n`.  Conversely, proving (42.5) with the sharp main
term `-s_(A,B)G_(T,K)` already proves the desired finite-prefix block sign.
There is no free positivity left after the mandatory affine cancellation.

The safe infinite-cell statement is only the contracted limit

\[
 \boxed{
 \mathfrak R_{1/2}(A,B)
 =\lim_{K\to\infty}
   \{A_{A,B;T,K}+s_{A,B}G_{T,K}\}.}                        \tag{42.7}
\]

No limit of the two summands is asserted separately.

## 3. Comparison with a second-order coefficient

The exact recurrence gives

\[
 L_{n+1}P_{n+1}-L_nP_n
 =-{(L_{n+1}-L_n)H_n\over L_nL_{n+1}}.                     \tag{42.8}
\]

If the pointwise expansion

\[
 P_n={C_0\over L_n}+{D_{\rm restricted}\over L_n^2}
       +o(L_n^{-2})
\]

has a remainder regular enough to difference, then

\[
 H_n=D_{\rm restricted}+o(1)=D_{\rm full}-1+o(1).          \tag{42.9}
\]

Thus `D_full>1` implies eventual singleton positivity `H_n>0`, and hence block
positivity with `B=A+1` for every sufficiently large start.  At the asymptotic
level this scalar second-order theorem is stronger than what the stopping
argument needs.  It does not by itself repay a weighted debt attached to one
of the finitely many earlier starts; those starts require a separate finite
check or estimate.

The stopping theorem only asks that, for every start `A`, some finite endpoint
`B>A` satisfy

\[
 \sum_{n=A}^{B-1}\beta_nH_n\geq0.                          \tag{42.10}
\]

It permits infinitely many negative `H_n`, oscillatory nonzero-frequency zero
pairs, and failure of a scalar second coefficient.  As a statement about an
abstract sequence, (42.10) is therefore a weaker, adaptive weighted-average
condition than (42.9) with a positive limit.  It is not equivalent to existence
or positivity of the second-order coefficient.

There is an important logical qualification: for the physical Nyman--Beurling
sequence, every-start stopping plus the divergent renewal weight is already an
RH-sufficient theorem.  Calling it "averaged" does not make it an easy or
RH-neutral consequence.

## 4. Circularity audit

1. **Finite-zero algebra is unconditional.** Equations (42.1)--(42.7) use a
   finite symmetric zero set and the remainder defined by exact equality.  They
   do not require RH and prove no sign.

2. **The RH diagonal cannot prove RH.** Using `rho=1/2+i gamma` to obtain
   (42.6) is conditional on RH.  Any block-positivity proof that depends on
   this specialization is at best an RH-conditional positivity result and
   cannot be fed into the RH-sufficient stopping theorem to establish RH.

3. **The coefficient route is conditional twice.** Cycle 40 assumes RH and
   strong zero-sum/finite-part convergence to define `D_full`.  It does not
   prove `D_full>1`.  Assuming that sign and then invoking (42.9) proves only a
   conditional block theorem, not RH.

4. **The sharp affine estimate is the target.** By (42.5), an asserted bound
   `A_(A,B;T,K)>=-s_(A,B)G_(T,K)` is exactly the desired block inequality at
   finite prefix.  Deriving it from block positivity, from `Q_A>=0`, or from
   the second-order sign and then presenting it as an independent zero-Gram
   bound is circular.

5. **Separate limiting arguments are invalid.** Taking `K` or `T` limits of
   the positive zero block and affine row separately discards the cancellation
   encoded by `r_T`.  A valid proof must control their contracted combination,
   uniformly in the stated order of limits.

6. **A genuinely new theorem must add arithmetic content.** It must prove a
   cancellation estimate for the combined affine/zero/endpoints packet from
   unconditional finite arithmetic data, or directly prove the finite
   weighted passage (42.10), without assuming RH, a positive second
   coefficient, or the desired residual sign.

## 5. Verdict

The exact identity is (42.4), and the exact required estimate is (42.5).  The
positive zero Gram is canceled at leading order by the affine row; its
positivity alone cannot establish `H` block positivity.  A positive,
difference-stable second-order coefficient would imply a stronger eventual
singleton theorem, whereas adaptive weighted block positivity is formally
weaker and does not require a scalar coefficient.  Neither conclusion is
currently proved, and using RH diagonalization or the conditional second-order
framework in an RH proof would be circular.
