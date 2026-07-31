\\ Exact p-power Mazur--Tate raw moments for 433a1, p=7 (PARI/GP 2.17.2).
default(parisizemax, 2000000000);

E = ellinit([1,0,0,0,1]);
[M, xp] = msfromell(E, 1);
p = 7;
gam = 8;

raw_moments(nn) =
{
  my(q = p^(nn+1), ord = p^nn, logs = Map());
  my(g = Mod(gam, q), z = Mod(1, q));
  my(D0 = 0, D1 = 0, D2 = 0);
  my(omega, principal, ell, ms);

  for (j = 0, ord-1,
    mapput(logs, lift(z), j);
    z *= g
  );
  if (z != 1, error("bad gamma order at level ", nn));

  for (a = 1, q-1,
    if (a % p,
      omega = lift(teichmuller(a + O(p^(nn+1)))) % q;
      principal = lift(Mod(a, q) / Mod(omega, q));
      if (!mapisdefined(logs, principal, &ell),
        error("missing logarithm at level ", nn, ", a=", a)
      );
      ms = mseval(M, xp, [oo, a/q]);
      D0 += ms;
      D1 += ms * ell;
      D2 += ms * ell^2
    )
  );
  if (denominator(D0) != 1 || denominator(D1) != 1 || denominator(D2) != 1,
    error("nonintegral moment at level ", nn)
  );
  [D0,D1,D2]
};

expected = Map();
mapput(expected, 4, [0,-4802,967053944]);
mapput(expected, 5, [0,621859,12876477045]);
mapput(expected, 6, [0,78942479,9062036974073]);

check(nn) =
{
  my(D = raw_moments(nn));
  if (D != mapget(expected, nn), error("moment mismatch at level ", nn));
  print("n=",nn," conductor=7^",nn+1," D0=",D[1]," D1=",D[2]," D2=",D[3])
};

if (ellglobalred(E)[1] != 433 || ellap(E,p) != -3, error("curve check failed"));
for (nn = 4, 6, check(nn));

\\ The compatible ordinary measure requires the lower-conductor V_7 term.
\\ These checks use the exact raw levels above; alpha is the unit root mod 7^7.
alpha = Mod(501645,7^7);
D4 = mapget(expected,4); D5 = mapget(expected,5); D6 = mapget(expected,6);
M5 = lift(alpha^-6 * (D5[3] - alpha^-1*(7*D4[3] + 6*7^5*D4[2]))) % 7^5;
M6 = lift(alpha^-7 * (D6[3] - alpha^-1*(7*D5[3] + 6*7^6*D5[2]))) % 7^6;
if (M5 != 9448 || M6 != 76676, error("ordinary stabilization mismatch"));
print("ordinary stabilized M2 mod 7^5 = ",M5);
print("ordinary stabilized M2 mod 7^6 = ",M6);
print("PASS: all exact raw moments agree.");
