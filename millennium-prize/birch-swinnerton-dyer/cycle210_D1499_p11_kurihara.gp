\\ Cycle 210: exact p=11 one-prime Kurihara certificate for the D=-1499 twist.
E = ellinit([1,0,0,0,1]);
A = ellinit([1,0,1,-46813,-3372156843]);
[M, xm] = msfromell(E, -1);

p = 11;
q = 1499;
ell = 661;
generator = 2;
expected = 203746;

if (znorder(Mod(generator, ell)) != ell-1, error("2 is not primitive modulo 661"));
if (ell % p != 1 || (ellap(A, ell) - ell - 1) % p != 0, error("661 is not a Kolyvagin prime at p=11"));

modp(x) =
{
  my(d = denominator(x));
  if (d % p == 0, error("nonintegral modular symbol at 11: ", x));
  lift(Mod(numerator(x), p) / Mod(d, p));
};

term(a) =
{
  my(U = 0);
  for (u = 1, q-1, U += kronecker(u, q) * mseval(M, xm, [oo, (a*q + ell*u)/(ell*q)]));
  modp(U);
  lift(znlog(Mod(a, ell), Mod(generator, ell))) * U;
};

C = sum(a = 1, ell-1, term(a));

if (C != expected, error("exact Kurihara lift mismatch: ", C));
if (modp(C) != 4, error("Kurihara residue mismatch: ", modp(C)));

xP = 399030891253207/156180668809;
yP = 7009131418974188521075/61722131771310373;
Al = ellinit([Mod(1,ell),0,Mod(1,ell),Mod(-46813,ell),Mod(-3372156843,ell)]);
Pl = [Mod(xP,ell), Mod(yP,ell)];
if (ellcard(Al) != 660, error("wrong point count at 661"));
if (ellorder(Al, Pl) != 165, error("wrong order for P modulo 661"));

print("PASS Cycle 210 D=-1499 p=11 Kurihara certificate");
print("ell=661 eta=2 #A(F_661)=660 a_661=2");
print("delta_tilde_661=", C, " = ", modp(C), " mod 11");
print("P mod 661=", lift(Pl), " order=165; nonzero in A(F_661)/11A(F_661)");
