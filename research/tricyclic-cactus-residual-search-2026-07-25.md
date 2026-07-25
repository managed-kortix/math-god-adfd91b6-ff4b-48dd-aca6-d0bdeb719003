# Tricyclic cactus residual triples: targeted counterexample search

## Scope

The sharp cactus DNN estimate gives, for a tricyclic cactus with cycle lengths
`l1,l2,l3`,

`s+(G)-n >= 2-sum epsilon_li`.

Its odd residual triples therefore include `{3,5,5}` and `{3,3,q}` for odd
`q`.  This note is computational reconnaissance for those triples, not a
proof for arbitrary attached trees.

The search covered all bouquet/Y connector lengths through four, all chain
incidences with connector lengths through four, pendant stars at every core
vertex through `10^8` leaves, brooms with stems through length five, random
multi-root star allocations, and all connector trees through order seven.
An additional rooted-tree scan attached every unlabeled tree through order ten
to each vertex of the leading cores.  No graph with `s+(G)<n` was found.

## Exact large-star reduction

For a fixed core `H`, attach `t` leaves at `v`.  The nonzero spectrum is that
of the symmetric quotient

`B_t = [[A(H),sqrt(t)e_v],[sqrt(t)e_v^T,0]]`,

and

`chi_Bt(x)=x chi_H(x)-t chi_(H-v)(x)`.

The other `t-1` eigenvalues are zero.  More importantly, direct separation of
the two unbounded roots gives the exact limiting identity

`lim_(t->infinity) (s+(G_t)-|G_t|) = deg_H(v)+s+(H-v)-|H|`.       (1)

Thus massive-star limits can be computed from the components left after
deleting the root, without numerically subtracting two quantities of order
`t`.  Forest components are harmless in (1), since `s+(T)=|E(T)|` for every
forest `T`.

## Leading candidate for `{3,5,5}`

Let a triangle contain `v`, join `v` by one bridge to each of two disjoint
pentagons, and put a `t`-leaf star at `v`.  The core has order 13 and deleting
`v` leaves `K2 disjoint-union C5 disjoint-union C5`.  Since

`s+(C5)=7-sqrt(5)`,

formula (1) gives

`lim (s+-n) = 4 + 1 + 2(7-sqrt(5)) - 13`
`             = 6-2sqrt(5) = 1.5278640450004206...`.             (2)

The exact quotient polynomial is

`(x-2)(x+1)(x^2+x-1)^3 R_t(x)`,

where

`R_t(x)=x^6-2x^5-(t+6)x^4+(2t+11)x^3`
`       +(2t+4)x^2-(5t+6)x+2t`.

High-precision quotient values are

| `t` | `s+-n` |
|---:|---:|
| 10 | 1.9752974821759910 |
| 1,000 | 1.5892444054798777 |
| 1,000,000 | 1.5298622318643786 |
| `10^12` | 1.5278660449986095 |

The same limit survives arbitrary extra forest components incident directly
with `v`; they cancel from (1).  This explains the many nonisomorphic tied
connector-tree hits.  It is an extremal family, not a unique graph shape.

## Leading candidates for `{3,3,q}`

For `q=1 mod 4`, let two triangles share `v`, join `v` by one bridge to a
disjoint `Cq`, and put the massive star at `v`.  Deleting `v` leaves two copies
of `K2` and `Cq`.  The cycle identity

`s+(Cq)-q = 1-sec(pi/q)`

then gives

`lim (s+-n) = 3-sec(pi/q)`.                                    (3)

This is smallest at `q=5`:

`4-sqrt(5)=1.7639320225002103...`.

For `q=3 mod 4`, the analogous value is exactly 2 because `s+(Cq)=q`.
Putting all three cycles through the star root also gives exactly 2 in the
limit for every odd `q`: deleting the root leaves two `K2` components and the
bipartite path `P_(q-1)`.

Observed minima agree with these formulas:

| triple | least candidate |
|---|---:|
| `{3,3,3}` | 2 |
| `{3,3,5}` | `4-sqrt(5)=1.7639320225...` |
| `{3,3,7}` | 2 |
| `{3,3,9}` | `3-sec(pi/9)=1.9358222275...` |
| `{3,3,13}` | `3-sec(pi/13)=1.9700721691...` |

For `{3,3,5}`, the quotient polynomial factors as

`(x-1)(x+1)^2(x^2+x-1) S_t(x)`,

where

`S_t(x)=x^6-2x^5-(t+7)x^4+(2t+11)x^3`
`       +(2t+10)x^2-(5t+9)x+2t`.

## Counterexample assessment

- No candidate threatens `s+(G)>=n`; the lowest observed/derived limit is
  `6-2sqrt(5)>1.52` above `n`.
- The DNN lower bound is misleadingly weak here.  It permits a deficit for
  `{3,5,5}` and every `{3,3,q}`, while exact star limits retain a large gap.
- A likely sharp residual-triple statement is
  `s+(G)-n >= 6-2sqrt(5)`, with equality unattained and approached by (2),
  including its harmless root-forest variants.
- Within `{3,3,q}`, the likely sharp constants are (3) for `q=1 mod 4` and 2
  for `q=3 mod 4`.
- The principal unresolved risk is not massive stars, brooms, connector
  length, or finite connector trees.  It is a genuinely multi-root unbounded
  tree allocation for which no relocation or concentration theorem is known.

The reproducible search driver is
`positive-square-energy/experiments/tricyclic_cactus_residual_search.py`.
