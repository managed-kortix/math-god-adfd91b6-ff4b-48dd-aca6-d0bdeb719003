# Family-S h1 certificate

**Status:** retained finite certificate for the exact order-18, seven-hole,
shared-low family-S `h=1` cell. It proves that no globally strict-SNC-bad
completion exists in this cell. It does **not** cover family-S `h=0`, another
`m=7` family, all order-18 oriented graphs, or Seymour's Second Neighborhood
Conjecture. No vertex- or arc-minimality clauses are used.

## Exact statement

Label the 18 vertices so that the common low deletion witness is `w=0`, the two
degree-nine vertices are `1,2`,

```text
A=N+(w)={1,...,8}, B=N++(w)={9,...,15}, C={16,17},
T={w} union A union B={0,...,15}.
```

The formula requires an oriented graph with exactly seven holes, outdegree nine
at `1,2` and eight elsewhere, strict badness `d++(v)<d+(v)` at every vertex,
the displayed root layers, and preservation of every member of `B` as an exact
second neighbor of `w` after deleting either high. It fixes exactly one hole
internal to `T` (`h=1`) through an exact finite C-incidence cover. The checked
CNF is UNSAT.

## Finite cover and bridge

The independent sorted-word census has 6,186 pre-V4 rows. Quotienting by the
commuting exchange of `C={16,17}` and exchange of the equal-degree highs
`{1,2}` gives 1,919 canonical rows: 745 V4 orbits of size two and 1,174 of size
four.

For a fixed canonical row, the full labelled stabilizer on `T` consists of
permutations inside complete C-incidence blocks:

- `w` is fixed;
- highs `1,2` merge only when their complete two-bit C types agree;
- ordinary A vertices merge only within one complete two-bit C type;
- B vertices merge only within one complete ordered two-symbol C type.

Because exactly one T-hole remains, every unordered T-pair may be moved to one
representative of its row-stabilizer orbit. A C exchange generally re-sorts the
ordinary-A and B labels by their transformed complete C-incidence types; it does
**not** fix those labels pointwise. The retained composite checker constructs
that full type-sorting canonicalizing permutation before applying the canonical
row stabilizer. It exhausts all `6,186 * C(16,2) = 742,320` pre-row/pair cases,
including every ambiguous canonicalizing V4 map, and constructs 921,120 explicit
composite mapping witnesses. A regression pins pre-row 3 under C exchange at
hole `{0,13}` to moved/retained hole `{0,14}`. The canonical rows have 61,696
pair orbits and 168,584 guarded nonrepresentative pair occurrences. This
normalization is special to exactly one T-hole and must not be reused for
multiple simultaneous T-holes.

The selector parent is

```text
base
and 28 common C-incidence units
and OR_R selector_R
and, for each R, selector_R -> (38 residual row units and hole normalizer_R).
```

No at-most-one selector clauses are needed. Any parent model satisfies a
selected child; any child model extends by selecting only that child.

## Frozen identities

```text
CNF variables             25,211
CNF clauses              330,705
CNF bytes              5,891,576
CNF SHA-256 31db9866c15372555f9c102b3126fb4e8730f879b5e82ca5f6791318398d4e43

ordered rows                1,919
ledger bytes               89,912
ledger SHA-256 9c82a2a1fbe44872278cc4d6fe71abd53c359d6cbf9e85eac9262986721e61fe
universe SHA-256 d713ca11b98de20010c923bf1cbe756230d2c9728834ffab51fb65c39068131f
full-map SHA-256 c8b8cc8696ac80cb89f6774cdf1a7ea1cd051c9516d3e0be809aa5fe4d37bcc2

raw DRAT bytes          30,989,483
raw DRAT SHA-256 32f35d5b3b0458c05f59bcf4467f3bb40103294e0100d7ba8276c2972cfa9de9
XZ-9 bytes               2,471,364
XZ-9 SHA-256 089e6ded1354db86151092c0603ca1d8aa5397bf7b4b7916c71ad6830375eaba
```

## Requirements

Default replay requires:

- Python 3.10 or newer;
- GNU/Linux x86-64 with glibc, for the retained proof-checker ELF;
- no network access and no external checkout or tool;
- Bash only for the command snippets/build recipe (the verifier itself is
  Python).

The package contains the pinned `drat-trim` binary, source, license and exact
build recipe. It also contains pinned CaDiCaL and its license solely for the
separate optional proof-reproduction command. The default verifier never runs
the solver. No documented command uses an absolute path.

## Verify from a clean checkout

From this package directory:

```bash
python3 -O -B verifier/verify_h1_package.py
python3 -O -B verifier/hostile_mutations.py
```

The default verifier is read-only. It checks the exact file tree and modes,
safe relative paths, canonical manifest, complete internal checksum map,
independently reconstructs the row universe and CNF in a temporary directory,
byte-compares the retained CNF, runs the complete composite bridge, authenticates
both compressed and raw proof identities, and replays the proof with the
package-local pinned checker. It does not run the SAT solver.

Optional proof reproduction is separate:

```bash
python3 -O -B verifier/reproduce_proof.py
```

The package-local solver must match the manifest's exact pinned binary identity.
The command requires UNSAT exit 20 and requires both the raw DRAT and
deterministic Python XZ-9 output to equal the retained bytes. It is optional and
does not participate in proof validity. `--solver` may point to a byte-identical
copy.

## Trust boundary

`metadata/SHA256SUMS` is a complete internal integrity map, not a signature and
not self-authentication. Authenticity must come from the Git commit/tree (or a
separately signed release) containing this package and verifier. Proof validity
comes from fresh package-local `drat-trim` replay; the solver is provenance and
optional reproducibility only.
