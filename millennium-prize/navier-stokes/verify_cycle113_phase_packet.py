#!/usr/bin/env python3
"""Exact full-Fourier verifier for the Cycle 113 packet (stdlib only)."""
from fractions import Fraction as F

def z(a=0,b=0): return (F(a),F(b))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,c): return (a[0]*c,a[1]*c)
def conj(a): return (a[0],-a[1])
def V(*x): return tuple(z(a,b) for a,b in x)
def va(a,b): return tuple(add(x,y) for x,y in zip(a,b))
def vs(a,c): return tuple(scale(x,c) for x in a)
def vd(a,b):
    out=z()
    for x,y in zip(a,b): out=add(out,mul(x,y))
    return out
def vc(a): return tuple(conj(x) for x in a)
def norm2(a): return sum((mul(conj(x),x)[0] for x in a),F(0))
def kn(k): return sum(x*x for x in k)

def project(k,v):
    kv=z()
    for x,y in zip(k,v): kv=add(kv,scale(y,x))
    return tuple(add(y,neg(scale(kv,F(x,kn(k))))) for x,y in zip(k,v))

def Q(a,b):
    """Bilinear Euler convolution: -i P_n sum_(r+s=n) (a_r.s)b_s."""
    out={}
    for r,ar in a.items():
      for s,bs in b.items():
        n=tuple(x+y for x,y in zip(r,s))
        if n==(0,0,0): continue
        ars=z()
        for x,y in zip(ar,s): ars=add(ars,scale(x,y))
        term=project(n,tuple(mul(z(0,-1),mul(ars,x)) for x in bs))
        out[n]=va(out.get(n,V((0,0),(0,0),(0,0))),term)
    return {k:v for k,v in out.items() if norm2(v)}

k=(1,0,0); p=(0,1,0); q=(1,1,0)
u={k:V((0,0),(1,0),(1,0)), p:V((1,0),(0,0),(1,0)),
   q:V((0,-1),(0,1),(0,-1))}
for n,v in list(u.items()): u[tuple(-x for x in n)]=vc(v)
du=Q(u,u)
a=Q(du,u)
for n,v in Q(u,du).items(): a[n]=va(a.get(n,V((0,0),(0,0),(0,0))),v)

assert du[k]==V((0,0),(1,0),(-2,0))
assert du[p]==V((-1,0),(0,0),(0,0))
assert du[q]==V((0,0),(0,0),(0,-2))
leak=set(du)-set(u)
assert leak=={(1,2,0),(2,1,0),(-1,-2,0),(-2,-1,0)}
assert sum((norm2(du[n]) for n in leak),F(0))==F(44,5)
stretch=sum((F(kn(n))*vd(vc(v),du[n])[0] for n,v in u.items()),F(0))
assert stretch==4
assert a[k]==V((0,0),(-F(2,5),0),(-F(16,5),0))
assert a[p]==V((-F(2,5),0),(0,0),(-F(24,5),0))
assert a[q]==V((0,F(4,5)),(0,-F(4,5)),(0,4))

# Taylor-polynomial arithmetic through t^2, coefficients not derivatives.
def padd(x,y):
    return [add(x[i] if i<len(x) else z(),y[i] if i<len(y) else z()) for i in range(max(len(x),len(y)))]
def pmul(x,y):
    o=[z(),z(),z()]
    for i,a0 in enumerate(x):
      for j,b0 in enumerate(y):
        if i+j<3:o[i+j]=add(o[i+j],mul(a0,b0))
    return o
def vjet(n): return [[u[n][j],du[n][j],scale(a[n][j],F(1,2))] for j in range(3)]
uk,up,uq=vjet(k),vjet(p),vjet(q)
def dotk(v,n):
    o=[z(),z(),z()]
    for j,c in enumerate(n): o=padd(o,[scale(x,c) for x in v[j]])
    return o
kp,pk=dotk(uk,p),dotk(up,k)
W=[padd(pmul(kp,up[j]),pmul(pk,uk[j])) for j in range(3)]
Xi=[z(),z(),z()]
for j in range(3): Xi=padd(Xi,pmul([conj(x) for x in uq[j]],W[j]))
assert Xi==[z(0,2),z(0,2),z(0,-F(52,5))]
print("stretching = 4")
print("leakage velocity squared = 44/5")
print("Xi(t) = 2i + 2i t - (52/5)i t^2 + O(t^3)")
print("all exact checks passed")
