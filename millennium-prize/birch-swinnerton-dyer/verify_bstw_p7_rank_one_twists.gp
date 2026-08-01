main() =
{
  my(base = ellinit("433a1"));
  my(Ds = [-1499, -29023]);
  my(models = [[1, 0, 1, -46813, -3372156843],
               [1, 1, 1, -17548636, -24475377572834]]);
  my(conductors = [972951433, 364730851057]);

  for (i = 1, #Ds,
    my(D = Ds[i]);
    my(q = abs(D));
    my(E = ellinit(models[i]));
    my(red = ellglobalred(E));

    my(minimal = ellminimalmodel(elltwist(base, D)));
    if ([minimal.a1, minimal.a2, minimal.a3, minimal.a4, minimal.a6] != models[i],
        error("minimal model mismatch for D=", D));
    if (red[1] != conductors[i] || red[1] != 433*q^2,
        error("conductor mismatch for D=", D));
    if (ellrootno(E) != -1, error("root-number mismatch for D=", D));
    if (ellap(E, 7) != 3, error("a_7 mismatch for D=", D));
    if (ellcard(E, 7) != 5, error("point-count mismatch at 7 for D=", D));
    if (valuation(E.disc, 433) != 1,
        error("minimal-discriminant valuation mismatch at 433 for D=", D));
    if (elllocalred(E, 433) != [1, 5, [1, 0, 0, 0], 1],
        error("local data mismatch at 433 for D=", D));
    if (elllocalred(E, q) != [2, -1, [1, 0, 0, 0], 2],
        error("local data mismatch at twist prime for D=", D));
    if (red[3] != 2, error("Tamagawa product mismatch for D=", D));
    if (elltors(E)[1] != 1, error("torsion mismatch for D=", D));

    print("D=", D);
    print("model=", models[i]);
    print("conductor=", red[1], "=433*", q, "^2");
    print("root_number=", ellrootno(E));
    print("a_7=", ellap(E, 7), ", #E(F_7)=", ellcard(E, 7));
    print("v_433(minimal_discriminant)=", valuation(E.disc, 433));
    print("local_433=", elllocalred(E, 433));
    print("local_", q, "=", elllocalred(E, q));
    print("tamagawa_product=", red[3]);
    print("torsion_order=", elltors(E)[1]);
  );
  print("certificate_status=PASS");
};

main();
