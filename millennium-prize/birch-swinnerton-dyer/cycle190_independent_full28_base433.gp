\\ Cycle 190: independent full 28-row base-level-433 replay.
\\ This producer does not import the Cycle 188/189 row tables or totals.
default(parisizemax, 4000000000);

E = ellinit([1,0,0,0,1]);
p = 7;
ell = 29;
generator = 2;
qs = [1499,29023];
short_weights = [0,2,3,4,2,5,3,6,6,4,1,0,1,5];

modp(x) =
{
  my(d = denominator(x));
  if (d % p == 0, error("non-7-integral rational: ",x));
  lift(Mod(numerator(x),p) / Mod(d,p));
};

dlog29(a) = lift(znlog(Mod(a,ell),Mod(generator,ell)));

main() =
{
  if (ellglobalred(E)[1] != 433 || E.disc != -433,
    error("base curve audit failed"));
  if (!isprime(ell) || znorder(Mod(generator,ell)) != ell-1,
    error("auxiliary-prime audit failed"));
  print("META,cycle=190,producer=full28,pari=",version(),
        ",curve=[1;0;0;0;1],level=433,p=7,ell=29,generator=2");

  for (iq = 1, #qs,
    my(q = qs[iq], D, epsilon, Tgen, change = 0, Tmin, M, x);
    my(rows = vector(ell-1), full = 0, paired = 0);
    if (!isprime(q) || gcd(q,2*p*433*ell) != 1,
      error("twist-prime audit failed for q=",q));
    D = if (q % 4 == 1,q,-q);
    epsilon = if (q % 4 == 1,1,-1);
    Tgen = elltwist(E,D);
    Tmin = ellminimalmodel(Tgen,&change);
    if (change[1] != 1, error("kappa is not 1 for q=",q,": ",change));
    if (ellglobalred(Tmin)[1] != 433*q^2,
      error("twist conductor mismatch for q=",q));

    [M,x] = msfromell(E,epsilon);
    for (a = 1, ell-1,
      my(U = 0, dl = dlog29(a));
      for (u = 1, q-1,
        U += kronecker(u,q) *
             mseval(M,x,[oo,(a*q+ell*u)/(ell*q)]));
      rows[a] = U;
      full += dl*U;
      print("ROW,",q,",",D,",",epsilon,",",a,",",dl,",",
            numerator(U),",",denominator(U));
    );
    for (a = 1, (ell-1)/2,
      if (rows[a] != rows[ell-a],
        error("a <-> 29-a symmetry failed at q=",q,", a=",a));
      paired += short_weights[a]*rows[a];
    );
    if (modp(full) != modp(paired),
      error("full/paired reductions disagree for q=",q));
    print("RESULT,",q,",",D,",",epsilon,",",
          numerator(full),",",denominator(full),",",
          numerator(paired),",",denominator(paired),",",modp(full),",",
          if(modp(full)==0,"ZERO","NONZERO"),",",
          [Tmin.a1,Tmin.a2,Tmin.a3,Tmin.a4,Tmin.a6],",",change);
  );
  print("PASS,Cycle 190 independent full-28-row replay");
};

main();
