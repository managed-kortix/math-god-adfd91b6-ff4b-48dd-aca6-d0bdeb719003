# Exact global-badness exclusion of the family-S `h=4` cell

## Scope and result

Use the order-18, seven-hole normal form.  The two degree-nine vertices are
`r=1,q=2`; all other vertices have degree eight.  In family S, a common low
robust witness `w=0` points to both highs.  Put

```
A=N+(w)={1,...,8}, B=N++(w)={9,...,15}, C={16,17},
T={w} union A union B.
```

This package excludes exactly the subcell in which four of the seven holes are
internal to `T`.  It imposes global SNC badness and both shared-low deletion
conditions, but **not arc minimality**.  It does not exclude the `h=0,1,2,3`
cells and therefore does not exclude all family S or all `m=7` graphs.

## Exact semantic formula

For every ordered pair, `a_ij` means the arc `i->j`.  Digons and loops are
forbidden.  A Tseitin variable records each two-walk `i->k->j`; `q_ij` is
linked exactly to

```
i != j, not a_ij, and some i->k->j.
```

Thus `q` is the exact second-neighborhood relation, not raw two-walk
reachability.  Exact unary counters impose

```
d+(1)=d+(2)=9; d+(v)=8 otherwise;
d++(1),d++(2)<=8; d++(v)<=7 otherwise;
exactly seven holes.
```

The last line of each degree case is precisely strict global badness
`d++(v)<d+(v)`.  The rooted row fixes `N+(0)=A`.  For every `b in B`, the two
clauses

```
some x in A\{1} has x->b;  some x in A\{2} has x->b
```

say that `b` remains an exact second neighbor of `0` after deleting either
high.  Because every `A->C` arc is excluded by the exact type row, these clauses
also give `N++(0)=B` and the two required equalities after deletion.  No vertex-
or arc-minimality selector is present.

The unsplit base has 23,292 variables and 89,170 clauses, SHA-256
`f95154c104e9a21dbe87b3e73cb07583cb8e801976ab1045cbb87d8e8780a060`.
It remained observationally UNKNOWN after a 600-second CaDiCaL run and several
short alternate CaDiCaL/Kissat modes.  No logical conclusion is drawn from
those timeouts.

## Why 43 rows cover the exact `h=4` cell

The exact C-incident type census fixes `w,r,q`, quotients the six ordinary A
labels by `S6`, the seven B labels by `S7`, and then quotients by swapping the
two C labels.  At `h=4` there are:

```
81 rows before the C swap, 5 fixed rows, 43 C-swap orbits.
```

They represent 729 fully labelled C-incidence states (369 labelled-state
orbits after C swap).  The 43 are therefore canonical **type orbits**, not
26,060 labelled rows; 26,060 is the all-`h` count before C swap.

The quotient is sound because each permutation fixes `w,r,q` and preserves
A/B/C membership, exact degrees, the seven-hole count, exact second-neighborhood
semantics, strict badness at every vertex, and both robustness column clauses.
Swapping the two C vertices preserves the same predicates.  Relabelling any
completion by these permutations maps its C incidence to exactly one of the 43
representatives.  Conversely each representative is imposed only by literal
units, with all T pairs still existential.  Hence UNSAT of all 43 formulas
covers every completion in the `h=4` cell.

## Certificate workflow and independent checks

`m7_family_s_badness_pilot.py` emits the base or one deterministic row CNF.
`check_m7_family_s_badness_cnf.py` imports neither the producer, `snc_cnf`, nor
the type-row census.  It hostile-parses the DIMACS, independently reconstructs
the complete variable order and clause stream, truth-tables its unary counter
implementation through width eight, validates the row's C-degree/hole
identities, and requires byte equality.

`m7_family_s_badness_campaign.py` solves all 43 rows, checks every CaDiCaL DRAT
with `drat-trim`, and can retain compressed proofs plus a content-hash manifest.
`verify_m7_family_s_badness_campaign.py` regenerates every CNF, reruns the
independent checker, authenticates compressed and raw proof hashes/sizes, and
replays all proofs.  SAT output, if any, is checked clause-by-clause and by a
producer-independent direct graph-semantic checker.

The audited run used CaDiCaL 1.7.3 at source commit
`38e073b389a877b0a0d3c91136d2443ab95fdeba`.  Proof replay is pinned to the
`drat-trim` binary SHA-256
`92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a`, built
from source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.  The strict verifier rejects
a different proof-checker binary.

In the audited run all 43 rows were certified UNSAT.  The raw proofs total
96,667,825 bytes; XZ-compressed proofs total 30,052,332 bytes.  These proof
artifacts should only be cited together with their generated manifest and full
replay; solver status alone is not the theorem.
