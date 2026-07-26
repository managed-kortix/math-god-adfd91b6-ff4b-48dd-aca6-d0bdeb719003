#!/usr/bin/env python3
"""Enumerate the exact 762 coarse C-margin rows in the m=8 witness branch."""
STATE=(('M',0,0),('01',1,0),('10',0,1))
CODE={'M':0,'01':1,'10':2}; SWAP={'M':'M','01':'10','10':'01'}


def key(r):
    s,r0,r1,n0,a0,b0,n1,a1,b1,g=r
    return (r0,r1,CODE[s],n0,a0,b0,n1,a1,b1,g)


def swap(r):
    s,r0,r1,n0,a0,b0,n1,a1,b1,g=r
    return (SWAP[s],r1,r0,n1,a1,b1,n0,a0,b0,g)


def rows():
    out=[]
    for state,d0,d1 in STATE:
        for r0 in range(6):
            for r1 in range(6-r0):
                external=5-r0-r1
                for n0 in (0,1):
                    a0=r0+1+d0-n0
                    if not 0<=a0<=8: continue
                    for n1 in (0,1):
                        a1=r1+1+d1-n1
                        if not 0<=a1<=8: continue
                        for b0 in range(external+1):
                            for b1 in range(external-b0+1):
                                row=(state,r0,r1,n0,a0,b0,n1,a1,b1,external-b0-b1)
                                if key(row)<=key(swap(row)): out.append(row)
    return sorted(out,key=key)


if __name__=='__main__':
    data=rows(); assert len(data)==762
    by_rho={r:sum(x[1]+x[2]==r for x in data) for r in range(6)}
    print(f"PASS rows={len(data)} by_rho={by_rho}")
    for i,row in enumerate(data): print(i,*row)
