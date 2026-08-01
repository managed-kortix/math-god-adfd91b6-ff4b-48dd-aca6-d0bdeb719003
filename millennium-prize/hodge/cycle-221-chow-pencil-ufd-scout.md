# Cycle 221: Chow-pencil UFD scout and common-factor counterexample

## Question

In the Cycle 218 notation put

\[
 P=F_{Y^+}F_{C_0^-},\qquad Q=F_{Y^-}F_{C_0^+}
\]

in the polynomial UFD containing the chosen Chow forms. Suppose the whole
projective pencil `[sP+tQ]` consists of Chow forms. Does unique factorization
force a common Chow factor or a componentwise factorization of the pencil?

It does not. UFD geometry gives a useful fixed-factor constraint, but the
claim that the pencil must factor componentwise is false, even when both
endpoints are reduced reducible cycles and the general member is integral.

## Exact UFD constraint

Let `R=k[u_1,...,u_N]`, let `P,Q` be nonzero homogeneous forms of the same
degree, and assume they are not proportional. Write

\[
 g=\gcd(P,Q),\qquad P=gp,\qquad Q=gq,
 \qquad \gcd(p,q)=1.                                      \tag{221.1}
\]

Then `sp+tq` is irreducible in `R[s,t]`. Indeed, regard it as a primitive
degree-one polynomial in `s` over `R[t]`. A nontrivial factorization would
have one factor of degree zero in `s`; comparison of the coefficient of `s`
and the constant coefficient would make that factor divide both `p` and `q`.
Gauss's lemma gives the assertion.

Consequently

\[
 sP+tQ=g(sp+tq)                                           \tag{221.2}
\]

is the complete universal factorization over `R[s,t]`: `g` is precisely the
fixed divisorial factor. For two distinct scalar members, with
`st'-s't != 0`, Bezout elimination in the two pencil coordinates gives

\[
 \gcd(sP+tQ,s'P+t'Q)=\gcd(P,Q)=g.                         \tag{221.3}
\]

The same statement can be phrased using subresultants: after choosing one
Chow coordinate as the polynomial variable and passing to the fraction field
of the other coordinates, the last nonzero subresultant recovers `g`; no new
factor can persist on two distinct members. A multivariate Macaulay resultant
should not be used naively here, since it detects a common projective zero, not
a common hypersurface factor.

If the general member of the Chow pencil is geometrically integral, its Chow
form is irreducible. Equation (221.2) then forces

\[
 \boxed{\gcd(P,Q)=1.}                                     \tag{221.4}
\]

For Cycle 218 this says that the two endpoint sums have no common irreducible
cycle component. Assuming the displayed factors are normalized, (221.4)
implies all four cross-coprimality conditions

\[
\begin{aligned}
 &\gcd(F_{Y^+},F_{Y^-})=1,
 &&\gcd(F_{Y^+},F_{C_0^+})=1,\\
 &\gcd(F_{C_0^-},F_{Y^-})=1,
 &&\gcd(F_{C_0^-},F_{C_0^+})=1.                            \tag{221.5}
\end{aligned}
\]

Thus a candidate endpoint cannot contain a component of the opposite
endpoint or of the opposite reference cycle. These are necessary open
conditions, not an emptiness proof.

## Counterexample to stronger factorization

Take `X=P^3_k` over an algebraically closed field of characteristic not two.
In the complete linear system of quadric divisors set

\[
 P=xy,\qquad Q=zw.                                        \tag{221.6}
\]

Multiplicativity of Chow forms for sums identifies the endpoints with the
reduced cycles

\[
 V(x)+V(y),\qquad V(z)+V(w).
\]

Every member

\[
 V(sxy+tzw)                                               \tag{221.7}
\]

is an effective quadric divisor, hence its point in the projective space of
quadrics is a Chow point. The endpoint polynomials have gcd one. If `st != 0`,
the quadratic form `sxy+tzw` has rank four, so it is irreducible: a reducible
quadric is a product of two linear forms and has rank at most two. Thus the
general cycle is geometrically integral even though both endpoints are reduced
and reducible.

This example has exactly the relevant algebraic behavior: multiplication at
the two sums, addition along the Chow-coordinate line, disappearance of all
endpoint factors in the interior, and no common factor. It also explains why
factoring `sp+tq` over `R[s,t]` cannot settle the incidence. Specialization can
merge endpoint components into an irreducible general cycle, while in other
examples geometric factorization may require algebraic extensions of
`k(s/t)` and need not descend to `k(s/t)`.

## Consequence for the frozen architecture

Irreducibility and resultants add (221.5) as cheap fail-closed witnesses to the
Cycle 218 moving-support open. They do not imply that one of `Y^+`, `Y^-`
shares a reference component, and they do not make the secant incidence empty.
Any no-go must use the higher-codimension Cayley--Chow equations of
`Chow_(3,D)(A_0)`, the geometry of `A_0`, or the relative tangent/jet
conditions. UFD factorization alone cannot retire the degree-one secant
architecture.

This is an exact structural scout and counterexample, not a point of the Cycle
218 incidence and not a Hodge-conjecture result.
