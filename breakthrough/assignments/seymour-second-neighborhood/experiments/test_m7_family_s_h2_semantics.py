#!/usr/bin/env python3
"""Independent semantic tests of gates, counters, and all 999 h=2 row units."""
import itertools,random
from check_m7_family_s_badness_cnf import Formula,and_gate,count,add_row,parse_row,A,B,C,ATYPES
from m7_family_s_h2_universe_check import independent_rows,swap

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def satisfies(clauses,val):return all(any(val[abs(z)]==(z>0)for z in q)for q in clauses)

def test_and():
    c=Formula();x=c.var('x');z=c.var('z');y=c.var('y');and_gate(c,y,x,z)
    for xb,zb,yb in itertools.product((False,True),repeat=3):
        val={x:xb,z:zb,y:yb};require(satisfies(c.clauses,val)==(yb==(xb and zb)),'and gate semantics')

def test_counter():
    rng=random.Random(0x5337)
    for n in range(1,18):
        c=Formula();xs=[c.var(f'x{i}')for i in range(n)];ys=count(c,xs,'t')
        samples=list(itertools.product((False,True),repeat=n))if n<=8 else[tuple(bool(rng.getrandbits(1))for _ in range(n))for _ in range(512)]
        for bits in samples:
            val={xs[i]:bits[i]for i in range(n)}
            for name,var in c.names.items():
                if name.startswith('cnt_t_'):
                    _,_,i,t=name.split('_');val[var]=sum(bits[:int(i)])>=int(t)
            require(satisfies(c.clauses,val),'counter defining clauses')
            require(all(val[y]==(sum(bits)>=k)for k,y in enumerate(ys,1)),'counter outputs')
            # Flip one output while retaining canonical other auxiliaries: exact
            # equivalence must make at least one defining clause false.
            if ys:
                y=ys[rng.randrange(len(ys))];bad=dict(val);bad[y]=not bad[y]
                require(not satisfies(c.clauses,bad),'counter admits flipped output')

def expected_arcs(row):
    state,dist,ac,bc,_=row;out={}
    ats=list(dist)+sum(([t]*n for t,n in enumerate(ac)),[])
    for u,t in zip([0,1,2]+list(range(3,9)),ats):
        for k,z in enumerate(C):out[u,z]='H'if ATYPES[t][k]else'I'
    bts=sum(([t]*n for t,n in enumerate(bc)),[])
    for b,t in zip(sorted(B),bts):
        for k,z in enumerate(C):out[b,z]=('O','I','H')[(t//3,t%3)[k]]
    out[16,17]=state
    return out

def test_rows():
    rows=sorted({min(r,swap(r))for r in independent_rows()});require(len(rows)==999,'row count')
    seen=set()
    for i,row in enumerate(rows):
        require(parse_row(__import__('json').dumps(row,separators=(',',':')))==row,f'row {i} parse')
        c=Formula();a=[[c.var(f'a_{u}_{v}')for v in range(18)]for u in range(18)];add_row(c,a,row)
        expect=expected_arcs(row);val={v:False for v in c.names.values()}
        # Fill all arc vars so that exactly the intended C-incidence units hold.
        for (u,z),symbol in expect.items():
            if (u,z)==(16,17):
                val[a[16][17]]=symbol=='01';val[a[17][16]]=symbol=='10';continue
            if u in A or u==0:
                val[a[u][z]]=False;val[a[z][u]]=symbol=='I'
            else:
                val[a[u][z]]=symbol=='I';val[a[z][u]]=symbol=='O'
        require(satisfies(c.clauses,val),f'row {i} intended units')
        for clause in c.clauses:
            require(len(clause)==1,f'row {i} nonunit')
            bad=dict(val);lit=clause[0];bad[abs(lit)]=not bad[abs(lit)]
            require(not satisfies([clause],bad),f'row {i} unit not fixed')
        signature=tuple(c.clauses);require(signature not in seen,f'row {i} duplicate literal signature');seen.add(signature)
    print('PASS independent auxiliary semantics and h2 fixed-row literals rows=999')
    print('PASS counter exhaustive widths=1..8 random_widths=9..17 samples_each=512 seed=0x5337')

def main():test_and();test_counter();test_rows()
if __name__=='__main__':main()
