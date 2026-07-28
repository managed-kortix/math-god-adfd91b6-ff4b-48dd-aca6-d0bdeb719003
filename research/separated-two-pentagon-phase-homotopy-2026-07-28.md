# Separated two-pentagon phase homotopy

**Date:** 2026-07-28

## Scope

This note isolates the analytic obstruction for a triangle-packing-one cactus
with two separated pentagons. It proves an exact homotopy derivative identity
and shows that deleting the joint-pentagon Sachs terms has the wrong phase
orientation. It does not prove or disprove positive square energy.

After rooted-tree message elimination, group positive matching carriers as

```text
Z  empty cycle set,
A  one triangle,
B  one pentagon,
C  one triangle and one pentagon,
D  both pentagons,
E  one triangle and both pentagons.
```

Packing one excludes two triangles but does not exclude both separated
pentagons. Since the cycle multipliers are `-2i` for a triangle and `+2i` for a
pentagon, the exact normalized polynomial is

```text
Psi=(Z+4C-4D)+i[2(B-A)+8E].                             (1)
```

The joint-pentagon contribution is `-4D+8iE`, a second-quadrant correction.
Equivalently, if `F` is obtained by deleting both pentagons, then
`Psi_F=D-2iE` and the correction is `-4Psi_F`.

Introduce

```text
Psi_lambda=(Z+4C-4 lambda D)+i[2(B-A)+8 lambda E].      (2)
```

Wherever the argument is continuously lifted and `Psi_lambda` is nonzero,
direct differentiation gives

```text
d/dlambda Arg(Psi_lambda)
 =8[D(B-A)+E(Z+4C)]/|Psi_lambda|^2.                    (3)
```

Indeed `d Arg=(R I'-I R')/(R^2+I^2)`, and the two terms proportional to
`lambda DE` cancel exactly. Thus if

```text
D(B-A)+E(Z+4C)>=0,                                     (4)
```

turning on the joint-pentagon carrier increases, rather than decreases, phase.
Condition (4) is automatic when `B>=A`; the difficult region is `A>B`.

For the bare one-triangle separated fan at `t=1`, exact matching recursion gives

```text
Z=2944, A=608, B=408, C=86, D=14, E=3,
D(B-A)+E(Z+4C)=7064>0.                                 (5)
```

Hence the natural claim that the joint-cycle package is phase-damping is
strictly false even on the smallest structural extremizer. Independent-
activity coefficient comparisons with two isolated weighted pentagons also
have negative coefficients; scalar rooted ratios cannot encode the necessary
mixed minor or winding sheet.

The surviving route is a direct integrated estimate retaining `D-2iE`, or a
winding-sensitive two-pivot Schur inequality on the rooted-message locus.
