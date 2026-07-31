# Notebook

## Collision certificate gate cycle 182

Cycle 181 does not contain enough raw information to reconstruct an exact
`q` collision: no named field, fixed `ell`, pair of twist primes, modular-symbol
rows, or Frobenius witnesses is present, and no Cycle 182 producer/data is
committed.  Cycle 182 therefore specifies a fail-closed certificate with three
independent layers: pinned exact modular-symbol replay, dependency-free mod-7
reduction, and class-separating Galois/Frobenius verification in
`L Q(zeta_(8*7*433*ell))`.  Polynomial factorization type alone is not an
adequate nonabelian Frobenius witness.  No collision is claimed.  See
`cycle-182-q-collision-certificate-specification.md`.

## Conductor/Frobenius audit cycle 181

For the fundamental-discriminant convention `D_q=q` if `q=1 mod 4` and
`D_q=-q` if `q=3 mod 4`, define `c(q,ell)` by applying the first augmentation
derivative to the Mazur--Tate element of `E^(D_q)`, equivalently by
`sum_a [a/ell]^+_(E^(D_q)) log_eta(a) mod 7`. The twist has conductor
`433 q^2`; the twist formula rewrites its values using base modular symbols
with denominator `q ell`. Thus a fixed residual Selmer governing field does not
automatically govern `c`, although conductor growth alone does not prove that
no finite extension can do so. For a named field `L`, exact factorization is
equivalent to constancy on Frobenius fibers, and a fixed-`ell` zero/nonzero
collision refutes `L`. Universal nonfactorization requires collisions along a
cofinal tower. See `cycle-181-conductor-and-frobenius-obstruction.md`.

## Conditional theorem cycle 181

Frobenianity of the decorated coordinate is not equidistribution.  If one
finite governing extension controls `(lambda,c)` and every fiber over
`S^* x F_7` has the same size, Chebotarev gives probability
`(1-7^(-r))/7` for each downward increment and `7^(-r-1)` for each upward
increment.  At `r=2`, the event `lambda!=0,c!=0` therefore has relative
density `(48/49)(6/7)=288/343`.  For two ordered primes, imposing squarefree
product only deletes the diagonal and preserves that relative density.  This
does not handle squarefree twists of unbounded length or project a decorated
pair count to prime twists.  Finite governance of `c`, balanced fibers, local
twist comparison, uniform primitivity, explicit reciprocity, and auxiliary-
prime removal remain unproved.  See
`cycle-181-frobenian-decorated-transition.md`.

## Bounded scout cycle 178

The concrete candidate is the prime quadratic-twist family of `433a1` at
`p=7`, restricted to one Frobenius packet with root number `-1` and one local
Selmer switch.  Decorating the one-step Selmer transition by a residual
Kurihara coordinate gives the exact candidate
`(S,z)->(ker(lambda),z+c)` for `lambda!=0` and
`(S,z)->(S+F_7,z+c)` for `lambda=0`.  Under uniform `(lambda,c)`, the
probabilities are `(1-7^(-r))/7` for each downward symbol increment and
`7^(-r-1)` for each upward symbol increment.
The one-step state space is finite.  The missing production lemma is that `c`
is controlled and equidistributed by a finite governing extension jointly
with `lambda`; ordinary Selmer governing fields do not imply this.  Bare
positive-density rank one is likely known, so only explicit certificate
density could be novel.  See `cycle-178-derived-symbol-prime-twist-scout.md`.
No rank-one density or BSD result is claimed.

## Bounded scout cycles 89--90

Prescribed modular visibility has an exact quotient-point/Kummer criterion.
Tamiozzo already proves broad auxiliary-level visibility of all `Sha[p]`
classes under substantial hypotheses, using a Selmer-dimensional set of
admissible primes. A dimension-free two-prime refinement is obstructed by
one-dimensional local switches and passive Selmer summands invisible to shallow
bipartite-system classes. The classical conductor-1246, `p=5` example is already
published by Cremona--Mazur. No BSD result or novelty is claimed.

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

## Bounded scout cycle 50

Normalized ordinary Mazur--Tate norm compatibility gives the tangent recurrence
`B~_(n+1)=B~_n mod 5^n`; before unit-root normalization it is
`B_(n+1)=alpha B_n mod 5^n`. The unstabilized distribution gives
`B_(n+1)=a_5B_n-5B_(n-1) mod 5^n`. These propagate information downward only.
The compatible series `5^N T` vanishes in every tangent quotient through level
`N` but not level `N+1`, so finite generation and Nakayama cannot turn bounded
level computations into exact tangent vanishing. This proves no BSD case.

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

## Bounded scout cycle 59

For sign `+1`, the Mazur--Tate functional equation modulo the augmentation
square gives `2B_n=-c_nA_n mod 5^n`. Thus exact all-level augmentation
vanishing forces tangent vanishing for `389a1`; bare Manin relations do not
prove the needed constant moment. No BSD case is proved.

## Bounded scout cycle 63

Ordinary interpolation gives `F_E(0)=(1-alpha^-1)^2 L(E,1)/Omega_E^+` up to a
fixed nonzero normalization. For `389a1` at `p=5`, `alpha!=1`, so exact
all-level augmentation vanishing is equivalent to `L(E,1)=0`. Root number `+1`
alone does not force this. A certified non-torsion rational point would imply
the vanishing noncircularly by the contrapositive of the rank-zero Gross--
Zagier--Kolyvagin theorem; interpolation and Cycle 59 would then kill both
constant and tangent moments. This is no BSD proof.

## Main-funnel cycle 173

For `433a1,p=7`, the exact cyclotomic order is two. The Cycle 136 localization
determinant proves that `P=(0,1)` and `Q=(-1,1)` are independent, hence positive
rank. The contrapositive used is only the established rank-zero implication
`L(E,1) != 0 => E(Q) finite`; it gives `L(E,1)=0` without asserting analytic
rank at least two. Interpolation gives `F(0)=0`. The exact functional equation
must be retained as `F(T)=w(E)u(T)F((1+T)^-1-1)`, with the conductor unit
`u(T)=(1+T)^(-ell(433))`. For `w(E)=+1`, coefficient comparison gives
`(1+u(0))F'(0)=u'(0)F(0)`; thus `u(0)=1` suffices only after the
constant zero is known, while the sign is essential. Finally Cycle 171's
`M2=F''(0)+F'(0)` and exact `M2=5 mod 7` imply `F''(0) != 0`. Hence
`ord_(T=0) F=2`. This is a p-adic order theorem, not rank-two p-adic BSD or a
complex analytic-rank-two proof.
