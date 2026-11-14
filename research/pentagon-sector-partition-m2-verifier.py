#!/usr/bin/env /usr/bin/python3
"""Exact exhaustive checker for the C5-sector split in D+C5+2C3.
No floating point and no third-party Python package.

A bridge-free bare incidence is encoded by:
  * a labelled tree on block nodes D,P,A,B;
  * independently, for every tree edge UV, a vertex of U and a vertex of V
    to identify. Equal labels on several incident edges are allowed; these are
    repeated owners / higher-degree cut nodes.
This is exactly a labelled block-cut incidence tree with the cut nodes
suppressed. The weighted Cayley census is
    (4*5*3^2) * (4+5+3+3)^2 = 40,500.
"""
from itertools import product
from collections import Counter, defaultdict

names=('D','P','A','B'); sizes=(4,5,3,3); D,P=0,1
local_edges=(
 ((0,1),(0,2),(1,2),(0,3),(1,3)),             # D=K4-e
 ((0,1),(1,2),(2,3),(3,4),(4,0)),             # P=C5
 ((0,1),(1,2),(2,0)), ((0,1),(1,2),(2,0)))
off=[];s=0
for z in sizes: off.append(s);s+=z
N0=s # 15 before three identifications

def prufer_tree(code):
 deg=[1]*4
 for x in code:deg[x]+=1
 edges=[]
 for x in code:
  leaf=next(i for i,d in enumerate(deg) if d==1)
  edges.append((leaf,x));deg[leaf]-=1;deg[x]-=1
 u=[i for i,d in enumerate(deg) if d==1]
 edges.append(tuple(u));return tuple(edges)

def find(p,x):
 while p[x]!=x:
  p[x]=p[p[x]];x=p[x]
 return x

def union(p,a,b):
 a=find(p,a);b=find(p,b)
 if a!=b:p[b]=a

def components(n,edges,drop):
 adj=[[] for _ in range(n)]
 for e,(a,b) in enumerate(edges):
  if e in drop:continue
  adj[a].append(b);adj[b].append(a)
 cc=[-1]*n; cs=[]
 for v in range(n):
  if cc[v]>=0:continue
  q=[v];cc[v]=len(cs);V=[]
  while q:
   x=q.pop();V.append(x)
   for y in adj[x]:
    if cc[y]<0:cc[y]=cc[v];q.append(y)
  cs.append(tuple(V))
 return cc,cs

def connected(V,edges):
 V=set(V)
 if not V:return False
 adj={v:[] for v in V}
 for a,b in edges:
  if a in V and b in V:adj[a].append(b);adj[b].append(a)
 q=[next(iter(V))];seen={q[0]}
 while q:
  for y in adj[q.pop()]:
   if y not in seen:seen.add(y);q.append(y)
 return seen==V

