# Withdrawn synthetic `R31-S:D3` diagnostic packet

Put `D=Theta(1,2,2)` and `sigma(X)=s^+(X)-|V(X)|`.  This note records the
historical synthetic diagnostic inequality

`sigma(D+T^3)>3`.                                             (D3)

It is **not** a remaining physical `R31-S` obligation.  Full-parent adjacency
reconstruction showed that the purported second degree-two diamond vertex has
no physical preimage: each first-simple doubled fibre contributes one actual
triangle.  The physical packet is closed instead by
`r31-s-physical-shared-triangle-closure.md` and
`research/r31-s-physical-parent-verifier.py`.  The coefficient audit below
remains useful evidence about a separate synthetic graph family, but it is not
a closure owner, theorem dependency, or transitive residual.

## Exact finite result that is established

On one doubled side the owner set is `{A,B,x}`, where `x` is the interior
owner.  Requiring `x` among the top roots gives

| shape | one-side records |
|---|---:|
| three direct blocks | `C(5,3)-C(4,3)=6` |
| chain of two plus one direct block | `3^2-2^2=5` |
| fork | `2` |
| chain of three | `1` |

Thus there are `6+5+2+1=14` records on one side and exactly 28 after reflecting
the doubled-`C4`.

For each bare record the finite audit constructs the hull, regenerates every
simple cycle, and forms the multivariate imaginary Sachs polynomial.  After
substituting activities `a_v=t+y_v`, it establishes that every imaginary
activity coefficient is negative except for at most one positive monomial
`6y`.  When that monomial is present, its same-support companions include

`6y-58yt^2-38yt^4-6yt^6`,                                    (1)

and owner-free companions include

`-18t-118t^3-70t^5-10t^7`.                                  (2)

Those exact integer identities are retained as a diagnostic lemma.  They are
not a phase-area certificate.

## The missing implication in the synthetic diagnostic

For

`Psi(t)=i^(-n) det(itI-A)=R(t)+iI(t)`,                         (3)

the desired signed Coulson estimate requires control of the **continuous**
argument of the full complex polynomial for every `t>0` and every legal
nonnegative activity vector.  The old argument asserted that whenever the
exceptional carrier makes `I(t)>=0`, equations (1)--(2), together with a
purported real Sachs comparison, force `R(t)<0`.  It then inferred that all
imaginary-axis crossings occur in the left half-plane and that the continuous
phase has the required sign/area.

The executable audit never constructs or checks the real Sachs expansion used
by that assertion.  It checks only the imaginary activity coefficients.
Moreover, the real activity expansion contains many coefficients of both
signs, so `I>=0 => R<0` does not follow coefficientwise from (1)--(2) without a
new exact factorization, injection, or semialgebraic inequality.  Even a proof
of that pointwise half-plane implication would still have to be connected
explicitly to the required strict phase-area integral.  Consequently the
previous conclusion

`-(4/pi) integral_0^infinity t Arg(Psi(t)) dt > -2`

and hence (D3) are withdrawn.

No graph counterexample to (D3) is asserted here.  The obstruction is a proof
and verification gap: the finite coefficient data are compatible with a true
theorem, but they do not establish it.

## What would prove the synthetic inequality

Any replacement must prove the uniform rooted-tree statement, not merely bare
cores or sampled activities.  Acceptable routes include:

1. an exact multivariate certificate for `I>=0 => R<0`, followed by a rigorous
   continuous-phase winding/area argument with strictness;
2. a direct signed Coulson integral bound with an exact positive decomposition;
3. an induced-piece or Gram inequality proving `sigma(D+T^3)>3` without the
   phase claim; or
4. a coupled doubled-`C4` packet that proves the parent `R31-S` inequality
   directly and thereby makes (D3) unnecessary.

None of these routes is required for the physical `R31-S` theorem.  The
multiblock master still exits nonzero for a different reason: other packet
families have an uncensused, unoriented actual-hull-bridge lane, and the old
generic bridge split is false for rank-one pentagon sides.

## Diagnostic verifier

Run

```text
python3 research/r31-s-d3-diamond-packet-verifier.py
python3 -O research/r31-s-d3-diamond-packet-verifier.py
```

The program must itself exit nonzero.  Its output authenticates the 28-record
census and imaginary-carrier identities, then reports that the real-part and
continuous-phase obligations for the synthetic inequality are unverified.  A
zero exit would be a semantic failure, not a theorem receipt.  This deliberate
failure is diagnostic only and does not reopen physical `R31-S`.
