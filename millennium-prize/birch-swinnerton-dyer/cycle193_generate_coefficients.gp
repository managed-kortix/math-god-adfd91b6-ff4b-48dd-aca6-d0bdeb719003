default(parisizemax, 512000000);

main() =
{
  my(M = 100000);
  my(E = ellinit(elltwist(ellinit("433a1"), -1499)));
  if (ellglobalred(E)[1] != 972951433, error("conductor mismatch"));
  if (ellrootno(E) != -1, error("root-number mismatch"));
  my(v = ellan(E, M));
  if (v[1] != 1, error("ellan normalization or indexing mismatch"));
  if (abs(v[433]) != 1, error("multiplicative bad-prime coefficient mismatch"));
  if (v[1499] != 0, error("additive bad-prime coefficient mismatch"));
  my(out = fileopen("millennium-prize/birch-swinnerton-dyer/cycle193_D-1499_coefficients.csv", "w"));

  filewrite(out, "n,a_n");
  for (n = 1, M, filewrite(out, Str(n, ",", v[n])));
  fileclose(out);
  print("coefficient_count=", M);
  print("conductor=", ellglobalred(E)[1]);
};

main();
