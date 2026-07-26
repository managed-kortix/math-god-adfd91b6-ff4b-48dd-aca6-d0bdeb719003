# Cycle 36: closure of the pointwise weighted-pair route

## Sharp finite theorem

Let `D_N=E_N-E_(2N)` denote the normalized shell decrement and retain one
common finite zero cutoff `T`. With the notation of
`finite-zero-shell-gram.md`, write

\[
D_N=A_{N,T}+Q_{N,T}+\Delta_{N,T},
\]

where `Q_(N,T)` is the zero-zero finite Mellin Gram block, `A_(N,T)` contains
the complete affine, trivial-zero, half-jump, interpolation, and jump-square
terms, and `Delta_(N,T)` is the exact signed cutoff correction.

The weakest exact weighted-pair inequality sufficient for contraction is

\[
\boxed{Q_{N,T}\ge -A_{N,T}-\Delta_{N,T}.}
\]

This is not an intermediate theorem. By the endpoint-correct explicit formula
it is exactly equivalent to `D_N>=0`. Replacing the signed cutoff correction by
an absolute majorant produces a strictly stronger sufficient condition.

Thus a theorem for the full augmented pair form is the original shell target
in zero coordinates, while a theorem for the pure zero-zero block alone is
insufficient and generally incomparable with contraction.

## Comparison with pair correlation

In a zero-height window near `H`, individual shell modes have normalized
frequencies `log(k)/log(H)` and `log(2k)/log(H)`. They lie in Montgomery's
proved support range when `2N<=H^(1-epsilon)`. The exact shell kernel is still
outside that theorem because it has separate `1/(bar(rho)sigma)` weights, both
signs and cross-height pairs, an atomic finite Mellin test, a signed difference
of Gram norms, affine and jump terms, and a required one-sided error below the
cancellation residual.

Montgomery's theorem controls a height-averaged translation-invariant
statistic. Neither its proved form nor the usual limiting pair-correlation
conjecture supplies the finite, uniform, one-sided augmented inequality above.

## Smoothed two-level route

Smoothing `k/N` gives a rapidly decaying Mellin test and places the problem in a
Weil/Goldston/Montgomery/Aryan two-level framework. The dyadic multiplier must
remain combined:

\[
\Phi_{N,\delta}(u)=\widehat W_{\delta,M}(u)e^{iu\log N}
\left({1\over\log^2N}-{2^{1+iu}\over\log^2(2N)}\right).
\]

The obstruction is unsmoothing. A transition of width `delta` changes
`O(delta N+1)` lattice terms. Even optimistic local mean-square control gives
an edge loss of order `delta N`; standard RH pointwise estimates lose more.
Making this smaller than the shell residual requires essentially sub-lattice
transition width, while known smooth two-level errors deteriorate polynomially
in test derivatives.

The missing result would be a cancellation-preserving two-level formula uniform
for a shrinking test family, together with a signed boundary theorem. No
identified result provides this.

## A weaker intermediate

Let `z=u+delta` be the weighted pair average and define

\[
G_N=-\langle u,\delta\rangle_{W_-}-{1\over2}R_{\rm jump}.
\]

Then

\[
D_N=2G_N-\|\delta\|_{W_-}^2.
\]

For fixed `0<c<1/2`, the inequality

\[
\boxed{G_N\ge c\|\delta\|_{W_-}^2}
\]

is genuinely weaker than contraction. Certified finite ratios are about
`0.541,0.433,0.367,0.412,0.318` at
`N=32,128,512,2048,8192`; hence `c=0.3` holds there, including scales where
contraction fails. No uniform asymptotic claim follows.

## Route decision

The pointwise restricted-shell weighted-pair route is closed as a reduction:

1. the exact augmented theorem is equivalent to shell contraction;
2. known pair-correlation results control only surrogates with the wrong
   weights, averaging, and error scale;
3. smoothing creates an unsmoothing problem at the same cancellation scale;
4. restricted-shell positivity does not itself imply the complete
   Nyman--Beurling liminf target.

The active route returns to the complete weighted block dissipation criterion,
which permits negative individual and shell decrements and directly implies
`liminf P_N=0` when its accumulated logarithmic weight diverges.
