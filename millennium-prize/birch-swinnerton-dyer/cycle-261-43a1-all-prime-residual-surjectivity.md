# Cycle 261: all-prime residual surjectivity for `43a1`

## Result

Let

\[
 E/\mathbf Q:\quad y^2+y=x^3+x^2.
\]

For every rational prime `p`, the residual representation is surjective:

\[
 \bar\rho_{E,p}:G_{\mathbf Q}\longrightarrow
 \operatorname{GL}_2(\mathbf F_p),\qquad
 \operatorname{im}\bar\rho_{E,p}=\operatorname{GL}_2(\mathbf F_p). \tag{261.1}
\]

This is a theorem-level argument from the displayed equation, semistable
isogeny theorems, local Tate-curve inertia, and two exact point counts. It does
not use the LMFDB/Cremona `nonmax_primes` field or a Galois-image database.

## Global and local inputs

The integral invariants of the displayed equation are

\[
 b_2=4,\quad b_4=0,\quad b_6=1,\quad b_8=1,
 \quad c_4=16,\quad \Delta=-43,
 \quad j=-4096/43.                                      \tag{261.2}
\]

Thus the equation is minimal, `E` is semistable, and its only bad prime is
`43`, where it has multiplicative reduction of type `I_1`. In particular
`v_43(Delta_min)=1`.

For every prime `p`, inertia at `43` supplies a nontrivial transvection on
`E[p]`. If `p != 43`, this is the usual tame Tate-curve matrix

\[
 \begin{pmatrix}1&t_p(\sigma)\\0&1\end{pmatrix};
\]

the image of `t_p` contains `v_43(Delta)=1 mod p`. If `p=43`, the Tate
parameter has valuation one and is not a 43rd power; its Kummer class gives the
same nonzero unipotent. The nonsplit unramified quadratic character changes
Frobenius but is trivial on inertia. After conjugation, the image therefore
contains

\[
 U=\begin{pmatrix}1&1\\0&1\end{pmatrix}.                \tag{261.3}
\]

The determinant is the mod-`p` cyclotomic character and is onto
`F_p^times` for every `p`.

## Irreducibility at every prime

The precise semistable input is not the false statement that Mazur's general
rational-isogeny theorem forbids every prime-degree isogeny above 7. Its exact
prime-degree list is
`2,3,5,7,11,13,17,19,37,43,67,163`. The semistable lemma used in the proof of
Fermat's Last Theorem says instead:

> If `E/Q` is semistable and `E[p]` is reducible, then either `E` or an elliptic
> curve over `Q` that is `p`-isogenous to `E` has a rational point of order
> `p`.

Equivalently, the two characters on a rational isogeny filtration are, after
possibly passing to the dual isogeny, the trivial and mod-`p` cyclotomic
characters. Mazur's rational-torsion theorem then excludes `p>7`. Consequently
`E[p]` is irreducible for every `p>=11`. This corollary, not the general list of
isogeny degrees by itself, handles all of the allowed degrees, including 43.
No `43a1`-specific conductor or discriminant condition enters this
irreducibility step beyond semistability.

The remaining odd primes have explicit Frobenius witnesses. Direct counting
on the displayed equation gives

| `q` | `#E(F_q)` | `a_q` | `a_q^2-4q` |
|---:|---:|---:|---:|
| `2` | `5` | `-2` | `-4` |
| `3` | `6` | `-2` | `-8` |

If `E[p]` had a rational invariant line, every good Frobenius polynomial would
split modulo `p`. But `-4=2 mod 3`, `-8=2 mod 5`, and `-4=3 mod 7` are
nonsquares. Frobenius at `q=2,3,2` proves irreducibility at `p=3,5,7`,
respectively. Notice that `q` is always distinct from `p` and from the bad
prime 43.

For `p=2`, completing the square gives the 2-division polynomial

\[
 f_2(x)=4x^3+4x^2+1.
\]

Its six rational-root candidates do not vanish, so it is irreducible, and
`disc(f_2)=-16*43` is not a square in `Q`. Its Galois group is therefore `S_3`,
which is `GL_2(F_2)`. This already proves (261.1) at two.

## Exceptional-subgroup elimination

Let `G_p` be the image. Dickson's subgroup classification in the following
standard transvection form is enough:

> If `p >= 7` and an irreducible subgroup of `GL_2(F_p)` contains a
> transvection, then it contains `SL_2(F_p)`.

