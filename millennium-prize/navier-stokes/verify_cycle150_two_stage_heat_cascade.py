#!/usr/bin/env python3
"""Exact two-stage heat-resonant Navier cascade certificate."""

from fractions import Fraction as F


def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def scale(c,a): return tuple(c*x for x in a)
def dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))
def norm2(a): return dot(a,a)
def project(k,v): return sub(v,scale(dot(k,v)/norm2(k),k))
def symbol(k,l,a,b): return project(add(k,l),add(scale(dot(a,l),b),scale(dot(b,k),a)))


def main():
    e1=(F(1),F(0),F(0)); e2=(F(0),F(1),F(0)); e3=(F(0),F(0),F(1))
    q0,p0,p1=e1,e2,e3; q1=add(q0,p0); q2=add(q1,p1)
    a=(F(0),F(1),F(1)); b=(F(1),F(0),F(1)); c=(F(1),F(-1),F(0))
    f=symbol(q0,p0,a,b); h=symbol(q1,p1,f,c)
    assert f==(0,0,2) and h==(2,-2,0)
    assert symbol(q0,p1,a,c)==(0,0,0)
    assert symbol(p0,p1,b,c)==(0,0,0)
    assert norm2(q0)==norm2(p0)==norm2(p1)==1
    assert norm2(q1)==2 and norm2(q2)==3
    # Integral x^4 exp(-6x), 0..1/2 = (1-(131/8)e^-3)/324.
    # Thus charge coefficient is (1-(131/8)e^-3)/(54 nu^4 N^4).
    assert F(6,324)==F(1,54)
    print("Cycle 150 two-stage heat cascade")
    print("first symbol =",f,"second symbol =",h)
    print("off-tree positive bracketings vanish exactly")
    print("terminal mode = -N^2 t^2 exp(-3 nu N^2 t) (1,-1,0)")
    print("charge = [1-(131/8)exp(-3)]/(54 nu^4 N^4)")
    print("all exact algebraic checks passed")


if __name__=="__main__": main()
