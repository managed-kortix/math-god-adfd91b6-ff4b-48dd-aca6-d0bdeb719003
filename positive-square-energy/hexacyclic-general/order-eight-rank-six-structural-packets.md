# Order-eight rank-six structural packets

## Scope

This is an exact structural reduction, not the complete order-eight kernel
theorem. It isolates finite symbolic equality families and the complete
edge-opening interface that can be used beside a DNN frontier computation.
The source is the frozen rank-six kernel fixture.

An order-eight rank-six kernel has thirteen edges and

`sum_v (deg(v)-3)=2`.

Hence its degree multiset is either `5,3,3,3,3,3,3,3` or
`4,4,3,3,3,3,3,3`. The exact split is `55+270=325`. There are 33 simple
kernels, split as `6+27`; all other 292 kernels force at least one physical
subdivision in every simple realization.

## Signed five-cycle equality packet

Exactly two order-eight kernels contract along their three singleton edges to
a five-cycle whose five quotient edges are doubled:

```text
K744: singles 05,14,23; doubles 07,16,27,36,45
K756: singles 05,14,23; doubles 07,16,25,34,67.
```

Give every doubled bundle one odd and one even path. Assign arbitrary parities
to the three singleton paths and contract each singleton with its corresponding
sign. On the five quotient classes put diagonal one and signed cycle-edge
correlation `-1/2`. Equivalently, the quotient Gram is

`Q=I-(1/2)S`,

where `S` is the signed adjacency matrix of a five-cycle. Switching leaves a
balanced or unbalanced cycle. Since every eigenvalue of `S` lies in `[-2,2]`,
`Q` is positive semidefinite.

Every singleton has transformed correlation one and costs zero. Each mixed
doubled bundle costs

`(1/3)+(2/3)=1`,

so the exact total DNN excess is five. Repeating the first alternating unit
vector twice gives a zero-cost `+2` extension on any coordinate. Thus each
template covers all same-parity lengthenings, not only a numerical frontier.

There are eight labeled singleton-parity rows on each kernel. The exact
automorphism group has order two and gives six physical-row orbits per kernel.
Consequently K744 and K756 contribute 12 finite equality-row templates, or
`12*14=168` canonical-plus-coordinate template keys before any coarse-DNN
overlap is removed. The structural verifier derives the two candidates from
the fixture; they are not entered as an assumed candidate list.

## Complete deletion-packet ledger

For every supported branch pair `e`, delete one copy of `e` and retain the two
endpoints as the marked attachment roots. This is the finite combinatorial
interface needed when an internal vertex of the physical path `P_e` is opened.
There are 3,594 kernel/support pairs, representing 4,225 physical edge copies.
Every deletion is connected, has rank five, and has one of exactly 19 block
profiles. A profile row is `(rank, vertices, edges)`; bridge blocks are retained
as rank-zero rows.

| support packets | block profile |
|---:|:---|
| 2696 | `(5,8,12)` |
| 312 | `(4,6,9)+(1,2,2)+(0,2,1)` |
| 218 | `(4,7,10)+(1,2,2)` |
| 66 | `(3,5,7)+2(1,2,2)+(0,2,1)` |
| 44 | `(3,4,6)+(2,4,5)+(0,2,1)` |
| 42 | `(3,5,7)+(2,4,5)` |
| 42 | `(3,5,7)+(2,3,4)+(0,2,1)` |
| 33 | `(3,4,6)+2(1,2,2)+2(0,2,1)` |
| 24 | `(2,4,5)+(2,3,4)+(1,2,2)+(0,2,1)` |
| 20 | `(3,6,8)+(2,3,4)` |
| 19 | `(3,6,8)+2(1,2,2)` |
| 18 | `(3,6,8)+(2,2,3)+(0,2,1)` |
| 16 | `(2,4,5)+3(1,2,2)+(0,2,1)` |
| 12 | `(2,3,4)+3(1,2,2)+2(0,2,1)` |
| 9 | `2(2,3,4)+(1,2,2)+2(0,2,1)` |
| 7 | `2(2,4,5)+(1,2,2)` |
| 6 | `5(1,2,2)+2(0,2,1)` |
| 6 | `(2,4,5)+(2,2,3)+(1,2,2)+2(0,2,1)` |
| 4 | `(2,2,3)+3(1,2,2)+3(0,2,1)` |

The first row is especially useful: 2,696 of the 3,594 supported openings
remain a single 2-connected rank-five block. Multiplicity weighting gives
3,327 of the 4,225 physical edge copies in this row.

## Simple excess-two kernels

The simple family has 429 supported edges. Exactly 420 deletions remain
2-connected. Only nine marked edges split into more than one cyclic block:

```text
K776: 46
K786: 05,06
K866: 56
K869: 15
K903: 07,36
K961: 27,36
```

Seven have profile `(3,5,7)+(2,4,5)`. The two K961 edges have profile
`(3,4,6)+(2,4,5)+(0,2,1)`. Therefore a deletion strategy for the simple
order-eight bases needs only a single-block marked rank-five packet plus these
nine explicitly named two-block interfaces. This is a structural reduction,
not yet a unit-credit theorem: an opening still needs `sigma>=1`, or a DNN
bound with one unit of slack, to pay the deleted nonempty tree.

The exact status of that proposed packet is recorded in
`marked-rank-five-one-credit-frontier.md`. The complete pentacyclic theorem
supplies only `sigma>=0`; its exact-budget and structural certificate rows do
not promote to one unit. In particular K756 can delete to the K118 signed-cycle
family, so those equality-ledger interfaces are genuinely present here.

## Exact audit

Run:

```sh
python3 research/rank-six-order-eight-structural-verifier.py
python3 -O research/rank-six-order-eight-structural-verifier.py
```

The verifier digest-locks the canonical kernel fixture; checks the order and
degree partitions; derives K744 and K756 from the singleton/double quotient
criterion; checks all 255 principal minors of every rational signed-cycle Gram;
checks exact costs, parity orbits, and free `+2` extensions; and independently
builds every deletion block profile with a multigraph-safe edge-stack
decomposition. It reports `scope=STRUCTURAL_REDUCTION_ONLY` to prevent this
packet ledger from being mistaken for the still-open complete order-eight
theorem.
