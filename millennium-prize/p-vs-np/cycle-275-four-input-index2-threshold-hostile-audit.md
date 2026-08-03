# Cycle 275: four-input `INDEX_2` threshold hostile audit

## Frozen semantics

Let

\[
 X=\{0,1\}^4,
\]

so a four-input Boolean truth table is an element of `\{0,1\}^X` and has
sixteen coordinates.  A midpoint cut is a set `A subset X` with `|A|=8`.
For

\[
 \rho\in\{0,1\}^A,
 \qquad
 \sigma\in\{0,1\}^{X\setminus A},
\]

there is exactly one completed function `f_{rho,sigma}:X -> {0,1}`, namely

\[
 f_{\rho,\sigma}(x)=
 \begin{cases}
   \rho(x),&x\in A,\\
   \sigma(x),&x\notin A.
 \end{cases}
\]

Thus the notation is sound only when `A` is a set of truth-table coordinates.
If `A` is instead a subset of the four input-variable names, `rho cup sigma`
does not specify a sixteen-bit truth table and the matrix is undefined.

Freeze the circuit model used in the preceding MCSP packets:

\[
 B=\{\operatorname {AND},\operatorname {XOR},\operatorname {NOT}\},
\]

with fan-in two for `AND` and `XOR`, fan-in one for `NOT`, free input and
constant sources, free fanout, and every Boolean gate counted.  Write `C_B(f)`
for minimum gate count and define

\[
 M_{A,s}(\rho,\sigma)
   =\mathbf 1[C_B(f_{\rho,\sigma})\le s].                       \tag{275.1}
\]

Changing any of free constants, the basis, fan-in, fanout, or whether `NOT`
gates are counted changes the threshold matrix and must not be left implicit.

## Exact `INDEX_2` test

The matrix contains the required pair-column pattern precisely if there are
two distinct columns `sigma_1,sigma_2` and four rows `rho_{00},rho_{01},
rho_{10},rho_{11}` such that

\[
 M_{A,s}(\rho_{ab},\sigma_1)=a,
 \qquad
 M_{A,s}(\rho_{ab},\sigma_2)=b
 \quad(a,b\in\{0,1\}).                                         \tag{275.2}
\]

Equivalently, the ordered pairs formed by the two columns contain all of
`00,01,10,11`.  This is the data-row/query-column orientation of `INDEX_2`;
transposing the convention does not change the residual-row conclusion.  Mere
nonidentity of the two columns, or merely obtaining both symbols in each
column, is not enough.

## Finite threshold range and endpoints

Every four-input function has finite `B`-circuit complexity.  For example,
XORing its disjoint satisfying minterms gives the crude uniform bound

\[
 C_B(f)\le 4+3(15)+14=63,                                      \tag{275.3}
\]

with the constant functions handled directly.  Hence

\[
 C_{\max}:=\max_{f:X\to\{0,1\}}C_B(f)
\]

exists and is at most `63`.  Since gate counts are integers, an existential
threshold can be restricted without loss to

\[
 0\le s<C_{\max};                                               \tag{275.4}
\]

the explicit coarse search range `0<=s<=62` is therefore sufficient.  At
`s>=C_max`, `M_{A,s}` is the all-one matrix, while at `s<0` it is the all-zero
matrix.  Neither constant matrix contains (275.2).  The nonnegative endpoint
`s=0` is not automatically constant because inputs, projections, and constants
are zero-gate functions under the frozen convention; it must be tested rather
than discarded by rhetoric.

Thus the property is impossible, not trivially true, at the genuinely constant
extremes.  Finiteness alone does not prove that an intermediate threshold has
the pattern.

## Logical defect

For an every-variable-order OBDD statement about one MCSP predicate, the needed
quantifiers are

\[
 \boxed{\exists s\in\{0,\ldots,C_{\max}-1\}\ 
        \forall A\subset X\ (|A|=8):\ P(A,s),}                 \tag{275.5}
\]

