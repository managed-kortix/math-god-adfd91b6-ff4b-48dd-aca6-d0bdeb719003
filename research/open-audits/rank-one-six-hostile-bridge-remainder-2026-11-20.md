# Rank-(1,6) hostile bridge remainder after the physical-hull reduction

Date: 2026-11-20. Status: **OPEN ANALYTIC REMAINDER / NONPROMOTIONAL**.

## Claim boundary

The exact physical-hull reduction in
`positive-square-energy/heptacyclic-general/physical-hull-bridge-reduction/theorem-note.md`
reduces every unresolved nontrivial positive-hull state, within simultaneous
physical-bridge cut partitions and the receipts stated there, to a marked
hostile rank-`(1,6)` bridge.  This note records the smallest remaining theorem
and the known route obstructions.  It does **not** close that theorem or the
global actual-hull-bridge lane.

Let `U` be a connected rank-one graph whose unique cycle has length
`q=1 (mod 4)`, with arbitrary rooted trees and marked bridge port `y`.  Let `R`
be the complete connected induced rank-six complement with marked port `x`, and
let `G=R+xy+U`.  Within the reduced unit-star residue, `R` inherits the same
center and all other unit hostile arms (or has one rank-six positive component
when the original star has one arm), together with its zero-rank trees and
chains.  Thus a theorem for every marked connected rank-six `R` would be
stronger than necessary, although every inequality below remains valid in that
larger class.  Put

```text
sigma(X)=s+(X)-|V(X)|,
Gamma(R,x;U,y)=s+(G)-s+(R)-s+(U).
```

Then the exact identity is

```text
sigma(G)=sigma(R)+sigma(U)+Gamma(R,x;U,y).              (1)
```

Consequently the weakest instance-exact missing theorem is

```text
sigma(R)+Gamma(R,x;U,y) >= -sigma(U).                   (2)
```

The cycle-only receipt `sigma(U)>=-delta_q`, where
`delta_q=sec(pi/q)-1`, gives the stronger sufficient target

```text
sigma(R)+Gamma(R,x;U,y) >= delta_q,                     (3)
```

and the length-uniform cap gives the still stronger sufficient target with
`delta_5=sqrt(5)-2`.  The known connected rank-six theorem supplies only
`sigma(R)>=0`; induced superadditivity supplies only `Gamma>=0`.  Neither alone
pays a hostile debit.

## Safe structural conclusions

1. A physical hull edge with rank split `2|5` or `3|4` dispatches by the
   completed lower-rank theorems and induced superadditivity; `2|5` is strict.
2. If no such edge exists, the reduced positive hull is a weighted star with
   unit-rank leaves and center weight `7-k`, for `1<=k<=7`.
3. An even unicyclic leaf dispatches weakly and a `3 mod 4` leaf dispatches
   strictly.
4. The unresolved outer states are marked hostile `1 mod 4` unicyclic arms
   against complete marked connected rank-six complements inheriting the
   remaining unit-star topology just described.  There are at most seven arm
   choices, but this is only a finite family of outer schemas, not a finite
   classification of the complements, ports, cycle lengths, or rooted tree
   messages.
5. The one-positive-component hull (a rank-seven bridge-free core with only
   zero-rank material beyond it) is outside this bridge reduction.

## Exact route obstructions

### A. A universal gain of `2/3` is false

The family and exact certificate are in
`research/open-audits/rank-one-six-bridge-gain-obstruction-2026-11-18.md` and
`research/rank-one-six-bridge-gain-obstruction-verifier.py`.  At the finite
member `t=10`, exact characteristic polynomials and rational Sturm intervals
give

```text
Gamma_10 < 66392469/100000000 < 2/3.
```

This refutes only the proposed universal `Gamma>=2/3` lemma.  It is not a
counterexample to `sigma(G)>=0`: the rank-six `K5` side has large reserve.

### B. Strict favorable credit is not spendable

For a triangle with `t` pendant leaves at each cycle vertex,

```text
sigma=2*sqrt(t+1)-sqrt(4t+1)>0,
```

but this tends to zero.  Therefore qualitative strictness from a favorable
rank-one arm cannot be converted into a fixed positive token.

### C. Bridge reselection need not improve the split

For every `p=2,...,7`, take a central positive component of rank `8-p` and
attach `p-1` hostile `C5` arms by independent bridge chains.  Every hull edge
has split `1|6`; for `p>=3`, having several positive components still forces
neither a balanced edge nor a favorable arm.

### D. Standard nonnegative-projector payment can be too small

