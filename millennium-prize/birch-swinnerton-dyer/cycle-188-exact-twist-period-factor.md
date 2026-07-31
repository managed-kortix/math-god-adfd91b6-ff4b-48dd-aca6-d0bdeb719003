# Cycle 188: exact twist period factor for `433a1`

## Result

Let

\[
 E:y^2+xy=x^3+1
\]

and let `q` be an odd prime not dividing `433`.  Put

\[
 D=D_q=\begin{cases}q,&q\equiv1\pmod4,\\-q,&q\equiv3\pmod4.
 \end{cases}
\]

Thus `D` is odd, squarefree, and `D=1 mod 4`.  The integral quadratic-twist
model

\[
 T_D:y^2-xy=x^3+\frac{D-1}{4}x^2+D^3                         \tag{188.1}
\]

is globally minimal, and its Neron differential is

\[
 \omega_D=\frac{dx}{2y-x}.
\]

With the period conventions of Cycle 187, the exact comparison factor is

\[
 \boxed{\kappa_q=1}                                         \tag{188.2}
\]

for every such `q`.  In particular `kappa_q` is a positive power of two with
exponent zero, is a `7`-adic unit, and has reduction `1` in `F_7`.  It can
never vanish modulo `7` in this family.

## Twist isomorphism and differential

Complete the squares by putting

\[
 Y=2y+x\quad\hbox{on }E,
 \qquad Z=2y-x\quad\hbox{on }T_D.
\]

The equations become

\[
 Y^2=4x^3+x^2+4,
 \qquad Z^2=4x^3+Dx^2+4D^3.
\]

Over `Q(sqrt(D))`, the map `phi_D:T_D -> E` is therefore

\[
 X=\frac{x}{D},\qquad Y=\frac{Z}{D\sqrt D}.
\]

Since `omega_E=dX/Y` and `omega_D=dx/Z`, direct substitution gives the exact
identity

\[
 \phi_D^*\omega_E=\sqrt D\,\omega_D.                         \tag{188.3}
\]

For `D=q>0`, (188.3) identifies the invariant real period and gives
`Omega_E^+=sqrt(q) Omega_(T_D)^+`.  For `D=-q<0`, take
`sqrt(D)=i sqrt(q)` and the pinned positive anti-invariant orientation of Cycle
187; then (188.3) gives
`Omega_E^-=sqrt(q) Omega_(T_D)^+`.  Both cases give (188.2), provided (188.1)
is the global minimal model.

## Global minimality

The invariants of (188.1) satisfy

\[
 c_4(T_D)=D^2,
 \qquad \Delta(T_D)=-433D^6.                                 \tag{188.4}
\]

These identities also follow from the usual weights `4` and `12` under a
quadratic twist, since `c_4(E)=1` and `Delta(E)=-433`.

Minimality is local and immediate from (188.4):

1. At `2`, the discriminant is odd, so the model has good reduction and is
   minimal.
2. At every odd prime not dividing `433D`, the discriminant is a unit.
3. At `433`, its valuation is one because `q != 433`, so no integral change
   with scaling divisible by `433` is possible.
4. At `q`, `v_q(Delta)=6<12`; hence an integral change with scaling divisible
   by `q` is impossible.  Equivalently, `v_q(c_4)=2<4` already obstructs it.

Thus (188.1) is globally minimal.  Translations used to select a different
minimal integral equation have scaling parameter `u=1` and preserve the Neron
differential.  More generally, if a generated twist model were changed to a
minimal model with scaling `u`, then the period factor would be `1/abs(u)` in
the convention `x_generated=u^2 x_minimal+r`; here the exact minimality proof
forces `u=1`.  No factor two, Manin factor, or real-component factor remains.

## First collision candidates

For the first Cycle 187 candidates, the generated model (188.1), its twist
parameter, and the exact factor are:

| `q` | `D_q` | `(a1,a2,a3,a4,a6)` of `T_D` | `kappa_q` |
|---:|---:|---|---:|
| 1499 | -1499 | `(-1,-375,0,0,-3368254499)` | 1 |
| 6287 | -6287 | `(-1,-1572,0,0,-248502281903)` | 1 |
| 3823 | -3823 | `(-1,-956,0,0,-55874402767)` | 1 |
| 8317 | 8317 | `(-1,2079,0,0,575307591013)` | 1 |

PARI's `ellminimalmodel` returns changes with scaling coordinate `u=1` for all
four models; only integral translations occur.  Hence the pair `(1499,6287)`
and the pair `(3823,8317)` require no period correction in the Cycle 187 base
symbol formula.  This settles the normalization gate only; it does not compute
their modular-symbol residues or prove a collision.
