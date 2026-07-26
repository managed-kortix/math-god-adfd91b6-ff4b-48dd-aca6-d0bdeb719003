# Notebook

Bounded scout is queued to audit the exact normalization and independently
certify the algebraic rank and the `T^2` coefficient for `389a1` at `p=5`.
No cyclotomic derivative is to be identified with a complex derivative.

## Bounded scout tick 2

For `389a1`, `a_5=-3`, so `p=5` is ordinary and has no exceptional zero.
LMFDB's `val=2` is the valuation of the 5-adic regulator, not the cyclotomic
order. Its Iwasawa data `[2,0]` means `lambda=2,mu=0`, but does not locate both
zeros at `T=0`. PARI differentiates in a weight variable with `T=6^s-1`; the
observed valuation two in the second derivative includes two factors of
`log_5(6)`. The next exact test is modular-symbol certification of zero
constant and linear cyclotomic moments, plus a replayable 2-Selmer rank upper
bound independent of analytic rank.

## Bounded scout cycle 36

The Iwasawa invariants alone cannot certify cyclotomic vanishing.  In
`Z_5[[T]]`, the series

`F(T)=T^2+5`

has `mu(F)=0` and `lambda(F)=2`: it is already a distinguished polynomial of
degree two.  Nevertheless `ord_(T=0) F=0`, since `F(0)=5`.  Thus the recorded
pair `[lambda,mu]=[2,0]`, even when exact, does not imply divisibility by `T`,
let alone by `T^2`.  The missing checkpoint remains exact vanishing of the
constant and linear modular-symbol moments; finite valuations cannot replace
those identities.

## Bounded scout cycle 39

No computation at fixed `5`-adic precision can certify the required exact
cyclotomic zeros.  For every `M>=1`, the series `T^2` and `T^2+5^M` have the
same reduction modulo `5^M`; both have `mu=0, lambda=2`, but their orders at
`T=0` are two and zero.  Therefore neither finite coefficient valuations nor
the Iwasawa invariants can replace exact modular-symbol identities for the
constant and linear moments.  This is a decisive obstruction to a
precision-only rank-two transfer calibration.

## Bounded scout cycle 41

The weight/cyclotomic normalization can be fixed without identifying the two
derivatives.  Write `F(T)=a_0+a_1T+a_2T^2+O(T^3)`, put
`T=exp(Ls)-1` with `L=log_5(6)`, and set `G(s)=F(T(s))`.  Then

`G(0)=a_0`, `G'(0)=La_1`, `G''(0)=L^2(a_1+2a_2)`.

Thus exact identities `a_0=a_1=0` imply
`a_2=G''(0)/(2L^2)`.  Without the linear zero, the second weight derivative
mixes `a_1` into the quadratic cyclotomic coefficient.  This settles only the
rank-two normalization; it creates no relation to a complex `L`-derivative.

## Bounded scout cycle 42

The conversion remains triangular at the next order. If
`F(T)=a_0+a_1T+a_2T^2+a_3T^3+O(T^4)`, `T=exp(Ls)-1`, and `G(s)=F(T(s))`, then

`G'''(0)=L^3(a_1+6a_2+6a_3)`.

After exact vanishing of `a_0,a_1`, one must still subtract the quadratic
moment:

`a_3=G'''(0)/(6L^3)-G''(0)/(2L^2)`.

Higher weight derivatives therefore cannot be read coefficientwise. This is
only normalization and gives no complex-derivative transfer.

## Bounded scout cycle 43

The triangular conversion has an exact all-order inverse. If
`F(T)=sum_(n>=0)a_nT^n`, `T=exp(Ls)-1`, and `G(s)=F(T(s))`, then

\[
{G^{(k)}(0)\over L^k}=\sum_{n=0}^k n!S(k,n)a_n,
\qquad
a_n={1\over n!}\sum_{k=0}^n s(n,k){G^{(k)}(0)\over L^k},
\]

where `S` and `s` are Stirling numbers of the second and signed first kinds.
This follows from the exponential generating function for `(exp x-1)^n` and
Stirling inversion. Consequently `T^r|F` is equivalent to exact vanishing of
the first `r` weight derivatives. This is only a formal certification
criterion; it supplies no modular-symbol vanishing or BSD result.

## Bounded scout cycle 46

At finite Mazur--Tate level `n`, reduction modulo `T^2` gives an augmentation
moment `A_n=sum c_n(a)` and a tangent moment
`B_n=sum c_n(a) ell_n(a) mod 5^n`, where
`<a>=gamma^(ell_n(a))`. Compatibility identifies these with `a_0` and
`a_1 mod 5^n` for the limiting Iwasawa series. Hence `T^2|F` is equivalent to
`A_n=0` and `B_n=0 mod 5^n` at every level. The even symmetry does not kill
the tangent moment: `<-a>=<a>` and paired plus-symbol terms double rather than
cancel. Exact linear vanishing therefore needs an all-level symbolic argument,
not symmetry or any finite precision. This proves no vanishing and no BSD case.
