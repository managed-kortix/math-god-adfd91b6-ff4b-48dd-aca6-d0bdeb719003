# Cycle 187: full Kummer Chebotarev densities and collision filters

## Group and class formula

For the certified field

\[
 L_0=\mathbf Q(E[7],7^{-1}P,7^{-1}Q),\qquad
 G=\operatorname{Gal}(L_0/\mathbf Q)
   =M\rtimes H,
\]

where `M=(F_7^2)^2`, `H=GL_2(F_7)`, one has

\[
 |H|=(7^2-1)(7^2-7)=2016,
 \qquad |G|=7^4|H|=4,840,416.
\]

Fix a residual representative `A in H`, put

\[
 d=\dim\operatorname{coker}(I-A),
 \qquad C=C_H(A),
\]

and let `O` be a `C`-orbit in
`(coker(I-A))^2`.  Cycle 184's conjugacy theorem and direct counting give
the density of the corresponding full `G`-conjugacy class:

\[
 \boxed{\delta(A,O)=\frac{|O|}{|C|7^{2d}}.} \tag{187.1}
\]

Indeed, the class contains
`(|H|/|C|)|O|7^(2(2-d))` elements: choose the residual conjugate, an
orbit point in the affine quotient, and one of the lifts through
`(I-A)M`. Dividing by `|M||H|=7^4|H|` proves (187.1).

## Complete table

In the table, the density is for each one of the full conjugacy classes in
that row, not for their union.  A projective row means one specified element
of `P^1(F_7)`, of which there are eight.

| residual type | residual classes | affine label per residual class | full classes | `|C_H(A)|` | density of each full class |
|---|---:|---|---:|---:|---:|
| `A=I` | 1 | zero | 1 | 2016 | `1/4,840,416` |
| `A=I` | 1 | fixed rank-one projective row | 8 | 2016 | `1/100,842` |
| `A=I` | 1 | rank two | 1 | 2016 | `1/2,401` |
| nonidentity unipotent at eigenvalue 1 | 1 | zero | 1 | 42 | `1/2,058` |
| nonidentity unipotent at eigenvalue 1 | 1 | fixed nonzero projective row | 8 | 42 | `1/343` |
| split semisimple `{1,lambda}`, `lambda!=1` | 5 | zero | 5 | 36 | `1/1,764` |
| split semisimple `{1,lambda}`, `lambda!=1` | 5 | fixed nonzero projective row | 40 | 36 | `1/294` |
| scalar `lambda I`, `lambda!=1` | 5 | unique | 5 | 2016 | `1/2,016` |
| nontrivial Jordan at `lambda!=1` | 5 | unique | 5 | 42 | `1/42` |
| split distinct eigenvalues, neither 1 | 10 | unique | 10 | 36 | `1/36` |
| irreducible quadratic | 21 | unique | 21 | 48 | `1/48` |

There are 48 residual `GL_2(F_7)` classes and 105 full Kummer classes. The
table's densities, multiplied by the indicated number of full classes, sum
exactly to one.

For `d=1`, the centralizer induces all six nonzero scalars on the quotient.
Thus the zero orbit has size one and each of the eight projective orbits has
size six. For `A=I`, simultaneous left `GL_2` action on the ordered pair has
the zero orbit, eight rank-one orbits of size 48 indexed by the ordered
projective coefficient row, and one rank-two orbit of size 2016. If 1 is not
an eigenvalue, `d=0` and there is no affine decoration.

## Densest compatible classes

Globally, a densest single full `L_0` class is any split semisimple residual
class with two distinct eigenvalues in `F_7^x-{1}`. Its density among all good
primes is

\[
 \boxed{\delta_{\max}=1/36.} \tag{187.2}
\]

Cycle 186 proved
`L_0 intersect Q(zeta_29)=Q`. Hence the quadratic condition
`(q/29)=1` is independent of every `L_0` class. In
`L_0 Q(sqrt(29))`, each compatible decorated class therefore has half its
old absolute density. The global maximum becomes

\[
 \boxed{1/72.} \tag{187.3}
\]

This global maximum is not in the Kolyvagin-prime packet used by the existing
local-row screen. If that packet retains

\[
 q=1\pmod 7,\qquad a_q=2\pmod 7,
 \qquad v_7(\#E(\mathbf F_q))=1,
\]

then the residual matrix is nonidentity unipotent. In that packet, every fixed
nonzero projective row is densest, with absolute density `1/343` in `L_0` and

\[
 \boxed{1/686} \tag{187.4}
\]

after imposing `(q/29)=1`. The zero-row class has density `1/4,116` after the
same quadratic filter, six times smaller. Conditional on being in the
nonidentity-unipotent residual class, the row probabilities are `1/49` for
zero and `6/49` for each projective direction.

## Collision-search filters

The highest-yield correct search does not use one progression modulo
`8*7*433*29`. It proceeds as follows.

1. Require `(q/29)=1`, represented by `Q(sqrt(29))`, but retain all 14
   nonzero quadratic-residue classes modulo 29. Fixing one residue class loses
   a factor 14 in candidate density and a factor 196 in same-class pair yield.
2. If the local Selmer/Kolyvagin switch is required, retain all eight nonzero
   projective rows and bucket candidates by their exact row. For expensive
   modular-symbol production, prioritize whichever row bucket fills first;
   all eight have equal Chebotarev density. Do not retain only a preselected
   row unless storage or comparison-map normalization requires it.
3. Do not fix `q mod 4`. The rule `D_q=q` for `q=1 mod 4` and `D_q=-q` for
   `q=3 mod 4` defines the fundamental discriminant; it is not itself an
   admissibility condition. Keeping both signs doubles candidate supply and
   quadruples pair opportunity relative to one sign, unless a theorem requires
   one twist sign.
4. Do not impose a character at 433, a root-number sign, or a 2-adic character
   merely for convenience. Add each only if it occurs in the frozen
   admissibility predicate. Each independent quadratic equality halves the
   prime supply and quarters the raw pair rate. If required, use its quadratic
   character field rather than a full residue class modulo its conductor.
5. Bucket every screened prime by the complete full-class key: residual type
   and affine label (zero/projective row, or rank for `A=I`). Compare `c(q,29)`
   only within a bucket. Across all buckets, this dominates committing in
   advance to one class; the densest bucket is only the first priority when
   exact-symbol production is the bottleneck.

For two independently sampled unfiltered good primes, the exact probability
that their `L_0` Frobenius classes agree is the class collision index

\[
 \sum_C\delta_C^2
 =\frac{78,876,293,599}{3,904,937,842,176}
 \mathrel{\sim}0.0201991.
\]

The `(q/29)=1` filter does not change this conditional probability. Inside the
nonidentity-unipotent residual packet, retaining zero and all eight projective
rows gives exact row-collision probability `289/2401`; after discarding the
zero row, the eight projective buckets are uniform and the probability is
`1/8`. Thus preserving all admissible projective buckets gives eight times the
asymptotic pair yield of fixing one row.

If `N` denotes the number of primes scanned before filters, a fixed nonzero
unipotent row with `(q/29)=1` supplies asymptotically `N/686` candidates and
about `N^2/(2*686^2)` unordered same-class pairs. An additional independent
fixed twist character changes `686` to `1372`. These are Chebotarev supply
rates only: they make no assertion that the varying-conductor coordinate
`c(q,29)` is random or that a zero/nonzero collision exists.

Reproduce the exact finite-group enumeration and all table checks with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle187_chebotarev_densities.py
```

No collision, finite-governance theorem, or BSD case is claimed.
