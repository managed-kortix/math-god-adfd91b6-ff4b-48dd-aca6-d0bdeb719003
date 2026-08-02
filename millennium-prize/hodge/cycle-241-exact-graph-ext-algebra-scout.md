# Cycle 241: exact graph-Ext algebra and smallest idempotents

## Scope

Work over `K=Q(i)` on

\[
A_0=E_i^3\times E_i^3,\qquad
F_k=O_{\Gamma_{u^k}},\quad u=2+i,\quad 0\leq k\leq6.
\]

This scout supplies an exact compressed binary Yoneda algebra for bounded
twisted-complex calculations and classifies the first noncentral idempotents.
It does not classify arbitrary projectors in the Karoubi envelope and therefore
does not decide `KI240`.

## Self algebra

Choose degree-one generators `a_1,...,a_6` for

\[
H^1(O_{\Gamma_k})\oplus H^0(N_{\Gamma_k/A_0}).
\]

For every vertex the exact graded algebra is

\[
\operatorname {Ext}^*(F_k,F_k)=
\Lambda_K(a_1,\ldots,a_6).
\tag{241.1}
\]

Write `a_I=a_(i_1)...a_(i_p)` for an increasing subset `I`. Then

\[
a_Ia_J=
\begin{cases}
0,&I\cap J\ne\varnothing,\\
(-1)^{\#\{(i,j)\in I\times J:i>j\}}a_{I\cup J},&I\cap J=\varnothing.
\end{cases}
\tag{241.2}
\]

Thus the dimensions in degrees zero through six are

\[
(1,6,15,20,15,6,1).
\]

Put `omega_k=a_1a_2a_3a_4a_5a_6` at vertex `k`.

## Cross algebra

For `i!=j`, let

\[
Z_{ij}=\Gamma_i\cap\Gamma_j=\ker(u^j-u^i:E_i^3\to E_i^3),
\qquad L_{ij}=\dim_K H^0(O_{Z_{ij}})=N(u^j-u^i)^3.
\]

Transversality gives

\[
\operatorname {Ext}^r(F_i,F_j)=
\begin{cases}
H^0(O_{Z_{ij}}),&r=3,\\
0,&r\ne3.
\end{cases}
\tag{241.3}
\]

Choose dual bases `x_(ij,s)`, `x_(ji,s)`, `0<=s<L_ij`, for the perfect
Serre pairings. The complete nonunit binary structure constants can be
normalized to

\[
x_{ji,t}x_{ij,s}=\delta_{st}\omega_i,
\qquad
x_{ij,s}x_{ji,t}=-\delta_{st}\omega_j.
\tag{241.4}
\]

The sign is graded cyclicity for two degree-three classes. Every product of two
cross classes with distinct outer vertices is zero because it would lie in a
cross `Ext^6`, and every product involving a positive-degree self class and a
cross class is zero because it would lie in cross degree greater than three.
Vertex units have the evident source/target action. Equations (241.1)--(241.4)
therefore give all binary structure constants without expanding billions of
intersection coordinates.

The 21 unordered-pair dimensions are:

| pair | `L_ij` | pair | `L_ij` | pair | `L_ij` |
|---|---:|---|---:|---|---:|
| 01 | 8 | 02 | 8000 | 03 | 1815848 |
| 04 | 262144000 | 05 | 32829478408 | 06 | 3989418056000 |
| 12 | 1000 | 13 | 1000000 | 14 | 226981000 |
| 15 | 32768000000 | 16 | 4103684801000 | 23 | 125000 |
| 24 | 125000000 | 25 | 28372625000 | 26 | 4096000000000 |
| 34 | 15625000 | 35 | 15625000000 | 36 | 3546578125000 |
| 45 | 1953125000 | 46 | 1953125000000 | 56 | 244140625000 |

For shifts, the convention is

\[
\operatorname {Hom}^d(F_i[r],F_j[s])
=\operatorname {Ext}^{d-r+s}(F_i,F_j).
\tag{241.5}
\]

Hence a cross basis element has shifted degree `d=3+r-s`. Equations
(241.2), (241.4), and (241.5) directly assemble sparse chain-map composition;
the Hom differential is

\[
\partial(f)=d_Cf-(-1)^{|f|}fd_C.
\tag{241.6}
\]

Together these formulas are sufficient to print the degree-one Hom matrix and
the nine corner-obstruction matrices of any specified finite packet once its
differential and diagonal obstruction coordinates are supplied.

## Smallest noncentral idempotents

A one-summand object `F_i[r]` has endomorphism algebra `K`, so it has only zero
and one. Two summands are minimal.

### Two equal copies

For `F_i[r] direct_sum F_i[r]`, the degree-zero algebra is `M_2(K)`. Every
nontrivial idempotent has rank one and is exactly

\[
e(a,b,c)=\begin{pmatrix}a&b\\c&1-a\end{pmatrix},
\qquad a(1-a)=bc.
\tag{241.7}
\]

All are noncentral. They split off a copy of `F_i[r]` and introduce no new
Karoubi object up to isomorphism.

### Two distinct shifted vertices

For `C=F_i[r] direct_sum F_j[r+3]`, `i!=j`, only one off-diagonal degree-zero
cross space occurs. With an orientation-compatible matrix convention,

\[
\operatorname {End}^0(C)=
T_L=\left\{\begin{pmatrix}a&x\\0&b\end{pmatrix}:
a,b\in K,\ x\in K^{L_{ij}}\right\}.
\tag{241.8}
\]

Solving `e^2=e` exactly gives, besides zero and one,

\[
e_x^+=\begin{pmatrix}1&x\\0&0\end{pmatrix},\qquad
e_x^-=\begin{pmatrix}0&x\\0&1\end{pmatrix},
\qquad x\in K^{L_{ij}}.
\tag{241.9}
\]

These are all noncentral. Conjugation by a unit `1+n`, `n` in the square-zero
radical, sends each to its `x=0` vertex projector. Thus this first cross-vertex
family also yields no new isomorphism class of summand.

The smallest actual one-arrow twisted complex is

\[
F_i[r]\longrightarrow F_j[r+2].
\]

Its degree-zero chain endomorphisms are diagonal scalars; commuting with a
nonzero arrow forces the scalars equal. Its only chain idempotents are zero and
one. Therefore every two-term indecomposable cross-arrow cone is already
Karoubi-rigid at degree zero.

## Exact artifact

The machine-readable artifact stores the exterior bases, multiplication rule,
all exact pair dimensions, normalized cross products, shift convention, and
idempotent families:

`millennium-prize/hodge/cycle241_graph_ext_algebra.json`

Regenerate or verify it with

```sh
python3 millennium-prize/hodge/verify_cycle241_graph_ext_algebra.py
python3 millennium-prize/hodge/verify_cycle241_graph_ext_algebra.py --check
```

The artifact is compressed deliberately: the largest cross space has dimension
`4103684801000`, so literal basis expansion is neither necessary nor feasible.
No Hodge-conjecture result is claimed.
