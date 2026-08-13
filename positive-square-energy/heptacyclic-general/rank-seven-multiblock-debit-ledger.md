# Rank-seven multiblock debit ledger

## Scope

This is a fail-closed analysis note for the main lane. It makes no theorem
claim. It classifies the positive block-rank partitions of seven, records the
rows already discharged by existing connected rank-at-most-six results or by
block-additive DNN certificates, and isolates the packets that still need an
owner-exact argument.

Write

`sigma(H)=s^+(H)-|V(H)|`.

For a cyclic block `B` of rank `r`, let `E(B)` denote the excess of the actual
exact DNN certificate being used:

`kappa(B)<=|E(B)|+E(B)`.

Define its debit by

`d(B)=E(B)-(r-1)`.                                             (1)

If the positive-rank blocks have ranks `r_1,...,r_k`, their DNN certificates
glue at cut vertices and rooted trees add exactly their edge counts. Since
`sum r_i=7`, the global excess-six target is equivalent to

`sum_i d(B_i)<=k-1`.                                          (2)

Thus `k-1` is the exact multiblock debit allowance. This accounting is about
the displayed DNN records only. A structural rank-at-most-six owner is not to
be assigned a debit unless it separately supplies a DNN certificate.

## Immediate connected-theorem split

Let the cyclic hull be the minimal block-cut subtree containing all cyclic
blocks. If an actual bridge occurs in this hull, deleting that bridge partitions
the vertices into two connected induced graphs of positive ranks `a` and
`7-a`, where `1<=a<=6`. The complete connected theorems through rank six give
nonnegative credit on both sides. Hence every such incidence is already
closed. The bridge edge crosses the induced vertex partition and needs no
owner; every connector vertex, other connector edge, and rooted branch remains
with its unique side.

Consequently every packet retained below is restricted to a bridge-free cyclic
hull: cyclic blocks meet through shared cut vertices. This restriction is
essential. The unquantified conclusion `sigma>=0` on a rank-six side cannot pay
a cycle-minus-cut tree of credit `-1`.

## Exact debit inputs

The following are the strongest uniform inputs needed for the first sieve.
They are bounds for actual certificate classes, not substitutes for their
physical ledgers.

| rank/class | DNN excess `E` | debit `d=E-(r-1)` |
|---|---:|---:|
| cycle `Q` | `epsilon(Q)<=1` | `epsilon(Q)<=1` |
| theta | `Delta<=D=(sqrt(17)-1)/2` | `<=alpha=(sqrt(17)-3)/2` |
| rank-three direct | `<=2` | `<=0` |
| canonical `S3` | `<12/5` | `<2/5` |
| actual `K4` | `3` | `1` |
| rank-four direct | `<=3` | `<=0` |
| structural `S4`, even state | `<18/5` | `<3/5` |
| structural `S4`, odd state | `<19/6` | `<1/6` |
| rank-five direct | `<=4` | `<=0` |
| all-odd `K5-e` | `<=2sqrt(7)-1` | `<=2sqrt(7)-5` |
| rank-five `K22`, `K71` structural classes | no quoted DNN owner | `NDNN` |
| rank-six DNN-owned class | `<=5` | `<=0` |
| rank-six structural class | no automatic DNN owner | `NDNN` |

Here `epsilon(C3)=1`, `epsilon(C5)=5-2sqrt(5)`, and even cycles have zero
debit. The inequalities used repeatedly below include

`3alpha+1<3`,

`2/5+alpha+2<3`,

`2sqrt(7)-5+alpha<1`.                                        (3)

## The fifteen partitions

The positive block ranks form exactly the following integer partitions of
seven. In the table, `k-1` is the debit allowance from (2). A direct row means
that every constituent block has the stated DNN owner. `Residual predicate`
is exact: it is evaluated using the actual certified excesses, not merely the
uniform maxima in the preceding table.

