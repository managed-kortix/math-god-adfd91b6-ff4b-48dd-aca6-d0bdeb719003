# Order-18 family-S `h=1` exact global-badness exclusion

## Exact theorem boundary

Work in the order-18 seven-hole normal form.  Let `r,q` be the two
outdegree-nine vertices and let every other vertex have outdegree eight.
Suppose one low vertex `w` is a robust deletion witness for both highs.  Put

```text
A=N+(w),  B=N++(w),  C=V\({w} union A union B),
T={w} union A union B.
```

There is no globally strict-SNC-bad completion in this shared-low family-S
cell having exactly one hole internal to `T`.  The finite formula uses neither
vertex-minimality nor arc-minimality.

This excludes only the exact family-S `h=1` cell.  It does not cover family-S
`h=0`, families D or H, another `m=7` family, all order-18 oriented graphs, or
Seymour's Second Neighborhood Conjecture.

## Exact finite cover

An independent sorted-word reconstruction gives 6,186 pre-V4 C-incidence rows.
The commuting actions exchange `C={16,17}` and the equal-degree highs.  Their
fixed counts `(e,C,H,CH)` are `(6,186,0,1,490,0)`, yielding 1,919 canonical
rows.  Multiplicity expansion gives 14,428,260 labelled states and 4,763,052
labelled V4 orbits.

For each canonical row, the stabilizer on
`T={0,...,15}` permutes vertices only inside complete C-incidence type blocks.
There are 61,696 unordered-pair orbits and 168,584 guarded nonrepresentative
pair occurrences over the canonical rows.  Since each row fixes six C-incident
holes while the base has exactly seven holes, every completion in the row has
exactly one T-hole.  One representative per row-stabilizer pair orbit is
therefore an exhaustive normalization.

The selector parent is

```text
base
and 28 common C-incidence units
and OR_R selector_R
and, for each R, selector_R ->
    (38 residual row units and all nonrepresentative-hole guards for R).
```

No at-most-one selector clauses are needed: every parent model satisfies a
selected child, while every child model extends by selecting only that child.

## Hostile bridge repair

A pre-integration hostile audit rejected an earlier composite checker because
it treated C exchange as fixing every ordinary label of `T`.  That is false:
a C exchange transposes the two-coordinate C-incidence types and generally
re-sorts ordinary-A and B labels in the canonical row realization.  For
pre-row 3, the source B-type word

```text
(4,4,4,4,5,5,7)
```

becomes `(4,4,4,4,7,7,5)` before sorting, while the canonical word is
`(4,4,4,4,5,7,7)`.  Consequently the source hole `{0,13}` maps under C
exchange to `{0,14}`, not `{0,13}`.

The retained checker now constructs the full canonicalizing permutation:
it applies the C/high type action, maps the high labels, and uses the
order-preserving bijection between every transformed ordinary-A/B type class
and its sorted canonical block.  It then supplies an explicit permutation
inside the canonical-row stabilizer from the moved pair to the retained pair.
The row-3 `{0,13}->{0,14}` case is a pinned regression.

The repaired bridge exhausts all `6,186*C(16,2)=742,320` pre-row/pair cases and
all 921,120 canonicalizer witnesses, including 178,800 cases with two
canonicalizing V4 elements.  Every ambiguity lands in one stabilizer orbit.
The transcript digest binding pre-row index, V4 element, source pair, full
16-label map, moved pair and target is

```text
c8b8cc8696ac80cb89f6774cdf1a7ea1cd051c9516d3e0be809aa5fe4d37bcc2
```

The canonical-row pair-orbit digest is

```text
922c184dcfaa6dc2fc2ae613b93b7e2b092a797faeeab9956f8865e44bdabb98
```

A separate hostile reconstruction rechecked all 742,320 cases, enumerated
7,644,052 admissible endpoint-image combinations inside transformed type
classes, and found no alternative canonicalizing bijection reaching a
different retained orbit.  It also checked transport of every exact 66-unit
row-incidence set and the actual selector/hole guards in the retained CNF.

## Formula and proof identities

```text
ordered V4 rows             1,919
ordered-universe SHA-256
  d713ca11b98de20010c923bf1cbe756230d2c9728834ffab51fb65c39068131f

CNF variables              25,211
CNF clauses               330,705
CNF bytes               5,891,576
CNF SHA-256
  31db9866c15372555f9c102b3126fb4e8730f879b5e82ca5f6791318398d4e43

raw DRAT bytes          30,989,483
raw DRAT SHA-256
  32f35d5b3b0458c05f59bcf4467f3bb40103294e0100d7ba8276c2972cfa9de9

XZ-9 proof bytes         2,471,364
XZ-9 SHA-256
  089e6ded1354db86151092c0603ca1d8aa5397bf7b4b7916c71ad6830375eaba
```

The default verifier independently reconstructs the exact ordered universe,
variable order, clause order and DIMACS bytes in a temporary directory.  It
runs the repaired bridge, authenticates compressed and raw proof identities,
and replays the proof with package-local, source-pinned `drat-trim`, requiring
both empty-clause detection and exactly one `s VERIFIED`.  The package-level
hostile suite rejects 29 tree, mode, schema, identity, semantic-CNF and proof
mutations.  A separate optional command runs package-local identity-pinned
CaDiCaL 1.7.3 and reproduces the exact raw and XZ proof bytes; the solver is not
part of proof validity.

## Reproduction

From the self-contained package at
`../certificates/m7-family-s-h1-certificate/`:

```sh
python3 -O -B verifier/verify_h1_package.py
python3 -O -B verifier/hostile_mutations.py

# Optional proof-production reproduction only:
python3 -O -B verifier/reproduce_proof.py
```

The retained binary tools target GNU/Linux x86-64 with glibc; the Python
verifiers require Python 3.10 or newer.  `metadata/SHA256SUMS` is an internal
integrity map, not a signature.  The containing Git commit/tree is the external
authenticity anchor.

## Scope conclusion

This is a retained exact finite-cell exclusion, not a solution of the frozen
assignment.  Family-S `h=0` and the mixed/distinct-low families remain open,
so no state transition, paper, announcement or publication action follows.
