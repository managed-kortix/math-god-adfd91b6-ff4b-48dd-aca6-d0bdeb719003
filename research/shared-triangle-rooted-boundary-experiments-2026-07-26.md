# Exact rooted boundary experiments for shared triangular clusters

## Retraction notice

The surplus calculations in the original version of this note omitted
algebraic multiplicities of repeated positive eigenvalues. In particular, the
bare central-triangle/three-petal core has `sigma=6`, not `sigma=3`. The strict
bound `sigma>3` is valid uniformly with arbitrary attached trees by the
matching-injection and Coulson argument. Treat the surplus increments and
monotonicity comparisons below as retracted pending a fresh audit of the
regenerated multiplicity-aware certificate. See
`research/central-three-petal-bound-repair-2026-07-26.md`.

## Verdict

The exact experiment supports a boundary-sensitive invariant, but not a simple
additive margin per triangle.

For a rooted graph `(G,v)`, the complete response to attaching an arbitrary
rooted tree `(T,r)` at `v` is the rational function

`a_T(x)=phi_T(x)/phi_(T-r)(x)-x`.                                 (1)

Indeed, identifying `v` and `r` gives

`phi_(G vee T)(x)=phi_(T-r)(x)[phi_G(x)+a_T(x) phi_(G-v)(x)]`.    (2)

Thus the exact boundary state is the projective pair

`[phi_G(x):phi_(G-v)(x)]`,                                      (3)

or equivalently the rooted ratio `R_G=phi_G/phi_(G-v)`. Every
rooted-tree attachment translates the ratio by `a_T` and multiplies by the
root-deleted forest factor. This is the natural invariant to test in a rooted
Coulson or matching-polynomial proof. The unrooted surplus `sigma(G)` alone
does not determine the attachment response.

The computations also expose two false natural conjectures. In common-cut
triangle bouquets, a new boundary triangle can raise surplus by much less than
one. Moreover, on the tested common-cut boundaries a hostile pentagon raises
surplus *more* than a triangle, despite the pentagon's negative isolated
ledger. Hostility is therefore not monotone under rooted gluing.

All claims below have integer characteristic polynomials and rational Sturm
certificates in
`research/shared-triangle-rooted-exact-certificate.json`. The generator is
`research/shared_triangle_rooted_exact.py`. Neither file uses floating-point
arithmetic. Decimal approximations are intentionally omitted.

## 1. Exact method

The script builds the adjacency matrix over the integers and computes
`phi_G=det(xI-A)` by Newton identities from the exact traces
`tr(A),...,tr(A^n)`. Positive roots are isolated by a Sturm sequence over
`fractions.Fraction`. If the disjoint rational intervals are `[l_i,u_i]`, then

`sum_i l_i^2-|V(G)| <= sigma(G) <= sum_i u_i^2-|V(G)|`.          (4)

The displayed certificate records every `[l_i,u_i]` and both rational endpoints
in (4). A sign or comparison is asserted only when the appropriate rational
intervals are disjoint. Repeated zero roots are removed before positive-root
isolation; they contribute nothing to `s+`.

The rooted coalescence identity (2) follows from the standard vertex formula

`phi_(G vee T)=phi_(G-v)phi_T+phi_G phi_(T-r)-x phi_(G-v)phi_(T-r)`.

This is useful computationally and conceptually: arbitrary finite rooted trees
do not require an ever-growing list of graph shapes. They enter through one
rational transfer `a_T`.

Sample exact transfers from the certificate are

| rooted tree | `a_T(x)` |
|---|---|
| one vertex | `0` |
| edge rooted at an end | `-1/x` |
| three-vertex path rooted at an end | `-x/(x^2-1)` |
| three-vertex path rooted at its middle | `-2/x` |
| four-vertex path rooted at an end | `(-x^2+1)/(x^3-2x)` |
| claw rooted at its center | `-3/x` |
| claw rooted at a leaf | `-x^2/(x^3-2x)` |

Different rooted trees can have the same transfer. For example, the four-
vertex path rooted at an inner vertex and the claw rooted at a leaf both have
`-x^2/(x^3-2x)`. Equation (2) then shows that their effect differs only through
the multiplicative root-deleted characteristic polynomial. This is an exact
rooted equivalence, not a numerical coincidence.

## 2. Boundary sensitivity of four-triangle packets

Two four-triangle shared clusters have sharply different spectra.

The common-cut bouquet, in which all four triangles share one root, has

`phi=x^9-12x^7-8x^6+30x^5+24x^4-28x^3-24x^2+9x+8`,             (5)

and its rational Sturm certificate puts `sigma` strictly above `3`.

The central-triangle/three-petal cluster has

`phi=x^9-12x^7-8x^6+42x^5+48x^4-36x^3-72x^2-27x`,              (6)

and factors as

`phi=x(x-3)(x^2-3)(x^5+3x^4-8x^2-9x-3)`.                       (7)

Its two positive roots are `3` and `sqrt(3)`, so

`s+=9+3=12`, and `sigma=12-9=3` exactly.                         (8)

This equality is important. It is a counterexample to the previously recorded
strict four-triangle claim `sigma>3`, because the allowed class includes the
bare core. Consequently every downstream argument using that strict base must
be weakened or repaired. In particular, the recurrence based on this packet
gives at most `sigma>=7-r` from this incidence, not strict `>7-r`. The likely
fault is the strict matching-polynomial/phase-to-energy step in the exceptional
central-petal proof: the exact spectrum forces `s+=s-=12`, so that argument
cannot yield strict square-energy imbalance for this graph.

