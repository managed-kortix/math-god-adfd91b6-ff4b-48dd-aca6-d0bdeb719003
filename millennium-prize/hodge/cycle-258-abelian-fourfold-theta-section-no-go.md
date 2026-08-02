# Cycle 258: abelian-fourfold theta-section support no-go

## Exact support

This scout leaves the Cycle 242 architecture rather than changing its
coefficient box.  Put

\[
 A_0=E_i^3\times E_i^3
\]

with the mixed `Q(i)` action and polarization convention of Cycle 151.  Define
the abelian fourfold

\[
 \nu:E_i^4\hookrightarrow A_0,
 \qquad
 (t_1,t_2,t_3,t_4)\longmapsto
 (t_1,t_2,t_3;t_1,t_2,t_4).                         \tag{258.1}
\]

Thus `B=nu(E_i^4)` is cut out by `y_1=x_1` and `y_2=x_2`.  On `E_i^4` take
the Gaussian Hermitian matrix

\[
 H_0=
 \begin{pmatrix}
 2&0&0&0\\
 0&2&0&0\\
 0&0&2&1\\
 0&0&1&2
 \end{pmatrix},
 \qquad H=3H_0,                                      \tag{258.2}
\]

and let `L_H` be the corresponding ample line bundle.  Since the eigenvalues
of `H_0` are `2,2,3,1`, it is positive definite.  The third power in (258.2)
is chosen so that the standard theorem for powers of ample line bundles gives
a very ample system without relying on a principal-polarization exception.
Freeze the architecture

\[
 T_s=V(s)\subset E_i^4,
 \qquad Y_s=\nu(T_s)\subset A_0,                     \tag{258.3}
\]

where `[s]` lies in the explicitly defined Zariski open of
`P H^0(E_i^4,L_H)` on which `T_s` is smooth.  Bertini makes this open nonempty.
For an exact computation one fixes the Appell--Humbert model (258.2), a theta
basis for `H^0(L_H)`, and algebraic coordinates for one section `s`; this is a
finite projective parameter space, not an unbounded choice of source curves.

The support is a smooth ample divisor in an abelian fourfold.  Lefschetz gives
`q(T_s)=4`, and adjunction gives `K_(T_s)=L_H|_(T_s)`, which is ample.  Hence it
is not an abelian threefold, a translate of a homomorphism graph, or a support
with trivial canonical bundle.  In particular (258.3) is genuinely non-graph.
It is also not the image of a product of three curves under an addition map:
there is one irreducible theta-section source and no three independent
difference divisors.  The `64<512` argument of Cycle 251 therefore has no
input here.

## Exceptional Weil coordinate

Use the determinant generators

\[
 \Omega_W=dz_1dz_2dz_3\,d\bar z_4d\bar z_5d\bar z_6,
 \qquad \Omega_{\bar W}=\overline{\Omega_W}.
\]

Equation (258.1) gives

\[
 \nu^*\Omega_W=
 dt_1dt_2dt_3\,d\bar t_1d\bar t_2d\bar t_4.          \tag{258.4}
\]

The only complementary term of `c_1(L_H)` is, up to the fixed nonzero
Appell--Humbert normalization,

\[
 H_{43}\,dt_4d\bar t_3=3\,dt_4d\bar t_3.             \tag{258.5}
\]

Consequently

\[
 \int_{Y_s}\Omega_W
 =\int_{E_i^4}c_1(L_H)\wedge\nu^*\Omega_W\ne0,        \tag{258.6}
\]

and conjugation gives the nonzero opposite determinant coordinate.  Therefore

\[
 \boxed{P_W[Y_s]\ne0}                                \tag{258.7}
\]

for every smooth section `s`.  This is a direct period calculation; it does
not infer the exceptional component from a Chern character to be constructed
later.  Notice why a diagonal `H` would fail: the off-diagonal entry `H_43` is
exactly the missing `(1,1)` pair in (258.4).

