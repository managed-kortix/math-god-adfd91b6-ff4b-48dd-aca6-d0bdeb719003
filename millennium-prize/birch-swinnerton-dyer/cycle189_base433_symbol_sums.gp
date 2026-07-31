\\ Cycle 189: exact level-433 symbol sums for [1:5] candidates.
\\ Output is checked against the committed raw-sum certificate.
default(parisizemax, 4000000000);

E = ellinit([1,0,0,0,1]);
p = 7;
ell = 29;
qs = [7589,14071,29023];
weights = [0,2,3,4,2,5,3,6,6,4,1,0,1,5];
active_a = [2,3,4,5,6,7,8,9,10,11,13,14];
expected = [[103/2,39,-39,-31/2,-103/2,-9,12,103/2,9,-103/2,-12,31/2],[188,111/2,195/2,64,385/2,-63,63,-111/2,-385/2,-3/2,3/2,-195/2],[-226,23/2,343/2,241,249/2,-30,30,-23/2,-249/2,291/2,-291/2,-343/2]];
expected_total = [359/2,1243/2,77/2];
expected_residue = [1,2,0];

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
      if (U != expected[iq][ia],
        error("raw-sum mismatch at q=",q,", a=",a,": ",U));
      total += weights[a]*U;
      print("ROW,",q,",",D,",",epsilon,",",a,",",weights[a],",",
            numerator(U),",",denominator(U));
    );
    if (total != expected_total[iq] || modp(total) != expected_residue[iq],
      error("completed-sum mismatch for q=",q,": ",total));
    print("RESULT q=",q," D=",D," epsilon=",epsilon," kappa=1 total=",total,
          " c_mod_7=",modp(total)," status=",if(modp(total)==0,"ZERO","NONZERO"),
          " model=",[Tmin.a1,Tmin.a2,Tmin.a3,Tmin.a4,Tmin.a6],
          " change=",change);
  );
  print("PASS: exact level-433 computations agree with committed Cycle 189 values");
};

main();
