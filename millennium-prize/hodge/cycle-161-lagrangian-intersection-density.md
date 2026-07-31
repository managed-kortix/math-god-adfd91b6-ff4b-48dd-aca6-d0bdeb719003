# Cycle 161: exact Lagrangian intersection strata and the eta-one locus

Let `p` be a prime, let `V` be a twelve-dimensional symplectic
`F_p`-space, and fix a nondegenerate symplectic six-space `G=Gamma[p]`.
For the polarization of the Cycle 151 seed this torsion decomposition is valid
only at good primes `p>=5`; it is not a decomposition into `O_K/p`-submodules.
Then

\[
V=G\mathbin\perp H,\qquad H=G^\perp,
\]

with both summands symplectic of dimension six.  Let `K` range over the
maximal isotropic subspaces of `V`; thus `dim K=6`.  Put

\[
a=\dim(K\cap G),\qquad b=\dim(K\cap H),\qquad r=3-a,
\qquad s=3-b.
\]

The stabilizer `Sp(G) x Sp(H)` classifies `K` by the pair `(a,b)`, subject to

\[
0\leq a,b\leq3,\qquad a=b.
\]

Indeed, after quotienting by `A=K cap G` and `B=K cap H`, the residual
Lagrangian is the graph of an anti-symplectic isomorphism

\[
A^\perp/A\longrightarrow B^\perp/B.
\]

The two quotient dimensions must agree, forcing `a=b`.  Conversely every such
graph gives a maximal isotropic `K`.  Hence there are exactly four stabilizer
orbits, indexed by

\[
d=\dim(K\cap\Gamma[l])=0,1,2,3.
\]

The formulas below remain valid for an abstract symplectic space over any
finite field `F_q`, but substituting `q=p^e` does **not** count kernels in
`A[p^e]`, which are modules over `Z/p^e Z`, not vector spaces over `F_(p^e)`.

Write the Gaussian coefficient as

\[
{3\brack d}_q=\prod_{i=0}^{d-1}\frac{q^{3-i}-1}{q^{d-i}-1}.
\]

The number of `d`-dimensional isotropic subspaces in a symplectic six-space is

\[
I_{3,d}(q)={3\brack d}_q\prod_{i=0}^{d-1}(q^{3-i}+1).
\]

For fixed intersections `A subset G` and `B subset H`, the number of
anti-symplectic isomorphisms between the residual symplectic spaces of
dimension `2(3-d)` is `|Sp_{2(3-d)}(q)|`.  Therefore the exact stratum size is

\[
\boxed{N_d(q)=I_{3,d}(q)^2|Sp_{2(3-d)}(q)|},
\qquad
|Sp_{2m}(q)|=q^{m^2}\prod_{i=1}^m(q^{2i}-1).
\]

Expanded, the four counts are

\[
\begin{aligned}
N_0(q)&=q^9(q^2-1)(q^4-1)(q^6-1),\\
N_1(q)&=q^4(q^2-1)(q^4-1)(q^2+q+1)^2(q^3+1)^2,\\
N_2(q)&=q(q^2-1)(q^2+1)^2(q^2+q+1)^2(q^3+1)^2,\\
N_3(q)&=(q+1)^2(q^2+1)^2(q^3+1)^2.
\end{aligned}
\]

Their sum is the standard number of Lagrangians in `V`:

\[
\boxed{N_{\rm all}(q)=\prod_{i=1}^6(q^i+1)}.
\]

Equivalently, the exact probability that a uniformly chosen maximal isotropic
has intersection dimension `d` is

\[
\boxed{P_d(q)=\frac{N_d(q)}{\prod_{i=1}^6(q^i+1)}}.
\]

For the prime-level incidence invariant used in the isogeny transport audit,

\[
\eta(K)=\frac{p^3}{|K\cap\Gamma[p]|},
\]

one has

\[
\boxed{\eta(K)=p^{3-d}.}
\]

Consequently the four strata are

| `d=dim(K cap Gamma[l])` | `eta` | exact count |
|---:|---:|---:|
| `0` | `p^3` | `N_0(p)` |
| `1` | `p^2` | `N_1(p)` |
| `2` | `p` | `N_2(p)` |
| `3` | `1` | `N_3(p)` |

Thus `eta=1` is exactly the `d=3` orbit: `K cap Gamma[l]` is a Lagrangian
three-space in `Gamma[l]`, and `K cap Gamma[l]^perp` is likewise Lagrangian.
In fact

\[
K=(K\cap\Gamma[l])\oplus(K\cap\Gamma[l]^\perp),
\]

so these are precisely the kernels adapted to the orthogonal decomposition.
Their exact density is

\[
\boxed{
P_{\eta=1}(p)=
\frac{(p+1)(p^2+1)(p^3+1)}
{(p^4+1)(p^5+1)(p^6+1)}.
}
\]

As `p` tends to infinity,

\[
P_0(p)=1-p^{-1}+O(p^{-2}),\qquad
P_1(p)=p^{-1}+O(p^{-2}),
\]

and more generally

\[
\boxed{P_d(p)=p^{-d^2}\bigl(1+O(p^{-1})\bigr).}
\]

Thus the whole nontransverse locus `d>=1` has density `l^-1+O(l^-2)`, but the
adapted `eta=1` locus is the deepest stratum and has exact decay

\[
\boxed{P_{\eta=1}(l)=l^{-9}\bigl(1+O(l^{-1})\bigr).}
\]

The intermediate strata `eta=l^2` and `eta=l` have densities asymptotic to
`l^-1` and `l^-4`, respectively; the generic transverse stratum has
`eta=l^3` and density tending to one.

This is an exact finite symplectic count.  Turning it into a density theorem
for arithmetic isogenies requires an independent monodromy/Chebotarev theorem
showing that the relevant kernels are equidistributed in the full Lagrangian
Grassmannian (or in specified stabilizer orbits).  The linear algebra alone
does not supply that arithmetic input or a Hodge-conjecture result.
