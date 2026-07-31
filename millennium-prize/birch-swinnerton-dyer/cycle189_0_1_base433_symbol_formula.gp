\\ Cycle 189: exact base-level-433 computation for the [0:1] row.
\\ Tested with PARI/GP 2.15.4.
default(parisizemax, 4000000000);

E = ellinit([1,0,0,0,1]);
p = 7;
ell = 29;
generator = 2;
qs = [8191,10949,19559,31963];
weights = [0,2,3,4,2,5,3,6,6,4,1,0,1,5];
active_a = [2,3,4,5,6,7,8,9,10,11,13,14];
artifact = "millennium-prize/birch-swinnerton-dyer/cycle189_0_1_base433_symbol_sums.csv";
continuation = type(getenv("CYCLE189_CONTINUE")) == "t_STR";
if (continuation, qs = [34679,39439,45053,66179,77617,99709,103811,109789,114311,176849,191143]);
if (continuation, artifact = "millennium-prize/birch-swinnerton-dyer/cycle189_0_1_base433_symbol_sums_continuation.csv");

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

  write(artifact,"q,D,epsilon,a,weight,numerator,denominator");
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

    [M,x] = msfromell(E,epsilon);
    for (ia = 1, #active_a,
      my(a = active_a[ia], U = 0);
      for (u = 1, q-1,
        U += kronecker(u,q) * mseval(M,x,[oo,(a*q+ell*u)/(ell*q)]));
      total += weights[a]*U;
      write(artifact,q,",",D,",",epsilon,",",a,",",weights[a],",",
            numerator(U),",",denominator(U));
      print("ROW q=",q," a=",a," weight=",weights[a]," U=",U);
    );
    print("RESULT q=",q," D=",D," epsilon=",epsilon," kappa=1 total=",total,
          " c_mod_7=",modp(total)," status=",if(modp(total)==0,"ZERO","NONZERO"),
          " model=",[Tmin.a1,Tmin.a2,Tmin.a3,Tmin.a4,Tmin.a6],
          " change=",change);
    if (continuation && modp(total) == 0, break);
  );
  print("PASS: exact base-level-433 computations completed");
};

main();
