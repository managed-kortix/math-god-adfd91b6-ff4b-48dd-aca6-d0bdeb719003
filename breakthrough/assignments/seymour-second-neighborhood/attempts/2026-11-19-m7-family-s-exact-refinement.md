# Exact first refinement of the shared-low family `S` at order 18, `m=7`

## Scope

Assume the order-18, seven-hole normal form and family `S`: one degree-eight
vertex `w` is a robust deletion witness for both degree-nine vertices `r,q`.
Write

```
A=N+(w), B=N++(w), C=V(D)\({w} union A union B), T={w} union A union B.
```

Then `|A|=8`, `|B|=7`, `|C|=2`, and `r,q in A`. This note refines the 210
corrected scalar `epsilon=0` rows to exact labelled hole/orientation states on
all pairs incident with `C`. It intentionally stops before orienting all pairs
inside `T`. It is a necessary projection, not an elimination of family `S` or
of `m=7`.

The choice of `S` rather than the mixed family `H` is forced by row economy at
this stage. `S` has one low-root system and no second root partition. `H`
additionally requires a synchronized degree-nine root with nine first and eight
exact-second neighbors. A full exact completion model may reverse this
comparison, but the first synchronized hole/orientation projection is strictly
smaller for `S`.

## Exact C-incident encoding

Label `C={c0,c1}`. For `i=0,1`, let

```
a_i = number of holes c_i--({w} union A),
r_i = e(c_i,B),
b_i = number of holes c_i--B,
m   = 1[c0c1 is a hole],
d_i = 1[c_i->c_(1-i)],
h   = number of holes internal to T.
```

Since neither high is in `C`, both C vertices have outdegree eight. Every
present pair from `c_i` to `{w} union A` points out of `c_i`, so

```
r_i=a_i-1-d_i,                                      (1)
d_0+d_1=1-m,                                        (2)
a_0+a_1+b_0+b_1+m+h=7.                              (3)
```

For a fixed scalar row, the exact labelled choices are independent:

```
choose the a_i holes among the 9 labels {w} union A;
choose the r_i C-to-B arcs among the 7 B labels;
choose the b_i C--B holes among the remaining 7-r_i labels;
all other C--B pairs point B-to-C.                  (4)
```

Thus its labelled multiplicity is

```
C(9,a_0) C(9,a_1)
C(7,r_0) C(7-r_0,b_0)
C(7,r_1) C(7-r_1,b_1).                              (5)
```

Summing (5) over the 210 scalar margins gives

```
138,188,079 labelled exact C-incident states.         (6)
```

The involution exchanging `c0,c1` has 3,789 fixed states. Burnside therefore
gives

```
69,095,934 C-swap orbits.                             (7)
```

This enormous increase from 108 scalar row orbits is a useful negative result:
**expanding individual C labels before synchronizing the residual T constraints
is the wrong finite-search representation.** The scalar ledger is the correct
outer shard; exact masks should remain existential inside a solver or be grouped
by the stabilizer of the distinguished root/high labels.

There is a much smaller exact pair-type representation.  Fix `w,r,q`, quotient
the other six A labels by `S_6`, quotient B by `S_7`, and then swap the two C
labels.  Record the C-hole type of each of `w,r,q`, multiplicities of the four
C-hole types among the six ordinary A labels, and multiplicities of the nine
ordered C-pair types among B (`C->B`, `B->C`, or hole independently for each C
endpoint).  Exact enumeration gives

```
26,060 type rows before the C swap,
174 rows fixed by the C swap,
13,117 exact C-incident type orbits.                 (7a)
```

Their residual-T-hole distribution is

```
h=0: 8,764; h=1: 3,093; h=2: 999; h=3: 218; h=4: 43. (7b)
```

Unlike the 69 million fully labelled orbits, these 13,117 rows are a practical
exact outer cover for C incidence.  Each row leaves all T orientations and
exactly `h` T-holes existential.  Production and independent multiset/Burnside
checkers agree on (7a)--(7b).

The orbit count by the number `h` of T-holes is

```
h=0: 61,327,035
h=1:  7,214,130
h=2:    532,665
h=3:     21,735
h=4:        369.                                      (8)
```

