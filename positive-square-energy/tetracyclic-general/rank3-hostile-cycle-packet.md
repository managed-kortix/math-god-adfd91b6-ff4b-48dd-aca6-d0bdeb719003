# Rank-three block plus one hostile cycle: canonical residual packet

## Theorem

Let `G` be connected and let its positive-rank cyclic blocks be

- one rank-three block `B`, which is a simple subdivision of the doubled
  triangle, doubled `C4`, or `K4`; and
- one unicyclic block `Q=C_q`, where `q=1 mod 4`.

Arbitrary bridge connectors and arbitrary rooted trees are allowed. Assume
that the physical row of `B` is one of the following rank-three residual
families:

1. doubled triangle: class `111`, both doubled pairs first-simple;
2. doubled `C4`: the exceptional eight-row kernel-automorphism orbit, with
   both doubled pairs first-simple and the two connectors arbitrary in their
   fixed opposite parities (four anchors in switching class `110` and four in
   class `111`);
3. all-odd `K4`: exactly one long path or no long path.

Then

`s^+(G)>=|V(G)|`,

strictly in every row covered below.

The main point is that a tetracyclic graph has a DNN excess budget of three,
not two. The canonical rank-three rows miss their old rank-three budget by
only a small explicit amount. Their exact canonical Gram costs, together with
the hostile cycle cost, still lie strictly below three. Thus no tricyclic
remainder is asked to pay both a deleted tree and a hostile deficit.

## 1. Exact block budget

For a graph `H`, let `kappa(H)` be the LTZ/DNN constant in correlation-dual
form. It satisfies

`s^-(H)<=kappa(H)`

and is additive over one-vertex sums. In particular, bridges and rooted trees
contribute exactly one per edge.

Suppose the rank-three subdivision `B` has `L` edges. It has `L-2` vertices.
If its exact path elimination has a correlation certificate of excess `e_B`,
then

`kappa(B)<=L+e_B`.                                           (1)

For an odd cycle,

`kappa(C_q)=q+epsilon_q`,

`epsilon_q=q tan^2(pi/(2q))`.                               (2)

The function `epsilon_q` decreases through odd integers, so for hostile
`q>=5`,

`epsilon_q<=epsilon_5=5-2sqrt(5)<3/5`.                      (3)

Let all bridge and tree blocks outside `B,Q` have altogether `t` edges. Block
additivity and (1)--(2) give

`kappa(G)<=L+q+t+e_B+epsilon_q`.                            (4)

The graph has

`|E(G)|=L+q+t`, `|V(G)|=L+q+t-3`.

Consequently, whenever

`e_B+epsilon_q<=3`,                                        (5)

we have

`s^+(G)=2|E(G)|-s^-(G)>=2|E(G)|-kappa(G)>=|V(G)|`.          (6)

Strict inequality in (5) gives strict inequality in (6). This calculation
already owns every connector and every attached tree; no territory deletion
is required.

For a branch path of length `l` and endpoint correlation `r`, use

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.                       (7)

A planar assignment of branch-vector angles gives a positive-semidefinite
correlation matrix automatically. The following three sections give the exact
canonical assignments needed in (5).

## 2. Doubled triangle

Write

`a,A:01`, `b,B:02`, `c:12`.

The structural orbit is `EO,EO` with odd `c`. When both doubled pairs are
canonical, interchange parallel members so that

`(a,A,b,B,c)=(2,1,2,1,1)`.                                 (8)

Give branch vertices `0,1,2` planar angles

`0, 3pi/5, 7pi/5`.                                         (9)

Substitution in (7) gives the exact excess

`e_DT=4tan^2(3pi/20)+2tan^2(pi/5)+tan^2(pi/10)<221/100`.    (10)

For an exact rational check, the standard pentagonal radical expressions and
one positive half-angle step give

`tan^2(3pi/20)<13/50`,

`tan^2(pi/5)<53/100`,

`tan^2(pi/10)<11/100`.

