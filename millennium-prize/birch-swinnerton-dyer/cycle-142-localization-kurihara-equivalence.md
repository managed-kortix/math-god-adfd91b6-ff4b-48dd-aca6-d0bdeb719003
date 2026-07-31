# Cycle 142: localization determinants force Kurihara nonvanishing

This cycle closes the one-way gap left in Cycle 141.  The bridge is not a
termwise scalar identity between a rational-point determinant and a Kurihara
number.  Instead, global Tate reciprocity makes the auxiliary determinant force
injectivity of `p`-singular localization on the modified canonical Selmer
group.  Kolyvagin-system rigidity and Kato's explicit reciprocity then force the
Kurihara number to be nonzero.

## The residual theorem

Let `p>=5`, let `T=E[p]`, and assume the standard Mazur--Rubin and Kim
hypotheses needed for:

- self-dual cartesian finite local conditions;
- one-dimensional finite and transverse lines at genuine Kolyvagin primes;
- Kato's core-rank-one residual Kolyvagin system;
- its primitivity;
- the residual pointwise explicit reciprocity law at `p`, with local torsion
  exponent zero.

Suppose the classical residual Selmer group has basis `P,Q`:

\[
S=\operatorname{Sel}(\mathbf Q,E[p])
  =\mathbf F_p P\oplus\mathbf F_p Q.
\]

For distinct genuine Kolyvagin primes `q,r`, choose arbitrary generators of
the finite local lines and define

\[
D_{q,r}(P,Q)=
\det\begin{pmatrix}
\operatorname{loc}_q P&\operatorname{loc}_q Q\\
\operatorname{loc}_r P&\operatorname{loc}_r Q
\end{pmatrix}.
\]

Then

\[
\boxed{
D_{q,r}(P,Q)\ne0
\quad\Longrightarrow\quad
\widetilde\delta^{(1)}_{qr}(E)\ne0.
}
\]

If Kim's minimal-support localization theorem applies and the minimal
Kurihara order is two, the reverse implication also holds.  Hence in the
rank-two primitive situation,

\[
\boxed{
D_{q,r}(P,Q)\ne0
\quad\Longleftrightarrow\quad
\widetilde\delta^{(1)}_{qr}(E)\ne0.
}
\]

## Proof of the new direction

At each auxiliary prime there is an orthogonal decomposition

\[
H^1(\mathbf Q_\ell,T)
=H^1_f(\mathbf Q_\ell,T)\oplus H^1_{\rm tr}(\mathbf Q_\ell,T),
\]

where both summands are lines and the finite--transverse Tate pairing is
perfect.

Assume `D_{q,r}!=0`.  Then

\[
S\xrightarrow{\sim}
H^1_f(\mathbf Q_q,T)\oplus H^1_f(\mathbf Q_r,T).
\tag{1}
\]

Let `c` satisfy finite local conditions at `p` and away from `qr`, and
transverse conditions at `q,r`.  Pair `c` globally with `P` and `Q`.  Every
local Tate pairing away from `q,r` vanishes because both classes satisfy the
self-annihilating finite conditions.  Global reciprocity gives two linear
equations pairing the transverse coordinates of `c` with the two rows in
(1).  Since the determinant is nonzero and the local pairings are perfect,

\[
\operatorname{loc}_q c=\operatorname{loc}_r c=0.
\]

Thus `c` lies in the strict-at-`q,r` subgroup of `S`, which is zero by the
injectivity in (1).  Therefore

\[
\boxed{
H^1_{f\text{ at }p,\,\mathrm{tr}\text{ at }q,r}(\mathbf Q,T)=0.
}
\tag{2}
\]

Now use the canonical modified Selmer structure: relaxed at `p`, transverse at
`q,r`, and finite elsewhere.  The kernel of its singular localization

\[
\operatorname{loc}_p^s:
H^1_{\mathcal F_{\rm can}(qr)}(\mathbf Q,T)
\longrightarrow H^1_s(\mathbf Q_p,T)
\]

is exactly the group in (2).  Hence this map is injective.  Core rank one and
Poitou--Tate show that its source is one-dimensional and its dual modified
Selmer group is zero: `qr` is a core vertex.

For a primitive residual core-rank-one Kolyvagin system, stub rigidity says
that the component at every core vertex generates the one-dimensional stub.
Consequently

\[
0\ne\bar\kappa^{\rm Kato}_{qr}
\in H^1_{\mathcal F_{\rm can}(qr)}(\mathbf Q,T).
\]

Injectivity gives

\[
\operatorname{loc}_p^s(\bar\kappa^{\rm Kato}_{qr})\ne0.
\]

Kim's pointwise refined explicit reciprocity law identifies the image of this
singular localization under the normalized dual exponential with a unit times
`delta_qr`.  Therefore `delta_qr!=0`.

This proof explains why an unspecified scalar formula was unnecessary.  It
also explains the exact limitations:

- `P,Q` must span the **full** residual classical Selmer group, not merely a
  chosen rational subspace;
- the primes must have genuine complementary one-dimensional finite and
  transverse local conditions;
- primitivity is needed to make the component at the resulting core vertex
  nonzero;
- the local torsion and normalization factors in explicit reciprocity must be
  `p`-units.

## The `433a1,p=7` consequence

For

\[
E: y^2+xy=x^3+1,
\qquad P=(0,1),\quad Q=(-1,1),
\]

Cycle 135 gives

\[
\widetilde\delta^{(1)}_{29\cdot113}=3\ne0\pmod7.
\]

Kim's theorem gives the residual Selmer upper bound, while Cycle 136 gives

\[
\det\begin{pmatrix}1&5\\1&4\end{pmatrix}=6\ne0,
\]

so `P,Q` give the matching lower bound and form a basis of the full residual
Selmer group.  The nonzero Kurihara component also makes Kato's residual
Kolyvagin system primitive.  Subject to the already recorded residual-image,
Manin, Tamagawa, and local hypotheses, the equivalence above therefore applies
to every genuine two-prime Kolyvagin product for this curve.

The exact exploratory data through 87 tested pairs--75 nonzero/nonzero and 12
zero/zero--are explained by this theorem, but are not used in its proof.

## Positive-density production

Residual surjectivity and independence of `P,Q` imply maximality of the
two-point Kummer extension.  Indeed, restriction is injective by Sah's lemma,
and the image in `E[p]^2` is a `GL_2(F_p)`-submodule.  If it were proper with
both coordinate projections nonzero, it would be the graph of a scalar
endomorphism, contradicting independence.

Cycle 141's projective Chebotarev count now combines with the proved converse.
Among ordered pairs of primes, the lower density of pairs with nonidentity-
unipotent Frobenius and nonzero two-prime Kurihara number is

\[
\boxed{\frac{p+1}{p^5}}.
\]

Conditioned on both primes having nonidentity-unipotent Frobenius, the density
is

\[
\boxed{
\left(1-\frac1p\right)\left(1-\frac1{p^2}\right).
}

For `p=7`, these are respectively

\[
\frac8{16807},\qquad\frac{288}{343}.
\]

Finite ramified or normalization-exception sets and the diagonal `q=r` have
zero pair density.  For unordered pairs the asymptotic count is half the
ordered count, while the density relative to all unordered pairs is the same.

This is a positive-density family theorem for mod-`p` two-prime Kurihara
nonvanishing under the stated rank-two/primitivity hypotheses.  It remains an
application and synthesis of Kolyvagin-system and explicit-reciprocity theory;
it does not prove the complex BSD leading-coefficient formula or any
Millennium problem.
