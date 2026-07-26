# Lag-`log 2` zero-model sign audit

## Question and normalization

This note tests only the following logical implication:

> Do critical-line location, conjugation symmetry, and Riemann--von Mangoldt
> scale zero density determine the sign of a quadratic correlation at logarithmic
> lag `h=log 2`?

They do not.  There are finite symmetric ordinate sets and infinite abstract
critical-line multisets with the same rough counting law for which the natural
lag statistic has either strict sign.

For distinct positive ordinates `Gamma={gamma_1,...,gamma_m}` and positive
amplitudes `a_j`, put

\[
 Z(t)=\sum_{j=1}^m a_j\cos(\gamma_jt).
\]

The conjugate exponentials in each cosine correspond to the critical-line pair
`1/2+i gamma_j,1/2-i gamma_j`.  Orthogonality gives

\[
 \lim_{X\to\infty}{1\over X}\int_0^X Z(t)Z(t+h)\,dt
 ={1\over2}\sum_{j=1}^m a_j^2\cos(h\gamma_j).
\]

Thus the amplitude-normalized lag statistic is

\[
 \mathcal C_h(\Gamma,a)
 ={\sum_j a_j^2\cos(h\gamma_j)\over\sum_j a_j^2}.
\tag{1}
\]

The same construction applies to any diagonal zero-wave quadratic statistic
whose spectral multiplier changes sign: replace `cos(h gamma)` by that
multiplier.  Positive zero-formula weights, including weights depending on
`1/4+gamma^2`, do not alter the examples below because every occupied phase can
be put in one strict sign region.

## Minimal finite models

Let `h=log 2`.

* The symmetric zero set
  \[
  \mathcal Z_+=\{1/2\pm i2\pi/h\}
  \]
  (whose positive-ordinate set is `Gamma_+={2pi/h}`) has
  `mathcal C_h=+1`.
* The symmetric zero set
  \[
  \mathcal Z_-=\{1/2\pm i\pi/h\}
  \]
  (whose positive-ordinate set is `Gamma_-={pi/h}`) has
  `mathcal C_h=-1`.

More generally, arbitrary positive amplitudes on ordinates

\[
 \gamma={2\pi k+\theta\over h},\qquad |\theta|\leq\pi/3,
\]

give `mathcal C_h>=1/2`, while ordinates with

\[
 \gamma={(2k+1)\pi+\theta\over h},\qquad |\theta|\leq\pi/3,
\]

give `mathcal C_h<=-1/2`.  Hence neither conjugation nor a prescribed positive
amplitude profile supplies a sign.

## Infinite simple models with rough zeta-zero density

The finite examples can be made compatible with the positive-ordinate
Riemann--von Mangoldt main term

\[
 M(T)={T\over2\pi}\log{T\over2\pi}-{T\over2\pi},
 \qquad M'(T)={1\over2\pi}\log{T\over2\pi}.
\tag{2}
\]

Start above a fixed large `T_0`.  In the phase variable `hT mod 2pi`, define

\[
 A_+=\{\theta:|\theta|\leq\pi/3\},\qquad
 A_-=\{\theta:|\theta-\pi|\leq\pi/3\}.
\]

Each set occupies one third of a phase period.  For either sign define the
continuous target measure

\[
 d\nu_\pm(t)=3M'(t)\,1_{A_\pm}(ht\bmod2\pi)\,dt.
\tag{3}
\]

Choose one simple ordinate whenever the cumulative mass of `nu_pm` crosses an
integer.  Equivalently, if `V_pm(T)=nu_pm([T_0,T])`, choose `gamma_n` by
`V_pm(gamma_n)=n`.  The ordinates are distinct and all lie in the selected
phase arcs.

Over each complete phase period `P=2pi/h`, the factor `3 1_A` has mean one.
Since

\[
 M''(t)={1\over2\pi t},
\]

comparison period by period, plus one incomplete terminal period, gives

\[
 V_\pm(T)=M(T)-M(T_0)+O(\log T).
\]

Indeed, the error from a complete period is bounded by a constant times
`sup M''` on that period, so these errors sum like `sum 1/k`; the incomplete
period contributes `O(M'(T))=O(log T)`.

Rounding cumulative mass to integers adds only `O(1)`.  After adding an
arbitrary finite initial segment, the resulting positive-ordinate count is

\[
 N_\pm(T)=M(T)+O(\log T).
\tag{4}
\]

This has the usual main term and even the rough size of the classical
Riemann--von Mangoldt remainder.  Reflecting every ordinate through zero makes
the associated zero multiset conjugation invariant and puts every abstract
zero on `Re s=1/2`.

Nevertheless, every ordinate in the positive model satisfies
`cos(h gamma)>=1/2`, and every ordinate in the negative model satisfies
`cos(h gamma)<=-1/2`.  Consequently every nonempty finite truncation, every
dyadic shell, and every positively weighted version of (1) has the prescribed
strict sign:

\[
 \mathcal C_h(\Gamma_+,a)\geq {1\over2},\qquad
 \mathcal C_h(\Gamma_-,a)\leq-{1\over2}.
\tag{5}
\]

This construction uses simple ordinates; multiplicities are unnecessary.  Its
constant-length phase gaps contain `O(log T)` expected zeros, exactly the amount
that an `O(log T)` counting remainder can hide.

## Finite density-matched ordinate sets

For any cutoff `Y>T_0`, truncate either quantile construction at `Y` and add the
negative ordinates.  The resulting finite set has

\[
 \#\{0<\gamma\leq T\}=M(T)+O(\log Y)
 \quad(T_0\leq T\leq Y),
\]

and its lag statistic has the corresponding sign.  If density is required only
at the endpoint, take exactly `round(M(Y))` distinct ordinates from the desired
phase arcs below `Y`; the phase arcs contain continuum-many choices, so this
places no restriction on simplicity.

## What the audit proves

The counting law controls the zero-frequency mass of the ordinate measure.
The lag statistic probes its Fourier coefficient at the nonzero frequency
`h=log 2`:

\[
 \sum_\gamma w_\gamma e^{ih\gamma}.
\]

Critical-line location and conjugation merely make its contribution real;
they do not choose its sign.  The constructions above show that even

1. all zeros on the critical line,
2. exact conjugate pairing,
3. simple ordinates,
4. positive prescribed amplitude weights, and
5. `N(T)=M(T)+O(log T)` rough density

leave the lag-`log 2` quadratic statistic free to have either sign.

Therefore an argument using only RH-type location and rough zero density cannot
force the sign needed in the dyadic square-energy comparison.  A valid sign
theorem would need additional phase-sensitive arithmetic input: for example, a
specific explicit-formula identity with a sign-definite spectral multiplier,
an Euler-product constraint that controls this fixed Fourier mode, or a new
theorem directly bounding the weighted coefficient at frequency `log 2`.

This is an abstract-model non-implication, not a counterexample involving the
actual zeta zeros and not a proof that RH cannot imply the desired sign after
the full zeta functional equation, Euler product, and explicit formula are
used.
