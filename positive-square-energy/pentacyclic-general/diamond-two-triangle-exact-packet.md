# Exact attached `D+T+T` packet

For a graph `X` with adjacency eigenvalues `lambda_j`, put

```text
s^+(X)=sum_(lambda_j>0) lambda_j^2,
s^-(X)=sum_(lambda_j<0) lambda_j^2,
sigma(X)=s^+(X)-|V(X)|.
```

Let

```text
D=Theta(1,2,2)=K_4-e,       T=C_3.
```

## Theorem

Suppose that two triangular blocks are joined to `D` by shared cut vertices
in one bridge-free block-cut incidence tree.  They may be direct at arbitrary,
possibly equal, vertices of `D`, or one may be nested from a vertex of the
other.  Arbitrary finite rooted trees may be attached at every vertex.  Then

```text
sigma(D+T+T)>3.                                                (1)
```

This note supplies the exact algebra omitted by earlier invocations of the
favorable rank-four packet.  The scope is deliberately narrow: positive
bridge connectors are excluded and belong to the surrounding bridge split.
It proves only `D+T+T`; it says nothing about the open `D+T^3` packet.

## 1. Tree compression and the one-sum identity

For an unweighted graph `X`, normalize its imaginary-axis characteristic
polynomial by

```text
Psi_X(t)=i^(-|X|) det(itI-A(X))
        =product_j (t+i lambda_j).                             (2)
```

For a core with independent positive activities `z=(z_v)`, use the weighted
version

```text
Psi_X(z)=i^(-|X|) det(i diag(z)-A(X));
```

setting every `z_v=t` recovers (2).  Its grouped Sachs expansion has positive
matching weights, while a selected cycle `C` contributes
`-2 i^(-|C|)`.  This fixes all normalization and sign conventions below.

For a forest `F` define its positive weighted matching partition by

```text
Z_F(z)=sum_(M matching of F) product_(v uncovered by M) z_v.
```

When all activities equal `t`, this is
`Z_F(t)=sum_M t^(|V(F)|-2|M|)`.  Orient every off-core tree edge toward the
core.  For the subtree `T_(u->v)` below an oriented edge `u->v`, let

```text
Q_(u->v)=Z_(T_(u->v))/Z_(T_(u->v)-u).
```

If the children of `u` are `w`, splitting a matching according to whether `u`
is uncovered or is matched to one child gives

```text
Z_(T_(u->v))
 =t product_w Z_(T_(w->u))
  +sum_w Z_(T_(w->u)-w) product_(x!=w) Z_(T_(x->u)),
Z_(T_(u->v)-u)=product_w Z_(T_(w->u)).
```

Thus

```text
Q_(u->v)=t+sum_(w child of u) 1/Q_(w->u)>=t>0.
```

Eliminating every branch therefore replaces a core diagonal variable by

```text
z_v=t+sum_(u branch-neighbor of v) 1/Q_(u->v)>=t>0.            (3)
```

This extraction is literally common to every grouped Sachs term.  For each
branch rooted at `u`, extract `Z_(T_(u->v))>0`.  If its core root survives,
the alternative using edge `uv` contributes the ratio
`Z_(T_(u->v)-u)/Z_(T_(u->v))=1/Q_(u->v)` to (3).  If a selected core cycle
deletes the root, the branch is a whole disconnected tree and contributes the
already extracted `Z_(T_(u->v))`; no quotient remains.  Multiplying over all
branches gives one positive real factor `K(t)` common to every cycle carrier.
A rooted tree identified with a core vertex is handled by removing that root
and treating the resulting components as branches.  Thus the actual
normalized determinant equals `K(t)` times the weighted-core polynomial, so
`K(t)` is harmless for phase.  It suffices (and is stronger than necessary)
to prove the claims below for independent positive activities; realizable tree
messages satisfy the smaller domain `z_v>=t`.

If graphs `X,Y` meet in exactly one vertex `w`, their normalized determinant
satisfies the exact one-sum identity

```text
Psi_(X vee_w Y)
 =Psi_X Psi_(Y-w)+Psi_(X-w)Psi_Y
  -z_w Psi_(X-w)Psi_(Y-w).                                    (4)
```

Here is a direct derivation.  In a grouped Sachs subgraph, every cycle lies
wholly in `X` or wholly in `Y`, and at the shared vertex `w` there are three
exclusive states: `w` is left unmatched (weight `z_w`), `w` is occupied by a
nontrivial Sachs component of `X` (a matching edge or a selected cycle), or
`w` is occupied by a nontrivial Sachs component of `Y`.  The product
`Psi_X Psi_(Y-w)` contains the first and `X`-occupied states, while
`Psi_(X-w)Psi_Y` contains the first and `Y`-occupied states.  Their common
unmatched class is `z_w Psi_(X-w)Psi_(Y-w)` and has been counted twice;
subtracting it once proves (4).  Equivalently, this is the determinant
one-vertex-sum identity applied term by term to the grouped Sachs expansion.

