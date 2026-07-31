# Cycle 192: exact PARI 2-descent and the large-point obstruction

## Result

Let `E=433a1`, with model

\[
 E: y^2+xy=x^3+1,
\]

and let `E^(D)` be its quadratic twist for `D=-1499,-29023`. PARI/GP 2.15.4
returns `ellrank` records `[1,1,0,L]`. Conservatively separating the certified
descent upper bound from lower-bound evidence gives

\[
 \operatorname{rank}E^{(-1499)}(\mathbf Q)=1,
 \qquad 0\leq\operatorname{rank}E^{(-29023)}(\mathbf Q)\leq1.
\]

For each curve `ellrank` returns `[1,1,0,L]`. Both curves have trivial rational
2-torsion. The `bnfcertify`-certified cubic class/unit arithmetic described in
Cycle 193 proves the descent upper bound

\[
 \dim_{\mathbf F_2}\operatorname{Sel}^{(2)}(E^{(D)}/\mathbf Q)\leq1.
\]

For `D=-1499`, the exact point below supplies rank at least one, so the rank and
2-Selmer dimension are exactly one and the Kummer sequence gives
`Sha(E^(-1499))[2]=0`. For `D=-29023`, no lower-bound witness is known: its
rank remains in `[0,1]`, its 2-Selmer dimension is only bounded above by one,
and `Sha(E^(-29023))[2]=0` is not claimed. None of these conclusions uses the
numerical analytic-rank output.

## Exact models and covers

The global minimal models and conductors are

| `D` | minimal coefficients `[a1,a2,a3,a4,a6]` | conductor |
|---:|:---|---:|
| `-1499` | `[1,0,1,-46813,-3372156843]` | `972951433 = 433*1499^2` |
| `-29023` | `[1,1,1,-17548636,-24475377572834]` | `364730851057 = 433*29023^2` |

Both have root number `-1`, Tamagawa product `2`, and trivial rational
torsion. A basis for the everywhere locally soluble 2-covers consists of one
quartic in each case:

\[
\begin{aligned}
C_{1499}:\quad z^2={}&-1499x^4+2998x^3+7495x^2+8994x-1499,\\
C_{29023}:\quad z^2={}&-29023x^4-58046x^3-29023x^2-232184x-116092.
\end{aligned}
\]

These exact quartics and the raw `ellrank` records are recomputed by the
verifier. Their interpretation is subject to the conservative bounds above.

## Mordell--Weil point for `D=-1499`

On the minimal model, PARI finds the exact point

\[
P_{1499}=\left(
\frac{399030891253207}{156180668809},
\frac{7009131418974188521075}{61722131771310373}
\right).
\]

Direct substitution verifies the Weierstrass equation. Its canonical height
in PARI's normalization is

\[
 \widehat h(P_{1499})=33.9633809679668513740121781891\ldots.
\]

Together with the 2-Selmer upper bound one, this point certifies the
Mordell--Weil rank. The 2-descent alone does not exclude an odd index in the
free part, so this report calls it a non-torsion point rather than a certified
integral generator. The BSD leading-term quotient for this point is
numerically `1.0000...`, consistent with index one and trivial `Sha`, but that
numerical check is not used as a proof of saturation.

An exact point on the associated quartic is

\[
 (x,z)=\left(\frac{1367}{2987},\frac{592400303}{8922169}\right),
\]

which maps to the displayed Mordell--Weil point up to sign.

## Bounded point-search obstruction for `D=-29023`

PARI returns a nominal `[1,1]` rank interval but no rational point:

```text
ellrank(E29023,0) = [1,1,0,[]]
ellrank(E29023,6) = [1,1,0,[]]
```

The certified conclusion is only the 2-Selmer upper bound one and the
Mordell--Weil rank interval `[0,1]`. It is not known from these artifacts
whether the displayed nonzero cover class comes from a rational point or from
`Sha[2]`. PARI's `ellheegner` exhausts a 1 GB stack, and exact
`hyperellratpoints` finds no point on `C_29023` through naive height `10000`.

The numerical analytic data explain the failure without being used in the
rank proof:

\[
 L'(E^{(-29023)},1)=75.6578918899708368505\ldots,
\qquad
 \frac{L'}{\operatorname{ellbsd}(E)}
 =2659.7556120373832309983\ldots.
\]

Thus, under the rank-one BSD leading-term formula with `|Sha|=1`, a generator
has canonical height about `2659.76`, far beyond the successful `D=-1499`
search. No exact Mordell--Weil coordinate for `D=-29023` is claimed.

## Root numbers and analytic-rank output

At 48 displayed decimal digits, PARI/GP 2.15.4 returns the following. The
twist models in this block are PARI's direct `elltwist` models, not the minimal
models tabulated above.

```text
PARI_VERSION=[2, 15, 4]
DISPLAYED_DECIMAL_DIGITS=48
D=-1499
TWIST_MODEL=[-1, -375, 0, 0, -3368254499]
CONDUCTOR=972951433
ELLROOTNO=-1
LFUNROOTRES=[0, 0, -1]
ELLANALYTICRANK=[1, 4.25102592248315418934753906455942820689058223725]
ELLL1_D0=0
ELLL1_D1=4.25102592248315418934753906455942820689058223725
D=-29023
TWIST_MODEL=[-1, -7256, 0, 0, -24447075035167]
CONDUCTOR=364730851057
ELLROOTNO=-1
LFUNROOTRES=[0, 0, -1]
ELLANALYTICRANK=[1, 75.6578918899708368505115715917633505694509817915]
ELLL1_D0=0
ELLL1_D1=75.6578918899708368505115715917633505694509817915
```

The proof statuses differ:

- `ellrootno=-1` is an exact local-arithmetic root-number computation and is
  treated as rigorous. The exact twist formula
  `w(E^(D))=w(E)*(D/-433)` independently gives the same signs.
- `lfunrootres=[0,0,-1]` agrees, but `lfunrootres` belongs to PARI's numerical
  L-function framework and is only a numerical consistency check here.
- `ellanalyticrank` decides vanishing by a floating-point threshold (the PARI
  manual says values below `eps`, by default `2^(-bitprecision/2)`, are taken
  as zero). PARI's L-function manual explicitly warns that its generic
  numerical outputs are not intended as theorem-proving certificates.
  Therefore the displayed analytic ranks and derivatives are high-precision
  numerical evidence, stable in separate 48- and 80-digit runs, but are not
  claimed as rigorous analytic-rank certificates.
- Independently, certified descent gives algebraic rank at most one for both
  twists. The exact `D=-1499` point proves rank one there. For `D=-29023`, the
  raw `ellrank=[1,1,0,[]]` lower endpoint is not promoted to a certificate in
  this audit: the rigorous interval remains `[0,1]` pending a point or certified
  analytic nonvanishing.

## Reproduction

Run

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/verify_cycle192_pari_2descent.gp
```

The script checks the models, conductors, torsion, root numbers, raw 2-descent
records, exact 2-cover quartics, and the `D=-1499` point. Its explicit status
lines report the conservative certified rank intervals. The large
analytic calculation and failed randomized searches are deliberately omitted
from the fast certificate.

To reproduce the slower analytic output, run

```sh
gp -fq -s 3G millennium-prize/birch-swinnerton-dyer/cycle192_pari_analytic.gp
```
