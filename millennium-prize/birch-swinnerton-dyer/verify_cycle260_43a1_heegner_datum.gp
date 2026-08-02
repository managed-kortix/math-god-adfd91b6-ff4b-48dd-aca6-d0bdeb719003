E = ellinit([0, 1, 1, 0, 0]);
K = bnfinit(x^2 - x + 2, 1);

if(E.disc != -43, error("wrong discriminant"));
if(ellglobalred(E)[1] != 43, error("wrong conductor"));
if(elltors(E)[1] != 1, error("unexpected rational torsion"));
if(!ellisoncurve(E, [0, 0]), error("P is not on E"));
if(ellmul(E, [0, 0], 2) != [-1, -1], error("wrong 2P"));
if(ellmul(E, [0, 0], 3) != [1, -2], error("wrong 3P"));
if(K.disc != -7, error("wrong field discriminant"));
if(K.no != 1, error("wrong class number"));
if(kronecker(-7, 43) != 1, error("43 does not split"));
if((37^2 + 7) % (4 * 43) != 0, error("Heegner congruence failed"));

print("PASS exact curve model, conductor, discriminant, torsion, and point checks");
print("PASS exact K discriminant, class number, and Heegner splitting checks");
print("GAP exact optimal-parametrization evaluation at the D=-7 CM point");
print("GAP certified all-prime residual-image packet, especially p=7 surjectivity");
print("GAP proof-enabled independent 2-Selmer replay");
