#!/usr/bin/env python3
"""Pure exhaustive mutation tests for the CNF gate/counter semantics."""
import itertools
from snc_cnf import CNF, equiv_and, threshold, add_mu2_link, add_witness_for_deleted


def satisfied(clauses, values):
    return all(any(values[abs(x)] == (x > 0) for x in clause)
               for clause in clauses)


def test_threshold(limit=8):
    for length in range(1, limit + 1):
        for bits in itertools.product((False, True), repeat=length):
            c=CNF(); xs=[c.var(f"x{i}") for i in range(length)]
            ys=threshold(c,xs,"t")
            values={xs[i]:bits[i] for i in range(length)}
            total=sum(bits)
            # Fill every intermediate counter by its documented meaning.
            for name,var in c.names.items():
                if name.startswith("cnt_t_"):
                    _,_,i,t=name.split("_")
                    values[var]=sum(bits[:int(i)]) >= int(t)
            assert satisfied(c.clauses,values),(length,bits)
            for y in ys:
                bad=dict(values); bad[y]=not bad[y]
                assert not satisfied(c.clauses,bad),(length,bits,y)
    print(f"PASS exact thresholds through length {limit}")


def test_mu2(limit=8):
    for width in range(3,limit+1):
        for d1 in range(width+1):
            for d2 in range(width+1):
                c=CNF(); outs=[c.var(f"o{i}") for i in range(width)]
                secs=[c.var(f"s{i}") for i in range(width)]; z=c.var("z")
                c.add(outs[0])
                for t in range(1,width): c.add(-secs[t-1],outs[t])
                c.add(-secs[width-1])
                for t in range(3,width+1): c.add(-outs[t-1],secs[t-3])
                add_mu2_link(c,outs,secs,z)
                base={outs[i]:d1>=i+1 for i in range(width)}
                base.update({secs[i]:d2>=i+1 for i in range(width)})
                valid=[]
                for zv in (False,True):
                    values=dict(base); values[z]=zv
                    if satisfied(c.clauses,values): valid.append(zv)
                expected=[]
                if d1-d2==1: expected=[False]
                elif d1-d2==2: expected=[True]
                assert valid==expected,(width,d1,d2,valid,expected)
    print(f"PASS exact mu2 linkage through width {limit}")


def semantic_cnf(n):
    c=CNF(); a=[[c.var(f"a_{i}_{j}") for j in range(n)] for i in range(n)]
    q=[[c.var(f"q_{i}_{j}") for j in range(n)] for i in range(n)]
    pvars={}; rvars={}
    for i in range(n): c.add(-a[i][i]); c.add(-q[i][i])
    for i in range(n):
        for j in range(i+1,n): c.add(-a[i][j],-a[j][i])
    for i in range(n):
        for j in range(n):
            if i==j: continue
            ps=[]
            for k in range(n):
                if k in (i,j): continue
                p=c.var(f"p_{i}_{k}_{j}"); pvars[i,k,j]=p; ps.append(p)
                equiv_and(c,p,a[i][k],a[k][j])
            r=c.var(f"r_{i}_{j}"); rvars[i,j]=r
            for x in ps: c.add(-x,r)
            c.add(-r,*ps)
            c.add(-q[i][j],r); c.add(-q[i][j],-a[i][j]); c.add(q[i][j],-r,a[i][j])
    return c,a,q,pvars,rvars


def test_graph_semantics(limit=4):
    checked=0
    for n in range(1,limit+1):
        c,a,q,pvars,rvars=semantic_cnf(n)
        pairs=list(itertools.combinations(range(n),2))
        for states in itertools.product(range(3),repeat=len(pairs)):
            arcs=set()
            for state,(i,j) in zip(states,pairs):
                if state==1: arcs.add((i,j))
                elif state==2: arcs.add((j,i))
            values={}
            for i in range(n):
                for j in range(n): values[a[i][j]]=(i,j) in arcs
            for (i,k,j),var in pvars.items(): values[var]=(i,k) in arcs and (k,j) in arcs
            for (i,j),var in rvars.items(): values[var]=any((i,k) in arcs and (k,j) in arcs for k in range(n))
            for i in range(n):
                for j in range(n):
                    exact=i!=j and (i,j) not in arcs and any((i,k) in arcs and (k,j) in arcs for k in range(n))
                    values[q[i][j]]=exact
            assert satisfied(c.clauses,values),(n,arcs)
            # Every q bit is forced: flipping it must violate the clauses under
            # the independently computed gate assignment.
            for i in range(n):
                for j in range(n):
                    bad=dict(values); bad[q[i][j]]=not bad[q[i][j]]
                    assert not satisfied(c.clauses,bad),(n,arcs,i,j)
            checked+=1
        print(f"PASS CNF semantics n={n} graphs={3**len(pairs)}")
    print(f"PASS CNF semantic total={checked}")


def test_witness_semantics(limit=4):
    checked=0
    for n in range(2,limit+1):
        c,a,q,pvars,rvars=semantic_cnf(n)
        mu2=[c.var(f"mu2_{i}") for i in range(n)]
        # Add witness family for one deletion at a time to keep selectors small.
        pairs=list(itertools.combinations(range(n),2))
        for states in itertools.product(range(3),repeat=len(pairs)):
            arcs=set()
            for state,(i,j) in zip(states,pairs):
                if state==1: arcs.add((i,j))
                elif state==2: arcs.add((j,i))
            n1=[{j for j in range(n) if (i,j) in arcs} for i in range(n)]
            n2=[]
            for i in range(n):
                reach={b for k in n1[i] for b in n1[k]}
                n2.append(reach-n1[i]-{i})
            base={a[i][j]:(i,j) in arcs for i in range(n) for j in range(n)}
            for (i,k,j),var in pvars.items(): base[var]=(i,k) in arcs and (k,j) in arcs
            for (i,j),var in rvars.items(): base[var]=any((i,k) in arcs and (k,j) in arcs for k in range(n))
            for i in range(n):
                base[mu2[i]]=len(n1[i])-len(n2[i])!=1
                for j in range(n): base[q[i][j]]=j in n2[i]
            for u in range(n):
                wc=CNF(); wc.names=dict(c.names); wc.clauses=list(c.clauses)
                add_witness_for_deleted(wc,n,u,a,q,pvars,mu2)
                candidates=[]
                for w in range(n):
                    if w==u or (w,u) not in arcs or len(n1[w])-len(n2[w])!=1: continue
                    remaining=set(range(n))-{u}
                    arcs2={(x,y) for x,y in arcs if x!=u and y!=u}
                    n1new={y for y in remaining if (w,y) in arcs2}
                    reach={b for k in n1new for b in remaining if (k,b) in arcs2}
                    n2new=reach-n1new-{w}
                    if n2new==n2[w]: candidates.append(w)
                selectors=[wc.names[f"wit_{w}_{u}"] for w in range(n) if w!=u]
                exists=False
                for bits in itertools.product((False,True),repeat=len(selectors)):
                    values=dict(base); values.update(dict(zip(selectors,bits)))
                    sat=satisfied(wc.clauses,values)
                    selected={w for w in range(n) if w!=u and values[wc.names[f"wit_{w}_{u}"]]}
                    assert sat==(bool(selected) and selected<=set(candidates)),(n,arcs,u,selected,candidates)
                    exists |= sat
                assert exists==bool(candidates),(n,arcs,u,candidates)
                checked+=1
    print(f"PASS robust witness semantics cases={checked}")


if __name__=='__main__':
    test_threshold(); test_mu2(); test_graph_semantics(); test_witness_semantics()
