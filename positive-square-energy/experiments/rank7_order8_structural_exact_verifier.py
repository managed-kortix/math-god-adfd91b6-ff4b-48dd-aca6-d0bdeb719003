#!/usr/bin/env python3
"""Read-only snapshot replay; no producer imports, numerical acceptance or theorem promotion."""
import hashlib
import json
import lzma
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAPSHOT = "cd74bca89019f92b08a7d9ba4ab494ed7794fa7a"
PINS = {'rank7_order8_theorem_eligible_combined_ledger.json': '69199fccf20574a133ffa605833b9abfecf692cae816571f25b50a4f986a233d', 'rank7_order8_after_packet_spectral_remainder.jsonl.xz': 'cc5ce720adb8d4ea650544dca5846462675d97433af9016313fce68e781e249b', 'rank7_order8_structural_cycle_gram_lane.json': '6e24ee40ee012565fdc11236c6c38345acb189e45044641795bb8938ff2736bc', 'rank7_order8_structural_cycle_gram_owners.jsonl.xz': '0d930818ee36a3b9dcd92ecbf5e72a3003b3a34abd6d93445a6870dd1585bef7', 'rank7_order8_after_structural_cycle_gram_remainder.jsonl.xz': '92cf8fd52a6aee253400b0bc1ae6753cd9b586608861c843486e2a6ab3c9e036', 'rank7_order8_next_structural_cycle_gram_lane.json': '3bc07246a784aa94f4166626299db544c9f6e28bcb8da9b288cff3159314514c', 'rank7_order8_next_structural_cycle_gram_owners.jsonl.xz': 'e298848502710680c1e2cd104068d2877380c26dfd839fe2109f15d0cce2b79b', 'rank7_order8_after_next_structural_cycle_gram_remainder.jsonl.xz': '263de7176faf01a67f0d2420f5c40ddc1ec31463a00fabd50c4ed743ea8b1621', 'rank7_order8_third_structural_cycle_gram_lane.json': '67c385d27dc28ef079d45a41a99b7ceb7cc247536b30feff57fed02f7f1f73dc', 'rank7_order8_third_structural_cycle_gram_owners.jsonl.xz': '7b88879db39db1a512ce6ff8d92997ec9007b7e4fbd205c5eced22c1fd052bfc', 'rank7_order8_after_third_structural_cycle_gram_remainder.jsonl.xz': '449ab5747999b1e6484d6c70408dfb86a8d0dc3ba14a69dd054bab011a6f285f'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def integer(x, minimum=0):
    require(type(x) is int and x >= minimum, "invalid integer")
    return x

def rational(x):
    require(type(x) is list and len(x) == 2, "rational shape")
    a, b = x
    integer(b, 1)
    require(type(a) is int, "rational numerator")
    y = F(a, b)
    require([y.numerator, y.denominator] == x, "noncanonical rational")
    return y

def canonical(x):
    # Decimal tokens are nonsemantic numerical hints only; preserve JSON spelling.
    if isinstance(x, Decimal):
        require(x.is_finite(), "nonfinite hint")
        return str(x)
    if type(x) is list:
        return "[" + ",".join(map(canonical, x)) + "]"
    if type(x) is dict:
        return "{" + ",".join(json.dumps(k)+":"+canonical(x[k]) for k in sorted(x)) + "}"
    return json.dumps(x, separators=(",", ":"), ensure_ascii=True, allow_nan=False)

def decode(raw, canonical_required=True):
    def pairs(items):
        d = {}
        for k,v in items:
            require(k not in d, "duplicate JSON key")
            d[k] = v
        return d
    def bad(s):
        raise ValueError("nonstandard JSON constant")
    x = json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                   parse_float=Decimal, parse_constant=bad)
    require(not canonical_required or (canonical(x)+"\n").encode("ascii") == raw, "noncanonical JSON")
    return x

def row(x):
    require(type(x) is list and len(x)==6, "row shape")
    for i in (0,1,2): integer(x[i])
    integer(x[5],1)
    edges, odds = x[3:5]
    require(type(edges) is list and type(odds) is list and len(edges)==len(odds), "edge shape")
    last=(-1,-1); degrees=[0]*8
    for e,o in zip(edges,odds):
        require(type(e) is list and len(e)==3, "edge triple")
        u,v,m=e
        integer(u); integer(v); integer(m,1); integer(o)
        require(u<v<8 and (u,v)>last and o<=m, "edge order/parity")
        last=(u,v); degrees[u]+=m; degrees[v]+=m
    require(sum(e[2] for e in edges)==14 and min(degrees)>=3, "kernel rank/degrees")
    return x

