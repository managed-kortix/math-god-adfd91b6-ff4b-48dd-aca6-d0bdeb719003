\\ Cycle 188: exact Cycle-187 base-symbol twist sums for q=1499,6287.
E = ellinit([1,0,0,0,1]);
[M, xm] = msfromell(E, -1);
p = 7;
ell = 29;
generator = 2;
qs = [1499, 6287];
expected_full = [-150, -1616];

modp(x) =
{
  my(d = denominator(x));
  if (d % p == 0, error("denominator is not a 7-adic unit: ", x));
  lift(Mod(numerator(x), p) / Mod(d, p));
};

dlog29(a) = lift(znlog(Mod(a, ell), Mod(generator, ell)));

process(q, expected) =
{
  my(D = if(q % 4 == 1, q, -q), Et, change = 0, Emin, kappa, C = 0);
  my(U, T, dl);
  Et = elltwist(E, D);
  Emin = ellminimalmodel(Et, &change);
  if (change[1] != 1, error("unexpected nonunit differential scale for q=", q, ": ", change));
  kappa = 1;
  print("twist q=", q, " D=", D, " conductor=", ellglobalred(Emin)[1], " minimal_model=", [Emin.a1,Emin.a2,Emin.a3,Emin.a4,Emin.a6], " minimal_change=", change, " kappa=", kappa);
  for (a = 1, ell-1,
    U = 0;
    for (u = 1, q-1, U += kronecker(u,q) * mseval(M,xm,[oo,(a*q+ell*u)/(ell*q)]));
    T = kappa*U;
    modp(T);
    dl = dlog29(a);
    C += dl*T;
    print(q, "\t", a, "\t", dl, "\t", dl%p, "\t", U, "\t", kappa, "\t", T, "\t", modp(T));
  );
  if (C != expected, error("raw full sum mismatch for q=", q, ": ", C));
  print("result q=", q, " raw_full_sum=", C, " c_mod7=", modp(C), " status=", if(modp(C)==0,"zero","nonzero"));
};

print("cycle=188");
print("pari_version=", version());
print("curve=[1,0,0,0,1]");
print("base_conductor=", ellglobalred(E)[1]);
print("p=7 ell=29 eta=2 sign=-1 endpoint=[oo,(a*q+29*u)/(29*q)]");
print("columns=q,a,dlog2,dlog2_mod7,U_a,kappa,T_a,T_a_mod7");

for (iq = 1, #qs, process(qs[iq], expected_full[iq]));
