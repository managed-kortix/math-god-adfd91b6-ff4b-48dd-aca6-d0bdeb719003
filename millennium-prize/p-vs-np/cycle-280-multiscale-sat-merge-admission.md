# Cycle 280: multiscale SAT merge lemma admission

## Decision

`C280-ADMIT`.

The independently supplied object is a new asymptotic unrestricted-circuit
lemma, not a request to discover a witness or repair an old mechanism. This
note freezes the statement, its quantifiers, its official relationship, its
novelty boundary, and one bounded hostile counterexperiment. Admission records
a complete research packet; it does not certify the supplied proof.

## Canonical target and circuit model

For definiteness, `3SAT_N:{0,1}^N->{0,1}` uses the following fixed parser.
Read `1^v 0 1^m 0`, put `ell=ceil(log_2(v+1))`, and then read exactly `3m`
literals, each represented by one sign bit and an `ell`-bit integer in
`{1,...,v}`. The remaining bits must be zero. Malformed strings map to zero;
well-formed strings map to one exactly when the represented three-CNF is
satisfiable. Repeated literals are allowed. This freezes one ordinary padded
canonical encoding; changing among linearly intertranslatable standard
encodings is not part of the packet.

An unrestricted fan-in-two circuit has constants, free fanout, unary gates,
and any of the 16 binary Boolean operations. Its size is its number of
non-input gates. Delete gates outside the output cone before applying the
definitions below.

For a gate `u`, restriction `rho`, and set `S` of input coordinates left free
by `rho`, say that `u` is `S`-active if there exist two completions extending
`rho` that agree outside `S` and give different values at `u`. For disjoint
nonempty free-coordinate sets `A,B`, a gate `g` is an `A/B` first merge under
`rho` when:

1. `g` is both `A`-active and `B`-active;
2. no strict predecessor of `g` in the restricted output cone is both
   `A`-active and `B`-active; and
3. the restricted output is separately `A`-active and `B`-active, so the merge
   is SAT-active rather than dead internal syntax.

At dyadic scale `k`, require
`2^k <= |A|,|B| < 2^(k+1)`. Denote the resulting predicate by
`FM_N(C,k,g,rho,A,B)`.

## Frozen multiscale lemma

The supplied **Multiscale SAT Merge Lemma** is the following statement with
the quantifier order made explicit:

\[
\begin{split}
 &\exists c>0\;\exists\eta>0\;\exists N_0\;\forall N\ge N_0\;
 \forall C\\
 &\quad [C\text{ computes }3SAT_N]\Longrightarrow
 \exists K_N\;\exists (G_k)_{k\in K_N}\;\exists
 (\rho_{k,g},A_{k,g},B_{k,g})_{k\in K_N,g\in G_k}
\end{split}                                                    \tag{280.1}
\]

such that

\[
 K_N\subseteq\{0,\ldots,\lfloor\log_2N\rfloor\},\qquad
 |K_N|\ge\lfloor\eta\log_2N\rfloor,                           \tag{280.2}
\]

\[
 G_k\subseteq Gates(C),\qquad |G_k|\ge\lfloor cN\rfloor
 \quad(k\in K_N),                                               \tag{280.3}
\]

\[
 G_k\cap G_{k'}=\varnothing\quad(k\ne k'),                    \tag{280.4}
\]

and, for every `k in K_N` and `g in G_k`,

\[
 FM_N(C,k,g,\rho_{k,g},A_{k,g},B_{k,g}).                        \tag{280.5}
\]

The restrictions and coordinate blocks may depend on `C,k,g`; the constants
`c,eta,N_0` may not depend on `N` or `C`. Most importantly, (280.4) is global
disjointness across scales. Pairwise distinct gates only within each `G_k`
would not imply the advertised lower bound.

## Immediate consequence

Equations (280.2)--(280.4) give, for every circuit covered by (280.1),

\[
 |C|\ge\left|\bigcup_{k\in K_N}G_k\right|
      =\sum_{k\in K_N}|G_k|
      \ge \lfloor\eta\log_2N\rfloor\lfloor cN\rfloor.
                                                                    \tag{280.6}
\]

Hence the supplied lemma implies

