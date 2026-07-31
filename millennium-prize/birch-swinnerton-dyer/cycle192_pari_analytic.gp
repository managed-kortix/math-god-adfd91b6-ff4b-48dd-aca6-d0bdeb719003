default(realprecision, 48);
default(parisizemax, 3000000000);

main() =
{
  my(base = ellinit([1, 0, 0, 0, 1]));
  my(Ds = [-1499, -29023]);
  my(D, T);

  print("PARI_VERSION=", version());
  print("DISPLAYED_DECIMAL_DIGITS=48");
  for (i = 1, #Ds,
    D = Ds[i];
    T = elltwist(base, D);
    print("D=", D);
    print("TWIST_MODEL=", vector(5, j, T[j]));
    print("CONDUCTOR=", ellglobalred(T)[1]);
    print("ELLROOTNO=", ellrootno(T));
    print("LFUNROOTRES=", lfunrootres(T));
    print("ELLANALYTICRANK=", ellanalyticrank(T));
    print("ELLL1_D0=", ellL1(T, 0));
    print("ELLL1_D1=", ellL1(T, 1));
  );
};

main();
