# Aggregate surrogate sign audit

## Question

Can the sign required in the dyadic shell correlation be deduced after
replacing `mu` and `Lambda` by sequences that retain only a convolution
relation or PNT-size aggregate information?

The answer is no.  There are two materially different meanings of
"retain the convolution":

1. If one retains

   \[
   a*\mathbf 1=\varepsilon,
   \]

   then there is no surrogate freedom: uniqueness of the Dirichlet inverse of
   `1` forces `a=mu` coefficient by coefficient.

2. If one retains only

   \[
   b=-a*\log,
   \]

   the relation that formally corresponds to `Lambda=-mu*log`, then `a` is
   arbitrary and this relation merely defines `b`.  It does not determine the
   sign of the shell correlation.

PNT-like information is weaker still.  It controls a few cumulative linear
functionals, whereas the required sign is a quadratic, phase-sensitive
two-scale statement.

## The invariant quantity

For an arbitrary real sequence `a(d)`, use the same normalized tapers as in the
shell recurrence:

\[
 c_M(d)=a(d){\log(M/d)\over\log M},\qquad
 A_M=\sum_{d\le M}{c_M(d)\over d},
\]

\[
 F_M(j)=1+jA_M-\sum_{d\le M}c_M(d)\lfloor j/d\rfloor.
\]

On `N/2<=k<N`, put

\[
 u_k=F_N(k),\qquad
 z_k=F_{2N}(2k)+{k\over2k+1}
       \bigl(F_{2N}(2k+1)-F_{2N}(2k)\bigr),
\]

and `delta=z-u`.  The correlation and shell decrement are

\[
 C_N(a)=\sum_{k=N/2}^{N-1}{N\over k(k+1)}u_k\delta_k,
\]

\[
 D_N(a)=-2C_N(a)-\|\delta\|_{W_-}^2-R_{\rm jump}(a).
\]

These definitions do not invoke primality or multiplicativity, so they give a
clean test of what the aggregate assumptions alone can imply.

## Numerical finite countermodels

The following values are floating-point reconnaissance, not interval
certificates. They illustrate the exact algebraic freedom but are not used as
rigorous sign certificates. At `N=32`, the actual Mobius sequence gives

\[
 C_{32}(\mu)=-0.1298628906,
 \qquad D_{32}(\mu)=+0.0155868294.
\]

Changing only `a(2)` to `mu(2)+1=0` gives

\[
 C_{32}(a)=-0.0925581969,
 \qquad D_{32}(a)=-0.0173954354.
\]

Thus even a one-coordinate convolution surrogate `b=-a*log` reverses the
decrement sign.  Defining `b` by that convolution makes the model satisfy the
formal `mu/Lambda` convolution exactly; what it violates is the inverse
identity `a*1=epsilon`.

The failure is not explained only by changing the two elementary taper moments.
Numerically solve for `h` supported on `{2,3,5}` with

\[
 h(2)=0.5039404018258645,\quad
 h(3)=-1.355910602738797,\quad h(5)=1.
\]

These displayed decimals approximate a solution of

\[
 \sum_d{h(d)\over d}=0,
 \qquad
 \sum_d{h(d)\log d\over d}=0.
\]

The exact logarithmic solution preserves `A_M(mu+t h)=A_M(mu)` for every
`M>=5`; the displayed rounded solution gives the following numerical values at
`N=32`:

| `t` | `C_32(mu+t h)` | `D_32(mu+t h)` |
|---:|---:|---:|
| `-1` | `-0.200442` | `+0.010561` |
| `0` | `-0.129863` | `+0.015587` |
| `1` | `-0.152869` | `-0.050883` |
| `10` | `-4.571238` | `-3.866444` |

Hence fixing the affine normalization at both scales still gives no sign.

There are also perturbations that reverse the correlation itself.  For
example, changing only `a(7)` by `t=5` gives

\[
 C_{32}(a)=+0.1304713659,
 \qquad D_{32}(a)=-0.8665469744.
\]

The sign of the mixed correlation is therefore not a consequence of the
floor geometry or of the formal `b=-a*log` convolution.

## Why PNT-like aggregates survive

For `b=-a*log`, a finite perturbation `a=mu+t h` changes the summatory
`b`-function by

\[
 -t\sum_d h(d)\log(\lfloor x/d\rfloor!).
\]

Stirling's formula shows that the possible `x log x` and `x` terms are linear
combinations of

\[
 \sum_d h(d)/d,
 \qquad \sum_d h(d)\log d/d.
\]

For the displayed three-point perturbation both vanish.  The remaining change
is `O_h(log x)`.  Therefore, if the original pair has

\[
 \sum_{n\le x}\Lambda(n)=x+o(x),
\]

then the perturbed convolution pair has the same PNT asymptotic.  It also has
the same scale-normalizing `A_M`.  Yet its finite shell sign differs.

Sparse copies of such moment-null blocks can be placed on increasingly remote
scales, with amplitudes chosen below the allowed `o(x)` aggregate error.  This
is the standard diagonal construction showing that an asymptotic aggregate
condition cannot impose a uniform local dyadic sign without an additional
rate and local-structure hypothesis.  The finite examples above are the
corresponding one-block witnesses.

## Exact identity that is missing

The local collapse used in the arithmetic argument is not merely
`Lambda=-mu*log`.  Opening it gives

\[
 \sum_{q\mid m}\mu(q)\log(M/q)
 =\log M\,(\mu*\mathbf1)(m)-(\mu*\log)(m).
\]

To obtain

\[
 \log M\,\mathbf1_{m=1}+\Lambda(m)\mathbf1_{m>1}
\]

one needs both exact coefficientwise identities

\[
 \boxed{\mu*\mathbf1=\varepsilon},
 \qquad
 \boxed{\Lambda=-\mu*\log}.
\]

The first identity is the indispensable one not contained in PNT and not
contained in the second convolution relation.  It says that `mu` is the exact
Dirichlet inverse of `1`; retaining it already forces the genuine Mobius
sequence, so there is no nontrivial surrogate class.

For the dyadic comparison, its operational local consequence is the exact
parity law

\[
 \boxed{\mu(2d)=-\mathbf1_{d\ \mathrm{odd}}\mu(d).}
\]

This law synchronizes the scale-`N` source with the even columns of the
scale-`2N` source.  Neither PNT, moment constraints, nor the isolated relation
`b=-a*log` supplies that synchronization.  Even the parity law plus aggregate
constraints would not by itself prove the desired correlation sign; it is a
necessary arithmetic input, not a sufficient angle theorem.

## Verdict

- PNT, even with the correct leading term and unchanged affine taper moments,
  does not determine either the correlation sign or the decrement sign.
- The isolated convolution `Lambda=-mu*log` does not determine them either.
- The exact identity beyond PNT that the local collapse indispensably uses is
  `mu*1=epsilon`; at two scales this appears concretely as the parity identity
  `mu(2d)=-1_(d odd)mu(d)`.
- After restoring these identities one has restored the actual Mobius source,
  but the sign problem remains a genuinely Mobius-specific mixed-correlation
  theorem.  It cannot be reduced to PNT-size aggregate information.
