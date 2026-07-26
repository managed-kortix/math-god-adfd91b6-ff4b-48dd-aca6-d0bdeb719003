# Notebook

Bounded scout is queued to verify the spectral-theorem implication with all
ceilings and limit quantifiers, and to distinguish full-operator contraction
from finite variational subspace measurements.

## Bounded scout tick 2

If the full physical transfer operator obeys
`<f,T^ceil(r0/a)f> <= q||f||^2` on the vacuum complement, positivity and the
spectral theorem give a finite-cutoff gap
`log(1/q)/(a ceil(r0/a))`, tending to `log(1/q)/r0`. Passage to the continuum
requires convergence of these rounded-time quadratic forms on a dense set of
vacuum-orthogonal states. Fixed-time correlator convergence, finite trial-space
contraction, or a merely nontrivial OS limit does not suffice.

## Bounded scout cycle 36

Escaping spectral states give an exact obstruction to trial-space or
pointwise-correlator evidence.  Let the vacuum complement be `ell^2(N)`, fix
`0<q<1`, and define positive contractions

`T_n=q I+(1-q) P_(e_n)`.

For every fixed finite coordinate trial space, `T_n` eventually restricts to
`q I`.  For every fixed `f in ell^2`,

`<f,T_n f>=q||f||^2+(1-q)|f_n|^2 -> q||f||^2`.

Nevertheless `T_n e_n=e_n`, so every cutoff has spectral radius one on the
vacuum complement and zero transfer-Hamiltonian gap.  Pointwise convergence of
all fixed correlators, even with eventual contraction on every fixed trial
space, cannot replace a uniform full-complement estimate controlling states
that escape with the cutoff.

## Bounded scout cycle 39

The same escaping-state example defeats even strong operator convergence.  For
`T_n=qI+(1-q)P_(e_n)` and every fixed `f in ell^2(N)`,

`||(T_n-qI)f||=(1-q)|f_n| -> 0`.

Thus `T_n -> qI` in the strong operator topology, not merely through quadratic
forms.  Nevertheless `T_n e_n=e_n` and `||T_n||=1` for every `n`, so every
cutoff transfer Hamiltonian still has zero gap.  A strongly convergent,
strictly contractive continuum transfer operator does not by itself yield the
uniform full-complement estimate required before taking the limit.

## Bounded scout cycle 41

Escaping states survive convergence at every fixed integer Euclidean time, not
only at one transfer step.  For `T_n=qI+(1-q)P_(e_n)` and every `k>=1`,

`T_n^k=q^kI+(1-q^k)P_(e_n)`.

Thus `T_n^k -> q^kI` strongly for each fixed `k`, so all fixed-state
integer-time correlators converge with exponential factor `q^k`.  Yet
`T_n^k e_n=e_n` and `||T_n^k||=1` for every cutoff and every `k`; the cutoff
transfer Hamiltonian still has zero gap.  Simultaneous strong convergence of
all fixed transfer powers is therefore insufficient without a uniform
full-vacuum-complement bound.

## Bounded scout cycle 42

The escaping-state example survives the whole fixed continuous functional
calculus. For every bounded continuous `f:[0,1]->C`,

`f(T_n)=f(q)I+(f(1)-f(q))P_(e_n) -> f(q)I`

strongly. Yet every `T_n` retains eigenvalue one, norm one, and zero
transfer-Hamiltonian gap. Thus even strong convergence of all fixed continuous
spectral observables cannot replace cutoff-uniform control of the moving
spectral edge.

## Bounded scout cycle 43

The same example defeats the entire fixed bounded Borel calculus. For
`T_n=qI+(1-q)P_(e_n)` and any fixed bounded Borel function `phi` on `[0,1]`,

\[
\phi(T_n)=\phi(q)I+(\phi(1)-\phi(q))P_{e_n}
\longrightarrow \phi(q)I
\]

strongly, because the `n`th coordinate of every fixed `ell^2` vector tends to
zero. This includes the endpoint projection
`1_{\{1\}}(T_n)=P_(e_n)->0` strongly. Yet every `T_n` retains eigenvalue one
and zero transfer-Hamiltonian gap. Hence even convergence of all fixed bounded
Borel spectral observables misses a moving edge state; cutoff-uniform norm
control is indispensable. This abstract no-go neither constructs Yang--Mills
theory nor proves a mass gap.
