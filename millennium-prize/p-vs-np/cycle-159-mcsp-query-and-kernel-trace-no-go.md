# Cycle 159: near-linear MCSP query complexity does not cross the time barrier

Let `N=2^n` and let `E_(n,s)` be the truth tables computed by fan-in-two
circuits of size at most `s`.  Standard circuit encoding gives

\[
\log_2|E_{n,s}|=O(s\log(n+s)).
\]

On an easy truth table, every exact deterministic decision tree for MCSP must
query at least

\[
\boxed{N-\log_2|E_{n,s}|}
\]

bits.  Indeed, after `q` answers matching the easy table, the consistent
subcube has `2^(N-q)` completions.  If this exceeds the total easy-set size, it
contains a hard completion with the same transcript.

Therefore

\[
\boxed{D(\operatorname{MCSP}[s])\ge N-O(s\log(n+s)).}
\]

At `s=N^(1/4)`, this is

\[
N-O(N^{1/4}\log N)=N-o(N).
\]

This is a sharp semantic input-reading lower bound, but it cannot exceed `N`
and therefore cannot supply the superlinear time lower bound needed by the
magnification hypotheses.

The projection-shattering result gives a complementary NO-certificate bound.
Any labeling of `q` domain points is fitted by a circuit of size

\[
3(q-1)+\min(n,q-1).
\]

Hence at `s=N^(1/4)`, every rejecting certificate needs at least

\[
\frac13N^{1/4}-O(\log N)
\]

coordinates.  This remains a certificate/query theorem, not an unrestricted
circuit lower bound.

Post-kernel trace invariants also fail as a shortcut.  A random-access
continuation using space `S` and time `T` is represented exactly by a layered
branching program of length `T` and width `2^{O(S+log T)}`.  Sequentially
simulating a `b`-bit resident kernel costs at most a factor `b`; when
`b=m^{o(1)}`, this changes only the subpolynomial part of a fixed time exponent.

Any statistic based on access order, information location, pebbling a selected
execution DAG, or syntactic dependency can be altered by ignored computation,
padding, pointer chains, and invertible state re-encodings without changing the
decision.  If the statistic is made junk- and representation-robust by
minimizing over equivalent computations, it becomes a semantic branching-
program/RAM complexity measure for the kernel predicate itself.  Proving the
desired lower bound for that measure is the original lower-bound problem, not a
reduction of it.

Thus Cycle 159 preserves an unconditional near-linear MCSP query theorem and
retires certificate covers, probe counts, sequentiality, and pebbling of a
chosen kernel evaluator as routes to unrestricted superlinear time or circuit
lower bounds.

No `P != NP` result is claimed.
