\\ Cycle 189: exact base-level-433 computation for [1:2] members.
\\ Tested with PARI/GP 2.15.4.
default(parisizemax, 4000000000);

E = ellinit([1,0,0,0,1]);
p = 7;
ell = 29;
generator = 2;
qs = [9521,11131];
weights = [0,2,3,4,2,5,3,6,6,4,1,0,1,5];
active_a = [2,3,4,5,6,7,8,9,10,11,13,14];
expected = [[7/2,-27,27,33/2,-7/2,3,-18,-123/2,-3,123/2,18,-33/2],[-35,91,65/2,31/2,-91,-107,-31/2,35,-65/2,-75/2,227/2,107]];
expected_total = [-867/2,186];
expected_residue = [4,4];
expected_model = [[1,1,1,-1888530,864071468336],[1,1,0,-2581232,-1380718842115]];
expected_change = [[1,-793,1,-396],[1,928,1,464]];

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

  print("q,D,epsilon,a,weight,numerator,denominator");
  for (iq = 1, #qs,
    my(q = qs[iq], D, epsilon, Tgen, change = 0, Tmin, M, x, total = 0);
    if (!isprime(q) || gcd(q,2*p*433*ell) != 1,
      error("twist-prime audit failed for q=",q));
    D = if (q % 4 == 1,q,-q);
    epsilon = if(q % 4 == 1,1,-1);
    Tgen = elltwist(E,D);
    Tmin = ellminimalmodel(Tgen,&change);
    if (change[1] != 1, error("kappa is not 1 for q=",q,": ",change));
    if (ellglobalred(Tmin)[1] != 433*q^2,
      error("twist conductor mismatch for q=",q));
    if ([Tmin.a1,Tmin.a2,Tmin.a3,Tmin.a4,Tmin.a6] != expected_model[iq]
        || change != expected_change[iq],
      error("twist model audit failed for q=",q));

    [M,x] = msfromell(E,epsilon);
    for (ia = 1, #active_a,
      my(a = active_a[ia], U = 0);
      for (u = 1, q-1,
        U += kronecker(u,q) * mseval(M,x,[oo,(a*q+ell*u)/(ell*q)]));
      if (U != expected[iq][ia],
        error("base-symbol sum mismatch at q=",q,", a=",a,": ",U));
      if (denominator(U) % p == 0,
        error("non-7-integral row at q=",q,", a=",a,": ",U));
      total += weights[a]*U;
      print(q,",",D,",",epsilon,",",a,",",weights[a],",",
            numerator(U),",",denominator(U));
    );
    if (total != expected_total[iq] || modp(total) != expected_residue[iq],
      error("c(q,29) mismatch for q=",q,": total=",total));
    print("RESULT q=",q," D=",D," kappa=1 total=",total,
          " c_mod_7=",modp(total)," status=",if(modp(total),"NONZERO","ZERO"),
          " conductor=",ellglobalred(Tmin)[1]," model=",
          [Tmin.a1,Tmin.a2,Tmin.a3,Tmin.a4,Tmin.a6]," change=",change);
  );
  print("PASS: exact Cycle 189 [1:2] computations match pinned values");
};

main();
