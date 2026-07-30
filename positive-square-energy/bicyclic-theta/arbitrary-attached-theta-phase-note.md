# Arbitrary attached theta: continuant phase reduction

## Status

This research proof note proves the arbitrary-attached-theta theorem.  The
proof is analytic and exact.  Its finite verifier checks the canonical packet
identities and ledger but is supporting only; no finite path-length census is
used for completeness.

## 1. Tree elimination and normalization

Let `G` be a finite simple connected graph whose 2-core is a theta `H` with
terminals `x,y` and internally disjoint `x-y` paths `P_0,P_1,P_2`.  Write
`ell_j=|E(P_j)|`.  Every component outside `H` is a rooted tree meeting `H` in
one vertex.

For a graph with positive vertex activities `a=(a_v)`, put

```text
Z_J(a)=sum_M product_(v not covered by M) a_v,
```

where the sum is over matchings of `J`.  Thus the bare signless matching
polynomial is `Z_J(t)=Z_J(a_v=t)`.

Orient every branch edge toward the core.  The standard leaf recurrence gives

```text
Q_(u->v)=t+sum_(w child of u) 1/Q_(w->u) > 0,
a_v=t+sum_(u branch-neighbor of v) 1/Q_(u->v) >= t.             (1)
```

Extracting the full branch partitions gives one common factor `K(t)>0`.
The factor is still common in a Sachs term in which core vertices are deleted:
if a core root is deleted, its former branches become whole tree components
and restore exactly the factors extracted in (1).  Hence no cycle-deletion
term carries a hidden quotient.

Normalize

```text
Psi_G(t)=i^(-|G|) det(it I-A(G)).
```

The three theta cycles meet at `x,y`, so no two can occur in one Sachs
subgraph.  A cycle of length `1 mod 4` contributes `+2i`, a cycle of length
`3 mod 4` contributes `-2i`, and an even cycle contributes `+2` in residue
`2 mod 4` and `-2` in residue `0 mod 4`.

A nonbipartite theta has exactly two odd cycles and one even cycle.  Label the
paths so that

```text
C_1=P_0 union P_1,   C_2=P_0 union P_2,   C_e=P_1 union P_2.   (2)
```

Let

```text
d_j=Z_(P_j-{x,y})(a),
epsilon=+1 if |C_e|=2 mod 4, and epsilon=-1 if |C_e|=0 mod 4.
```

The exact grouped Sachs expansion is

```text
Psi_G/K = R + 2i(sigma_1 d_2+sigma_2 d_1),                    (3)
R=Z_H(a)+2 epsilon d_0,                                       (4)
```

where `sigma_j=+1` for a hostile cycle (`|C_j|=1 mod 4`) and
`sigma_j=-1` for a favorable cycle (`|C_j|=3 mod 4`).

The terminal Schur reduction by the path continuant recurrence has the form

```text
Psi_G/K = W=pq-(u+iv)^2,
Re W=pq-u^2+v^2>0.                                            (5)
```

Here is a direct matching proof of the strict sign, so (5) is not being used
as a spectral branch assertion.  Eliminate path interiors successively with

```text
K()=1,  K(c_1)=c_1,
K(c_1,...,c_r)=c_r K(c_1,...,c_(r-1))+K(c_1,...,c_(r-2)).      (6)
```

Every denominator is a positive continuant.  The useful determinant identity
(for at least two listed variables)

```text
K(c_1,...,c_r)K(c_2,...,c_(r-1))
 -K(c_1,...,c_(r-1))K(c_2,...,c_r)=(-1)^r                    (7)
```

is obtained by induction from (6).  More directly, apply the omitted-path
packet (9) below to the even cycle `C_e`.  It gives

```text
Z_H(a)=z_e d_0+E_e,   E_e>=0,   z_e=Z_(C_e)(a|C_e).            (7a)
```

Every activity on `C_e` is at least `t`.  An even cycle has two perfect
matchings, and the all-unmatched matching has positive weight, so
`z_e>Z_(C_e)(0)=2`.  Equations (4) and (7a) now give

