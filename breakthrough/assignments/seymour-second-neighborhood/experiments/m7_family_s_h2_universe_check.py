#!/usr/bin/env python3
"""Independent exact h=2 row universe and weighted-coverage reconstruction.

This checker imports neither the production row generator nor the CNF producer.
It derives pair-type multisets directly from the two low-C degree equations and
the seven-hole equation, checks C-swap closure, and can compare an ordered JSON
row ledger fail-closed against the independently reconstructed canonical set.
"""
import argparse,hashlib,json
from collections import Counter,defaultdict
from itertools import combinations_with_replacement,product
from math import factorial
from pathlib import Path

A_TYPES=((0,0),(0,1),(1,0),(1,1))
STATES=(('M',0,0,1),('01',1,0,0),('10',0,1,0))
SW={'M':'M','01':'10','10':'01'}

def hist(word,k):return tuple(word.count(i) for i in range(k))
def multinomial(counts):
    z=factorial(sum(counts))
    for n in counts:z//=factorial(n)
    return z

def swap(row):
    state,dist,a,b,h=row;sa=(0,2,1,3)
    return (SW[state],tuple(sa[x]for x in dist),tuple(a[sa[x]]for x in range(4)),
            tuple(b[3*(x%3)+(x//3)]for x in range(9)),h)

def independent_rows():
    # Distinguished w,r,q are labelled.  Ordinary A and B labels are quotiented
    # only by multiplicity, constructed here as sorted words rather than weak
    # compositions used by the production census.
    u=defaultdict(list)
    for dist in product(range(4),repeat=3):
        for word in combinations_with_replacement(range(4),6):
            ac=hist(word,4)
            a0=sum(A_TYPES[t][0]for t in dist)+sum(A_TYPES[t][0]for t in word)
            a1=sum(A_TYPES[t][1]for t in dist)+sum(A_TYPES[t][1]for t in word)
            u[a0,a1].append((dist,ac))
    b=defaultdict(list)
    for word in combinations_with_replacement(range(9),7):
        bc=hist(word,9)
        r0=sum(t//3==0 for t in word);r1=sum(t%3==0 for t in word)
        b0=sum(t//3==2 for t in word);b1=sum(t%3==2 for t in word)
        b[r0,r1].append((b0,b1,bc))
    out=[]
    for state,d0,d1,m in STATES:
        for (a0,a1),urs in u.items():
            r0,r1=a0-1-d0,a1-1-d1
            for dist,ac in urs:
                for b0,b1,bc in b.get((r0,r1),()):
                    h=7-a0-a1-m-b0-b1
                    if h==2:out.append((state,dist,ac,bc,h))
    return out

def row_json(row):return json.dumps(row,separators=(',',':'))
def parse_row(x):
    if not isinstance(x,list)or len(x)!=5:raise ValueError('malformed row')
    return (x[0],tuple(x[1]),tuple(x[2]),tuple(x[3]),x[4])

def main():
    p=argparse.ArgumentParser();p.add_argument('--ordered-ledger',type=Path);x=p.parse_args()
    pre=independent_rows();can=sorted({min(r,swap(r))for r in pre});fixed=[r for r in pre if r==swap(r)]
    if len(pre)!=1964 or len(fixed)!=34 or len(can)!=999:
        raise RuntimeError(f'wrong independent h2 census pre={len(pre)} fixed={len(fixed)} canonical={len(can)}')
    if len(set(pre))!=len(pre) or any(swap(r)not in set(pre)for r in pre):
        raise RuntimeError('h2 pre-swap universe is duplicate or not swap-closed')
    # Each type row expands ordinary-A and B multiplicities to labelled states.
    # Type-level fixed rows are not pointwise fixed labelled states: a C swap
    # may exchange ordinary labels of types 01 and 10.  Pointwise fixed states
    # require a missing C-pair, diagonal distinguished/A/B types, and hence one
    # common labelled mask for the two C rows.
    labelled_pre=sum(multinomial(r[2])*multinomial(r[3])for r in pre)
    fixed_type_row_weight=sum(multinomial(r[2])*multinomial(r[3])for r in fixed)
    pointwise_fixed_rows=[r for r in pre if r[0]=='M' and all(t in (0,3)for t in r[1])
                          and r[2][1]==r[2][2]==0
                          and all(r[3][t]==0 for t in range(9)if t not in (0,4,8))]
    pointwise_fixed_labelled=sum(multinomial(r[2])*multinomial(r[3])for r in pointwise_fixed_rows)
    labelled_orbits=(labelled_pre+pointwise_fixed_labelled)//2
    got=(labelled_pre,fixed_type_row_weight,len(pointwise_fixed_rows),pointwise_fixed_labelled,labelled_orbits)
    if got!=(1065015,18375,11,315,532665):raise RuntimeError(f'wrong weighted coverage {got}')
    if x.ordered_ledger:
        payload=json.loads(x.ordered_ledger.read_text(encoding='ascii'))
        got=[parse_row(r)for r in payload]
        if len(got)!=len(set(got)):raise RuntimeError('ordered ledger has duplicate rows')
        if got!=can:
            raise RuntimeError(f'ordered ledger mismatch missing={set(can)-set(got)} orphan={set(got)-set(can)}')
    universe_bytes=('m7-family-s-h2-universe-v1\n'+'\n'.join(row_json(r)for r in can)+'\n').encode('ascii')
    print('PASS independent h2 pre_swap_type_rows=1964 fixed_type_rows=34 canonical_orbits=999')
    print('PASS independent h2 labelled_states=1065015 fixed_type_row_weight=18375 pointwise_fixed_rows=11 pointwise_fixed_labelled=315 labelled_C_swap_orbits=532665')
    print(f'PASS independent h2 ordered_universe_sha256={hashlib.sha256(universe_bytes).hexdigest()}')

if __name__=='__main__':main()
