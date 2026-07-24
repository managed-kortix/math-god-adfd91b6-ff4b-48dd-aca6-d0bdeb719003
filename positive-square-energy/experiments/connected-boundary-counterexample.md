# Connectedizing the disconnected boundary construction

## 1. Exact disconnected candidate

Let `D` be the nine-vertex graph with graph6 string

```
HQzV]zn
```

and let `e={2,3}` (zero-based graph6 labeling).  Put

```
S(A) = tr((A_+)^2) = s^+(A).
```

Exact characteristic-polynomial/root isolation can certify the following
strict inequalities; the decimals are only discovery data:

```
S(D)       = 36.665892147475496...
S(D+e)     = 36.635149762774869...
drop       =  0.030742384700627...
4(D_+)_23  = -0.74482418200506...
```

For an odd cycle,

```
S(C_r)-r = 1-sec(pi/r)                         (r = 1 mod 4).
```

Consequently the disconnected graph

```
X = D disjoint-union 117 C_5 disjoint-union C_13
```

has 607 vertices and

```
S(X)-607
 = S(D)-9 - 117(sqrt(5)-2) - (sec(pi/13)-1)
 = 0.0160109490504... > 0,
```

whereas adding `e` gives

```
S(X+e)-607 = -0.0147314356502... < 0.
```

Thus this is a strict disconnected threshold crossing.  Its margins are about
`1.47e-2`, so any connectedization must perturb each of the two square
energies by less than that amount (or control their difference more sharply).

The infinitesimal version has much more room.  At `A(D)+tA(e)`,

```
dS/dt at t=0 = 4(D_+)_{23} = -0.744824182005... < 0.
```

Adding untouched components does not alter this derivative.  One may tune a
continuous weighted deficit component to put the direct sum exactly on
`S=n`; the resulting disconnected weighted boundary point has a strictly
negative inward derivative.

## 2. What continuity does prove

Let the components of a finite direct sum `A_0` be joined along any tree, and
give every joining edge weight `epsilon>0`.  Write

```
A_epsilon = A_0 + epsilon B.
```

The support graph of `A_epsilon` is connected.  The map

```
A -> S(A) = sum_i max(lambda_i(A),0)^2
```

is continuous (indeed locally Lipschitz in Frobenius norm), as is the same map
after adding the fixed edge `e`.  The strict margins above therefore imply:

> For all sufficiently small positive `epsilon`, `A_epsilon` is a connected
> weighted adjacency matrix with `S(A_epsilon)>n` but
> `S(A_epsilon+A(e))<n`.

Likewise, after tuning the disconnected weighted construction to `S=n`, the
negative derivative persists for sufficiently small `epsilon`.  This gives a
rigorous asymptotic connected *weighted* counterexample without needing an
explicit numerical epsilon.  Weyl plus the scalar Lipschitz estimate
`|x_+^2-y_+^2| <= (|x|+|y|)|x-y|` gives an explicit epsilon if required.

This does not produce a connected simple unweighted graph: replacing a small
weighted bridge by a long unweighted path is not a norm-small perturbation.

## 3. Why long paths do not implement weak bridges

The tempting assertion that a length-`L` path decouples its endpoint blocks as
`L -> infinity` is false at the level needed here.  For spectral parameters
inside `[-2,2]`, the path Green function is oscillatory and does not decay.
Only eigenvalues outside that band see exponentially weak endpoint transfer.
The dense component `D` has a relevant positive eigenvalue
`1.79493236...` inside the path band.  Hence norm-resolvent convergence to the
disjoint union is unavailable, and ordinary continuity cannot justify the
replacement.

There is also a scale obstruction.  The disconnected construction uses 118
deficit cycles.  Making 119 components connected needs at least 118 bridges.
Each bridge/path junction has an order-one spectral shift, while the entire
threshold-crossing margin is only `0.0147...`.  Numerics confirm that the
junction corrections repair rather than preserve the cycle deficits.

Two natural connectedizations were tested:

1. Attach all `C_5` blocks by internally disjoint paths to one vertex of `D`.
2. Arrange the `C_5` blocks in a chain, separated by paths of lengths through
   32.

Both acquire positive surplus linear in the number of cycles.  In the chain,
the asymptotic surplus increment is about `0.85` per `C_5` block, rather than
the disconnected increment `2-sqrt(5)=-0.236...`.  Increasing path length does
not remove this repair.  No threshold crossing results.

## 4. Exact derivative violation already available

If the target claim is unrestricted edge monotonicity or positivity of the
boundary derivative (rather than threshold preservation at `S=n`), `D` itself
is already a connected exact candidate.  Its spectrum has only two positive
eigenvalues, and its characteristic polynomial factors as

```
x^2 (x+1) (x+2)^3 (x^3-7x^2+6x+6).
```

The spectral projector formula modulo the cubic gives an algebraic expression
for `(D_+)_{23}`.  Isolating the three cubic roots and evaluating the resulting
algebraic sum with rational interval arithmetic proves

```
4(D_+)_{23}<0.
```

Direct comparison of the characteristic polynomials before and after adding
`e` proves the stronger finite statement `S(D+e)<S(D)`.  The exhaustive
nine-vertex scan found only five connected graph/nonedge pairs with a decrease;
this pair has the largest observed decrease, `0.0307423847...`.

## 5. Conclusion

The small-weight bridge route rigorously converts the construction to a
connected weighted counterexample.  The proposed long-unweighted-path route
does not follow from continuity and appears quantitatively hostile.  The exact
nine-vertex graph `D` settles a connected boundary-derivative violation unless
the claim requires the point itself to satisfy `S(D)=|V(D)|`.  Reaching that
unweighted boundary, or an actual simple-graph threshold crossing, still needs
a gadget whose junction spectral shift is below the cycle deficit; paths and
bridges tested here have the opposite sign.
