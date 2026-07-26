# Rooted `T^6P` residuals: exact activity-polynomial certificate search

**Date:** 2026-07-26

## Verdict

For each of the four residual marked kernels R1--R4 in
`octacyclic-rooted-six-triangle-finite-reduction-2026-07-26.md`, arbitrary
rooted trees were eliminated exactly by Schur complementation.  This gives one
independent core activity

```text
a_v(t)=t+y_v(t),  y_v(t)>=0
```

at every cyclic-hull vertex.  The complete grouped Sachs polynomial was then
expanded over `ZZ[t,y_0,...,y_16]`.

No proof of the desired rooted margin was found.  More strongly, each of the
three natural pointwise certificates fails coefficientwise for every kernel:

```text
R >= 0,                 -I >= 0,
2R-Z_5(t)I >= 0,        Z_5(t)=t^5+5t^3+5t,
```

where `Psi=R+iI` is the normalized Schur--Sachs polynomial after the positive
forest factor is removed.  The failures include exact negative monomials listed
below.  Therefore there is no direct monomial-preserving matching injection for
any displayed inequality.  Ordinary SOS certificates are also impossible for
the inequalities having the exact negative orthant witnesses below.  This is a
failure of these certificate targets, not a counterexample to
`sigma>1-delta`.

The executable certificate is

```bash
python research/octacyclic-t6p-rooted-activity-certificates.py
```

It uses only the Python standard library and exact integer/rational arithmetic.

## Schur--Sachs formulation

Let `H` be one realized residual core, including its rooted pentagon, and let
`K(t)>0` be the product of the deleted rooted-tree matching denominators.  For
each collection `S` of pairwise vertex-disjoint cyclic blocks, put

```text
Z_(H-V(S))(a)=sum_M product_(v unmatched by M) a_v.
```

A triangle has normalized Sachs multiplier `-2i` and the pentagon has
multiplier `+2i`.  Hence the attachment-uniform polynomial is exactly

```text
Psi_G(t)/K(t)
 = sum_(S disjoint) (-2i)^#triangles(S) (2i)^#pentagons(S)
                    Z_(H-V(S))(a)
 = R(t,y)+i I(t,y).                                      (1)
```

If `R>0`, comparison with the isolated pentagon phase is the polynomial
cross-product inequality

```text
2R-Z_5 I>0                                                (2)
```

when `I>0`; when `I<=0` the phase comparison is automatic.  Thus
`R>0` together with (2) would imply `Theta_G<theta_5`, then
`D(G)>-2delta` by signed Coulson integration, and in fact

```text
sigma(G)>6-delta>1-delta.                                 (3)
```

The still stronger condition `-I>0` would keep the characteristic curve in the
lower half-plane and imply `D(G)>0`, hence `sigma(G)>6`.  These are sufficient,
not necessary, formulations of the requested rooted margin.

## Exact failed monomials

Vertices are numbered by the script: shared cuts first in increasing incidence
label, followed by private triangle vertices and then the four private
pentagon vertices.  All monomials below occur after substituting `a_v=t+y_v`.

| kernel | first negative term of `R` | first negative term of `-I` | first negative term of `2R-Z_5I` |
|---|---:|---:|---:|
| R1 | `-23 y_2` | `-2 y_0 y_1` | `-46 y_2` |
| R2 | `-23 y_3` | `-2 y_0 y_1` | `-46 y_3` |
| R3 | `-15 y_4` | `-2 y_0 y_1` | `-30 y_4` |
| R4 | `-11 y_4` | `-4 y_4 y_5` | `-22 y_4` |

The complete expansion statistics are:

