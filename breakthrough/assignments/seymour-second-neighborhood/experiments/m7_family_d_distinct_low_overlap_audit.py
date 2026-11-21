"""Transparent finite audit for family-D overlap geometries with k=0 or 1.

This script enumerates exact 3x3 overlap tables for two rooted partitions,
filters them by all pair statuses forced by the exact rooted layers, exact
outdegrees (hence exactly seven holes), pointwise selected-deletion support, and
the private-endpoint consequence of the disjoint low-witness-set branch.

It is a checker for a finite *projection*, not a graph-completion solver and not
an SNC UNSAT certificate.  In particular it does not impose global badness or
arc minimality.  The proof report states precisely which counts are theorem
level and which are only enumerative audit output.
"""
from itertools import product
from collections import deque, Counter
L='ABC'

def tables(R,C,k):
    # Solve all 3x3 tables with M22=k from four top-left entries.
    for a in range(R[0]+1):
      for b in range(R[0]-a+1):
        c=R[0]-a-b
        for d in range(R[1]+1):
          for e in range(R[1]-d+1):
            f=R[1]-d-e
            g=C[0]-a-d; h=C[1]-b-e
            if min(c,f,g,h)>=0 and g+h+k==R[2] and c+f+k==C[2]:
                yield ((a,b,c),(d,e,f),(g,h,k))

def vertices(g):
    lu,lv,su,sv,M=g
    D={'u':('R',sv),'v':(su,'R'),'r':('A',lv),'q':(lu,'A')}
    z=0
    for i in range(3):
      for j in range(3):
        for _ in range(M[i][j]):D[f'x{z}']=(L[i],L[j]);z+=1
    assert z==14
    return D

def pair_options(g):
    D=vertices(g); V=list(D); O={}
    # codes 0=hole, 1=first listed tail, 2=second listed tail
    for ii,x0 in enumerate(V):
      for y0 in V[ii+1:]:
        x,y=sorted((x0,y0))
        opts={0,1,2}
        for coord,root in ((0,'u'),(1,'v')):
          # Root-to-layer relation.
          if x==root or y==root:
            other=y if x==root else x
            rootcode=1 if x==root else 2
            if D[other][coord]=='A': opts &= {rootcode}
            else: opts.discard(rootcode)
          # No S_s -> C_s.
          X,Y=D[x][coord],D[y][coord]
          if X in ('R','A') and Y=='C':opts.discard(1)
          if Y in ('R','A') and X=='C':opts.discard(2)
        if not opts:return None
        O[tuple(sorted((x,y)))]=opts
    return D,O

def lower_circulation(D,O):
    """Degree feasibility for a supplied exact pair-option dictionary."""
    P=list(O); V=list(D); S=0;T=1;p0=2;v0=p0+len(P);base=v0+len(V);SS=base;TT=base+1;N=base+2
    vi={x:v0+i for i,x in enumerate(V)}; cap=[{} for _ in range(N)]; bal=[0]*N
    def edge(a,b,lo,hi):
      bal[a]-=lo;bal[b]+=lo
      cap[a][b]=cap[a].get(b,0)+hi-lo;cap[b].setdefault(a,0)
    for i,p in enumerate(P):
      opts=O[p]; edge(S,p0+i,0 if 0 in opts else 1,1)
      if 1 in opts:edge(p0+i,vi[p[0]],0,1)
      if 2 in opts:edge(p0+i,vi[p[1]],0,1)
    for x in V:
      d=9 if x in ('r','q') else 8;edge(vi[x],T,d,d)
    edge(T,S,0,1000)
    target=0
    for i,b in enumerate(bal[:base]):
      if b>0:edge(SS,i,0,b);target+=b
      elif b<0:edge(i,TT,0,-b)
    flow=0
    while True:
      prev=[None]*N;prev[SS]=-1;q=deque([SS])
      while q and prev[TT] is None:
        a=q.popleft()
        for b,c in cap[a].items():
          if c>0 and prev[b] is None:prev[b]=a;q.append(b)
      if prev[TT] is None:break
      aug=10**9;x=TT
      while x!=SS: aug=min(aug,cap[prev[x]][x]);x=prev[x]
      x=TT
      while x!=SS:
        a=prev[x];cap[a][x]-=aug;cap[x][a]=cap[x].get(a,0)+aug;x=a
      flow+=aug
    return flow==target

