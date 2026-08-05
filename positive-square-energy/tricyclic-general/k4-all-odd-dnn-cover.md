# The all-odd switching class of arbitrary `K4` subdivisions

## Theorem

Let `B` be a simple subdivision of `K4` whose six branch-path parities lie in
the all-odd switching class. Attach arbitrary rooted trees at arbitrary
vertices of `B`, identifying only their roots with the existing graph. For the
resulting graph `G`,

`s^+(G) >= |V(G)|`.

Except for limits inherited from the DNN inequality, every DNN case below has
a strict certificate. This note, together with
`k4-seven-switching-classes.md`, closes all eight switching classes. Switching
is used only to transport endpoint Gram vectors; physical path lengths are
never switched.

## 1. Exact DNN path reduction

Write the branch vertices as `1,2,3,4`, the six branch paths as `P_ij`, their
lengths as `l_ij`, and

`L = sum_(ij) l_ij`.

The bare subdivision has `L` edges and `L-2` vertices. Let `kappa` be the
LTZ/DNN constant in correlation-dual form. It satisfies

`s^-(H) <= kappa(H)`

and is additive over one-vertex sums. If unit branch vectors have correlation
`r_ij`, exact elimination of `P_ij` gives the excess over its `l_ij`-edge
baseline as

`f_l(r) = l tan^2(acos((-1)^l r)/(2l)).`                    (1)

Thus a branch correlation matrix `R` with

`sum_(ij) f_(l_ij)(R_ij) <= 2`                             (2)

gives `kappa(B)<=L+2`, and hence

`s^+(B)=2L-s^-(B)>=2L-kappa(B)>=L-2=|V(B)|`.               (3)

For fixed endpoint correlation and fixed parity,

`f_(l+2)(r) <= f_l(r)`.                                    (4)

Indeed, after fixing the transformed endpoint angle `beta`, the excess is
`l tan^2(beta/(2l))`; differentiating in `l` gives a negative derivative
because `sin z cos z<z` for `0<z<pi/2`. Therefore an odd path is either
unit (`l=1`) or long, in which case its worst length is three.

## 2. Reduction of the switching class to the physical all-odd row

Because the parity row is in the all-odd switching class, there are bits
`s_1,...,s_4` such that

`l_ij mod 2 = 1 xor s_i xor s_j`.                           (5)

Normalize `s_4=0`. Given normalized unit vectors `u_i`, use the physical
vectors

`v_i=(-1)^(s_i)u_i`.                                       (6)

Then

`(-1)^(l_ij) <v_i,v_j> = -<u_i,u_j>`.                      (7)

Consequently the transformed endpoint angle in (1) is exactly the angle for
an odd normalized path with endpoint correlation `<u_i,u_j>`. Its coefficient
and denominator, however, remain the physical `l_ij`.

If a physical path is even, then `l_ij>=2`. For a fixed transformed angle
`beta`, the function `x tan^2(beta/(2x))` decreases for all real `x>=1`.
Therefore its cost is no larger than the odd canonical length-one cost having
the same transformed angle:

`l_ij tan^2(beta/(2l_ij)) <= tan^2(beta/2)`.                (8)

If it is odd, its canonical physical length is already one. Call a physical
path unit when its length is one and long otherwise. A long path has length at
least two when even and at least three when odd. Thus its cost is bounded by
the length-two or length-three value, respectively. Every certificate below is
evaluated with these physical lower lengths; no length is switched.

It remains to classify the six physical paths as unit or long and prove (2)
at their physical lower lengths one, two, and three.

## 3. At least three long paths: one simplex certificate

Use the regular-simplex Gram matrix

`R_ii=1,  R_ij=-1/3  (i!=j)`.                              (9)

It is positive semidefinite, with eigenvalues `4/3,4/3,4/3,0`. A unit path
costs

`f_1(-1/3)=tan^2(acos(1/3)/2)=1/2`.                        (10)

Put `beta=acos(1/3)`. A long odd path costs at most

`f_3(-1/3)=3tan^2(beta/6)<1/6`.                            (11)

Here is an exact proof of (11). If `t=tan(beta/6)`, the triple-angle identity
and `tan(beta/2)=1/sqrt(2)` give

`(3t-t^3)/(1-3t^2)=1/sqrt(2)`.

On `0<t<1/sqrt(3)` the left side is strictly increasing. At
`t=1/(3sqrt(2))`, which is the boundary `3t^2=1/6`, its value is
`53/(45sqrt(2))>1/sqrt(2)`. Therefore `t<1/(3sqrt(2))`, proving (11).

If `q>=3` paths are long, the total excess is strictly less than

`(6-q)/2+q/6 = 3-q/3 <= 2`.                                (12)

when all paths are physically odd. For an even long path the length-two cost is

`2tan^2(beta/4)<1/4`.                                       (13)

Indeed, the half-angle identity reduces this to
`sqrt(2/3)>7/9`, whose square is `2/3>49/81`. A nonconstant
switching vector in (5) makes exactly three or four physical paths even: they
are the edges of a nontrivial cut of `K4`. All of them are long. Therefore, if
at least four paths in total are long, the simplex excess is strictly below

`(6-q)/2+q/4 = 3-q/4 <= 2`.                                (14)

The only case not yet strict is exactly three long paths consisting of a
three-edge physical even cut and three unit odd paths.

There is one useful strengthening for the later switching audit. If precisely
three paths are long and the physical switch in (5) makes all three long paths
even and all three unit paths odd, (12) by itself has only comparison value
two. In that row use the simplex matrix (9) again, but evaluate its physical
length-two costs rather than bounding them by length-three odd costs. The three
unit odd paths contribute `3/2`. Each long even path contributes at most

`2tan^2(acos(1/3)/4)<1/6`,

