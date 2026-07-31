#!/usr/bin/env python3
"""Exact PEL and exterior-algebra certificate for the Cycle 151 seed."""

from fractions import Fraction


def transpose(a): return [list(row) for row in zip(*a)]
def matmul(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in transpose(b)] for r in a]
def determinant(a):
    a=[r[:] for r in a]; n=len(a); sign=1; prev=1
    for k in range(n-1):
        if a[k][k]==0:
            r=next((r for r in range(k+1,n) if a[r][k]),None)
            if r is None: return 0
            a[k],a[r]=a[r],a[k]; sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                num=a[i][j]*pivot-a[i][k]*a[k][j]
                assert num%prev==0; a[i][j]=num//prev
            a[i][k]=0
        prev=pivot
    return sign*a[-1][-1]


names=[x for j in range(1,7) for x in (f"dz{j}",f"dbar{j}")]
idx={x:i for i,x in enumerate(names)}
def gen(x): return {1<<idx[x]:1}
def add(*fs):
    o={}
    for f in fs:
        for m,c in f.items():
            o[m]=o.get(m,0)+c
            if not o[m]: del o[m]
    return o
def scale(c,f): return {m:c*v for m,v in f.items() if c*v}
def wedge(a,b):
    o={}
    for ma,ca in a.items():
      for mb,cb in b.items():
        if ma&mb: continue
        crossings=sum((ma>>(i+1)).bit_count() for i in range(12) if mb>>i&1)
        m=ma|mb; o[m]=o.get(m,0)+(-1 if crossings&1 else 1)*ca*cb
    return {m:c for m,c in o.items() if c}
def coeff(f,order):
    inds=[idx[x] for x in order]; mask=sum(1<<i for i in inds)
    inv=sum(inds[i]>inds[j] for i in range(len(inds)) for j in range(i+1,len(inds)))
    return (-1 if inv&1 else 1)*f.get(mask,0)


def main():
    weights=[1,1,1,-1,-1,-3]
    assert determinant([[weights[i] if i==j else 0 for j in range(6)] for i in range(6)])==-3
    eps=[[0,1],[-1,0]]; D=[1,1,1,1,1,3]
    E=[[0]*12 for _ in range(12)]
    for k,d in enumerate(D):
        for i in range(2):
            for j in range(2): E[2*k+i][2*k+j]=d*eps[i][j]
    assert determinant(E)==9 and transpose(E)==[[-x for x in r] for r in E]
    # 3 is inert in Q(i), so odd v_3 certifies nonsplit signed determinant.
    assert all((x*x+1)%3 for x in range(3))

    graph={0:1}
    for j in range(1,4):
        graph=wedge(graph,wedge(add(gen(f"dz{j}"),scale(-1,gen(f"dz{j+3}"))),
                                add(gen(f"dbar{j}"),scale(-1,gen(f"dbar{j+3}")))))
    W=["dz1","dz2","dz3","dbar4","dbar5","dbar6"]
    Wb=["dbar1","dbar2","dbar3","dz4","dz5","dz6"]
    assert coeff(graph,W)==1 and coeff(graph,Wb)==-1
    # Each real graph factor is (i/2) times its complex-basis factor.
    normalization=(Fraction(0,1),Fraction(-1,8))
    normalized_W=(normalization[0]*coeff(graph,W),normalization[1]*coeff(graph,W))
    normalized_Wb=(normalization[0]*coeff(graph,Wb),normalization[1]*coeff(graph,Wb))
    assert normalized_W==(0,Fraction(-1,8))
    assert normalized_Wb==(0,Fraction(1,8))
    print("Cycle 151 nonsplit diagonal seed")
    print("Hermitian determinant = -3; alternating determinant = 9")
    print("polarization type = (1,1,1,1,1,3); signature = (3,3)")
    print("diagonal W^6 coefficient = 1; conjugate coefficient = -1")
    print("normalized coefficients = -i/8, +i/8")
    print("all exact checks passed")


if __name__=="__main__": main()
