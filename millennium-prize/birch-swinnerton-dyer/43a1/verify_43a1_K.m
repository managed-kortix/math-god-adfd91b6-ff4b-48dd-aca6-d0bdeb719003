// Exact K=Q(sqrt(-7)) rank, torsion, and Mordell--Weil index certificate.
// Run with Magma V2.29-1 or later: magma verify_43a1_K.m

Q := Rationals();
E := EllipticCurve([Q | 0, 1, 1, 0, 0]);
P := E![0, 0, 1];

R<t> := PolynomialRing(Q);
K<a> := NumberField(t^2 - t + 2);
EK := BaseChange(E, K);
PK := EK![0, 0, 1];

// Magma's twist convention is pinned by the resulting minimal model.
Et := MinimalModel(QuadraticTwist(E, -7));
assert aInvariants(Et) eq [Q | 0, -1, 1, -16, -106];
assert Conductor(Et) eq 2107;

// These are full 2-descents, not analytic-rank computations.
S, stoA, Sbad, AtoS, localmaps := TwoSelmerGroup(E);
St, SttoA, Stbad, AttoSt, localmapst := TwoSelmerGroup(Et);
assert #S eq 2;
assert #St eq 1;
assert AtoS(P) ne Identity(S);
lo, hi := RankBounds(E);
lot, hit := RankBounds(Et);
assert lo eq 1 and hi eq 1;
assert lot eq 0 and hit eq 0;

// For a quadratic extension, the rational and anti-rational eigenspaces give
// rank E(K) = rank E(Q) + rank E^(-7)(Q).
assert Rank(E) + Rank(Et) eq 1;

// Full Mordell--Weil computations include saturation of the returned basis.
GQ, phiQ := MordellWeilGroup(E);
GK, phiK := MordellWeilGroup(EK);
assert #TorsionSubgroup(E) eq 1;
assert #TorsionSubgroup(EK) eq 1;
assert Invariants(GQ) eq [0];
assert Invariants(GK) eq [0];

qgen := phiQ(GQ.1);
kgen := phiK(GK.1);
assert qgen eq P or qgen eq -P;
assert kgen eq PK or kgen eq -PK;

print "BASE_MODEL", aInvariants(E);
print "TWIST_MODEL", aInvariants(Et);
print "TWIST_CONDUCTOR", Conductor(Et);
print "BASE_TWO_SELMER_GROUP", S;
print "TWIST_TWO_SELMER_GROUP", St;
print "BASE_RANK_BOUNDS", lo, hi;
print "TWIST_RANK_BOUNDS", lot, hit;
print "K_RANK", Rank(E) + Rank(Et);
print "K_TORSION", TorsionSubgroup(EK);
print "BASE_MORDELL_WEIL_GROUP", GQ;
print "K_MORDELL_WEIL_GROUP", GK;
print "BASE_GENERATOR", qgen;
print "K_GENERATOR", kgen;
print "K_GENERATOR_IS_PLUS_OR_MINUS_P", true;
print "E_K_FREE_EQUALS_Z_P", true;