def transpose(a): return list(map(list,zip(*a)))
def mul(a,b):
    bt=transpose(b)
    return [[sum(x*y for x,y in zip(r,c)) for c in bt] for r in a]
def inverse(a):
    n=len(a); w=[[F(v) for v in r]+[F(i==j) for j in range(n)] for i,r in enumerate(a)]
    for c in range(n):
        pivot=next((r for r in range(c,n) if w[r][c]),None)
        require(pivot is not None,"singular incidence")
        w[c],w[pivot]=w[pivot],w[c]; z=w[c][c]; w[c]=[v/z for v in w[c]]
        for r in range(n):
            if r!=c:
                z=w[r][c]; w[r]=[v-z*t for v,t in zip(w[r],w[c])]
    return [r[n:] for r in w]

def check_projector(p,b):
    require(p==transpose(p) and mul(p,p)==p,"projector symmetry/idempotence")
    require(all(v==0 for r in mul(b,p) for v in r),"projector not cycle-valued")
    require(sum(p[i][i] for i in range(14))==7,"cycle rank")

def replay(owner):
    require(type(owner) is list and len(owner)==4,"owner shape")
    r,c,hint,stored_types=owner; row(r)
    require(type(hint) in (int,Decimal),"hint type")
    require(type(c) is list and len(c)==6,"certificate shape")
    require(type(c[0]) is int and c[0]==r[1] and c[1] is True,"source_index is not stream_index")
    stored_cost=rational(c[2]); stored_m=rational(c[3]); w=rational(c[5])
    require(w>=0,"negative cycle weight")
    s=[[F(0) for _ in range(8)] for _ in range(8)]; incident=[[] for _ in range(8)]; paths=[]
    for (u,v,m),o in zip(r[3],r[4]):
        s[u][v]=s[v][u]=m-2*o
        incident[u].append((m,o)); incident[v].append((m,o))
        for length in (([1]+[3]*(o-1)) if o else [])+[2]*(m-o): paths.append((u,v,length))
    keys=[(sum(s[u]),tuple(sorted(incident[u],reverse=True))) for u in range(8)]
    types=sorted(set(keys)); expected=[[int(k),[list(t) for t in ts]] for k,ts in types]
    require(stored_types==expected and canonical(stored_types)==canonical(expected),"wrong local types")
    require(type(c[4]) is list and len(c[4])==len(types),"parameter count")
    pars=[]
    for t in c[4]:
        require(type(t) is list and len(t)==2,"parameter shape")
        pars.append(tuple(map(rational,t)))
    b=[[F(0) for _ in paths] for _ in range(7)]; a=[[F(0) for _ in paths] for _ in range(8)]
    for j,(u,v,l) in enumerate(paths):
        if u<7:b[u][j]=1
        if v<7:b[v][j]=-1
        a[u][j]=1; a[v][j]=-1 if l%2 else 1
    cut=mul(mul(transpose(b),inverse(mul(b,transpose(b)))),b)
    p=[[F(i==j)-cut[i][j] for j in range(14)] for i in range(14)]
    check_projector(p,b)
    ap=mul(a,p); cycle=mul(ap,transpose(ap))
    require(cycle==mul(mul(a,p),transpose(a)),"cycle Gram identity")
    x=[]
    for u in range(8):
        d,t=pars[types.index(keys[u])]
        x.append([d*(u==v)+t*s[u][v] for v in range(8)])
    xx=mul(x,transpose(x)); H=[[xx[u][v]+w*cycle[u][v] for v in range(8)] for u in range(8)]
    M=max(H[u][u] for u in range(8)); require(M>0 and M==stored_m,"wrong normalizer")
    completion=[1-H[u][u]/M for u in range(8)]
    require(all(z>=0 for z in completion),"negative diagonal completion")
    G=[[H[u][v]/M+(completion[u] if u==v else 0) for v in range(8)] for u in range(8)]
    require(G==transpose(G) and all(G[u][u]==1 for u in range(8)),"unit Gram")
    terms=[]
    for u,v,L in paths:
        t=G[u][v]*(-1 if L%2 else 1)
        require(-1<t<=1,"invalid correlation")
        q=(1-t)/(1+t); require(q>=0,"negative path numerator")
        terms.append(q/L)
        # For every integer k>=0, q/L-q/(L+2k)=2kq/(L(L+2k))>=0.
        require(q/L-q/(L+2)==2*q/(L*(L+2)),"monotonic identity")
    cost=sum(terms); require(cost==stored_cost and cost<=6,"wrong cost")
    for j,(_,_,L) in enumerate(paths):
        frontier=cost-terms[j]+terms[j]*F(L,L+2)
        require(0<=frontier<=cost<=6,"frontier budget")
    return r