## Finite deformation target

Nonzero exceptional projection is only the admission gate.  Let `S` be the
nine-dimensional determinant-`-3` PEL germ and write its tangent vector as
`C in M_3(C)`, with the off-diagonal Beltrami matrix fixed in Cycle 152.  For a
fixed algebraic section `s`, the exact target is

\[
 \boxed{
 \rho_{Y_s}:T_0S\longrightarrow H^1(Y_s,N_{Y_s/A_0})=0.}         \tag{258.8}
\]

Here the equality means that the map is zero, not that its target group
vanishes.  The normal sequence

\[
 0\to L_H|_{T_s}\to N_{Y_s/A_0}
 \to O_{T_s}^{\oplus2}\to0                         \tag{258.9}
\]

makes (258.8) finitely testable.  In the theta embedding supplied by `3H_0`,
one computes the Kodaira--Spencer action on the ideal
`(y_1-x_1,y_2-x_2,s)`, reduces the nine resulting Cech classes through the
finite Koszul resolution of `s`, and asks whether every matrix entry is zero.
Equivalently, after choosing the standard affine theta charts, (258.8) is the
vanishing of a specified finite matrix over the algebraic coefficient field
of `s`.  A single nonzero entry rejects that section.

Before the raw test, impose the cheaper semiregularity potential equations

\[
 \boxed{C\mathbin{\lrcorner}[Y_s]=0
 \quad\hbox{for all nine basis matrices }C.}          \tag{258.10}
\]

The class `[Y_s]=nu_*c_1(L_H)` is independent of `s`, so (258.10) is one exact
rational exterior-algebra calculation.  It fails.  Write the class, suppressing
one common nonzero Appell--Humbert scalar, as

\[
 \alpha=(dz_4-dz_1)(d\bar z_4-d\bar z_1)
 (dz_5-dz_2)(d\bar z_5-d\bar z_2)\,\widetilde h,       \tag{258.11}
\]

where `nu^*widetilde h=c_1(L_H)`.  Take the PEL basis tangent
`C=E_(12)`, with indices numbered from one.  Its Beltrami derivation sends

\[
 dz_1\longmapsto d\bar z_5,
 \qquad dz_5\longmapsto d\bar z_1,                    \tag{258.12}
\]

and kills the other holomorphic basis forms (the relevant two polarization
weights are both one).  In `C contracted alpha`, the coefficient of

\[
 dz_3dz_4\,d\bar z_1d\bar z_3d\bar z_4d\bar z_5       \tag{258.13}
\]

is `-6`, in the integral normalization of (258.2).  In particular

\[
 \boxed{E_{12}\mathbin{\lrcorner}[Y_s]\ne0.}          \tag{258.14}
\]

This single coefficient is an exact rejection witness for every section in
the architecture.  It is the balanced part of the effective support class;
the exceptional projection proved in (258.7) is horizontal but cannot cancel
this coefficient.  Thus no member reaches the raw obstruction map (258.8),
the 45 quadratic lifts, or an all-order algebraization question.

## Disposition

The exact bounded target and its disposition are therefore:

1. non-graph support and smooth existence: pass;
2. nonzero exceptional Weil coordinate: pass by (258.6);
3. potential deformation vanishing: fail by the coefficient `-6` in (258.13);
4. raw first-order and higher lifts: not reached.

This is a genuinely new, finitely falsified architecture: its support exists,
is non-graph, avoids the three-curve sum collision theorem, and has a proved
nonzero exceptional Weil coordinate, but it cannot deform in all nine PEL
directions.  The fixed architecture is retired rather than repaired by adding
graph components.  There is no viable Hodge route from this candidate.  No
Hodge or Millennium result is claimed, and focused Navier work remains the
main lane.

Reproduce the exceptional complement and the exact contraction witness with

```sh
python3 millennium-prize/hodge/verify_cycle258_theta_section_no_go.py
```
