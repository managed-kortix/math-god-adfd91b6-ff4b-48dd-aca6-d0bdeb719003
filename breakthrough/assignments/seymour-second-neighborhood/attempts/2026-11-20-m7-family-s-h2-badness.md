# Exact global-badness exclusion of family-S `h=2`

## Exact theorem boundary

In the order-18 seven-hole normal form, let `r,q` be the two degree-nine
vertices and all others have degree eight. Suppose one low vertex `w` is a
robust deletion witness for both highs. With

```
A=N+(w), B=N++(w), C=V\({w} union A union B), T={w} union A union B,
```

there is no globally bad completion having exactly two holes internal to `T`.
No vertex- or arc-minimality clause is used. This closes only the exact
shared-low family-S `h=2` cell. It gives no inference for `h=0,1`, any other
`m=7` family, all order 18, or Seymour's conjecture.

The one-way bridge is the same exact relabelling argument as for `h=3`: fix
`w,r,q`, quotient the six ordinary A labels and seven B labels by their
permutation groups, record every C incidence by multiplicity, then quotient by
swapping C. These relabellings preserve degree, holes, exact second distance,
global badness, root layers and both deletion-robustness clauses. Every genuine
configuration therefore maps to one canonical row, but a row need not complete.
For each `b in B`, requiring an A predecessor other than `r` and one other than
`q` is exactly what preserves the two-walk `w->A->b` under either deletion; row
units exclude A-to-C arcs, so no extra exact second neighbor can occur.

## Independent cover

The independent sorted-word census derives the row universe from the two low-C
degree equations and seven-hole equation, importing neither production census
nor CNF production. At `h=2` it finds

```
1,964 pre-C-swap type rows; 34 fixed type rows; 999 canonical rows.
1,065,015 labelled states; 315 pointwise fixed; 532,665 labelled C-swap orbits.
```

The 34 type-level fixed rows have total multiplicity weight 18,375, but most
of those labelled states are permuted rather than fixed pointwise by swapping
C.  Exactly 11 fixed type rows contain the 315 pointwise-fixed states used in
Burnside's formula.

The exact ordered-universe SHA-256 is
`f75ccdf6075085bbfe1cb1b9f1058452a37c644f0870057fcc38a3ef05e16d0b`.
An independent DIMACS reconstructor byte-compares all variables and clauses.
Auxiliary tests truth-table gates and counters and validate all row units.

## Single exact logical package

The exact consecutive range `[0,999)` has 999 paths, no residual, and totals
735,323,691 raw proof bytes and 154,581,588 XZ bytes. The latter is strictly
below the exclusive 250,000,000-byte logical-package convention. Largest is row
979: 3,750,648 raw and 1,212,404 compressed bytes.

The retained manifest SHA-256 is
`8fcd8e16b596fd368c33c9c273a1cf0ec50b2c27b8a61ce2ae6f4e041b77e8fc`.
It binds the exact consecutive range, every ordered row JSON, regenerated CNF
size/hash, compressed proof size/hash and raw proof size/hash. Its
`ordered_residual` is empty.

The strict `python -O` verifier independently reconstructs the full universe,
checks safe exact filenames and absence of symlinks/missing/orphan files,
recomputes the exclusive cap, byte-checks every independently reconstructed
CNF, authenticates decompressed proofs, and requires both
`c detected empty clause` and `s VERIFIED` from the pinned checker for each of
999 proofs. Hostile mutations check their exact failure gates for order,
duplicate/missing rows, range, JSON aliases/duplicate keys, CNF/proof hashes,
exclusive-cap equality, missing/orphan/nonregular artifacts, and substitution
of the proof checker or either independently authenticated helper.

## Provenance versus proof validity

The proof-producing run used the presently observed CaDiCaL 1.7.3 executable,
SHA-256 `5bfb078ad14e690745df9667a69b4d148d58e1ef3e39f7f782a0a30e259d7f8a`,
from a checkout currently at source commit
`38e073b389a877b0a0d3c91136d2443ab95fdeba`. This is recorded producer
provenance for this run, not a claim about an unavailable historical binary.

Proof validity is separate: fresh replay uses `drat-trim` executable SHA-256
`92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a`
from a checkout currently at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The verifier authenticates this
exact checker executable before replay. Compression/decompression is Python
3.12.13 `lzma` at preset 9, with Python executable SHA-256
`7d43f6e86a6c6dd12005ec77eb2055f1be3f1bb3adedf8afe0a87973fa7371ce`
and runtime `liblzma.so.5` SHA-256
`26b37d25f7ca2a2d348de8ecabacda12e921cd933b21fa069a179760db77219d`.

The retained repository package consists of the 999 compressed DRAT artifacts,
the exact manifest, independent universe checker, independent semantic tests,
strict verifier, and hostile mutation suite.  It is a finite theorem package for
the `h=2` shared-low cell only; it is not a paper or a publication claim.
