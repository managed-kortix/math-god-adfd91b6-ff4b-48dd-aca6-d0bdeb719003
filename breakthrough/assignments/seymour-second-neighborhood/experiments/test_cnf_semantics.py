#!/usr/bin/env python3
"""Pure exhaustive mutation tests for the CNF gate/counter semantics."""
import itertools
from snc_cnf import CNF, equiv_and, threshold


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


if __name__=='__main__':
    test_threshold(); test_graph_semantics()
