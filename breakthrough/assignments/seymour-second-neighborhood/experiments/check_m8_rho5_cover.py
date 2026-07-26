#!/usr/bin/env python3
"""Independent labelled-mask orbit audit of the 735-leaf rho=5 cover."""
import hashlib
from collections import Counter

STATES=(('M',0,0),('01',1,0),('10',0,1)); CODE={'M':0,'01':1,'10':2}
NAME={v:k for k,v in CODE.items()}; SWAP={'M':'M','01':'10','10':'01'}


def pair_counts():
    out=Counter()
    for x in range(128):
        for y in range(128): out[x.bit_count(),y.bit_count(),(x&y).bit_count()]+=1
    assert sum(out.values())==16384
    return out


def swap(inv):
    r0,r1,s,n0,n1,e0,e1,k,t=inv
    return (r1,r0,CODE[SWAP[NAME[s]]],n1,n0,e1,e0,k,t)


def leaf(inv):
    r0,r1,s,n0,n1,e0,e1,k,t=inv
    return (NAME[s],r0,r1,n0,n1,e0,e1,k,t)


def main():
    qa=pair_counts(); xb=pair_counts(); records={}; rows=set()
    for r0,r1 in ((0,5),(1,4),(2,3)):
        for state,d0,d1 in STATES:
            for n0 in (0,1):
                for n1 in (0,1):
                    a0=r0+1+d0-n0; a1=r1+1+d1-n1
                    rows.add((state,r0,r1,n0,n1))
                    for e0 in (0,1):
                        for e1 in (0,1):
                            q0,q1=a0-e0,a1-e1
                            if not (0<=q0<=7 and 0<=q1<=7): continue
                            for k in range(8):
                                qm=qa[q0,q1,k]
                                if not qm: continue
                                for t in range(8):
                                    xm=xb[r0,r1,t]
                                    if not xm: continue
                                    inv=(r0,r1,CODE[state],n0,n1,e0,e1,k,t)
                                    assert min(inv,swap(inv))==inv and inv not in records
                                    records[inv]=2*qm*xm
    keys=[leaf(x) for x in records]
    lines=['seymour-snc-rho5-cover-v1','group=S7AxS7BxC2','rows=36',
           f'leaves={len(keys)}']+[','.join(map(str,x)) for x in keys]
    cover=('\n'.join(lines)+'\n').encode()
    assert len(rows)==36 and len(records)==735 and len({x[:-1] for x in records})==323
    assert sum(records.values())==63517608
    digest=hashlib.sha256(cover).hexdigest()
    assert digest=='0e4aa2220d8e87a67d5152130c5e26ebc16655a53b7fae6735a249cc0606171e'
    print(f'PASS rows=36 colored=323 leaves=735 labeled=63517608 cover_sha256={digest}')


if __name__=='__main__': main()
