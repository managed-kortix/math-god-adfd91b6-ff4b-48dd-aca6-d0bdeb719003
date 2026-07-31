# Cubic kernels 13--15: rational residual frontiers

## Scope

This artifact attacks the 16 kernel-13--15 residual orbits from the exact
physical three-color sieve. Kernel 17 remains separate and is already covered
by its seven-template switching packet. The source split is

`K13=5, K14=6, K15=5`.

For each orbit, the target consists of its canonical first-simple path-length
vector and all nine vectors obtained by increasing one physical path length by
two. Thus the full target has

`16 canonical + 144 one-coordinate-plus-two = 160` frontiers.

## Deterministic path-vector search

The generator uses seeded four-dimensional branch-vector search, equal-angle
path interpolation, rational stereographic rounding, and denominators
`32,64,128,256`. Every accepted witness is then rebuilt independently from
`fractions.Fraction`; floating-point values never enter the acceptance test.

The frozen result is

`148 strict rational certificates + 12 unresolved equality candidates`.

All 148 accepted costs are strictly below three. There are no accepted
equalities. The unresolved targets are exactly three kernel-14 residual rows,
each at the canonical vector and physical coordinates `0,3,8` increased by two:

```text
(0,0,0,0,1,0,0,1,0,1,0,1,0,0,0)
(0,0,0,0,1,0,1,1,0,1,0,1,0,0,0)
(0,0,0,1,1,0,1,1,0,1,0,1,0,0,0)
```

The numerical reduced costs approach three from above for these 12 targets;
the fixture labels them equality candidates, not certificates. Every target
for kernels 13 and 15 has a strict rational witness. The other three kernel-14
residual rows also have all ten strict frontier witnesses.

## Exact audit

Run

```text
python research/rank-four-cubic-kernels-residual-frontier-verifier.py
python -O research/rank-four-cubic-kernels-residual-frontier-verifier.py
```

The verifier checks the source residual fixture, target ordering, canonical and
one-coordinate-plus-two length vectors, search metadata, rational unit vectors,
internal path widths, exact costs, strict inequalities, unresolved pattern,
normal/optimized output identity, hostile mutations, and canonical digest.

The fixture is

`research/fixtures/rank-four-cubic-kernels-residual-frontiers.json`

with SHA-256 digest

`8b14bcc20767f2dfdb58577a001b6bc9300295e880c4c84fadc52a60458bc00c`.
