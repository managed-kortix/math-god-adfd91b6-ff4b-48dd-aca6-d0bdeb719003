# Exact single-bridge Coulson/spectral-shift phase theorem and two sharp route obstructions

Date: 2026-11-21. Status: **PROVED IDENTITY / EXACT ROUTE OBSTRUCTIONS / NONPROMOTIONAL**.

## 1. Scope

Let `U,R` be finite simple graphs, marked at `y,x`, and let `G` be obtained by adding the single edge `xy`. Write

```text
chi_H(z)=det(zI-A(H)),
m_U(z)=chi_(U-y)(z)/chi_U(z),
m_R(z)=chi_(R-x)(z)/chi_R(z),
Psi_H(t)=i^(-|V(H)|) chi_H(it),
Theta_H(t)=sum_j arctan(lambda_j(H)/t),   t>0,
```

where each arctangent lies in `(-pi/2,pi/2)`. The conclusions below fix the determinant sign, continuous branch, zero-mode behavior, and integrability. They do **not** prove or refute the missing hostile rank-`(1,6)` inequality. They show that two tempting pointwise phase routes are false even when `U=C5` and the positive rank-six component of `R` is bridge-free, as allowed in the literal `k=1` inherited state (the marked port may lie in an attached tree).

## 2. Exact coupled phase formula

The rooted bridge determinant identity is

```text
chi_G(z)=chi_U(z)chi_R(z)-chi_(U-y)(z)chi_(R-x)(z)
        =chi_U(z)chi_R(z) F(z),
F(z)=1-m_U(z)m_R(z).                                      (1)
```

The minus sign follows either by expansion in the bridge entries or by the matrix determinant lemma applied to the rank-two symmetric cross block. For `t>0`, none of `chi_U(it),chi_R(it),chi_G(it)` vanishes: all adjacency eigenvalues are real and `it` is nonreal. Hence `F(it)` is finite and nonzero. (The displayed factorization uses the generic resolvent convention `m(z)=(zI-A)^{-1}`. If one instead defines a rooted resolvent at `itI-A` with an extra sign, that sign must not be silently imported here.)

Define

```text
Delta(t)=Theta_G(t)-Theta_U(t)-Theta_R(t).                  (2)
```

From `Psi_H(t)=product_j(t+i lambda_j(H))`, each `Theta_H` is the continuous argument of `Psi_H` tending to zero at infinity. Equation (1) therefore gives

```text
exp(i Delta(t))=F(it)/|F(it)|,                              (3)
```

and **Delta is the unique continuous lift of the argument of `F(it)` whose
limit is zero as `t -> infinity`**.  Here uniqueness means among continuous
real-valued lifts with that normalization; two lifts differ by a constant in
`2 pi Z`.

For this particular single-edge coupling one can say more: the lift is always
principal at every positive `t`.  Put

```text
D=A(U) direct_sum A(R),       M=A(G),
p=(e_y+e_x)/sqrt(2),          q=(e_y-e_x)/sqrt(2),
M=D+p p^T-q q^T.
```

For a real symmetric matrix `H`, let `N_H(s)` count its eigenvalues `<=s`,
with multiplicity, and define the spectral shift

```text
xi(s)=N_D(s)-N_M(s).
```

If `B=D+p p^T`, rank-one interlacing gives, away from eigenvalues,

```text
N_D(s)-N_B(s) in {0,1},       N_B(s)-N_M(s) in {-1,0},
|xi(s)|<=1.                                                   (3a)
```

(The second comparison uses `M=B-q q^T`: a negative rank-one update can only
increase a sublevel counting function by at most one.)

The choice of values at the finitely many eigenvalues is immaterial below.
For `f_t(s)=arctan(s/t)`, the finite-dimensional counting-function
identity

```text
tr f_t(M)-tr f_t(D)=integral f_t'(s)[N_D(s)-N_M(s)] ds
```

(the boundary term vanishes because the two matrices have the same order)
gives the exact Poisson representation

```text
Delta(t)=integral_(-infinity)^infinity
              [t/(t^2+s^2)] xi(s) ds.                        (3b)
```

The function `xi` vanishes outside a bounded spectral interval.  If all spectra
lie in `[-L,L]`, then the Poisson kernel is positive and

```text
|Delta(t)| <= integral_(-L)^L t/(t^2+s^2) ds
             =2 arctan(L/t)<pi.                              (3c)
```

Thus the strictness is not an equality-case assumption about `xi`; it follows
from compact spectral support.  The constant `pi` is sharp over unbounded
families of finite matrices.

Consequently

```text
Delta(t)=Arg F(it) in (-pi,pi) for every t>0,
```

and `F(it)` never meets the negative real axis at positive `t`.  Thus a
single bridge cannot create a hidden full winding on `(0,infinity)`.  The
branch hazard is at the one-sided endpoint `t=0`, where the limit may equal
`-pi` while the conventional principal value at a negative real number is
`+pi`.

