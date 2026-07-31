# Cycle 190: final fail-closed certificate through `L_0`

## Theorem

Let

\[
 E: y^2+xy=x^3+1,\quad p=7,\quad P=(0,1),\quad Q=(-1,1),
\]

and let

\[
 L_0=\mathbf Q(E[7],7^{-1}P,7^{-1}Q).
\]

Fix `ell=29`, `eta=2 mod 29`, and the frozen admissible domain of primes `q`
defined by

```text
(q,2*7*29*433)=1, (q/29)=1, w(E^(D_q))=-1,
q=1 mod 7, a_q(E)=2 mod 7, and v_7(#E(F_q))=1,
```

where `D_q=q` for `q=1 mod 4` and `D_q=-q` for `q=3 mod 4`. Define
`V(q)` to mean `c_eta(q,29)=0 mod 7`, with `c_eta` the exact one-prime
modular-symbol coordinate fixed in Cycle 181.

**Theorem (strict `L_0`-nonfactorization).** There is no conjugacy-invariant
function

\[
 f:\operatorname{Gal}(L_0/\mathbf Q)\longrightarrow\{0,1\}
\]

such that `V(q)=f(Frob_q)` for every prime in the frozen domain. Equivalently,
the vanishing predicate is not Frobenian through `L_0` in this exact,
no-exception sense.

Indeed, the primes

\[
 q_0=29023,\qquad q_1=1499
\]

are in the domain and have the same Frobenius conjugacy class in `L_0`, namely
`(nonidentity unipotent,[1:5])`, whereas

\[
 c_\eta(29023,29)=0,\qquad c_\eta(1499,29)=4\ne0\pmod7.
\]

Here “no-exception” is essential. A standard Frobenian set is often defined
only up to finitely many exceptional primes. One finite collision does not
disprove that weaker eventual notion, and this report makes no such claim.
It also makes no BSD claim, density claim, or nonfactorization claim for fields
strictly larger than `L_0`.

## Prime and packet certificate

The dependency-free verifier proves primality by trial division through the
integer square root and checks all packet predicates exactly. Its finite-field
replay gives

| `q` | `D_q` | `#E(F_q)` | `a_q` | `v_7(#E)` | `(q/29)` | root number |
|---:|---:|---:|---:|---:|---:|---:|
| 29023 | -29023 | 29050 | -26 | 1 | 1 | -1 |
| 1499 | -1499 | 1526 | -26 | 1 | 1 | -1 |

Both primes are `1 mod 7`; both traces are `2 mod 7`. Thus the residual
characteristic polynomial is `(T-1)^2`. The Frobenius is not the identity,
because identity on `E[7]` would force all 49 points of `E[7]` into
`E(F_q)`, contrary to `v_7(#E(F_q))=1`. Hence both residual classes are the
unique nonidentity-unipotent conjugacy class in `GL_2(F_7)`.

The auxiliary condition also follows directly: `a_29(E)=2`, and
`(D_q/29)=(q/29)=1`, so
`a_29(E^(D_q))=2=29+1 mod 7` for both primes.

## Explicit Kummer witnesses and transport

Use the exact change of variables

\[
 X=4x,\qquad W=8y+4x,
\]

which transports `E` to `W^2=X^3+X^2+64` and sends
`P` to `(0,8)` and `Q` to `(-4,4)`. For `n_q=#E(F_q)/7`, exact scalar
multiplication gives

| `q` | `n_q` | `n_q P` | `n_q Q` | checked relation |
|---:|---:|:---:|:---:|:---:|
| 29023 | 4150 | `(24326,16085)` | `(19138,16433)` | `n_q Q=5 n_q P` |
| 1499 | 218 | `(1042,847)` | `(1463,497)` | `n_q Q=5 n_q P` |

Each displayed `n_q P` is nonzero and killed by 7. It therefore generates the
one-dimensional quotient detected by localization, and the ordered Kummer row
is `[1:5]` at both primes. The explicit comparison map is the unique
`F_7`-linear transport taking the displayed generator at `29023` to the
displayed generator at `1499`; the two checked relations show that it also
takes the image of `Q` to the image of `Q`. Thus it transports `(P,Q)` as
`(1,5)` to `(1,5)`, rather than merely comparing labels in unrelated bases.

Cycle 185 proves

\[
 \operatorname{Gal}(L_0/\mathbf Q)
 = (E[7]\oplus E[7])\rtimes\operatorname{GL}_2(\mathbf F_7),
\]

and Cycle 184 proves that over a nonidentity unipotent the complete affine
conjugacy invariant is exactly the zero row or the ordered projective row.
The explicit transport therefore certifies equality of the full `L_0`
Frobenius conjugacy classes.

## Exact modular-symbol certificate

For `epsilon_q=(-1/q)`, define the fixed-level-433 sums

\[
 U_a(q)=\sum_{u=1}^{q-1}(u/q)
 \left[(aq+29u)/(29q)\right]^{\epsilon_q}_E.
\]

Cycle 188 proves that the exact period factor is `kappa_q=1`. With

```text
(w_2,w_3,w_4,w_5,w_6,w_7,w_8,w_9,w_10,w_11,w_13,w_14)
 = (2,3,4,2,5,3,6,6,4,1,1,5),
```

the shortened exact sum is `sum_a w_a U_a(q)`. The committed rows give

| `q` | exact full integer-log sum | exact shortened sum | residue |
|---:|---:|---:|---:|
| 29023 | not needed by the paired formula | `77/2` | 0 |
| 1499 | `-150` | `365/2` | 4 |

All supplied denominators are 1 or 2 and hence are units modulo 7. The
verifier reconstructs every displayed sum from the committed rows, checks all
28 discrete logarithms for `q=1499`, checks the 12 paired rows and weights for
`q=29023`, and reduces only after exact rational summation.

The arithmetic provenance is pinned by these SHA-256 values:

```text
67bb4bc0fb1b666a9100ad5db5e998d02db82c6e9c11ceb5c640530a3930395c  cycle188_433a1_base_twist_sums.gp
bb3e049dd19bd558c83d92560a168fac2d3cbb68e31b8c51bce00fc26bcfca3a  cycle188_base_twist_sums.tsv
dd212f962025100c412e40c2d70b3020911fedfd4568d0964a7362628f37fcc1  cycle189_base433_symbol_sums.gp
2b4508f39aff3b07a68d781ce04d779549a0167b98a8f57f56ead5c591ad0dbf  cycle189_base433_symbol_sums.csv
```

The two GP producers are the exact modular-symbol provenance layer. The final
Python verifier does not invoke PARI: it locks those producers and outputs by
hash, then separately replays the certificate arithmetic from the outputs. It
is not an independent modular-symbol backend.

## Fail-closed replay

Run from the repository root:

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle190_final_certificate.py
python3 -O millennium-prize/birch-swinnerton-dyer/verify_cycle190_final_certificate.py
```

The verifier uses explicit exception-raising requirements rather than Python
`assert`, so optimization cannot disable a check. It fails on a missing or
changed hashed artifact, malformed or incomplete rows, composite prime, packet
failure, wrong point count, wrong finite-field witness, failed Kummer
transport, nonintegral denominator, wrong rational total, or wrong residue.
