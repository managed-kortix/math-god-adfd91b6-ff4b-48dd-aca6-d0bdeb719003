# Cycle 141: projective Kummer localization density and the missing reciprocity bridge

The exact `433a1` computations of Cycles 135--136 suggest separating two
logically different mechanisms.  Kummer theory and Chebotarev readily produce
pairs of auxiliary primes at which two fixed rational points have an invertible
localization matrix.  They do **not** by themselves make the two-prime Kurihara
number nonzero.  The missing bridge is an explicit reciprocity theorem comparing
the Kurihara/Kato derivative with the rational-point determinant line.

Let `p` be odd, put `V=E[p]`, and suppose

\[
\operatorname{Gal}\bigl(\mathbf Q(E[p],p^{-1}P,p^{-1}Q)/\mathbf Q\bigr)
 \simeq (V\oplus V)\rtimes\operatorname{GL}(V).
\]

This hypothesis includes both surjectivity of the residual representation and
maximality of the two-point Kummer kernel.  A Frobenius element can be written

\[
g=(u,v,A),\qquad u,v\in V.
\]

Condition on `A` being a nonidentity unipotent.  Then

\[
C_A=V/(A-I)V
\]

is one-dimensional, and the localizations of `P,Q` are represented by

\[
(\bar u,\bar v)\in C_A^2.
\]

For fixed `A`, the map `V^2 -> C_A^2` is surjective with every fiber of size
`p^2`.  Hence a coordinate row is uniform in `F_p^2` after choosing a basis of
`C_A`.  The coordinate row itself is not canonical: conjugacy and a local basis
change multiply both entries by the same unit.  The intrinsic datum is therefore

\[
(0,0)\quad\text{or}\quad[\bar u:\bar v]\in\mathbf P^1(\mathbf F_p).
\]

All nonidentity unipotents form one conjugacy class of size `p^2-1`, and

\[
|\operatorname{GL}_2(\mathbf F_p)|=p(p-1)^2(p+1).
\]

Thus their prime density is

\[
\frac{1}{p(p-1)}.
\]

Conditioned on this Frobenius class,

\[
\Pr(\text{zero row})=\frac1{p^2},
\qquad
\Pr(\text{a fixed projective direction})=\frac{p-1}{p^2}.
\]

Consequently two independently ranged auxiliary primes have an invertible
two-point localization matrix with conditional density

\[
\boxed{
\frac{|\operatorname{GL}_2(\mathbf F_p)|}{p^4}
=\left(1-\frac1p\right)\left(1-\frac1{p^2}\right).
}
\]

Conditioned further on both rows being nonzero, the density is `p/(p+1)`.
Among all ordered prime pairs, the corresponding product density is

\[
\boxed{\frac{p+1}{p^5}}.
\]

For `p=7`, these values are

\[
\frac1{42},\qquad \frac{288}{343},\qquad\frac8{16807}.
\]

The identity Frobenius must be excluded: the congruences
`ell = 1 (mod p)` and `a_ell = ell+1 (mod p)` alone also permit `A=I`, for
which `C_A` is two-dimensional.  Literal equidistribution in a canonically
identified `F_p^2` is also false; only zero and projective direction are
conjugacy-invariant Chebotarev conditions.

For `433a1,p=7`, exact exploratory arithmetic on 37 auxiliary-prime pairs found

\[
\widetilde\delta^{(1)}_{qr}=0
\quad\Longleftrightarrow\quad
\det L_{q,r}=0
\]

in every tested case.  The nonzero ratio `delta/det` attained every element of
`F_7^times`, and an exact four-prime rectangle disproved factorization of that
ratio into independent prime-local units.  This is evidence only, not a
theorem or a committed certificate census.

The theorem-strength gap is therefore a vanishing-locus reciprocity statement,
not the Chebotarev count.  One would need to prove, with canonical determinant
lines and all integral normalizations specified, that the two-prime
Kurihara/Kato leading term is a unit multiple of the rational-point
localization determinant.  Existing Kato/Kurihara theory instead identifies
the Kurihara scalar with a `p`-local dual-exponential image of a core-rank-one
derived Kolyvagin class.  A two-prime derivative must not be renamed a
rank-two Kolyvagin system.

There is one useful correction to Cycles 135--136.  The explicit determinant

\[
\det\begin{pmatrix}1&5\\1&4\end{pmatrix}=6\ne0
\]

already proves that the displayed rational points are independent modulo seven
and hence gives rank at least two.  Kim's Kurihara theorem supplies the Selmer
upper bound.  Thus no separate database or descent rank determination is needed
to sandwich the rank, provided every hypothesis of Kim's theorem has been
independently verified.  The determinant alone gives no upper bound: an extra
Selmer class could lie in the kernel of the chosen localization map.

Reproduce the finite-group counts at `p=7` with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle141_kummer_density.py
```

This is a conditional Chebotarev mechanism and a precise gap statement, not a
new BSD theorem and not a proof of the complex leading-coefficient formula.
