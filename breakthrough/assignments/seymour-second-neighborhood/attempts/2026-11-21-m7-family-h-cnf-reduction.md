# Provisional exact CNF reduction for the order-18, seven-hole family H

## Status and scope

This note treats only family H from
`2026-11-19-m7-witness-pattern-cover.md`.  It does **not** claim Seymour's
second-neighborhood conjecture, the whole `m=7` case, or either other witness
family.  The mathematical result here is a forward reduction from a family-H
candidate to each of two finite CNFs.  The reported CaDiCaL/DRAT results are
provisional computational evidence until the checked artifacts are replayed
from the committed generator.  No proof file is retained in this packet.

Assume an oriented graph `D` on 18 vertices with exactly seven missing
unordered pairs.  Its two degree-nine vertices are `q,r`; every other vertex
has degree eight.  Assume every vertex is strictly non-Seymour:

```
|N++(x)| < |N+(x)| for every vertex x.                         (1)
```

Family H chooses a low vertex `v` and arcs

```
v -> q -> r,                                                    (2)
```

such that `v` remains a tight witness after deleting `q`, and `q` remains a
tight witness after deleting `r`:

```
N++_(D-q)(v) = N++_D(v),
N++_(D-r)(q) = N++_D(q).                                       (3)
```

For `A=N+(v)`, `B=N++(v)`, and
`C=V(D)\({v} union A union B)`, tightness gives

```
|A|=8, |B|=7, |C|=2, q in A.                                  (4)
```

The walk in (2), exact-distance-two semantics, and orientation split the
candidate space into two exhaustive labelled location cases:

```
case A: r in A;       case B: r in B.                           (5)
```

Labels are fixed as

```
v=0, q=1, A={1,...,8}, B={9,...,15}, C={16,17};
case A has r=2, and case B has r=9.                              (6)
```

Relabelling is legitimate because the ordinary vertices within the relevant
blocks are indistinguishable before labels are chosen.  The generator further
sorts the three possible `q`-pair statuses (out, in, hole) within each uniform
block.  A permutation inside a block is an automorphism of every other clause,
so every orbit has a sorted representative.  This is a symmetry break, not a
new graph hypothesis.

## Exact formula

`experiments/m7_family_h_cnf.py` is standalone and deterministic.  Its named
variables are:

```
a_i_j       iff i -> j;
p_i_k_j     iff i -> k and k -> j;
r_i_j       iff some length-two i-k-j walk exists;
q_i_j       iff j is an exact second neighbor of i;
h_i_j       iff the unordered pair {i,j} is missing;
cnt_*       exact unary sequential-counter states.
```

The clauses impose, with all displayed quantifiers finite over `{0,...,17}`:

1. no loops or digons;
2. `q_i_j <-> (!a_i_j and OR_k(a_i_k and a_k_j))` for every `i != j`;
3. exact outdegree nine at `q,r`, and eight elsewhere;
4. exactly seven missing unordered pairs;
5. strict badness (1), namely `|N++(q)|<=8`, `|N++(r)|<=8`, and
   `|N++(x)|<=7` for every low `x`;
6. the exact rooted layers (4), plus the necessary root-support clauses
   `OR_{a in A} a->b` for every `b in B` and the forced absence of all
   `A->C` arcs;
7. `|N++(q)|=8`, `q->r`, and `{v} union C subset N++(q)`;
8. for every `b in B`, an `A\{q}` predecessor of `b`, which is exactly the
   preservation needed in (3) for the low root;
9. for every `x in N++(q)\{r}`, a `q-k-x` path with `k != r`, which is exactly
   the preservation needed in (3) for the high root;
10. the proved within-block status ordering described above.

Items 8 and 9 are both necessary for a family-H candidate.  Conversely, the
formula intentionally omits arc-minimality, strong connectivity, and selectors
for unrelated deletion witnesses.  These omissions only relax the candidate
hypotheses.  Therefore:

> **Forward reduction.** Every family-H candidate satisfying (1)--(4) can be
> relabelled to a satisfying assignment of case A or case B.  Consequently,
> independently checked UNSAT certificates for both generated CNFs eliminate
> family H under the displayed assumptions.

This implication is the exact mathematical content.  Solver output by itself
is not substituted for certificate checking.

## Independent negative control

`experiments/test_m7_family_h_cnf.py` evaluates a fixed graph without trusting
the CNF auxiliaries.  It has degree sequence `(8,9,9,8,...,8)`, exactly the
seven holes

```
{1,16}, {1,17}, {12,17}, {13,17}, {14,17}, {15,17}, {16,17},
```

and exact layers

```
N+(0)  ={1,...,8},       N++(0)={9,...,15},
N+(1)  ={2,3,9,...,15},  N++(1)={0,4,5,6,7,8,16,17}.
```

Both equalities in (3) hold.  It nevertheless has Seymour vertices
`3,...,17`; hence it is deliberately **not** globally bad.  The test constructs
all graph-semantic and counter-variable truth values directly, checks that the
graph satisfies every clause when global badness is omitted, and checks that
precisely the expected badness clauses fail in the production formula.  This
catches accidental UNSAT caused by the local family-H constraints.