```text
R=(z_e+2)d_0+E_e>0                  if epsilon=+1,
R=(z_e-2)d_0+E_e>0                  if epsilon=-1.              (7b)
```

Thus `Re W=R>0` in every channel.  Identity (7) is the continuant determinant
behind both the terminal Schur form (5) and the four endpoint packets below;
(7a)-(7b) give the sign without suppressing an alternating transfer term.  In
particular the continuous argument tending to zero at infinity is always the
principal argument in `(-pi/2,pi/2)`.

## 2. The exact omitted-path packet

The algebra needed below can be stated without suppressing any coefficient.
Let `C` be either odd cycle and let the omitted path be

```text
Q: x=v_0,v_1,...,v_(r-1),v_r=y.
```

Put `c_i=a_(v_i)`.  Partition a matching according to use of the first and
last edges of `Q`.  Define

```text
D_Q=K(c_1,...,c_(r-1)),
L_Q=0                              if r=1,
    =K(c_2,...,c_(r-1))           if r>=2,
R_Q=0                              if r=1,
    =K(c_1,...,c_(r-2))           if r>=2,
M_Q=1                              if r=1,
    =0                              if r=2,
    =K(c_2,...,c_(r-2))           if r>=3.                     (8)
```

Empty continuants in (8) are `1`.  All displayed packets are nonnegative and
every nonzero packet is strictly positive.  If

```text
z_C=Z_C(a|C),  z_C^x=Z_(C-x)(a),
z_C^y=Z_(C-y)(a),  z_C^(xy)=Z_(C-{x,y})(a),
```

then the four disjoint endpoint states give the exact identity

```text
Z_H(a)=z_C D_Q+z_C^x L_Q+z_C^y R_Q+z_C^(xy) M_Q.              (9)
```

This includes a direct omitted edge (`r=1`) and a two-edge omitted path
(`r=2`); these are precisely the reasons for the separate definitions in
(8).  Formula (9), not informal coefficient monotonicity, is the path packet
factorization used below.

The weighted cycle comparator is `z_C`.  Restoring the tree elimination does
not alter it: the actual isolated-cycle carrier is

```text
K_C(t)(z_C+2i sigma_C),   K_C(t)>0.
```

Moreover, every core activity in `z_C` satisfies `a_v>=t`, and `Z_C(a)` is a
polynomial with nonnegative coefficients in those activities.  Therefore

```text
z_C >= Z_C(t).                                                  (10)
```

This proves the weighted-to-bare phase comparison, with all positive branch
factors restored:

```text
0<Arg(z_C+2i)<=Arg(Z_C(t)+2i)                                  (11)
```

for a hostile cycle.  Notice that (10) compares an isolated weighted cycle,
not the attached theta with its bare theta; the latter comparison is false.

## 3. Zero hostile cycles

If both odd cycles are favorable, (3) gives

```text
Im W=-2(d_1+d_2)<0.
```

Together with `Re W>0`, this proves

```text
Arg W<0.                                                       (12)
```

Thus the zero-hostile channel is proved for both residues of the even cycle.

## 4. One hostile and one favorable

Suppose `C_1` is hostile and `C_2` favorable.  Set

```text
B=d_2=Z_(H-V(C_1))(a),   A=d_1=Z_(H-V(C_2))(a),
Z_q=Z_(C_q)(t),          q=|C_1|.
```

Take `C=C_1` and `Q=P_2` in (9).  Since deletion of the even cycle leaves the
interior of `P_0`, equations (4) and (9) give the exact algebraic difference

```text
R-Z_q(B-A)
 =(z_C1-Z_q)B+Z_q A
   +z_C1^x L_(P2)+z_C1^y R_(P2)+z_C1^(xy) M_(P2)
   +2 epsilon d_0.                                             (13)
```

This is the required factorization; no coefficient is switched according to
the sign of `B-A`.

If `epsilon=+1`, every summand on the right of (13) is nonnegative and
`Z_q A>0`.  Hence `R>Z_q(B-A)`.  If `B-A<=0`, then `Arg W<=0`; if `B-A>0`,
division by `RZ_q>0` gives

