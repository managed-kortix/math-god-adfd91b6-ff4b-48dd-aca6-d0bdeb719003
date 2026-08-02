# Cycle 241: exact KI240 toy-projector search

## Result

No `KI240 FAIL` packet is obtained.  The first algebraic models that retain the
actual self-Ext algebra and the actual degree-three cross-Ext grading have an
exact corner obstruction: every noncentral projector available in the smallest
cross-Hom atom is a graph projector, and conjugating a summand into a graph does
not remove its Atiyah corner.  This is a bounded structural rejection, not an
exhaustion of arbitrary finite packets and therefore not `KI240 PASS` or
`KI240 WALL`.

## Actual Ext model

For each generator use

\[
 \operatorname {Ext}^*(F_k,F_k)=\Lambda^*\mathbb Q^6,
\]

with dimensions `(1,6,15,20,15,6,1)`.  For distinct generators retain the
Cycle 199 calculation

\[
 \operatorname {Ext}^r(F_i,F_j)=0\quad(r\ne3).
\]

Positive self-Ext classes therefore annihilate a cross degree-three class:
their products would lie in a cross group of degree greater than three, which
is zero.  Opposite cross products can first return in self degree six, never in
the degree-two Atiyah corner.  These are actual Ext products, not a quiver with
invented degree-one arrows.

The nine rational PEL basis vectors are the matrix units `B_rs`.  For
`u^k=a_k+b_k i`, the graph obstruction used in the search is

\[
 \rho_k(B)=Q^{-1}B^t-(a_k^2+b_k^2)B,
 \qquad Q=\operatorname {diag}(1,1,3).
\]

Exact row reduction gives ranks

\[
 (6,9,9,9,9,9,9).
\]

Thus every generator has a printed basis direction with nonzero raw
obstruction.  The computation uses `Fraction`, with no floating arithmetic.

## First noncentral atom

A degree-zero cross map between distinct shifted generators first occurs when
their shifts differ by three.  On one such cross basis vector the degree-zero
endomorphism algebra is the upper-triangular algebra.  Write

\[
 e=\begin{pmatrix}a&x\\0&b\end{pmatrix}.
\]

The exact idempotent equations are

\[
 a^2-a=0,\qquad b^2-b=0,\qquad(a+b-1)x=0.             \tag{241.1}
\]

The noncentral solutions are the graph families
`[[1,x],[0,0]]` and `[[0,x],[0,1]]`.  If `o` is a nonzero diagonal
degree-two graph obstruction, cross-degree vanishing gives

\[
 (eoe)_{11}=o_{11}\ne0
\]

on the selected graph summand.  Hence the noncentral parameter changes the
embedding but cannot make even one nonzero diagonal corner a boundary.

Singular independently imposes (241.1), both independent raw-corner equations
`a=b=0`, and the saturation equation `t(a+b)-1=0` requiring nonzero diagonal
K-class.  The Groebner basis is the unit ideal.  It also verifies that `x`
remains free after setting `(a,b)=(1,0)`, so the calculation does include a
genuine noncentral family rather than silently reducing to central projectors.

## Boundary of the computation

This rules out only zero-differential packets supported on one cross-Hom atom.
It does not classify projectors on longer twisted complexes with self-Ext-one
differentials.  Such a search requires chain-level or minimal-`A_infinity`
structure constants for the seven-generator dg subcategory and chain-level
representatives of all nine Atiyah cocycles.  Cycles 199--201 print Ext groups
and the products needed for their no-go arguments, but not this full finite
input.  Substituting generic constants would cease to preserve the actual Ext
structure and could manufacture a false packet.

Therefore the exact status is `KI240 INCOMPLETE`: the smallest noncentral toy
families meet a unit-ideal corner obstruction, while no valid all-nine-boundary
packet is known.

Reproduce with

```sh
python3 millennium-prize/hodge/verify_cycle241_ki240_toy_search.py
Singular -q millennium-prize/hodge/cycle241_ki240_toy_idempotents.sing
```
