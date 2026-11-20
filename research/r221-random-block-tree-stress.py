import random,sys
sys.setrecursionlimit(100000)
def comps(V,E,removed=set()):
 adj={v:set() for v in V}
 for a,b in E:
  if (min(a,b),max(a,b)) in removed: continue
  adj[a].add(b);adj[b].add(a)
 out=[];seen=set()
 for s in V:
  if s in seen:continue
  q=[s];seen.add(s);C=set()
  while q:
   x=q.pop();C.add(x)
   for y in adj[x]:
    if y not in seen:seen.add(y);q.append(y)
  out.append(C)
 return out

def sigma_inv(blocks,root):
 V=set().union(*(b[1] for b in blocks)); E=set().union(*(b[2] for b in blocks))
 Ds=[i for i,b in enumerate(blocks) if b[0]=='D'];Ts=[i for i,b in enumerate(blocks) if b[0]=='T']
 cnt={v:sum(v in b[1] for b in blocks) for v in V};cuts={v for v,n in cnt.items() if n>1}
 adj={('B',i):[] for i in range(len(blocks))}
 for v in cuts:adj[('C',v)]=[]
 for i,b in enumerate(blocks):
  for v in b[1]&cuts:adj[('B',i)].append(('C',v));adj[('C',v)].append(('B',i))
 par={('B',root):None};q=[('B',root)]
 while q:
  x=q.pop(0)
  for y in adj[x]:
   if y not in par:par[y]=x;q.append(y)
 if len(par)!=len(adj): return False,('bad bct',len(par),len(adj))
 ext=[i for i in range(len(blocks)) if blocks[i][0] in ('D','T') and i!=root]
 chosen=set()
 for i in ext:
  path=[];x=('B',i)
  while x is not None:path.append(x);x=par[x]
  ks=[x[1] for x in path[::-1] if x[0]=='B' and blocks[x[1]][0]=='K2']
  if ks:chosen.add(ks[0])
 def anc(a,b):
  x=('B',b)
  while x is not None:
   if x==('B',a):return True
   x=par[x]
  return False
 for a in chosen:
  for b in chosen:
   if a!=b and (anc(a,b) or anc(b,a)):return False,('not antichain',a,b)
 removed={tuple(sorted(next(iter(blocks[i][2])))) for i in chosen}
 CC=comps(V,E,removed)
 rootv=next(iter(blocks[root][1]));rc=next(C for C in CC if rootv in C)
 for C in CC:
  if C==rc:continue
  inv=[i for i in ext if blocks[i][1]<=C]
  if not inv:return False,('away empty',C)
  r=sum(2 if blocks[i][0]=='D' else 1 for i in inv)
  if not 1<=r<=5:return False,('rank away',r)
  if r==1 and blocks[inv[0]][0]!='T':return False,('rank1 not T',inv)
 other=Ds[1] if root==Ds[0] else Ds[0]
 if not blocks[other][1]<=rc:return True,None
 node=('B',other);pn=par[node]
 if not(pn and pn[0]=='C'): return False,('no parent cut',pn)
 c=pn[1]; DE=blocks[other][2]
 RE={e for e in E if e[0] in rc and e[1] in rc}
 C2=comps(rc,RE,DE)
 if len(C2)!=4:return False,('comp count',len(C2),blocks[other][1],C2)
 own={next(iter(C&blocks[other][1])):C for C in C2 if len(C&blocks[other][1])==1}
 if set(own)!=blocks[other][1]:return False,('owners',[(C&blocks[other][1]) for C in C2])
 U=own[c];W=set().union(*(C for x,C in own.items() if x!=c))
 WE={e for e in E if e[0] in W and e[1] in W}
 if len(comps(W,WE))!=1:return False,('W disconnected',c,blocks[other][1],W,WE)
 down=[];up=[]
 for t in Ts:
  if blocks[t][1]<=W:down.append(t)
  elif blocks[t][1]<=U:up.append(t)
  elif not blocks[t][1]<=rc: pass # already first-bridge away
  else:return False,('triangle split',t,blocks[t][1],W,U,rc)
 for i,b in enumerate(blocks):
  if b[0]=='D' and b[1]<=W:return False,('diamond down',i)
 deg=sum(c in e for e in DE)
 rank=len(WE)-len(W)+1;want=(1 if deg==2 else 0)+len(down)
 if rank!=want:return False,('rank mismatch',rank,want,deg,len(down))
 if not blocks[root][1]<=U:return False,('root missing U',c)
 if len(up)>3:return False,('too many up',len(up))
 return True,None

def gen():
 V=[];blocks=[];n=0
 def new():
  nonlocal n;n+=1;V.append(n);return n
 def addD(root=None,orbit=None):
  if root is None:vs=[new() for _ in range(4)]
  else:
   fresh=[new() for _ in range(3)]
   vs=[root,*fresh] if orbit==3 else [fresh[0],fresh[1],root,fresh[2]]
  es={(min(vs[i],vs[j]),max(vs[i],vs[j])) for i,j in [(0,1),(0,2),(1,2),(0,3),(1,3)]}
  blocks.append(('D',set(vs),es));return vs
 def addT(root):
  vs=[root,new(),new()];es={(min(vs[i],vs[j]),max(vs[i],vs[j])) for i,j in [(0,1),(1,2),(2,0)]};blocks.append(('T',set(vs),es));return vs
 def bridge(root,L):
  prev=root
  for _ in range(L):
   z=new();blocks.append(('K2',{prev,z},{(min(prev,z),max(prev,z))}));prev=z
  return prev
 d0=addD(); attach=list(d0)
 labels=['D','T','T','T'];random.shuffle(labels)
 for lab in labels:
  root=random.choice(attach)
  if random.random()<.55:root=bridge(root,random.randint(1,4));attach.append(root)
  vs=addD(root,random.choice([2,3])) if lab=='D' else addT(root)
  attach+=vs
  for _ in range(random.randrange(3)):attach.append(bridge(random.choice(vs),random.randint(1,3)))
 for _ in range(random.randrange(10)): bridge(random.choice(attach),random.randint(1,4))
 return blocks
random.seed(221)
for rr in [0,1]:
 for it in range(100000):
  b=gen();Ds=[i for i,x in enumerate(b) if x[0]=='D'];ok,why=sigma_inv(b,Ds[rr])
  if not ok:print('FAIL',rr,it,why,b);raise SystemExit(1)
print('random block-tree topology: 200000/200000 invariant checks passed')
