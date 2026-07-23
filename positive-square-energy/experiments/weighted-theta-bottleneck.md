# One rooted-tree attachment: exact bottleneck

This note begins the extension of the bare-theta theorem to a theta 2-core
with one arbitrary rooted tree attached by one edge.  It records a sharp
reduction and an exact finite certificate, not a proof of the full extension.

If `H` is the theta core and the rooted tree attaches at `v`, the weighted
2-core reduction gives

`s^+(G)>=|G|-|H|+s^+(A(H)-dE_vv)`,

where `0<=d<=1/2`.  Thus it suffices to prove the weighted-theta statement at
the monotone endpoint `d=1/2`.

Numerical screening through path length 30 identifies the unique apparent
minimum as branch-rooted `Theta(2,3,3)`, with weighted slack about
`0.0110385661`.  The exact characteristic polynomial is

`(x-1)(x+1)(2x^5+x^4-14x^3-4x^2+20x-7)/2`.

Let the positive roots of the quintic be `r_1,r_2,r_3`.  An exact Sturm chain
isolates one root in each interval

`(9/20,23/50)`, `(21/25,17/20)`, `(79/35,34/15)`.

The additional factor supplies the positive eigenvalue 1, so

`s^+ > 1+(9/20)^2+(21/25)^2+(79/35)^2`

`    =3431369/490000=7+1369/490000>7`.

Hence the apparent extremal finite case is rigorously safe.  This does not
show that no larger theta/root pair has smaller slack.  The remaining task is
a uniform argument reducing all weighted thetas to finitely many branch-root
exceptions or adapting the three bare-theta witnesses to the diagonal penalty.

One tempting route fails: applying the P3-removal lemma away from the root
leaves a diagonally penalized bipartite unicyclic graph, whose square energy can
lie more than `1/16` below its order.  The root penalty must therefore enter a
global variational witness rather than being passed unchanged through the
bare-theta deletion proof.