\[
 C(3SAT_N)=\Omega(N\log N)                                      \tag{280.7}
\]

for unrestricted fan-in-two nonuniform circuits.

## Relationship to official P versus NP

This would be a major asymptotic partial result: it is a superlinear lower
bound for an explicit NP-complete Boolean family in the unrestricted circuit
model. It is not a solution of official P versus NP. The official question asks
whether every nondeterministic-polynomial-time language has a deterministic
polynomial-time algorithm. The bound `Omega(N log N)` is compatible with
`3SAT` having circuits of size `N^2`, `N^10`, or any other polynomial size, and
it supplies no uniform superpolynomial time lower bound. In particular, NP
completeness does not amplify this superlinear bound into `P != NP`.

The precise partial conclusion is only

\[
 3SAT\notin SIZE(o(N\log N))                                    \tag{280.8}
\]

for the frozen encoding and circuit model. No stronger uniform or nonuniform
separation is admitted.

## Novelty and stop-rule audit

The packet is non-equivalent to Cycles 76--77 `Stream-Merge`. Those cycles
concerned a canonical local optimization used inside an upper-bound algorithm
for relational `search-MCSP`, and failed to transfer hardness of the
canonicalized operation to the easier relation. Equation (280.1) instead
quantifies directly over every unrestricted circuit computing canonical
`3SAT_N`; it has no streamer, update-time parameter, canonical-output relation,
or algorithm-to-proof compiler.

It is also non-equivalent to the retired Cycle 264 `AMT` address/data gadget
and the Cycle 269 local charging repair. Those routes sought additivity across
semantic components and were broken by a shared payload core. The present
lemma does not sum component complexities or assign unit charges. Its required
resource is a globally disjoint collection of physical gates across dyadic
scales. Thus the old shared-circuit breaker does not formally refute (280.1).
Conversely, merely relabeling one shared gate at many scales would violate
(280.4) and would not prove the lemma.

## One bounded finite counterexperiment

Freeze the four-input, three-gate circuit

\[
 h_0=a\wedge b,\qquad h_1=c\wedge d,\qquad g=h_0\vee h_1.       \tag{280.9}
\]

Use exactly two proposed scales and inspect only the gate `g`:

- at scale zero, restrict `b=d=1` and take `A={a}`, `B={c}`;
- at scale one, use the empty restriction and take `A={a,b}`,
  `B={c,d}`.

In both cases `g` is an `A/B` first merge and the output is separately active
in both blocks. Therefore the weak reading "one internally pairwise-distinct
set at each scale" may choose `{g}` twice and falsely count two gates although
the union has size one.

The experiment has no search, randomness, or scaling parameter. Its fixed
terminal outputs are:

- `OVERLAP-CAUGHT` if the packet forbids reuse of `g` across the two scales;
- `COUNTEREXAMPLE` if the packet permits reuse but still sums the two sets;
- `WALL` only if first merge or SAT-active is left undefined.

Under (280.4) it returns `OVERLAP-CAUGHT`: the toy circuit attacks the tempting
weaker quantifier, not the frozen lemma. Stop after this one circuit; do not
enumerate larger circuits or treat finite survival as evidence for (280.1).

## Admission boundary

All four intake items are present: an exact non-equivalent asymptotic lemma,
its exact unrestricted-circuit consequence and limited official relationship,
all inputs for one finite hostile test, and fixed terminal outputs with a stop.
The next legitimate operation is a hostile proof audit of the independently
supplied derivation of (280.1), especially the production of global
cross-scale disjointness. Admission does not authorize reporting (280.7) as a
theorem until that proof is reproduced and survives review.

Record:

`C280-ADMIT; MULTISCALE SAT MERGE PACKET FROZEN WITH GLOBAL CROSS-SCALE
DISJOINTNESS; OMEGA(N LOG N) IS A MAJOR UNRESTRICTED-CIRCUIT PARTIAL RESULT,
NOT P!=NP; STREAM-MERGE AND AMT STOPS NOT REOPENED; FIXED THREE-GATE
COUNTEREXPERIMENT RETURNS OVERLAP-CAUGHT; PROOF NOT YET CERTIFIED.`
