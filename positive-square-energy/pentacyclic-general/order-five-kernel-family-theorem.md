# Complete order-five rank-five kernel-family theorem

## Theorem and exact scope

Let `K` be any of the 24 order-five kernels in the exact rank-five suppressed
kernel classification, let `B` be a simple subdivision of `K`, and attach
arbitrary rooted trees to obtain `G`. Then `s^+(G)>=|V(G)|`. More precisely,
one of two proof conclusions applies:

1. a DNN certificate gives `kappa(B) <= |E(B)|+4`; or
2. an induced-territory structural packet proves `s^+(G)>=|V(G)|` directly.

The second alternative is essential. In particular, no universal DNN
excess-four assertion is made for the all-odd `K5-e` family: its unsubdivided
member has optimized excess `2sqrt(7)-1>4`.

The formerly excluded all-odd `K5-e` family, kernel 32 with physical row
`(0,1,1,1,1,1,1,1,1,1)`, is closed by the exact disjunctive 19,683-state
theorem described below.

## Exhaustive composition

The digest-locked rank-five fixture contains exactly 24 kernels of order five.
The regular-tetrahedron census reconstructs 6282 labeled physical rows and
4238 genuine automorphism orbits. It certifies 4030 orbits and leaves 208.
After separating the all-odd `K5-e` orbit, 207 residual parity rows remain for
the original all-length frontier.

Every order-five rank-five kernel has nine suppressed paths. For each residual
row, the all-length cover consists of its canonical shortest vector and all
nine one-path length-plus-two vectors. Fixed-parity path monotonicity then
closes every longer length vector. The exact frontier therefore has

`207 * (1+9) = 2070`

targets. Its disjoint certificate partition is:

| method | exact targets |
|:---|---:|
| strict rational Gram path-vector witnesses | 2062 |
| kernel 35 symbolic equality templates | 4 |
| kernel 22 structural attached-`K4` closures | 4 |
| total | 2070 |

The separated all-odd `K5-e` family has its own exact unit/residue sieve:

`19683 = 18848 simplex + 53 actual-K4 + 640 theta + 142 residual`.

The full automorphism group is the genuine `S_3 x S_2` action: degree forces
preservation of the two branch-vertex parts, and all twelve such permutations
are automorphisms. The 142 residual states form 16 orbits under this full
group. Each orbit has a strict exact rational path-vector witness at its
shortest path vector, and fixed-parity monotonicity covers all longer paths of
the same residue. The all-unit state is closed structurally by retaining an
actual attached `K4`; no arbitrary all-odd `K4` subdivision is assigned extra
credit. The complete statement, hand-checkable parameter/cost tables, and
independent verifier are in
`positive-square-energy/pentacyclic-general/all-odd-k5e-induced-territory-frontier.md`.

The rational records and the paper table store every branch and internal path
vector by rational stereographic parameters. The verifier rebuilds all unit
vectors with `Fraction`, reconstructs every transformed odd/even path,
recomputes every step cost `(1-r)/(1+r)`, requires the exact total to equal the
stored reduced fraction and be strictly less than four, and locks both paper
tables to the fixture.

## Kernel 35 equality templates

The four equality targets are two residual rows, each at its canonical vector
and at the frontier obtained by lengthening path zero. In kernel 35 the
lengthened `01` path has zero cost because vertices 0 and 1 are respectively
coincident or antipodal as dictated by its parity. The four active doubled
bundles `04,13,23,24` have endpoint correlation `-1/2`. Each contributes

`1/3 + 2*(1/3) = 1`,

so the exact total is four independently of whether the zero-cost `01` path
has length `1/3` or `2/4`. The fixture freezes both 5-by-5 rational Gram
templates. The verifier checks symmetry, unit diagonal, every principal minor,
the required correlations, target identities, and the formal cost identity.

## Kernel 22 structural closures

In the pair order

`01,02,03,04,12,13,14,23,24,34`,

kernel 22 has multiplicities `(0,0,1,2,1,1,1,1,1,1)`.  Denote its physical
paths by `P03`, `P04^0`, `P04^1`, and `Pij` for the six pairs
`ij in {12,13,14,23,24,34}`.  The four non-Gram targets are the two parity
choices `|P03|=2` and `|P03|=1`, each at the canonical vector and at path-zero
frontier `|P03|+2`.  In all four targets the two `04` paths have lengths one
and two, while every `Pij` is the edge `ij`.

Here is the required attachment-uniform territory construction.  Let `C` be
the union of the three paths `P03,P04^0,P04^1`.  Delete branch vertex `0`, all
internal vertices of these three paths, and every rooted tree owned at any of
those deleted branch/internal vertices.  Call the resulting induced territory
`A`.  Put every other vertex, including every rooted tree owned at
`1,2,3,4`, in `H`.

The physical paths are internally disjoint.  After their endpoints `3,4` are
left in `H`, their portions in `A` are three paths meeting only at `0` (a
length-one `04` path contributes no internal vertex).  Thus `A` is nonempty,
connected, acyclic, and induced; adjoining a rooted tree at its unique owner
preserves all four properties.  Its credit is `sigma(A)=-1`.  The complement
`H` is also induced and connected.  Its core is exactly the six physical edges
`12,13,14,23,24,34`, so `H` is an actual `K4` with arbitrary rooted trees
attached at its four vertices.  The attached-`K4` theorem gives
`sigma(H)>2`.  Induced superadditivity now gives

`sigma(G) >= sigma(A)+sigma(H) > -1+2 = 1`,

and hence the required spectral conclusion, strictly.  This is the structural
alternative of the theorem; it makes no inference about `kappa`.

This proves exactly the four listed keys.  It also composes correctly with the
finite frontier.  For a fixed-parity descendant, if only `P03` is made longer,
the corresponding `P03+2` structural target and fixed-parity path monotonicity
apply.  If any of the other eight paths is made longer, use that path's strict
rational one-coordinate frontier (one of the 2062 records) and monotonicity.
The canonical structural target handles the zero-increment case.  Thus every
monotone descendant is covered without pretending that a lengthened `Pij`
still belongs to the actual `K4` in the structural partition.

## Fail-closed audit

The deterministic theorem fixture is
`pentacyclic/research/order5-kernel-family-theorem.json`, with SHA-256

`4d8b826b397dc269c7853b8bd386d00bf469282b52720b8dac96d850e9e616d8`.

It is regenerated from the source-locked fresh search output, not copied into
the verifier as an unchecked result table. Run both modes:

```text
python3 pentacyclic/research/order5-kernel-family-theorem-verifier.py
python3 -O pentacyclic/research/order5-kernel-family-theorem-verifier.py
```

The standalone verifier for the 207-row branch locks the kernel fixture, tetra
census, exact search results, and theorem fixture; requires exact source keys
and all 2070 frontier
keys; checks all path vectors and costs; audits the symbolic and structural
templates; reconstructs each K22 physical subdivision and verifies its induced
tree/actual-K4 partition and exhaustive rooted-tree ownership; and rejects
hostile changes to keys, counts, source locks, costs, lengths, Gram entries,
and structural opening data through explicit exceptions.
The all-odd `K5-e` verifier separately locks its sieve and deterministic fixture,
checks all 16 rational witnesses and 142 exact transports, and rejects its
hostile mutations in normal and optimized modes.
