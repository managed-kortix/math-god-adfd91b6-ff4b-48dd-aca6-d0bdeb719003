# Cycle 51: exact additive-12 target and certified frontier

## The RH-sufficient target

Put

\[
\beta_n={\log(n+1)-\log n\over
\log n\,\log^2(n+1)},
\qquad
w_n=1-{\log n\over\log(n+1)}.
\]

The fixed half-strength additive-12 candidate is

\[
\boxed{
\forall M\ge3\ \exists B\in\{M+1,\ldots,M+12\}:\quad
\sum_{n=M}^{B-1}\beta_nH_n\ge0.}                 \tag{51.1}
\]

By the exact singleton recurrence, this is equivalent endpoint by endpoint to

\[
\boxed{P_M-P_B\ge\sum_{n=M}^{B-1}w_nP_n.}        \tag{51.2}
\]

Equivalently, with `S_M(r)=sum_(j=0)^(r-1) beta_(M+j)H_(M+j)`, the complete
local condition is

\[
\boxed{\max_{1\le r\le12}S_M(r)\ge0.}            \tag{51.3}
\]

The full twelve-cell sum need not be nonnegative; an earlier successful prefix
is enough.

A proof for every `M` would be RH-sufficient in this funnel. Iterating the
successful endpoints gives consecutive blocks covering the tail and

\[
\sum_{n\ge3}w_nP_n\le P_3<\infty.
\]

Since `sum w_n=infinity`, this forces `liminf P_n=0`, which is the established
Nyman--Beurling sufficient criterion used here. No converse from RH to (51.1)
is known; the target may be strictly stronger than RH.

## Exact impulse budget

Let

\[
H_q-H_{q-1}=-A_q+J_q,
\qquad A_q\ge0,
\]

with `J_q=0` when `mu(q)=0`, and define

\[
\mathcal B_{q,B}=\sum_{n=q}^{B-1}\beta_n.
\]

Then the correctly indexed forms are

\[
\boxed{
\sum_{n=M}^{B-1}\beta_nH_n
=\mathcal B_{M,B}H_{M-1}
-\sum_{q=M}^{B-1}\mathcal B_{q,B}A_q
+\sum_{q=M}^{B-1}\mathcal B_{q,B}J_q,}           \tag{51.4}
\]

and, equivalently,

\[
\boxed{
\sum_{n=M}^{B-1}\beta_nH_n
=\mathcal B_{M,B}H_M
-\sum_{q=M+1}^{B-1}\mathcal B_{q,B}A_q
+\sum_{q=M+1}^{B-1}\mathcal B_{q,B}J_q.}         \tag{51.5}
\]

The first form includes the event at `q=M`; the second absorbs it into `H_M`.
Neither includes `q=B`.

Thus occurrence or sign data for squarefree events cannot prove (51.1). The
favorable impulses must quantitatively pay the incoming debt, all radial drift,
and every adverse impulse with the correct triangular weights. By CRT there
are arbitrarily long intervals containing no squarefree integer at all, and
even primes need not have favorable `J_q`. The missing input is a complete
Vasyunin correlation budget, not a fixed-gap theorem.

## Certified finite extension

The complete restricted Vasyunin scan was extended at 192-bit Arb precision.
The repository certificate bundle `cycle51-scan-3072/` contains four compressed
JSONL streams, summaries, and resume checkpoints. Together with the prior
checkpoint, they certify local cells through `n=3071` and energies through
`P_3072`.

The exact finite findings are:

- the only negative `H_n`, and the only local half-strength failures, through
  `3071` remain
  `2,39,40,95,96,99,100,219,220,221,222,226`;
- every local cell `227<=n<=3071` succeeds immediately;
- every start `3<=M<=3060` has a fully tested successful endpoint within twelve
  cells;
- starts `3061,...,3071` have certified singleton success, but their complete
  twelve-future-cell windows are not present;
- the historical longest first recovery remains `[219,231)`, length twelve;
- the weakest new local ratio on `2304<=n<=3071` is at `n=2656` and equals
  `0.675813756182894001113034643508481...>1/2`.

The distinction between cell and window frontiers is essential. This finite
extension supplies no asymptotic stopping theorem and no RH result.

## Reproduction

The summaries contain the uncompressed certificate hashes. Reproduce each leg
with `cycle41_local_scan.py`, beginning from `cycle42-checkpoint-2304.json` and
using the successive checkpoints in `cycle51-scan-3072/`. The exact commands
and provenance are recorded in `cycle51-scan-3072/README.md`.
