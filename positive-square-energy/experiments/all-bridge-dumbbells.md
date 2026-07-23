# Every bridge dumbbell satisfies the positive square-energy bound

Let `D_{p,q}` be formed from disjoint cycles `C_p,C_q`, `p,q>=3`, by adding
one bridge between distinguished vertices.  Then

`s^+(D_{p,q})>p+q`.

## Proof by parity

If both lengths are even, the whole graph is bipartite and has `p+q+1`
edges, so `s^+=p+q+1`.

Suppose exactly one length is odd, say `r`, and the even length is `e`.  If
`r>=5`, choose three consecutive nonattachment vertices on `C_r`.  They
induce a `P3`, and deleting any one breaks the odd cycle while leaving a
connected bipartite unicyclic graph with `p+q-1` edges.  The exact improved
P3-removal lemma therefore gives

`s^+(D_{r,e})>=p+q-1+17/16=p+q+1/16`.

If `r=3`, the two original cycles are disjoint induced subgraphs.  Hence

`s^+(D_{3,e})>=s^+(C_3)+s^+(C_e)=4+e=p+q+1`.

It remains to treat two odd cycles.  For odd `n`, put

`delta_n=sec(pi/n)-1`,

so `s^+(C_n)-n` equals `-delta_n` for `n=1 mod 4` and `+delta_n` for
`n=3 mod 4`.  The existing equal-odd theorem settles `p=q`, and the existing
`C5--Cq` theorem settles every pair with a length-five side.  A triangle side
is settled by induced superadditivity: its surplus is one and every odd-cycle
deficit is less than one.

For the remaining unequal odd lengths `p,q>=7`, the gluing lemma has correction
matrix

`[[-d_p,1],[1,-d_q]]`, `d_n=csc(pi/(2n))/n`.

Exact sine bounds give `d_n<2/3` for odd `n>=7`; hence its positive eigenvalue
is greater than `1/3`, and the correction exceeds `1/9`.  Also

`delta_n < 242/(49n^2-242)`.

Thus one negative cycle deficit is always less than `1/9`.  If both cycles
have negative deficit and are unequal (with C5 removed), their lengths are at
least 9 and 13, and

`242/3727+242/8039 < 1/9`.

So the gluing correction strictly dominates all possible deficits.  This
exhausts all cycle-length pairs.

The special equal and C5 ingredients are independently exact-certified in
`equal-odd-dumbbell-proof.md` and `c5-odd-dumbbell-theorem.md`.
