# Rank-six orders eight through ten: rational-density reduction and a template counterexample

## Verdict

The proposed statement

> every coarse residual has a rational Gram certificate of excess at most five

has not yet been proved for all rank-six kernels of orders eight through ten.
There is, however, a rank-uniform lemma that removes rational reconstruction
from every **strict** residual.  Consequently an exact proof need only separate

1. strict feasibility below five; and
2. the exposed equality face at cost five.

The signed-five-cycle and tetrahedron-plus-apex constructions are exact
equality-face certificates.  They do not, by themselves, classify the coarse
residuals.  An authenticated order-eight row below gives a counterexample to
that stronger template-only claim.

The matching lower bounds and minimizer-locus descriptions for both constructions
are proved in `cost-five-equality-face-lemma.md`. In particular, the known
cost-five Grams are global optima of their canonical objectives, not merely
feasible points. That lemma also shows that the Gram completion within either
geometry need not be unique.

## Lemma (strict real certificates rationalize)

Let `P_1,...,P_m` be paths with prescribed lengths and endpoint signs.  Suppose
unit vectors have been assigned to every branch and internal path vertex so
that no consecutive transformed vectors are antipodal and

`E=sum_(consecutive x,y) (1-<x,y>)/(1+<x,y>) < b`.

Then there is an assignment by rational unit vectors, in the same dimension,
whose Gram matrix is rational and positive semidefinite and whose excess is
also strictly less than `b`.

The assertion remains true for any finite collection of frontiers sharing the
same branch vectors, provided one real assignment makes every frontier cost
strictly less than `b`.

### Proof

Rational points are dense on every unit sphere in ambient dimension at least
two.  One
explicit dense parametrization is stereographic projection

`t -> (2t_1,...,2t_(d-1),1-||t||^2)/(1+||t||^2)`

with rational `t` in ambient dimension `d`.  (The one-dimensional ambient case
has only the already-rational unit vectors `+1,-1`.)  Approximate every vector
in the finite collection simultaneously by a rational unit vector.  All
resulting inner products are rational, and their matrix is a Gram matrix, hence
is positive semidefinite.

The step function `h(r)=(1-r)/(1+r)` is continuous away from `r=-1`.  There
are finitely many steps, so the total cost is continuous in all vectors on a
neighborhood of the given assignment.  If `delta=b-E>0`, sufficiently close
simultaneous rational approximations change every relevant total by less than
`delta`.  Their costs therefore remain below `b`.  The same argument applied
to the union of finitely many frontier chains proves the shared-branch version.
`QED`

## Consequence for the correlation SDP dual

For rank six take `b=5`.  The lemma shows that denominator searches and a full
ledger of rational vectors are not mathematically needed for rows for which a
strict real inequality has already been proved.  A reduced proof can instead
have three layers:

1. an exact combinatorial or analytic certificate that the optimum is `<5`;
2. a finite classification of rows whose optimum can equal `5`;
3. exact rational Grams only for those equality rows.

Compactness makes this especially useful after the parity/frontier reduction:
there are finitely many canonical targets.  If equality targets are identified
exactly and every other target is proved strict, the strict targets rationalize
without recording individual rational witnesses.  This is a proof reduction,
not a numerical one: floating-point output alone does not prove strictness or
exclude an unrecognized equality face.

The lemma cannot rationalize a merely non-strict real witness of cost exactly
five.  Rational approximants may approach that witness only from the side with
cost greater than five.  Thus equality classification is the essential SDP-face
problem and cannot be discarded.

## Exact equality packets already available

The rank-uniform signed-cycle quotient has five mixed doubled bundles.  With
quotient Gram `Q=I-S/2`, every signing is positive semidefinite, each mixed
bundle costs one, and all contracted singleton supports cost zero.  This gives
exact excess five for

`K744, K756` at order eight, `K971` at order nine, and `K1133` at order ten.

At order eight the tetrahedron-plus-apex recognizer finds 33 residual parity
orbits on 13 kernels.  Six odd tetrahedron edges cost `6/2`, two mixed apex
bundles cost `2`, and the three signed contractions cost zero, again totaling
five.  These records are plausible equality-face candidates, but the current
recognizer explicitly does not prove that they are the complete equality set.

## Counterexample to a template-only residual theorem

Consider order-eight residual source index zero, on `K646`.  Its support data
`(edge, multiplicity, number of odd paths)` are

```text
06:(1,1)  07:(2,1)  16:(1,1)  17:(2,1)  25:(2,1)
27:(1,0)  34:(2,1)  36:(1,0)  45:(1,0).
```

Its best regular-tetrahedron coloring has scaled cost `162`, namely `27/5`, so
it is a genuine coarse residual above the budget `150/30=5`.  It is neither a
signed-five-cycle quotient nor a tetrahedron-plus-apex row:

- it has five singleton and four doubled supports, rather than three singleton
  and five doubled supports for the order-eight signed-cycle packet;
- it has four doubled supports, rather than the two apex bundles required by
  the tetrahedron-plus-apex quotient.

Nevertheless the exact order-eight checkpoint stores one denominator-256
rational realization shared by the canonical target and all 13 coordinate
frontiers.  Exact `Fraction` reconstruction gives maximum frontier cost

`4.001986657770123... < 5`.

The pack verifier recomputes every rational unit vector and every exact step
cost; the decimal is only a readable rendering.  Thus `K646/source 0` is a
counterexample to either assertion that tetrahedral coloring closes every row
or that all residuals belong to the signed-cycle/simplex-apex equality
geometries.  It is not a counterexample to the desired DNN bound.

## What remains for orders eight through ten

A census-free theorem now reduces to an equality-separation lemma of the form:

> For every canonical rank-six target of orders eight through ten, either a
> named signed-cycle or simplex/apex face applies, or the correlation-path
> optimum is strictly less than five.

The rational-density lemma would then finish every strict case.  No current
combinatorial SDP dual proves this disjunction.  In particular, the first
28,000 order-eight residual orbits being exactly closed by rational shared
witnesses is strong evidence but does not establish the remaining order-eight
rows, order nine, or order ten.

The useful rigorous conclusion is therefore the strict-rationalization lemma,
together with the counterexample above to the stronger claim that the known
combinatorial templates alone eliminate the residual census.

## Reproduction

The relevant exact artifacts and audits are:

```sh
python3 research/rank-six-orders7-10-structural-verifier.py
python3 research/rank-six-order-eight-structural-verifier.py
python3 positive-square-energy/experiments/rank6_order8_symbolic_recognizers.py
python3 positive-square-energy/experiments/rank6_order8_sparse_pipeline.py \
  --verify-pack positive-square-energy/experiments/rank6_order8_search_ckpt/chunk-00000-20000.r8g.xz
```
