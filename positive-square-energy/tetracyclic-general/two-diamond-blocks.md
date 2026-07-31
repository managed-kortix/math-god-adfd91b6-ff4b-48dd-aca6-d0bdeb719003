# Two diamond blocks

## Theorem

Let a finite simple connected graph have exactly two positive-rank cyclic
blocks, both `Theta(1,2,2)` (diamonds), with arbitrary bridge blocks and rooted
trees. Then `s^+(G)>|V(G)|`.

An attached diamond has surplus `sigma=s^+-|V|>1`: its normalized Sachs
polynomial has strictly negative imaginary part for every positive spectral
parameter because its only odd cycles are two favorable triangles, while its
four-cycle contribution is real. Coulson therefore gives `D=s^+-s^->0`, and
as the territory is bicyclic, `sigma=1+D/2>1`.

If a bridge separates the diamonds, cut it into two induced attached-diamond
territories. Their total surplus is greater than two.

Suppose instead that the diamonds share a cut `c`. Assign `c` and the first
intact diamond to territory H.

- If c has diamond-degree three in the second diamond, its other three vertices
  induce a path; with every branch rooted there they form one nonempty tree T.
- If c has diamond-degree two, transfer one of its degree-three neighbors p to
  H, together with the edge cp and all branches rooted at p. This is only an
  attached tree at c, so H remains an attached diamond. The two vertices left
  from the second diamond induce an edge and, with their branches, one tree T.

In either orbit, the territories are induced, disjoint, connected, and own
every branch exactly once. Thus `sigma(H)>1`, `sigma(T)=-1`, and induced
square-energy superadditivity gives `sigma(G)>0`.
