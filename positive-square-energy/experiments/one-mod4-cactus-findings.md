# Targeted search: two 1 mod 4 cycle blocks with trees

This note is computational reconnaissance, not a theorem.  The target is
`s^+(G)-|V(G)|` for connected bicyclic cacti whose two cycle blocks have
length `1 mod 4`, with arbitrary tree attachments.

## Search performed

`one_mod4_cactus_search.py` compresses a star of `t` leaves at a core vertex
to one weighted leaf of weight `sqrt(t)`.  The omitted `t-1` eigenvalues are
zero, so this is an exact equitable-quotient reduction for square energy
apart from numerical eigensolution.

The targeted scan included:

- cycle pairs from `{5,9}` in the main 1.47-million-candidate run, both sharing
  a vertex and joined by paths of up to eight edges;
- stars of up to 1024 leaves at every core vertex, two-root asymmetric stars,
  three-root small exhaustive allocations, and random allocations on up to six
  roots;
- a focused extension through cycle length 41 and connector length 30 with a
  million-leaf star at every possible core root (102,300 quotient matrices);
- all unlabeled trees through order 12, rooted at every vertex and coalesced at
  every core vertex of the two-C5 families through connector length eight
  (1,287,585 rooted instances);
- random trees and broom/path families through order 200.

No negative slack occurred.

## Extremal family found

The smallest family found is two `C5` blocks joined by a path of two edges,

`C5 - u - C5`,

with `t` leaves attached at the middle vertex `u`.  It has `n=t+11`.  Its
compressed characteristic polynomial is

`(x-2)(x^2+x-1)^3 Q_t(x)`,

where

`Q_t(x)=x^5-x^4-(t+5)x^3+(t+4)x^2+(3t+2)x-2t`.

Numerically:

| `t` | `s^+-n` |
|---:|---:|
| 100 | 0.52966244196236098 |
| 1,000 | 0.52805178435146691 |
| 10,000 | 0.52788291848863812 |
| 1,000,000 | 0.52786423385357235 |

At `t=10^6`, exact rational isolation of the five roots of `Q_t`, together
with a rational lower bound on `sqrt(5)`, certifies

`s^+-n > 0.5278642338535552421481`.

As `t` tends to infinity, the three bounded roots of `Q_t` tend to the roots
of `-x^3+x^2+3x-2=-(x-2)(x^2+x-1)`, while the other two roots are asymptotic
to `+/-sqrt(t)`.  Therefore

`s^+(G_t)-|V(G_t)| -> 5-2 sqrt(5) = 0.5278640450004206...`.

The first correction is positive:

`s^+(G_t)-|V(G_t)| = 5-2sqrt(5)
 + 4(sqrt(5)-2)/(5t) + O(t^-2)`.

Thus this family approaches a positive constant, not zero.

For comparison, the bare bridge `C5--C5` has slack
`0.59387375123695...`; the bare path-two handcuff has
`0.65224947682514...`.  Placing the huge star at the middle of the latter
creates the lower limit above.  Huge stars at the shared vertex, bridge
endpoints, or remote cycle vertices were all less dangerous.

## Interpretation

The computations do not support a counterexample or the guess that the
infimum is zero.  They instead suggest the sharper extremal conjecture

`s^+(G)-|V(G)| >= 5-2sqrt(5)`

for bicyclic cacti with two cycle blocks of length `1 mod 4` and arbitrary
trees, with equality unattained and approached only by the middle-star
`C5-P3-C5` family (up to harmless descriptions of the same rooted shape).

This remains conjectural: the scans do not exhaust arbitrary rooted trees of
unbounded order or simultaneous non-star attachments at all core vertices.
The exact quotient family is nevertheless evidence against both a crossing
and an infimum of zero.
