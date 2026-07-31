# Cycle 183: randomized OBDD splice-distribution obstacle

## Target reduction

Fix a variable order `pi`, cut it after the coordinate set `P`, and write
`Q=[N]\setminus P`.  A bounded-error randomized `pi`-OBDD of midpoint width
`W` induces a public-coin one-way protocol of cost `ceil(log_2 W)`: Alice runs
the prefix on `x|_P`, sends the midpoint state, and Bob continues on `x|_Q`.
The full random tape can be shared.  Consequently, extending the exact splice
argument requires a distributional one-way lower bound for the induced
prefix/suffix matrix, not merely many pairwise exact distinctions.

Let `C={x_1,...,x_m}` be the easy-table code used in the exact argument, and
put

\[
 a_i=x_i|_P,\qquad b_i=x_i|_Q.
\]

The available splice assertion is

\[
 f(a_i,b_i)=1,
 \qquad
 \text{and for every }i\ne j,
 \quad f(a_i,b_j)=0\text{ or }f(a_j,b_i)=0.                 \tag{1}
\]

Here `f=MCSP[s]`, with 1 denoting an easy table.  Equation (1) forces `m`
different deterministic messages: for each pair, one of the two indicated
columns distinguishes its two rows.  This is exactly the step yielding width
at least `m` for an exact OBDD.

## Fingerprinting defeats every witness-splice distribution

The same promise has constant public-coin randomized communication.

**Fingerprint lemma.**  Suppose (1) holds.  Form a promise problem containing
all diagonal inputs `(a_i,b_i)`, labelled 1, and any collection of certified
hard cross-splices `(a_i,b_j)`, labelled 0.  Its public-coin one-way complexity
with error `epsilon` is at most

\[
 \left\lceil\log_2\left\lceil1/\epsilon\right\rceil\right\rceil+O(1),
\]

independently of `m`.

First note that all `a_i` are distinct.  If `a_i=a_j`, then both cross-splices
are the original easy tables `x_j` and `x_i`, contradicting (1).  The same
argument shows that all `b_i` are distinct.  Thus, on the promise, Alice and
Bob can recover their respective indices `i` and `j`; local computation is
free in communication complexity.

Using public randomness, choose a pairwise-independent hash
`h:[m] -> [K]`, where `K>=1/epsilon`.  Alice sends `h(i)`, and Bob accepts iff
`h(i)=h(j)`.  Every diagonal input is accepted.  Every certified hard
cross-splice has `i!=j` and is accepted with probability at most `1/K`.  The
message has `ceil(log_2 K)` bits.  The orientation selected separately for
each pair is irrelevant.

This also rules out the proposed Yao rescue.  For every distribution `mu`
supported on these diagonal and certified-hard splice witnesses, averaging
the fingerprint protocol over its public hash gives error at most `epsilon`.
Therefore some fixed hash is a deterministic constant-message protocol with
`mu`-error at most `epsilon`.  No distribution over these witnesses can make
all small deterministic protocols err by more than `epsilon`.

If the branching-program convention supplies only private coins, the standard
public-to-private conversion on an index domain of size `m` costs only
`O(log log m+log(1/epsilon))` bits.  Hence even that convention does not recover
the exact `log m` lower bound from pairwise splice separation.

## Why the exact proof loses its force

Exact subfunction counting treats the `m` prefix residuals as objects that
must be represented with zero error.  Randomized messages are distributions,
and fingerprints let a constant-size message distinguish any requested pair
with constant probability.  Pairwise total-variation separation of message
distributions is therefore not a substitute for disjoint deterministic
states.  Equality is the canonical extreme: it has `m` exact one-way messages
but constant public-coin randomized communication.

The MCSP counting estimate says that many cross-splices are hard.  That tends
to make the restricted matrix closer to equality--diagonal easy and
off-diagonal hard--which is favorable for fingerprinting rather than for a
randomized lower bound.  The estimate supplies no complexity in the pattern
of the comparatively rare easy off-diagonal entries.

## What a successful randomized lower bound would need

A lower bound must use a richer promise distribution for which Bob cannot
reduce the task to testing whether two codeword indices agree.  For example,
one would need to prove that the full easy/hard cross-splice matrix contains a
distributionally hard one-way subproblem--such as many rows whose labels on a
common random set of columns encode many independently recoverable bits--and
then apply an information, corruption, discrepancy, or random-access-code
bound.  The current support-size estimate

\[
 \Pr[(a_i,b_j)\text{ is easy}\mid k]
 \le {|E|\over\binom d k}
\]

controls only the number of easy outcomes in one splice orbit.  It gives no
row-pattern independence, no common-column structure, and no lower bound on
mutual information.  It therefore cannot establish such a communication
minor.

There is also no gain from mixing cuts or random orders in the witness
distribution.  Conditioned on the public cut, the prefix and suffix strings
still identify their codewords and the same fingerprint protocol applies.
Hiding the cut from a party would no longer model the OBDD-to-communication
reduction.

## Consequence

The exact width lower bound does not extend to bounded-error randomized OBDDs
through a distribution over the existing pair-dependent splice witnesses.
The obstruction is stronger than the earlier failure to union-bound one order
over all inputs: even for one fixed good order, the entire natural witness
promise has constant public-coin one-way complexity.  This does not construct
a small randomized OBDD for MCSP; it shows that the current restricted matrix
cannot prove a randomized OBDD lower bound.  A new MCSP-specific theorem about
the labelled cross-splice matrix, beyond sparsity/counting, is required.

At the MMW parameter the earlier independent ceiling also remains:
`log|C|<=O(s log(n+s))=N^o(1)`.  Thus even a hypothetical recovery of the exact
`Omega(log|C|)` communication bound would still not force fixed-power space or
trigger the relational search-MCSP magnification theorem.  No complexity-class
separation is claimed.
