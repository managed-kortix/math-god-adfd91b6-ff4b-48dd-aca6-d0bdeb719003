# Bridge-path cactus cycle closure: counterexample search

## Target

For a cactus `H`, let `u,v` be joined by a path all of whose edges are bridges.
The tested claim is

`s+(H+uv) >= s+(H)`.

Adding `uv` closes that bridge path into one new cactus cycle.  This note is
counterexample-oriented computational reconnaissance, not a proof of the
unweighted claim.

## Weighted counterexample

The edge-weighted extension is false on five vertices.  Let `H` be the path

`0--1--2--3--4`

with every displayed edge of weight `4`, and add the unit edge `04`.  Exact
rational root isolation gives

`s+(H+04)-s+(H) = -0.474077261882... < 0`.

The characteristic polynomials are

`chi_H(x)=x(x^2-48)(x^2-16)`

and

`chi_(H+04)(x)=x^5-65x^3+800x-512`.

Thus even zero vertex potentials suffice; arbitrary potentials are not needed.
Uniform path weight `w` already changes sign between `w=2` and `w=4`.

This weighted example has no immediate unweighted cactus realization.  The
usual equitable realization of a weight `4` by twin blow-ups introduces many
4-cycles sharing edges, while subdivision does not approximate a large edge
weight spectrally.  Searches with stars therefore treated stars as exact
unweighted quotient gadgets rather than claiming such a realization.

## Unweighted search

The search used exact symmetric quotients for pendant stars: `t` leaves at a
root become one quotient leaf of edge weight `sqrt(t)`, with the omitted
`t-1` eigenvalues equal to zero.  It covered:

- bridge paths through 50 edges;
- pendant stars with counts through `10^12`, including asymmetric multi-root
  allocations;
- brooms with stems through eight edges;
- asymmetric bouquets of pre-existing `C3` and `C5` blocks along the path;
- 20,000 additional random `C3/C5`-decorated path instances;
- every cactus in the NetworkX graph atlas through order seven and every
  eligible closure pair (366 pairs).

No negative unweighted increment was found.  The lowest observed graph has
seven vertices and edges

`01,12,23,34,45,46,56`,

with closure edge `04`.  In words, it is a five-vertex bridge path whose final
vertex is the cut vertex of a triangle.  Exact isolation gives

`s+(H)=7.8870456660868138346...`,

`s+(H+04)=8.6360676996151575639...`,

and increment

`0.7490220335283437293... > 0`.

Its characteristic polynomials are

`chi_H(x)=(x+1)(x^6-x^5-6x^4+4x^3+9x^2-3x-2)`

and

`chi_(H+04)(x)=x(x+1)(x^2+x-1)(x^3-2x^2-4x+7)`.

The bare path minimum in the tested range is the `P5 -> C5` increment
`3-sqrt(5)=0.763932022500210...`; the terminal triangle improves it slightly
to the current `0.749022...` frontier.  Huge stars did not lower this frontier.

## Reproduction

Run

```text
python positive-square-energy/experiments/bridge_path_cycle_closure_certificate.py
python positive-square-energy/experiments/bridge_path_cycle_closure_search.py \
  --trials 5000 --max-path 30 --max-star 1000000000
```

The first command is exact.  The second is a seeded floating-point discovery
search; larger trial counts extend, but do not certify, the family coverage.
