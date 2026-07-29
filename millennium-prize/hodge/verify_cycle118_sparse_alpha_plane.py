#!/usr/bin/env python3
"""Exact F_32 certificate for the sparse alpha-visible Hermitian plane."""
MOD = 0b100101  # t^5+t^2+1

def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1; a<<=1
        if a&32:a^=MOD
    return r&31
def add(a,b): return a^b
def power(a,n):
    r=1
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a); n//=2
    return r

t=2
assert add(add(power(t,5),power(t,2)),1)==0
A=[[0,t,add(t,1)],
   [t,add(power(t,2),1),add(power(t,2),t)],
   [add(t,1),add(power(t,2),t),power(t,2)]]
for i in range(3):
  for j in range(3):
    s=0
    for k in range(3):s=add(s,mul(A[k][i],A[k][j]))
    assert s==(1 if i==j else 0)
assert sum(x!=0 for row in A for x in row)==8

# Sixteen Lucas-supported terms in variables (u,v,p,q,r,s,w,z).
terms=[
(18,0,17,4,0,8,0,19),(18,0,1,4,16,24,0,3),
(18,0,16,4,1,9,0,18),(18,0,0,4,17,25,0,2),
(2,16,17,4,0,8,16,3),(2,16,1,20,0,24,0,3),
(2,16,16,4,1,9,16,2),(2,16,0,20,1,25,0,2),
(16,2,17,4,0,8,2,17),(16,2,1,4,16,24,2,1),
(16,2,16,4,1,9,2,16),(16,2,0,4,17,25,2,0),
(0,18,17,4,0,8,18,1),(0,18,1,20,0,24,2,1),
(0,18,16,4,1,9,18,0),(0,18,0,20,1,25,2,0)]
vals=(A[0][1],A[0][2],A[1][0],A[1][1],A[1][2],A[2][0],A[2][1],A[2][2])
P=0
for exps in terms:
    q=1
    for a,e in zip(vals,exps):q=mul(q,power(a,e))
    P=add(P,q)
assert P==add(add(power(t,3),power(t,2)),t)==power(t,12)
assert mul(P,add(power(t,2),t))==1
print("A^T A = I; support size = 8")
print("alpha coefficient = t^3+t^2+t = t^12 != 0")
print("inverse = t^2+t")
print("all exact checks passed")