For a triangle at `w` whose private vertices have activities `a,b`, put

```text
d=ab+1>0,        e=a+b>0.
```

Since

```text
Psi_(T-w)=d,
Psi_T=z_w d+e-2i,
```

equation (4) reduces to

```text
Psi_(X+T)=d Psi_X+(e-2i)Psi_(X-w).                             (5)
```

The subtraction in (4) is precisely what cancels the duplicate `z_w d` term;
a product of the two block polynomials would be false.

## 2. Exact diamond states

Label the diamond by the edge set

```text
pq, pr, qr, ps, qs,
```

so `r,s` are its two degree-two vertices.  Its grouped Sachs expansion is

```text
Psi_D=R+iI,
R=pqrs+pr+ps+qr+qs+rs>0,
I=-2(r+s)<0.                                                   (6)
```

The four deleted-root states are

```text
Psi_(D-p)=qrs+r+s,
Psi_(D-q)=prs+r+s,
Psi_(D-r)=pqs+p+q+s-2i,
Psi_(D-s)=pqr+p+q+r-2i.                                       (7)
```

Consequently, if

```text
Psi_(D-u)=R_u+iI_u,
```

then for every `u in V(D)`,

```text
R_u>0,        I_u<=0.                                         (8)
```

For distinct `u,v`, `D-{u,v}` is a forest and its matching state
`F_uv=Psi_(D-{u,v})` is strictly positive.  Explicitly, with the deleted pair shown, the six states are

```text
F_pq=rs,      F_pr=qs+1,    F_ps=qr+1,
F_qr=ps+1,    F_qs=pr+1,    F_rs=pq+1.                        (9)
```

All inequalities (6)--(9) are coefficientwise in arbitrary positive
activities, so they already include the rooted-tree messages (3).

## 3. Two direct triangles

Give triangle `j` private activities `a_j,b_j` and abbreviate

```text
d_j=a_j b_j+1,        e_j=a_j+b_j.
```

### Equal roots

If both triangles have root `u`, applying (5) twice gives

```text
Psi_G=d_1d_2 Psi_D
     +[d_2(e_1-2i)+d_1(e_2-2i)]Psi_(D-u).                     (10)
```

Taking imaginary parts and using (6), (8),

```text
Im Psi_G
 =d_1d_2 I+(d_2e_1+d_1e_2)I_u-2(d_1+d_2)R_u<0.              (11)
```

### Distinct roots

If the roots are distinct `u,v`, deletion of the second root from the first
one-sum leaves the corresponding deleted host state.  A second use of (5)
gives

```text
Psi_G=d_1d_2 Psi_D
     +d_2(e_1-2i)Psi_(D-u)+d_1(e_2-2i)Psi_(D-v)
     +(e_1-2i)(e_2-2i)F_uv.                                  (12)
```

Therefore

```text
Im Psi_G
 =d_1d_2 I+d_2(e_1I_u-2R_u)+d_1(e_2I_v-2R_v)
  -2(e_1+e_2)F_uv<0.                                         (13)
```

There are four equal-root and six unordered distinct-root records.  Equations
(10)--(13) cover all ten direct/direct incidences, including repeated owners.

## 4. Nested triangles

Attach the first triangle at `u`, with private activities `a,b`, and attach the
second at its private vertex `a`, with private activities `c,d`.  Put

```text
d_1=ab+1, e_1=a+b, d_2=cd+1, e_2=c+d.
```

Deleting `a` from the first attachment leaves the pendant edge `ub`, hence

```text
Psi_((D+T_1)-a)=b Psi_D+Psi_(D-u).                             (14)
```

Equations (5) and (14) give

```text
Psi_G=[d_1d_2+b(e_2-2i)]Psi_D
     +[d_2(e_1-2i)+(e_2-2i)]Psi_(D-u),                        (15)
```

and thus

```text
Im Psi_G
 =(d_1d_2+be_2)I-2bR+(d_2e_1+e_2)I_u-2(d_2+1)R_u<0.         (16)
```

If the second triangle is rooted at `b` instead, delete `b`: the coefficient
`b` in (14)--(16) is replaced by `a`, and the same strict sign proof follows.
Thus the eight marked private-child positions reduce, by swapping the names
`a,b` together with their independent activities and rooted branches, to the
four labelled representatives checked here.  If the second triangle uses the
entry cut `u` of the upstream triangle, all three block nodes meet the same cut
node; this is repeated-owner direct/direct incidence, not a new nested chain.
Hence the genuinely nested case uses one of the two private vertices, which
are exchanged by the rooted-triangle reflection.  The four labelled choices
of `u`, together with the direct records above, exhaust a bridge-free
block-cut tree with root block `D` and two external block nodes: the nodes are
either both children of `D`, or one is the child of the other.

