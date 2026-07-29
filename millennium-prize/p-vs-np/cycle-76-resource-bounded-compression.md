# Cycle 76: resource-bounded compression funnel

Let `N=2^n` and

\[
s(n)=2^{n/\log^*n}=N^{1/\log^*n}.
\]

McKay--Murray--Williams prove that if exact `search-MCSP^A[s]`, for some fixed
`A in PH`, has no deterministic one-pass streaming algorithm with both
`poly(s)` space and `poly(s)` update time, then `P!=NP`. For `A=SAT`, it
suffices to exclude simultaneous `N^epsilon` space and update time for one
fixed `epsilon>0`. This is a full-reach implication, not a lower bound.

For any prefix/suffix split let

\[
R_x=\{y:xy\text{ has a size-}s\text{ SAT-oracle circuit}\}.
\]

There are at most `|L_s|+1` distinct residuals: all empty residuals coincide,
and selecting one yes completion from each nonempty residual injects them into
the yes set. Since

\[
|L_s|\le2^{O(s\log(n+s))},
\]

ordinary continuation signatures and one-way fooling sets have ceiling
`O(s log(n+s))=N^o(1)`. Complementary no-residuals and multiple search
witnesses do not evade this semantic count.

Previously emitted output must also be charged: with `w` state bits and `L`
output bits at the cut, the valid injection bound is `w+L>=log|F|`. Circuit
output itself carries `O(s log(n+s))` bits. Pure fixed-power space lower bounds
are false with unbounded update time, because the short local oracle calls can
be brute-forced in `poly(s)=N^o(1)` space.

The promoted bottleneck is therefore a uniform, update-time-sensitive,
non-localizable lower bound for exact `Stream-Merge`. The prefix history is
already summarized semantically by the current circuit, so a putative extra
many-block consistency game would be false: the process is Markovian. The hard
step is local canonical minimization and universal agreement. For `A=SAT`, MMW
place the required merge predicate at the corresponding higher PH level, not
in ordinary SAT. Any method surviving arbitrary local-oracle replacement
collides with the known locality upper bound. No lower bound or `P!=NP` result
is claimed.
