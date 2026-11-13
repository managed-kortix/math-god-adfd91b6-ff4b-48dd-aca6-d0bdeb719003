# The `R31-S` interior-owner diamond plus three triangles: open analytic packet

Put `D=Theta(1,2,2)` and `sigma(X)=s^+(X)-|V(X)|`.  The remaining
interior-owner obligation in the doubled-`C4` frontier is

`sigma(D+T^3)>3`.                                             (D3)

The incidence hull is bridge-free, the three triangular blocks may be direct,
repeated at one cut, or nested, and arbitrary finite rooted trees are allowed
at every vertex.  **This packet is open in the committed proof system.**  The
coefficient audit described below is useful exact evidence, but it does not
prove (D3).

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

## The missing implication

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

## What would close the packet

Any replacement must prove the uniform rooted-tree statement, not merely bare
cores or sampled activities.  Acceptable routes include:

1. an exact multivariate certificate for `I>=0 => R<0`, followed by a rigorous
   continuous-phase winding/area argument with strictness;
2. a direct signed Coulson integral bound with an exact positive decomposition;
3. an induced-piece or Gram inequality proving `sigma(D+T^3)>3` without the
   phase claim; or
4. a coupled doubled-`C4` packet that proves the parent `R31-S` inequality
   directly and thereby makes (D3) unnecessary.

Until one of these is committed and adversarially verified, the authoritative
owner ledger has final residual `R31-S`, and the multiblock master exits
nonzero.

## Diagnostic verifier

Run

```text
python3 research/r31-s-d3-diamond-packet-verifier.py
python3 -O research/r31-s-d3-diamond-packet-verifier.py
```

The program must itself exit nonzero.  Its output authenticates the 28-record
census and imaginary-carrier identities, then reports that the real-part and
continuous-phase obligations are unverified.  A zero exit would be a semantic
failure, not a theorem receipt.
