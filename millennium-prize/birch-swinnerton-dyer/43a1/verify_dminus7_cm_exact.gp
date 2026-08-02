\\ Exact formal-q and elimination certificate for the D=-7 CM image on 43a1.
\\ Run with: gp -fq verify_dminus7_cm_exact.gp

default(parisize, "512M");

E = ellinit([0, 1, 1, 0, 0]);
if (qfbclassno(-7) != 1, error("D=-7 does not have class number one"));
if (polclass(-7) != x + 3375, error("unexpected Hilbert class polynomial"));
if (37^2 + 7 != 4 * 43 * 8, error("Heegner quadratic-form identity failed"));
if (qfbred(Qfb(43, 37, 8)) != qfbred(Qfb(1, 37, 344)), error("tau and 43*tau do not give the same D=-7 ideal class"));
if (ellmoddegree(E) != 2, error("unexpected modular degree"));
if (elltors(E)[1] != 1, error("nontrivial rational torsion leaves a Fricke translation ambiguity"));
prec = 170;
XY = elltaniyama(E, prec);
X = XY[1];
Y = XY[2];
if (valuation(X) != -2 || pollead(X) != 1, error("unexpected X normalization at infinity"));
if (valuation(Y) != -3 || pollead(Y) != -1, error("unexpected Y normalization at infinity"));
if (valuation(Y^2 + Y - X^3 - X^2) < 120, error("Taniyama series do not satisfy the stated model deeply enough"));

\\ Fix both the Fricke sign and the sign of the parametrization.  The latter
\\ equality is pi^*(dx/(2y+1)) = f(q)dq/q, not merely equality up to sign.
mf = mfinit([43, 2], 0);
forms = mfeigenbasis(mf);
pullback = x * deriv(X) / (2 * Y + 1);
form_index = 0;
for (i = 1, #forms, if (mfcoefs(forms[i], 20) == vector(21, n, polcoef(pullback, n - 1)), if (form_index, error("newform normalization is not unique"), form_index = i)));
if (!form_index, error("no normalized newform matches the Taniyama differential"));
f = forms[form_index];
fcoefs = mfcoefs(f, 100);
for (n = 0, 100, if (polcoef(pullback, n) != fcoefs[n + 1], error("Taniyama parametrization/newform normalization mismatch")));
fricke = mfatkin(mfatkininit(mf, 43), f);
if (mfcoefs(fricke, 100) != fcoefs, error("the 43a1 newform does not have Fricke eigenvalue +1"));

E4 = Ser(mfcoefs(mfEk(4), prec + 60));
Delta = Ser(mfcoefs(mfDelta(), prec + 60));
j = E4^3 / Delta;
j43 = subst(j, x, x^43);

\\ Riemann--Roch bases at O. Here ord_O(X)=-2 and ord_O(Y)=-3.
basisS = vector(43);
basisS[1] = 1;
for (i = 1, 21, basisS[1 + i] = X^i);
for (i = 0, 20, basisS[23 + i] = X^i * Y);

basisR = vector(44);
basisR[1] = 1;
for (i = 1, 22, basisR[1 + i] = X^i);
for (i = 0, 20, basisR[24 + i] = X^i * Y);

fit(series, basis, lo, hi) =
{
  my(M, v, c);
  M = matrix(hi - lo + 1, #basis, r, s,
             polcoef(basis[s], lo + r - 1));
  v = vector(hi - lo + 1, r, polcoef(series, lo + r - 1))~;
  if (matrank(M) != #basis, error("Riemann--Roch interpolation rank failure"));
  c = matsolve(M, v);
  if (M * c != v, error("formal-q interpolation residual is nonzero"));
  c;
};

\\ Interpolate only through the constant term, then make the identity proof
\\ independent of those equations by checking m further positive coefficients.
cS = fit(j + j43, basisS, -43, 0);
cR = fit(j * j43, basisR, -44, 0);

check_identity(series, basis, coeffs, m) =
{
  my(d = series - sum(i = 1, #basis, coeffs[i] * basis[i]));
  if (serprec(d, x) <= m, error("insufficient formal-q precision for uniqueness"));
  for (n = -m, m, if (polcoef(d, n) != 0, error(Str("formal-q identity check failed at exponent ", n))));
  if (valuation(d) <= m, error("Riemann--Roch uniqueness threshold was not exceeded"));
};

check_identity(j + j43, basisS, cS, 43);
check_identity(j * j43, basisR, cR, 44);

AS = sum(i = 1, 22, cS[i] * x^(i - 1));
BS = sum(i = 23, 43, cS[i] * x^(i - 23));
AR = sum(i = 1, 23, cR[i] * x^(i - 1));
BR = sum(i = 24, 44, cR[i] * x^(i - 24));

if (subst(AS, x, 0) != -6750, error("CM trace does not hold at P"));
if (subst(AR, x, 0) != 3375^2, error("CM norm does not hold at P"));

curve = y^2 + y - x^3 - x^2;
eqS = AS + BS * y + 6750;
eqR = AR + BR * y - 3375^2;

resS = polresultant(curve, eqS, y);
resR = polresultant(curve, eqR, y);
resSR = polresultant(eqS, eqR, y);
if (resS == 0 || resR == 0 || resSR == 0, error("degenerate zero resultant"));
common = gcd(gcd(resS, resR), resSR);
common /= pollead(common);
if (common != x, error("CM fiber is not supported only at x=0"));

\\ At x=0 the curve gives y(y+1)=0. The trace equation separates the
\\ two points because BS(0)=-22750 is nonzero: only y=0 survives.
if (subst(BS, x, 0) != -22750, error("fiber-separation coefficient changed"));
if (subst(subst(eqS, x, 0), y, 0) != 0, error("P does not satisfy trace"));
if (subst(subst(eqS, x, 0), y, -1) == 0, error("-P also satisfies trace"));

print("MODEL=y^2+y=x^3+x^2");
print("MODULAR_DEGREE=", ellmoddegree(E));
print("FRICKE_EIGENVALUE=+1");
print("PARAMETRIZATION_DIFFERENTIAL_SIGN=+1");
print("CM_POLYNOMIAL=T+3375");
print("CM_43_CLASS_IDENTITY=1");
print("TRACE_AT_P=-6750");
print("NORM_AT_P=11390625");
print("IDENTITY_CHECKS=S:43,R:44");
print("COMMON_X_RESULTANT=", common);
print("UNIQUE_CM_FIBER_POINT=(0,0)");
print("FORMAL_Q_CERTIFICATE_PASSED=1");