Let `B_r` be `r` copies of `C5` sharing one vertex, with one pendant marked
vertex `u` at that common vertex.  If
`p_r=(Pi_+(A(B_r)))_{uu}` and `lambda_r>2` is the root of

```text
lambda^3-(2r+2)lambda-1=0,
```

then

```text
p_r=(3lambda_r^3+3lambda_r^2+2lambda_r+1)
    /((2lambda_r^3+1)(lambda_r^2+lambda_r+1)) < 1/(r+2).
```

Thus `p_1 p_6<1/24`.  For the hostile rank-one side `B_1`, its actual deficit
is greater than `5791/40000>1/7`.  Hence this standard projector-product token
cannot pay even that one hostile arm.  This is a route obstruction, not a graph
counterexample; the full joined graph is a cactus and its rank-six side has
additional reserve.

## Universal negative-part bridge certificate

There is nevertheless a clean universal lower bound on the **actual** bridge
gain.  It does not close the hostile remainder by itself.

For arbitrary real symmetric marked-side matrices `A_U,A_R`, let

```text
D=A_U direct_sum A_R,
E=e_y e_x^T+e_x e_y^T,
M=D+E,
Phi(H)=tr(H_+^2).
```

Here `H_+` is the positive-semidefinite positive spectral part and
`H_-=(-H)_+` is the positive-semidefinite negative spectral part.  Thus the
graph bridge gain is

```text
Gamma=Phi(M)-Phi(D).
```

Put

```text
P=D_+,       N=D_-,       Z=E-N,       W=Z_+,
rho=max(0,lambda_max(Z)).
```

Then

```text
Gamma >= Phi(E-D_-)=rho^2.                                (4)
```

Indeed, the exact variational identity

```text
Phi(H)=max_{X positive semidefinite}
       {2 tr(HX)-tr(X^2)}                                  (5)
```

has optimizer `X=H_+`.  The trial `X=P+W` is positive semidefinite.  Since
`M=P+Z` and `Phi(D)=tr(P^2)`, its value relative to `Phi(D)` is

```text
2 tr((P+Z)(P+W))-tr((P+W)^2)-tr(P^2)
 =2 tr(PZ)+2 tr(ZW)-tr(W^2)
 =tr(W^2).                                                  (6)
```

The two `tr(PW)` terms cancel between the linear and quadratic expressions;
no orthogonality of `P` and `W` is asserted.  The last equality uses
`tr(PZ)=tr(PE)-tr(PN)=0`: `P,N` are orthogonal spectral parts of the block-
diagonal matrix `D`, while `P` is block diagonal and `E` is block off
diagonal.  Spectral functional calculus gives `ZW=W^2`.

The quadratic form of `Z` is nonpositive on the codimension-one subspace
consisting of all vectors whose `y` coordinate on the `U` side is zero.
Consequently `Z` has at most one positive eigenvalue, so
`Phi(Z)=rho^2`, proving (4).

The value `rho` has an exact marked resolvent characterization.  Write
`N_U=(A_U)_-`, `N_R=(A_R)_-`, and for `t>0` put

```text
n_U(t)=<e_y,(tI+N_U)^(-1)e_y>,
n_R(t)=<e_x,(tI+N_R)^(-1)e_x>.
```

A Schur-complement determinant calculation gives

```text
det(tI-Z)=det(tI+N_U) det(tI+N_R)
           (1-n_U(t)n_R(t)).                               (7)
```

Both factors `n_U,n_R` are positive and strictly decreasing, and their product
tends to zero as `t` tends to infinity.  Define the **extended** limit

```text
L=lim_{t downarrow 0} n_U(t)n_R(t) in (0,infinity].
```

Then `L>1` exactly when `rho>0`, in which case `rho` is the unique positive
root of `n_U(rho)n_R(rho)=1`.  If `L<1`, then `rho=0`.  If `L=1`, then
`rho=0` and the coupled crossing occurs at the zero eigenvalue; this does not
assert that zero is simple or the only zero eigenvalue, because uncoupled
kernel modes may also occur.  Ordinary inverses at `t=0` are not part of the
statement.  Spectrally,

```text
n_U(t)=||Pi_ker(N_U)e_y||^2/t
       +<e_y,N_U^dagger e_y>+O(t),
```

and similarly on the `R` side, which makes the extended convention explicit.

For the hostile graph remainder, (4) yields the rigorous marked sufficient
condition

```text
sigma(R)+rho^2 >= -sigma(U).                               (8)
```

The true `Gamma` can be strictly larger than `rho^2`; no proof currently shows
that (8) holds automatically for every inherited unit-star residue.

