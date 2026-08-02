require(c, message) = if(!c, error(message));

D = -115;
N = 433 * 1499^2;
model = [1, 0, 1, -46813, -3372156843];
P = [399030891253207 / 156180668809, 7009131418974188521075 / 61722131771310373];
E = ellinit(model);

require(isfundamental(D), "auxiliary discriminant is not fundamental");
require(qfbclassno(D) == 2, "wrong auxiliary class number");
require(gcd(D, N) == 1, "auxiliary discriminant is not coprime to N");
require(kronecker(D, 433) == 1, "433 does not split");
require(kronecker(D, 1499) == 1, "1499 does not split");
require(Mod(54, 433)^2 == Mod(D, 433), "wrong root modulo 433");
require(Mod(431, 1499)^2 == Mod(D, 1499), "wrong root modulo 1499");

b4N = 2219057073;
b = b4N % (2 * N);
c = (b^2 - D) / (4 * N);
Q = Qfb(N, b, c);
require(Mod(b4N, 4 * N)^2 == Mod(D, 4 * N), "Heegner root is not a square root modulo 4N");
require(b^2 - 4 * N * c == D, "CM form has wrong discriminant");
require(gcd([N, b, c]) == 1, "CM form is not primitive");
require(qfbred(Q) == Qfb(5, 5, 7), "wrong CM ideal class");
require(qfbred(qfbcompraw(Q, Q)) == Qfb(1, 1, 29), "CM ideal class does not have order two");

require(ellglobalred(E)[1] == N, "wrong conductor");
require(ellrootno(E) == -1, "wrong root number for A");
require(elltors(E)[1] == 1, "nontrivial rational torsion");
require(ellisoncurve(E, P), "reference point is not on A");

aux = ellminimalmodel(elltwist(E, D));
auxmodel = [aux.a1, aux.a2, aux.a3, aux.a4, aux.a6];
require(auxmodel == [1, 1, 1, -619095588, 5128622847262406], "wrong auxiliary twist model");
require(ellglobalred(aux)[1] == 12867282701425, "wrong auxiliary twist conductor");
require(ellrootno(aux) == 1, "auxiliary twist does not have even sign");

base = ellinit([1, 0, 0, 0, 1]);
[MS, plus_symbol] = msfromell(base, 1);
auxiliary_twist_discriminant = 1499 * 115;
require(isfundamental(auxiliary_twist_discriminant), "composite twist discriminant is not fundamental");
aux_from_base = ellminimalmodel(elltwist(base, auxiliary_twist_discriminant));
require([aux_from_base.a1, aux_from_base.a2, aux_from_base.a3, aux_from_base.a4, aux_from_base.a6] == auxmodel, "twist-composition model mismatch");
central_symbol_sum = 0;
for(a = 1, auxiliary_twist_discriminant - 1, if(gcd(a, auxiliary_twist_discriminant) == 1, central_symbol_sum += kronecker(auxiliary_twist_discriminant, a) * mseval(MS, plus_symbol, [oo, a / auxiliary_twist_discriminant])));
require(central_symbol_sum == 64, "wrong auxiliary central modular-symbol sum");

print("A_MODEL=", model);
print("A_CONDUCTOR=", N);
print("A_NERON_DIFFERENTIAL=dx/(2*y+x+1)");
print("A_ROOT_NUMBER=-1");
print("A_TORSION_ORDER=1");
print("A_REFERENCE_POINT=", P);
print("AUXILIARY_DISCRIMINANT=", D);
print("AUXILIARY_CLASS_NUMBER=2");
print("SPLITTING_ROOT_433=54");
print("SPLITTING_ROOT_1499=431");
print("HEEGNER_ROOT_MOD_4N=", b4N);
print("CM_FORM=", Q);
print("CM_FORM_REDUCED_CLASS=", qfbred(Q));
print("AUXILIARY_TWIST_MODEL=", auxmodel);
print("AUXILIARY_TWIST_CONDUCTOR=", ellglobalred(aux)[1]);
print("AUXILIARY_TWIST_ROOT_NUMBER=", ellrootno(aux));
print("AUXILIARY_TWIST_DISCRIMINANT_RELATIVE_TO_433a1=", auxiliary_twist_discriminant);
print("AUXILIARY_EXACT_CENTRAL_MODULAR_SYMBOL_SUM=", central_symbol_sum);
print("AUXILIARY_TWIST_NONVANISHING_CERTIFICATE=PASS");
print("EXACT_HEEGNER_DATUM_CHECKS=PASS");
print("OPTIMAL_PARAMETRIZATION_CERTIFICATE=ABSENT");
print("EXACT_CM_TRACE_COORDINATES=ABSENT");
print("MANIN_NORMALIZATION_CERTIFICATE=ABSENT");
print("HK236_ITEM_1=TERMINAL_OBSTRUCTION");
