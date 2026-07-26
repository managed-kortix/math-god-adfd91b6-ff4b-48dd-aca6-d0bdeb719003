#!/usr/bin/env python3
"""Independent weighted audit that 136 groups partition the 735-leaf cover."""
import hashlib
from collections import Counter,defaultdict
STATES=(('M',0,0),('01',1,0),('10',0,1)); SPLITS=((0,5),(1,4),(2,3))


def mults():
    c=Counter()
    for x in range(128):
        for y in range(128): c[x.bit_count(),y.bit_count(),(x&y).bit_count()]+=1
    return c


def main():
    aa=mults(); bb=mults(); rows=set(); groups=[]; leaves=[]; total=0
    for r0,r1 in SPLITS:
        for state,d0,d1 in STATES:
            for n0 in (0,1):
                for n1 in (0,1):
                    rows.add((state,r0,r1,n0,n1))
                    for e0 in (0,1):
                        for e1 in (0,1):
                            q0=r0+1+d0-n0-e0; q1=r1+1+d1-n1-e1
                            if not (0<=q0<=7 and 0<=q1<=7): continue
                            g=(state,r0,r1,n0,n1,e0,e1); groups.append(g)
                            for k in range(8):
                                if not aa[q0,q1,k]: continue
                                for t in range(8):
                                    if not bb[r0,r1,t]: continue
                                    leaves.append(g+(k,t)); total+=2*aa[q0,q1,k]*bb[r0,r1,t]
    assert len(rows)==36 and len(groups)==136 and len(set(groups))==136
    assert len(leaves)==735 and len(set(leaves))==735 and total==63517608
    glines=['seymour-snc-rho5-groups-v1']+[','.join(map(str,g)) for g in groups]
    gd=hashlib.sha256(('\n'.join(glines)+'\n').encode()).hexdigest()
    clines=['seymour-snc-rho5-cover-v1','group=S7AxS7BxC2','rows=36','leaves=735']+[','.join(map(str,x)) for x in leaves]
    cd=hashlib.sha256(('\n'.join(clines)+'\n').encode()).hexdigest()
    assert gd=='cd8ff2b4ae155e696e4ead024add6216b04ba82482c5e3ee3f0add86a0bc54f4'
    assert cd=='0e4aa2220d8e87a67d5152130c5e26ebc16655a53b7fae6735a249cc0606171e'
    print(f'PASS groups=136 leaves=735 labeled={total} group_sha256={gd} cover_sha256={cd}')


if __name__=='__main__': main()
