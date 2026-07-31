# Cycle 168: full prime-Hecke trace and Chow complexity

The full prime-Hecke trace does not repair the degree/denominator tradeoff.
Raw trace is integral and effective but has degree of order `p^12`. Weight
normalization lowers this to order `p^9` but has exact denominator `p^3` on
the fine Hecke correspondence. Averaging gives constant rational degree 16,
but its exact denominator is `p^3 N_p` and its support has `N_p` sheets. Thus
none of these normalizations gives bounded integral Chow complexity.

## Conventions and number of Hecke sheets

Let `p>=5`, let `Gamma` be the Cycle 151 diagonal, and let `K` run through all
PEL-stable maximal isotropic subgroups of `A_0[p]`. Write

\[
 f_K:A_0\longrightarrow B_K=A_0/K,
 \qquad f_K^*M_K=pL,
\]

and let `N_p` be the number of kernels. Cycle 163 gives

\[
 N_p=
 \begin{cases}
 (p+1)(p^3+1)(p^5+1),&p\equiv3\pmod4,\\[2mm]
 \displaystyle\sum_{r=0}^6{6\brack r}_p,&p\equiv1\pmod4.
 \end{cases}
\]

The exact expanded formulas are

\[
 \boxed{N_p^{\rm inert}
 =p^9+p^8+p^6+p^5+p^4+p^3+p+1}
\]

and

\[
 \boxed{N_p^{\rm split}
 =p^9+3p^8+4p^7+7p^6+9p^5+11p^4
   +9p^3+8p^2+5p+7}.
\]

In particular, in both cases

\[
 N_p=p^9(1+O(p^{-1})),
\]

with first correction `p^-1` in the inert case and `3p^-1` in the split
case. These are sheet counts on a fine level cover. Quotienting by
automorphisms or forgetting the Hecke kernel changes the stack-theoretic
degree and must not be mixed with this trace.

## Cycle multiplicities and exact degree

Put

\[
 d_K=\dim_{\mathbf F_p}(K\cap\Gamma[p]),
 \qquad \delta_K=p^{d_K},
 \qquad \eta_K=p^{3-d_K},
\]

and let `Y_K=f_K(Gamma)` with its reduced structure. Then

\[
 (f_K)_*[\Gamma]=\delta_K[Y_K],
 \qquad
 p^{-3}(f_K)_*[\Gamma]=\eta_K^{-1}[Y_K].
\]

Since `L|Gamma` has type `(2,2,4)`, its normalized degree is 16. Therefore

\[
 \deg_{M_K}((f_K)_*[\Gamma])=16p^3,
 \qquad
 \deg_{M_K}(Y_K)=16\eta_K.
\]

On the disjoint target of the finite Hecke correspondence define the raw
trace

\[
 Z_p^{\rm raw}=\sum_K(f_K)_*[\Gamma].
\]

It is an integral effective cycle and has exact total degree

\[
 \boxed{\deg Z_p^{\rm raw}=16p^3N_p.}
\]

Thus

\[
 \deg Z_p^{\rm raw}=
 \begin{cases}
 16(p^{12}+p^{11}+p^9+p^8+p^7+p^6+p^4+p^3),
   &p\equiv3\pmod4,\\
 16(p^{12}+3p^{11}+4p^{10}+7p^9+9p^8+11p^7
  +9p^6+8p^5+5p^4+7p^3),
   &p\equiv1\pmod4.
 \end{cases}
\]

In particular its exact leading asymptotic is `16p^12(1+O(p^-1))`.
For the middle-weight trace and its probabilistic average,

\[
 Z_p^{\rm wt}=p^{-3}Z_p^{\rm raw},
 \qquad
 Z_p^{\rm avg}={1\over N_p}Z_p^{\rm wt},
\]

one has

\[
 \boxed{\deg Z_p^{\rm wt}=16N_p\sim16p^9},
 \qquad
 \boxed{\deg Z_p^{\rm avg}=16}.
\]

The constant degree of the average is only a rational-cycle statement.

## Exceptional cohomological projection

Let

\[
 \alpha=P_{\rm Weil,A_0}[\Gamma]
 =-{i\over8}\Omega_W+{i\over8}\Omega_{\bar W}\ne0
\]

