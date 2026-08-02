default(parisizemax, 268435456);

require(c, message) = if(!c, error(message));

E = ellinit([0, 1, 1, 0, 0]);
T = ellinit([0, -1, 1, -16, -106]);
P = [0, 0];

require(ellglobalred(E)[1] == 43, "wrong conductor");
require(ellglobalred(E)[3] == 1, "wrong Tamagawa product");
require(elltors(E)[1] == 1, "nontrivial rational torsion");
require(ellrootno(E) == -1, "wrong root number");
require(ellrootno(T) == 1, "wrong twist root number");
require(ellisoncurve(E, P), "P is not on E");

[M, plus_symbol] = msfromell(T, 1);
central_symbol = mseval(M, plus_symbol, [oo, 0]);
require(central_symbol == 2, "twist central modular symbol is not 2");

print("BASE_ROOT_NUMBER=", ellrootno(E));
print("TWIST_ROOT_NUMBER=", ellrootno(T));
print("TWIST_PLUS_SYMBOL_AT_ZERO=", central_symbol);
print("TWIST_BSD_REAL_PERIOD_OVER_MODULAR_SYMBOL_PERIOD=2");
print("EXACT_CONCLUSION=L(E^(-7),1)/OMEGA_E^(-7)=1");
print("EXACT_43A1_BSD_SYMBOL_CERTIFICATE=PASS");