There is also an exact area form.  The equal traces give

```text
integral xi(s) ds=tr(M)-tr(D)=0.
```

For a fixed `t`, multiply (3b) by `t` and subtract the zero term
`integral xi`; this gives

```text
t Delta(t)=-integral [s^2/(t^2+s^2)] xi(s) ds.
```

This rewritten integrand is absolutely integrable on the product domain:
`xi` has compact support and

```text
integral_0^infinity s^2/(t^2+s^2) dt=pi|s|/2.
```

Consequently absolute Fubini gives

```text
integral_0^infinity t Delta(t) dt
  =-(pi/2) integral_(-infinity)^infinity |s| xi(s) ds,
Gamma=1+integral_(-infinity)^infinity |s| xi(s) ds.           (3d)
```
Formula (3d) is also exactly the finite-dimensional Krein trace identity for
the test function `s_+^2`: here `(s_+^2)'=2s_+=s+|s|`, while

```text
integral s xi(s) ds=[tr(M^2)-tr(D^2)]/2=1.
```

Thus `Gamma=integral 2s_+ xi=1+integral |s|xi`, with the unit term coming
from the bridge's trace-square increment; it must not be dropped.  Since
`|xi|<=1` alone gives no lower bound on the signed weighted moment
`integral |s|xi`, (3d) does not by itself pay the hostile debit; this is the
precise spectral-shift obstruction rather than merely a phase-sign issue.

The signed Coulson identity and the trace-square increment

```text
(s+(G)+s-(G))-(s+(U)+s-(U)+s+(R)+s-(R))=2
```

then give the exact bridge-gain formula

```text
Gamma=s+(G)-s+(U)-s+(R)
     =1-(2/pi) integral_0^infinity t Delta(t) dt.           (4)
```

### Endpoint and integrability audit

As `t -> infinity`, the Neumann series gives, for a simple loopless graph,

```text
m_H(it)=1/(it)+deg_H(mark)/(it)^3+(A_H^3)_(mark,mark)/(it)^4
          +O(t^(-5)),
F(it)=1+t^(-2)-(deg_U(y)+deg_R(x))t^(-4)
          +i[(A_U^3)_(y,y)+(A_R^3)_(x,x)]t^(-5)+O(t^(-6)),
Delta(t)=O(t^(-5)).                                        (5)
```

For adjacency matrices `(A_H^3)_(v,v)=2` times the number of triangles through
`v`.  Indeed the corresponding terms in `m_Um_R` are
`+(deg_U+deg_R)t^(-4)-i(A_U^3+A_R^3)t^(-5)`; subtracting that product fixes
both displayed signs.  The weaker `O(t^(-3))` already suffices for (4).

At zero, `|Delta(t)|` is bounded because it is a fixed finite difference of
bounded arctangent sums (for the fixed finite graphs under discussion). More
precisely,

```text
lim_(t downarrow 0) Delta(t)
 = (pi/2)[sig(A_G)-sig(A_U)-sig(A_R)],                      (6)
```

where `sig(A)=n_+(A)-n_-(A)` and zero eigenvalues contribute zero. Thus `t Delta(t)=O(t)` at zero, including singular side matrices. No inverse at `t=0` is used.

The rooted resolvents themselves have the exact asymptotic expansion

```text
m_H(it)=alpha_H/(it)-<e,A_H^dagger e>+O(t),
alpha_H=||Pi_ker(A_H)e||^2.                                 (7)
```

Hence poles caused by marked zero modes are real features of the factorization, but (2), (6) remain the safe branch convention. Formula (7) also shows why substituting ordinary inverses at zero is invalid.

## 3. Obstruction I: the bridge correction has no fixed phase sign

Take `U=C5`, marked at any vertex, and let `R_1` have vertices `0,...,6`, mark `x=3`, and edges

```text
25,16,05,15,12,03,26,04,34,14,36,01.                       (8)
```

It is connected, has `12-7+1=6`, and deletion of each edge leaves it connected, so it is itself a bridge-free rank-six center. Its rooted polynomials are

```text
chi_R1(z)=z^7-12z^5-10z^4+23z^3+20z^2-9z-6,
chi_(R1-x)(z)=z^6-9z^4-8z^3+9z^2+8z-1.                     (9)
```

Also

```text
chi_C5(z)=z^5-5z^3+5z-2,
chi_(C5-y)(z)=z^4-3z^2+1.                                  (10)
```

Let `F_1(it)` be (1). Multiplying its numerator by the conjugate of its denominator does not change the signs of its real and imaginary parts. Exact expansion gives a strictly positive even real polynomial and

```text
sign Im F_1(it)=sign[t J(t^2)],
J(s)=2s^9+20s^8+38s^7-286s^6-1740s^5-4070s^4
     -4844s^3-2960s^2-836s-84.                             (11)
```