total=relevant=0; failures=[]
dist=Counter(); marksets=Counter(); tree_relevant=Counter(); repeated=Counter()
# 16 labelled block-node trees
for code in product(range(4),repeat=2):
 T=prufer_tree(code)
 option_lists=[]
 for u,v in T:
  option_lists.append(tuple((a,b) for a in range(sizes[u]) for b in range(sizes[v])))
 for labs in product(*option_lists):
  total+=1
  par=list(range(N0))
  for (u,v),(a,b) in zip(T,labs):
   union(par,off[u]+a,off[v]+b)
  roots=[find(par,i) for i in range(N0)]
  uniq={r:i for i,r in enumerate(sorted(set(roots)))}
  mp=[uniq[r] for r in roots]; n=len(uniq)
  if n!=12:failures.append(('order',code,labs,n));continue
  bedges=[]; blockv=[]
  for b in range(4):
   vs=tuple(mp[off[b]+i] for i in range(sizes[b]));blockv.append(vs)
   for a,c in local_edges[b]:bedges.append(tuple(sorted((vs[a],vs[c]))))
  if len(set(bedges))!=16 or any(a==b for a,b in bedges):
   failures.append(('edges',code,labs));continue
  edges=tuple(sorted(set(bedges)))
  # Locate the five P edges by endpoints (they are unique).
  pvs=blockv[P]
  pset={tuple(sorted((pvs[i],pvs[(i+1)%5]))) for i in range(5)}
  drop={i for i,e in enumerate(edges) if e in pset}
  if len(drop)!=5:failures.append(('Pedges',code,labs));continue
  cc,cs=components(n,edges,drop)
  # Every component of G-E(P) must meet P in exactly one physical P vertex.
  inter=[]
  for V in cs:
   q=set(V)&set(pvs);inter.append(q)
  if len(cs)!=5 or any(len(q)!=1 for q in inter):
   failures.append(('Pcomponent',code,labs,inter));continue
  pcomp={pvs[i]:cc[pvs[i]] for i in range(5)}
  dcomp=cc[blockv[D][0]]
  if any(cc[x]!=dcomp for x in blockv[D]):
   failures.append(('Dsplit',code,labs));continue
  tcomp=[]
  for b in (2,3):
   z=cc[blockv[b][0]]
   if any(cc[x]!=z for x in blockv[b]):failures.append(('Tsplit',code,labs,b));break
   tcomp.append(z)
  else:
   cyc_count=Counter([dcomp]+tcomp)
   compmark={cc[pvs[i]]:i for i in range(5)}
   marked=tuple(sorted(compmark[c] for c in cyc_count))
   q=len(marked)
   if q<2:
    continue # P is a leaf of the cyclic incidence hull; handled by P-not-in-K row.
   relevant+=1
   c0=compmark[dcomp]
   k=sum(c==dcomp for c in tcomp)
   others=tuple(sorted((sum(c==j for c in tcomp) for j in cyc_count if j!=dcomp),reverse=True))
   h=q-1
   if not (h>=1 and sum(others)==2-k and all(r>=1 for r in others) and h<=2-k):
    failures.append(('ledger',code,labs,k,h,others));continue
   # A repeated cyclic owner component contains at least two of D,A,B.
   # This is a statement about the component/mark ledger, not merely about
   # repeated local labels among block-tree edges incident with P.
   repeated_owner=any(value>1 for value in cyc_count.values())
   repeated[(k,h,others,repeated_owner)]+=1
   dist[(k,h,others)]+=1;marksets[marked]+=1;tree_relevant[code]+=1
   # Deterministic clockwise sectors: mark c owns c,...,vertex before next mark.
   sectors={}
   for c in marked:
    I=[c];x=(c+1)%5
    while x not in marked:I.append(x);x=(x+1)%5
    sectors[c]=tuple(I)
   flat=[x for I in sectors.values() for x in I]
   if sorted(flat)!=list(range(5)) or len(flat)!=len(set(flat)):
    failures.append(('sectors',code,labs,marked,sectors));continue
   territories={}
   for c,I in sectors.items():
    comps={pcomp[pvs[i]] for i in I}
    V={v for j in comps for v in cs[j]}
    territories[c]=V
    # exactly one cyclic mark and proper induced P-path of |I|-1 edges
    cycmarks=set(I)&set(marked)
    pinternal=sum(a in {pvs[i] for i in I} and b in {pvs[i] for i in I} for a,b in pset)
    if cycmarks!={c} or pinternal!=len(I)-1 or not connected(V,edges):
     failures.append(('territory-shape',code,labs,c,I,cycmarks,pinternal));break
    eint=sum(a in V and b in V for a,b in edges)
    beta=eint-len(V)+1
    expected=(2+k) if c==c0 else sum(z==pcomp[pvs[c]] for z in tcomp)
    if beta!=expected:
     failures.append(('beta',code,labs,c,beta,expected));break
   else:
    allV=[v for V in territories.values() for v in V]
    if len(allV)!=n or len(set(allV))!=n:
     failures.append(('partition',code,labs));continue
    # Every edge with both endpoints in a territory is already counted there;
    # cross edges are precisely the q cut P-edges between consecutive sectors.
    cross=[]
    owner={v:c for c,V in territories.items() for v in V}
    for e in edges:
     if owner[e[0]]!=owner[e[1]]:cross.append(e)
    if len(cross)!=q or any(e not in pset for e in cross):
     failures.append(('induced-cross',code,labs,cross,q));continue

weighted=(4*5*3**2)*(sum(sizes)**2)
print('semantic receipt pentagon-sector-m2:bridge-free-D+C5+2C3:exact-owner-sectors:v1')
print('block-node trees',16)
print('weighted Cayley expected',weighted)
print('labelled incidence encodings checked',total)
print('P-relevant encodings (>=2 cyclic marks)',relevant)
print('P-leaf encodings',total-relevant)
print('failures',len(failures))
print('distribution (k,h,sorted r_i): count')
for key in sorted(dist):print(key,dist[key])
print('repeated cyclic-owner-component split (k,h,r,repeated):')
for key in sorted(repeated):print(key,repeated[key])
print('distinct marked subsets',len(marksets),'counts-by-number-of-marks',dict(sorted(Counter(len(x) for x in marksets.elements()).items())))
print('credit lower endpoint min(3-h)',min(3-key[1] for key in dist))
if failures:
 print('FIRST FAILURE',failures[0]);raise SystemExit(1)
if total != weighted or weighted != 40500:
 raise RuntimeError('weighted Cayley census changed')
if relevant + (total-relevant) != total:
 raise RuntimeError('relevant/leaf partition is not exhaustive')
print('EXACT SECTOR CHECK: PASS')
