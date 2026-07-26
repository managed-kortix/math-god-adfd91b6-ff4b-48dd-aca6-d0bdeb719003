#!/usr/bin/env python3
"""Enumerate 136 representative-free margin groups covering 735 leaves."""
import hashlib
from m8_rho5_leaves import DELTA, leaves


def groups():
    for r0,r1 in ((0,5),(1,4),(2,3)):
        for state in ('M','01','10'):
            d0,d1=DELTA[state]
            for n0 in (0,1):
                for n1 in (0,1):
                    for e0 in (0,1):
                        for e1 in (0,1):
                            q0=r0+1+d0-n0-e0; q1=r1+1+d1-n1-e1
                            if 0<=q0<=7 and 0<=q1<=7:
                                yield (state,r0,r1,n0,n1,e0,e1)


if __name__=='__main__':
    data=list(groups()); assert len(data)==136 and len(set(data))==136
    expanded=sum(sum(x[:7]==g for x in leaves()) for g in data)
    assert expanded==735
    raw=('seymour-snc-rho5-groups-v1\n'+'\n'.join(','.join(map(str,g)) for g in data)+'\n').encode()
    print(f'PASS groups=136 expanded_leaves=735 sha256={hashlib.sha256(raw).hexdigest()}')