| kernel | polynomial | nonzero monomials | negative monomials | minimum coefficient | SHA-256 |
|---|---|---:|---:|---:|---|
| R1 | `R` | 517308 | 1867 | -101 | `d66519bd773a8aa153c0131382441b3485280238bb5d473f2e6d53a8bc4e9f73` |
| R1 | `-I` | 186744 | 6782 | -20 | `e8406c23c97db868be5e0399f253ddb122bc2ea4e5b0283ddddd7d8f50fe2e02` |
| R1 | `2R-Z_5I` | 574656 | 527 | -92 | `2d5b2707a988d7926a8a9df77b4139a3acb5822d2941f35ed76fe1052dda6140` |
| R2 | `R` | 528156 | 4594 | -244 | `85b86285f5958140a321e20afac6c9eab149139e06226e77bb91b8947f8d9b26` |
| R2 | `-I` | 202000 | 6473 | -20 | `48e98896dfdf44944e081616bd6e40db8ed8382cd6621d64641351240005a7d2` |
| R2 | `2R-Z_5I` | 588874 | 2548 | -370 | `a739b0090f50e7c9a6acb91b29fb46abc96d1d20bdbd49a96558e14601735eb5` |
| R3 | `R` | 534262 | 6704 | -472 | `9efc427d2a333d92a4609cee8f08bada6ec2d0b364a6def6879247dca1dc9182` |
| R3 | `-I` | 210561 | 6138 | -24 | `9ba1c68f6783a4392da4d4a6be3c4c0843bb0d7a3168f8a53800baae6ff52a70` |
| R3 | `2R-Z_5I` | 596336 | 3953 | -430 | `db53b998cf57e236b8442d85e93fbd57cd8a0266e07665683fa48541fd848c0c` |
| R4 | `R` | 513262 | 5860 | -356 | `83ddbde82f2f69712da221270356c93d2a3669558257b6ddb7aaf8e4501d6682` |
| R4 | `-I` | 196038 | 3600 | -20 | `deaa78862727dca6c73fe05ffb11949aa8f5cc7f89d3d9029bbdabd2bf2deae1` |
| R4 | `2R-Z_5I` | 578133 | 2933 | -450 | `bd2e6bf4bab0b6b179bd5d8290c6150cb5d80c93d89c51fc41abdbb2b18feddb` |

The hashes encode every term as `(t-degree,y-mask,coefficient)`, not merely the
summary rows.

## Exact nonpositivity witnesses

The coefficient failures are not artifacts of a poor monomial basis.  The
following points give exact negative evaluations of `-I`:

```text
R1: t=1,   y_0=y_1=100:  -I=-502144;
R2: t=1/10,y_0=y_1=10:   -I=-2085619518255247/25000000000000;
R3: t=1/10,y_0=y_1=10:   -I=-1378041735369997/25000000000000;
R4: t=1/10,y_4=y_5=10:   -I=-3848954342875047/25000000000000.   (4)
```

Every point in (4) is realizable by rooted trees.  At `t=1`, 100 leaves at a
core vertex contribute `y=100`; at `t=1/10`, one leaf contributes `y=1/t=10`.
Thus `-I>=0` is false for every kernel, and no ordinary SOS proof of that
inequality can exist.

For R2--R4 no attachment is needed to disprove the positive-real chart.  At
`y=0`, their exact real parts are respectively

```text
R2=t^17+23t^15+198t^13+801t^11+1570t^9+1369t^7+406t^5-49t^3-31t,
R3=t^17+23t^15+202t^13+845t^11+1682t^9+1293t^7-10t^5-289t^3-67t,
R4=t^17+23t^15+194t^13+757t^11+1346t^9+797t^7-194t^5-185t^3-19t.
```

Each is strictly negative at the exact rational point `t=1/100`.  Therefore
the conjunction `R>0` and (2), and any SOS proof of its first inequality, is
impossible for R2--R4.  The continuous Coulson argument may still lie on a
lower winding sheet, exactly as in the known multiple-triangle obstruction.

The script also finds exact nonnegative-orthant points where `2R-Z_5I<0` for
all four kernels (for example, `t=1/10`, one selected activity `y_v=1`).  Those
points certify failure on the free activity orthant.  Unlike (4), this audit
does not claim that each particular `y_v=1` value is attained by a finite tree
message at that same `t`; coefficientwise and free-orthant certificates are
nevertheless ruled out exactly.

## What remains open

The bare specialization `y=0` of `-I` and `2R-Z_5I` has nonnegative
coefficients for all four kernels.  Tree activities destroy that
coefficientwise positivity.  The search therefore rules out the most direct
attachment-uniform coefficient, matching-injection, positive-real-chart, and
ordinary-SOS routes.  It does not rule out a winding-sensitive Schur theorem,
a Positivstellensatz using additional realizability relations among tree
messages, or a direct integrated phase bound weak enough to prove only
`sigma>1-delta`.

Consequently R1--R4 remain exact unresolved kernels; no claimed proof of the
rooted margin should cite the failed inequalities above.
