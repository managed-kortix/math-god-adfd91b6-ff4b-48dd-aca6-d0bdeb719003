E = ellinit([1, 0, 0, 0, 1]);
qs = [1499, 6287, 3823, 8317];

if (E.c4 != 1 || E.disc != -433, error("unexpected base invariants"));

checkq(q) =
{
  my(D, coeffs, T, TT, change, M, kappa);
  if (!isprime(q) || q == 433 || q % 2 == 0, error("invalid q", q));
  D = if (q % 4 == 1, q, -q);
  if (D % 4 != 1, error("D is not 1 mod 4", D));

  coeffs = [-1, (D - 1) / 4, 0, 0, D^3];
  T = ellinit(coeffs);
  TT = elltwist(E, D);
  if (vector(5, j, T[j]) != vector(5, j, TT[j]), error("explicit model differs from elltwist", q));
  if (T.c4 != D^2 || T.disc != -433 * D^6, error("incorrect twist invariants", q));

  change = 0;
  M = ellminimalmodel(T, &change);
  if (change[1] != 1, error("nontrivial minimal scaling", q, change));
  if (M.disc != T.disc, error("discriminant changed", q));

  kappa = 1 / abs(change[1]);
  if (kappa != 1 || numerator(kappa) % 7 == 0 || denominator(kappa) % 7 == 0, error("bad kappa", q, kappa));
  print([q, D, coeffs, change, kappa, Mod(kappa, 7)]);
};

for (i = 1, #qs, checkq(qs[i]));

print("cycle 188 exact twist-period checks passed");
