#!/usr/bin/env python3
"""Scout local extendability of all family-S C-incident type rows.

Requires z3-solver.  This is deliberately an observational scout, not a proof
certificate.  For each of the 26,060 pre-C-swap rows it asks whether the exact
C incidence extends to an oriented graph having the order-18 degree sequence,
seven holes, root N+(0)={1,...,8}, and simultaneous shared-low B-column
robustness.  Exact global badness and arc minimality are omitted.
"""
import time
from m7_family_s_type_rows import rows
try:
    import z3
except ImportError:
    raise SystemExit("z3-solver is required for this optional scout")

N=18; A=set(range(1,9)); B=set(range(9,16)); C=(16,17); HIGHS={1,2}
a=[[z3.Bool(f'a_{i}_{j}') for j in range(N)] for i in range(N)]
s=z3.Solver(); s.set(timeout=5000)
for i in range(N): s.add(z3.Not(a[i][i]))
for i in range(N):
    for j in range(i+1,N): s.add(z3.Not(z3.And(a[i][j],a[j][i])))
for i in range(N):
    s.add(z3.PbEq([(a[i][j],1) for j in range(N) if j!=i],
                  9 if i in HIGHS else 8))
s.add(z3.PbEq([(z3.And(z3.Not(a[i][j]),z3.Not(a[j][i])),1)
               for i in range(N) for j in range(i+1,N)],7))
for j in range(N): s.add(a[0][j] if j in A else z3.Not(a[0][j]))
for b in B:
    s.add(z3.Or([a[x][b] for x in A-{1}]))
    s.add(z3.Or([a[x][b] for x in A-{2}]))

selector={}
def guard(name,formula):
    z=z3.Bool(name); selector[name]=z; s.add(z3.Implies(z,formula))

for u in [0,1,2]+list(range(3,9)):
    for t,bits in enumerate(((0,0),(0,1),(1,0),(1,1))):
        clauses=[]
        for k,c in enumerate(C):
            clauses.append(z3.And(z3.Not(a[u][c]),z3.Not(a[c][u]))
                           if bits[k] else z3.And(a[c][u],z3.Not(a[u][c])))
        guard(f'U{u}T{t}',z3.And(clauses))
for b in sorted(B):
    for t in range(9):
        clauses=[]
        for k,c in enumerate(C):
            symbol=(t//3,t%3)[k]
            clauses.append(z3.And(a[c][b],z3.Not(a[b][c])) if symbol==0 else
                           z3.And(a[b][c],z3.Not(a[c][b])) if symbol==1 else
                           z3.And(z3.Not(a[b][c]),z3.Not(a[c][b])))
        guard(f'B{b}T{t}',z3.And(clauses))
guard('SM',z3.And(z3.Not(a[16][17]),z3.Not(a[17][16])))
guard('S01',z3.And(a[16][17],z3.Not(a[17][16])))
guard('S10',z3.And(a[17][16],z3.Not(a[16][17])))

counts={}; start=time.time(); data=rows()
for index,row in enumerate(data):
    state,distinguished,a_counts,b_counts,_=row
    assumptions=[]
    atypes=list(distinguished)+sum(([t]*n for t,n in enumerate(a_counts)),[])
    for u,t in zip([0,1,2]+list(range(3,9)),atypes):
        assumptions.append(selector[f'U{u}T{t}'])
    btypes=sum(([t]*n for t,n in enumerate(b_counts)),[])
    for b,t in zip(sorted(B),btypes): assumptions.append(selector[f'B{b}T{t}'])
    assumptions.append(selector['S'+state])
    result=str(s.check(*assumptions)); counts[result]=counts.get(result,0)+1
    if result!='sat': print('NON-SAT',index,result,row)
assert counts=={'sat':26060}
print(f"OBSERVATION all_local_extensions_sat={len(data)} seconds={time.time()-start:.3f}")
print("WARNING no badness/arc-minimality and no proof certificates; no pruning follows")
