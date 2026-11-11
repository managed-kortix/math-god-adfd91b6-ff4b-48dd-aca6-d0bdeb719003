#!/usr/bin/env python3
"""Exact rooted-cell placements of degree>=2 vertices in a k=4 shape."""
import argparse
from m9_k4_shapes import P,build,exact
from snc_cnf import threshold

A=tuple(range(2,9)); B=tuple(range(9,16)); R=(0,)

def and2(c,y,x,z):
    c.add(-y,x);c.add(-y,z);c.add(y,-x,-z)
def and3(c,y,x,z,t):
    c.add(-y,x);c.add(-y,z);c.add(-y,t);c.add(y,-x,-z,-t)

def emit(rho,shape,alpha,beta,epsilon,out,kappa=None,eta=None,lam=None):
    n2=P[shape][0]
    if min(alpha,beta,epsilon)<0 or epsilon not in (0,1) or alpha+beta+epsilon!=n2:
        raise ValueError("placement counts must partition n2")
    c,ge2,_=build(rho,shape); tag=f"pl{rho}{shape}{alpha}{beta}{epsilon}"
    for cell,value,name in ((A,alpha,"a"),(B,beta,"b"),(R,epsilon,"r")):
        exact(c,threshold(c,[ge2[v] for v in cell],tag+name),value)
    if lam is not None and (kappa is None or eta is None):
        raise ValueError("lambda requires kappa and eta")
    if (kappa is None)!=(eta is None):raise ValueError("kappa and eta must be supplied together")
    if kappa is not None:
        if kappa not in (5,6) or not 0<=eta<=4:raise ValueError("bad kappa/eta")
        K={}
        for b in B:
            y=c.var(f"K_{b}_{tag}");K[b]=y
            and2(c,y,c.var(f"a_{b}_16"),c.var(f"a_{b}_17"))
        exact(c,threshold(c,list(K.values()),tag+"kappa"),kappa)
        inside=[]
        for i in B:
            for j in B:
                if i>=j:continue
                y=c.var(f"HK_{i}_{j}_{tag}");inside.append(y)
                and3(c,y,K[i],K[j],c.var(f"h_{i}_{j}"))
        exact(c,threshold(c,inside,tag+"eta"),eta)
        if lam is not None:
            lo=max(0,beta-(7-kappa));hi=min(beta,kappa)
            if not lo<=lam<=hi:
                raise ValueError(f"lambda must lie in [{lo},{hi}] for this placement")
            marked=[]
            for b in B:
                y=c.var(f"LK_{b}_{tag}");marked.append(y);and2(c,y,K[b],ge2[b])
            exact(c,threshold(c,marked,tag+"lambda"),lam)
    with open(out,"w",encoding="ascii",newline="\n") as f:
        for name,num in c.names.items():f.write(f"c var {num} {name}\n")
        f.write(f"p cnf {len(c.names)} {len(c.clauses)}\n")
        for cl in c.clauses:f.write(" ".join(map(str,cl))+" 0\n")
    split="" if kappa is None else f" kappa={kappa} eta={eta}"
    if lam is not None:split+=f" lambda={lam}"
    print(f"rho={rho} shape={shape} alpha={alpha} beta={beta} epsilon={epsilon}{split} vars={len(c.names)} clauses={len(c.clauses)}")

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("rho",type=int,choices=range(3));p.add_argument("shape",choices=P);p.add_argument("alpha",type=int);p.add_argument("beta",type=int);p.add_argument("epsilon",type=int);p.add_argument("output");p.add_argument("--kappa",type=int);p.add_argument("--eta",type=int);p.add_argument("--lambda-k",dest="lam",type=int);a=p.parse_args();emit(a.rho,a.shape,a.alpha,a.beta,a.epsilon,a.output,a.kappa,a.eta,a.lam)
