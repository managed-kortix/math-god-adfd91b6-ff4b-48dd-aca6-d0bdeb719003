# Tick 22: human compression of the `rho=3`, two-T-hole branch

This note records a proved subcase and the exact remaining human obstruction.
The complete row is already eliminated by the checked aggregate certificates.

Let `K` be the B vertices dominating both C vertices. Since all B--C pairs are
present and eleven point from B to C, either the B-to-C profile is `(4,3,0)` or
`(5,1,1)` (numbers dominating two, one, or zero C vertices). Thus `|K|` is four
or five.

Assume first that neither T-hole meets the unique degree-nine vertex `r`. The
two-hole accessibility templates compress all low-A predecessors of members of
`K` into at most three vertices `P={a*,a1,a2}`. For `b in K`, write `p_b` for
its number of low-A predecessors, `h_b` for T-holes from `b` to low A, and
`q_b=1[b->r]`. Exact degree eight gives

```
d_B+(b)=p_b+h_b-2-q_b <= 1+h_b.                 (1)
```

If `x=|K|`, summing (1) and counting arcs internal to K yields

```
C(x,2)-H_K <= x+H_KA,                            (2)
```

where `H_K` counts holes inside K and `H_KA` holes from K to low A. For `x=5`,
(2) is impossible with only two holes. For `x=4`, equality is forced: both
holes meet K, every `p_b=3`, every `q_b=0`, and no member of K points to
`B\K`.

A hole cannot lie inside K: its endpoint designated inaccessible in the
template would simultaneously be an outneighbor of each of the three
predecessors. Hence both holes join K to low A. Write one as `y_i z_i`, with
`z_i in K` and `y_i in A'`. The endpoint identity forces `y_i` to precede all
members of `K\{z_i}`, so `y_i in P`; but `y_i z_i` is missing, contradicting
the already forced `p_{z_i}=3`. Therefore the branch in which neither hole
meets `r` is impossible.

If a hole meets `r`, the same degree count would finish once one proves that
the union of low-A predecessor classes still has size at most three. The open
human synchronization issue is that the other hole can support opposite
endpoints for different predecessors. No such unproved bound is used in the
computational row elimination.

## Rejected shortcut

An attempted global injection of inaccessible incidences into hole endpoints
is invalid with two holes: the same target and endpoint mark can support two
different closed outneighborhoods by using the second hole to absorb their
difference. Therefore no aggregate `15`-incidence bound is claimed here.
