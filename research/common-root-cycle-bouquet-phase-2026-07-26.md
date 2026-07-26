# Common-root cycle bouquets: exact root states and residue phase bounds

## Scope

Let `G` be a connected cactus with cyclic blocks

`C_{ell_1},...,C_{ell_r}`

all meeting in one common cut vertex `o`, and with no other intersections
between cyclic blocks. Allow an arbitrary tree at every vertex of this cyclic
core. The result below applies when

`ell_j != 0 mod 4` for every `j`.                                     (1)

Thus odd lobes of both residues and lobes of length `2 mod 4` are allowed.
There is deliberately no assertion for a bouquet containing a cycle of length
`0 mod 4`: its Sachs contribution has negative real sign and destroys the
positive-real-part argument used here.

Write

`D(H)=s^+(H)-s^-(H)`

and, for odd `ell`, put

`vartheta_ell(t)=atan(2/Z_{C_ell}(t)),  t>0`,                    (2)

where `Z_{C_ell}(t)` is the signless matching partition of the bare cycle.

## Theorem

Under (1), the continuous imaginary-axis phase

`Theta_G(t)=Arg(i^(-n) phi_G(it))`, `Theta_G(t)->0` as `t->infinity`,

satisfies the pointwise two-sided bound

`-sum_(ell_j=3 mod 4) vartheta_{ell_j}(t)`
`    <= Theta_G(t)`
`    <= sum_(ell_j=1 mod 4) vartheta_{ell_j}(t)`.                (3)

Consequently,

`sum_(ell_j=1 mod 4) D(C_{ell_j}) <= D(G)`
`    <= sum_(ell_j=3 mod 4) D(C_{ell_j}).`                       (4)

In particular, since a bouquet with `r` cyclic blocks has `m=n-1+r`,

`s^+(G) >= n+r-1-sum_(ell_j=1 mod 4) delta_{ell_j}`,            (5)

where

`delta_ell=sec(pi/ell)-1`,
`D(C_ell)=-2 delta_ell` for `ell=1 mod 4`.                       (6)

The sums in (3)--(5) are empty when the indicated residue does not occur.
Lengths `2 mod 4` improve the real carrier but contribute no phase term.

## 1. Exact elimination of arbitrary attached trees

Every component outside the cyclic core has a unique core neighbor: two such
neighbors, together with the path between them through the component and the
connected core, would create another cyclic block. Thus the entire off-core
forest splits canonically into rooted branches. For a forest `F`, define

`Z_F(t)=sum_M t^(|V(F)|-2|M|)`,                                 (7)

the sum being over all matchings. Orient each off-core branch toward its core
vertex. For an oriented edge `u->p`, let `T_{u->p}` be the subtree below `u`
and set

`q_{u->p}=Z_{T_{u->p}}(t)/Z_{T_{u->p}-u}(t)`.                  (8)

Splitting according to the status of `u` gives the exact recursion

`q_{u->p}=t+sum_(w child of u) 1/q_{w->u} >= t`.                (9)

After all off-core vertices are eliminated, every core vertex `v` has the
effective activity

`a_v=t+sum_(u attached at v) 1/q_{u->v} >= t`,                 (10)

and all terms have the same positive real prefactor

`K_tree=prod_(u adjacent to the core) Z_{T_{u->v}}(t)>0`.       (11)

This factor is also common to every Sachs cycle carrier. If a selected cycle
deletes its core root, a branch at that root contributes its full partition
already extracted in (11); branches at surviving roots are absorbed through
(10). Hence no quotient depending on the selected lobe remains. This is why
the reduction covers arbitrary rooted trees, not only leaves or stars.

## 2. The two exact states of a lobe

Fix lobe `j` and list its `ell_j-1` nonroot activities consecutively as
`x_{j,1},...,x_{j,ell_j-1}`. For the path continuant

`K()=1`, `K(x_1)=x_1`,
`K(x_1,...,x_k)=x_k K(x_1,...,x_{k-1})+K(x_1,...,x_{k-2})`,     (12)

define

`A_j=K(x_{j,1},...,x_{j,ell_j-1})`,                            (13)

`B_j=K(x_{j,2},...,x_{j,ell_j-1})`
`    +K(x_{j,1},...,x_{j,ell_j-2})`.                           (14)

These are the exact two root-boundary states:

- `A_j`: the common root is unavailable to the lobe, so the nonroot path is
  matched internally;
- `B_j`: the root is matched through one of the two incident lobe edges, with
  the two endpoint choices summed.

Let `a=a_o`. A core matching either leaves `o` unmatched or matches it into
exactly one lobe. Therefore its matching carrier is exactly

`Z_core=(prod_j A_j)(a+sum_j B_j/A_j)`.                         (15)

There is a third Sachs status, selection of the whole cycle. Since all cycles
contain `o`, at most one cycle can be selected. Selecting lobe `j` deletes its
vertices and leaves state `A_k` on every other lobe, so its carrier is

