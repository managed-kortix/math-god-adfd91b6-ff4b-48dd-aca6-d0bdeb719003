\\ Exact/arbitrary-precision PARI/GP packet for Cremona 43a1.
default(realprecision, 80);

E = ellinit([0,1,1,0,0]);
P = [0,0];

print("PARI_VERSION=", version());
print("MODEL=", E.a1, ",", E.a2, ",", E.a3, ",", E.a4, ",", E.a6);
print("DISCRIMINANT=", E.disc);
print("J_INVARIANT=", E.j);
G = ellglobalred(E);
print("GLOBAL_REDUCTION=", G);
print("CONDUCTOR=", G[1]);
print("TAMAGAWA_PRODUCT=", G[3]);
print("LOCAL_AT_43=", elllocalred(E,43));

print("P_ON_CURVE=", ellisoncurve(E,P));
print("TORSION=", elltors(E));
print("RANK_DESCENT=", ellrank(E,4,[P]));
Q = [-3/4,1/8];
print("DESCENT_POINT_Q=", Q);
print("FIVE_P=", ellmul(E,P,5));
print("DESCENT_POINT_EQUALS_FIVE_P=", Q == ellmul(E,P,5));
print("P_HEIGHT=", ellheight(E,P));
print("P_DIVISIBLE_BY_2=", ellisdivisible(E,P,2));
print("P_DIVISIBLE_BY_3=", ellisdivisible(E,P,3));
print("P_DIVISIBLE_BY_5=", ellisdivisible(E,P,5));

C = ell2cover(E);
print("TWO_COVER_BASIS_SIZE=", #C);
print("TWO_COVER_BASIS=", C);

print("TWO_DIVISION_POLYNOMIAL=", elldivpol(E,2));
print("TWO_DIVISION_FACTORIZATION=", factor(elldivpol(E,2)));
print("RATIONAL_ISOGENY_CLASS=", ellisomat(E,0,1));
print("FROBENIUS_COLUMNS=[q,a_q,#E(F_q)]");
forprime(q=2,97,if(q != 43,a = ellap(E,q); print([q,a,q+1-a])));

\\ D=-7 has class number one and 43 splits.  The root b=37 gives
\\ tau=(-b+sqrt(D))/(2N), with b^2-D divisible by 4N.
D = -7; b = 37; N = 43;
print("HEEGNER_D=", D);
print("HEEGNER_CONGRUENCE_QUOTIENT=", (b^2-D)/(4*N));
print("KRONECKER_D_OVER_43=", kronecker(D,43));
print("CLASS_NUMBER_D=", qfbclassno(D));
tau = (-b + sqrt(D))/(2*N);
qcm = exp(2*Pi*I*tau);
z = sum(n=1,1200,ellak(E,n)/n*qcm^n);
Z = ellztopoint(E,z);
print("HEEGNER_TAU=", tau);
print("HEEGNER_Q_ABS=", abs(qcm));
print("MODULAR_LOG_PARTIAL_SUM=", z);
print("MODULAR_IMAGE_NUMERICAL=", Z);
H = ellheegner(E);
print("ELLHEEGNER_POINT=", H);
print("ELLHEEGNER_POINT_ON_CURVE=", ellisoncurve(E,H));
print("ELLHEEGNER_EQUALS_P=", H == P);

print("ANALYTIC_RANK_NUMERICAL=", ellanalyticrank(E));
print("BSD_LEADING_TERM_FROM_P=", ellbsd(E)*ellheight(E,P));
print("MODULAR_DEGREE=", ellmoddegree(E));
print("DATABASE_LOOKUP=", ellsearch("43a1"));

if(E.disc != -43, error("wrong discriminant"));
if(G[1] != 43 || G[3] != 1, error("wrong global reduction"));
if(!ellisoncurve(E,P), error("P is not on E"));
if(Q != ellmul(E,P,5), error("descent point relation failed"));
if(elltors(E)[1] != 1, error("unexpected torsion"));
if(#C != 1, error("unexpected 2-cover basis size"));
if((b^2-D) % (4*N), error("Heegner congruence failed"));
if(kronecker(D,43) != 1 || qfbclassno(D) != 1,error("Heegner hypothesis/class number failed"));
if(!ellisoncurve(E,H), error("ellheegner result is not on E"));
print("ALL_ASSERTIONS_PASSED=1");
