#!/usr/bin/env python3
"""Independent subset checker for the m9 k4 missing-graph cover."""
import hashlib
import itertools
import sys

# Deliberately duplicated: this checker imports no production cover code.
PROFILES = {
    "c4": (4,0,0,0,4), "paw": (3,1,0,1,3),
    "p5": (3,0,0,0,2), "triangle_edge": (3,0,0,1,3),
    "fork": (2,1,0,0,1), "k1_4": (1,1,1,0,0),
    "p4_edge": (2,0,0,0,1), "two_p3": (2,0,0,0,0),
    "claw_edge": (1,1,0,0,0), "p3_two_edges": (1,0,0,0,0),
    "four_matching": (0,0,0,0,0),
}
EDGES = {
    "c4": ((0,1),(1,2),(2,3),(0,3)),
    "paw": ((0,1),(1,2),(0,2),(0,3)),
    "p5": ((0,1),(1,2),(2,3),(3,4)),
    "triangle_edge": ((0,1),(1,2),(0,2),(3,4)),
    "fork": ((0,1),(0,2),(0,3),(1,4)),
    "k1_4": ((0,1),(0,2),(0,3),(0,4)),
    "p4_edge": ((0,1),(1,2),(2,3),(4,5)),
    "two_p3": ((0,1),(1,2),(3,4),(4,5)),
    "claw_edge": ((0,1),(0,2),(0,3),(4,5)),
    "p3_two_edges": ((0,1),(1,2),(3,4),(5,6)),
    "four_matching": ((0,1),(2,3),(4,5),(6,7)),
}
EXPECTED_KEY_HASH = "51700d5bd4f592859442da60b83b9c49a434d9a31b09618bfe61b09326b61195"
EXPECTED_LEDGER_HASH = "9e8ebba3b2617beb5ee58c052e4f59a03abbb20a3a09f9d11c4ee6b2019f1cae"


def audit_representative(shape):
    edges = EDGES[shape]
    assert len(edges) == len(set(edges)) == 4
    assert all(0 <= u < v for u, v in edges)
    order = 1 + max(max(e) for e in edges)
    deg = [0] * order
    for u, v in edges:
        deg[u] += 1; deg[v] += 1
    n2 = sum(d >= 2 for d in deg)
    n3 = sum(d >= 3 for d in deg)
    n4 = sum(d >= 4 for d in deg)
    triangles = sum(all(tuple(sorted(e)) in edges for e in ((a,b),(a,c),(b,c)))
                    for a,b,c in itertools.combinations(range(order),3))
    core = sum(deg[u] >= 2 and deg[v] >= 2 for u,v in edges)
    assert (n2,n3,n4,triangles,core) == PROFILES[shape]
    return {v for v,d in enumerate(deg) if d >= 2}, order


def coordinates(shape, kappa):
    edges = EDGES[shape]
    marked, order = audit_representative(shape)
    V = set(range(order)); out = set()
    # Independently choose support subsets in the root, B, and K. The remaining
    # support is in A'; omitted isolates fill all unused cell capacities.
    for root in [set()] + [{v} for v in V]:
        rest = V-root
        for bsize in range(min(7,len(rest))+1):
            for bt in itertools.combinations(sorted(rest),bsize):
                B=set(bt)
                if len(rest-B)>7: continue
                for ksize in range(min(kappa,len(B))+1):
                    for kt in itertools.combinations(sorted(B),ksize):
                        K=set(kt)
                        if len(B-K)>7-kappa: continue
                        out.add((len(marked&(rest-B)),len(marked&B),len(marked&root),
                                 sum(u in K and v in K for u,v in edges),len(marked&K)))
    return out


def rows():
    feasible={(s,k):coordinates(s,k) for s in PROFILES for k in (5,6)}
    out=[]
    for rho in range(3):
      for shape,profile in PROFILES.items():
       n2=profile[0]
       for epsilon in (0,1):
        for alpha in range(n2-epsilon+1):
         beta=n2-epsilon-alpha
         for kappa in (5,6):
          for eta in range(5):
           for lam in range(max(0,beta-(7-kappa)),min(beta,kappa)+1):
            key=(f"m9-k4/rho={rho}/shape={shape}/alpha={alpha}/beta={beta}/"
                 f"epsilon={epsilon}/kappa={kappa}/eta={eta}/lambda={lam}")
            coord=(alpha,beta,epsilon,eta,lam)
            out.append((key,coord in feasible[shape,kappa]))
    return sorted(out)


def main():
    result=rows(); assert len(result)==len({k for k,_ in result})==2925
    assert sum(ok for _,ok in result)==1140
    keys="".join(k+"\n" for k,_ in result).encode("ascii")
    ledger="".join(f"{k}\t{'FEASIBLE' if ok else 'EMPTY'}\n" for k,ok in result).encode("ascii")
    assert hashlib.sha256(keys).hexdigest()==EXPECTED_KEY_HASH
    assert hashlib.sha256(ledger).hexdigest()==EXPECTED_LEDGER_HASH
    if len(sys.argv)==2:
        with open(sys.argv[1],"rb") as f: supplied=f.read()
        assert supplied==ledger
    elif len(sys.argv)!=1: raise SystemExit("usage: check_m9_k4_cover.py [ledger.txt]")
    print(f"PASS keys=2925 feasible=1140 empty=1785 ledger_sha256={EXPECTED_LEDGER_HASH}")


if __name__=="__main__": main()
