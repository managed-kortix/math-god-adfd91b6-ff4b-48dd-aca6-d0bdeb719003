\\ Independent PARI/GP certificate for the C5--Cq analytic tail algebra.

fail(s)=error(Str("FAIL ",s));
check(b,s)=if(!b,fail(s));

z='z; c='c;
A=z^8-z^7-2*z^6+2*z^5-z^4+z-1;
B=z^8-z^7+z^4-2*z^3+2*z^2+z-1;

\\ Laurent numerator identities for the nine-term Chebyshev-U factor.
P8=z^8-2*z^7-z^6+4*z^5-3*z^4+z^3+z-2+z^-1;
Q1=1-2*z-z^2+4*z^3-3*z^4+z^5+z^7-2*z^8+z^9;
check(z*P8==(z-1)*A,"Laurent P identity");
check(Q1==(z-1)*B,"Laurent Q identity");
check(B+z^8*subst(A,z,1/z)==0,"unit-circle reciprocal identity");

\\ Exactly one A-root above one, bracketed beyond 5/3; B positive there.
check(polsturm(A,1,+oo)==1,"unique A root >1");
check(subst(A,z,5/3)<0 && subst(A,z,17/10)>0,"A root bracket");
shiftB=subst(B,z,z+1);
check(vecmin(Vec(shiftB))>0,"B(1+t) positive coefficients");

\\ Rational phase derivative and its exact Sturm bounds.
N=-4*(c-1)*(32*c^5-24*c^3+2*c+5);
D=256*c^8-256*c^7-576*c^6+576*c^5+384*c^4-400*c^3-60*c^2+92*c-17;
check(polsturm(D,-1,1)==0 && subst(D,c,0)<0,"D<0");
check(polsturm(N-10*D,-1,1)==0 && subst(N-10*D,c,0)>0,"delta prime upper");
check(polsturm(N+10*D,-1,1)==0 && subst(N+10*D,c,0)<0,"delta prime lower");
R=(1-c^2)*(deriv(N,c)*D-N*deriv(D,c))^2-3600*D^4;
check(polsturm(R,-1,1)==0 && subst(R,c,0)<0,"delta second bound");

\\ Degree-10 majorant used for positivity of the limiting phase integral.
V=[-1176,932897,-18738928,160421290,-784298040,2400555593,-4738265457,6012185972,-4728030260,2094110383,-398872274];
PP=sum(k=0,10,V[k+1]/1000*c^k);
E=PP*D-N;
qr=divrem(E,c-1); check(qr[2]==0,"phase majorant endpoint factor"); Ered=qr[1];
check(polsturm(Ered,0,1)==0 && subst(E,c,0)<0,"phase majorant");
phase_upper=7623356367059/433125-(1434244074019/256000)*(355/113);
check(phase_upper<0,"positive phase integral using pi<355/113");

\\ Exact q=727 worst-case tail constants; monotonicity is elementary from
\\ positive inverse powers of a=q/2-10.
a=707/2; p=22/7;
M=8*p^2/a^2+240*p^2/a^3;
err=(2*a+27)*M/96+M/162;
check(err==7362936152/1402617781467 && err<1/100,"quadrature error");
margin=(34/15)^2+2-(161/72+9/2);
check((161/72)^2>5 && margin==241/600 && margin>err,"energy margin");

print("PASS independent PARI C5--Cq tail certificate");
print("quadrature_error=",err);
print("remaining_margin=",margin-err);
quit;
