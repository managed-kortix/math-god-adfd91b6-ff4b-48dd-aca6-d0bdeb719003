# Routes

## Active gate: fixed-degree relative Chow production

For the Cycle 151 seed `alpha_0=P_Weil[Gamma]` on
`A_0=E_i^3 x E_i^3`, use `D_0=930187500000000000`.  Since
`deg(Gamma_(u^k))=(1+5^k)^2(1+3*5^k)`, freeze the two polarization degrees to
the exact degrees of the Cycle 169 pair:
`d_+=6072151396206990896` and `d_-=2315779370123038256`.  The product of the
resulting relative Chow spaces is a finite-type ambient pair space over the
nine-dimensional PEL base.  Produce an effective pair `(Y^+,Y^-)` such that

1. `[Y^+]-[Y^-]=D_0 alpha_0` in `CH^3(A_0)`, with an explicit rational
   equivalence;
2. its relative Chow germ maps onto all nine PEL tangent directions; and
3. a rank-nine first-order lift extends through second order.

The rational-equivalence condition is not itself known to be finite type at
fixed endpoint degrees.  It is the countable union of finite-type incidences
`R_(e,n,h)` parametrizing an auxiliary effective cycle and a chain of rational
curves in the degree-`d_++d_-+e` Chow scheme.  Thus a positive certificate must
give one explicit incidence witness.  A negative certificate must either give
explicit uniform bounds on `(e,n,h)`, reducing to a finite union, or obstruct
every incidence stratum uniformly; connected components detect only algebraic
equivalence and do not suffice.  The transformed-graph pair has rank zero, and
no single effective cycle can represent the signed class, so a positive
certificate must introduce genuinely new support.  This is a production gate,
not the Hodge conjecture.

The Cycle 196 divisor-cube decomposition does not supply that support. Cycle
197's Appell--Humbert calculation shows that the only integral divisor classes
remaining `(1,1)` over the full PEL germ are multiples of the polarization
`P`. Full-base triple intersections therefore span only `P^3`, which has zero
exceptional Weil projection. The particular graph-divisor triples have common
base dimensions `3,0,0,0,0,0,0`. Thus smooth effective replacements in the
same line bundles cannot yield the required rank-nine pair; the active search
must leave the fixed-line-bundle complete-intersection architecture.
