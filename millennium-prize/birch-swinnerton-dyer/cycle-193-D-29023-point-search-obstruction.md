# Cycle 193: the `D=-29023` point-search obstruction after higher descent

## Exact target

The minimal model of the quadratic twist of `433a1` by `D=-29023` is

\[
 E:\quad y^2+xy+y=x^3+x^2-17548636x-24475377572834.
\]

Certified cubic arithmetic and PARI 2-descent give 2-Selmer dimension at most
one and hence `rank E(Q)` in `[0,1]`. No exact point or rigorous analytic
nonvanishing is known, so rank one and `Sha(E)[2]=0` are not claimed. The
reported nontrivial 2-cover is

\[
 C:\quad z^2=-29023x^4-58046x^3-29023x^2-232184x-116092.
\]

This cycle attempted to recover an exact point rather than infer one from
floating-point data.

## Independent 2-cover and lattice searches

PARI/GP 2.15.4 had already returned no point with `ellrank` effort six,
overflowed a 1 GB stack in `ellheegner`, and found no point on `C` through
naive height `10000`.

An independent eclib 20250627 run verified that `C` is everywhere locally
soluble and that its Jacobian is exactly the displayed minimal model.  Its
quartic minimisation is already minimal.  Reduction gives the equivalent
quartic

\[
 z^2=-29023x^4+58046x^3-29023x^2-232184x+116092.
\]

The Stoll--Cremona two-stage quartic sieve found no rational point on either
the original or reduced model through projective naive height `3000`; the
reduced model was also searched through height `10000` with no point.

This is a bounded search result, not a proof that `C(Q)` is empty. The current
certificates do not decide whether this Selmer class comes from `E(Q)` or from
`Sha(E)[2]`.

## Magma higher descent

Magma V2.29-8 independently returned the equivalent two-cover

\[
 z^2=-29023x^4+58046x^3-29023x^2+232184x-116092.
\]

`FourDescent` produced one everywhere locally soluble 4-cover.  In
coordinates `[u1:u2:u3:u4]` it is the intersection

\[
\begin{aligned}
0={}&4u_1^2+8u_1u_2+3u_1u_3+10u_1u_4-4u_2^2+3u_2u_4
      -5u_3^2+7u_3u_4-7u_4^2,\\
0={}&u_1^2+8u_1u_2+23u_1u_3-4u_1u_4+4u_2^2+3u_2u_3
      +10u_2u_4+10u_3^2-8u_3u_4+24u_4^2.
\end{aligned}
\]

The Elkies quadric-intersection search found no point through naive height
`10^8`.

`EightDescent` completed in about seven seconds.  It found a fake Selmer set
of cardinality one and returned two reduced degree-eight genus-one covers in
`P^7`.  Generic lattice searches on both covers found no point through
height `3*10^13`; several additional seeded searches through height `10^10`
also returned no point.  A height `10^14` job exceeded the calculator's
60-second limit. The existence of the degree-eight covers shows that the
relevant classes lift through this computed descent stage; it neither rules
out every 2-primary obstruction nor exhibits a rational point.

## Heegner and analytic methods

PARI's `ellheegner` did not complete within the available memory.  Magma's
`HeegnerPoint` likewise exceeded the public calculator's approximately
300 MB memory limit.  The numerical leading-term calculation from Cycle 192
predicts canonical generator height

\[
 2659.7556120373832309983\ldots,
\]

conditional on the rank-one BSD leading-term formula with `|Sha|=1`.  This
explains why direct point coordinates can be enormous, but it is not used as
an exact certificate.

## Honest endpoint

No exact rational coordinates were recovered. There is no local obstruction on
the reported coverings, and both higher descents return locally soluble
coverings. This does not prove that a rational point exists. The exact certified
rank interval is `[0,1]`, and no claim about `Sha(E)[2]` is made. The obstruction
encountered is computational: the searches did not find a rational point, while
both available Heegner implementations exceed their memory limits.

Therefore no coordinates are claimed. The exact certified conclusion is only
that the listed bounded searches failed, not that a rational point exists only
at large height and not that one fails to exist.

## Reproduction snippets

The exact Cycle 192 certificate remains

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/verify_cycle192_pari_2descent.gp
```

The eclib search used `quartic_points` from eclib 20250627, with the quartic
coefficients above and bounds `3000` and `10000`.  The central Magma commands
were

```magma
E := EllipticCurve([1,1,1,-17548636,-24475377572834]);
C := TwoDescent(E)[1];
F := FourDescent(C)[1];
PointsQI(F, 10^8 : OnlyOne := true);
D, maps := EightDescent(F : StopWhenFoundPoint := true);
[ PointSearch(X, 3*10^13 : Dimension := 1) : X in D ];
```
