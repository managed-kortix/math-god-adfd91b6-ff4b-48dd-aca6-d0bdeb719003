# Hostile audit of the family-S `h(T)=0` human proof

**Verdict: PASS.** The proof was reconstructed independently from the frozen
exact-second-neighborhood definition and the committed order-18 normal form.
No SAT/DRAT result was used as a premise, and no graph or finite abstraction
survived the actual hypotheses.

The audited conclusion is restricted exactly to the globally strict-bad,
order-18, seven-hole, shared-low family-S cell with `h(T)=0`, conditional on
the committed vertex-minimal-then-arc-minimal normal-form reduction.  It does
not exclude family D, family H, every seven-hole graph, every order-18 graph,
or a counterexample to Seymour's Second Neighborhood Conjecture.

## 1. Upstream bridge

One presentation gap in the older normal-form note had to be repaired
explicitly.  The sentence in
`attempts/2026-11-19-m7-hostile-normal-form.md` that derives two degree-nine
vertices from 146 arcs and `delta+>=8` is not valid from those facts alone: the
numeric excess may be `(2)` as well as `(1,1)`.

The missing cap follows noncircularly from committed lemmas.  The arc-deletion
inequality in `agents/tick1-structure.md`, with the non-tail monotonicity repair
in `agents/tick2-hostile-structure-audit.md`, gives

```text
1 <= mu(v)=d+(v)-d++(v) <= 2.
```

Exact first and second neighborhoods are disjoint, so on 18 vertices

```text
18 >= 1+d+(v)+d++(v)=1+2d+(v)-mu(v),
```

and therefore `d+(v)<=9`.  Seven holes give 146 arcs, and now the excess two
above baseline degree eight forces exactly `9,9,8^16`.  With that composition,
the robust-witness cover supplies family S, its shared low root, both highs in
`A`, the exact `8/7/2` layers, and the `A not-> C` barrier.  Global strict
badness and `h(T)=0` provide the remaining terminal hypotheses.  No circularity
was found.

## 2. Six pressure points

### 2.1 No arc from `U={w} union A` to `C`

`w` has no outarc to `C` because `A=N+(w)`.  If `a in A` pointed to `c in C`,
then `w->a->c`; since `c` is neither `w` nor a first outneighbor of `w`, exact
semantics would put `c in N++(w)=B`.  Thus the cut direction is correct even
when some `U--C` pairs are holes.

### 2.2 Score transport and `e(B,C)=10`

When `h(T)=0`, `D[T]` is a 16-vertex tournament with 120 arcs.  No outarc of
`U` leaves `T`, and the `U` score sum is

```text
8+9+9+6*8=74.
```

The `B` score sum in `T` is therefore 46.  Every `b in B` has full outdegree
eight, so its missing score inside `T` counts exactly its actual arcs to `C`,
including no assumption about completeness of the `B--C` cut.  Hence

```text
e(B,C)=7*8-46=10.
```

For seven entries in `{0,1,2}`, total ten forces at least one (in fact at least
three) entries equal to two.  A common `C`-dominator exists.

### 2.3 Inaccessible-inneighbor lemma

If `z->a` in a tournament and `z` is not reached by an `a`-started two-walk,
then every `x in N_T+(a)` satisfies `z->x`; the opposite direction would give
`a->x->z`.  Thus

```text
d_T+(z) >= d_T+(a)+1.
```

Tournament completeness is essential here.  With a missing `xz` pair, the
inference would fail; the proof never applies it outside `T`.

### 2.4 Five exact `T`-second neighbors

An ordinary `a in A` has T-score eight and hence seven T-inneighbors.  An
inaccessible one has T-score at least nine by the lemma.  The transported score
census shows that only `r,q` have T-score at least nine, so at most two of the
seven are inaccessible and at least five are exact second neighbors inside
`D[T]`.

### 2.5 Saturation and the high-high arc

If ordinary `a` points to a common `C`-dominator `b`, both vertices of `C` are
additional exact second neighbors through `a->b->C`; `a not-> C` ensures
exactness.  Strict badness caps the full second neighborhood at seven.  Thus
exactly five T-inneighbors are reached and the two inaccessible ones are
exactly `r,q`.

Each high then dominates `a` and all eight T-outneighbors of `a`, already nine
targets.  The arc between `r` and `q` gives its tail a tenth target, because
both highs are T-inneighbors of `a` and neither lies among those nine.  This
contradiction excludes every ordinary predecessor of a common dominator.

### 2.6 Final common-dominator degree contradiction

For a fixed common dominator `b in B`, tournament completeness gives `b->w`
and `b` toward all six ordinary vertices of `A`; it also points to both
vertices of `C`.  These nine targets are distinct:

```text
{w} union (A\{r,q}) union C.
```

But `b` is low and has outdegree eight.  This is the final contradiction.

## 3. Hostile weakening tests

The proof's boundaries were actively checked:

- replacing exact second distance by raw two-walk reach destroys the needed
  endpoint exclusion;
- allowing a missing pair inside `T` destroys both the inaccessible lemma and
  the final orientation reversal;
- one external exact second, or non-strict badness, need not force both highs
  inaccessible;
- permitting another T-score at least nine invalidates identification of the
  inaccessible pair;
- five instead of six ordinary A vertices leave only eight final targets;
- total seven across `B->C` admits `(1,1,1,1,1,1,1)` and no common dominator;
- strengthening robust support to two distinct predecessors is false and is
  not used.

The tiny dependency-free checker
`experiments/verify_m7_family_s_h0_human.py` rechecks the integer transport,
all 161 `B->C` count vectors, the 256 local orientations in the tournament
lemma, saturation, both high-high orientations, and the terminal count.  These
checks corroborate transparent local steps; they are not a certificate for the
upstream normal-form reduction.

## 4. Hypothesis audit

Once the rooted terminal package is fixed, the proof does not use vertex or
arc minimality, strong connectivity, deletion-robustness support, badness
outside the six ordinary A vertices, degrees in `C`, or computation.
Robustness is used only upstream to identify the shared-low root and its exact
layers.  Arc minimality is used only upstream to bound deficits and thereby
justify the degree cap and exact degree census.

**Final determination:** the human theorem and its bridge pass.  The corrected
degree-cap composition must accompany any future citation of the order-18
seven-hole degree census.
