# Cycle 190: strict no-exception fixed-`L_0` nonfactorization theorem

## Frozen objects and domain

Fix

\[
 E=433\mathrm a1:y^2+xy=x^3+1,\quad p=7,\quad
 P=(0,1),\quad Q=(-1,1),\quad \ell=29,
\]

and

\[
 L_0=\mathbf Q(E[7],7^{-1}P,7^{-1}Q).
\]

For a prime `q` not dividing `2*7*29*433`, put `D_q=q` when
`q=1 mod 4` and `D_q=-q` when `q=3 mod 4`. Let `A` be the set of such primes
satisfying exactly

\[
 \left(\frac q{29}\right)=1,\qquad
 w(E^{(D_q)})=-1,\qquad q\equiv1\pmod7,
\]

\[
 a_q(E)\equiv2\pmod7,\qquad
 v_7(\#E(\mathbf F_q))=1.                       \tag{190.1}
\]

The last three conditions make residual Frobenius nonidentity unipotent. This
is the frozen Cycle 187 search packet, without the computational cutoff
`q<200000`. No stronger Kolyvagin-prime, Tamagawa, nonanomalous, Selmer-switch,
or Kurihara-primitivity condition is included in the definition of `A`.

Choose `eta=2 mod 29`. For `q in A`, let `c(q,29) in F_7` be the normalized
one-prime Kurihara derivative of the plus Mazur--Tate element of `E^(D_q)`, with
the endpoint, period, and symbol conventions of Cycles 181, 187, and 188. Its
invariant form is

\[
 \mathfrak c(q,29)\in
 (M_q^+/7M_q^+)\mathbin\otimes_{\mathbf F_7}(I_{29}/I_{29}^2). \tag{190.2}
\]

Only the vanishing of (190.2) is used below.

## Frobenian definitions

Write `G_0=Gal(L_0/Q)` and let `G_0^#` be its set of conjugacy classes. A
scalar function `d:A -> F_7` is **strictly `L_0`-Frobenian on `A`** if there is a
function

\[
 F:G_0^\#\longrightarrow\mathbf F_7
\]

such that `d(q)=F(Frob_q(L_0))` for every `q in A`. Since `ell=29` is fixed,
including `Frob_29` as a second, constant argument gives the same definition.

The intrinsic vanishing predicate is **strictly `L_0`-Frobenian** if there is a function

\[
 Z:G_0^\#\longrightarrow\{0,1\}
\]

such that

\[
 Z(\operatorname{Frob}_q(L_0))=1
 \quad\Longleftrightarrow\quad \mathfrak c(q,29)=0             \tag{190.3}
\]

for every `q in A`, with no exceptional primes. This strict definition is not
the standard eventual convention that permits finitely many exceptions. A
line-valued strict Frobenian formulation must instead provide
isomorphisms from all lines in (190.2) to one fixed line and a class function
with values in that line.

## Theorem

**Theorem 190.1 (strict fixed-`L_0` nonfactorization).** On the packet `A`, the
vanishing predicate (190.3) is not strictly `L_0`-Frobenian. Consequently:

1. the pinned scalar `q -> c(q,29)` is not strictly `L_0`-Frobenian;
2. no choice of nonzero line trivializations can make the invariant
   coordinates `mathfrak c(q,29)` the pullback of a function on `G_0^#`;
3. no subextension of `L_0/Q`, or quotient of `G_0`, governs the vanishing of
   `mathfrak c(q,29)` on `A`.

More precisely, the two primes

\[
 q_0=29023,\qquad q_1=1499                              \tag{190.4}
\]

belong to `A` and satisfy

\[
 \operatorname{Frob}_{q_0}(L_0)
 =\operatorname{Frob}_{q_1}(L_0)\quad\text{in }G_0^\#,
 \qquad c(q_0,29)=0,\qquad c(q_1,29)=4.                 \tag{190.5}
\]

## Proof

Cycle 185 proves

\[
 G_0\simeq E[7]^2\rtimes\operatorname{GL}_2(\mathbf F_7).
\]

For a nonidentity-unipotent linear part, Cycle 184 proves that the full
semidirect-product conjugacy class is determined by the linear conjugacy class
and the zero or ordered projective localization row. Exact finite-field replay
gives (190.1) for both primes in (190.4), and gives the same nonzero ordered row
`[1:5]`. Their full `L_0` Frobenius conjugacy classes therefore agree.

The exact fixed-level-433 modular-symbol formula, together with the globally
minimal twist model and the proved period factor `kappa_q=1`, gives

\[
 c(29023,29)=\overline{77/2}=0,
 \qquad c(1499,29)=4
 \quad\text{in }\mathbf F_7.
\]

All completed denominators are 7-adic units. Thus one Frobenius fibre contains
both a zero and a nonzero coordinate, contradicting (190.3). A function through
a quotient of `G_0` would pull back to a function on `G_0^#`, proving the last
assertion.

## Trivialization invariance

Changing the primitive root modulo 29 rescales the augmentation line by an
element of `F_7^x`. Changing a primitive generator or orientation of a modular-
symbol line also rescales that line by an element of `F_7^x`. These changes may
alter the displayed nonzero residue `4`, and independent trivializations do not
make equality of two nonzero scalar residues intrinsic. They cannot turn zero
into nonzero or conversely. Hence the contradiction in (190.5) survives even
independent unit rescalings of the two source lines; it does not require a
comparison of their nonzero scalar values.

## Exact exclusions and limits

- The theorem concerns only the fixed field `L_0`, fixed auxiliary prime 29,
  fixed curve, fixed points, prime twists, and packet `A`.
- It does not assert that the two primes are conjugate in any proper extension
  of `L_0`, including a cyclotomic compositum. Such an extension may separate
  them.
- It does not prove that no finite Galois extension governs `c`. Universal
  nonfactorization would require collisions for a cofinal tower of finite
  extensions.
- It does not refute an eventual Frobenian statement allowing finitely many
  exceptional primes; a single finite collision cannot do so.
- It does not assert equidistribution, infinitude, positive density, or even a
  second collision. Chebotarev cannot be applied to `c` through `L_0` after
  this obstruction.
- It does not establish any omitted local, Selmer, Kolyvagin-system, or
  primitivity hypotheses and does not identify `c` with a Selmer determinant
  through explicit reciprocity.
- It does not determine the algebraic rank, analytic rank, Tate--Shafarevich
  group, regulator, or leading coefficient of either twist.

In particular, Theorem 190.1 proves neither BSD for either displayed curve nor
any case, average, or density statement toward BSD. It falsifies strict,
no-exception factorization through one named finite field for one auxiliary
modular-symbol coordinate.
BSD for all elliptic curves over `Q` would still require the rank equality
`ord_(s=1)L(E,s)=rank E(Q)` for every curve (and the refined conjecture requires
still more); no implication from this non-governance statement supplies that
bridge.