where `P(A,s)` is the `INDEX_2` condition (275.2).  The superficially similar
statement

\[
 \forall A\subset X\ (|A|=8)\ 
        \exists s_A:\ P(A,s_A)                                \tag{275.6}
\]

is strictly weaker and does not prove the desired claim: it allows the MCSP
threshold, hence the Boolean function represented by the communication matrix,
to change with the variable order.  A separate successful threshold for each
cut is not one fixed `MCSP_(4,s)` with width at least four in every order.

Accordingly, the logical defect is a quantifier swap if the proposed property
uses `forall A exists s`, or leaves the scope of `exists s` ambiguous.  The
repair is to place one bounded `exists s` before the universal balanced-cut
quantifier.  If the proposal already has the order (275.5), no endpoint or
finiteness defect remains; proving (275.5) is then a finite exhaustive question,
not a consequence of the definitions.

## Hostile verdict

`P275-FOUR-INPUT-INDEX2 AUDIT: the completion matrix is well-defined only over
the sixteen input assignments, the exact minor requires all four pair patterns,
and thresholds reduce to a finite nonconstant range.  The substantive logical
failure is allowing the existential threshold to depend on the balanced cut;
that changes the MCSP predicate with the OBDD order and cannot establish an
every-order lower bound for one fixed function.`

This audit identifies a finite-definition and quantifier defect only.  It proves
no nontrivial MCSP lower bound, unrestricted circuit lower bound, or
`P != NP` statement.

## Same-packet resource analysis

This section adds no mathematical intake.  It prices the exhaustive repair of
the frozen four-input packet on the current host (two hardware threads,
`4,105,240,576` bytes of RAM, `1,954,074,624` bytes currently available, and no
swap).

### Exact synthesis algorithm

Represent every four-input signal by its 16-bit truth table.  Start a circuit
state with the four projections and the two constants.  At depth `d`, a state
has at most `k=6+d` available signals.  Generate successors by applying `NOT`
to one signal or `AND`/`XOR` to one unordered pair, canonicalize the resulting
available-signal set, and breadth-first deduplicate it.  The first layer
containing a truth table is its exact complexity.  A parent state, operation,
and operands give an upper-bound circuit certificate; exhaustive completion of
all preceding layers gives the lower-bound certificate.  Replaying the layers
is therefore part of verification: the parent trace alone cannot certify
minimality.

The same-packet ANF construction in the companion exact-DAG design sharpens
(275.3): compute all eleven nonlinear monomials with eleven `AND` gates and XOR
the selected subset of the sixteen ANF terms with at most fifteen gates.  Hence
`C_max<=26`, so only thresholds `0,...,25` and synthesis depths through 26 are
needed.

For an implementation-independent finite bound, enumerate syntactic circuits
instead of relying on deduplication.  A length-`d` circuit has at most

\[
 P_d=\prod_{i=0}^{d-1}(6+i)(8+i)
     ={(d+5)!\over5!}{(d+7)!\over7!}                         \tag{275.7}
\]

gate choices: with `k=6+i` signals there are `k` unary choices and
`2 binom(k+1,2)=k(k+1)` commutative binary choices, hence `k(k+2)` total.
Enumerating every length through 26, evaluating each new gate as one 16-bit
Boolean operation, and retaining the least depth seen for every output is an
exact terminating algorithm.  Its concrete worst-case circuit count is

\[
 \sum_{d=0}^{26}P_d=
118173592517895525957484073499803224361661437534879082860452687873,
                                                                    \tag{275.8}
\]