The archived exploratory cores
`experiments/legacy-family-h/h_qrow_exact.py` and `hxe_sym.py` are retained
verbatim for provenance (SHA-256 respectively
`61d272ff5115d7aa2d69209e5124e6b8c1116d03c830207f5ea0f4eff7415f5b` and
`05b7a436044db12946672c77201032662cf15d146658ede8ef52db3b658e5457`).
They depend on `snc_cnf.py`, are not the production generator, and are not
imported by the exact semantic test.

## Reproduction

From `breakthrough/assignments/seymour-second-neighborhood` run:

```
python3 -B experiments/test_m7_family_h_cnf.py
python3 -B experiments/m7_family_h_cnf.py --case A \
  --output /tmp/m7-family-h-A.cnf --map-output /tmp/m7-family-h-A.map
python3 -B experiments/m7_family_h_cnf.py --case B \
  --output /tmp/m7-family-h-B.cnf --map-output /tmp/m7-family-h-B.map
```

The writer fails closed rather than overwriting an existing output.  For the
committed generator the expected comment-free DIMACS records are:

```
case A: 23292 variables, 89249 clauses, 1572702 bytes,
        sha256 22f8107f8dc0d3fd9ce03ea4e7b2995a8b749457d721dc0ee16e40ac10e8e012
case B: 23292 variables, 89249 clauses, 1572685 bytes,
        sha256 4686ccca33f81749c8b88cccfd06a566323ee7a0e8bd83726778a76a8eb35b60
map:    456630 bytes,
        sha256 01643ce36c1daaa7eb3e28c7ac9a87303e58e279e15b39efa2d8d9e79025e7c2
```

The existing pinned tools can then be used without adding binaries:

```
SOL=certificates/m7-family-s-h1-certificate/tools/cadical-1.7.3
CHK=certificates/m7-family-s-h1-certificate/tools/drat-trim
$SOL -q /tmp/m7-family-h-A.cnf /tmp/m7-family-h-A.drat
$CHK /tmp/m7-family-h-A.cnf /tmp/m7-family-h-A.drat
# repeat for B; optionally compress only after verification
xz -9 -k /tmp/m7-family-h-A.drat
```

Do not infer success from a timeout, an exit code without `s UNSATISFIABLE`, or
an unchecked proof.

## Provisional solver and clause-family scout

A separate run restricted global badness to `B union C={9,...,17}` while
keeping `|N++(q)|=8` in the mixed-tightness group.  Each formula then had
23,292 variables and 89,241 clauses.  CaDiCaL 1.7.3 returned UNSAT for both;
`drat-trim` independently printed `s VERIFIED` for both ASCII DRAT files.
Exact scout records were:

```
case A CNF sha256 ba88f34742be989ae93f3812b1f51b9e4a5f59c7580409f1920ee46880ae7dd8
case B CNF sha256 31a363c14974bde72f36394fc43b243aaf6cd1110fa3b40034b4f9c9f43950d0

case A DRAT: 655910844 bytes,
  sha256 b1c2c675456d3e1c98904fc708449a6c4d5457204d3986257cdb0e8d92d91a6d
  Python lzma FORMAT_XZ preset=9: 233234708 bytes,
  sha256 86c20401ee737d3f64a461318fe7cc12f83debd0062729d123cb1c20b59b9ae4
case B DRAT: 1032268369 bytes,
  sha256 33aaf885904f5e6e84073f87da4b621257fd90e52d4c05480ac7b62b810310a7
  Python lzma FORMAT_XZ preset=9: 374599004 bytes,
  sha256 947b19b30ce3b7db59d3c1a5e37a2c1d71b6a5db93fed0792e638f89d09bf2ac
```

The raw and compressed proofs are intentionally not retained.  This establishes
only a replayable target: the production generator does not expose a command
line switch for partial badness, and the scout CNFs/proofs are not committed.

`drat-trim`'s proof-dependent original-clause cores had 18,066 clauses in case
A and 17,453 in case B.  In those particular cores every coarse clause family
except `low_root_second` and `low_root_support` appeared.  Case A used all nine
badness units `9,...,17`; case B used the eight units `10,...,17` and omitted
the badness unit for `r=9`.  These facts show only that this proof trace did not
use the omitted clauses; a DRAT core is not a minimal unsatisfiable subset.

Deletion of an entire family from those proof-dependent cores gave actual SAT
models for both cases for each of:

```
oriented, exact-distance-two semantics, degree, distance-two counters,
global-badness units, hole semantics, seven-hole cardinality,
low-root-first, low-root-no-C, and status symmetry.
```

Thus each of those families is necessary **relative to that extracted core**.
Notice especially that status symmetry is logically only symmetry breaking,
yet its deletion makes this *proof-dependent subset* SAT: extraction selected
only a canonical slice of the otherwise symmetric clauses.  This does not make
the status-order clauses a hypothesis of the underlying graph theorem.

Deleting any one of mixed tightness, `q->r`, high-root exhaustion, either
robustness family did not yield a SAT model in the allotted runs; most instead
were eventually solved UNSAT, so those tests do not establish necessity.  In
particular, there is no claim that the committed semantic presentation is a
minimal clause-family UNSAT formula.

Badness on `C` alone is SAT in both cases.  Badness on `B` alone remained
unresolved under long time limits.  Badness on `B union C` is the strongest
proved partial-badness scout here: it suffices computationally in both cases,
but only the full production formulas belong to this packet.  All timings and
minimality statements remain provisional until an independent artifact replay.
