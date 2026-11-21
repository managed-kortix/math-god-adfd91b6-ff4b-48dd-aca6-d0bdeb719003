#!/usr/bin/env python3
"""Exact rational-interval check of the auxiliary uniform-certificate obstruction.

Graph: a central K_{1,3}; two disjoint C5 arms are joined by bridges from the
center of K_{1,3} to one vertex of each cycle.  The script uses only Fraction
arithmetic.  Positive parts are enclosed through rational eigenvalue intervals
and exact spectral-projector formulas, using interval matrix arithmetic.
"""
from fractions import Fraction as F


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[1],a[1]-b[0])
def mul(a,b):
    z=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]); return (min(z),max(z))
def inv(a):
    require(not (a[0] <= 0 <= a[1]), "attempted inversion of an interval containing zero")
    return (1/a[1],1/a[0])
def div(a,b): return mul(a,inv(b))
def sq(a):
    if a[0] <= 0 <= a[1]: return (F(0),max(a[0]*a[0],a[1]*a[1]))
    z=(a[0]*a[0],a[1]*a[1]); return (min(z),max(z))
def pt(x): return (F(x),F(x))

def mm(A,B):
    n=len(A);m=len(B[0]);r=len(B)
    return [[sum_iv(mul(A[i][k],B[k][j]) for k in range(r)) for j in range(m)] for i in range(n)]
def sum_iv(xs):
    z=pt(0)
    for x in xs:z=add(z,x)
    return z
def eye(n): return [[pt(1 if i==j else 0) for j in range(n)] for i in range(n)]
def scalar_shift(M,l):
    n=len(M);return [[sub(pt(M[i][j]),l) if i==j else pt(M[i][j]) for j in range(n)] for i in range(n)]
def matscale(M,a): return [[mul(x,a) for x in row] for row in M]
def matadd(A,B):return [[add(A[i][j],B[i][j]) for j in range(len(A))] for i in range(len(A))]

def projector(M,lam,others):
    P=eye(len(M));den=pt(1)
    for mu in others:
        P=mm(P,scalar_shift(M,mu));den=mul(den,sub(lam,mu))
    return matscale(P,inv(den))

def pospart(M,positive,allroots):
    Z=[[pt(0) for _ in M] for _ in M]
    for lam in positive:
        others=list(allroots);others.remove(lam)
        Z=matadd(Z,matscale(projector(M,lam,others),lam))
    return Z

def matrix(edges,n):
    A=[[0]*n for _ in range(n)]
    for i,j in edges:A[i][j]=A[j][i]=1
    return A

def embed(P,I,n):
    Z=[[pt(0) for _ in range(n)] for _ in range(n)]
    for a,i in enumerate(I):
        for b,j in enumerate(I):Z[i][j]=P[a][b]
    return Z

def phi_interval(positive):return sum_iv([sq(x) for x in positive])

# Vertex order: central leaves 0,1,2; center 3; cycles 4..8 and 9..13.
edges=[(0,3),(1,3),(2,3)]
for o in (4,9):
    edges += [(o+i,o+(i+1)%5) for i in range(5)] + [(3,o)]
A=matrix(edges,14)
U1=list(range(4,9));U2=list(range(9,14));R1=[i for i in range(14) if i not in U1];R2=[i for i in range(14) if i not in U2]
def principal(I):return [[A[i][j] for j in I] for i in I]

# Rational isolating intervals.  Their signs and uniqueness are checked below.
s5=(F(2236067,1000000),F(2236068,1000000))
a=div(sub(s5,pt(1)),pt(2)); mphi=mul(pt(-1),div(add(s5,pt(1)),pt(2)))
r13=(F(2302775,1000000),F(2302776,1000000)); m13=(F(-1302776,1000000),F(-1302775,1000000))
c0=(F(-2214320,1000000),F(-2214319,1000000))
c1=(F(539188,1000000),F(539189,1000000))
c2=(F(1675130,1000000),F(1675131,1000000))
rootsU=[pt(2),a,a,mphi,mphi]  # multiplicities prevent projector use; C5 formula below
# C5 positive part is polynomial p(C) interpolating values at its three distinct eigenvalues.
C=principal(U1)
# p(x)=alpha*x^2+beta*x+gamma, solved exactly over intervals by Lagrange projectors.
distinct=[pt(2),a,mphi]
PU=pospart(C,[pt(2),a],distinct)
rootsR=[pt(0),pt(0),m13,r13,mphi,a,c0,c1,c2]
# Zero is repeated; remove its nullspace factor by using distinct eigenvalues only: spectral
# projectors depend on the distinct minimal-polynomial roots.
distR=[pt(0),m13,r13,mphi,a,c0,c1,c2]
PR=pospart(principal(R1),[r13,a,c1,c2],distR)
X1=matadd(embed(PU,U1,14),embed(PR,R1,14))
# Swap the two cycles to obtain X2.
perm={i:i for i in range(14)}
for i in range(5):perm[4+i]=9+i;perm[9+i]=4+i
X2=[[X1[perm[i]][perm[j]] for j in range(14)] for i in range(14)]
V=matscale([[sq(sub(X1[i][j],X2[i][j])) for j in range(14)] for i in range(14)],pt(F(1,4)))
Vsum=sum_iv(x for row in V for x in row)
phiU=add(sq(pt(2)),mul(pt(2),sq(a)))
phiR=phi_interval([r13,a,c1,c2])
base=sub(add(phiU,phiR),pt(14))
cert=add(base,Vsum)

# Root/sign checks for all nonquadratic isolating intervals.
def p3(t):return t*t*t-4*t+2
for I in (c0,c1,c2):
    require(p3(I[0])*p3(I[1])<0, "cubic interval does not bracket a root")
# The intervals are disjoint and cubic derivative has fixed sign on each; hence unique.
# p' = 3x^2-4: fixed signs on c0,c1,c2 using rational square checks.
require(3*c0[1]*c0[1] > 4, "left cubic interval is not monotone")
require(3*c1[1]*c1[1] < 4, "middle cubic interval is not monotone")
require(3*c2[0]*c2[0] > 4, "right cubic interval is not monotone")
require(s5[0]*s5[0] < 5 < s5[1]*s5[1], "sqrt(5) interval is invalid")
require(r13[0]*r13[0]-r13[0]-3 < 0 < r13[1]*r13[1]-r13[1]-3,
        "positive quadratic-root interval is invalid")

def outward_decimal(I, digits=12):
    scale=10**digits
    lo=I[0].numerator*scale//I[0].denominator
    hi=-((-I[1].numerator*scale)//I[1].denominator)
    return f"[{lo/scale:.{digits}f}, {hi/scale:.{digits}f}]"
print("base interval:",outward_decimal(base))
print("variance interval:",outward_decimal(Vsum))
print("uniform certificate interval:",outward_decimal(cert))
require(cert[1] < 0, "certificate upper bound is not negative")
require(cert[1] < F(-64,1000), "certificate upper bound is not below -8/125")
print("exact comparison: certificate upper bound < -8/125")
print("PASS: exact rational interval upper bound is negative")
