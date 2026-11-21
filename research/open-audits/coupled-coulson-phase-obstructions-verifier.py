#!/usr/bin/env python3
"""Dependency-free exact checks for coupled-Coulson route obstructions."""
from fractions import Fraction as Q

def require(condition,message="verification failed"):
    if not condition:
        raise AssertionError(message)

def trim(p):
    while len(p)>1 and p[-1]==0:p.pop()
    return p

def add(a,b):
    c=[Q(0)]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    return trim(c)
def neg(a):return [-x for x in a]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def deriv(a):return [Q(i)*a[i] for i in range(1,len(a))] or [Q(0)]
def divmodp(a,b):
    a=a[:];q=[Q(0)]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and a!=[0]:
        k=len(a)-len(b);z=a[-1]/b[-1];q[k]=z
        for j,x in enumerate(b):a[j+k]-=z*x
        trim(a)
    return trim(q),trim(a)
def sturm(p):
    s=[trim(p),deriv(p)]
    while s[-1]!=[0]:
        _,r=divmodp(s[-2],s[-1]);r=neg(r)
        if r==[0]:break
        s.append(r)
    return s
def signat(p,x):
    v=sum(c*x**i for i,c in enumerate(p));return (v>0)-(v<0)
def variations(vals):
    vals=[x for x in vals if x]
    return sum(vals[i]!=vals[i-1] for i in range(1,len(vals)))
def roots_between(p,a,b):
    s=sturm(p)
    return variations([signat(x,a) for x in s])-variations([signat(x,b) for x in s])
def at_i(high):
    n=len(high)-1;re=[Q(0)]*(n+1);im=[Q(0)]*(n+1)
    powers=((1,0),(0,1),(-1,0),(0,-1))
    for j,c in enumerate(high):
        k=n-j;a,b=powers[k%4];re[k]=Q(c)*a;im[k]=Q(c)*b
    return trim(re),trim(im)
def cmul(x,y):
    return sub(mul(x[0],y[0]),mul(x[1],y[1])),add(mul(x[0],y[1]),mul(x[1],y[0]))
def cconj(x):return x[0],neg(x[1])
def factor_polynomials(chiR,minorR):
    chiU=[1,0,-5,0,5,-2];minorU=[1,0,-3,0,1]
    den=cmul(at_i(chiR),at_i(chiU));prod=cmul(at_i(minorR),at_i(minorU))
    num=sub(den[0],prod[0]),sub(den[1],prod[1])
    return cmul(num,cconj(den))


def connected_without(n,edges,skip=None):
    adj=[[] for _ in range(n)]
    for k,(u,v) in enumerate(edges):
        if k==skip:continue
        adj[u].append(v);adj[v].append(u)
    seen={0};stack=[0]
    while stack:
        u=stack.pop()
        for v in adj[u]:
            if v not in seen:seen.add(v);stack.append(v)
    return len(seen)==n

def matmul(a,b):
    n=len(a);m=len(b);r=len(b[0])
    return [[sum(a[i][k]*b[k][j] for k in range(m)) for j in range(r)] for i in range(n)]

def charpoly_graph(n,edges,deleted=None):
    vs=[v for v in range(n) if v!=deleted];idx={v:i for i,v in enumerate(vs)}
    A=[[0]*len(vs) for _ in vs]
    for u,v in edges:
        if u in idx and v in idx:A[idx[u]][idx[v]]=A[idx[v]][idx[u]]=1
    power=[row[:] for row in A];traces=[]
    for k in range(1,len(vs)+1):
        traces.append(sum(power[i][i] for i in range(len(vs))))
        if k<len(vs):power=matmul(power,A)
    # Newton/Faddeev--LeVerrier coefficients, highest degree first.
    c=[Q(1)]
    for k in range(1,len(vs)+1):
        value=-sum(c[k-j]*traces[j-1] for j in range(1,k+1))/k
        require(value.denominator==1);c.append(value)
    return [int(x) for x in c]

