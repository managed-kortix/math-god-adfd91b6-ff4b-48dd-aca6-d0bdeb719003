default(parisizemax, 512000000);

main() =
{
  my(base = ellinit("433a1"));
  my(Ds = [-1499, -29023]);
  my(expected_models = [[1, 0, 1, -46813, -3372156843],
                        [1, 1, 1, -17548636, -24475377572834]]);
  my(reduced_polynomial = x^3 + x - 8);
  my(B = bnfinit(reduced_polynomial, 1));
  my(quotient_certified, full_certified);
  my(P1499 = [399030891253207/156180668809, 7009131418974188521075/61722131771310373]);
  my(D, E, f2, R);

  quotient_certified = bnfcertify(B, 1);
  full_certified = bnfcertify(B);
  if (quotient_certified != 1, error("class-group quotient certification failed"));
  if (full_certified != 1, error("full BNF certification failed"));
  if (B.disc != -1732 || B.sign != [1, 1], error("certified cubic invariant mismatch"));
  if (B.clgp[1] != 2 || B.clgp[2] != [2], error("certified class-group mismatch"));

  print("PARI_VERSION=", version());
  print("CUBIC_REDUCED_POLYNOMIAL=", reduced_polynomial);
  print("CUBIC_DISCRIMINANT=", B.disc);
  print("CUBIC_SIGNATURE=", B.sign);
  print("CUBIC_CLASS_GROUP=", B.clgp);
  print("CUBIC_FUNDAMENTAL_UNITS=", B.fu);
  print("CUBIC_TORSION_UNITS=", B.tu);
  print("BNFCERTIFY_QUOTIENT=", quotient_certified);
  print("BNFCERTIFY_FULL=", full_certified);

  for (i = 1, #Ds,
    D = Ds[i];
    E = ellminimalmodel(ellinit(elltwist(base, D)));
    if (vector(5, j, E[j]) != expected_models[i],
        error("minimal model mismatch for D=", D));

    f2 = x^3 + E.b2*x^2 + 8*E.b4*x + 16*E.b6;
    if (polredabs(f2) != reduced_polynomial,
        error("2-division cubic mismatch for D=", D));
    R = ellrank(E, 0);
    if (R[1] != 1 || R[2] != 1 || R[3] != 0,
        error("raw ellrank record mismatch for D=", D));
    if (D == -1499,
      if (!ellisoncurve(E, P1499), error("D=-1499 point mismatch"));
      if (elltors(E)[1] != 1, error("D=-1499 torsion mismatch"));
      if (#R[4] != 1 || R[4][1] != P1499, error("D=-1499 point-list mismatch")),
      if (#R[4] != 0, error("D=-29023 unexpectedly has a point witness"))
    );

    print("D=", D);
    print("MINIMAL_MODEL=", vector(5, j, E[j]));
    print("TWO_DIVISION_CUBIC=", f2);
    print("TWO_DIVISION_CUBIC_DISCRIMINANT=", factor(poldisc(f2)));
    print("TWO_DIVISION_CUBIC_POLREDABS=", polredabs(f2));
    print("ELLRANK_RAW=", R);
    print("CERTIFIED_2SELMER_DIMENSION_UPPER_BOUND=1");
    if (D == -1499,
        print("CERTIFIED_ALGEBRAIC_RANK_INTERVAL=[1, 1]"),
        print("CERTIFIED_ALGEBRAIC_RANK_INTERVAL=[0, 1]"));
  );
  print("CERTIFICATE_STATUS=PASS");
};

main();
