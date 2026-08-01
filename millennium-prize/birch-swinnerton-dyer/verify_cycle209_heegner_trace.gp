iferr(default(parisizemax, 4000000000), E, error("cannot set parisizemax: ", E));

require(c, message) = if(!c, error(message));

D = -115;
N = 433 * 1499^2;
E = ellinit([1, 0, 1, -46813, -3372156843]);
P = [399030891253207 / 156180668809, 7009131418974188521075 / 61722131771310373];

require(isfundamental(D), "D is not fundamental");
require(qfbclassno(D) == 2, "wrong class number");
require(gcd(D, N) == 1, "D is not coprime to N");
require(kronecker(D, 433) == 1, "433 does not split");
require(kronecker(D, 1499) == 1, "1499 does not split");
require(Mod(54, 433)^2 == Mod(D, 433), "wrong square root at 433");
require(Mod(431, 1499)^2 == Mod(D, 1499), "wrong square root at 1499");
heegner_root = 2219057073;
require(Mod(heegner_root, 4 * N)^2 == Mod(D, 4 * N), "D is not a square modulo 4N");

require(ellglobalred(E)[1] == N, "wrong conductor");
require(ellrootno(E) == -1, "wrong root number");
require(elltors(E)[1] == 1, "nontrivial rational torsion");
require(ellisoncurve(E, P), "P is not on E");

Hprimitive = ellheegner(E);
require(Hprimitive == P || Hprimitive == ellneg(E, P), "Heegner descent output is not +/-P");

\\ The value 8 is not extracted or certified by this script. It is the
\\ nondirected floating candidate reported by PARI's internal index stage.
if(Hprimitive == P, coeff = 8, coeff = -8);
Htrace = ellmul(E, Hprimitive, 8);
require(Htrace == ellmul(E, P, coeff), "wrong trace multiple");

E7 = ellinit([1, 0, 1, -46813, -3372156843] * Mod(1, 7));
P7 = Mod(1, 7) * P;
H7 = Mod(1, 7) * Htrace;
require(P7 == [Mod(6, 7), Mod(5, 7)], "wrong reduction of P");
require(ellorder(E7, P7) == 5, "wrong order of P mod 7");

require(Mod(coeff, 7) != 0, "Heegner coefficient vanishes mod 7");

print("FIELD_DISCRIMINANT=", D);
print("CLASS_NUMBER=", qfbclassno(D));
print("SPLITTING_ROOT_433=54");
print("SPLITTING_ROOT_1499=431");
print("HEEGNER_DESCENT_POINT=", Hprimitive);
print("PARI_CANDIDATE_HEEGNER_TRACE=", Htrace);
print("REFERENCE_POINT=", P);
print("NUMERICAL_CANDIDATE_TRACE_COEFFICIENT=", coeff);
print("NUMERICAL_CANDIDATE_TRACE_COEFFICIENT_MOD_7=", lift(Mod(coeff, 7)));
print("P_MOD_7=", lift(P7));
print("PARI_CANDIDATE_TRACE_MOD_7=", lift(H7));
print("EXACT_DOWNSTREAM_ARITHMETIC=PASS");
print("RIGOROUS_HEEGNER_INDEX_CERTIFICATE=NO");