less than `1.182 x 10^65`.  Thus depth-first exhaustive synthesis takes at
most the number in (275.8) circuit evaluations and fewer than 26 times that
many primitive 16-bit gate evaluations if each circuit is evaluated from
scratch.  An array of 32 16-bit
signals, 26 16-bit recursion choices, and the 65,536-byte complexity table uses
65,652 bytes of algorithmic storage, excluding implementation stack overhead.
The algorithm can emit all upper certificates in at most
`65536*26*2=3,407,872` bytes when each gate is encoded in 16 bits.  This small
memory bound does not make the time bound usable.  The table plus these traces
is a recomputation certificate: a checker verifies each upper trace and reruns
the exhaustive enumeration through one less than the claimed complexity for
the lower bounds.  Its verification-time bound is again (275.8); no succinct
lower-bound certificate follows merely from parent pointers.

Undeduplicated breadth enumeration has the same `P_d` bound on generated paths
and a useless certified frontier cap.  Even before hash-table and parent
metadata, storing each depth-26 path as its 26 non-source 16-bit signals
has the upper bound

\[
 52P_{26}=52{31!\over5!}{33!\over7!}>6.13\mathbin{\times}10^{66}
 \quad\hbox{bytes}.                                             \tag{275.9}
\]

The displayed quantity is an upper bound, not a claim that all those states are
distinct or necessary.  Canonical deduplication can be dramatically better in
practice, but the packet contains no proved frontier cap below current RAM.
Consequently a BFS run that starts under that RAM cap has no certified
completion guarantee.

### Exact balanced-cut pass

Once the 65,536 exact complexities are available, enumerate the exactly
`binom(16,8)=12,870` cuts.  For one cut and threshold, store each of the 256
columns as a 256-bit vector (four 64-bit words).  A column pair `u,v` passes
exactly when each of

\[
 \neg u\mathbin{\&}\neg v,\quad
 \neg u\mathbin{\&}v,\quad
 u\mathbin{\&}\neg v,\quad
 u\mathbin{\&}v
\]

is nonempty.  This is precisely the four-pattern test (275.2), not a proxy.
There are `binom(256,2)=32,640` pairs.  Testing every cut and every possible
nonconstant threshold `0,...,25` therefore has the concrete worst-case bounds

\[
 12,870\cdot26\cdot32,640=10,921,996,800                 \tag{275.10}
\]

column-pair tests and at most

\[
 4\cdot4\cdot10,921,996,800=174,751,948,800              \tag{275.11}
\]

64-bit quadrant-word tests.  Building one threshold matrix directly costs at
most `12,870*26*65,536=21,929,656,320` table comparisons and bit writes across
the full pass.  Sorting the 65,536 tables once by complexity and updating
columns incrementally reduces this to exactly
`12,870*65,536=843,448,320` bit insertions, plus sorting and resets.  Early exits
and omission of thresholds absent from the complexity spectrum only improve
these bounds.

The working memory is 8,192 bytes for the columns, 65,536 bytes for the
complexity table, and 102,960 bytes for one 64-bit success mask per cut, plus
constant enumeration and witness storage: 176,688 bytes in these three arrays.
A positive certificate needs at most 77,221 bytes when its threshold, two
columns, and four rows per cut are byte-encoded.  A negative certificate needs
at most 52 bytes for one 16-bit failing-cut index per candidate threshold.  In
either case a checker recomputes the four nonempty quadrants.

### Feasibility verdict

The balanced-cut bitset phase fits easily in current memory and is a bounded
two-core computation in the memory sense, although (275.11) gives no practical
wall-clock guarantee and makes an optimized compiled implementation
appropriate.  The exact-complexity phase is the decisive blocker.  Its
only unconditional packet-internal bound is over `1.18 x 10^65` circuit
extensions, while the available undeduplicated BFS frontier cap is over
`6.13 x 10^66` bytes before metadata.  This does not prove that a highly
deduplicated implementation would consume that space; it proves that the
packet supplies no host-fitting guarantee.  The current host is therefore
**not feasible for a certified end-to-end run under the available bounds**.  A
run would become authorizable only after supplying and verifying a substantially smaller
frontier/maximum-depth bound or an independently checkable exact complexity
table; neither is supplied by this same packet.