### Monotone interpolation between the negative-part certificate and the gain

The endpoint certificate in (4) belongs to a continuous exact family.  Keep

```text
P=D_+,       N=D_-,       Z=E-N,       b=tr(P^2)=Phi(D),
H_t=Z+tP,
h(t)=Phi(H_t)-t^2 b                 (t>=0).
```

Because `P,N` are block diagonal spectral parts, `PN=0`; because `E` is block
off diagonal, `tr(EP)=0`.  Hence

```text
tr(ZP)=0.                                                   (9)
```

Then `h` is continuously differentiable, nondecreasing, and concave on
`[0,infinity)`, with the exact formulas

```text
h'(t)=2 tr(P(H_t)_-) >= 0,                                 (10)
h(s)-h(t)=2 integral_t^s tr(P(H_u)_-) du     (0<=t<=s),    (11)
h(t)=tr(Z^2)-Phi(-H_t).                                    (12)
```

Indeed, the scalar function `(x_+)^2` is continuously differentiable even at
zero, so spectral trace differentiation gives

```text
d/dt Phi(H_t)=2 tr(P(H_t)_+).
```

Since `tr(PH_t)=tb` and `H_t=(H_t)_+-(H_t)_-`, subtracting `2tb` proves
(10), and integration proves (11).  Alternatively, for `s>=t`, the positive-
semidefinite trial

```text
X=(H_t)_+ +(s-t)P
```

in (5) gives directly

```text
Phi(H_s)>=Phi(H_t)+(s^2-t^2)b.
```

For (12), use (9) to write

```text
tr(H_t^2)=tr(Z^2)+t^2b
         =Phi(H_t)+Phi(-H_t).
```

The map `H -> Phi(H)` is convex by (5), so (12) also proves concavity of
`h`.  This scalar trace-functional argument does not assert the false operator
claim that the negative-part matrix is Loewner monotone.

At the endpoints,

```text
h(0)=Phi(E-D_-)=rho^2,
h(1)=Phi(D+E)-Phi(D)=Gamma.                                 (13)
```

The first equality in (13) uses the single-edge fact that `E-D_-` has at most
one positive eigenvalue.  More generally `h(0)=Phi(E-D_-)`, not necessarily
the square of its largest eigenvalue.  For one unweighted graph bridge,
`tr(E^2)=2` and `tr(EN)=0`, so (12) also becomes

```text
h(t)=2+tr(N^2)-Phi(-H_t).                                   (14)
```

For a nontrivial interval `0<=t<s`, equality `h(s)=h(t)` holds exactly when
`tr(P(H_u)_-)=0` for every `u in [t,s]`, equivalently when the range of `P` is
orthogonal to the negative spectral subspace of `H_u` throughout that
interval.  Since `h` is differentiable, nondecreasing, and concave, the
single condition `tr(P(H_t)_-)=0` (equivalently `h'(t)=0`) at the left
endpoint already forces the later plateau.

The tangent bound has a sharper exact equality statement.  Put

```text
R_t=(H_t)_-,       q_t=tr(P R_t).
```

Firm nonexpansiveness of orthogonal projection onto the positive-semidefinite
cone gives, for `s>t`,

```text
(s-t)(q_t-q_s)
 =<R_t-R_s,(-H_t)-(-H_s)> >= ||R_t-R_s||_F^2.              (15a)
```

Thus `q_t` is nonincreasing.  If `R_t=R_s=R`, then the positive/negative
spectral decomposition gives

```text
tr(R H_t)=-tr(R^2)=tr(R H_s),
```

so `(s-t)tr(PR)=0`.  Hence `q_t>0` forces `q_s<q_t` for every `s>t`, whereas
`q_t=0` forces `q_s=0` thereafter.  Since
`h(1)-h(t)=2 integral_t^1 q_u du`, for every `0<=t<1` one therefore has

```text
q_t=0  ==>  Gamma=h(t),
q_t>0  ==>  0<Gamma-h(t)<2(1-t)q_t.                        (15b)
```

In particular, if `W=Z_+`,

```text
c=tr(W^2)=Phi(Z),       a=tr(PW),
```

then `tr(PZ)=0` implies `q_0=tr(PZ_-)=a`.  Consequently

```text
0<=Gamma-c<=2a,                                          (15c)
```

with equality throughout exactly when `a=0`; if `a>0`, both inequalities in
`0<Gamma-c<2a` are strict.  The identity `c=rho^2` in this paragraph retains
the single-edge (or, more generally, at-most-one-positive-eigenvalue) scope
stated above.

