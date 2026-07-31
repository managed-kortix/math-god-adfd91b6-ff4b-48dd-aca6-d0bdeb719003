# The all-odd K4-subdivision class

Let every one of the six branch paths of a K4 subdivision have odd length.
Call a path unit if its length is one and long otherwise (hence length at least
three). The core has `L` edges and `L-2` vertices. We prove `s^+>=L-2`, with
arbitrary rooted-tree attachments, by an exact DNN/partition cover.

For odd l and endpoint correlation r, the path excess over its l-edge baseline
in the elliptope dual is

`f_l(r)=l tan^2(acos(-r)/(2l))`.

It decreases with l among odd lengths.

## At least three long paths

Use four regular-simplex unit vectors, with every off-diagonal correlation
`-1/3`. A unit path contributes `1/2`. A long path contributes at most

`3 tan^2(acos(1/3)/6)<1/6`.

The last inequality follows exactly from the triple-angle formula (all sides
are positive). If q paths are long, total excess is strictly below
`(6-q)/2+q/6=3-q/3<=2` for `q>=3`.

## Exactly two long paths

There are two placements.

If they are opposite, assign planar branch angles `(0,pi/4,pi,5pi/4)` with
the long paths on the two pi/4 pairs. The excess is at most

`8 tan^2(pi/8)=24-16sqrt(2)<2`.

If they are adjacent, put the common endpoint at angle zero, the two other
endpoints at `3pi/8,13pi/8`, and the fourth at pi. At canonical long length
three the excess is

`6 tan^2(5pi/48)+tan^2(pi/8)+2tan^2(3pi/16)<2`.

For an exact rational check use respectively the strict upper bounds
`7/60,7/40,9/20`; their weighted sum is `71/40`. Longer paths only improve
the certificate.

## Zero or one long path

With one long path, delete one internal vertex and all branches rooted there.
That induced territory is one nonempty tree of surplus `-1`; the complement
has attached core `Theta(1,2,2)`, whose two favorable triangles give surplus
strictly greater than one. Thus the total surplus is positive.

With no long path the core is K4. Its spectrum is `{3,-1,-1,-1}`, so its
positive square energy is 9; the established attached-K4 packet gives the same
strict conclusion under arbitrary rooted trees.

One-vertex additivity of kappa extends every DNN row to arbitrary rooted trees.
These four cases exhaust the all-odd switching class.
