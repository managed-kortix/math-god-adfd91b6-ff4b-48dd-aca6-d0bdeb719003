#!/usr/bin/env python3
"""Exact pair-type rows for the order-18 m=7 shared-low family S.

The stabilizer fixes w,r,q, permutes the six ordinary A vertices and the seven
B vertices, and may swap the two C vertices.  A row records:

* each of w,r,q's pair type to C (hole to neither/one/both C vertices);
* multiplicities of the four C-hole types among the six ordinary A vertices;
* multiplicities of the nine C-pair types among B (for each C endpoint:
  C->B, B->C, or hole);
* the C-pair state (hole, c0->c1, c1->c0);
* the residual number h of holes internal to T.

This is the exact orbit-level synchronization of every pair incident with C.
It does not orient pairs internal to T and is not an SNC elimination.
"""
from collections import Counter,defaultdict
from itertools import product

C_HOLE_TYPES=((0,0),(0,1),(1,0),(1,1))
# B symbols from C's viewpoint: 0=C->B, 1=B->C, 2=hole.
C_STATES=(('M',0,0,1),('01',1,0,0),('10',0,1,0))
SWAP_STATE={'M':'M','01':'10','10':'01'}


def compositions(n,k,prefix=()):
    if k==1:
        yield prefix+(n,); return
    for x in range(n+1):
        yield from compositions(n-x,k-1,prefix+(x,))


def swap_row(row):
    state,distinguished,a_counts,b_counts,h=row
    # Swap the two C coordinates.  The type maps are involutions.
    swap_a=(0,2,1,3)
    distinguished=tuple(swap_a[x] for x in distinguished)
    a_counts=tuple(a_counts[swap_a[x]] for x in range(4))
    b_counts=tuple(b_counts[3*(k%3)+(k//3)] for k in range(9))
    return (SWAP_STATE[state],distinguished,a_counts,b_counts,h)


def rows():
    # C-hole patterns on U={w} union A, with w,r,q distinguished and the six
    # ordinary A labels quotiented by multiplicity.
    u_by_margin=defaultdict(list)
    for distinguished in product(range(4),repeat=3):
        for counts in compositions(6,4):
            a0=(sum(C_HOLE_TYPES[x][0] for x in distinguished)+
                sum(counts[x]*C_HOLE_TYPES[x][0] for x in range(4)))
            a1=(sum(C_HOLE_TYPES[x][1] for x in distinguished)+
                sum(counts[x]*C_HOLE_TYPES[x][1] for x in range(4)))
            u_by_margin[a0,a1].append((distinguished,counts))

    # B pair types, quotiented by S7.  Index 3*i+j means C0 symbol i and C1
    # symbol j.
    b_by_outmargin=defaultdict(list)
    for counts in compositions(7,9):
        r0=sum(counts[3*i+j] for i in range(3) for j in range(3) if i==0)
        r1=sum(counts[3*i+j] for i in range(3) for j in range(3) if j==0)
        b0=sum(counts[3*i+j] for i in range(3) for j in range(3) if i==2)
        b1=sum(counts[3*i+j] for i in range(3) for j in range(3) if j==2)
        b_by_outmargin[r0,r1].append((b0,b1,counts))

    out=[]
    for state,d0,d1,m in C_STATES:
        for (a0,a1),urows in u_by_margin.items():
            # Both C vertices are low in family S.
            r0,r1=a0-1-d0,a1-1-d1
            if min(r0,r1)<0 or max(r0,r1)>7:
                continue
            for distinguished,a_counts in urows:
                for b0,b1,b_counts in b_by_outmargin.get((r0,r1),()):
                    h=7-a0-a1-m-b0-b1
                    if h>=0:
                        out.append((state,distinguished,a_counts,b_counts,h))
    return out


def main():
    labelled=rows()
    canonical={min(row,swap_row(row)) for row in labelled}
    fixed=sum(row==swap_row(row) for row in labelled)
    by_h=Counter(row[-1] for row in canonical)
    assert len(labelled)==26060
    assert fixed==174
    assert len(canonical)==13117==(len(labelled)+fixed)//2
    assert by_h=={0:8764,1:3093,2:999,3:218,4:43}
    print(f"PASS family-S type rows before C-swap={len(labelled)} fixed={fixed}")
    print(f"PASS family-S exact C-incident type orbits={len(canonical)} by_h={dict(sorted(by_h.items()))}")
    print("NOTE each row leaves exactly h holes and all orientations internal to T existential")

if __name__=='__main__':main()
