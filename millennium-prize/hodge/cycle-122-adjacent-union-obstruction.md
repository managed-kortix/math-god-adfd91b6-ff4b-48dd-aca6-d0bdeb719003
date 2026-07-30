# Cycle 122: adjacent Hermitian-plane union obstruction

The Hodge main funnel tests whether interacting characteristic-two planes can
lift as one subscheme even when their components do not.  The first exact pair
is obstructed.

Over `k=F_2[t]/(t^5+t^2+1)`, let `A` be the Cycle 118 matrix and

\[
 u=(1,t,t+1)^t.
\]

Then `A-I=uu^t` has rank one.  Hence the graph planes `L_A` and `L_I`
intersect in a projective line.  Their span is a projective three-space with
coordinates

\[
 y=x+us,
\]

and their reduced union is the `(1,1,2)` complete intersection

\[
 q=s(s+u^tx)=0
\]

in characteristic two.  Its fundamental cycle remains alpha-visible because
`P_alpha(A)=t^12` and `P_alpha(I)=0`.

The exact verifier works in `W_2(F_32)` with true Witt-vector addition,
multiplication, negation, and division by two.  This is essential: Teichmuller
lifts are multiplicative but not additive.  It restricts the standard
degree-33 Fermat equation to a lifted spanning `P^3`, reduces modulo the lifted
quadric `s(s-U)=0`, and forms the divided remainder `h` over `F_32`.

The complete embedded first-order normal map is

\[
 H^0(O_Z(1))^{\oplus2}\oplus H^0(O_Z(2))
 \longrightarrow H^0(O_Z(33)),
\]

with `17` columns in a target of dimension `1156`.  Exact sparse elimination
gives

\[
 \operatorname{rank}M=17,\qquad
 \operatorname{rank}[M\mid h]=18.
\]

Thus `h` is not in the image: `L_A union L_I` has no flat embedded lift inside
the standard Fermat hypersurface over `W_2(F_32)`.  This is a nonlinear union
obstruction, not an invalid sum of component Hilbert obstructions.

Among all `1023` line-intersecting orthogonal neighbors, three candidates pass
the weaker screen in which all nine component middle obstruction coordinates
cancel while the alpha coefficient remains nonzero.  The preferred candidate
uses `z=(1,t+1,t)` in `B=A(I+zz^t)`.  Its full reducible-union normal map has not
yet been certified.  That is the next exact experiment.

The result excludes only this adjacent pair.  It does not obstruct every pair,
relative Chow classes, higher unions, compatible `W_n` lifts, or the Hodge
conjecture.
