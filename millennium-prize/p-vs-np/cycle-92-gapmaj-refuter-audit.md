# Cycle 92: constructive GapMaj refuter audit

## Exact full-reach theorem

Chen--Jin--Santhanam--Williams, Theorem 1.6, proves the following.  Let
\[
 \varepsilon(n)\le (\log n)^{-\omega(1)}
\]
with integer `1/epsilon` computable in `poly(1/epsilon)` time.  If every
randomized `poly(1/epsilon)`-time algorithm using
\[
 o(1/\varepsilon^2)
\]
queries for promised GapMaj has an algorithm-dependent, polylogtime-uniform
`AC0` refuter producing a promised error on infinitely many lengths, then
`P != NP`.

The quantifiers are
\[
 \forall A\ \exists R_A\ \exists^\infty n,
\]
not one universal refuter and not an all-large-length claim.  Under `P=NP`,
the proof constructs one `O(epsilon^-1.91)`-query learner that succeeds on the
outputs of every such uniform `AC0` family.  This is a valid full-reach target.

## Exact failure of seed fixing

Average query hardness cannot be converted by fixing the random seed.  On
three bits, choose a coordinate `I` uniformly, query `x_I`, and output it.  For
majority on three bits, every input is answered correctly with probability at
least `2/3`, but every fixed coordinate projection fails on both
\[
 e_I\quad\hbox{and}\quad {\bf1}-e_I.
\]
Thus exactly
\[
 \max_x\mathbb E_I[\operatorname{err}(x,I)]=1/3,
 \qquad
 \mathbb E_I\max_x\operatorname{err}(x,I)=1.
\]
No scalar pessimistic estimator with terminal domination and initial value
below one can produce a universally good fixed seed.  The four-bit/two-fair-bit
version has promise `|x|<=1` versus `|x|>=3` and success at least `3/4`.

Bounded independence also does not fool arbitrary query algorithms, because
the query bound does not restrict computation on the random tape.  An
algorithm may test membership in the support of a `k`-wise independent source,
behave badly there, and solve exactly off that support.  Exact conditional
error computation for a succinct arbitrary algorithm additionally contains
`#SAT`.

## Remaining extraction barrier

The ordinary adaptive-query lower bound is clean: on uniform layers of weights
`n/2 +- Delta`, transcript total variation is
\[
 O(\Delta\sqrt q/n).
\]
It gives a dense distribution of errors.  It does not choose one error by a
deterministic polylogtime-uniform `AC0` family.  Sampling, minimax, and averaging
preserve probability, not shallow uniformity; testing whether a sampled point
is an error requires the correct GapMaj label and the candidate's random error
probability.  Adaptivity further prevents a standard switching lemma from
simultaneously controlling every reachable transcript.

The candidate seed-fixing mechanism is retired.  The CJSW theorem remains a
valid full-reach theorem, but its shallow hard-input extraction assertion is
the substantive missing lower bound, not a routine derandomization of query
hardness.  No complexity separation is claimed.
