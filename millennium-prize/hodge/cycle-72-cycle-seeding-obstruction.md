# Cycle 72: the cycle-seeding obstruction

## Generic algebraicity is exactly the missing seed

Let `V` be a reduced irreducible marked Hodge component in a smooth projective
family, with flat rational class `gamma`, and let `bar eta` be its geometric
generic point. Consider

\[
(GA_V):\qquad
\gamma_{\bar\eta}\in\operatorname{im}
\left(CH^p(X_{\bar\eta})_\mathbf Q\to
H^{2p}(X_{\bar\eta},\mathbf Q(p))\right).            \tag{72.1}
\]

Then `(GA_V)` is equivalent, after finite generically dominant base change, to
the existence of a relative Chow/Hilbert component carrying `gamma` and
dominating `V`.

- A dominant cycle component restricts to a generic cycle.
- A generic cycle is defined over a finite extension of `C(V)`; spreading it
  over an open set and taking its proper Chow closure produces a dominating
  component.

Thus the component-independent seed requested after Cycle 71 is not supplied by
formal geometry: it is the generic Hodge assertion itself.

## Exact propagation theorem

Assume `(GA_V)`. After shrinking and finite base change, write the generic
rational cycle as a difference of effective cycles of fixed degree. Its point
lies in a product of relative Chow spaces. The closure of its component is
proper and dominant over `V`, hence surjective. The universal difference cycle
has class `gamma` generically and therefore everywhere, because both are flat
sections of the pulled-back local system.

Consequently,

\[
\boxed{(GA_V)\Longrightarrow
\gamma_v\text{ is algebraic for every }v\in V(\mathbf C).}        \tag{72.2}
\]

This is a propagation theorem, not a seed theorem.

## Why the standard formal mechanisms cannot seed

- Cattani--Deligne--Kaplan proves that the Hodge locus is algebraic, not that
  its marked class is algebraic.
- Relative Chow spaces are countable in Hilbert data, but a countable union of
  proper closed images can be dense without any dominant member.
- Properness specializes generic cycles; it does not generize a cycle existing
  only on a special fiber.
- Spread starts from an object over the generic field; it does not manufacture
  that object.
- Degeneration to Fermat or toric fibers additionally requires incidence with
  the chosen boundary, exact monodromy/lattice class matching, survival in the
  weight spectral sequence, and a cycle component dominating back toward `V`.
- Rational algebraic `K_0` is isomorphic through Chern character to rational
  Chow groups. A perfect-complex lift of `gamma` exists exactly when the class
  is already algebraic. Deligne lifts exist for every Hodge class and therefore
  do not imply algebraicity; normal functions address only the secondary
  Abel--Jacobi layer.

Abstract polarized VHS data can be held fixed while the collection of cycle
parameter spaces is declared empty or nonempty. This shows formally that VHS,
countability, and properness alone do not encode cycle realization. It is a
logical no-go, not a geometric counterexample to Hodge.

## Reach limitation and prior art

Even domination of every marked component for every hypersurface fourfold
would prove the rational Hodge conjecture only for codimension-two classes on
those hypersurfaces. No unconditional reduction from arbitrary smooth
projective varieties to this family is known; hyperplane restriction would
require an algebraic inverse Lefschetz operator, and blowup or degeneration
introduces the Hodge problem for centers or special fibers.

Broad seeded families are already known. Complete-intersection components are
treated by Dan's variational Hodge theorem, and certain combinations of linear
cycles by work of Villaflor Loyola and collaborators. These propagate supplied
low-complexity cycles but do not provide arbitrary component seeds.

Therefore the Hodge component-domination tactic has reached its rotation gate:
the branch-promotion criterion is settled, while the remaining universal seed
is equivalent to generic algebraicity. Cycles 70--72 remain useful exact
calibrations. No Hodge solution is claimed.
