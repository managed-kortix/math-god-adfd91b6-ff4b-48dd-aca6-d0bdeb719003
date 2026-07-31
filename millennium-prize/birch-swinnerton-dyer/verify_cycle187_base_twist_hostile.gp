\\ Hostile exact validation of Cycle 187 against direct twist msfromell.
default(parisizemax, 4000000000);

E = ellinit([1,0,0,0,1]);
[M, xpm] = msfromell(E);
xp = xpm[1];
xm = xpm[2];

validate(q) =
{
  my(D = if(q % 4 == 1, q, -q));
  my(Eraw = elltwist(E, D), change, Eq);
  my(Mq, xq, eps = kronecker(-1,q), xb);
  my(direct, translated_plus, translated_minus, cycle187, corrected);
  my(c_direct = 0, c_cycle187 = 0, c_minus = 0, c_paired = 0, j);

  Eq = ellminimalmodel(Eraw, &change);
  if (change[1] != 1, error("unexpected differential factor at q=", q));
  if (ellglobalred(Eq)[1] != 433*q^2,
    error("unexpected twist conductor at q=", q));
  [Mq, xq] = msfromell(Eq, 1);
  xb = if(eps == 1, xp, xm);

  print("BEGIN q=", q, " D=", D, " model=", Eq[1..5],
        " change=", change, " conductor=", ellglobalred(Eq)[1]);
  for(a = 1, 28,
    direct = mseval(Mq, xq, [oo, a/29]);
    translated_plus = sum(u = 1, q-1,
      kronecker(u,q) * mseval(M, xb,
        [oo, (a*q + 29*u)/(29*q)]));
    translated_minus = sum(u = 1, q-1,
      kronecker(u,q) * mseval(M, xb,
        [oo, (a*q - 29*u)/(29*q)]));
    cycle187 = translated_plus;
    corrected = cycle187;
    j = znlog(Mod(a,29), Mod(2,29));
    c_direct += j * direct;
    c_cycle187 += j * cycle187;
    c_minus += j * translated_minus;
    print("ROW q=", q, " a=", a, " direct=", direct,
          " plus=", translated_plus, " minus=", translated_minus,
          " cycle187=", cycle187, " corrected=", corrected);
    if (direct != corrected,
      error("Cycle 187 formula mismatch at q=", q, ", a=", a));
    if (translated_minus != eps * direct,
      error("translation-sign audit mismatch at q=", q, ", a=", a));
  );
  for(a = 1, 14,
    j = znlog(Mod(a,29), Mod(2,29));
    c_paired += 2*j*sum(u = 1, q-1,
      kronecker(u,q) * mseval(M, xb,
        [oo, (a*q + 29*u)/(29*q)]));
  );
  print("C q=", q, " direct=", c_direct, " cycle187=", c_cycle187,
        " minus_translation=", c_minus, " paired=", c_paired,
        " mod7=", lift(Mod(c_direct,7)));
  if (c_direct != c_cycle187 || c_minus != eps*c_direct,
    error("Kurihara-sum mismatch at q=", q));
  if (Mod(c_paired,7) != Mod(c_direct,7),
    error("paired formula mismatch at q=", q));
  print("PASS q=", q, " rows=28 kappa=1 translation_sign=chi_q(-1)=", eps);
};

validate(3);
validate(5);
print("PASS all 56 direct-symbol comparisons");