After substituting `cos(pi/5)=(1+sqrt(5))/4`, each comparison reduces by at
most two squarings of positive sides to an integer inequality. Their weighted
sum is `221/100`, proving (10) without decimal optimization.

Every placement of the odd member in either doubled pair has the same cost
after relabelling the parallel paths. Hence (10) covers all four labelled
canonical structural rows. From (3),

`e_DT+epsilon_q<221/100+3/5=281/100<3`.                     (11)

Equations (4)--(6) prove the claimed strict surplus. This replaces both old
subcases (`c=1` and `c>=3`) by one uniform tetracyclic DNN certificate.

## 3. Doubled `C4`

Write

`a,A:01`, `b:12`, `c,C:23`, `d:30`.

The tricyclic ledger has exactly `64` labelled parity words. Twenty-eight
words containing an odd--odd doubled side are DNN with the uniform rational
upper bound `229/150<2`. The old no-`OO` slice has `28` further DNN words and
one exceptional eight-row automorphism orbit. Under the fixed switching
normalization, that orbit contains four rows in class `110` and four in class
`111`; it is not one switching class. After a genuine kernel automorphism and
compatible interchanges within the parallel fibres, normalize one first-simple
parity anchor to

`(a,A,b,c,C,d)=(2,1,2,2,1,1)`.                             (12)

The branch angles

`0, 2pi/3, pi/2, 7pi/6`                                    (13)

give

`e_DC4=2+2tan^2(pi/24)+tan^2(pi/12)<9/4`.                   (14)

Indeed `tan^2(pi/12)=7-4sqrt(3)<3/40`, and one more positive
half-angle step gives `tan^2(pi/24)<1/20`. Therefore the left side of (14) is
strictly smaller than `2+1/10+3/40=87/40<9/4`. Each radical inequality is
verified by one squaring of positive sides.

The four vertex automorphisms, together with compatible exchanges inside the
two parallel fibres, induce `16` genuine edge permutations. Their orbit of the
parity row `010011` is exactly

`010011, 010101, 011010, 011100,`

`100011, 100101, 101010, 101100`.

Transporting the planar vectors (13) along the same physical kernel
isomorphism merely permutes the six path contributions, so every transported
Gram matrix has the same cost (14). This is automorphism transport, never
switching transport. If both doubled pairs retain their first-simple lengths,
the two connectors may have arbitrary lengths of their fixed parities:
componentwise fixed-parity monotonicity applied to the transported witness
preserves (14). If instead a doubled member is longer than first-simple, the
separate exact bounds `1862/1000` or `1662/1000` apply. Hence one first-simple
witness covers the complete eight-anchor orbit and all connector-only
descendants, with its four-plus-four switching-class split. By (3),

`e_DC4+epsilon_q<9/4+3/5=57/20<3`.                          (15)

This is the desired hostile repair. In particular, it avoids the invalid
ledger

`sigma(TT)>1`, `sigma(tree)=-1`, `sigma(Q)>=-delta_q`,

whose sum need not be positive.

## 4. All-odd `K4` with exactly one long path

By symmetry let `P_01` be the unique long path. Fixed-parity monotonicity makes
length three the hardest case, so take

`l_01=3`, and `l_ij=1` on the other five paths.             (16)

Give branch vertices `0,1,2,3` angles

`0, pi/5, 4pi/5, 7pi/5`.                                   (17)

The exact path excess is

`e_K=3tan^2(2pi/15)+3tan^2(pi/5)+2tan^2(pi/10)<12/5`.       (18)

One exact rational audit is

`tan^2(2pi/15)<199/1000`,

`tan^2(pi/5)<529/1000`,

`tan^2(pi/10)<106/1000`.

The last two follow directly from the standard `sqrt(5)` expressions. For the
first, use `2pi/15=pi/3-pi/5`, substitute the same `sqrt(5)` expressions in
the tangent subtraction formula, and square positive sides. After clearing
denominators the three comparisons are integer inequalities. They give

