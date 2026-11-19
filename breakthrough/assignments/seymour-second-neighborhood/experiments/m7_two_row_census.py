#!/usr/bin/env python3
"""Transparent exact scalar C-row census for the order-18 m=7 low-root form."""
import collections,itertools

def rows(epsilon):
    out=[]
    for x in ((0,0),(0,1),(1,0)):
        if sum(x)!=epsilon: continue
        for missing_cc in (0,1):
            ds=((0,0),) if missing_cc else ((1,0),(0,1))
            for d in ds:
                for aa in itertools.product(range(10),repeat=2):
                    rr=tuple(x[i]+aa[i]-1-d[i] for i in range(2))
                    if min(rr)<0: continue
                    for bb in itertools.product(range(8),repeat=2):
                        h=7-sum(aa)-sum(bb)-missing_cc
                        if h<0: continue
                        if any(rr[i]>7-bb[i] for i in range(2)): continue
                        rho=sum(rr)
                        assert sum(aa)+missing_cc==3+rho-epsilon
                        assert sum(bb)+h==4+epsilon-rho
                        out.append((x,missing_cc,d,aa,bb,h,rr,rho))
    return out

def swap(z):
    x,m,d,a,b,h,r,rho=z
    return (x[::-1],m,d[::-1],a[::-1],b[::-1],h,r[::-1],rho)

for eps in (0,1):
    labelled=rows(eps)
    canonical={min(z,swap(z)) for z in labelled}
    lc=collections.Counter(z[-1] for z in labelled)
    cc=collections.Counter(z[-1] for z in canonical)
    expected=(210,108,{0:45,1:60,2:54,3:36,4:15},{0:24,1:30,2:28,3:18,4:8}) if eps==0 else (756,378,{0:126,1:180,2:180,3:144,4:90,5:36},{0:63,1:90,2:90,3:72,4:45,5:18})
    assert (len(labelled),len(canonical),dict(lc),dict(cc))==expected
    print(f"PASS epsilon={eps} labelled={len(labelled)} canonical={len(canonical)} rho={dict(sorted(lc.items()))}")
