default(parisizemax, 4000000000);

require(c, message) = if(!c, error(message));

B = ellinit([1, 0, 0, 0, 1]);
A = ellinit([1, 0, 1, -46813, -3372156843]);
P = [399030891253207 / 156180668809, 7009131418974188521075 / 61722131771310373];
d = 172385;

require(factor(d) == [5, 1; 23, 1; 1499, 1], "wrong auxiliary twist");
require(isfundamental(d), "auxiliary twist is not fundamental");
require(ellglobalred(B)[1] == 433, "wrong base conductor");
require(ellglobalred(A)[1] == 433 * 1499^2, "wrong rank-one conductor");
require(ellrootno(A) == -1, "wrong rank-one root number");
require(elltors(A)[1] == 1, "nontrivial rational torsion");
require(ellisoncurve(A, P), "P is not on A");

[M, x] = msfromell(B, 1);
S = 0;
for (a = 1, d - 1, c = kronecker(a, d); if(c, S += c * mseval(M, x, [oo, a / d])));
require(S == 64, "exact modular-symbol sum is not 64");
require(issquare(S, &index), "analytic factor is not a square");
require(index == 8, "analytic square-root factor is not 8");

Hplus = ellmul(A, P, index);
Hminus = ellneg(A, Hplus);
require(ellisoncurve(A, Hplus), "8P is not on A");
require(Hminus == ellmul(A, P, -index), "sign check failed");

print("AUXILIARY_TWIST_DISCRIMINANT=", d);
print("EXACT_MODULAR_SYMBOL_SUM=", S);
print("EXACT_ANALYTIC_INDEX_SQUARE_FACTOR=", S);
print("EXACT_ANALYTIC_SQUARE_ROOT_FACTOR=", index);
print("INTEGRAL_MORDELL_WEIL_INDEX=NOT_PROVED_WITHOUT_SHA_INPUT");
print("CANDIDATE_TRACE_PLUS=", Hplus);
print("CANDIDATE_TRACE_MINUS=", Hminus);
print("EXACT_ANALYTIC_FACTOR_CERTIFICATE=PASS");
print("EXACT_TRACE_TO_CANDIDATE_IDENTIFICATION=NOT_PROVED");
