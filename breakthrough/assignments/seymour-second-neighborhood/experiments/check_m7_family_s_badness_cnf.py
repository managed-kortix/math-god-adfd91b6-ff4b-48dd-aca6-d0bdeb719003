#!/usr/bin/env python3
"""Producer-independent exact reconstruction of family-S badness CNFs.

The checker does not import the producer, ``snc_cnf``, or the type-row census.
It reconstructs the complete variable order and clause stream, derives and
checks the row key directly from its JSON form, and byte-authenticates the
DIMACS payload after hostile parsing.
"""
import argparse,hashlib,json
from pathlib import Path

N=18; W=0; A=set(range(1,9)); B=set(range(9,16)); C=(16,17); HIGHS={1,2}
ATYPES=((0,0),(0,1),(1,0),(1,1))

class Formula:
    def __init__(self):self.names={};self.clauses=[]
    def var(self,name):
        if name not in self.names:self.names[name]=len(self.names)+1
        return self.names[name]
    def add(self,*z):self.clauses.append(tuple(z))

def and_gate(c,y,x,z):c.add(-y,x);c.add(-y,z);c.add(y,-x,-z)
def count(c,inputs,tag):
    prev=[]
    for i,x in enumerate(inputs,1):
        cur=[]
        for t in range(1,i+1):
            y=c.var(f'cnt_{tag}_{i}_{t}');cur.append(y)
            u=prev[t-1] if t<=len(prev) else None
            v=prev[t-2] if t>=2 else True
            if u is not None:c.add(-u,y)
            if v is True:c.add(-x,y)
            else:c.add(-x,-v,y)
            if u is None:
                if v is True:c.add(-y,x)
                else:c.add(-y,x);c.add(-y,v)
            elif v is True:c.add(-y,u,x)
            else:c.add(-y,u,x);c.add(-y,u,v)
        prev=cur
    return prev

def audit_counter():
    """Truth-table the independently implemented unary counter on small inputs."""
    import itertools
    for n in range(1,9):
        c=Formula();xs=[c.var(f'x_{i}') for i in range(n)];ys=count(c,xs,'audit')
        for bits in itertools.product((False,True),repeat=n):
            val={xs[i]:bits[i] for i in range(n)}
            for name,var in c.names.items():
                if name.startswith('cnt_audit_'):
                    _,_,i,t=name.split('_');val[var]=sum(bits[:int(i)])>=int(t)
            if not all(any(val[abs(z)]==(z>0)for z in q)for q in c.clauses):
                raise RuntimeError('counter truth-table audit failed')
            for k,y in enumerate(ys,1):
                if val[y]!=(sum(bits)>=k):raise RuntimeError('counter output audit failed')

def exact(c,z,k,tag):
    q=count(c,z,tag)
    if k:c.add(q[k-1])
    if k<len(z):c.add(-q[k])

def reconstruct_base():
    c=Formula();a=[[c.var(f'a_{i}_{j}')for j in range(N)]for i in range(N)]
    q=[[c.var(f'q_{i}_{j}')for j in range(N)]for i in range(N)]
    for i in range(N):c.add(-a[i][i]);c.add(-q[i][i])
    for i in range(N):
        for j in range(i+1,N):c.add(-a[i][j],-a[j][i])
    for i in range(N):
        for j in range(N):
            if i==j:continue
            paths=[]
            for k in range(N):
                if k in (i,j):continue
                p=c.var(f'p_{i}_{k}_{j}');paths.append(p);and_gate(c,p,a[i][k],a[k][j])
            r=c.var(f'reach_{i}_{j}')
            for p in paths:c.add(-p,r)
            c.add(-r,*paths)
            c.add(-q[i][j],r);c.add(-q[i][j],-a[i][j]);c.add(q[i][j],-r,a[i][j])
    for i in range(N):
        exact(c,[a[i][j]for j in range(N)if j!=i],9 if i in HIGHS else 8,f'd1_{i}')
        secs=count(c,[q[i][j]for j in range(N)if j!=i],f'd2_{i}')
        c.add(-secs[8 if i in HIGHS else 7])
    holes=[]
    for i in range(N):
        for j in range(i+1,N):
            h=c.var(f'h_{i}_{j}');holes.append(h)
            c.add(-h,-a[i][j]);c.add(-h,-a[j][i]);c.add(h,a[i][j],a[j][i])
    exact(c,holes,7,'holes')
    for j in range(N):c.add(a[W][j]if j in A else-a[W][j])
    for b in B:
        c.add(*[a[x][b]for x in sorted(A-{1})]);c.add(*[a[x][b]for x in sorted(A-{2})])
    return c,a