```text
Arg W=atan(2(B-A)/R)<atan(2/Z_q),                               (14)
```

which is the bare hostile phase.

It remains to treat `epsilon=-1`.  The following canonical injection lemma is
the needed exact statement.  It is recorded with its proof because replacing
the negative even-cycle coefficient by a positive one would be invalid.

**Lemma 4.1 (one-hostile monotone packet).**  Suppose
`|C_1|=1 mod 4`, `|C_2|=3 mod 4`, and `|C_e|=0 mod 4`.  For fixed `t>0`, let
`Z_q=Z_(C_1)(t)` and define

```text
F(a)=Z_H(a)-2d_0-Z_q(B-A).                                    (15)
```

On the orthant `a_v>=t`,

```text
F(a)>=F(t)>0.                                                   (16)
```

**Proof.**  Write `I_j=V(P_j)-{x,y}`.  Differentiating a matching partition
with respect to the activity at `v` simply deletes `v`.  Thus (15) gives

```text
v=x or y:  partial_v F=Z_(H-v),
v in I_1:  partial_v F=Z_(H-v)+Z_q Z_(I_1-v),
v in I_2:  partial_v F=Z_(H-v)-Z_q Z_(I_2-v),
v in I_0:  partial_v F=Z_(H-v)-2Z_(I_0-v).                     (17)
```

Here `I_j-v` may have two path components, and its `Z` is the product of their
matching partitions.  For `v in I_2`, unite a matching of `C_1` with a
matching of `I_2-v`, using no boundary edge from an `I_2-v` component to a
terminal.  The two vertex sets partition `V(H-v)`, so the union preserves the
complete uncovered-vertex monomial.  Restriction to the two sets is its
inverse.  Consequently, coefficientwise,

```text
Z_(H-v)(a)>=Z_(C_1)(a|C_1) Z_(I_2-v)(a)
            >=Z_q Z_(I_2-v)(a),                               (18)
```

where the last inequality uses `a_u>=t` for every cycle vertex.  The same
no-boundary-edge injection, from matchings of `C_e` and `I_0-v` into matchings
of `H-v`, gives

```text
Z_(H-v)(a)>=Z_(C_e)(a|C_e) Z_(I_0-v)(a).                       (19)
```

The even cycle has two perfect matchings of weight `1`, and its empty matching
has positive weight.  Hence `Z_(C_e)(a|C_e)>2`.  Equations (17)--(19) show that
every coordinate derivative of `F` is nonnegative; the terminal, `I_1`, and
`I_0` derivatives are strictly positive.  Increasing the coordinates one at
a time from `t` to `a_v` proves `F(a)>=F(t)`.

For strict bare positivity put

```text
a=ell_0,   b=ell_1,   c=ell_2,
K_r=K(t,...,t) (r entries),   K_(-1)=0,   K_0=1.
```

The three residues force `a` even and `b,c` odd, and

```text
Z_q=Z_(C_(a+b))(t)=K_(a+b)+K_(a+b-2).                          (20)
```

We first prove coefficientwise that

```text
(K_(a+b)+K_(a+b-2))K_(b-1)>=2K_(a-1).                         (21)
```

Index `P_0` as `x=u_0,u_1,...,u_a=y`, index `P_1` as
`x=w_0,w_1,...,w_b=y`, and let `J=z_1...z_(b-1)` be a separate path.
For each matching `M` of `u_1...u_(a-1)`, define two pairs in
`Match(C_(a+b)) x Match(J)`.  In both pairs, match `J` perfectly by
`z_1z_2,z_3z_4,...,z_(b-2)z_(b-1)`.

