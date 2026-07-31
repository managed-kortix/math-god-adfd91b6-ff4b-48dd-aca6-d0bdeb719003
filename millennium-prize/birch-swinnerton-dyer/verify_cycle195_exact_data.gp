default(parisizemax, 512000000);

main() =
{
  my(model = [1, 0, 1, -46813, -3372156843]);
  my(P = [399030891253207/156180668809,
          7009131418974188521075/61722131771310373]);
  my(E = ellinit(model), red, tors, h);

  if (!ellisoncurve(E, P), error("exact point check failed"));
  red = ellglobalred(E);
  if (red[1] != 972951433, error("conductor mismatch"));
  if (red[3] != 2, error("Tamagawa product mismatch"));
  if (elllocalred(E, 433) != [1, 5, [1, 0, 0, 0], 1],
      error("local data mismatch at 433"));
  if (elllocalred(E, 1499) != [2, -1, [1, 0, 0, 0], 2],
      error("local data mismatch at 1499"));
  tors = elltors(E);
  if (tors != [1, [], []], error("torsion mismatch"));
  if (ellrootno(E) != -1, error("root number mismatch"));

  default(realprecision, 100);
  h = ellheight(E, P);
  if (h < 33.96338096796685137401217818912911624353760513342938 ||
      h > 33.96338096796685137401217818912911624353760513342940,
      error("height reference mismatch"));

  print("model=", model);
  print("point=", P);
  print("discriminant=", E.disc);
  print("conductor=", red[1]);
  print("torsion=", tors);
  print("root_number=", ellrootno(E));
  print("local_433=", elllocalred(E, 433));
  print("local_1499=", elllocalred(E, 1499));
  print("tamagawa_product=", red[3]);
  print("pari_height_reference=", h);
  print("certificate_status=PASS");
};

main();
