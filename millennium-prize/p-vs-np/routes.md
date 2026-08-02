# Routes

Scout lemma: polynomial-cardinality anticheckers for dense-encoded 3-COLOR
against unrestricted fan-in-two circuits of size `N^2`. This gives only a
quadratic lower bound; a separate all-exponents amplification theorem would
be required for `P != NP`. First exact test: finite circuit/hitting-set
enumeration at six graph vertices.

Cycle 180 bounded prospect: state an exact random-order MCSP model and prove a
query or streaming lower bound there. This remains a restricted-model theorem
unless it applies to relational `search-MCSP^SAT` at
`s(n)=2^(n/log^* n)` and preserves exactness, oracle access, space, and per-item
update time strongly enough to trigger the McKay--Murray--Williams implication.
Decision MCSP, canonical output, average-order success, or a near-linear query
bound alone does not imply `P != NP`.

Cycle 182 calibration: a lower bound for exact `pi`-OBDD size on most random
orders is a genuine residual-state strengthening of query depth. It gives a
random-partition deterministic one-way communication bound and, for a matched
fixed-order exact decision streamer, space at least `log L-log(N+1)`. It does
not cover best-order or adaptive/repeated-read branching programs, does not
charge update time, and does not transfer from Boolean decision MCSP to the MMW
search relation. Novelty remains conditional on a primary-source audit.

Cycle 182 hostile audit: midpoint splice packing is valid for exact all-order
decision MCSP only after conditioning on the number of disagreements in the
prefix; the candidate splice has support `binom(d,k)`, not `2^N`, and balance
alone does not imply hardness. More decisively, a code of easy tables has
`log|C|<=O(s log(n+s))=N^o(1)` at the MMW value of `s`, so the resulting width
argument cannot force fixed-power space. Average-order correctness also does
not give one permutation correct on all pairwise splices, and decision-state
distinguishability supplies neither relational-search nor update-time hardness.

Cycle 182 gives an exact affine-plane order family: transverse slope blocks
meet in one point, so balanced block prefixes have exact product intersections
up to one boundary block. Equality has width at least `2^((q^2-1)/2)` in every
one of these `q(q-1)` designated orders, by an exact split-pair count. This does
not cover an adversarial OBDD order (the paired order has width two), and no
reverse simulation transfers OBDD hardness to exact relational
`search-MCSP^SAT`. The live obstruction is quantifier order: one efficiently
computable function must hide a family of matchings so that every variable
order leaves one matching with `Omega(N)` independent cross-cut bits, without
letting the program read a selector first.

Cycle 183 rules out an every-order strengthening of the same Reed--Muller
splice packing. Put the hyperplane `x_1=0` in the first half of the order. For
`f,g in RM(d,n)`, the splice `(1+x_1)f+x_1g` lies in `RM(d+1,n)`, so every
off-diagonal splice is easy whenever the MCSP threshold contains that code.
For an arbitrary half-set with indicator `a`, the exact hard-pair count is the
sum over nonzero `q in RM(d,n)` of
`|RM(d,n)|-|(RM(d,n)+aq) cap E|`. Generalized Hamming weights control
restriction kernels and expose the large hyperplane-supported subcode, but do
not control these circuit-easiness intersections.

Cycle 183 randomized audit: no Yao distribution supported only on the natural
diagonal easy tables and certified hard cross-splices can extend the exact
width bound.  At a fixed cut the prefix and suffix codewords have unique
indices, so public-coin equality fingerprinting solves the whole witness
promise with `O(log(1/epsilon))` one-way bits, independent of `|C|`; hence every
such input distribution has a constant-message deterministic protocol of
error at most `epsilon`.  Mixing public cuts does not help.  A randomized OBDD
lower bound needs a richer labelled cross-splice matrix with an information-
hard row pattern, which the present support-size/counting estimate does not
supply.  This is an obstacle to the proof route, not a small randomized OBDD.

Cycle 183 referee decision: do not spend main-funnel compute optimizing the
same random-order easy-table packing.  Its MMW ceiling and model-transfer gaps
are structural.  The only live OBDD scout is qualitatively stronger: one
explicit polynomial-time function must hide a polynomial-size matching family
so that every variable order has a balanced cut retaining `Omega(N)`
independent bits, with no input-readable selector.  Even success would remain
an all-order OBDD theorem, not a `P != NP` result.

Cycle 206 closes the abstract selector-free benchmark but not its MCSP
transfer. For `HWB_(8m)(x)=x_(|x|)`, every midpoint partition contains an exact
`INDEX_m` communication-matrix minor: use `m` data/compensator pairs to keep
the prefix weight fixed at `m` or `3m`, and let the suffix weight address the
data bit. Hence every variable order has exact OBDD width at least `2^m`
without a separate selector input. The natural MCSP quadratic-code replacement
has an exact counterorder: put the affine hyperplane `u_1=0` first. Every splice
of two `RM(2,n)` words then lies in `RM(3,n)` and is easy once
`s>=3 sum_(j<=3) binom(n,j)`, so that splice matrix contains no nonconstant
minor. The surviving problem is an MCSP-specific selector-free construction,
not the order-oblivious combinatorics alone.

Cycle 207 hostile audit finds no flaw in the `HWB_(8m)` midpoint theorem. With
one-based coordinates, all data and compensator coordinates lie in the prefix,
suffix queries leave the data untouched, and distinct address indices require
distinct suffix weights, ruling out duplicate columns. The exact cut submatrix
is `K(z,j)=z_j`, with data words as rows and queries as columns; under the
opposite convention this is called the transpose of `INDEX_m`. The zero-weight
value is unused. The all-order OBDD lower bound is formal, while the MCSP and
unrestricted-model transfer gaps remain.

Cycle 208 isolates the exact MCSP transfer as `AMT(n,s,m)`: every balanced cut
must admit consistent rows and queries whose completions are easy iff the
queried row bit is one. A direct-sum implementation must prove a uniform
one-sided complexity gap after maximizing over all unqueried component choices;
this is stronger than recovering each component by restriction. The literal
disjoint-subcube gadget fails by gate sharing. Even pairwise distinct
components `f_i=H XOR x_i` combine as `H XOR x_a`, costing `C(H)+O(t)` rather
than `sum_i C(f_i)`. Easy circuit templates also obey the entropy ceiling
`m=O(r log(n+r))`, which is `N^o(1)` at the MMW threshold. A live construction
therefore needs genuine anti-sharing rigidity and still lacks the relational-
search/update-time transfer.

Cycle 264 freezes the smallest nontrivial literal address/data multiplexer with
an exact one-gate breaker. For `H=AND_8` and `f_i=H XOR x_i`, essential-variable
counting gives exact costs `C_B(H)=7` and `C_B(f_i)=8`, while computing `H` once
and multiplexing `x_1,x_2` gives an eleven-gate shared circuit. Thus
`11<2(7-1)=12`, so even the conservative additive baseline fails, and
`11<8+8` refutes exact additivity. Since the desired rigidity is universal over
unqueried component choices, this explicit joint choice is a complete breaker
for the frozen gadget. It does not refute abstract `AMT` or imply an MCSP or
P-versus-NP lower bound.
