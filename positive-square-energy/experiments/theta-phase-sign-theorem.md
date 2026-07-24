# Sign theorem for theta signed-square energy

This note proves an exact qualitative theorem for every simple theta graph.
It uses the parity-uniform phase carrier from `theta-imaginary-phase.md`.

For an odd path length `l`, put

`A_l(z)=z^((l-1)/2)/(1+z^l)`;

for an even path length put

`B_l(z)=z^(l/2-1)/(1-z^l)`, for `0<z<1`.

After dividing the phase polynomials `P,Q` by the positive common factor
`F`, their summands are

`P/F=sum_(l odd) (-1)^((l-1)/2) A_l`,

`Q/F=sum_(l even) (-1)^(l/2) B_l`.                              (1)

## Shorter paths dominate

If `a<b` are odd, then

`A_a-A_b = z^((a-1)/2)(1-z^((b-a)/2))(1-z^((a+b)/2))`

`            / ((1+z^a)(1+z^b)) > 0`.                         (2)

If `a<b` are even, then

`B_a-B_b = z^(a/2-1)(1-z^((b-a)/2))(1+z^((a+b)/2))`

`            / ((1-z^a)(1-z^b)) > 0`.                         (3)

The plus sign in the final factor of (3) is essential.  Therefore the sign
of each nonempty parity sum in (1) is the sign of its shortest path's
coefficient.  There is no cancellation: equal lengths have equal signs, and
unequal opposite-sign terms are strictly separated by (2) or (3).

Let `o` be the shortest odd path and `e` the shortest even path.  For a
nonbipartite theta, both exist, and for every `0<z<1`,

`sign(P)=(-1)^((o-1)/2)`, `sign(Q)=(-1)^(e/2)`.                 (4)

Hence

`sign(PQ)=(-1)^((o+e-1)/2)`.                                   (5)

The cycle formed by these two paths is the shortest odd cycle of the theta.

## Spectral consequence

The phase carrier is `H=R+i sqrt(z)S`, with `R>=0` and
`S=2z(1+z)^2PQ`.  Thus its canonical phase `alpha=Arg H` has the strict sign
of `PQ` in every nonbipartite theta.  Since

`tr(A|A|)=-(2/pi) integral_0^1 (z^-2-1)alpha(z) dz`,

the signed-square trace has the opposite sign.  We obtain:

**Theorem.** For a simple theta graph `G`:

1. If `G` is bipartite, `tr(A|A|)=0` and `s^+(G)-|G|=1`.
2. If its shortest odd cycle has length `1 mod 4`, then
   `tr(A|A|)<0` and `s^+(G)-|G|<1`.
3. If its shortest odd cycle has length `3 mod 4`, then
   `tr(A|A|)>0` and `s^+(G)-|G|>1`.

In particular, the bare `4/5` theorem is automatic for every theta except
those whose shortest odd cycle has length `1 mod 4`.  The three known
exceptions all have shortest odd cycle `C5`, as does the first safe
near-extremizer `Theta(2,3,6)`.  Thus the remaining quantitative obstruction
is exactly the negative signed-square class.
