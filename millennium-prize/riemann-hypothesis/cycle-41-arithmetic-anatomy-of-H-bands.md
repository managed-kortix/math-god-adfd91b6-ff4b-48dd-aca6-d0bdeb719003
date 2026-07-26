# Cycle 41: arithmetic anatomy of the certified negative H bands

## Scope

This note explains the finite certified bands

\[
 39\!:\!40,\qquad 95\!:\!100,\qquad 219\!:\!226
\]

in the Cycle 40 quantity

\[
 H_n=\|D_n\|^2-C_n\|U_n\|^2,\qquad
 C_n=L_nL_{n+1},\quad L_n=\log n,
\]

where

\[
 U_n=\chi+\sum_{a\le n}\mu(a)\rho_a,
 \qquad D_n=\sum_{a\le n}\mu(a)L_a\rho_a.
\]

All stated signs and intervals are certified with outward-rounded Arb balls.
The decomposition below is exact, but the observations are finite diagnostics:
they are not an eventual sign theorem and make no RH claim.

## Exact one-step recurrence

Put `q=n+1`, `m=mu(q)`, and

\[
 X_{n,q}=\langle U_n,\rho_q\rangle,
 \qquad Y_{n,q}=\langle D_n,\rho_q\rangle,
 \qquad G_{q,q}=\|\rho_q\|^2.
\]

Since

\[
 U_q=U_n+m\rho_q,\qquad D_q=D_n+mL_q\rho_q,
\]

direct expansion gives

\[
\boxed{
 H_{n+1}-H_n=
 -(C_{n+1}-C_n)\|U_n\|^2
 +2\mu(n+1)\big(L_{n+1}Y_{n,n+1}-C_{n+1}X_{n,n+1}\big)
 +\mu(n+1)^2\big(L_{n+1}^2-C_{n+1}\big)G_{n+1,n+1}.}
\tag{41.1}
\]

Every term is a finite complete-Gram expression. In particular,

\[
 C_{n+1}-C_n=L_{n+1}(L_{n+2}-L_n)>0,
\]

\[
 L_{n+1}^2-C_{n+1}
 =-L_{n+1}\log\left(1+{1\over n+1}\right)<0,
\]

and

\[
 G_{q,q}={\log(2\pi)-\gamma\over q}-{1\over q^2}>0.
\]

Thus the scale drift, the first term of (41.1), is always strictly negative,
and the squarefree diagonal cost, the third term, is also strictly negative.
Only the signed linear correlation can compensate them.

Using the complete restricted Vasyunin matrix,

\[
 X_{n,q}=g_q+\sum_{a\le n}\mu(a)G_{a,q},\qquad
 Y_{n,q}=\sum_{a\le n}\mu(a)L_aG_{a,q},
\tag{41.2}
\]

where `g_q=(L_q+1-gamma)/q`. Equations (41.1)-(41.2), together with the
finite cotangent formula for `G_(a,q)`, are the exact arithmetic certificate.

## Event law

Equation (41.1) separates two event types.

1. If `q=n+1` is nonsquarefree, then `mu(q)=0` and

\[
 \boxed{H_{n+1}-H_n=-(C_{n+1}-C_n)\|U_n\|^2<0.}
\tag{41.3}
\]

There is no new Mobius coordinate. A run of nonsquarefree integers is therefore
a deterministic downward slide caused solely by the increasing scale `C_n`.

2. If `q` is squarefree, a new coordinate enters. On all relevant transitions
the Arb certificate gives

\[
 B_{n,q}:=L_qY_{n,q}-C_{n+1}X_{n,q}<0.
\]

Consequently `mu(q)=+1` reinforces both negative costs, whereas `mu(q)=-1`
reverses the linear term and gives the compensating jump. This sign of `B` is
certified for the displayed finite windows; it is not asserted for every `n`.
Primes are especially visible compensators because every prime has `mu=-1`,
but squarefree composites with an odd number of prime factors compensate by
the same mechanism.

## Structural endpoints

The local sign bands are generated and terminated by the following events.

| transition | factorization/event | certified effect |
|---|---|---|
| `H_38 -> H_39` | `39=3*13`, `mu=+1` | crosses into the `39-40` band |
| `H_39 -> H_40` | `40`, nonsquarefree | pure negative drift |
| `H_40 -> H_41` | `41` prime, `mu=-1` | exits the band |
| `H_94 -> H_95` | `95=5*19`, `mu=+1` | crosses into `95-96` |
| `H_95 -> H_96` | `96`, nonsquarefree | pure negative drift |
| `H_96 -> H_97` | `97` prime, `mu=-1` | first local exit |
| `H_97 -> H_100` | `98,99,100`, all nonsquarefree | three pure drifts; recrossing occurs at `H_99` |
| `H_100 -> H_101` | `101` prime, `mu=-1` | final local exit |
| `H_218 -> H_219` | `219=3*73`, `mu=+1` | crosses into `219-222` |
| `H_219 -> H_220` | `220`, nonsquarefree | pure negative drift |
| `H_220 -> H_221` | `221=13*17`, `mu=+1` | deepens the band |
| `H_221 -> H_222` | `222=2*3*37`, `mu=-1` | partial compensation |
| `H_222 -> H_223` | `223` prime, `mu=-1` | first local exit |
| `H_223 -> H_225` | `224,225`, nonsquarefree | downward slide remains positive |
| `H_225 -> H_226` | `226=2*113`, `mu=+1` | isolated recrossing |
| `H_226 -> H_227` | `227` prime, `mu=-1` | final local exit |

