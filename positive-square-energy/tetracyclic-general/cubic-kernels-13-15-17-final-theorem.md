# Cubic kernels 13--15 and 17: exact final theorem

## Theorem

Use upper-triangle pair order

`01,02,03,04,05,12,13,14,15,23,24,25,34,35,45`.

Every simple subdivision of cubic rank-four kernel 13, 14, 15, or 17 satisfies

`s^+(G) >= |V(G)|`.

The conclusion remains true after arbitrary rooted trees are attached at
arbitrary vertices, including internal vertices of subdivided paths. The
asserted inequality is nonstrict. In particular, the three symbolic kernel-14
families below are equality certificates, not strict certificates.

## Exact finite partition

The physical-row fixture contains all 376 genuine automorphism orbits of the
1400 labeled physical rows. The exact equilateral three-color sieve gives

`376 = 359 certified + 17 residual`.

The residual split is `K13=5, K14=6, K15=5, K17=1`. No switching quotient is
used in this census.

For the 16 residual orbits of kernels 13--15, the physical all-length frontier
has one canonical first-simple vector and nine one-coordinate `+2` vectors per
orbit. Its exact partition is

`160 = 148 strict rational certificates + 12 symbolic K14 targets`.

The 148 records use exact `Fraction` arithmetic and have cost strictly below
the tetracyclic excess budget three. The twelve remaining targets are the
canonical vector and coordinates `0,3,8` for each of these kernel-14 rows:

```text
(0,0,0,0,1,0,0,1,0,1,0,1,0,0,0)
(0,0,0,0,1,0,1,1,0,1,0,1,0,0,0)
(0,0,0,1,1,0,1,1,0,1,0,1,0,0,0).
```

The symbolic certificates in `kernel14-three-equality-rows-all-length.md`
cover those twelve targets and every other coordinate frontier for the same
three rows. Their Gram determinants are `1/2,0,1/2`; every two-by-two principal
minor is `3/4`. Each mixed doubled bundle has exact cost `1/3+2/3=1`, every
singleton has cost zero, and each canonical total is exactly three.

Kernel 17 has 512 labeled physical parity rows and 74 genuine automorphism
orbits. The seven exact planar templates in
`kernel17-all-odd-switching-cover.md`, with all 32 branch sign switches per
template, cover all 512 rows. In particular they cover every labeled member of
the residual sieve orbit at its canonical vector and at all nine coordinate
frontiers. Their disjoint first-cover gains are

`284,123,56,24,13,8,4`,

so the final kernel-17 residual is zero.

## All-length and attachment closure

For a path of length `l` and fixed branch-endpoint correlation `r`, exact path
elimination gives

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.

For fixed parity, `f_l(r)` is nonincreasing under `l -> l+2`. Given any
same-parity descendant of a canonical physical row, use the canonical
certificate if no coordinate changed. Otherwise choose any changed physical
coordinate and use its stored `+2` frontier certificate; every other change is
a further even increment and cannot increase the eliminated cost. This covers
simultaneous increments, arbitrary lengths, and every member of all 17
residual orbits. The three kernel-14 symbolic certificates and all seven
kernel-17 templates themselves already apply at every fixed-parity length.

If the core has `L` edges, tetracyclicity gives `|V|=L-3`. An excess bound at
most three gives `kappa(H)<=L+3`, hence

`s^+(H) >= 2L-(L+3)=L-3=|V(H)|`.

Rooted-tree DNN constants add under one-vertex sums, and a tree contributes
exactly its number of edges. Attaching arbitrary rooted trees therefore
preserves the same nonstrict conclusion.

## Fail-closed acceptance

Run

```text
python research/rank-four-cubic-kernels-final-verifier.py
python -O research/rank-four-cubic-kernels-final-verifier.py
```

The final verifier invokes and requires acceptance from all three dependency
verifiers: the 359-row sieve, the 148-certificate residual fixture, and the
kernel-17 seven-template audit. It then directly checks the three kernel-14
matrices, all principal minors and determinants, exact singleton and bundle
costs, the twelve missing keys, and the full 30-target kernel-14 symbolic
frontier. It also reconstructs the complete labeled kernel-17 residual orbit,
checks its canonical and all coordinate frontiers, and reevaluates the seven
templates on all 512 physical rows.

Acceptance uses explicit exceptions, rejects hostile mutations, and requires
byte-identical normal and optimized output. Missing dependencies, missing
fixtures, altered ledgers, and incomplete coverage fail closed.

Residual: none for cubic kernels 13--15 and 17.
