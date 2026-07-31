# Cycle 193: certified cubic arithmetic behind the 2-Selmer upper bounds

## Result

PARI/GP 2.15.4 freshly reruns `ellrank` and returns the following raw records:

| `D` | minimal model | `ellrank(E,0)` |
|---:|:---|:---|
| `-1499` | `[1,0,1,-46813,-3372156843]` | `[1,1,0,L]` |
| `-29023` | `[1,1,1,-17548636,-24475377572834]` | `[1,1,0,[]]` |

The definitive conservative interpretation retains only the certified
2-Selmer upper bound one from the descent data. For `D=-1499`, the separately
checked exact non-torsion point supplies the lower bound, so its rank is exactly
one. For `D=-29023`, the empty point list supplies no lower-bound witness, so
the certified rank interval is `[0,1]` until an exact point or rigorous analytic
nonvanishing proof is provided. The raw first coordinate returned by `ellrank`
is recorded for reproducibility but is not promoted to a certificate here.

## Certified cubic field

The scaled 2-division cubics used by the descent are

```text
D=-1499:  x^3 + x^2 - 749000*x - 215818037936
D=-29023: x^3 + 5*x^2 - 280778168*x - 1566424164661360
```

Although their polynomial discriminants contain `D^6`, `polredabs` reduces
both to the same cubic field

```text
K = Q(theta),  theta^3 + theta - 8 = 0.
```

This is expected because quadratic twisting does not change the Galois module
`E[2]`. Running `bnfinit(x^3+x-8,1)` and then full `bnfcertify` gives

```text
CUBIC_DISCRIMINANT=-1732
CUBIC_SIGNATURE=[1, 1]
CUBIC_CLASS_GROUP=[2, [2], [[2, 0, 1; 0, 2, 1; 0, 0, 1]]]
CUBIC_FUNDAMENTAL_UNITS=[Mod(-6*x + 11, x^3 + x - 8)]
CUBIC_TORSION_UNITS=[2, -1]
BNFCERTIFY_QUOTIENT=1
BNFCERTIFY_FULL=1
```

Therefore the relevant cubic field's full class group and full unit group are
certified unconditionally, not merely under the GRH assumptions normally
attached to raw `bnfinit` output. The class group is `Z/2Z`, the unit rank is
one, and `-6*theta+11` is a fundamental unit (up to the torsion unit `-1`).
There are not two distinct cubic class/unit groups to certify: the two twist
cubics define this same field.

This certification closes a possible hidden-GRH concern in the cubic
class/unit arithmetic used for the 2-descent upper bound. It is not a second
implementation of 2-descent, does not certify `ellrank`'s lower endpoint, and
does not prove that a locally soluble cover has a rational point. Thus it proves
the Selmer/rank upper bound, while lower bounds must come from independent
points or certified analytic arguments.

## Reproduction

Run the committed fail-closed verifier:

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/verify_cycle193_bnf_rank_certification.gp
```

The complete output on this host is:

```text
PARI_VERSION=[2, 15, 4]
CUBIC_REDUCED_POLYNOMIAL=x^3 + x - 8
CUBIC_DISCRIMINANT=-1732
CUBIC_SIGNATURE=[1, 1]
CUBIC_CLASS_GROUP=[2, [2], [[2, 0, 1; 0, 2, 1; 0, 0, 1]]]
CUBIC_FUNDAMENTAL_UNITS=[Mod(-6*x + 11, x^3 + x - 8)]
CUBIC_TORSION_UNITS=[2, -1]
BNFCERTIFY_QUOTIENT=1
BNFCERTIFY_FULL=1
D=-1499
MINIMAL_MODEL=[1, 0, 1, -46813, -3372156843]
TWO_DIVISION_CUBIC=x^3 + x^2 - 749000*x - 215818037936
TWO_DIVISION_CUBIC_DISCRIMINANT=[-1, 1; 2, 8; 433, 1; 1499, 6]
TWO_DIVISION_CUBIC_POLREDABS=x^3 + x - 8
ELLRANK_RAW=[1, 1, 0, [[399030891253207/156180668809, 7009131418974188521075/61722131771310373]]]
CERTIFIED_2SELMER_DIMENSION_UPPER_BOUND=1
CERTIFIED_ALGEBRAIC_RANK_INTERVAL=[1, 1]
D=-29023
MINIMAL_MODEL=[1, 1, 1, -17548636, -24475377572834]
TWO_DIVISION_CUBIC=x^3 + 5*x^2 - 280778168*x - 1566424164661360
TWO_DIVISION_CUBIC_DISCRIMINANT=[-1, 1; 2, 8; 433, 1; 29023, 6]
TWO_DIVISION_CUBIC_POLREDABS=x^3 + x - 8
ELLRANK_RAW=[1, 1, 0, []]
CERTIFIED_2SELMER_DIMENSION_UPPER_BOUND=1
CERTIFIED_ALGEBRAIC_RANK_INTERVAL=[0, 1]
CERTIFICATE_STATUS=PASS
```

## Sage/mwrank audit

Sage is not installed on this host. Debian's independent eclib `mwrank`
20231211 was installed and invoked as follows:

```sh
printf '%s\n' '[1,0,1,-46813,-3372156843]' | mwrank -q -v 1 -s
printf '%s\n' '[1,1,1,-17548636,-24475377572834]' | mwrank -q -v 1 -s
```

It began its binary-quartic descent, reported one invariant pair and the
2-adic index `1`, but did not finish within a 20-minute limit even for the
first curve. A separate 15-minute run on the direct `D=-1499` twist reached
the nontrivial quartic `(1499,0,-10493,8994,-5996)` before timing out; the
`D=-29023` search only reached the range with leading coefficient up to
`66586`. These are useful independent intermediate checks, but they are not
claimed as completed mwrank rank certificates.
