#!/usr/bin/env python3
"""Exact mirror-free designated Euler cascade in Z^3."""

from fractions import Fraction as F


def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def scale(c,a): return tuple(c*x for x in a)
def dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))
def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm2(a): return dot(a,a)
def rotate(a): return (a[2],a[0],a[1])
def project(k,v): return sub(v,scale(dot(k,v)/norm2(k),k))


def outputs(q,p,a,b):
    alpha=dot(a,p); beta=dot(b,q)
    intended=project(add(q,p),add(scale(alpha,b),scale(beta,a)))
    mirror=project(sub(q,p),sub(scale(beta,a),scale(alpha,b)))
    return intended,mirror


def parallel(a,b): return cross(a,b)==(0,0,0)


def main():
    q=(F(1),F(2),F(3)); a=(F(32),F(-1),F(-10))
    expected=[14,50,194,770,3074,12290,49154]
    rows=[]
    for n in range(6):
        p=rotate(q)
        if n==0: b=(F(-6),F(8),F(5))
        else: b=rotate(a)
        assert norm2(q)==norm2(p)==expected[n]
        assert dot(q,a)==0 and dot(p,b)==0
        intended,mirror=outputs(q,p,a,b)
        qnext=add(q,p); normal=cross(q,p)
        assert mirror==(0,0,0)
        assert intended!=(0,0,0) and parallel(intended,normal)
        rows.append((n,q,p,qnext,sub(q,p),intended))
        q=qnext; a=normal
    assert norm2(q)==expected[6]
    # Fixed-radius mirrors: d_(n+1)=-R^2 d_n.
    assert all(norm2(row[4])==F(6) for row in rows)
    print("Cycle 147 mirror-free designated cascade")
    print("shell radii squared =",expected)
    print("all six designated mirrors vanish exactly")
    print("all intended outputs are nonzero and polarization-compatible")
    print("all exact checks passed")


if __name__=="__main__": main()
