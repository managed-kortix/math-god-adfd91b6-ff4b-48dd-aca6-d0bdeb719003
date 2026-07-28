# Incidence-demand coalescence: exact valid scope

**Date:** 2026-07-28

## Verdict

The demand-coalescing triangle split extends from private interface marks to
whole hostile incidence branches, but only under complete-profile and current-
ownership hypotheses.  Without them the hostile side may have profile `TPP`
rather than `PP`, or the operation may attempt to retrieve vertices from an
already closed sibling territory.

## Lemma

Let one current active induced territory wholly own a triangle `R=abx` and all
of the following complete incidence branches:

1. the complete branch at `a` has exactly one cyclic block, a pentagon;
2. the complete branch at `b` has exactly one cyclic block, a pentagon;
3. every other retained cyclic branch meets `R` at `x` and is triangular;
4. at least one triangle is retained on the `x` side.

Then the active territory has an induced refinement into

```text
PP  +  nonempty triangular cactus,                         (1)
```

and therefore has positive surplus.

## Proof

Give the consecutive interval `{a,b}` and the complete `a`- and `b`-branches
to the first owner.  Give the singleton interval `{x}` and all complete
`x`-branches to the second owner.  Every off-hull tree follows the owner of its
unique attachment.

The first territory is connected through the edge `ab`; the second is
connected through `x`.  Distinct branches cannot reconnect away from `R`,
because that would make a cycle in the incidence tree or give an off-hull tree
two attachments.  Thus both territories are induced, disjoint, and exhaustive.
The crossing edges `ax,bx` are discarded, so neither territory retains `R`.
The vertices `a,b,x` and every shared cut have exactly one owner.

By the complete-profile hypotheses, the first territory has precisely two
pentagonal cyclic blocks and hence is a proved nonnegative `PP` packet.  The
second is a nonempty triangular cactus and is strict.  Consequently

```text
sigma(G)>=sigma(PP)+sigma(triangular)>0.
```

Because all named objects lie in one current active territory, the operation
is a refinement and cannot retrieve vertices from a sibling territory.

## Why weaker formulations are false

If the `a` branch contains a pentagon and an additional triangle, the same
split produces `TPP`, not `PP`.  The `PP` certificate cannot be invoked by
ignoring the triangle.  If an earlier router has already separated part of an
`a` branch, assigning the original complete branch to the new hostile owner
would be illegal reassignment rather than nested refinement.

The lemma is therefore a valid new local transition, not a proof that every
marked incidence tree exposes this transition and not a proof of the all-rank
separator theorem.
