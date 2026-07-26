# Candidate Lemma S: rigorous quantifier audit and minimal counterexample

**Date:** 2026-07-26

## 1. Verdict

Candidate Lemma S in
`research/rank-uniform-triangular-router-interface-theorem-2026-07-26.md`
is false as written. Its smallest counterexample has triangular rank one and no
external interfaces. Its cycle-cut incidence tree is

```text
P_A - x - T - y - P_B,
```

where `x` and `y` are distinct vertices of the triangle `T`. Thus the shared-cut
cluster consists of one triangle between two pentagons at distinct cuts.

The only router split destroys `T` and leaves the two separate pentagonal
territories. Its rank-uniform state is

```text
(p,e,c,t)=(2,0,0,0),
```

so it is not accepting. The unsplit cluster is a proved positive `TPP` packet,
but it is neither a common-cut packet nor a rooted Schur--Sachs terminal of the
types named in Lemma S(3). The defect is therefore an omitted bounded-rank
terminal, not a graph counterexample to positive square energy.

## 2. The marked incidence object

Let `I` have cycle nodes `T,P_A,P_B`, cut nodes `x,y`, and edges

```text
T-x, P_A-x, T-y, P_B-y.
```

The cuts `x,y` occupy distinct vertices of `T`. Take no external interfaces and
no attached trees. This satisfies every hypothesis of Lemma S:

* `I` is a bipartite tree;
* its unique triangle has incidence degree two;
* each cut has degree two;
* it has exactly two distinguished pentagons; and
* it has zero, hence at most two, labelled external interfaces.

It is one of the four connected shared-cut incidences in the exact tricyclic
`{3,5,5}` theorem: the triangle-middle incidence with distinct cut vertices.

## 3. Exhaustion of router sequences

The only triangle node is `T`. Removing it leaves exactly the two incidence
branches containing `P_A` and `P_B`. Hence Theorem 3.1 applies with `d=2,e=0`.
The two cut marks `x,y` receive nonempty proper consecutive intervals of sizes
`1,2`, in either order.

Each interval owns one pentagon branch. No interval retains `T`, since each is
a proper path in the triangle. There is no private interface, so no naked
interface territory is created. The final cyclic territories contain precisely
`P_A` and `P_B`. Consequently the unique nonempty router sequence has

```text
p=2, e=0, c=0, t=0.
```

There is no second triangle and therefore no further refinement. The empty
sequence retains the whole `TPP` cluster. These are all router sequences.

## 4. Failure of the three conclusions

### 4.1 No accepting state

The split state `(2,0,0,0)` is not accepted by Theorem 4.1. Its ledger is

```text
c-e-p*delta=-2delta<0.
```

There is no triangular packet from which to obtain strict credit `c` or flag
`t`. The empty sequence is not a finite-state packetization with separately
charged pentagonal deficits and certified triangular credit.

### 4.2 No `PP` territory and strict triangular territory

Any strict triangular territory retaining `T` contains all three vertices of
`T`, in particular both cuts `x,y`. A connected territory retaining both
pentagons also contains `x,y`. Two disjoint induced territories cannot both own
those vertices. Conversely, after splitting `T` between `x` and `y`, the two
pentagons lie in distinct territories and no triangle remains. Thus conclusion
(2) cannot occur.

### 4.3 No terminal of the stated type

The unsplit `TPP` cluster is not common-cut: `P_A` meets `T` at `x`, `P_B`
meets `T` at `y`, and `x!=y`. The common-cut Schur--Sachs theorem explicitly
does not cover clusters with several cut vertices.

Nor does a proved all-rank rooted theorem cover two hostile cycles at two
distinct roots. The apparent all-rank rooted hostile-cycle absorption theorem
is explicitly retracted beyond its packing-one lemma, and in any event treats
one hostile cycle, not this two-pivot `TPP` core.

The graph is analytically harmless for a different reason. The exact connected
shared-cut `{3,5,5}` theorem proves

```text
sigma(TPP)>6-2sqrt(5)>0
```

for this incidence and arbitrary attached trees. That theorem is a separate
finite rank-three coefficient certificate, not a common-cut or rooted terminal
named in Lemma S(3). It cannot be added to the conclusion silently.

## 5. Minimality

Lemma S requires one or two distinguished pentagons. Triangular rank zero has
no triangle router and is outside the intended triangular incidence problem.
Thus one is the least positive triangular rank.

With one triangle and two pentagons, a connected shared-cut incidence tree
needs at least one cut node. The one-cut case is exactly the common-cut bouquet
and conclusion (3) applies. A non-common-cut connected cluster needs at least
two cut nodes, hence at least the five incidence nodes occurring above.
Choosing the triangle as the middle cycle gives two distinct router branches
and the failed state `(2,0,0,0)`. Hence this is a minimal counterexample both in
triangular rank and in the number of incidence nodes. Other colorings of a
five-node incidence path need not be unique minimal representatives; uniqueness
is not claimed.

No external marking is needed. Adding interfaces can only introduce extra
ownership constraints or naked costs; it cannot make this smaller.

## 6. Exact rank-eight/rank-nine patterns and the failed induction

The fixed-rank tables avoid this base failure by leaving certified triangular
packets after their router splits. For example, the fully shared octacyclic
rows `U4--U6` end respectively in

```text
P+P+A_4,
P+P+T+A_3,
P+P+T+T+A_2,
```

with exact margins `3-2delta`, `2-2delta`, and `1-2delta`. The weakest row is
positive because `A_2` contributes one integer credit.

Descending the same pattern to the present base removes the last retained
triangle packet and yields merely

```text
P+P,
```

with margin `-2delta`. Thus the rank-uniform state records the arithmetic
correctly but does not make the terminal set closed under induction.

The seven-triangle two-interface patterns exhibit the same issue from the
external-demand side: residual repairs work only when a retained `A_5` or
`A_6` packet supplies one or two credits. Those exact rank-nine certificates do
not prove that arbitrary pruning always reaches a positive state before all
triangle credit disappears.

More generally, the available arbitrary-r triangular estimate is only

```text
sigma(A_r)>max(0,7-r)
```

from the current packet inputs. It gives qualitative strictness at high rank,
not the integer credit needed to pay two fixed pentagonal deficits. Therefore
the exact rank-eight/rank-nine patterns cannot by themselves prove Lemma S for
arbitrary rank.

## 7. Corrected target

The literal counterexample is removed by replacing conclusion (3) with

> one terminal locked or bounded-rank packet to which a proved packet estimate
> applies, including the connected `TP`, `PP`, and `TPP` bases and the
> common-cut Schur--Sachs families.

Under this correction the path `P-x-T-y-P` is accepted as the proved `TPP`
base. This does **not** prove the amended lemma. One still needs a pruning
invariant showing that every larger incidence tree reaches an accepting state
or an enlarged terminal, with no packet margin spent twice. The rank-ten exact
two-interface census already leaves fifteen zero-score rows on two incidence
templates, illustrating that the rank-eight/rank-nine finite patterns do not
stabilize into a proof automatically.

The rigorous conclusion is therefore

```text
candidate Lemma S: false as written;
minimal counterexample: P-x-T-y-P with x!=y;
amended all-rank separator lemma: still open.
```