There is also an exact lower tail envelope.  Projection nonexpansiveness and
Cauchy--Schwarz give, for `u>=t`,

```text
q_u >= max(0,q_t-b(u-t)).                                  (15d)
```

For `L=1-t`, define, when `b>0`,

```text
Psi_L(q,b) = q^2/b                 if 0<=q<=bL,
             2qL-bL^2             if q>=bL.
```

If `b=0`, then `P=0` and `q=0`, and set `Psi_L(0,0)=0`.  Integrating (15d)
and combining it with (15b) gives the nonsmooth-safe sandwich

```text
h(t)+Psi_(1-t)(q_t,b) <= Gamma <= h(t)+2(1-t)q_t.          (15e)
```

Equality in the lower inequality is equivalent to
`q_u=max(0,q_t-b(u-t))` throughout `[t,1]`.  No eigenvalue-crossing
regularity beyond continuity is being assumed.

At `t=0`, this tail estimate has a useful elementary form.  The fixed trial
`W` in (5), and the tangent at zero from concavity, give for `0<=t<=1`

```text
c+2at-bt^2 <= h(t) <= c+2at.                               (15f)
```

Equivalently, the lower trial may be transported to the actual matrix `Z+P`
as `X=W+(1-t)P`.  Maximizing the lower quadratic over `0<=t<=1` yields

```text
Gamma >= c+psi(a,b),
psi(a,b) = a^2/b       if b>0 and 0<=a<=b,
           2a-b        if b>0 and a>=b,
           0           if b=0.                             (15g)
```

The `b=0` case has `P=0` and `a=0`.  Formula (15g) is a lower certificate,
not an identity; optimizing the full two-ray cone below may be stronger.

### Exact marked cyclic-space compression

All of these quantities admit a potentially much smaller exact baseline than
`b=Phi(D)`.  Write `D=A_U direct_sum A_R`, let `e_y,e_x` be the two marked
coordinate vectors, and define the sidewise cyclic spaces

```text
K_U=span{A_U^k e_y:k>=0},       K_R=span{A_R^k e_x:k>=0},
K=K_U direct_sum K_R.
```

Because the side matrices are symmetric, `K` is reducing for `D`; because the
coupling is the single marked edge, `E` acts only on `K`.  Hence on
`K direct_sum K^perp`,

```text
D=D_* direct_sum D_0,       E=E_* direct_sum 0.
```

The passive block `D_0` occurs identically before and after gluing, so the
bridge gain is exactly the gain of the active block.  If
`P=P_* direct_sum P_0` and `N=N_* direct_sum N_0`, then

```text
Z=Z_* direct_sum (-N_0),
H_t=H_(t,*) direct_sum (tP_0-N_0),       H_(t,*)=Z_*+tP_*,
Phi(H_t)=Phi(H_(t,*))+t^2 Phi(D_0),
Z_+=(Z_*)_+ direct_sum 0,
(H_t)_-=(H_(t,*))_- direct_sum N_0.                         (15h)
```

It follows that `Gamma`, `h(t)`, `c`, `a`, and `q_t` are exactly unchanged,
while every occurrence of `b` in (15d)--(15g) may be replaced by

```text
b_*=Phi(D_*)
   =sum_{lambda>0, Pi^U_lambda e_y !=0} lambda^2
    +sum_{mu>0, Pi^R_mu e_x !=0} mu^2.                     (15i)
```

Each supported distinct eigenvalue is counted once on each side.  A repeated
eigenspace on one side contributes only its marked cyclic direction, while a
numerically equal eigenvalue occurring on both sides is counted twice.  This
compression is exact, not a truncation: it removes only reducing spectral
modes invisible to the marked bridge.  Thus `c+psi(a,b_*)` and the tail bound
with `b_*` are always at least as strong as their uncompressed versions.

For rational symmetric side data and a coordinate mark, the active baseline
can be reconstructed exactly without computing eigenvectors.  Fix the
generic characteristic-polynomial convention

```text
chi_A(z)=det(zI-A),
m_i(z)=<e_i,(zI-A)^(-1)e_i>=chi_(A^(i))(z)/chi_A(z),
```

where `A^(i)` is the principal submatrix obtained by deleting marked row and
column `i`.  Let

```text
g_A=gcd_(Q[z])(chi_A,chi_(A^(i))),
d_(A,i)=monic(chi_A/g_A).                                  (15j)
```

Then the displayed resolvent is reduced after dividing numerator and
denominator by `g_A`.  Spectrally,

