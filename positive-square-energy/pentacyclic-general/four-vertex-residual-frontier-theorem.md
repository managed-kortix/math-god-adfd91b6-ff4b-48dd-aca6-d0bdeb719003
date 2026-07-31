# Rank-five four-vertex residual frontier theorem

## Theorem

For each of the 13 residual physical orbits left by the exact tetrahedral
sieve, let `L` be its first-simple canonical eight-path length vector. Every
simple subdivision represented by that orbit has DNN excess at most four.
More precisely, for each residual orbit select the finite frontier covering set

`{L} union {L+2e_i : 0<=i<8}`.

Every selected target is certified. Of the resulting 117 targets, 116 have strict
exact rational Gram path-vector certificates. The canonical kernel-9 target
has an exact symbolic positive-semidefinite equality certificate of cost four.
Fixed-parity path monotonicity then covers every coordinatewise larger length
vector, so the 13 residual orbits are closed.

Together with the tetrahedral sieve this proves the DNN excess-four bound for
all physical parity rows of all 13 rank-five four-vertex kernels.

## Exhaustive source and frontier covering set

Edge order is `01,02,03,12,13,23`. A physical row records the number of odd
paths in each bundle. The source verifier independently reconstructs all 1281
physical rows, quotients by genuine kernel automorphisms into 821 orbits, and
recomputes the exact sieve partition

`821 = 808 certified + 13 residual`.

Each four-vertex rank-five kernel has eight physical paths. The canonical
first-simple realization assigns odd lengths `1,3,...` within each bundle and
length two to every even path. The selected covering set for each residual
orbit consists explicitly of the canonical vector and each of its eight
one-coordinate-plus-two vectors:

`13*(1+8)=117`.

This is a sufficient fixed-parity frontier covering set: `L` is coordinatewise
below every `L+2e_i`. The selection includes `L` to certify
the canonical realization and includes every `L+2e_i` to start monotone
coverage after any first coordinate increase. Increasing that path length
again by two cannot increase its eliminated path cost, while the other paths
and their common branch Gram vectors are unchanged.

## Exact rational certificates

Every strict record stores four rational stereographic parameter triples and
all rational internal path-vector parameters. A parameter row `t` represents
the unit vector

`u(t)=((1-|t|^2)/(1+|t|^2), 2t/(1+|t|^2))`.

For consecutive transformed path vectors `x,y`, the exact excess contribution
is

`(1-<x,y>)/(1+<x,y>)`.

The verifier rebuilds every vector and every path from `fractions.Fraction`,
rejects antipodal steps and malformed path widths, recomputes the stored cost,
and checks it is strictly below four. It also reconstructs each branch Gram
matrix and checks all principal minors exactly. No floating-point value enters
acceptance.

## Kernel-9 equality

The sole non-strict target is the canonical kernel-9 row

`(0,1,1,1,1,0)`

with path lengths `(1,2,1,2,1,2,1,2)`. Its four branch vectors occur in two
coincident pairs. The exact Gram matrix is

```text
1    1   -1/2 -1/2
1    1   -1/2 -1/2
-1/2 -1/2  1    1
-1/2 -1/2  1    1
```

It is positive semidefinite: its nonzero two-by-two quotient is the Gram
matrix of two unit vectors with correlation `-1/2`; equivalently every
principal minor is nonnegative. The endpoint angle is `2*pi/3`. Each odd
direct path costs `(1-1/2)/(1+1/2)=1/3`; equal spacing on each even two-edge
path gives two transformed steps of angle `pi/3`, hence cost `2/3`. Thus

`4*(1/3+2/3)=4`.

The verifier freezes the matrix, checks every principal minor with exact
rational arithmetic, and checks the symbolic path-cost identity separately.

## Fail-closed artifacts

The frozen fixture is

`research/fixtures/rank-five-four-vertex-residual-frontiers.json`

with SHA-256

`09a7b38b1e9f5e18aaddc1f9e0114b8490151f2062d3f51100c52eb314eb56d2`.

Run:

```text
python3 research/rank-five-four-vertex-residual-frontier-verifier.py
python3 -O research/rank-five-four-vertex-residual-frontier-verifier.py
```

The verifier digest-locks and audits the source sieve, checks exact coverage of
all 117 frontier keys, verifies all Fraction costs and PSD conditions, rejects
ten hostile mutations, and requires byte-identical normal and optimized-mode
output.