| partition | `k-1` | immediate disposition | residual predicate or packet |
|---|---:|---|---|
| `1^7` | 6 | existing rank-uniform cactus result | none; the sharp-DNN residual is owned structurally by that result |
| `2+1^5` | 5 | DNN when `Delta+sum epsilon_i<=6` | `R21: Theta(1,2,r)+T^5`; and `D+T^4+P` |
| `2+2+1^3` | 4 | DNN when `Delta_1+Delta_2+sum epsilon_i<=6` | `R221: D+D+T^3` |
| `2+2+2+1` | 3 | all rows DNN, since `3alpha+1<3` | none |
| `3+1^4` | 4 | every rank-three direct row is DNN | `R31-S: S3+T^4`; `R31-K: K4+Q^4` when `sum epsilon_i>3` |
| `3+2+1+1` | 3 | direct and `S3` rows are DNN by (3) | `R321: K4+Theta(1,2,r)+T^2`; and `K4+D+T+P` |
| `3+2+2` | 2 | every non-`K4` rank-three row is DNN | `R322: K4+D+D` |
| `3+3+1` | 2 | all rows without a `K4`, and `K4` plus a direct rank-three row, are DNN | `R331-S: K4+S3+Q` when `d(S3)+epsilon(Q)>1`; `R331-K: K4+K4+Q` for odd `Q` |
| `4+1^3` | 3 | every rank-four direct row is DNN | `R41: S4+T^3`; and even-state `S4+T^2+P` when its actual debit sum exceeds three |
| `4+2+1` | 2 | every rank-four direct row is DNN | `R421: S4+Theta+Q` when `d(S4)+(Delta-1)+epsilon(Q)>2` |
| `4+3` | 1 | all rows except a structural `S4` paired with `K4` are DNN | `R43: S4+K4` physical rows with `d(S4)>0` |
| `5+1+1` | 2 | every rank-five direct row is DNN | `R511-K5e: all-odd K5-e+T^2`; all `K22/K71+Q_1+Q_2` structural rows |
| `5+2` | 1 | all DNN-owned rows, including all-odd `K5-e`, close by (3) | `R52-NDNN: K22+Theta` and `K71+Theta` structural rows |
| `6+1` | 1 | DNN rows by shared-Gram gluing; K223 by its marked-cycle packet; both K110 rows by the exact attached-`K4` shared-cut inequality | none |
| `7` | 0 | single-block lane, not multiblock | outside this ledger |

For the `S3` and `S4` rows, the named packet is retained only for physical
states whose actual displayed debit makes the corresponding strict inequality
fail. The coarse upper bounds prove that no additional cycle profile survives:
one nontriangle already supplies enough debit reduction in `R31-S`; in `R41`,
one pentagon can survive only in the even `S4` state, while every other
nontriangle profile is DNN-closed. Likewise, the exact theta-cycle
classifications used in the rank-six ledger
reduce `R21`, `R221`, `R321`, and `R322` to the displayed families. Equality in
every DNN predicate is closed and is not a packet residual.

## Owner-exact packet registry

After removing actual-bridge incidences and all rows satisfying (2), the
current multiblock obligation is the following disjoint registry.

| key | block partition | required owner action |
|---|---|---|
| `R21` | `2+1^5` | closed by the nested induced-piece theorem: theta-arm/six-triangle and `D+TT` typed anchors |
| `R221` | `2+2+1^3` | closed by the physical second-diamond nested induced-piece packet |
| `R31-S` | `3+1^4` | reduced to the canonical doubled-`C4` plus three-triangle packet; all 110 marked incidences close except two one-sided root-sensitive packets `C4` and `D3` |
| `R31-K` | `3+1^4` | closed by the actual-`K4+T` anchor and three nested first-boundary territories |
| `R321` | `3+2+1+1` | closed by the actual-`K4` terminal-triangle allocation, including nested theta incidence |
| `R322` | `3+2+2` | closed by the actual-`K4` two-boundary induced-piece packet |
| `R331` | `3+3+1` | closed: `R331-S` and `R331-K` by the actual-`K4` two-debit induced-piece theorem |
| `R41` | `4+1^3` | closed by the typed `S4` opening, retained rank-three-plus-triangle anchor, and three induced territories |
| `R421` | `4+2+1` | closed by the typed `S4` opening and nested theta/cycle first-boundary packet |
| `R43` | `4+3` | closed: exact `S4` opening plus the external actual `K4`; the retained-owner channel boundary-opens it to an actual `K3` |
| `R511-K5e` | `5+1+1` | closed after regenerating the 53 actual-`K4` and 640 favorable-theta structural states |
| `R511-K22` | `5+1+1` | retain the certified attached `K4` from `K22`; pay its original owner territory and two external cycle boundaries |
| `R511-K71` | `5+1+1` | closed on all nine targets by the actual `K4`, positive unicyclic owner, and two nested cycle boundaries |
| `R52-K22` | `5+2` | closed: retained actual `K4` pays the exact K22 owner tree and one theta first-boundary debit |
| `R52-K71` | `5+2` | closed: retained actual `K4`, favorable unicyclic side, and one theta first-boundary debit |
| `R61` | `6+1` | closed: K110 all-unit and one-long by the exact shared-cut packet for every cut orbit and length; canonical all-unit K223 by `r61-k223-marked-cycle-packet.md` |

