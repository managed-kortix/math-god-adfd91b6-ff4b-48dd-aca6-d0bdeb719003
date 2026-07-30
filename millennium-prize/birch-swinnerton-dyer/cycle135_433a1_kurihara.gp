\\ Exact Kurihara-sum positive control for 433a1 at p=7 and n=29*113.
E = ellinit([1,0,0,0,1]);
[M, xp] = msfromell(E, 1);

p = 7;
l1 = 29;
l2 = 113;
n = l1*l2;
g1 = 2;
g2 = 3;

if (znorder(Mod(g1, l1)) != l1-1, error("2 is not primitive modulo 29"));
if (znorder(Mod(g2, l2)) != l2-1, error("3 is not primitive modulo 113"));

modp(q) =
{
  my(d = denominator(q));
  if (d % p == 0,
    error("modular symbol has denominator divisible by 7: ", q));
  lift(Mod(numerator(q), p) / Mod(d, p));
};

T = matrix(p, p);
terms = 0;
addterm(a) =
{
  my(ms, d1, d2);
  if (gcd(a, n) != 1, return());
  ms = mseval(M, xp, [oo, a/n]);
  d1 = znlog(Mod(a, l1), Mod(g1, l1)) % p;
  d2 = znlog(Mod(a, l2), Mod(g2, l2)) % p;
  modp(ms); \\ Enforce 7-integrality before adding the exact rational value.
  T[d1+1, d2+1] += ms;
  terms++;
};
for (a = 1, n-1, addterm(a));

expected_T = [13, -18, -14, 24, 9, -18, 8; 22, -1, -24, -4, 23, -13, -8; 4, 30, -16, -10, 12, 2, -24; -9, 13, 11, -24, 11, 13, -9; -24, 2, 12, -10, -16, 30, 4; -8, -13, 23, -4, -24, -1, 22; 8, -18, 9, 24, -14, -18, 13];
if (T != expected_T, error("grouped modular-symbol matrix mismatch"));
if (terms != eulerphi(n), error("unit count mismatch: ", terms));

C = matrix(p, p, i, j, modp(T[i,j]*(i-1)*(j-1)));
row_contributions = vector(p, i, sum(j = 1, p, C[i,j]) % p);
column_contributions = vector(p, j, sum(i = 1, p, C[i,j]) % p);
delta = sum(i = 1, p, sum(j = 1, p, C[i,j])) % p;
if (delta != 3, error("Kurihara delta mismatch: ", delta));

print("curve=[1,0,0,0,1] conductor=", ellglobalred(E)[1], " p=", p, " n=", n, " roots=", [g1,g2]);
print("a_p=", ellap(E,p), " a_29=", ellap(E,l1), " a_113=", ellap(E,l2), " unit_terms=", terms);
print("rows=dlog_29_mod_7=0..6; cols=dlog_113_mod_7=0..6");
print("grouped_exact_modular_symbols=");
print(T);
print("weighted_contributions_mod_7=");
print(C);
print("row_contributions_mod_7=", row_contributions);
print("column_contributions_mod_7=", column_contributions);
print("delta_mod_7=", delta);