This gives a precise meaning to the broad labels `95-100` and `219-226`:
they are arithmetic episodes, not contiguous sets of negative indices. Their
actual negative runs are

\[
 39\!:\!40,\quad 95\!:\!96,\quad 99\!:\!100,
 \quad 219\!:\!222,\quad \{226\}.
\]

The starts `39,95,219` share the same trigger: a squarefree semiprime with
`mu=+1`. The final local exits `41,101,227` are the immediately following
`mu=-1` prime events. The internal holes and recrossings are explained exactly
by nonsquarefree drift and the parity of the next squarefree event.

## Certified magnitudes

Representative 256-bit enclosures for (41.1) are:

| transition | `H_n` | drift | linear | diagonal | `H_(n+1)` |
|---|---:|---:|---:|---:|---:|
| `38 -> 39` | `1.250287779136674` | `-0.01198955094244936` | `-1.332000180892171` | `-0.002937237885759719` | `-0.09663919058370593` |
| `40 -> 41` | `-0.1249718160672120` | `-0.02782633353119986` | `1.352665882926049` | `-0.002698327474472044` | `1.197169405853165` |
| `94 -> 95` | `0.06469577911752177` | `-0.01392857629418035` | `-0.8302142751449610` | `-0.0006275021544975429` | `-0.7800745744761171` |
| `96 -> 97` | `-0.8023129635279448` | `-0.02205907993825949` | `0.8428277872162607` | `-0.0006048162546170152` | `0.01785092749543936` |
| `98 -> 99` | `0.004158369775044091` | `-0.01358425239193431` | `0` | `0` | `-0.009425882616890221` |
| `100 -> 101` | `-0.02290369740159763` | `-0.01337319529737084` | `0.8454366380647906` | `-0.0005630841076108138` | `0.8085966612582114` |
| `218 -> 219` | `0.1982949962804471` | `-0.008203824361121903` | `-0.4864479964013498` | `-0.0001408181482280848` | `-0.2964976426302527` |
| `220 -> 221` | `-0.3076311359692057` | `-0.01109243393163032` | `-0.4907100702382696` | `-0.0001385216142246122` | `-0.8095721617533302` |
| `222 -> 223` | `-0.3307552174820198` | `-0.01102508657266747` | `0.4950861279944198` | `-0.0001362822738138647` | `0.1531695416659187` |
| `225 -> 226` | `0.1369651658433067` | `-0.008058282606240828` | `-0.4980407750952153` | `-0.0001330263463251528` | `-0.3692669182044746` |
| `226 -> 227` | `-0.3692669182044746` | `-0.01083836970847536` | `0.5007198889825628` | `-0.0001319676159571422` | `0.1204826334536557` |

The omitted radii are below `5e-16` in every displayed field; the reproduction
script prints the full Arb balls rather than these shortened decimal centers.

## Weighted compensation

Local return to `H_n>0` does not yet repay the exact half-strength block debt.
The relevant surplus is

\[
 S(a,b)=\sum_{n=a}^{b-1}\eta_nH_n,
 \qquad
 \eta_n={L_{n+1}-L_n\over L_nL_{n+1}^2}>0.
\tag{41.4}
\]

The first certified recovery endpoints and deepest excursions are

| start `a` | deepest endpoint | certified minimum of `S(a,b)` | first `b` with `S(a,b)>=0` |
|---:|---:|---:|---:|
| `39` | `41` | `[-0.00010973780740451422732 +/- 3.05e-25]` | `42` |
| `95` | `101` | `[-0.00017409370067049317581 +/- 4.12e-24]` | `103` |
| `219` | `223` | `[-5.0099899358267480505e-5 +/- 5.95e-26]` | `231` |
| `226` | `227` | `[-1.0219726320174780561e-5 +/- 4.83e-25]` | `230` |

For example, `223` restores the local sign after the first `219` run, but the
weighted debt remains. The later `mu=+1` event at `226` adds a second deficit.
The `mu=-1` events at `227,229,230,231` (two primes and two odd-parity
squarefree composites) supply the eventual compensation at endpoint `231`.
This is the mechanism behind the longest first-recovery block `[219,231)`.

## Reproduction and checks

Run the event table and weighted recovery scan with

```text
uv run --with python-flint python cycle41_h_event_analysis.py \
  --max-n 240 --bits 192
```

Run the focused certificate tests with

```text
uv run --with python-flint python -m unittest -v \
  test_cycle41_h_event_analysis.py \
  test_cycle40_complete_diagnostics.py test_complete_gram.py
```

The tests certify the recurrence against independently updated norms, pure
negative drift at every nonsquarefree event through `232`, the complete list of
12 negative indices, the stated trigger/compensation event signs, and the four
weighted first-recovery endpoints.
