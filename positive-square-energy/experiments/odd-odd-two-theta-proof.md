# Odd--odd--two theta graphs

## Theorem

For all odd positive integers `a,b`, the simple theta graph
`G=Theta(a,b,2)` satisfies

`s^+(G)>|V(G)|`.

Equivalently, if a new vertex is joined to two vertices in different
bipartition classes of an even cycle, the positive square energy increases by
strictly more than one.

## Variational lemma

For every real symmetric matrix `M`,

`s^+(M)=max_{X>=0} (2 tr(MX)-tr(X^2))`.

This follows by diagonalizing `M`; the scalar maximum of `2 lambda x-x^2`
over `x>=0` is `(lambda_+)^2`.

Let `A` be the adjacency matrix of an even cycle `C_N`, let `u,v` lie in
different bipartition classes, and put `b=e_u+e_v`.  The enlarged adjacency
matrix is

`M=[[A,b],[b^T,0]]`.

Write `P=A_+`, `p=b^TPb`, and `q=b^TP^2b`.  Use the positive-semidefinite
witness

`X=[[P,Pb/2],[b^TP/2,p/4]]`.

It is PSD by its Gram factorization through the rectangular matrix with rows
`P^(1/2)` and `b^TP^(1/2)/2`.  Since `AP=P^2`, direct multiplication gives

`2tr(MX)-tr(X^2)=s^+(C_N)+2p-q/2-p^2/16`.

The cycle spectrum lies in `[-2,2]`, so `0<=P<=2I` and `P^2<=2P`.  Thus
`q<=2p`, and

`s^+(G)>=s^+(C_N)+p-p^2/16`.                         (1)

## Uniform lower bound on p

Because the cycle is bipartite,

`P=(|A|+A)/2`.

The matrix `|A|=(A^2)^(1/2)` preserves the two bipartition classes.  Hence
`|A|_{uv}=0`.  Vertex transitivity gives

`p=r_N+1_{u~v}`,

where `r_N=tr|A|/N` is the mean absolute adjacency eigenvalue.

For `N>=6`, the second and fourth spectral moments are exactly

`E(lambda^2)=2`, `E(lambda^4)=6`.

The fourth identity counts the six closed four-step walks at a cycle vertex.
Holder's inequality gives

`E(lambda^2)<=E(|lambda|)^(2/3) E(lambda^4)^(1/3)`,

so

`r_N>=2/sqrt(3)`.

Also Cauchy--Schwarz gives `r_N<=sqrt(2)`, hence
`p<=1+sqrt(2)<3`.  The function `f(x)=x-x^2/16` is increasing on `[0,3]`,
and therefore

`p-p^2/16 >= 2/sqrt(3)-1/12 >1`.

The final strict inequality is equivalent, after positive squaring, to
`192>169`.

For `N=4`, every opposite-class pair is adjacent.  The cycle spectrum is
`{2,0,0,-2}`, so `r_4=1`, `p=2`, and
`p-p^2/16=7/4>1`.

Finally `s^+(C_N)=N` by bipartite spectral symmetry.  Equation (1) now yields

`s^+(G)>N+1=|V(G)|`.

Taking the two cycle arcs between `u,v` to have the odd lengths `a,b` gives
exactly `Theta(a,b,2)`.

## Audits

Three independent derivations reproduced the PSD witness and all constants.
Exact screening through `C_60` found no counterexample; this is only an audit,
not part of the proof.  The smallest observed actual gain was
`1.7108314535...` for antipodal attachment to `C_6`.  The phrase “different
bipartition classes” is essential; it does not mean geometrically antipodal.