For completeness, the ten direct records are the unordered owner multisets
from the four labelled vertices: four repeated-owner and six distinct-owner
records.  The diamond automorphism group exchanges `p,q` and independently
exchanges `r,s`, so these ten collapse to five bare-core orbits; the four
nested owners collapse to two.  We nevertheless check all four labelled
vertices and all ten multisets.  This is the safe convention when rooted-tree
activities break the bare-core symmetries.

## 5. Continuous phase and square energy

A warning about signs is essential.  The positive real quantities used above
are the host state `R`, the deleted-host states `R_u`, and the two-deletion
forest states `F_uv`.  They are exactly the ingredients needed to make the
*imaginary* part after the second attachment strict.  The resulting full
polynomial need not have positive real part; no such extra assertion is used.

Equations (11), (13), and (16) prove

```text
Im Psi_G(t)<0 for every t>0.                                  (17)
```

The positive tree factors removed in Section 1 do not alter this sign.  Since
the normalized characteristic curve never meets the real axis and tends to
the positive real axis as `t` tends to infinity, its continuous eigenvalue
argument is the unique branch

```text
Theta_G(t) in (-pi,0),        Theta_G(t)->0.                   (18)
```

There is no principal-argument reset when the real part changes sign.  In
fact, the full packet's real part need not be positive even on realizable
activities: with no attached trees all activities equal `t`, and for direct
roots `r,s` one obtains
`Re Psi_G=t^8+11t^6+31t^4+9t^2-12`, which is negative for sufficiently
small `t>0`.  The proof neither needs nor claims `Re Psi_G>0`.  The strict
lower-half-plane statement is exactly what fixes the continuous branch.

For completeness, the signed Coulson identity follows with this normalization,
rather than being an additional convention.  From (2), choose each scalar
factor argument in `(-pi/2,pi/2)` and sum:

```text
Theta_*(t)=sum_j atan(lambda_j/t).
```

This is a continuous argument of `Psi_G` tending to zero at infinity.  Hence
it equals the branch in (18): two continuous lifts of the same circle-valued
map differ by a constant multiple of `2pi`, and their common limit makes that
constant zero.  Since `sum_j lambda_j=tr A=0`, integration by parts has
vanishing boundary terms and gives

```text
integral_0^infinity t Theta_G(t) dt
 =-(pi/4) sum_j sign(lambda_j) lambda_j^2.
```

Indeed, `Theta'_G(t)=-sum_j lambda_j/(t^2+lambda_j^2)` and
`Theta_G(t)=O(t^(-3))` at infinity after the trace term cancels, while
`Theta_G(t)` is bounded at zero and hence `t^2 Theta_G(t)->0`.  After integration by parts, use

```text
sum_j lambda_j t^2/(t^2+lambda_j^2)
 =-sum_j lambda_j^3/(t^2+lambda_j^2)
```

and `integral_0^infinity dt/(t^2+lambda^2)=pi/(2|lambda|)` for
`lambda!=0`.  Zero eigenvalues contribute zero.  Thus

```text
Delta(G)=s^+(G)-s^-(G)
        =-(4/pi) integral_0^infinity t Theta_G(t) dt>0.        (19)
```

The packet is tetracyclic, also after arbitrary tree attachments, so
`|E(G)|=|V(G)|+3` and

```text
s^+(G)+s^-(G)=2|E(G)|.
```

Combining this with (19) proves

```text
sigma(G)=s^+(G)-|V(G)|=3+Delta(G)/2>3,
```

which is (1).

## 6. Semantic verifier

Run

```text
python3 research/diamond-two-triangle-packet-verifier.py
python3 -O research/diamond-two-triangle-packet-verifier.py
```

The standard-library verifier independently regenerates the Sachs polynomial
for all 10 direct and 4 normalized nested records.  It compares the displayed
one-sum/direct/nested formulas with those full weighted core polynomials,
locks the explicit diamond/deleted-diamond states (6)--(9), derives the core
rank from the realized graphs, checks coefficientwise strict negativity of the
imaginary parts, and retains the explicit negative-real direct-`r,s`
specialization as a regression.  It rejects hostile one-sum, triangle-sign,
cross-term, pendant, incidence, owner, strictness, host-sign,
full-real-positivity, rank, and diamond-edge mutations, and requires identical
normal/optimized output.

The executable is a finite weighted-core certificate, not a replacement for
the whole theorem proof.  The arbitrary-tree factorization, the reflection
transport from the four normalized nested records to the other four marked
private-child positions, the continuous phase lift, and the signed Coulson
integration are the mathematical arguments in Sections 1, 4, and 5.  A
transitive dependency gate must therefore lock this theorem note separately
from the child executable and must not describe the executable alone as an
end-to-end proof of arbitrary attachments or square energy.
