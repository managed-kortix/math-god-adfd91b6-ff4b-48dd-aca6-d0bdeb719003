#!/usr/bin/env python3
"""Split m=9,k=4 by one of the eleven unlabeled T-hole shapes."""
import argparse
from snc_cnf import generate, threshold

P={"c4":(4,0,0,0,4),"paw":(3,1,0,1,3),"p5":(3,0,0,0,2),
   "triangle_edge":(3,0,0,1,3),"fork":(2,1,0,0,1),
   "k1_4":(1,1,1,0,0),"p4_edge":(2,0,0,0,1),
   "two_p3":(2,0,0,0,0),"claw_edge":(1,1,0,0,0),
   "p3_two_edges":(1,0,0,0,0),"four_matching":(0,0,0,0,0)}

def exact(c,o,v):
    if v==0:c.add(-o[0])
    elif v==len(o):c.add(o[-1])
    else:c.add(o[v-1]);c.add(-o[v])
def and3(c,y,a,b,d):
    c.add(-y,a);c.add(-y,b);c.add(-y,d);c.add(y,-a,-b,-d)

def build(rho,shape):
    c=generate(18,7,9,True,(),(0,1),True)
    for j in range(18):
        if j!=1:c.add(-c.var(f"h_{min(1,j)}_{max(1,j)}"))
    exact(c,threshold(c,[c.var(f"a_{x}_{b}") for x in (16,17)
                         for b in range(9,16)],f"k4rho{rho}{shape}"),rho)
    hs=[c.var(f"h_{i}_{j}") for i in range(16) for j in range(i+1,16)]
    exact(c,threshold(c,hs,f"k4holes{rho}{shape}"),4)
    ge2={};ge3={};ge4={}
    for v in range(16):
        d=threshold(c,[c.var(f"h_{min(u,v)}_{max(u,v)}") for u in range(16)
                       if u!=v],f"k4deg{v}{rho}{shape}")
        ge2[v],ge3[v],ge4[v]=d[1],d[2],d[3]
    n2,n3,n4,nt,nq=P[shape]
    for vals,n,tag in ((ge2,n2,"n2"),(ge3,n3,"n3"),(ge4,n4,"n4")):
        exact(c,threshold(c,list(vals.values()),f"k4{tag}{rho}{shape}"),n)
    tris=[]
    for u in range(16):
      for v in range(u+1,16):
       for w in range(v+1,16):
        y=c.var(f"k4tri_{u}_{v}_{w}_{rho}_{shape}");tris.append(y)
        and3(c,y,c.var(f"h_{u}_{v}"),c.var(f"h_{u}_{w}"),c.var(f"h_{v}_{w}"))
    if nt: c.add(*tris)
    else:
        for y in tris:c.add(-y)
    core=[]
    for u in range(16):
      for v in range(u+1,16):
        y=c.var(f"k4core_{u}_{v}_{rho}_{shape}");core.append(y)
        and3(c,y,c.var(f"h_{u}_{v}"),ge2[u],ge2[v])
    exact(c,threshold(c,core,f"k4q{rho}{shape}"),nq)
    return c,ge2,ge3

def emit(rho,shape,out):
    c,_,_=build(rho,shape)
    with open(out,"w",encoding="ascii",newline="\n") as f:
      for name,num in c.names.items():f.write(f"c var {num} {name}\n")
      f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
      for cl in c.clauses:f.write(" ".join(map(str,cl))+" 0\n")
    print(f"rho={rho} shape={shape} vars={len(c.names)} clauses={len(c.clauses)}")

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("rho",type=int,choices=range(3));p.add_argument("shape",choices=P);p.add_argument("output");a=p.parse_args();emit(a.rho,a.shape,a.output)
