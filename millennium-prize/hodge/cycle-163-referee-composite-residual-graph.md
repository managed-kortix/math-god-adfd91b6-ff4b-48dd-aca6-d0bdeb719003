# Cycle 163: referee audit of the composite residual graph

The order and graph assertions in Cycle 162 are valid over arbitrary
prime-power torsion, including nonfree isotropic intersections, provided the
ambient decomposition has two factors of the same order and `K` is
Lagrangian.  The proof below supplies the missing point: the projections of
`K` are exactly `A_K^perp` and `B_K^perp`.

## Finite-group theorem

Let `R=Z/p^e Z`.  Let `G` and `H` be finite `R`-modules equipped with perfect
alternating pairings into `R`, and give

\[
M=G\perp H
\]

the orthogonal-sum pairing.  Let `K\leq M` be Lagrangian, meaning
`K=K^perp`.  Define

\[
A=K\cap G,\qquad B=K\cap H,
\]

and let

\[
C=\operatorname{pr}_G K,\qquad D=\operatorname{pr}_H K.
\]

Then

\[
\boxed{C=A^\perp,\qquad D=B^\perp.}
\]

Moreover `K/(A\oplus B)` is canonically the graph of an anti-isometry

\[
\phi:C/A\overset{\sim}{\longrightarrow}D/B.
\]

No freeness assumption on `A`, `B`, `C`, `D`, or `K` is used.

### Proof of the projection identities

For every `a in A` and `(g,h) in K`, isotropy gives

\[
0=\langle(a,0),(g,h)\rangle=\langle a,g\rangle_G.
\]

Thus `C subset A^perp`; similarly, `D subset B^perp`.  The converse
inclusions follow from a simultaneous order argument.

The projection sequence

\[
0\longrightarrow B\longrightarrow K\overset{\operatorname{pr}_G}{
\longrightarrow}C\longrightarrow0
\]

gives `|C|=|K|/|B|`.  Perfectness gives
`|S^perp|=|G|/|S|` for every subgroup `S` of `G`, and likewise in `H`.
Since a self-annihilating subgroup of a finite perfectly paired group has
`|K|^2=|M|=|G||H|`, the inclusions and the two projection sequences yield

\[
\frac{|K|}{|B|}\leq\frac{|G|}{|A|},\qquad
\frac{|K|}{|A|}\leq\frac{|H|}{|B|}.
\]

Multiplying and using `|K|^2=|G||H|` shows that equality holds in both.
Hence `C=A^perp` and `D=B^perp`.

### Proof of the residual graph

Send the class of `(g,h) in K` modulo `A direct-sum B` to `(g+A,h+B)`.
Its image lies in `(C/A) direct-sum (D/B)`.  Its kernel is exactly
`A direct-sum B`.  Projection of the image to `C/A` is surjective by the
definition of `C`; if `g in A`, subtract `(g,0) in A` and obtain `(0,h) in K`,
so `h in B`.  Thus that projection is also injective.  The same argument
applies to `D/B`.  The image is consequently the graph of a unique
isomorphism `phi:C/A -> D/B`.

For `(g,h),(g',h') in K`, isotropy says

\[
\langle g,g'\rangle_G+\langle h,h'\rangle_H=0.
\]

The pairings descend to `C/A=A^perp/A` and `D/B=B^perp/B`, so `phi` is
anti-symplectic (more precisely, an anti-isometry of the induced perfect
alternating finite modules).  The induced quotient pairings are perfect even
when `A` and `B` are nonfree: the annihilator of `A^perp/A` is
`(A^perp)^perp/A=A/A`, using perfectness and the finite-cardinality identity
`|S^perp|=|G|/|S|`.

## Equality of the two intersections

The theorem does **not** imply `|A|=|B|` unless `|G|=|H|`.  From either
projection identity,

\[
\frac{|K|}{|B|}=\frac{|G|}{|A|},
\]

and therefore

\[
\boxed{\frac{|A|}{|B|}=\sqrt{\frac{|G|}{|H|}}.}
\]

In Cycle 162, `G` and `H` are both rank-six symplectic `R`-modules, so
`|G|=|H|=p^{6e}` and

\[
\boxed{|A|=|B|=:\delta.}
\]

This proves the claimed equality without assuming that either intersection is
free or a direct summand.

## Exact residual order and `eta^2`

Assume now `|G|=|H|=N^2`; in the application `N=p^{3e}` locally and
`N=m^3` globally.  Since `|K|=sqrt(|G||H|)=N^2`, the subgroup
`A direct-sum B` has order `delta^2`.  Hence

\[
\boxed{|K/(A\oplus B)|=\frac{N^2}{\delta^2}
=\left(\frac{N}{\delta}\right)^2.}
\]

With `eta=N/delta`, this is exactly `eta^2`.  It also follows from the graph:

\[
|A^\perp/A|=\frac{|G|}{|A|^2}
=\frac{N^2}{\delta^2}=\eta^2.
\]

Thus `eta` is an integer.  Indeed `A subset A^perp` gives
`delta^2 <= |G|=N^2`, and `delta` is a power of `p`; locally this implies
`delta divides N`.  Chinese remaindering gives the corresponding assertion for
arbitrary `m`.

## Nonfree stress test

Take `R=Z/p^2 Z`, let `G=H=R^2` with the standard symplectic form, and put

\[
A=pG,\qquad B=pH,\qquad K=A\oplus B.
\]

Here `A` and `B` are isomorphic to `(Z/p Z)^2`, hence are not free as
`R`-modules.  Also `A=A^perp`, `B=B^perp`, so `K=K^perp` in `G perp H`.
One has

\[
|A|=|B|=p^2,\quad |K|=p^4,\quad
K/(A\oplus B)=0,
\]

while `N=p^2` and `eta=N/delta=1`.  The formula gives residual order
`1=eta^2`, exactly as required.

A nontrivial nonfree residual example is obtained over `R=Z/p^3 Z` by taking
`A=p^2G`, `B=p^2H`.  Then `A^perp=pG`, and any anti-symplectic isomorphism

\[
pG/p^2G\simeq pH/p^2H
\]

defines a Lagrangian inverse-image graph `K`.  Here `delta=p^2`, `N=p^3`, and

\[
|K/(A\oplus B)|=p^2=eta^2.
\]

## Counterexample to the unqualified equality

Equal ambient factor orders are essential.  Let `G` be a symplectic plane over
`F_p`, let `H=0`, and let `K` be a Lagrangian line in `G`.  Then `K` is
Lagrangian in `G perp H`, but

\[
|K\cap G|=p\ne1=|K\cap H|.
\]

Therefore the Cycle 162 sentence should read: projection and orthogonality,
**together with `|G|=|H|` and `K=K^perp`**, give `|A_K|=|B_K|`.  Under those
hypotheses the equality and the `eta^2` formula are fully valid for arbitrary
`Z/p^e Z`-modules and nonfree isotropic subgroups.
