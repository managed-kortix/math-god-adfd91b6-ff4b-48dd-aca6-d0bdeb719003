# Two-pivot Schur--Sachs theory for a triangular cactus between hostile pentagons

**Date:** 2026-07-26

## 1. Verdict

Write

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5.
```

There is an exact rank-two boundary theory for a triangular cactus `A` with
marked vertices `x,z`.  Its state is a symmetric `2 x 2` Schur matrix, or
projectively the four rooted characteristic minors

```text
[Phi_A : Phi_(A-x) : Phi_(A-z) : Phi_(A-{x,z})].
```

This state composes exactly under edge, path, tree, and one-vertex cycle
attachments.  The determinant of the final two-pivot matrix gives the complete
normalized Schur--Sachs polynomial, and the continuous phase is recovered
exactly by a lift formula with an integer winding term.

This analytic reduction covers both requested interfaces:

```text
P | A_7 | P,                 (D9a)
entry-locked T^7 P | P.     (D9b)
```

It does **not** prove a uniform positive surplus.  The failure is now isolated:
the proposed theorem is equivalent to one integrated, winding-sensitive
inequality for the determinant of the transferred `2 x 2` state.  Positivity
of the matrix entries, a principal `atan`, and scalar projective ratios cannot
establish it.  A bare seven-triangle example already has a determinant crossing
the negative real axis and winding onto a lower sheet.  Thus the missing fact
is an invariant cone or crossing theorem for the full projective matrix state,
not another Schur elimination identity.

No counterexample to `sigma(G)>0` is found or asserted.

## 2. Exact two-pivot state

Let `H` be a finite weighted graph with marked vertices `x,z`, and put

```text
M_H(lambda)=lambda I-A_H.
```

Eliminate every vertex except `x,z`.  Whenever the interior block is
invertible, the Schur complement is

```text
S_H(lambda)=M_H[{x,z}]-M_H[{x,z},U] M_H[U]^(-1) M_H[U,{x,z}]
           =[[alpha, -gamma],[-gamma, beta]],                 (2.1)
```

where `U=V(H)-{x,z}`.  Jacobi's determinant identity gives

```text
det M_H                 = det M_H[U] (alpha beta-gamma^2),
det M_(H-x)             = det M_H[U] beta,
det M_(H-z)             = det M_H[U] alpha,
det M_(H-{x,z})         = det M_H[U].                         (2.2)
```

Hence, writing `Phi_J=det(lambda I-A_J)`,

```text
alpha = Phi_(H-z)/Phi_(H-{x,z}),
beta  = Phi_(H-x)/Phi_(H-{x,z}),
gamma^2 =
  [Phi_(H-x) Phi_(H-z)-Phi_H Phi_(H-{x,z})]
  /Phi_(H-{x,z})^2.                                           (2.3)
```

Equations (2.1)--(2.3) prove that the projective four-minor state is complete.
The sign of `gamma` is fixed by the chosen terminal order and the actual Schur
elimination.  The four minors determine it only up to the harmless gauge
`e_z -> -e_z`; only `gamma^2` enters the present targets because both external
arms are diagonal boundary loads.  At isolated poles, (2.2) gives the
continuation by polynomial identity.  Thus no genericity assumption remains.

A single rooted ratio is insufficient.  It loses the mixed minor, equivalently
the off-diagonal transfer `gamma`; two triangular cacti can agree at each
one-root response and differ after both hostile arms are installed.

## 3. Transfer matrices and arbitrary trees

For a rooted tree branch directed toward the core, define the imaginary-axis
message

```text
q_(u->v)(t)=Z_(T_(u->v))(t)/Z_(T_(u->v)-u)(t)
           =t+sum_(w child of u) 1/q_(w->u)(t)>0.             (3.1)