Indeed a subgroup containing an element of order `p` cannot lie in a Cartan
normalizer; if it does not contain `SL_2`, Dickson puts its projective image in
a Borel or in `A_4`, `S_4`, or `A_5`. Irreducibility excludes the Borel, and
none of the exceptional groups has order divisible by `p >= 7`. Thus (261.3)
and irreducibility give `SL_2(F_p) subset G_p` for every `p >= 7`. The
surjective determinant then gives `G_p=GL_2(F_p)`. This explicitly covers
`p=7`, `p=43`, and the entire large-prime tail.

At `p=3,5`, where exceptional projective groups can have order divisible by
`p`, the verifier performs the finite relative-position check. Any nonidentity
transvection in `GL_2(F_p)` is conjugate to `U`. Conjugating the whole image to
make that transvection equal to `U` preserves the trace and determinant of the
Frobenius matrix but does not fix its position. The verifier therefore
enumerates every invertible matrix `A` having the exact Frobenius trace and
determinant:

| `p` | witness | number of possible `A` | every `#<U,A>` | `#GL_2(F_p)` |
|---:|---|---:|---:|---:|
| `3` | `q=2`, `(tr,det)=(-2,2)` | `6` | `48` | `48` |
| `5` | `q=3`, `(tr,det)=(-2,3)` | `20` | `480` | `480` |

Hence the image is full at both primes, independently of how the inertia and
Frobenius eigenlines are positioned. Together with the `S_3` calculation at
two, this proves (261.1) for all primes.

## Reproduction and trust boundary

Run the exact, dependency-free verifier with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle261_43a1_residual.py
```

The script checks the division-polynomial discriminant, point counts,
Frobenius discriminants, and all small-prime matrix groups. Its checks use
explicit exceptions rather than Python `assert`, so `python3 -O` cannot turn a
failed check into `PASS`. The infinite tail is not a bounded database search:
it is discharged by the semistable reducibility lemma, Mazur's rational-torsion
theorem, and Dickson's subgroup theorem. The other external input is the
standard Tate-curve inertia formula.

References: B. Mazur, *Modular curves and the Eisenstein ideal*, Publ. Math.
IHES 47 (1977), 33--186 (rational torsion); B. Mazur, *Rational isogenies of
prime degree*, Invent. Math. 44 (1978), 129--162 (the general isogeny list);
J.-P. Serre, *Proprietes galoisiennes des points d'ordre fini des courbes
elliptiques*, Invent. Math. 15 (1972), 259--331, especially the semistable and
subgroup arguments; and the Tate-curve description in J. Silverman, *Advanced
Topics in the Arithmetic of Elliptic Curves*, Chapter V.

## Hostile audit of the conductor prime

The assertion at `p=43` needs a characteristic-43 argument, not the tame
formula used when `p!=43`. Over the unramified quadratic extension where the
curve is a Tate curve, write its parameter as `q`. Type `I_1` gives
`v_43(q)=1`. Over `Q_43(mu_43)`, the class of `q` in
`K^times/K^{times 43}` has nonzero valuation, so adjoining `q^(1/43)` is a
degree-43 Kummer extension. A generator of its wild inertia fixes `mu_43` and
sends `q^(1/43)` to `zeta_43 q^(1/43)`; on `E[43]` this is a nonidentity
unipotent, hence a transvection. The nonsplit multiplicative twist is
unramified and is therefore trivial on inertia. Thus the `p=43` transvection
claim is valid, but it specifically uses `v_43(Delta_min)=1` (more generally,
`43` not dividing that valuation), not merely the conductor value 43.

The hostile result is therefore `CORRECTED PASS`, not a retraction. The former
attribution to a blanket "Mazur semistable isogeny theorem" was imprecise, and
the verifier was not fail-closed under `python -O`; both defects are corrected
here. The all-prime conclusion survives.

## Consequence for Cycle 260

The residual-image item in the Cycle 260 closure packet is now closed, in the
stronger all-prime surjective form. In particular Cha's surjectivity hypothesis
at the ramified prime `p=7` is certified, and `p=43` is not an exception.
The exact normalized Heegner-point identity, Mordell--Weil/index certificate,
and independently replayed 2-descent identified there remain separate gaps;
this cycle makes no claim that `Sha(43a1/Q)=0` is already proved.
