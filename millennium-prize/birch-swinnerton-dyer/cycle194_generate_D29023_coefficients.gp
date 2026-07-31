default(parisizemax, 1000000000);

main() =
{
  my(D = -29023, M = 650000);
  my(E = ellinit(elltwist(ellinit("433a1"), D)));
  my(minimal = ellminimalmodel(E));
  my(model = vector(5, j, minimal[j]));
  my(conductor = ellglobalred(minimal)[1]);
  my(root_number = ellrootno(minimal));
  my(red433 = elllocalred(minimal, 433));
  my(red29023 = elllocalred(minimal, 29023));
  if (model != [1, 1, 1, -17548636, -24475377572834], error("minimal-model mismatch"));
  if (conductor != 364730851057, error("conductor mismatch"));
  if (root_number != -1, error("root-number mismatch"));
  my(v = ellan(E, M));
  if (v[1] != 1, error("coefficient-normalization mismatch"));
  if (red433[1] != 1 || abs(v[433]) != 1, error("bad-prime 433 mismatch"));
  if (red29023[1] != 2 || v[29023] != 0, error("bad-prime 29023 mismatch"));
  my(out = fileopen("millennium-prize/birch-swinnerton-dyer/cycle194_D-29023_coefficients.csv", "w"));

  filewrite(out, "n,a_n");
  for (n = 1, M, filewrite(out, Str(n, ",", v[n])));
  fileclose(out);

  out = fileopen("millennium-prize/birch-swinnerton-dyer/cycle194_D-29023_metadata.txt", "w");
  filewrite(out, Str("producer=PARI/GP ", version()));
  filewrite(out, "base_curve=433a1");
  filewrite(out, Str("twist_D=", D));
  filewrite(out, Str("minimal_model=", model));
  filewrite(out, Str("conductor=", conductor));
  filewrite(out, Str("root_number=", root_number));
  filewrite(out, "bad_prime_433_reduction=multiplicative");
  filewrite(out, Str("a_433=", v[433]));
  filewrite(out, "bad_prime_29023_reduction=additive");
  filewrite(out, Str("a_29023=", v[29023]));
  filewrite(out, Str("coefficient_count=", M));
  filewrite(out, "coefficient_method=ellan");
  fileclose(out);

  print("coefficient_count=", M);
  print("minimal_model=", model);
  print("conductor=", conductor);
  print("root_number=", root_number);
};

main();