```text
m_i(z)=sum_lambda alpha_lambda/(z-lambda),
alpha_lambda=<e_i,Pi_lambda e_i>=||Pi_lambda e_i||^2.
```

Consequently `d_(A,i)` is monic and squarefree; its roots are exactly the
distinct real eigenvalues supported at the mark, and each root is a simple
pole of `m_i` with positive residue.  Applying (15j) directly to the two
marked sides gives

```text
b_*=sum_(lambda>0:d_(A_U,y)(lambda)=0) lambda^2
    +sum_(mu>0:d_(A_R,x)(mu)=0) mu^2.                       (15k)
```

The two sums are sidewise: a numerical eigenvalue shared by the sides is
counted once in each.  Sturm sequences can isolate and sign-classify the
roots.  Exact equality and non-strict or boundary comparisons require exact
real-algebraic sign arithmetic; a strict inequality may instead be certified
by rational isolating intervals refined until the sides separate.  A floating
pole sum is not a certificate.  For nonrational algebraic data, the same
construction requires a specified exact real coefficient field and embedding,
with effective polynomial-gcd, real-root, and sign arithmetic.

For a higher-rank cross coupling, the active space is the minimal `D`-reducing
subspace containing the range of `E`.  The scalar cofactor identity (15j)
remains valid for each coordinate mark, but the two scalar root sums in (15k)
compute `b_*` only for one coordinate generator on each side, equivalently a
rank-one off-diagonal cross block.  Higher rank requires the joint cyclic
spaces generated by the sidewise cross ranges; a supported eigenspace then
contributes its eigenvalue square with the dimension of its projected cross
range, rather than necessarily once.

Consequently every fixed `t in [0,1]` gives the rigorous bridge certificate

```text
Gamma >= Phi(E-D_-+tD_+)-t^2 Phi(D).                        (15)
```

For `t=0` this is (4); for `t=1` it is the identity `Gamma=Gamma`.  Thus
maximizing over the whole closed interval is tautological.  To close the
hostile remainder, one still needs a usable lower estimate at some `t<1`
that, together with `sigma(R)`, pays the arm deficit.  Conversely, (15c) is
an exact counterexample test when compared with the **actual** deficit: if
`d_U=-sigma(U)` and

```text
c+2a < d_U-sigma(R),
```

then `sigma(G)<0`.  If `d_U` is replaced by the larger uniform envelope
`delta_q`, the same strict inequality only refutes closure against that
stronger sufficient target; it does not imply a graph counterexample.

A different reusable strengthening is obtained from any finite collection of
positive-semidefinite rays `X_1,...,X_m`.  With

```text
h_i=tr(M X_i),       G_ij=tr(X_i X_j),
```

(5) gives the exact finite-cone certificate

```text
Gamma >= sup_{z_i>=0}
         {2 h^T z-z^T G z-Phi(D)}.                         (16)
```

The Gram matrix `G` is positive semidefinite.  This is only a lower bound on
`Gamma` unless the cone contains a true optimizer.  Taking the two rays `P,W`
and the feasible coefficients `(1,1)` recovers (4); optimizing those rays can
only improve it.  Explicitly, if

```text
b=tr(P^2),       a=tr(PW),       c=tr(W^2)=rho^2,
```

then the two-ray objective at `(s,t)` is

```text
2bs+2(a+c)t-bs^2-2ast-ct^2-b,       s,t>=0.                (17)
```

and its value at `(1,1)` is exactly `c`.

## Finite scout boundary

The companion packet
`research/finite-scouts/rank-one-six-bridge-gain/` reports no negative payment
value in four explicitly separated finite slices.  Its exhaustive Graph Atlas
slice and reported extrema are independently replayed with exact integer
characteristic polynomials and Sturm intervals.  The broad canonical-short
kernel and generated unit-star no-negative counts remain persisted numerical
census outputs: `final_verify.py` does not regenerate and Sturm-replay every
one of those joins.  They are reconnaissance, not evidence for (2) in full.

## Next theorem

Prove (2) for every actual marked hostile rank-`(1,6)` bridge, prove that the
marked condition (8), the active cyclic-space bound (15g)--(15i), an
interpolation/tail certificate (15e), or a stronger finite-cone certificate
(16) always pays the instance deficit on the inherited unit-star residue, or
derive a strictly stronger packet-specific induced owner partition that pays
the same deficit.
Reserve and bridge gain must be treated jointly.  Any projector, moment,
resolvent, or Coulson-phase inequality is useful only after it is
quantitatively compared with `-sigma(U)-sigma(R)` for all marked ports and
arbitrary rooted payloads.