This is a packet-template registry, not yet a complete physical owner ledger.
The five keys `R331-S`, `R331-K`, `R43`, `R52-K22`, and `R52-K71` are expanded
and closed in `two-debit-induced-piece-theorem.md`; its persisted exact ledger
regenerates the four K22 and nine K71 structural targets. The R61 theorem-owner
partition has been expanded to three typed physical families, and all three
shared-cut packets are closed.

The subsequent `nested-induced-piece-packet-theorem.md` expands all eleven
keys remaining after those closures into an owner-typed manifest. It proves the
maximal currently supported nine-key subset

`R21, R221, R31-K, R321, R322, R41, R421, R511-K5e, R511-K71`

and returns exactly `R31-S` and `R511-K22`. The returned doubled-`C4` subclass
has a pinned retained threshold `>1` against three remaining demands, while the
K22 row has an anchor threshold `>2` against its owner tree and two arbitrary
cycle boundaries. Thus the full multiblock theorem remains open on exactly
those two keys; this ledger no longer has nine unexpanded packet templates.
Rank-six structural targets cannot in general be inferred by subtracting the
DNN-owned key set unless the final manifest exposes a disjoint typed owner
partition.

## Ownership contract for the next pass

For each retained physical row, root the bridge-free block-cut incidence tree
at its distinguished structural block. The final ledger must assign vertices
before charging credit:

1. a shared cut belongs to the upstream territory only;
2. a boundary-open block contributes the block minus that cut, all path
   remnants on the opened side, and all descendants rooted away from the cut;
3. a structural opening takes the opened internal vertex and its complete
   owner class, while both endpoint path remnants remain with the retained
   side unless the physical structural theorem says otherwise;
4. nested cyclic demands remain one complete first-boundary territory until an
   explicit second opening is made; the intermediate cut is never charged
   twice;
5. every positive connector was already removed by the connected-theorem
   split, so no shared-cut packet may silently absorb one;
6. rooted trees, connector remnants, and deeper descendants follow exactly one
   owner.

The accepting key equality must be

`all multiblock physical keys`

`= bridge-split keys disjoint union DNN keys disjoint union packet-owner keys`.

The packet-owner keys are now expanded. The exact owner residual is
`{R31-S, R511-K22}`.  Inside `R31-S`, the marked-cut census in
`r31-s-doubled-c4-three-triangle-frontier.md` removes every noncanonical,
non-doubled-`C4`, positive-route, opened-owner, and balanced-cut row.  Its exact
remaining statements are the one-sided rooted packets `C4` and `D3`; the old
coarse description as three independent negative territories is not sharp.
Until both returned keys are proved, no complete
multiblock or all-connected rank-seven conclusion follows from this note.

## Exact debit arithmetic audit

The reductions in the partition table use the following strict comparisons.
They are listed to prevent a decimal or unquantified-margin substitution in a
later verifier.

1. `2+2+2+1`:

   `3alpha+1=(3sqrt(17)-7)/2<3`, since `sqrt(17)<13/3`.

2. Non-`K4` `3+2+1+1`:

   `2/5+alpha+2=(5sqrt(17)+9)/10<3`, since `sqrt(17)<21/5`.

3. All-odd `K5-e+Theta`:

   `2sqrt(7)-5+alpha<1` is equivalent to
   `4sqrt(7)+sqrt(17)<15`; squaring once reduces it to
   `sqrt(119)<12`, hence to `119<144`.

4. `R31-S`: if one of four cycles is a nontriangle, then

   `d(S3)+sum epsilon_i<2/5+3+p<4`, because `p<3/5`.

5. `R41`: for the odd `S4` state, one nontriangle gives

   `1/6+2+p<3` since `p<5/6`. For the even state, two
   nontriangles give `3/5+1+2p<3` since `p<7/10`; with exactly
   one nontriangle, only `P` can be worst and the exact predicate is retained.

6. All-odd `K5-e+Q_1+Q_2`: one nontriangle gives

   `2sqrt(7)-5+1+p<2`; equivalently `sqrt(7)-sqrt(5)<1/2`, whose
   positive-side double squaring gives `529<560`.

These checks establish only the stated DNN sieve. They do not close any packet
in the owner registry.