In particular `h<=4`. This is only the already sound identity
`b_0+b_1+h=4-rho` with `rho=r_0+r_1`; it is not new pruning.

Aggregating only by `(rho,h)` gives the following exact C-orbit counts and
numbers of labelled scalar margins:

```
 rho h    C-orbits   scalar margins
  0  0      364,959       15
  0  1      132,678       12
  0  2       33,201        9
  0  3        5,103        6
  0  4          369        3
  1  0    4,756,752       24
  1  1    1,297,296       18
  1  2      216,216       12
  1  3       16,632        6
  2  0   18,686,808       27
  2  1    3,397,464       18
  2  2      283,248        9
  3  0   26,253,612       24
  3  1    2,386,692       12
  4  0   11,264,904       15.                       (9)
```

The independent checker reconstructs (6)--(8) by generating functions rather
than importing the production formulas.

## Simultaneous robustness: exact statement and limit

For `b in B`, put `P_b={a in A:a->b}`. Root exactness says `P_b` is nonempty.
Robustness after deleting each high says exactly

```
P_b != {r},  P_b != {q}.                             (10)
```

A singleton `P_b={a}` with `a in A\{r,q}` is legal. Therefore no sound
projection may replace (10) by `|P_b|>=2`. The already committed shared-low
local model exhibits singleton support outside the two highs.

Equation (10) affects only the internal T orientation and is invisible to the
C-incidence count (6). The next useful shard should therefore keep each of the
108 scalar C-row orbits and synchronize the following T data without expanding
C masks:

```
- h(T)=h;
- exact A--B column types subject to (10);
- A-row residual outdegree after A--A and A--B choices;
- B-row residual outdegree after B--T and B--C choices;
- the two distinguished high rows r,q;
- exact badness and arc-minimal gain/loss clauses.               (11)
```

## Hostile countermodels before pruning

`experiments/m7_family_s_countermodels.py` directly verifies two opposite
local extremes under exact-distance-two semantics:

```
(rho,h,C-hole)=(4,0,1),
(rho,h,C-hole)=(0,4,0).                              (12)
```

A third fixed graph realizes a B column with the singleton predecessor set
`P_9={3}`, where `3` is an ordinary member of `A\{r,q}`.  Every graph has
exactly seven holes, highs `1,2`, root `N+(0)={1,...,8}`,
`N++(0)={9,...,15}`, and the same exact second neighborhood after deleting
either high. None is claimed globally bad or arc-minimal.

Consequences of (12): none of the following is derivable from degree census,
seven-hole budget, root exactness, and shared-low robustness alone:

```
rho<=3; h<=3; the C-pair is forced present; the C-pair is forced missing;
every family-S leaf has a T-hole; every family-S leaf has no T-hole;
every B column has at least two A predecessors.                            (13)
```

Any future pruning of those cells must explicitly use global badness,
arc-minimality, or another additional hypothesis and must survive these
countermodels.

As a broader hostile scout, `m7_family_s_local_extend.py` tested every one of
the 26,060 pre-C-swap type rows.  All 26,060 extend to an oriented graph with
the exact degree sequence, seven holes, fixed root row, and simultaneous
shared-low B-column robustness.  This is an uncertified Z3 observation (no
global badness or arc minimality), not a proof that every row is nonempty.
Its legitimate conclusion is strategic: the local package alone showed no
additional pruning at all, so the next model must add a genuinely global
condition rather than more local wishful counting.

## Reproducibility

Run

```
python3 experiments/m7_family_s_exact_rows.py
python3 experiments/m7_family_s_exact_rows_check.py
python3 experiments/m7_family_s_type_rows.py
python3 experiments/m7_family_s_type_rows_check.py
python3 experiments/m7_family_s_countermodels.py
# Optional observation; requires z3-solver:
python3 experiments/m7_family_s_local_extend.py
```

The first two scripts independently evaluate the fully labelled row sum and
Burnside fixed set.  The next two independently enumerate the 13,117 exact type
orbits.  The countermodel script checks three fixed hostile graphs directly.
The optional final scout reports solver observations only.  No UNSAT claim or
proof certificate is made.