because the half-angle identity reduces the strict inequality to
`sqrt(8/9)>11/13`, whose square is `8/9>121/169`. Thus the total excess is
strictly below `3/2+3/6=2`.                                (15)

## 4. Exactly two long paths: the two edge orbits

With only two long paths the switch in (5) must be constant, since a
nonconstant switch already creates at least three even, hence long, paths.
Thus all six physical paths are odd. There are only two placements under
`Aut(K4)`: opposite and adjacent.

### Opposite long paths

Put the long paths on `12` and `34`, and give the four branch vectors planar
angles

`(0, pi/4, pi, 5pi/4)`.                                    (13)

For an odd path, the transformed angle is `pi` minus the smaller angle between
its endpoint vectors. The two long paths therefore have transformed angle
`3pi/4`, two unit paths have transformed angle zero, and two unit paths have
transformed angle `pi/4`. The total excess is

`6tan^2(pi/8)+2tan^2(pi/8)`
`=8tan^2(pi/8)=24-16sqrt(2)<2`.                             (14)

The final inequality is equivalent to `sqrt(2)>11/8`, whose square is
`2>121/64`.

### Adjacent long paths

Put the long paths on `12` and `13`, and use planar angles

`(0,3pi/8,13pi/8,pi)`.                                     (15)

The two long paths have transformed angle `5pi/8`. Among the four unit paths,
one has transformed angle `pi/4`, two have transformed angle `3pi/8`, and one
has transformed angle zero. Thus the exact canonical excess is

`6tan^2(5pi/48)+tan^2(pi/8)+2tan^2(3pi/16)`.                (16)

The following strict rational bounds certify (16) exactly:

`tan^2(5pi/48)<7/60`,
`tan^2(pi/8)<7/40`,
`tan^2(3pi/16)<9/20`.                                      (17)

They imply that (16) is smaller than

`6(7/60)+7/40+2(9/20)=71/40<2`.                            (18)

For a self-contained audit of (17), use

`tan^2 x<q  iff  cos(2x)>(1-q)/(1+q)`                      (19)

for `0<x<pi/2`, together with `pi<355/113` and the alternating lower
Taylor bound

`cos y > 1-y^2/2+y^4/24-y^6/720`                           (20)

for `0<y<pi/2`. Substituting respectively

`(y,q)=(5pi/24,7/60),(pi/4,7/40),(3pi/8,9/20)`

and replacing `pi` by `355/113` in the decreasing polynomial in (20) gives,
after clearing positive denominators, the positive numerators

`8858386029377237523769`,
`287162942936656949`,
`831220125392302623`,                                      (21)

respectively. The verifier artifact reproduces these integer checks.

Longer paths only improve (14) and (16) by (4).

## 5. Zero or one long path: exact induced deletion

The DNN budget is not the right tool for these final two configurations. Use
an actual induced vertex partition instead.

### Exactly one long path

Let `P_ab` be the unique physical long path. It has
length at least two: length at least three if odd, and at least two if even.
Choose an internal vertex `v` of `P_ab`, and let `T` be `v` together with the
entire rooted tree attached at `v`. Then `T` is a nonempty induced tree, so

`sigma(T):=s^+(T)-|V(T)|=-1`.                              (22)

The induced complement `H=G-V(T)` is connected. The two remnants of `P_ab`
are rooted trees, and the unique cyclic block of `H` is the theta between the
complementary branch vertices `c,d`, with path lengths

`l_cd,  l_ca+l_ad,  l_cb+l_bd`.                             (23)

After applying (5), all three numbers in (23) have the same parity: each has
parity `1 xor s_c xor s_d`. Thus the theta is bipartite. An attached bipartite
theta has

`sigma(H)=1`.                                               (24)

Induced square-energy superadditivity now gives

`sigma(G)>=sigma(T)+sigma(H)=0`.                            (25)

This deletion is physical: it does not replace the long path by a switched
path, and it assigns every attached branch to exactly one induced territory.

### No long path

No physical path is long. If `s_i!=s_j`, (5) makes the physical path even,
so it cannot have length one and would be long by the normalization above.
Therefore all `s_i` are equal. With `s_4=0`, all are zero, and every physical
path has length one. The cyclic block is the actual unsubdivided `K4`.

For completeness, the attached-`K4` packet is strict. In its grouped Sachs
expansion, every triangle singleton contributes negative imaginary phase,
while four-cycles contribute only to the real part. Hence the continuous-
argument/Coulson lemma gives `s^+>s^-`. Since `m=n+2` for a unique attached
`K4` block,

`s^+>m=n+2>n`.                                              (26)

Equivalently, this is the established unique-`K4` rooted-tree packet lemma.

## 6. Rooted trees in the DNN cases

Sections 3 and 4 prove `kappa(B)<=L+2` for the bare cyclic block. The DNN
constant is additive over one-vertex sums, and a tree with `t` edges has
`kappa=t`. Attaching such a rooted tree adds `t` to `kappa`, `|E|`, and
`|V|`. Thus the calculation (3) is unchanged. Sections 5 already include all
rooted trees through exact induced territories and the attached-`K4` packet.

The four cases -- at least three, exactly two, exactly one, or zero physical
long paths -- are exhaustive. Therefore every arbitrary subdivision in the
all-odd switching class, with arbitrary rooted-tree attachments, satisfies
`s^+(G)>=|V(G)|`.

## Verification artifact

Run

`python3 positive-square-energy/experiments/k4_all_odd_exact_verify.py`

and repeat with `python3 -O`. The script uses only integer/rational arithmetic.
It verifies the simplex triple-angle comparison, the opposite-edge radical
comparison, all three adjacent-edge Taylor certificates, the final `71/40<2`
budget, and the eight switching rows' canonical unit/long lower-length rules.
