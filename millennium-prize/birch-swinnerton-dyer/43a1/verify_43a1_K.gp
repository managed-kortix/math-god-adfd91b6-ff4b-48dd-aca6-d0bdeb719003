\\ Exact PARI replay for the K=Q(sqrt(-7)) rank and torsion inputs.
E = ellinit([0,1,1,0,0]);
P = [0,0];
T = ellminimalmodel(elltwist(E,-7));

if([T.a1,T.a2,T.a3,T.a4,T.a6] != [0,-1,1,-16,-106], error("wrong twist model"));
if(T.disc != -43*7^6, error("wrong twist discriminant"));
if(ellglobalred(T)[1] != 43*7^2, error("wrong twist conductor"));

basecovers = ell2cover(E);
twistcovers = ell2cover(T);
if(#basecovers != 1, error("base 2-Selmer basis size is not one"));
if(#twistcovers != 0, error("twist 2-Selmer group is nontrivial"));
if(ellrank(T,4) != [0,0,0,[]], error("twist full descent did not prove rank zero"));

if(kronecker(-7,2) != 1 || ellcard(E,2) != 5, error("split-prime torsion check failed"));
if(kronecker(-7,3) != -1, error("3 is not inert"));
a3 = ellap(E,3);
card9 = (3+1)^2-a3^2;
if(card9 != 12 || gcd(ellcard(E,2),card9) != 1, error("odd-torsion reduction check failed"));
f2 = elldivpol(E,2);
if(#factor(f2)[,1] != 1 || poldegree(f2) != 3, error("rational 2-division cubic is reducible"));

print("BASE_MODEL=[0,1,1,0,0]");
print("TWIST_MODEL=",[T.a1,T.a2,T.a3,T.a4,T.a6]);
print("TWIST_DISCRIMINANT=",T.disc);
print("TWIST_CONDUCTOR=",ellglobalred(T)[1]);
print("BASE_TWO_COVER_BASIS_SIZE=",#basecovers);
print("TWIST_TWO_COVER_BASIS_SIZE=",#twistcovers);
print("TWIST_RANK_DESCENT=",ellrank(T,4));
print("SPLIT_PRIME_2_CARDINALITY=",ellcard(E,2));
print("INERT_PRIME_3_TRACE=",a3);
print("INERT_PRIME_3_CARDINALITY_OVER_F9=",card9);
print("ODD_TORSION_ELIMINATED_BY_REDUCTIONS=",gcd(ellcard(E,2),card9));
print("TWO_PRIMARY_TORSION_ELIMINATED_BY_IRREDUCIBLE_CUBIC=1");
print("K_RANK_EQUALS_BASE_RANK_PLUS_TWIST_RANK=1");
print("ALL_EXACT_K_RANK_TORSION_ASSERTIONS_PASSED=1");
