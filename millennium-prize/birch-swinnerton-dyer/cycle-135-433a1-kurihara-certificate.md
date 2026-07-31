# Cycle 135: an exact rank-two Kurihara certificate for 433a1

For

\[
E=433\mathrm a1:\quad y^2+xy=x^3+1,
\]

the prime `p=7` and auxiliary product

\[
n=29\cdot113
\]

give an exact nonzero two-prime Kurihara number.  This is a reproducible new
computational instance of a published Selmer-structure theorem, not a new BSD
theorem or a proof of the complex leading-coefficient formula.

Choose primitive roots

\[
\eta_{29}=2,\qquad \eta_{113}=3.
\]

Exact point counts give

\[
\#E(\mathbf F_7)=11,\quad a_7=-3,
\]

\[
\#E(\mathbf F_{29})=28,\quad a_{29}=2,
\qquad
\#E(\mathbf F_{113})=112,\quad a_{113}=2.
\]

Thus `7` is good ordinary and nonanomalous, while both auxiliary primes satisfy

\[
\ell\equiv1\pmod7,
\qquad
a_\ell\equiv\ell+1\pmod7.
\]

Using PARI's exact period-normalized plus modular symbols, group the 3136 unit
residues modulo `3277` by their two discrete logarithms modulo seven.  The exact
grouped matrix is

```text
[ 13 -18 -14  24   9 -18   8
  22  -1 -24  -4  23 -13  -8
   4  30 -16 -10  12   2 -24
  -9  13  11 -24  11  13  -9
 -24   2  12 -10 -16  30   4
  -8 -13  23  -4 -24  -1  22
   8 -18   9  24 -14 -18  13 ]
```

Weighting entry `(i,j)` by `ij` modulo seven gives total

\[
\boxed{
\widetilde\delta^{(1)}_{29\cdot113}(E)=3\in\mathbf F_7^\times.
}
\]

The row and column contribution checks are

```text
rows:    0,2,2,5,4,1,3
columns: 0,3,3,6,4,3,5
```

and each totals `3 mod 7`.

Kim's published Theorem 1.8 gives Selmer corank at most two from this nonzero
two-prime value.  The explicit points and invertible localization matrix of
Cycle 136 supply the reverse rank inequality without a separate database or
descent rank determination.  Under the theorem's residual-surjectivity and Manin-normalization
hypotheses, the unit valuation then yields

\[
\operatorname{Sel}(\mathbf Q,E[7^\infty])
\simeq(\mathbf Q_7/\mathbf Z_7)^2,
\qquad
\Sha(E/\mathbf Q)[7^\infty]=0.
\]

The curve has minimal discriminant `-433`, conductor `433`, Tamagawa product
one, Manin constant one, and maximal mod-seven image according to the audited
curve data.  The points `(0,1)` and `(-1,1)` lie on the curve; the rigorous rank
two lower bound is independently certified by Cycle 136; the upper bound still
comes from Kim's published theorem and is not re-proved by the dependency-free
verifier.

The exact residue depends on primitive-root conventions up to a nonzero unit;
nonvanishing is canonical.  Literature searches found published rank-two
Kurihara examples for `389a1` and `3456a1`, but not this `433a1,p=7` instance.
The general theorem and its arithmetic implication are prior work, and database
predictions already suggest trivial Sha.  The claim here is therefore an exact,
apparently unprinted computational certificate and replayable application—not
mathematical novelty at Millennium scale.

Reproduce the modular symbols with a PARI/GP installation supporting
`msfromell`:

```sh
gp -q millennium-prize/birch-swinnerton-dyer/cycle135_433a1_kurihara.gp
```

Verify the compact certificate and local arithmetic with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle135_433a1_kurihara.py
```

No full BSD or Millennium solution is claimed.
