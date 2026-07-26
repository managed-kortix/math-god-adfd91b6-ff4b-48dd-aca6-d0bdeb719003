#!/usr/bin/env python3
"""Canonical 735-leaf cover of the corrected m=8 rho=5 row."""
import hashlib
DELTA={'M':(0,0),'01':(1,0),'10':(0,1)}


def leaves():
    for r0,r1 in ((0,5),(1,4),(2,3)):
        for state in ('M','01','10'):
            d0,d1=DELTA[state]
            for n0 in (0,1):
                for n1 in (0,1):
                    a0=r0+1+d0-n0; a1=r1+1+d1-n1
                    for e0 in (0,1):
                        for e1 in (0,1):
                            q0=a0-e0; q1=a1-e1
                            if not (0<=q0<=7 and 0<=q1<=7): continue
                            for k in range(max(0,q0+q1-7),min(q0,q1)+1):
                                for t in range(r0+1):
                                    yield (state,r0,r1,n0,n1,e0,e1,k,t)


def stream(data):
    lines=['seymour-snc-rho5-cover-v1','group=S7AxS7BxC2',
           'rows=36',f'leaves={len(data)}']
    lines += [','.join(map(str,x)) for x in data]
    return ('\n'.join(lines)+'\n').encode()


if __name__=='__main__':
    data=list(leaves()); assert len(data)==735 and len(set(data))==735
    raw=stream(data)
    print(f"PASS leaves={len(data)} sha256={hashlib.sha256(raw).hexdigest()}")
    print(raw.decode(),end='')
