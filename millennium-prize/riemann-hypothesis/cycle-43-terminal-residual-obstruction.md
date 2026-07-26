# Cycle 43: terminal residual identity and scalar closure obstruction

## Scope

This note isolates the terminal term in the half-strength renewal budget. The
finite identity applies to the physical Mobius--Vasyunin path. The hostile
continuations below are only scalar paths: they show that generic monotonicity
and finite weighted energy cannot control the terminal term. They are not
physical continuations and do not prove or disprove RH.

Put `L_n=log n` and

\[
w_n=1-{L_n\over L_{n+1}},\qquad
\beta_n={L_{n+1}-L_n\over L_nL_{n+1}^2}.
\]

Suppose

\[
P_n-P_{n+1}-w_nP_n=\beta_nH_n,                  \tag{43.1}
\]

the tail `T_a=sum_(n>=a)w_nP_n` converges, and `Q_a=P_a-T_a`.
For `a<=q<M`, write

\[
B_{q,M}=\sum_{n=q}^{M-1}\beta_n.
\]

## Exact terminal identity

**Lemma 43.1.** For every `a<M`,

\[
Q_a-Q_M=\sum_{n=a}^{M-1}\beta_nH_n.             \tag{43.2}
\]

If, for `a<q<M`,

\[
H_q-H_{q-1}=-A_q+J_q,                            \tag{43.3}
\]

then

\[
\boxed{Q_a=Q_M+B_{a,M}H_a
-\sum_{q=a+1}^{M-1}B_{q,M}A_q
+\sum_{q=a+1}^{M-1}B_{q,M}J_q.}                 \tag{43.4}
\]

For the physical Cycle 41 recurrence, `A_q>=0` and `J_q=0` when
`mu(q)=0`, so the last sum may be restricted to squarefree indices.

**Proof.** Since `T_a=w_aP_a+T_(a+1)`, (43.1) gives
`Q_a-Q_(a+1)=beta_a H_a`. Summing proves (43.2). Also

\[
H_n=H_a+\sum_{q=a+1}^n(-A_q+J_q).
\]

Insert this into the finite sum in (43.2) and reverse the order of summation.
The coefficient of the `q`th increment is exactly `B_(q,M)`, proving (43.4).

Thus a finite impulse computation does not close the infinite budget: it
leaves the exact terminal scalar `Q_M`.

## Scalar terminal no-go theorem

**Proposition 43.2.** Fix a finite nonnegative nonincreasing scalar prefix
through `P_M=p>0`, with its residual data prescribed only through index
`M-1`. There are nonnegative nonincreasing continuations with finite weighted
energy and satisfying (43.1), after defining the future `H_n` by that identity,
for which `Q_M>0`; there are also such continuations for which `Q_M<0`.

For the positive continuation, choose any real `s>1` and set

\[
P_n=p\left({L_M\over L_n}\right)^s\quad(n\ge M).
\]

With `r_n=L_n/L_(n+1)`,

\[
P_n-P_{n+1}=P_n(1-r_n^s)>P_n(1-r_n)=w_nP_n.
\]

Hence the tail sum is strictly smaller than the telescoping variation `P_M`,
and `Q_M>0`.

For the negative continuation, choose `N>=M` so that
`sum_(n=M)^N w_n>1`, which is possible because `sum w_n` diverges. Set

\[
P_n=p\ (M\le n\le N),\qquad P_n=0\ (n>N).
\]

Then the weighted tail is finite and

\[
Q_M=p\left(1-\sum_{n=M}^Nw_n\right)<0.
\]

Both constructions preserve the fixed prefix and scalar recurrence. The
condition `p>0` is necessary for this two-sided construction under
nonnegativity and monotonicity.

The critical profile deserves separate mention. If `P_n=C/L_n`, then

\[
P_{n+1}=(1-w_n)P_n,
\qquad
w_nP_n=C(1/L_n-1/L_{n+1}),
\]

so every residual in (43.1) is zero and `Q_M=0`. Positive terminal budget
requires faster decay, not the exactly reciprocal-log equality profile.

## Consequence and limitation

Nonnegativity and monotonicity of `P_n`, finite weighted energy, and the scalar
half-strength recurrence do not determine the sign of `Q_M`. Any finite
certificate that drops `Q_M`, assumes it tends to zero, or bounds it from those
generic facts alone has an unproved terminal step.

The physical future is not freely selectable: its `P,H,A,J` are fixed by the
Mobius coefficients and the fractional-part Gram geometry, and its `J_q` has a
specific squarefree-supported correlation formula. Proposition 43.2 therefore
does not refute a physical inequality `Q_M>=0`. It proves that such an
inequality must use genuinely future Mobius--Vasyunin arithmetic, for example a
uniform weighted impulse budget. No RH result is claimed.

## Reproduction

The finite summation and index conventions have a dependency-free exact
rational audit:

```text
python verify_cycle43_terminal_identity.py
```
