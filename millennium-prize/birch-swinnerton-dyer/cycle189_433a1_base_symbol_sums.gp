\\ Cycle 189: exact base-level-433 producer for the [1:3] q bucket.
\\ Run with: gp -q cycle189_433a1_base_symbol_sums.gp > cycle189_base_symbol_sums.csv
default(parisizemax, 4000000000);

E = ellinit([1,0,0,0,1]);
p = 7;
ell = 29;
qs = [11831,14897,48889];
active_a = [2,3,4,5,6,7,8,9,10,11,13,14];
weights = [0,2,3,4,2,5,3,6,6,4,1,0,1,5];

modp(x) =
{
  my(d = denominator(x));
  if (d % p == 0, error("non-7-integral completed sum: ",x));
  lift(Mod(numerator(x),p) / Mod(d,p));
};

main() =
{
  my(seen_zero = 0, seen_nonzero = 0);
  if (ellglobalred(E)[1] != 433 || E.disc != -433,
    error("base curve audit failed"));
  if (!isprime(ell) || znorder(Mod(2,ell)) != ell-1,
    error("auxiliary-prime audit failed"));
  print("q,D,epsilon,a,weight,numerator,denominator");

  for (iq = 1, #qs,
    my(q = qs[iq], D, epsilon, Tgen, change = 0, Tmin, M, x, total = 0);
    if (!isprime(q) || gcd(q,2*p*433*ell) != 1,
      error("twist-prime audit failed for q=",q));
    D = if (q % 4 == 1,q,-q);
    epsilon = if (q % 4 == 1,1,-1);
    Tgen = elltwist(E,D);
    Tmin = ellminimalmodel(Tgen,&change);
    if (change[1] != 1, error("kappa is not 1 for q=",q,": ",change));
    if (ellglobalred(Tmin)[1] != 433*q^2,
      error("twist conductor mismatch for q=",q));
    if (epsilon == 1, [M,x] = msfromell(E,1), [M,x] = msfromell(E,-1));

    for (ia = 1, #active_a,
      my(a = active_a[ia], U = 0);
      for (u = 1, q-1,
        U += kronecker(u,q) * mseval(M,x,[oo,(a*q+ell*u)/(ell*q)]));
      total += weights[a]*U;
      print(q,",",D,",",epsilon,",",a,",",weights[a],",",
            numerator(U),",",denominator(U));
    );
    my(residue = modp(total));
    print("#RESULT,q=",q,",total_num=",numerator(total),
          ",total_den=",denominator(total),",c_mod_7=",residue,
          ",status=",if(residue==0,"ZERO","NONZERO"),
          ",model=",[Tmin.a1,Tmin.a2,Tmin.a3,Tmin.a4,Tmin.a6],
          ",change=",change);
    if (residue == 0, seen_zero = 1, seen_nonzero = 1);
    if (seen_zero && seen_nonzero,
      print("#STOP,zero/nonzero collision found within [1:3]");
      break());
  );
};

main();