```

After extracting the positive forest denominator, an attachment at a core
vertex changes its diagonal activity from `t` to

```text
a_v(t)=t+sum 1/q_(u->v)(t)>=t.                                (3.2)
```

For a path whose successive effective activities are `a_1,...,a_m`, Gaussian
elimination is equivalently the projective transfer

```text
(K_j,K_(j-1))^T = L(a_j)(K_(j-1),K_(j-2))^T,
L(a)=[[a,1],[1,0]],
K_j=a_j K_(j-1)+K_(j-2).                                     (3.3)
```

Thus a connector has transfer `L(a_m)...L(a_1)`.  At a cactus cut, incident
branch self-energies add to the corresponding diagonal of (2.1).  At a
triangle or pentagon block, eliminate its private path by (3.3) and add the
resulting `2 x 2` Dirichlet-to-Neumann matrix.  These are exact rational
operations, so successive block elimination computes `S_A(it)` for an
arbitrary two-root triangular cactus and arbitrary attached trees.

The Sachs terms are not extra data.  They are exactly the nonmatching terms in
the determinant of the same Schur matrix.  Equivalently one may compute each
minor in (2.3) by the grouped formula

```text
Psi_J(t)=sum_(C pairwise vertex-disjoint cycles of J)
         product_(C in C)(-2 i^(-|C|)) Z_(J-V(C))(a),          (3.4)
```

where triangles have multiplier `-2i` and pentagons multiplier `+2i`.
Equations (2.3) and (3.4) are the two-pivot Schur and Sachs descriptions of the
same state.

## 4. Hostile pentagon boundary map

Let a weighted pentagon be attached at one terminal `x`, either by identifying
its root with `x` or through a path.  Eliminating the four private pentagon
vertices gives a scalar Schur correction `h_P(t)` at `x` and a nonzero
normalized determinant factor `d_P(t)`.  In Schur notation this is the diagonal
update

```text
S -> S + h_P(t) e_x e_x^T,                                   (4.1)
```

followed by multiplication by `d_P(t)`.  A nonempty bridge path first applies
the continuant transfer (3.3), so it has the same form with a continued-fraction
self-energy.  The extracted forest and path denominators are positive after
normalization.  The pentagon factor and its Sachs phase remain in `d_P` and
`h_P`; they are not discarded.

Consequently two hostile arms give

```text
S_final(t)=S_A(t)+h_L(t)e_x e_x^T+h_R(t)e_z e_z^T,
F_G(t)=D(t) det S_final(t),                                   (4.2)
```

where `D(t)` is the product of the normalized terminal-arm and eliminated-core
factors.  Formula (4.2) is valid for `P|A_7|P`, including coincident roots by
taking the one-pivot degeneration.  Equivalently, absorb the terminal-arm
factors into a denominator-free four-minor version of (4.2); this is the safest
form for phase accounting.

For entry-locked `T^7P|P`, include the clustered pentagon in `A` before forming
its two-terminal state: one terminal is its locked incidence cut and the other
is the external entry.  The remote pentagon then acts by (4.1).  If both marks
coincide, (4.2) degenerates to the established scalar common-cut theorem; if
they do not, it is genuinely rank two.

## 5. Exact phase and winding

Normalize

```text
F_G(t)=i^(-|V(G)|) Phi_G(it).
```

It never vanishes for `t>0`, because the zeros of `Phi_G` are real.  Let
`theta_G(t)` be the unique continuous argument with
`theta_G(t)->0` as `t->infinity`.  For the principal argument in `(-pi,pi]`,
there is a unique integer lift label `k(t)`, locally constant away from
principal-branch crossings, such that

```text
theta_G(t)=Arg_pr F_G(t)+2 pi k(t),                            (5.1)
```

is continuous and `k(t)=0` for sufficiently large `t`.  Equivalently,

```text
theta_G(t)=-Im integral_t^infinity F_G'(u)/F_G(u) du.          (5.2)
```

At the lower endpoint,

```text
lim_(t downarrow 0) theta_G(t)
 = (pi/2)(n_+(G)-n_-(G)),                                    (5.3)
