\\ Cycle 188: exact base-level-433 computation of c(q,29).
\\ Tested with PARI/GP 2.15.4. Output is checked against the committed CSV.
default(parisizemax, 4000000000);

E = ellinit([1,0,0,0,1]);
p = 7;
ell = 29;
generator = 2;
qs = [3823,8317];
weights = [0,2,3,4,2,5,3,6,6,4,1,0,1,5];
expected = [[-122,57,469/2,265/2,-57,-51,-265/2,122,-469/2,-55/2,-17/2,51],[-41,251/2,-229/2,-52,275/2,132,-132,-251/2,-275/2,37/2,-37/2,229/2]];
active_a = [2,3,4,5,6,7,8,9,10,11,13,14];
expected_total = [-90,-1413/2];
expected_residue = [1,4];

modp(x) =
{
  my(d = denominator(x));
  if (d % p == 0, error("non-7-integral completed sum: ", x));
  lift(Mod(numerator(x),p) / Mod(d,p));
};

main() =
{
if (ellglobalred(E)[1] != 433 || E.disc != -433,
  error("base curve audit failed"));
if (!isprime(ell) || znorder(Mod(generator,ell)) != ell-1,
  error("auxiliary-prime audit failed"));

for (iq = 1, #qs,
  q = qs[iq];
  if (!isprime(q) || gcd(q,2*p*433*ell) != 1,
    error("twist-prime audit failed for q=",q));
  D = if (q % 4 == 1,q,-q);
  epsilon = if(q % 4 == 1,1,-1);
  Tgen = elltwist(E,D);
  change = 0;
  Tmin = ellminimalmodel(Tgen,&change);
  if (change[1] != 1, error("kappa is not 1 for q=",q,": ",change));
  if (ellglobalred(Tmin)[1] != 433*q^2,
    error("twist conductor mismatch for q=",q));
  if (iq == 1 && [Tmin.a1,Tmin.a2,Tmin.a3,Tmin.a4,Tmin.a6]
      != [1,1,1,-304486,-55939199084], error("q=3823 model mismatch"));
  if (iq == 2 && [Tmin.a1,Tmin.a2,Tmin.a3,Tmin.a4,Tmin.a6]
      != [1,0,1,-1441094,575973336189], error("q=8317 model mismatch"));

  if (epsilon == 1, [M,x] = msfromell(E,1), [M,x] = msfromell(E,-1));
  total = 0;
  for (ia = 1, #active_a,
    a = active_a[ia];
    U = 0;
    for (u = 1, q-1,
      U += kronecker(u,q) * mseval(M,x,[oo,(a*q+ell*u)/(ell*q)]));
    if (U != expected[iq][ia],
      error("base-symbol sum mismatch at q=",q,", a=",a,": ",U));
    total += weights[a]*U;
    print(q,",",D,",",epsilon,",",a,",",weights[a],",",
          numerator(U),",",denominator(U));
  );
  if (total != expected_total[iq] || modp(total) != expected_residue[iq],
    error("c(q,29) mismatch for q=",q,": total=",total));
  print("RESULT q=",q," D=",D," kappa=1 total=",total,
        " c_mod_7=",modp(total)," status=NONZERO model=",
        [Tmin.a1,Tmin.a2,Tmin.a3,Tmin.a4,Tmin.a6]," change=",change);
);
print("PASS: exact base-level-433 computations agree with committed values");
};

main();
