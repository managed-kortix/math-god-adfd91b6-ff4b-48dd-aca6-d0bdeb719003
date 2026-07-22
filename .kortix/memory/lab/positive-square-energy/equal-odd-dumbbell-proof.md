# Equal odd-cycle dumbbells

Let `D_n` be formed from two disjoint copies of `C_n` by adding one edge
between distinguished vertices. For every odd `n>=3`,

`s^+(D_n)>2n`.

## Cycle calculation

Put `a=pi/(2n)`. A finite cosine-square sum gives

`s^+(C_n)-n = 1-sec(pi/n)` if `n=1 (mod 4)`,

`s^+(C_n)-n = sec(pi/n)-1` if `n=3 (mod 4)`.

Indeed the positive eigenvalues are `2cos(2pi j/n)` over `|j|<n/4`.
Substitute `cos^2(u)=(1+cos(2u))/2` and use the Dirichlet-kernel identity

`1+2 sum_{j=1}^r cos(jx)=sin((r+1/2)x)/sin(x/2)`.

For `r=(n-1)/4` or `(n-3)/4`, elementary angle identities reduce the result
to the two displayed formulas.

For `n=3 (mod 4)`, the two cycles are vertex-disjoint induced subgraphs of
`D_n`. Superadditivity therefore yields

`s^+(D_n) >= 2s^+(C_n) = 2n+2(sec(pi/n)-1)>2n`.

## The congruence class n=1 (mod 4)

Apply the gluing lemma of arXiv:2506.07264v1 with base graph `K_2`, gluing a
rooted `C_n` onto each endpoint. Since `C_n` is vertex-transitive, every
diagonal entry of its negative spectral part is

`d=tr(A^-(C_n))/n`.

The correction matrix in the gluing lemma is

`Gamma=[[-d,1],[1,-d]]`,

whose positive square energy is `(1-d)^2` whenever `d<1`. For
`n=1 (mod 4)`, the cycle formula and `s^++s^-=2n` give

The useful estimate comes from the trace norm. For every odd n, the exact
odd-cycle energy formula is

`E(C_n)=2 csc(pi/(2n))`.

This is the corresponding Dirichlet-kernel sum of
`sum_j |2cos(2pi j/n)|` for odd n.

Hence `d=E(C_n)/(2n)=csc(pi/(2n))/n`. Put `t=pi/(2n)`. Since
`sin(t)>t-t^3/6`, the inequality `d<2/3` follows from

`pi(1-pi^2/(24n^2))>3`.

Using `pi>333/106`, `pi<22/7`, and n>=13 verifies this by an exact rational
comparison. Therefore `(1-d)^2>1/9`.

Also `cos x>=1-x^2/2` and `pi<22/7` show, for n>=13,

`2(sec(pi/n)-1)<1/9`.

The gluing lemma gives

`s^+(D_n)>=2[n+1-sec(pi/n)]+(1-d)^2>2n`.

The only remaining n=1 mod 4 cases, n=5 and n=9, pass the standalone exact
SymPy certificate and independent PARI verification in
`dumbbell_all_odd_certificate.py` and `dumbbell-all-odd-pari.txt`.