`prod_(k!=j) A_k`.                                              (16)

Equations (15) and (16) are the complete root-state derivation; there are no
multi-cycle terms.

## 3. Exact normalized Sachs carrier

A cycle of length `ell` has multiplier

`-2 i^(-ell) = +2i, -2, -2i, +2`

for `ell=1,0,3,2 mod 4`, respectively. Combining this sign table with
(15)--(16), and dividing only by the positive factor
`K_tree prod_j A_j`, gives

`Psi_G/(K_tree prod_j A_j)=X+iY`,                               (17)

where, under (1),

`X=a+sum_j B_j/A_j+2 sum_(ell_j=2 mod 4) 1/A_j >0`,             (18)

`Y=2 sum_(ell_j=1 mod 4) 1/A_j`
`  -2 sum_(ell_j=3 mod 4) 1/A_j`.                              (19)

Thus `Theta_G=atan(Y/X)` lies continuously in `(-pi/2,pi/2)` and tends to
zero at infinity. Formula (18) also pinpoints the obstruction at residue zero:
a `0 mod 4` lobe would contribute `-2/A_j` to `X`. Positivity of `X` would no
longer follow, so neither (3) nor its proof extends to that case.

## 4. Residue phase comparison

For an odd lobe `j`, its weighted isolated-cycle matching partition, using the
same effective activities, is

`c_j=a A_j+B_j`.                                                (20)

Set `p_j=2/A_j` and `b_j=B_j/A_j`. From (18),

`X>=a+b_j` for every odd `j`.                                  (21)

If `Y>0`, then

`tan Theta_G=Y/X`
` <= sum_(ell_j=1 mod 4) p_j/X`
` <= sum_(ell_j=1 mod 4) p_j/(a+b_j)`
` = sum_(ell_j=1 mod 4) 2/c_j`.                                (22)

If `Y<=0`, the desired upper bound is immediate. Applying the elementary
subadditivity

`atan(u_1+...+u_k)<=atan(u_1)+...+atan(u_k)`, `u_j>=0`,         (23)

to (22) yields

`Theta_G<=sum_(ell_j=1 mod 4) atan(2/c_j)`.                     (24)

The matching polynomial has nonnegative coefficients and every effective
activity is at least `t`, so

`c_j>=Z_{C_{ell_j}}(t)`.                                       (25)

Equations (24)--(25) prove the upper half of (3). Replacing `Y` by `-Y` and
using the `3 mod 4` lobes proves the lower half in exactly the same way.

Finally, the signed Coulson identity

`D(G)=-(4/pi) integral_0^infinity t Theta_G(t) dt`              (26)

turns (3) into (4). The standard cycle evaluation (6), together with
`s^+(G)+s^-(G)=2m=2(n-1+r)`, gives (5).

## 5. Application: the common-root `C3355` bouquet

Take two triangle lobes and two pentagon lobes, all through `o`, with arbitrary
trees attached anywhere. Here `r=4`, and only the two pentagons occur in the
upper phase sum. Since

`delta_5=sec(pi/5)-1=sqrt(5)-2`,                               (27)

(5) gives

`s^+(G) >= n+3-2(sqrt(5)-2)`
`         = n+7-2sqrt(5) > n`.                                 (28)

Equivalently, `D(G)>=2D(C_5)=8-4sqrt(5)`. This proves the
four-cycle bouquet case directly and remains valid for every attached tree.
It does not rely on an induced-packet partition of the core.

## 6. Application: the common-root `C333q` bouquet

Take three triangle lobes and one `C_q` lobe through `o`, again with arbitrary
trees. The theorem gives the following cases:

- If `q=1 mod 4`, then only `C_q` occurs in the upper phase sum, and

  `s^+(G) >= n+3-delta_q=n+4-sec(pi/q)>n`.                      (29)

- If `q=2 mod 4`, the long lobe contributes only the positive real term
  `2/A_q`; hence `Theta_G<=0`, `D(G)>=0`, and

  `s^+(G)>=n+3`.                                                (30)

- If `q=3 mod 4`, every odd lobe has negative Sachs phase; again
  `Theta_G<=0`, `D(G)>=0`, and `s^+(G)>=n+3`.                   (31)

There is no conclusion here for `q=0 mod 4`. In that residue the long cycle
contributes `-2/A_q` to the real carrier, and a separate argument would be
required. In particular, (29)--(31) must not be quoted as an all-`q` theorem.

## Conclusion

The common-root geometry makes the full Sachs expansion a one-root,
three-state calculation: root unmatched, root matched into one lobe, or one
whole lobe selected as a cycle. After exact tree elimination this yields
(17)--(19), and positivity of the real carrier for residues `1,2,3 mod 4`
reduces the bouquet phase to the sum of the adverse `1 mod 4` isolated-cycle
phases. The resulting bound is uniform in the number and lengths of lobes and
in all attached trees, but intentionally excludes every `0 mod 4` lobe.
