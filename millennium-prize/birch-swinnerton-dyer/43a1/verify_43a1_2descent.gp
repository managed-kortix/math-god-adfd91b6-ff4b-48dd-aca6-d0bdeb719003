\\ Independent exact replay with PARI/GP 2.15.4 or later.
\\ ell2cover is documented to return a basis of all everywhere locally
\\ soluble 2-covers.  This script also verifies its explicit quartic and map.

E = ellinit([0,1,1,0,0]);
P = [0,0];
R_expected = x^4 - 2*x^2 + 4*x + 1;
C = ell2cover(E);

if(#C != 1, error("2-Selmer basis does not have size one"));
R = C[1][1]; M = C[1][2];
if(R != R_expected, error("unexpected explicit quartic"));
if(!ellisoncurve(E, Mod(M, y^2-R)), error("cover map does not land on E"));
if(subst(R,x,0) != 1, error("missing rational point (0,1) on cover"));

H = [0,1];
image = substvec(M,[x,y],H);
if(!ellisoncurve(E,image), error("rational cover point has invalid image"));
diff = ellsub(E,image,P);
if(!ellisdivisible(E,diff,2), error("cover image is not in the Kummer class of P"));

f2 = elldivpol(E,2);
if(#factor(f2)[,1] != 1 || poldegree(f2) != 3, error("nontrivial rational 2-torsion"));

print("MODEL=[0,1,1,0,0]");
print("TWO_DIVISION_POLYNOMIAL=",f2);
print("TWO_TORSION_DIMENSION=0");
print("TWO_COVER_BASIS_SIZE=",#C);
print("TWO_COVER_QUARTIC=",R);
print("COVER_RATIONAL_POINT=",H);
print("COVER_POINT_IMAGE=",image);
print("COVER_POINT_IMAGE_MINUS_P_IS_2_DIVISIBLE=1");
print("TWO_SELMER_DIMENSION=1");
print("KUMMER_IMAGE_GENERATED_BY=P_MOD_2E");
print("SHA_TWO_DIMENSION=0");
print("ALL_EXACT_2DESCENT_ASSERTIONS_PASSED=1");