in the normalized complex-form convention of Cycle 151. The PEL-linear
endomorphism `u=2+i` descends through every PEL-stable kernel, so its rational
interpolation projector commutes with isogeny pushforward. Hence, sheet by
sheet,

\[
 \boxed{P_{\rm Weil,B_K}((f_K)_*[\Gamma])=(f_K)_*\alpha},
\]

and

\[
 \boxed{P_{\rm Weil,B_K}(p^{-3}(f_K)_*[\Gamma])
 =p^{-3}(f_K)_*\alpha\ne0.}
\]

The last nonvanishing follows because an isogeny induces an isomorphism on
rational cohomology. Thus the exceptional projection of the full trace on
the disjoint Hecke target is exactly

\[
 \boxed{P_{\rm Weil}(Z_p^{\rm raw})
   =\bigoplus_K(f_K)_*\alpha,}
\]

with the analogous factors `p^-3` and `(N_pp^3)^-1` for weight normalization
and averaging. If every target cohomology is identified with the source by
the middle-weight map `I_K=p^-3(f_K)_*`, then

\[
 P_{\rm Weil}(Z_p^{\rm wt})\leftrightarrow N_p\alpha,
 \qquad
 P_{\rm Weil}(Z_p^{\rm avg})\leftrightarrow\alpha.
\]

This is an identification of the local systems sheet by sheet, not a claim
that cycles on distinct fibers can be added in one fiber. There is no
cohomological cancellation in the full trace before an additional pushdown
or monodromy identification is specified.

## Exact denominator and complexity verdict

Cycle 162 proves that every reduced `[Y_K]` is primitive in integral
cohomology and integral Chow. Consequently the coefficient `eta_K^-1` above
has exact denominator `eta_K`. The full Hecke set contains transverse kernels
with `d_K=0`, hence `eta_K=p^3`. On the direct sum of the fine Hecke sheets
this gives

\[
 \boxed{\operatorname{den}(Z_p^{\rm wt})=p^3},
 \qquad
 \boxed{\operatorname{den}(Z_p^{\rm avg})=N_pp^3}.
\]

The second equality is exact because a transverse primitive sheet has
coefficient `1/(N_pp^3)`. Clearing denominators in the average recovers the
raw trace and therefore degree `16p^3N_p`.

Explicitly, the averaged denominators are

\[
 \operatorname{den}(Z_p^{\rm avg})=
 \begin{cases}
 p^{12}+p^{11}+p^9+p^8+p^7+p^6+p^4+p^3,
   &p\equiv3\pmod4,\\
 p^{12}+3p^{11}+4p^{10}+7p^9+9p^8+11p^7
  +9p^6+8p^5+5p^4+7p^3,
   &p\equiv1\pmod4.
 \end{cases}
\]

These denominator statements are for the labeled fine Hecke cover. After
forgetting the kernel, coincident quotient points can merge branches; an exact
denominator there requires the stabilizer and coincidence multiplicities of
that separate pushdown.

Thus:

1. raw trace has integral coefficients but degree `~16p^12`;
2. weight-normalized trace has degree `~16p^9` and denominator `p^3`;
3. averaged trace has degree 16 but denominator `N_pp^3~p^12` and `N_p~p^9`
   distinguished Hecke sheets;
4. denominator clearing always returns unbounded integral degree.

Therefore normalization does **not** yield bounded integral Chow complexity.
It only yields a bounded-degree rational average after allowing an unbounded
denominator and an unbounded finite correspondence. This remains a no-go for
extracting one bounded integral Chow stratum from the full Hecke trace.

For comparison, restricting at split primes to the completely adapted sheets
gives

\[
 N_p^{\eta=1}=2(p+1)(p^2+1)=2p^3+2p^2+2p+2.
\]

Their weight-normalized cycles are integral reduced cycles, but their sum has
degree `16N_p^{eta=1}~32p^3`; averaging restores degree 16 at exact denominator
`N_p^{eta=1}` on the fine disjoint target. Even the adapted subtrace therefore
does not have bounded integral Chow complexity.

No generic algebraicity or Hodge-conjecture conclusion follows.