def partition(source, owners, remainder):
    byid={}; last=-1
    for payload in owners:
        r=replay(payload); require(r[0]>last,"owner order/overlap"); last=r[0]
        byid[r[0]]=r
    expected=[]; consumed=set(); ids=set(); prev=-1
    for raw in source:
        r=row(decode(raw)); require(r[0]>prev and r[1] not in ids,"source duplicate/order")
        prev=r[0]; ids.add(r[1])
        if r[0] in byid:
            require(r==byid[r[0]],"owner not exact source row"); consumed.add(r[0])
        else: expected.append(raw)
    require(consumed==set(byid),"owner omission from source")
    require(expected==remainder,"not ordered byte complement")

def artifact(name):
    raw=(HERE/name).read_bytes()
    require(hashlib.sha256(raw).hexdigest()==PINS[name],"immutable artifact changed: "+name)
    return raw

def stream(info):
    require(type(info) is dict and set(info)=={"path","record_total","raw_sha256","artifact_sha256"},"stream schema")
    require(info["path"] in PINS and info["artifact_sha256"]==PINS[info["path"]],"stream pin")
    raw=lzma.decompress(artifact(info["path"])); lines=raw.splitlines(keepends=True)
    require(type(info["record_total"]) is int and len(lines)==info["record_total"] and hashlib.sha256(raw).hexdigest()==info["raw_sha256"],"raw stream authentication")
    for line in lines: decode(line)
    return lines

def main():
    ledger=decode(artifact("rank7_order8_theorem_eligible_combined_ledger.json"))
    info=ledger["exact_remainder_stream"]; source=stream(info)
    previous="rank7_order8_theorem_eligible_combined_ledger.json"
    counts=[83856,83744,83647,83611]
    for i,prefix in enumerate(("","next_","third_")):
        name="rank7_order8_"+prefix+"structural_cycle_gram_lane.json"
        report=decode(artifact(name), canonical_required=False)
        require(report["source_ledger"]=={"path":previous,"sha256":PINS[previous]} and report["source_stream"]==info,"source chain")
        require(report["full_theorem"] is False,"claim boundary")
        require(report["scanned_remainder_total"]==counts[i] and report["remaining_remainder_total"]==counts[i+1],"lane counts")
        owners=[decode(x) for x in stream(report["owner_stream"])]; rem=stream(report["reduced_remainder_stream"])
        require(len(source)==counts[i] and len(rem)==counts[i+1] and len(owners)==counts[i]-counts[i+1],"partition counts")
        require(report["owned_orbit_total"]==len(owners) and report["owned_target_total"]==15*len(owners),"owner counts")
        require(report["theorem_lift"]=={
            "all_length":"for fixed parity and Gram, each nonnegative path cost (1-t)/(L(1+t)) weakly decreases when L increases by two",
            "induced_owner":"each accepted kernel realization is owned together with every same-parity subdivision it induces",
            "rooted_trees":"DNN one-vertex additivity supplies arbitrary rooted-tree attachments"},"lift contract")
        partition(source,owners,rem)
        source=rem; info=report["reduced_remainder_stream"]; previous=name
    print("structural I-III exact read-only replay: PASS")
    print("83856 -> 83744 -> 83647 -> 83611; owners=245; frontier_costs=3675")
    print("all-length monotonicity verified; rooted-tree lift conditional on DNN one-vertex additivity")

if __name__=="__main__": main()