```

with the usual limiting interpretation when zero eigenvalues occur.  Equations
(5.1)--(5.3), not `atan(Im F/Re F)`, fix the phase sheet exactly.

For a connected rank-nine cactus, `|E|=n+8`, so

```text
sigma(G)=8-(2/pi) integral_0^infinity t theta_G(t) dt.         (5.4)
```

Therefore the desired uniform theorem for either target is exactly

```text
integral_0^infinity t theta_G(t) dt < 4 pi.                   (5.5)
```

All quantities in (5.5) are generated by the projective state (2.3), the local
transfers (3.1)--(3.3), and the lift (5.1).

## 6. Why the natural two-pivot comparison fails

The scalar common-cut proof works because its normalized Schur expression has
positive real part.  No analogous right-half-plane invariant holds here.
Consider the seven-triangle cactus

```text
T1=(0,1,2),   T2=(0,3,4),    T3=(3,5,6),
T4=(5,7,8),   T5=(3,9,10),   T6=(6,11,12),
T7=(12,17,18).
```

Coalesce pentagons at the two marked vertices `0` and `18`.  This is a bare
`P|A_7|P` two-pivot core.  Exact integer determinant expansion gives

```text
F(t)=R(t)+i I(t),

R=t^23+31t^21+394t^19+2640t^17+10055t^15+21899t^13
  +25637t^11+12713t^9-1296t^7-3522t^5-1159t^3-129t,

I=-14t^20-320t^18-2928t^16-13908t^14-37286t^12-57480t^10
  -50042t^8-23608t^6-5512t^4-460t^2+6.                      (6.1)
```

Thus `R(t)=-129t+O(t^3)<0` and `I(t)=6+O(t^2)>0` near zero.
Its exact characteristic polynomial factors as

```text
(x-1)(x+1)^3(x^2-3)(x^2+x-1)^2
(x^13-4x^12-15x^11+64x^10+83x^9-370x^8-212x^7+924x^6
 +257x^5-896x^4-153x^3+164x^2+43x+2).                       (6.2)
```

Sturm counting gives inertia `(10,13,0)`.  Hence (5.3) gives

```text
theta_G(0+)=-3pi/2,                                         (6.3)
```

whereas the principal argument near zero is `+pi/2`.  One full `2 pi` lift is
essential.  In particular:

1. `Re F>0` is false;
2. a principal `atan` or unsigned projective slope gives the wrong sheet;
3. entrywise positivity of continuants does not control the determinant phase;
4. comparing only the two diagonal rooted ratios loses the winding carried by
   the mixed minor.

The core in (6.1) has positive numerical surplus (about `12.2920`, by numerical
root evaluation only), so it is an obstruction to the proof chart, not to the
target inequality.  The exact certificate below does not use that decimal.

The determinant, factorization, coefficient signs, and Sturm inertia count are
reproduced exactly by

```bash
/tmp/opencode/octacyclic-cacti-venv/bin/python \
  research/two-pivot-winding-obstruction-certificate.py
```

## 7. Isolated remaining theorem

The exact missing statement can now be formulated without ambiguity.

**Two-pivot winding theorem (open).** For every seven-triangle cactus `A` with
two marked cyclic-hull vertices (possibly equal), every collection of finite
rooted trees, and the hostile boundary maps producing `P|A_7|P` or entry-locked
`T^7P|P`, the determinant in (4.2), continuously lifted by (5.1), satisfies
(5.5).

A sufficient pointwise version would place the lifted determinant phase below
an explicit integrable majorant.  A weaker integrated proof would also suffice.
Either proof must use one of the following genuinely new ingredients:

```text
- an invariant cone in the projective space of symmetric 2 x 2 Herglotz states;
- a signed crossing theorem counting every negative-real-axis crossing; or
- an exact finite certificate retaining the mixed minor and its winding label.
```

The `2 x 2` transfer state therefore completes the analytic reduction and
pinpoints the failure.  It does not, by itself, supply the uniform positive
surplus requested for the two rank-nine kernels.
