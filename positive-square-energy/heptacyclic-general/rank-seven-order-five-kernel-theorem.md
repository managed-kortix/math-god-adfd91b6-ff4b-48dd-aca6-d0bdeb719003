# Rank-seven kernels of order five

## Theorem and exact scope

Let `K` be any of the 233 loopless 2-connected minimum-degree-three
rank-seven kernels on five branch vertices. Let `B` be any simple subdivision
of `K`, and attach arbitrary finite rooted trees at branch or subdivision
vertices. Then the resulting graph `G` satisfies

`s+(G) >= |V(G)|`.

This is an order-five single-block theorem only. It makes no claim about
rank-seven kernel orders six through twelve, graphs with multiple positive-rank
blocks, all connected heptacyclic graphs, or any higher-order frontier.

## Exact residual census

The verifier reads the proved-complete rank-seven kernel fixture, selects the
233 order-five kernels, and independently regenerates every physical parity
row and every automorphism orbit. The exact totals are 132,774 physical rows
and 109,342 orbits. The regular-tetrahedron coarse Gram sieve certifies 109,327
orbits and leaves exactly these 15 coarse residual orbits:

```text
K75:  (1,1,1,1,1)                         orbit size 1
K102: (1,1,1,1,1)                         orbit size 1
K121: (1,1,1,1,1)                         orbit size 1
K148: (1,1,1,1,1)                         orbit size 1
K153: (1,1,1,1,1)                         orbit size 1
K199: (1,1,1,1,1)                         orbit size 1
K201: (1,1,1,1,1)                         orbit size 1
K206: (1,1,1,1,1)                         orbit size 1
K217: (1,1,1,1,1)                         orbit size 1
K227: (1,1,1,1,1)                         orbit size 1
K249: (1,1,1,1,1)                         orbit size 1
K269: (1,1,1,1,1,1,1,1,1,1)             orbit size 1
K269: (1,1,1,1,1,1,1,1,1,2)             orbit size 1
K272: (1,1,1,1,1)                         orbit size 1
K286: (1,1,1,1,1)                         orbit size 1
```

Here a coordinate gives the number of odd paths in the corresponding nonzero
parallel class. The kernel number is the one-based index in the complete
rank-seven fixture. The verifier computes, rather than trusts, this list and
the displayed orbit sizes.

For completeness, the coarse sieve colors the five branch vertices by at most
four regular-tetrahedron vectors. A class with odd paths must have differently
colored endpoints. After multiplying excess by 30, a differently colored class
of multiplicity `m` with `o>0` odd paths costs at most

`15 + 5(o-1) + 18(m-o) = 18m+10-13o`,

using the exact atoms `1/2`, `1/6`, and `3/5`. If `o=0`, differently colored
endpoints cost at most `18m`; equal endpoints cost zero. The verifier tries all
set-partition colorings and accepts exactly costs at most `180`. The atom
inequalities and their positive-semidefinite midpoint Grams are the exact
rank-seven tetrahedral atoms proved in the orders-two-through-four theorem.
The chosen branch coloring is retained under all same-parity lengthening.

## Canonical-plus-eleven frontier

Every order-five rank-seven kernel has eleven physical paths. For a parallel
class of multiplicity `m` containing `o` odd paths, use canonical simple
lengths

```text
o=0: (2,...,2),
o>0: (1,3,...,3,2,...,2).
```

For each residual orbit the finite frontier consists of this canonical vector
and each of its eleven one-coordinate length-plus-two vectors. Thus the target
set has exactly `15*12=180` keys. The exact disjoint ownership ledger is

```text
176 exact rational Gram-chain certificates of excess at most 6,
  4 structural K269 certificates,
180 total.
```

Every rational witness gives five rational stereographic branch parameters and
all rational internal parameters. Rational stereographic projection constructs
unit vectors exactly. The verifier checks every transformed path chain with
`Fraction`, recomputes

`sum (1-r)/(1+r) <= 6`,

and checks equality with the stored exact cost. Consequently these records are
exact symbolic Gram certificates, not floating-point evidence. The numerical
fields in the search fixture are ignored by the proof verifier.

## The four structural targets

K269 is `K5` with one doubled edge. In each of its two residual parity rows,
the only rationally unresolved targets are the canonical target and the target
that lengthens the nonunit member of the doubled pair. In all four cases one
member of that pair remains a unit edge and the other is a path of length at
least two.

Put every internal vertex of the latter path, together with every rooted tree
whose root lies there, in one induced nonempty tree. Its induced complement is
an actual `K5` with arbitrary rooted trees at its five vertices. The proved
attached-`K5` packet has surplus strictly greater than one: remove one core
vertex and its rooted tree, leaving an attached `K4` packet of surplus strictly
greater than two, while the removed tree has surplus minus one. The deleted
nonempty tree has surplus minus one, so induced superadditivity gives strictly
positive total surplus. This proves `s+(G)>|V(G)|` for these four targets.

The argument assigns every attached tree to exactly one induced piece and works
unchanged when the selected nonunit path is further lengthened.

## Arbitrary subdivisions and rooted trees

Every simple realization in a fixed physical parity orbit is, after permuting
paths within parallel classes, a coordinatewise same-parity descendant of its
canonical vector. If it is canonical, use that target. Otherwise choose any
coordinate that is longer by at least two and use the corresponding frontier
target. Retain its branch Gram and replace every path by its optimal equal-angle
chain. The exact path formula

`f_q(r)=q tan^2(acos((-1)^q r)/(2q))`

is nonincreasing under `q -> q+2`, so simultaneous further lengthening cannot
increase the excess. The four structural targets use the preceding induced
decomposition instead. This exhausts all simple subdivisions; no
parity-changing or spectral subdivision monotonicity is asserted.

For a DNN-owned core with `L` edges, rank seven gives `|V(B)|=L-6` and the
certificate gives `kappa(B)<=L+6`. If attached rooted trees contain `t` edges,
one-vertex additivity and `kappa(T)=|E(T)|` give

`kappa(G)<=L+6+t`.

Since `s-(G)<=kappa(G)` and `s+(G)+s-(G)=2(L+t)`, it follows that

`s+(G)>=L-6+t=|V(G)|`.

## Fail-closed audit

Run

```text
python3 research/rank-seven-order-five-kernel-theorem-verifier.py
python3 -O research/rank-seven-order-five-kernel-theorem-verifier.py
```

The verifier digest-locks the complete kernel source, the 180-target rational
fixture, and this proof note. It regenerates the exact orbit census and residual
set, reconstructs the complete Cartesian frontier, verifies all rational chains
and four structural keys, pins the narrow theorem scope, rejects hostile data,
digest, numeric-type, nonfinite, ownership, and overclaim mutations, and requires normal
and optimized executions to emit byte-identical output.
