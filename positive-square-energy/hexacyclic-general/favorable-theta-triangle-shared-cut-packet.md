# Favorable theta plus a triangle at an arbitrary shared cut

## 1. The packet theorem

For a connected graph `X`, put

`sigma(X)=s+(X)-|V(X)|` and `D(X)=s+(X)-s-(X)`.

**Theorem 1 (attachment-uniform shared-cut packet).** Let `G` have exactly two
cyclic blocks. One is a theta `H` with terminals `x,y` and internally disjoint
paths `P_0,P_1,P_2`. Its two odd cycles are both of length `3 mod 4`. The other
cyclic block is a triangle `T`, and `H` and `T` meet in one cut vertex `w`,
which may be any vertex of `H`. Arbitrary finite rooted trees may be attached
at every vertex of the two blocks. Then

`D(G)>0` and consequently `sigma(G)>2`.                       (1)

In particular, the conclusion is uniform in the choice of the shared cut,
the sizes and shapes of all rooted trees, and whether `w` is a terminal or an
internal vertex of any theta path.

This is exactly the bridge-free packet needed in hexacyclic multiblock item 7.
It does not claim the same margin across a positive connector. That case is
separated at its first actual bridge in the item-7 owner argument.

## 2. Tree elimination and the rooted one-sum identity

For positive vertex activities `a=(a_v)`, write

`Z_J(a)=sum_M product_(v not covered by M) a_v`,               (2)

where the sum runs over the matchings of `J`. Orient every off-core tree edge
toward the core. Successive leaf elimination replaces the activity at a core
vertex by

`a_v=t+sum_(u branch-neighbor of v) 1/Q_(u->v)>=t>0`,          (3)

where `Q_(u->v)>0`, and extracts a common positive factor `K(t)`. The same
factor is restored when a core root is deleted, so it is common to every
grouped Sachs term. Positive factors do not affect phase. This is the exact
tree-elimination convention of
`bicyclic-theta/arbitrary-attached-theta-phase-note.md`, Section 1.

Let `Psi_X` denote the resulting normalized grouped Sachs polynomial of a
weighted core `X`; thus the actual normalized characteristic polynomial is a
positive multiple of `Psi_X`. If weighted graphs `X` and `Y` meet only in a
vertex `w`, partitioning a Sachs subgraph according to the block that supplies
the state at `w` gives the rooted one-sum identity

`Psi_(X vee_w Y)`
` =Psi_X Psi_(Y-w)+Psi_(X-w) Psi_Y`
`  -a_w Psi_(X-w) Psi_(Y-w)`.                                 (4)

There is no division in (4). For the zero-cycle terms it is the usual matching
partition at `w`. A cycle belongs wholly to one block, so the same partition
applies to every grouped cycle term. Thus (4) remains valid after arbitrary
rooted trees have been compressed by (3).

Let the two private vertices of `T` have activities `b,c`. Since a triangle is
`3 mod 4`,

`Psi_(T-w)=bc+1`,
`Psi_T=a_w(bc+1)+b+c-2i`.                                     (5)

Put

`d=bc+1>0` and `e=b+c>0`.

Applying (4) to `X=H` and (5) gives the exact formula

`Psi_G=d Psi_H+(e-2i)Psi_(H-w)`.                              (6)

Equation (6) is important: replacing it by a product of the theta and triangle
polynomials would count the shared root twice and is false.

## 3. Signs for the theta and the deleted-root state

Write

`Psi_H=R+iI` and `Psi_(H-w)=R_0+iI_0`.                         (7)

The arbitrary-attached-theta phase proof gives `R>0`. Because both odd theta
cycles are favorable, its zero-hostile branch gives

`I<0`.                                                         (8)

For completeness, the latter sign is also immediate from the grouped Sachs
expansion: the two odd cycles contribute `-2i` times strictly positive
matching partitions, the even cycle contributes only to the real part, and
two theta cycles cannot occur together.

We need the stronger rooted statement

`R_0>0` and `I_0<=0`.                                         (9)

There are three exhaustive positions for `w`.

1. If `w` is `x` or `y`, then `H-w` is a forest. Hence
   `Psi_(H-w)=Z_(H-w)>0`.
2. If `w` is internal to a path whose omission leaves one of the two odd
   cycles, then `H-w` is that favorable odd unicyclic graph with trees and
   path remnants attached. Its grouped expansion is
   `Z_(H-w)-2i Z_F`, where both matching partitions are positive. Thus
   `R_0>0` and `I_0<0`.
