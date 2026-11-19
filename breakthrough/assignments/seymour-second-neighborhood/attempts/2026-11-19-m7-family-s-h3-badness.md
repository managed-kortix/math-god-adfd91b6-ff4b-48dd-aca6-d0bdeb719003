# Exact global-badness exclusion of family-S `h=3`

## Theorem and exact boundary

In the order-18, seven-hole normal form, suppose the two degree-nine vertices
are `r,q`, every other vertex has degree eight, and one low vertex `w` is a
robust deletion witness for both highs.  Put

```
A=N+(w),  B=N++(w),  C=V\({w} union A union B),
T={w} union A union B.
```

There is no globally bad completion with exactly three holes internal to `T`.
Equivalently, the exact shared-low family-S `h=3` cell is empty.  This statement
uses neither vertex nor arc minimality.

This theorem says nothing about `h=0,1,2`, the distinct-low family, either
high-root family, or any other `m=7` family.  In particular it is not a closure
of family S, `m=7`, order 18, or Seymour's conjecture.

## One-way bridge to the finite cover

Relabel a genuine configuration so that

```
w=0, r=1, q=2, A={1,...,8}, B={9,...,15}, C={16,17}.
```

For each of `w,r,q`, record which C incidences are holes.  Record the
multiplicity of the four such hole types among the six ordinary A vertices.
For each B vertex record its ordered pair of C incidences, each one being
`C->B`, `B->C`, or a hole, and record the nine multiplicities.  Finally record
the C-pair state.  The two low-C outdegree equations and the seven-hole equation
force exactly one of 436 pre-C-swap type rows at `h=3`.  There are no C-swap
fixed rows, hence exactly 218 canonical rows.

Permuting the six ordinary A labels, permuting the seven B labels, and swapping
C preserves every hypothesis: degree sequence, holes, exact second-neighborhood
semantics, global badness, rooted layers, and the two deletion-robustness
conditions.  Thus every genuine `h=3` configuration relabels into one of the
218 canonical CNFs.  This is a one-way cover statement; a row need not have a
completion.  Checked UNSAT of every row plus this bridge proves emptiness of the
cell.

The ordinary-label multiplicity weights give 43,470 fully labelled type states
before the C swap.  The C swap has zero fixed type rows and zero fixed labelled
states at `h=3`, so these form 21,735 labelled-state C-swap orbits.  The 218
canonical rows cover those weighted orbits; they are not 21,735 separate CNFs.

## Exact formula

The formula has arc variables for all ordered pairs, excludes loops and digons,
and links exact-second variables to

```
i != j, not(i->j), and some i->k->j.
```

Exact counters impose degree nine on `r,q`, degree eight elsewhere, exactly
seven holes, and strict badness `d++(v)<d+(v)` at every vertex.  The root row
fixes `N+(w)=A`.  For each `b in B`, one A predecessor other than `r` and one
other than `q` is required.  Since the row fixes every A-to-C arc absent, these
clauses give `N++(w)=B` both originally and after deletion of either high.  A
row adds only exact C-incidence unit clauses.  All T pairs remain existential.

## Independent cover and encoding boundaries

`m7_family_s_h3_universe_check.py` imports neither row production nor CNF
production.  It reconstructs multisets from the two low-C degree equations and
the hole equation using sorted words, verifies C-swap closure, exact set
cardinalities and weighted counts, and compares an ordered ledger by exact set
and order equality with duplicate rejection.  Its ordered-universe SHA-256 is

```
356bf301e8df633d503800ebfe79a5405011eca53dd9f69f76ba5a0b55cf3705.
```

`check_m7_family_s_badness_cnf.py` imports neither the producer, `snc_cnf`, nor
the row census.  It hostile-parses DIMACS, independently reconstructs every
variable and clause, validates each row from the degree/hole margins, and
requires byte equality.  `test_m7_family_s_h3_semantics.py` independently tests
the AND definition, exhaustively truth-tables counters through width eight,
uses fixed-seed random assignments through width seventeen, and checks every
fixed literal of all 218 independently regenerated rows.

## Certificates and replay

All 218 exact CNFs have checked DRAT refutations.  The raw proofs total
252,432,213 bytes.  Their deterministic XZ representations total 66,265,340
bytes.  The largest raw proof is row 215 at 8,154,291 bytes.  The manifest binds
each ordered row to its CNF bytes/hash, compressed proof bytes/hash, and raw
proof bytes/hash; its SHA-256 is

```
558cd23ac90d16d4022e9bd6a446077b8360b3c6d9ec4c0d35950ce39ea20b21.
```

Proof generation used CaDiCaL 1.7.3, source commit
`38e073b389a877b0a0d3c91136d2443ab95fdeba`, binary SHA-256
`5bfb078ad14e690745df9667a69b4d148d58e1ef3e39f7f782a0a30e259d7f8a`.
The manifest also pins SHA-256 identities of the CNF producer, independent CNF
reconstructor, independent universe checker, and semantic test source.

Strict replay pins `drat-trim`, source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary SHA-256
`92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a`.
The verifier requires both `c detected empty clause` and `s VERIFIED` for every
proof, not a solver status code.

`test_m7_family_s_h3_verifier_mutations.py` negatively mutates row order, row
uniqueness/completeness, CNF and proof hashes, artifact presence/extraneousness,
and the checker binary pin; all eight hostile cases must be rejected.

The strict verifier uses explicit exceptions rather than Python assertions, so
`python -O` does not disable its checks.  It rejects a wrong checker binary,
wrong metadata, duplicate/missing/orphan/out-of-order rows, nonempty residual,
missing/orphan proof files, any hash or size mismatch, CNF reconstruction
failure, decompression failure, absent empty-clause detection, or failed DRAT
verification.

From the experiments directory, replay with:

```sh
python3 m7_family_s_h3_universe_check.py
python3 test_m7_family_s_h3_semantics.py
python3 -O verify_m7_family_s_h3_campaign.py \
  --manifest m7-family-s-badness-h3-manifest.json \
  --proof-dir ../certificates/m7-family-s-badness-h3 \
  --drat-trim /path/to/pinned/drat-trim \
  --cnf-checker ./check_m7_family_s_badness_cnf.py \
  --universe-checker ./m7_family_s_h3_universe_check.py
```

Only the successful independent cover check and full fresh certificate replay,
not the original proof-producing solver exits, establish the finite theorem.