The certificate tests seven nontrivial rooted trees at a selected boundary of
each of the central-petal packet, common-cut packet, and a five-triangle chain.
All 21 resulting graphs have rationally certified positive surplus. But the
surplus can move in either direction: several tree attachments lower the
common-cut or chain surplus, whereas all sampled attachments raise the bare
central-petal value. Thus `sigma` is neither attachment-monotone nor a complete
boundary state. The pair (3), not one scalar margin, controls the operation.

## 3. Exact hostile-pentagon comparisons

At the selected root, the experiment compares the same base packet after
adding either a triangle petal or a pentagon petal. Let

`Delta_k(G,v)=sigma(G with a rooted C_k petal at v)-sigma(G)`.   (9)

Every interval below is copied from the rational certificate; inequalities are
proved by cross-multiplication of integers.

For the four-triangle common-cut bouquet,

`Delta_3 < 6369216888783828830958013 /`
`          19342813113834066795298816 < 1`,                     (10)

while

`Delta_5 > 232853434990625338225528837 /`
`          309485009821345068724781056`.                         (11)

The lower bound in (11) is strictly larger than the upper bound in (10).
Consequently

`0 < Delta_3 < Delta_5`                                         (12)

is an exact statement for this rooted boundary.

For the seven-triangle common-cut bouquet, similarly,

`Delta_3 < 1268698672844889451627672061 /`
`          4951760157141521099596496896 < 1`,                    (13)

and

`Delta_5 > 61583779836531785615968303 /`
`          77371252455336267181195264 > Delta_3`.                (14)

The central-three-petal and five-triangle-chain samples behave differently:
there `Delta_3>Delta_5>0`. The ordering of triangle and pentagon increments is
therefore itself boundary-sensitive.

These observations do not prove arbitrary-tree absorption of a hostile
pentagon. They do show that charging the isolated deficit
`delta_5=sqrt(5)-2` after gluing can be very misleading: a pentagon that is
hostile as a singleton can be favorable at a locked common cut.

## 4. False conjectures and certificates

**False conjecture A.** Adding one triangle at a boundary raises `sigma` by at
least one.

The four-triangle common-cut bouquet is a counterexample by (10). The
seven-triangle bouquet is another by (13). These are exact spectral
counterexamples, not failures of a decomposition method.

**False conjecture B.** At a fixed boundary, a hostile pentagon contributes no
more surplus than a triangle.

Both common-cut bouquets refute this by the disjoint rational intervals
(10)--(14). In contrast, the central-petal and chain samples have the opposite
ordering. No boundary-free ordering survives.

**False conjecture C.** A positive unrooted margin predicts resistance to tree
attachments.

The common-cut four-triangle core has surplus strictly above `3`, yet attaching
a three-vertex path at its root yields a certified surplus strictly below `3`.
Likewise, the five-triangle chain's sampled rooted trees all lower its surplus.
An unrooted scalar cannot support the desired guard-export induction.

**Counterexample to the recorded strict packet theorem.** The bare central-
three-petal core has `sigma=3` exactly by (7)--(8), while it satisfies the
stated hypotheses of the claimed four-triangle shared-cluster theorem. This is
not merely absence of a uniform gap. It falsifies strict `sigma>3` as stated.
Any use of strictness at ranks four through seven needs an independent repair.

## 5. Candidate invariant and next analytic target

The experiment suggests keeping the rooted Weyl/Schur data

`R_(G,v)(x)=phi_G(x)/phi_(G-v)(x)`                              (15)

on the imaginary axis, together with the signless matching analogue used by
the Sachs-phase argument. A rooted tree attachment performs

`R -> R+a_T`,                                                     (16)

before multiplication by a forest factor. A boundary lemma should therefore
seek a pointwise half-plane, argument, or domination region for `R(ix)` that
is invariant under the class of tree transfers `a_T(ix)`. A scalar lower bound
on `sigma` is too coarse and, as the counterexamples show, need not be monotone.

For the locked common-cut target, all lobes meet at one root, so their Schur
corrections add. This makes the bouquet analytically simpler than arbitrary
incidence trees and is the best next test case for common-cut absorption:

1. derive the exact `R(ix)` recursion for a triangle lobe, pentagon lobe, and
   arbitrary rooted forest activity;
2. identify a rational inequality or argument cone preserved when triangle
   lobes are added;
3. prove that one pentagon plus at least one triangle remains in the favorable
   cone for every admissible rooted-tree activity;
4. then test whether the same two-coordinate state composes along binary
   shared cuts.

The current data are evidence for this route, not a proof of the all-rank
candidate lemma. The exact deliverable is narrower: it identifies the minimal
rooted characteristic-polynomial state, certifies substantial boundary
sensitivity, and supplies explicit counterexamples to two plausible additive
margin conjectures.

## Reproduction

Run

```text
python research/shared_triangle_rooted_exact.py --bits 36 \
  --output research/shared-triangle-rooted-exact-certificate.json
```

The script requires only the Python standard library. Increasing `--bits`
refines all dyadic Sturm intervals without changing the symbolic
characteristic polynomials or rooted transfer identities.