The coefficient signs of `J` have exactly one variation, so Descartes' rule gives at most one positive root; `J(4)=-1898340<0<J(9)=1532308920`, so there is exactly one. (The verifier also checks this with a rational Sturm sequence.) Explicit exact evaluations show the corresponding phase sign change:

```text
F_1(i)   =269/225 -(8/225)i,
F_1(3i)  =17282138743/16090515363
          +(4685960/5363505121)i.                          (12)
```

Because the real part is positive for every `t>0`, `Delta_1(t)` is the principal argument here and changes sign once. Thus neither

```text
Delta(t)<=0 for all t>0
```

nor the reverse pointwise sign can be a universal theorem for the allowed bridge-free rank-six center. A successful Coulson proof must use a genuinely integrated inequality or additional reserve; with the convention in (1), each rooted resolvent is anti-Herglotz (`Im m(z)<0` for `Im z>0`), but this one-sided half-plane property does not impose a sign on the product in (1).

## 4. Obstruction II: the principal endpoint reset can choose the wrong side

Take `U=C5` again. Let `R_2` have vertices `0,...,6`, mark `x=4`, and edges

```text
12,13,36,03,04,16,56,02,35,23,15,01.                       (13)
```

Here `R_2` is connected and rank six. Its edge `04` is a pendant bridge, while the induced subgraph on `{0,1,2,3,5,6}` is bridge-free and still has rank six. Thus it is an allowed `k=1` complement consisting of a bridge-free rank-six center with a zero-rank tree attached, and the marked port `x=4` lies in that tree. Its rooted polynomials are

```text
chi_R2(z)=z^7-12z^5-16z^4+11z^3+26z^2+8z-2,
chi_(R2-x)(z)=z^6-11z^4-16z^3+3z^2+16z+7.                  (14)
```

For `F_2` from (1), the same conjugate-denominator expansion has imaginary part

```text
-2t(4t^16+66t^14+437t^12+1519t^10+3037t^8
       +3584t^6+2439t^4+871t^2+123),                       (15)
```

which is strictly negative for every `t>0`. Its real part is the even polynomial

```text
K(t^2),
K(s)=s^12+35s^11+472s^10+3405s^9+14905s^8+41966s^7
    +77881s^6+95385s^5+75478s^4+36617s^3+9715s^2+1032s-12.
                                                                    (16)
```

Descartes' rule gives at most one positive zero, while `K(0)<0<K(1)`, so exactly one occurs. Therefore the curve `F_2(it)` starts, as `t downarrow 0`, just below the negative real axis and ends at `1` through the lower half-plane. The continuous branch selected at infinity satisfies

```text
-pi<Delta_2(t)<0,
lim_(t downarrow 0) Delta_2(t)=-pi.                         (17)
```

As the universal strip theorem (3c) requires, for every positive `t` the continuous branch equals the principal argument in `(-pi,0)`, but its endpoint is the one-sided limit `-pi`. Assigning the conventional principal value `Arg F_2(0)=+pi`, or otherwise resetting the branch at the negative real zero-endpoint, produces a `2pi` error. The inertia audit agrees exactly: `R_2` has inertia `(3,4,0)`, `C5` has `(3,2,0)`, and the joined graph has `(5,7,0)`, so (6) gives `-pi`.

This example is nonsingular on both sides and in the join. The branch issue is therefore not a zero-mode artifact.

## 5. Consequence for the hostile remainder

Equations (1)--(7) are a safe exact starting point.  In particular, (3c) validates the principal branch for every positive `t`; no full winding is hidden there.  The examples nevertheless prove that neither of the following shortcuts is available in the actual `k=1` state (already with a bridge-free rank-six center and permitted zero-rank payload):

1. a universal pointwise sign for the bridge phase correction `Delta`; or
2. resetting its positive-`t` principal lift to the conventional principal value at `t=0` without taking the one-sided limit.

They do not obstruct an **area** inequality. The weakest missing theorem remains

```text
sigma(R)+1-(2/pi) integral_0^infinity t Delta(t) dt
   >= -sigma(U).                                            (18)
```

Any proof of (18) must couple the signed phase area to `sigma(R)` (or exploit more structure than rank and bridgelessness). Separate anti-Herglotz half-plane signs of `m_U,m_R` cannot by themselves pay the hostile debit, because multiplication destroys half-plane closure and the correction in Section 3 crosses the real axis.

## 6. Exact reproduction

Run

```text
python research/open-audits/coupled-coulson-phase-obstructions-verifier.py
```

The verifier is dependency-free and uses rational polynomial arithmetic and
Sturm sequences.  It independently reconstructs the graph and rooted-minor
characteristic polynomials, joined-graph characteristic polynomials, bridge
sets, and inertia triples, and checks the real/imaginary numerator polynomials
and positive-root counts used in (9)--(16).  No floating-point comparison is
used.  Run it both normally and with `python -O`; its gates are unconditional.
