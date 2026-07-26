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
