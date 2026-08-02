# Cycle 264: exact BSD corollary for `43a1`

## Outcome

This is a routine curve-specific corollary of the Cycle 263 theorem and the
standard, exactly normalized Gross--Zagier formula. It is not a new theorem
and has no implication for general BSD.

Let

\[
 E:y^2+y=x^3+x^2,
 \qquad P=(0,0),
\]

and let `Omega_E` denote the full real Neron period. Cycle 263 proves

\[
 E(\mathbf Q)=\mathbf ZP,
 \quad E(\mathbf Q)_{\rm tors}=0,
 \quad \Sha(E/\mathbf Q)=0,
 \quad c_{43}=1.
\]

Consequently the rank-one BSD arithmetic expression is exactly

\[
 \Omega_E\widehat h(P).                                  \tag{264.1}
\]

## Exact analytic comparison

Put `T=E^(-7)`, on the global minimal model

\[
 T:[0,-1,1,-16,-106].
\]

The exact Neron-normalized plus modular symbol of `T` satisfies

\[
 [0]^+_T=2.
\]

In PARI's documented convention,
`[0]^+_T=L(T,1)/Omega_T^+`, where `Omega_T^+` generates the invariant real
homology. For this one-real-component model the BSD real period is
`2 Omega_T^+`. Thus the modular-symbol integration formula gives the exact,
nonzero identity

\[
 L(T,1)=\Omega_T.                                        \tag{264.2}
\]

No decimal period recognition occurs here: the rational symbol is exactly
`2`, and the second factor two is topological, not numerically recognized.

Cycle 261 identifies the normalized class-number-one Heegner point for
`K=Q(sqrt(-7))` exactly as `y_K=P`. The specialized Gross--Zagier formula,
with the strong-Weil parametrization, Manin constant one, Neron
differentials, and full real periods used in that certificate, is

\[
 L'(E,1)L(T,1)
   =\Omega_E\Omega_T\widehat h(y_K).                     \tag{264.3}
\]

Substituting `y_K=P` and (264.2), then cancelling the nonzero period
`Omega_T`, gives the exact equality

\[
 \boxed{L'(E,1)=\Omega_E\widehat h(P)}.                  \tag{264.4}
\]

This use of Gross--Zagier is not circular: it is a height formula independent
of BSD. The proof of `Sha(E/Q)=0` used Kolyvagin's upper bound and 2-descent,
not (264.4) or an analytic BSD quotient. Conversely, (264.4) uses the already
proved exact CM-point identity, not PARI's floating `ellheegner`, `ellbsd`, or
rounded recognition.

The root number is `-1`, so `L(E,1)=0`; equations (264.2)--(264.3), together
with the nontorsion point `P`, show `L'(E,1) != 0`. Hence the analytic order
is exactly one. Comparing (264.4) with (264.1) proves the full BSD
leading-coefficient formula for this one curve.

## Reproduction and scope

The finite exact modular-symbol check is replayed by
`43a1/verify_43a1_bsd_symbol.gp`. Its output certifies the rational symbol and
the algebraic local data; Gross--Zagier and the modular-symbol integration
formula remain ordinary published-theorem trust boundaries.

This corollary says only that BSD, including the exact leading coefficient,
holds for `43a1`. It proves no family statement and no case of the general
rank conjecture beyond this specified curve. No novelty is claimed.
