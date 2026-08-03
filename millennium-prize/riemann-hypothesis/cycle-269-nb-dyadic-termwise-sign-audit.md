# Cycle 269: dyadic endpoint termwise-sign audit

## Decision

`R269-NB-TERM-SIGN` stops at a symbolic obstruction and one bounded certified
scale.  The unresolved quadratic numerator in (264.9) is exactly a difference
of two squared endpoint residuals.  Complete Mobius divisor identities evaluate
it on the Chebyshev prefix, but after that prefix they do not order the two
squares.  No sign of the complete functional follows.

At the bounded small scale `N=8`, exact interval arithmetic gives both a
positive and a negative grouped
cell.  Thus a proof of (264.9) cannot make every grouped cell nonnegative.  The
negative cell is produced by cancellation among individually much larger
constant, linear, and quadratic pieces; in particular it is not a negative
witness for the quadratic numerator itself.

## Exact polarization

For a cutoff `Y`, define the integer-endpoint floor transform and its residual

\[
 S_Y(k)=\sum_{a<Y}c_a(Y)\left\lfloor{k\over a}\right\rfloor,
 \qquad R_Y(k)=S_Y(k)-1.
\tag{269.1}
\]

The coefficient identity `c_a(N)-c_a(2N)=alpha d_a`, including the zero
extensions through `2N`, gives

\[
 X_k-S_{2N}(k)=\alpha Y_k,
 \qquad Y_k={R_N(k)-R_{2N}(k)\over\alpha}.
\tag{269.2}
\]

Consequently the difficult numerator has the exact polarization

\[
 \boxed{2(X_k-1)Y_k-\alpha Y_k^2
 ={R_N(k)^2-R_{2N}(k)^2\over\alpha}.}
\tag{269.3}
\]

Thus its sign is precisely the pointwise assertion

\[
 |R_{2N}(k)|\leq |R_N(k)|.
\tag{269.4}
\]

This is not supplied by Gram positivity: (269.3) is a difference of squares,
not a square.  Nor does ordinary Mobius inversion settle it past the complete
range.  For `k<=N`, the identities in (264.7) give

\[
 R_N(k)={\psi(k)\over\log N},\qquad
 R_{2N}(k)={\psi(k)\over\log(2N)}.
\]

Equivalently, in the normalized Cycle 264 variables,

\[
 X_k-1=Y_k={\psi(k)\over\log N},\qquad
 2(X_k-1)Y_k-\alpha Y_k^2
 =(2-\alpha){\psi(k)^2\over(\log N)^2}\geq0.
\tag{269.5}
\]

After `k>N`, the omitted divisors differ at the two cutoffs and the complete
convolutions `sum_(a|n) mu(a)` and `sum_(a|n) mu(a) log a` no longer evaluate
either residual.  Applying them merely restores the truncated Mobius tails;
it does not prove (269.4).  Equation (269.3) therefore isolates the required
new input rather than deriving a global sign.

## Certified opposite-sign cells

Let `B_(N,k)` denote the entire bracket in (264.9).  At `N=8`, `alpha=1/4`,
the exact coefficients give

\[
 A\in[0.47811954789244096537\ldots],\qquad
 D\in[0.47205418929713026397\ldots],
\]

and

\[
 C=2AD-\alpha D^2
 \in[0.3956878817267106100627138186290\ldots]>0.
\tag{269.6}
\]

For `k=1`, `X_1=1` and `Y_1=0`, hence

\[
 B_{8,1}=C>0.
\tag{269.7}
\]

For `k=35`, 256-bit Arb evaluation from the exact logarithmic expressions
certifies

\[
\begin{aligned}
 X_{35}&=17.2666820929421646870081720854\ldots,\\
 Y_{35}&=16.8817831207424209147594713065\ldots,\\
 C&= 0.395687881726710610062713818629\ldots,\\
 L_{35}&=-0.775149108595142455738597203548\ldots,\\
 {Q_{35}\over35\cdot36}
 &=0.379343292095462012590776233301\ldots,
\end{aligned}
\tag{269.8}
\]

where `L_35` is the logarithmic linear piece and `Q_35` is the numerator in
(269.3).  Therefore

\[
 \boxed{B_{8,35}
 =-0.000117934772969833085107151618106\ldots<0.}
\tag{269.9}
\]

The same certificate gives
`Q_35=477.972548040282135864378053959...>0`.  Hence the negative grouped cell
does not answer the stronger question whether every actual `Q_k` is positive;
it answers the architecture question: neither grouped-cell positivity nor the
sign of the quadratic channel alone can prove the total sum term by term.

The reproducible command is

```text
uv run --with python-flint python millennium-prize/riemann-hypothesis/verify_cycle269_nb_dyadic_termwise.py
```

## Stop rule

The symbolic obstruction (269.3) was found, so only the bounded small scale
`N=8` was certified.  No larger-scale search, cutoff escalation, conjecture of
global quadratic positivity, endpoint-monotonicity claim, or RH claim is made.
