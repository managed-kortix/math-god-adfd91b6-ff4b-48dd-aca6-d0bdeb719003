default(parisizemax, 512000000);

main() =
{
  my(base = ellinit("433a1"));
  my(Ds = [-1499, -29023]);
  my(models = [[1, 0, 1, -46813, -3372156843], [1, 1, 1, -17548636, -24475377572834]]);
  my(conductors = [972951433, 364730851057]);
  my(covers = [-1499*x^4 + 2998*x^3 + 7495*x^2 + 8994*x - 1499, -29023*x^4 - 58046*x^3 - 29023*x^2 - 232184*x - 116092]);
  my(P1499 = [399030891253207/156180668809, 7009131418974188521075/61722131771310373]);
  my(D, raw, minimal, change, descent, cover, E1499);

  for (i = 1, #Ds,
    D = Ds[i];
    raw = ellinit(elltwist(base, D));
    minimal = ellminimalmodel(raw, &change);
    if (vector(5, j, minimal[j]) != models[i], error("minimal model mismatch for D=", D));
    if (ellglobalred(minimal)[1] != conductors[i], error("conductor mismatch for D=", D));

    descent = ellrank(minimal, 0);
    if (descent[1] != 1 || descent[2] != 1 || descent[3] != 0, error("raw 2-descent record mismatch for D=", D));
    if (elltors(minimal)[1] != 1, error("unexpected rational torsion for D=", D));
    if (ellrootno(minimal) != -1, error("root-number mismatch for D=", D));

    cover = ell2cover(ellrankinit(minimal));
    if (#cover != 1 || cover[1][1] != covers[i], error("2-cover mismatch for D=", D));

    print("D=", D);
    print("minimal_model=", models[i]);
    print("conductor=", ellglobalred(minimal)[1]);
    print("torsion_order=", elltors(minimal)[1]);
    print("root_number=", ellrootno(minimal));
    print("ellrank_raw=", descent);
    print("selmer_cover=", cover[1][1]);
    print("certified_2selmer_dimension_upper_bound=1");
    if (D == -1499,
        print("certified_algebraic_rank_interval=[1,1]"),
        print("certified_algebraic_rank_interval=[0,1]"));
  );

  E1499 = ellinit(models[1]);
  if (!ellisoncurve(E1499, P1499), error("P1499 is not on the curve"));
  if (elltors(E1499)[1] != 1, error("torsion check failed for P1499 argument"));
  if (ellrank(E1499, 0, [P1499])[1] != 1, error("P1499 does not certify the lower bound"));
  print("P1499=", P1499);
  print("P1499_height=", ellheight(E1499, P1499));
  print("certificate_status=PASS");
};

main();