def inertia(poly):
    low=list(map(Q,reversed(poly)));zeros=0
    while zeros<len(low)-1 and low[zeros]==0:zeros+=1
    reduced=low[zeros:]
    # Count roots with multiplicity by successive gcds with the derivative.
    pos=negc=0;p=reduced
    while len(p)>1:
        sf=divmodp(p, polynomial_gcd(p,deriv(p)))[0]
        pos+=roots_between(sf,Q(0),Q(20));negc+=roots_between(sf,Q(-20),Q(0))
        p=polynomial_gcd(p,deriv(p))
    return pos,negc,zeros

def polynomial_gcd(a,b):
    a=a[:];b=b[:]
    while b!=[0]:
        _,r=divmodp(a,b);a,b=b,r
    if a==[0]:return a
    lead=a[-1];return [x/lead for x in a]

def audit_structure(name,edges,mark,bridges,chi,minor,gchi,want_inertias):
    require(len(edges)==12 and len({tuple(sorted(e)) for e in edges})==12)
    require(connected_without(7,edges))
    found={tuple(sorted(edges[k])) for k in range(12) if not connected_without(7,edges,k)}
    require(found=={tuple(sorted(e)) for e in bridges})
    require(charpoly_graph(7,edges)==chi)
    require(charpoly_graph(7,edges,mark)==minor)
    c5=[(7+i,7+(i+1)%5) for i in range(5)]
    require(charpoly_graph(12,edges+[(mark,7)]+c5)==gchi)
    got=(inertia(chi),inertia([1,0,-5,0,5,-2]),inertia(gchi))
    require(got==want_inertias)
    print(name+' structure/charpoly/inertia: PASS')

def check(name,chi,minor,re_expected,im_expected,re_roots,im_roots):
    re,im=factor_polynomials(chi,minor)
    require(re==list(map(Q,re_expected)));require(im==list(map(Q,im_expected)))
    require(roots_between(re,Q(0),Q(100))==re_roots)
    # remove the forced t factor before counting positive roots
    imred=im[1:]
    require(roots_between(imred,Q(0),Q(100))==im_roots)
    print(name+': PASS')

audit_structure('sign-changing correction',
 [(2,5),(1,6),(0,5),(1,5),(1,2),(0,3),(2,6),(0,4),(3,4),(1,4),(3,6),(0,1)],3,[],
 [1,0,-12,-10,23,20,-9,-6],[1,0,-9,-8,9,8,-1],
 [1,0,-18,-10,100,76,-221,-164,217,116,-97,-20,13],
 ((3,4,0),(3,2,0),(6,6,0)))
audit_structure('nonprincipal endpoint branch',
 [(1,2),(1,3),(3,6),(0,3),(0,4),(1,6),(5,6),(0,2),(3,5),(2,3),(1,5),(0,1)],4,[(0,4)],
 [1,0,-12,-16,11,26,8,-2],[1,0,-11,-16,3,16,7],
 [1,0,-18,-16,90,120,-144,-252,60,182,6,-42,-3],
 ((3,4,0),(3,2,0),(5,7,0)))
check('sign-changing correction',
 [1,0,-12,-10,23,20,-9,-6],[1,0,-9,-8,9,8,-1],
 [156,0,2509,0,16261,0,55301,0,109397,0,133421,0,104148,0,53087,0,17706,0,3789,0,494,0,35,0,1],
 [0,-84,0,-836,0,-2960,0,-4844,0,-4070,0,-1740,0,-286,0,38,0,20,0,2],0,1)
check('nonprincipal endpoint branch',
 [1,0,-12,-16,11,26,8,-2],[1,0,-11,-16,3,16,7],
 [-12,0,1032,0,9715,0,36617,0,75478,0,95385,0,77881,0,41966,0,14905,0,3405,0,472,0,35,0,1],
 [0,-246,0,-1742,0,-4878,0,-7168,0,-6074,0,-3038,0,-874,0,-132,0,-8],1,0)
print('ALL PASS')
