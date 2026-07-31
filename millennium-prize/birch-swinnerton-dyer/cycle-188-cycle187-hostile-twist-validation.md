# Cycle 188: hostile validation of the Cycle 187 twist formula

## Verdict

The Cycle 187 base-symbol formula passes an exact comparison with direct
`msfromell` twist symbols for both parity cases, `q=3` and `q=5`, at every
`a=1,...,28`.  There is no missing period factor, global sign, or endpoint
translation in (187.3)/(187.9).

The exact convention validated here is

\[
 [a/29]^+_{E^{(D_q)}}=
 \sum_{u=1}^{q-1}\left(\frac uq\right)
 \left[a/29+u/q\right]^{\chi_q(-1)}_E,                 \tag{188.1}
\]

for these two twists.  Their exact differential factor is one, so
`kappa_q=1`.  Changing `+u/q` to `-u/q` multiplies the result by
`chi_q(-1)`: it is a genuine sign error for `q=3`, and is invisible for
`q=5`.

## Pinned inputs

The base curve is

\[
 E=[1,0,0,0,1],\qquad y^2+xy=x^3+1,
\]

and all symbols use PARI's path `[oo,r]`, which represents
`[r]-[oo]`.  The direct twist models and minimization changes are:

| `q` | `D_q` | minimal model | change `[u,r,s,t]` | conductor |
|---:|---:|---|---|---:|
| 3 | -3 | `[1,-1,0,0,-27]` | `[1,0,1,0]` | 3897 = 433*3^2 |
| 5 | 5 | `[1,1,0,0,125]` | `[1,0,1,0]` | 10825 = 433*5^2 |

In both changes the differential scaling coordinate is `u=1`.  Thus the
minimalization introduces no Neron-differential multiplier.  Equivalently,

\[
 \frac{\Omega_E^-}{\sqrt3\,\Omega_{E^{(-3)}}^+}=1,
 \qquad
 \frac{\Omega_E^+}{\sqrt5\,\Omega_{E^{(5)}}^+}=1.       \tag{188.2}
\]

No factor of two arises from real components: all three curves have negative
discriminant and one real component.

## All-symbol comparison

Listed in order `a=1,...,28`, direct `msfromell(E_q,1)` gives:

```text
q=3:
3, 5/2, -1/2, -5/2, 3/2, 1, 1/2, -3, -5/2, -3/2, -1, 5/2,
0, 0, 0, 0, 5/2, -1, -3/2, -5/2, -3, 1/2, 1, 3/2, -5/2,
-1/2, 5/2, 3

q=5:
-1/2, 0, 0, 3/2, -1/2, 0, 1, 1/2, 0, -3/2, 1/2, 1/2,
-1/2, -1, -1, -1/2, 1/2, 1/2, -3/2, 0, 1/2, 1, 0, -1/2,
3/2, 0, 0, -1/2
```

The Cycle 187 sum with the base minus symbol for `q=3` and base plus symbol
for `q=5` reproduces these vectors entry by entry as exact rationals: 56 of
56 rows agree.  Every denominator is `1` or `2`, hence is 7-integral.

As a hostile translation test, replacing each endpoint

\[
 (aq+29u)/(29q)=a/29+u/q
\]

by `(aq-29u)/(29q)=a/29-u/q` gives the negative of every nonzero `q=3`
row and leaves every `q=5` row unchanged.  Therefore

\[
 \sum_u\chi_q(u)[a/29-u/q]_E^{\epsilon_q}
 =\epsilon_q[a/29]^+_{E^{(D_q)}}.                         \tag{188.3}
\]

An implementation using the minus translation must insert the missing factor
`epsilon_q=chi_q(-1)`; the committed Cycle 187 formula uses the plus
translation and needs no such factor.

## Kurihara coordinate

With the full integer discrete logarithm `log_2(a)` in `0,...,27`, both the
direct rows and Cycle 187 rows give

| `q` | exact weighted sum | residue `c_2(q,29)` in `F_7` |
|---:|---:|---:|
| 3 | -44 | 5 |
| 5 | -14 | 0 |

The minus-translation variants are respectively `44` and `-14`, confirming
the same `epsilon_q` sign rule at the derived-coordinate level.

The paired formula (187.5) is, as stated there, an identity after reduction
modulo seven, not an equality of the unreduced integer-log sums.  Using
`2 log_2(a)` for `1<=a<=14` gives unreduced totals `-72` for `q=3` and
`-70` for `q=5`; these reduce to `5` and `0`, respectively.  Treating the
pairing as an exact rational identity before reducing logarithms would be a
translation from `F_7` back to the integers that Cycle 187 does not claim.

## Error inventory

1. **Missing factor in Cycle 187:** none.  `kappa_3=kappa_5=1` on the actual
   minimal models, and no factor two or Manin factor appears.
2. **Sign error in Cycle 187:** none under PARI's `[oo,r]` convention and the
   pinned positive Gauss sum.  The base minus orientation agrees with
   `msfromell` for `q=3`.
3. **Translation error in Cycle 187:** none.  The required cusp is exactly
   `a/29+u/q=(aq+29u)/(29q)`.
4. **Hostile alternative:** using `a/29-u/q` without multiplying by
   `chi_q(-1)` is wrong.  It negates all odd-character (`q=3 mod 4`) rows.
5. **Pairing scope:** (187.5) is only a modulo-seven formula.  Promoting it to
   an unreduced equality loses multiples of seven.

## Reproduction

Run with PARI/GP supporting `msfromell`:

```sh
gp -q millennium-prize/birch-swinnerton-dyer/verify_cycle187_base_twist_hostile.gp
```

The verifier constructs both direct twist spaces, emits every exact row,
checks the conductor and differential factor, compares both endpoint
translations, verifies the paired residue, and fails closed on any mismatch.
The validation reported here used PARI/GP 2.15.4.