`e_K<3(199/1000)+3(529/1000)+2(106/1000)`

`    =2396/1000<12/5`,

proving (18). Increasing the long odd length by two only decreases its term,
so the certificate covers every exactly-one-long row. The six choices of long
edge are equivalent under `K4` automorphisms. Finally,

`e_K+epsilon_q<12/5+3/5=3`.                                 (19)

Thus (6) is strict.

## 5. Unsubdivided `K4`

If no all-odd path is long, the rank-three block is the unsubdivided `K4`.
Here the regular-simplex DNN certificate has excess three, leaving no room for
the hostile cycle, so use an induced packet instead.

The attached-`K4` Sachs theorem gives, for every `K4` with arbitrary rooted
trees,

`sigma(K4 packet)>2`.                                      (20)

If `K4` and `Q` are joined by a nontrivial bridge route, cut one actual bridge
and assign the whole connector to either side. The hostile unicyclic packet
satisfies

`sigma(Q packet)>=-delta_q`, `delta_q=sec(pi/q)-1<1`.

Therefore induced superadditivity gives

`sigma(G)>2-delta_q>0`.                                    (21)

If the blocks share a cut vertex `z`, put `z`, the complete `K4`, and every
branch on its side in one territory. Put `Q-z` and every branch on the other
side in the second territory. The second territory is a nonempty tree and has
credit `-1`; the first has credit `>2` by (20). Hence

`sigma(G)>2-1=1`.                                          (22)

The territories are induced and own each branch exactly once. This argument
does not drop the mixed `Q`--`K4` Sachs terms; it avoids them by an actual
vertex partition.

## 6. Complete canonical census

| kernel | canonical physical rows | certificate | rank-four balance |
|---|---:|---|---:|
| doubled triangle class `111` | `4` | angles (9), `e_B<221/100` | `<281/100` |
| doubled `C4` exceptional orbit: doubled pairs first-simple, connectors arbitrary in fixed parity (`4` anchors class `110`, `4` class `111`) | `8` parity anchors | one representative, genuine-automorphism transport, and connector monotonicity, angles (13), `e_B<9/4` | `<57/20` |
| all-odd `K4`, one long path | `6` edge orbits | angles (17), `e_B<12/5` | `<3` |
| all-odd `K4`, no long path | `1` | `K4 | Q` or `K4 | (Q-z)` | `>0` surplus |

The first three counts are labelled first-simple structural anchors after the
simplicity constraints. For doubled `C4`, the eight parity anchors form one
genuine-kernel-automorphism orbit, not one switching class. If both doubled
pairs retain first-simple lengths, connector paths may have arbitrary lengths
of their fixed parities: (14) and fixed-parity monotonicity cover them. If
either doubled pair is longer, the `1862/1000` or `1662/1000` descendant bound
applies. The no-long row is exactly the unsubdivided `K4`. Together these
alternatives are the complete rank-three payload needed for this hostile-cycle
packet.

## 7. Audit boundary

This note does not replace the nonstructural rank-three ledgers. The complete
rank-`3+1` block-type proof combines this packet with

- the 28 doubled-triangle DNN rows outside class `111`;
- all `28` doubled-`C4` odd--odd rows (uniform `e_B<229/150`), the `28`
  DNN rows in the old no-`OO` slice, the exceptional eight-anchor orbit with
  first-simple doubled pairs and arbitrary fixed-parity connectors, and the
  longer-doubled-path certificates for its remaining descendants (four anchors
  class `110`, four class `111`);
- the 56 non-all-odd `K4` rows; and
- the all-odd `K4` certificates with at least two long paths.

For any such row, block additivity must use its actual certified rank-three
excess and check (5); one cannot merely quote `s^+(B)>=|V(B)|`, because that
unquantified statement has no hostile-cycle reserve. The canonical rows above
pass the stronger exact check. No edge-addition monotonicity, switching of
physical lengths, numerical SDP evidence, or impossible tree-plus-hostile
margin is used.