3. If `w` is internal to the path whose omission leaves the even cycle `C`,
   then `I_0=0`. If `|C|=2 mod 4`, its real cycle term is positive. If
   `|C|=0 mod 4`, then
   `R_0=Z_(H-w)-2Z_F>0`. To see the strict inequality, fix a matching of the
   forest `F` obtained after deleting `C`. Extend it in two disjoint ways by
   either perfect matching of the even cycle. These extensions preserve its
   complete uncovered-vertex monomial and inject two copies of `Match(F)` into
   `Match(H-w)`. The empty matching on `C`, together with the fixed forest
   matching, supplies an additional positive monomial. Coefficientwise,

   `Z_(H-w)>2Z_F`.                                             (10)

This proves (9). The injection in (10) remains valid with arbitrary positive
activities and arbitrary attached trees; it is not merely a bare-core count.

## 4. The phase branch and strict credit

Taking imaginary parts in (6)--(7) gives

`Im Psi_G=dI+eI_0-2R_0`.                                      (11)

By `d,e>0`, (8), and (9), every term on the right is nonpositive and the first
and last are strictly negative. Therefore

`Im Psi_G(t)<0` for every `t>0`.                               (12)

No assertion about the sign of `Re Psi_G` is needed. The normalized
characteristic curve never meets the real axis and tends to the positive real
axis as `t` tends to infinity. Its continuous eigenvalue argument is therefore
the unique branch

`Theta_G(t) in (-pi,0)`, `Theta_G(t)->0` as `t->infinity`.     (13)

In particular, there is no principal-argument reset if the real part changes
sign. The signed Coulson identity now yields

`D(G)=-(4/pi) integral_0^infinity t Theta_G(t) dt>0`.          (14)

The integrand is strictly positive for every `t>0`; convergence is the usual
finite-graph Coulson convergence. Since `G` is tricyclic, including all tree
attachments,

`|E(G)|=|V(G)|+2` and `s+(G)+s-(G)=2|E(G)|`.

Consequently

`sigma(G)=2+D(G)/2>2`,                                        (15)

which proves Theorem 1.

## 5. Exact dependency and hostile self-check

The only imported analytic input is the positive-real-part/tree-elimination
theorem for an arbitrary attached theta. Its exact continuant identities,
matching injections, low-length conventions, and phase ledger are checked by

```text
python3 positive-square-energy/experiments/arbitrary_attached_theta_phase_verifier.py
python3 -O positive-square-energy/experiments/arbitrary_attached_theta_phase_verifier.py
```

The rooted one-sum identity, all four root-position types, deleted-root signs,
and the full packet's negative imaginary part are checked independently with
exact multivariate polynomial arithmetic by

```text
python3 positive-square-energy/experiments/favorable_theta_triangle_shared_cut_verifier.py
python3 -O positive-square-energy/experiments/favorable_theta_triangle_shared_cut_verifier.py
```

That verifier also requires incorrect triangle-sign and duplicated-root
mutations to fail. It is corroborative: the proof for arbitrary lengths is the
matching argument in Sections 2--4, not a finite census.

The present favorable branch uses only the zero-hostile sign from that theorem;
it does not use its weaker universal bound
`D>=-4(sqrt(5)-2)`.

The proof was checked against the following failure modes.

1. **Arbitrary root.** Terminal roots, roots on either odd-cycle-omitting path,
   and roots on the even-cycle-omitting path are exactly the three cases in
   Section 3.
2. **The hostile even residue.** A `0 mod 4` even cycle contributes `-2`, not
   `+2`; the coefficient-preserving two-perfect-matching injection (10) is what
   keeps `R_0` strictly positive.
3. **Two-cycle Sachs terms.** A theta cycle disjoint from `w` can coexist with
   the external triangle. Those terms are retained by the product
   `(e-2i)Psi_(H-w)` in (6); dropping them would make the proof invalid.
4. **Shared-root accounting.** Formula (4) subtracts the duplicated unmatched
   root state. Neither `w` nor a tree rooted at `w` is counted twice.
5. **Phase branch.** Equation (12), not a claim that the real part stays
   positive, fixes the continuous branch in `(-pi,0)` and prevents a hidden
   winding or principal-argument jump.
6. **Strictness.** The term `dI` is already strict, and `-2R_0` is independently
   strict. No limiting attachment or equality case can turn (14) into a weak
   inequality.
7. **Scope.** A positive connector between the blocks is not silently absorbed
   into this packet. It must be cut as a separate owner territory, exactly as
   in hexacyclic item 7.

Thus the favorable-theta-plus-triangle packet used by item 7 has a direct,
attachment-uniform proof for every physical shared cut.