def arc_code(p,x,y):
    return 1 if p[0]==x and p[1]==y else 2

def permits(O,x,y):
    p=tuple(sorted((x,y)));return arc_code(p,x,y) in O[p]

def robust_potential(D,O):
    for coord,deleted in ((0,'r'),(1,'q')):
      A=[x for x in D if D[x][coord]=='A' and x!=deleted]
      for b in [x for x in D if D[x][coord]=='B']:
        if not any(permits(O,a,b) for a in A):return False
    return True

def force_private(O,D,coord,other,b):
    Q={p:set(s) for p,s in O.items()}
    for a in [x for x in D if D[x][coord]=='A']:
      p=tuple(sorted((a,b))); code=arc_code(p,a,b)
      if a==other:Q[p]&={code}
      else:Q[p].discard(code)
      if not Q[p]:return None
    return Q

def private_degree_feasible(g,D,O):
    needs=[]
    for coord,other,loc in ((0,'q',g[0]),(1,'r',g[1])):
      if loc=='A':needs.append((coord,other,[b for b in D if D[b][coord]=='B']))
    def rec(j,Q):
      if j==len(needs):return lower_circulation(D,Q)
      coord,other,bs=needs[j]
      for b in bs:
        R=force_private(Q,D,coord,other,b)
        if R is not None and rec(j+1,R):return True
      return False
    return rec(0,O)

def swap(g):
    lu,lv,su,sv,M=g
    return lv,lu,sv,su,tuple(tuple(M[j][i] for j in range(3)) for i in range(3))
def flat(g):return g[:4]+tuple(z for row in g[4] for z in row)
def canon(g):return min(flat(g),flat(swap(g)))

def run(k):
    geometries=[]
    for lu,lv,su,sv in product(L,repeat=4):
      R=[8,7,2];C=[8,7,2]
      for a in (su,'A',lu):R[L.index(a)]-=1
      for a in (sv,lv,'A'):C[L.index(a)]-=1
      if min(R+C)<0:continue
      for M in tables(R,C,k):
        g=(lu,lv,su,sv,M); z=pair_options(g)
        if z is not None:geometries.append((g,*z))
    base={canon(g):(g,D,O) for g,D,O in geometries}
    degree={key:x for key,x in base.items() if lower_circulation(x[1],x[2])}
    support={key:x for key,x in degree.items() if robust_potential(x[1],x[2])}
    private={key:x for key,x in support.items() if private_degree_feasible(*x)}

    rawdeg=[x for x in geometries if lower_circulation(x[1],x[2])]
    rawsup=[x for x in rawdeg if robust_potential(x[1],x[2])]
    rawpriv=[x for x in rawsup if private_degree_feasible(*x)]
    fixed=sum(flat(g)==flat(swap(g)) for g,D,O in rawpriv)
    return len(geometries),len(base),len(rawdeg),len(degree),len(rawsup),len(support),len(rawpriv),fixed,len(private),Counter(g[:4] for g,D,O in private.values())

EXPECTED = {
    0: (1216, 647, 394, 212, 374, 201, 234, 22, 128),
    1: (462, 253, 89, 50, 74, 42, 38, 6, 22),
}

def main():
    for k in (0, 1):
        result = run(k)
        prefix = result[:9]
        if prefix != EXPECTED[k]:
            raise RuntimeError(f"k={k}: expected {EXPECTED[k]}, got {prefix}")
        print(
            f"PASS k={k}: raw={result[0]}, root-swap-orbits={result[1]}, "
            f"degree-orbits={result[3]}, support-orbits={result[5]}, "
            f"private-orbits={result[8]}"
        )
    print("PASS exact finite projection audit (not a completion/UNSAT proof)")

if __name__ == "__main__":
    main()