For `iota_0`, retain `M` and add the unique perfect matching of the path
`y,w_(b-1),...,w_1,x`.  For `iota_1`, replace every edge `u_i u_(i+1)` of
`M` by `u_(i+1)u_(i+2)`, and add the unique perfect matching of the path
`w_(b-1),...,w_1,x,u_1`.  Both complementary paths have the even order `b+1`.
Together with the perfect matching of `J`, each map adds exactly `b` edges,
so it preserves the number of uncovered vertices and therefore the power of
`t`.  Restriction recovers `M` in the first image, and restriction followed by
a one-step reverse shift recovers it in the second.  The images are disjoint:
every `iota_1` image contains `xu_1`, while no `iota_0` image does.  This proves
(21).  It also covers `b=1`: `J` is empty, the first complementary perfect
matching is the direct edge `xy=P_1`, and the second is `xu_1`.

Apply the exact omitted-path formula (9) to `C_1` with omitted path `P_2`.
Deleting one terminal from the bare cycle leaves a path on `a+b-1` vertices;
deleting both leaves the disjoint interiors of `P_0` and `P_1`.  After the
`Z_qK_(c-1)` terms cancel in (15), formula (9) gives, for the direct omitted
edge `c=1`,

```text
F(t)=Z_qK_(b-1)-2K_(a-1)+K_(a-1)K_(b-1),                      (22)
```

and, for `c>=3`,

```text
F(t)=Z_qK_(b-1)-2K_(a-1)
     +2K_(a+b-1)K_(c-2)+K_(a-1)K_(b-1)K_(c-3).                (23)
```

These exhaust the cases because `c` is odd.  The first difference in (22)
and (23) is nonnegative by (21), and the remaining terms are strictly positive
for `t>0`.  Simplicity only rules out the simultaneous subcase `b=c=1`, which
would repeat the edge `xy`; the separate `b=1` and `c=1` arguments above need
no further exception.  Thus `F(t)>0`, proving (16).  QED.

By (15)--(16), `R>Z_q(B-A)`, so the sign split and arctangent argument
used for (14) applies unchanged.  Thus every one-hostile channel satisfies

```text
Arg W<Arg(Z_(C_q)(t)+2i).                                      (24)
```

## 5. Two hostile cycles

Suppose both `C_1,C_2` are hostile.  Write `z_j=z_(C_j)` and `B_1=d_2`,
`B_2=d_1`.  Applying (9) with the other path omitted gives, exactly,

```text
R=z_j B_j+E_j,
E_j=z_Cj^x L_Q+z_Cj^y R_Q+z_Cj^(xy)M_Q+2 epsilon d_0.          (25)
```

For `epsilon=+1`, (25) is a positive path-packet factorization, so

```text
2B_j/R <= 2/z_j.                                               (26)
```

Put

```text
Theta=Arg W=atan(2(B_1+B_2)/R),
theta_j=Arg(z_j+2i)=atan(2/z_j).
```

If `theta_1+theta_2<pi/2`, then

```text
tan(theta_1+theta_2)
 =(2/z_1+2/z_2)/(1-4/(z_1z_2))
 >=2/z_1+2/z_2
 >=2(B_1+B_2)/R.
```

Monotonicity of `atan` proves `Theta<=theta_1+theta_2`.  If the sum equals or
exceeds `pi/2`, the conclusion follows directly from `0<Theta<pi/2`.
This also settles the product-comparator branch issue: the continuous argument
of

```text
(z_1+2i)(z_2+2i)=(z_1z_2-4)+2i(z_1+z_2)
```

is `theta_1+theta_2 in (0,pi)`.  When the real part crosses zero the argument
passes continuously through `pi/2`; there is no principal-argument reset.
Combining this fact with (11) yields

```text
Arg W<=theta_1+theta_2
     <=Arg(Z_(C_1)(t)+2i)+Arg(Z_(C_2)(t)+2i).                  (27)
```

For `epsilon=-1`, the residues force `P_1,P_2` even and `P_0` odd.  In
particular each omitted path `Q` in (25) has even length at least two.  Its
left and right continuants contain their perfect-matching monomial, so

```text
L_Q>=1,   R_Q>=1.                                               (28)
```

There are coefficient-preserving injections