def parse_row(text):
    x=json.loads(text)
    if not(isinstance(x,list)and len(x)==5):raise ValueError('row must have five fields')
    state,dist,ac,bc,h=x
    if state not in ('M','01','10') or len(dist)!=3 or len(ac)!=4 or len(bc)!=9:
        raise ValueError('malformed row')
    if any(type(z)is not int or z<0 for z in dist+ac+bc+[h]) or any(z>3 for z in dist):
        raise ValueError('invalid row entry')
    if sum(ac)!=6 or sum(bc)!=7 or not 0<=h<=4:raise ValueError('not a family-S type row')
    # Independent degree/hole-margin validation of the exact C incidence.
    m=int(state=='M');d=(0,0)if m else((1,0)if state=='01'else(0,1))
    aa=[sum(ATYPES[t][k]for t in dist)+sum(ac[t]*ATYPES[t][k]for t in range(4))for k in range(2)]
    rr=[sum(n for t,n in enumerate(bc)if(t//3,t%3)[k]==0)for k in range(2)]
    bb=[sum(n for t,n in enumerate(bc)if(t//3,t%3)[k]==2)for k in range(2)]
    if any(rr[k]!=aa[k]-1-d[k]for k in range(2)) or 7!=sum(aa)+sum(bb)+m+h:
        raise ValueError('row violates exact C degree/hole identities')
    return(state,tuple(dist),tuple(ac),tuple(bc),h)

def add_row(c,a,row):
    state,dist,ac,bc,_=row
    ts=list(dist)+sum(([t]*n for t,n in enumerate(ac)),[])
    for u,t in zip([0,1,2]+list(range(3,9)),ts):
        for k,z in enumerate(C):
            if ATYPES[t][k]:c.add(-a[u][z]);c.add(-a[z][u])
            else:c.add(a[z][u]);c.add(-a[u][z])
    ts=sum(([t]*n for t,n in enumerate(bc)),[])
    for b,t in zip(sorted(B),ts):
        for k,z in enumerate(C):
            symbol=(t//3,t%3)[k]
            if symbol==0:c.add(a[z][b]);c.add(-a[b][z])
            elif symbol==1:c.add(a[b][z]);c.add(-a[z][b])
            else:c.add(-a[b][z]);c.add(-a[z][b])
    if state=='M':c.add(-a[16][17]);c.add(-a[17][16])
    elif state=='01':c.add(a[16][17]);c.add(-a[17][16])
    else:c.add(a[17][16]);c.add(-a[16][17])

def serialize(c):
    z=''.join(f'c var {n} {name}\n'for name,n in c.names.items())
    z+=f'p cnf {len(c.names)} {len(c.clauses)}\n'
    z+=''.join(' '.join(map(str,q))+' 0\n'for q in c.clauses)
    return z.encode('ascii')

def hostile_parse(raw):
    lines=raw.decode('ascii').splitlines();names=[];cla=[];header=None
    for no,line in enumerate(lines,1):
        if line.startswith('c var '):
            if header is not None:raise ValueError('map after header')
            f=line.split(maxsplit=3)
            if len(f)!=4 or int(f[2])!=len(names)+1 or f[3] in names:raise ValueError('bad variable map')
            names.append(f[3]);continue
        if line.startswith('p '):
            if header is not None:raise ValueError('duplicate header')
            f=line.split();
            if len(f)!=4 or f[:2]!=['p','cnf']:raise ValueError('bad header')
            header=tuple(map(int,f[2:]));continue
        if header is None:raise ValueError(f'unexpected line {no}')
        z=tuple(map(int,line.split()))
        if not z or z[-1]!=0 or 0 in z[:-1]:raise ValueError('bad clause')
        cla.append(z[:-1])
    if header!=(len(names),len(cla)) or any(abs(x)>len(names)for q in cla for x in q):
        raise ValueError('dimensions/literal range mismatch')
    return names,cla

def main():
    p=argparse.ArgumentParser();p.add_argument('cnf',type=Path);p.add_argument('--row')
    p.add_argument('--base',action='store_true');x=p.parse_args()
    if x.base==(x.row is not None):p.error('choose exactly one of --base or --row JSON')
    row=None if x.base else parse_row(x.row)
    audit_counter();c,a=reconstruct_base()
    if row is not None:add_row(c,a,row)
    raw=x.cnf.read_bytes();names,cla=hostile_parse(raw)
    expected_names=list(c.names)
    if names!=expected_names or cla!=c.clauses or raw!=serialize(c):raise RuntimeError('CNF differs from independent reconstruction')
    print(f'PASS independent badness CNF vars={len(names)} clauses={len(cla)} sha256={hashlib.sha256(raw).hexdigest()}')

if __name__=='__main__':main()
