# Root-congruence witness for a weighted theta

This note records a new exact witness for the one-root weighted-theta problem.
It is a proved matrix lemma and a computationally strong route, not yet a
uniform proof for all rooted thetas.

Let `A` be the adjacency matrix of a loopless graph, let `P=A_+`, fix a root
vector `e`, and put

`S=tr(P^2)`, `a=e^T P e`, `q=e^T P^2 e`, `E=ee^T`.

For `0<=k<=1`, set `C_k=I-(1-k)E` and `X_k=C_k P C_k`.  Congruence gives
`X_k>=0`.  For `B=A-E/2`, exact trace expansion using `AP=P^2` and
`e^T A e=0` gives

`tr(B X_k)=S-2(1-k)q-k^2 a/2`,

`tr(X_k^2)=S+2(k^2-1)q+(k^2-1)^2 a^2`.

The variational formula therefore gives the direct bound

`s^+(B) >= S-2(1-k)^2 q-k^2 a-(1-k^2)^2 a^2`.                 (1)

If `tr(BX_k)>0`, optimal scalar rescaling gives the stronger ratio

`s^+(B) >= (S-2(1-k)q-k^2 a/2)^2`

`                 / (S+2(k^2-1)q+(k^2-1)^2 a^2)`.             (2)

These formulas have been independently rederived twice and are checked
symbolically by `root_congruence_certificate.py`.

## A fixed rational parameter

At `k=6/7`, (1) proves the desired order bound whenever

`S-n >= 2q/49 + 36a/49 + 169a^2/2401`.                        (3)

Unlike the earlier scaled-full-positive-part baseline, this witness passes
all three of its branch-rooted exceptions.  Floating discovery scans found no
failure among all 225,185 rooted theta instances with path lengths at most 30,
nor among a deliberately nonuniform scan of 828,894 rooted vertices with path
lengths as large as 1021.  The unique observed minimum of the direct witness
margin is branch-rooted `Theta(2,3,3)`, approximately `0.0013140591`.
These scans are evidence only.

The cleaner rational `k=43/50` raises that observed minimum to approximately
`0.0013676523`; the rootwise optimum is approximately `0.8603224464`.  The
small improvement does not justify complicating the first uniform proof
attempt, so (3) remains the main target.

## Rootwise optimization

The loss in (1) is

`L_k=2q(1-k)^2+a^2(1-k^2)^2+ak^2`.

Its stationary points satisfy the exact cubic

`2a^2 k^3 + (2q+a-2a^2)k - 2q = 0`.                            (4)

Thus an adaptive witness can replace (3) by the weaker condition
`S-n >= min_{0<=k<=1} L_k`.  A fixed parameter is preferable only if it makes
the theta-specific spectral estimates substantially simpler.

## What remains

The missing theorem is a uniform theta-specific relation between the bare
surplus `S-n` and the rooted moments `a,q`.  Generic bounds
`a^2<=q`, `a<=sqrt(deg(v))/2`, and `q<=deg(v)` are too coarse near the finite
bottleneck.  A useful exact identity is

`S-n = 1 + sum_v (q_v-deg(v)/2)`,

because `2q_v-deg(v)=(A|A|)_{vv}`.  It shows that the obstruction is a
global/local signed-square correlation.

A pure pointwise polynomial minorant for the global `x_+^2` trace cannot by
itself stabilize on arbitrarily long paths: if its infinite-path mean were
exactly one, it would have to equal `x_+^2` throughout `[-2,2]`.  The viable
route is therefore hybrid: exact short cases, polynomial/walk bounds for the
local moments, and a Chebyshev/phase bound for the global theta defect.

For bipartite thetas the weighted endpoint is already immediate from
`S=n+1` and `a<=sqrt(3)/2`, even using the unmodified witness `P`.  Only
nonbipartite rooted thetas remain.
