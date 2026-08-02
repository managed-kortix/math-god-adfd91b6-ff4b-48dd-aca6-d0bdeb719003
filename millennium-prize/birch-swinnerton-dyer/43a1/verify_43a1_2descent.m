// Exact full 2-descent certificate for E: y^2+y=x^3+x^2.
// Run with Magma V2.29-1 or later:
//   magma verify_43a1_2descent.m

Q := Rationals();
E := EllipticCurve([Q | 0, 1, 1, 0, 0]);
P := E![0, 0, 1];

assert Discriminant(E) eq -43;
T, TtoE := TwoTorsionSubgroup(E);
assert #T eq 1;

// This is Magma's non-isogeny descent in the cubic etale algebra defined by
// the 2-division polynomial.  The returned group is the full 2-Selmer group,
// not merely a rank bound or a point-search result.
S, stoA, Sbad, AtoS, localmaps := TwoSelmerGroup(E);
assert #S eq 2;
assert Ngens(S) eq 1;

// AtoS is the global Kummer/descent map E(Q) -> Sel_2(E/Q).  Thus P maps
// to the unique nonzero Selmer class and already spans the complete group.
kP := AtoS(P);
assert kP ne Identity(S);
assert AtoS(2*P) eq Identity(S);
assert sub<S | kP> eq S;

// Independently request explicit everywhere locally soluble 2-covers.  For
// rank one and Sha[2]=0 there is one nontrivial cover up to F_2-basis.
covers, covermaps, Emap := TwoDescent(E);
assert #covers eq 1;

print "MODEL", aInvariants(E);
print "TWO_DIVISION_POLYNOMIAL", DivisionPolynomial(E, 2);
print "TWO_TORSION_ORDER", #T;
print "TWO_SELMER_GROUP", S;
print "TWO_SELMER_ORDER", #S;
print "TWO_SELMER_DIMENSION", 1;
print "DESCENT_BAD_PRIMES", Sbad;
print "SELMER_GENERATOR_ETALE_CLASS", stoA(S.1);
print "KUMMER_P", kP;
print "KUMMER_2P", AtoS(2*P);
print "TWO_COVER_BASIS_SIZE", #covers;
print "TWO_COVER_BASIS", covers;
print "LOCAL_MAP_COUNT", #localmaps;
print "SHA_TWO_ORDER", (#S * #T) div 2;
print "ALL_EXACT_2DESCENT_ASSERTIONS_PASSED", true;
