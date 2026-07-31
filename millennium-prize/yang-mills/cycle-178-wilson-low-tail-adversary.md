# Cycle 178: Wilson low/tail adversary

This note attacks the Cycle 174 proposal to split the physical transfer
operator into a low Wilson block and a representation tail.  The attack is
already exact in the one-plaquette `SU(2)` Hilbert space and survives every
finite lattice through gauge-invariant spin-network states.  It does not rule
out a tail estimate containing electric/Casimir smoothing; it quantifies what
such an estimate must pay.

## One plaquette reaches every representation

Use normalized Haar measure and the orthonormal class characters
`chi_j`, `j=0,1/2,1,...`, with `chi_0=1`.  Multiplication by the normalized
fundamental Wilson plaquette

\[
 w={1\over2}\chi_{1/2}
\]

obeys the exact Clebsch--Gordan rule

\[
 w\chi_j={1\over2}(\chi_{j+1/2}+\chi_{j-1/2}),
 \qquad \chi_{-1/2}=0.
\]

Let `Pi_J` project onto spins `j<=J`, and choose the normalized tail state
`f_J=chi_(J+1/2)`.  Then

\[
 \Pi_J f_J=0,
 \qquad
 \Pi_J(wf_J)={1\over2}\chi_J,
 \qquad
 \|\Pi_J w(I-\Pi_J)\|\ge {1\over2}.
\]

Thus no representation cutoff makes the magnetic plaquette block diagonal or
gives an operator-norm small low/tail coupling.  For the usual Wilson magnetic
term `lambda_beta(1-w)` the corresponding cross block has norm at least
`lambda_beta/2`; in Hamiltonian normalization `lambda_beta` grows like an
inverse power of the bare coupling.  Weak coupling amplifies this obstruction
rather than suppressing it.

The same conclusion holds for a character series
`v=sum_l v_l chi_l`: multiplication contains arbitrarily high output spins
whenever infinitely many `v_l` are nonzero.  Even the fundamental Wilson term
is sufficient for the fixed boundary coupling above, so a decay estimate for
the coefficients `v_l` alone does not close the operator-norm tail.

## Exact escaping states and the gauge quotient

The example is not removed by Gauss' law.  On a spatial lattice containing a
closed plaquette `p`, the spin-network function

\[
 F_{p,j}(U)=\chi_j(U_p)
\]

is gauge invariant.  Haar orthogonality after integrating a link belonging
only to `p` gives `\|F_(p,j)\|=1` and orthogonality for distinct `j`.  Therefore

\[
 F_{p,J+1/2}\in (I-\Pi_J)H_{\rm phys}
\]

is a physical escaping state at every cutoff, and multiplication by `w_p`
places a component of norm `1/2` back in the low block.  On periodic lattices,
one may instead use a noncontractible spin-network loop; the representation
label remains a genuine gauge-invariant degree of freedom.  Gauge fixing can
change coordinates but cannot delete these Peter--Weyl sectors.

For any fixed `J`, choosing disjoint plaquettes gives many orthonormal escaping
states.  Hence finite volume does not repair the one-state obstruction, while
trace or Hilbert--Schmidt estimates acquire multiplicity factors.  If `K`
disjoint plaquettes support the channels above, then the compression to their
orthogonal one-plaquette boundary channels satisfies

\[
 \|\Pi_{\rm low}M(I-\Pi_{\rm low})\|_{\rm HS}^2\ge {K\over4}
\]

for the direct-sum boundary channels of plaquette multiplication `M`.  Since
`K` is proportional to the spatial volume, a uniform HS estimate must be
normalized locally or pay at least `K^(1/2)`; a trace estimate pays at least
`K`.  Operator norm avoids this volume growth but still has the unavoidable
constant `1/2`.

## What a valid tail estimate must contain

Let `C` be the electric Casimir, `C chi_j=j(j+1)chi_j`.  The previous boundary
state also gives the sharp necessary scale for a Casimir-weighted estimate:

\[
 \|\Pi_J w(I-\Pi_J)(1+C)^{-s/2}\|
 \ge {1\over2}[1+(J+1/2)(J+3/2)]^{-s/2}.
\]

So positive regularity can make a weighted cross block decay only at the
corresponding polynomial rate; unweighted `s=0` cannot decay at all.  Conversely,
the character recurrence and `\|w\|_infty<=1` show that the unweighted bound is
at most one.  The unavoidable constant therefore lies in `[1/2,1]`, independent
of `J` and volume.

For the Cycle 174 decomposition, a bound only on
`S(I-Pi_J)` could still be true because the transfer operator may supply
electric heat damping before or after magnetic multiplication.  But it cannot
follow from representation truncation or character-coefficient decay alone.
One must prove, on the gauge-invariant/OS physical quotient and uniformly in
volume, an ordering-sensitive estimate such as

\[
 \|e^{-tC/2}M_\beta e^{-tC/2}(I-\Pi_J)\|\le r_J(a),
 \qquad r_J(a)<\sqrt{1-q_J(a)^2},
\]

at a cutoff choice `J=J(a)` compatible with a fixed physical time.  The
boundary calculation forces this estimate to absorb at least

\[
 {\lambda_\beta\over2}\exp\left[-{t\over2}
 \{J(J+1)+(J+1/2)(J+3/2)\}\right]
\]

up to the precise transfer ordering.  In particular, if
`lambda_beta -> infinity`, keeping the boundary channel below a fixed `r<1`
requires at least

\[
 tJ^2 \gtrsim \log\lambda_\beta+O(1).
\]

This is a necessary scaling calibration, not a sufficient estimate: products
over plaquettes, noncommuting electric and magnetic pieces, volume-uniformity,
the OS quotient, and the continuum limit remain to be controlled.

## Checkpoint

The bare Wilson low/tail proposal is false in operator norm.  The magnetic
plaquette couples every representation cutoff across its boundary with norm at
least `1/2`, physical gauge-invariant escaping states realize the bound, and
volume-sensitive norms worsen with the number of plaquettes.  The only live
version must build electric/Casimir smoothing and exact transfer ordering into
the tail norm, with constants uniform after Gauss and OS quotient and along the
weak-coupling continuum trajectory.  No Yang--Mills construction or mass gap is
claimed.