```text
iota_x: Match(P_0-{x,y}) -> Match(C_j-x),
iota_y: Match(P_0-{x,y}) -> Match(C_j-y).                       (29)
```

For `iota_x`, keep the matching on the interior of `P_0` and add the unique
perfect matching of the even path `P_j-x`; for `iota_y`, use the reflected
perfect matching of `P_j-y`.  These edge sets are disjoint, cover the remaining
endpoint, and preserve exactly the uncovered vertices and hence every
activity monomial.  Therefore the four endpoint states in (25) factor as

```text
E_j=E_(j,x)+E_(j,y)+z_Cj^(xy)M_Q,
E_(j,x)=(z_Cj^x-d_0)L_Q+d_0(L_Q-1),
E_(j,y)=(z_Cj^y-d_0)R_Q+d_0(R_Q-1).                            (30)
```

All five terms on the right of (30) have nonnegative coefficients.  This is
the promised explicit `E_1,E_2` four-state factorization and proves `E_j>=0`.
It includes an edge `P_0` (`d_0=1`) and an omitted path of length two
(`L_Q=R_Q=1`, `M_Q=0`) without an empty-state ambiguity.  Consequently (26)
and the branch argument proving (27) also hold for `epsilon=-1`.

## 6. Integration

Let

```text
delta=sec(pi/5)-1=sqrt(5)-2.
```

For a hostile odd cycle `C_q`, `q=1 mod 4`, the bare spectrum gives

```text
D(C_q)=s+(C_q)-s-(C_q)=-2(sec(pi/q)-1)
```

and the signed Coulson identity gives

```text
integral_0^infinity t Arg(Z_(C_q)(t)+2i) dt
  =(pi/2)(sec(pi/q)-1).                                       (31)
```

The quantity `sec(pi/q)-1` decreases for `q>=5`, and is at most `delta`.
Consequently (12), (24), and (27) imply

```text
D(G)=-(4/pi) integral_0^infinity t Arg W(t) dt
     >=-4delta>-2.                                             (32)
```

There are at most two hostile cycles; favorable or negative phases only
improve (32).  Finally a bicyclic graph has `m=n+1`, so

```text
s+(G)+s-(G)=2m=2n+2,
s+(G)=n+1+D(G)/2 >= n+1-2delta > n.                            (33)
```

because `2delta=2sqrt(5)-4<1` (equivalently `sqrt(5)<5/2`).

## 7. Bipartite theta cores and the theorem

If the theta core is bipartite, then every attached tree preserves the same
bipartition.  Hence `G` is bipartite, its spectrum is symmetric, and

```text
s+(G)=s-(G)=|E(G)|.
```

Attaching a tree by one root identification adds equally many vertices and
edges.  Since a theta has two more edges than a tree, every graph considered
here has `|E(G)|=|V(G)|+1`.  Thus in the bipartite case
`s+(G)=|V(G)|+1>|V(G)|`.

Combining this observation with (33) proves the result.

**Theorem 7.1 (arbitrary attached theta).**  Let `G` be a finite simple
connected graph whose 2-core is a theta graph, and attach arbitrary finite
rooted trees at arbitrary core vertices.  Then

```text
s+(G)>|V(G)|.
```

The strict quantitative nonbipartite estimate is
`D(G)>=-4(sqrt(5)-2)>-2`; the bipartite estimate is
`s+(G)=|V(G)|+1`.

## 8. Supporting exact verifier

Run from `positive-square-energy/`:

```text
python3 experiments/arbitrary_attached_theta_phase_verifier.py
python3 -O experiments/arbitrary_attached_theta_phase_verifier.py
```

The program constructs matching partitions from edge lists, checks the
four-state identity (9), the low-length conventions in (8), the bare injection
(21), the bare specializations (22)--(23), both `E_j` identities (30), and the
phase ledger.  It then applies
hostile mutations to signs, endpoint packets, low-length conventions, and the
ledger and requires every mutation to fail.  It uses explicit exceptions, not
`assert`, so normal and optimized runs execute the same fail-closed gates.  The
verifier is corroborative only and is not a uniform certificate.
