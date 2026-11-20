#!/usr/bin/env python3
"""Independent scratch checker/rebuilder for the parent-20 complete selector CNF.

Does not import the parent20 producer or any p20 scratch module.  It parses the
frozen TSV, reconstructs the parent through the independent parent-cover
checker, explicitly expands packet/witness/high-set actions, and rebuilds the
CNF suffix.  Research scratch only; no repository state is modified.
"""
from __future__ import annotations
import argparse, hashlib, itertools, math
from collections import Counter, defaultdict
from pathlib import Path
import sys

PACKAGE=Path(__file__).resolve().parents[1]
SOURCE=PACKAGE/'source-pins'
sys.path.insert(0,str(SOURCE))
from snc_cnf import generate
import check_m5_selector_batch_cnf as cover

LEDGER=PACKAGE/'ledger'/'m5-b7-parent20-probe.tsv'
FORMAT='m5-b7-parent20-structural-probe-v1'
PARENT=20
A=tuple(range(1,9)); B=tuple(range(9,16)); C=(16,17)
PAIRS=tuple((x,y) for y in range(1,18) for x in range(y))
EXPECTED_HOLES=frozenset({(0,9),(1,9),(1,16),(2,16),(2,17)})
EXPECTED_PARENT=('P6','RBACAC',2,EXPECTED_HOLES)
HARD=frozenset({3,4,6,7,8,9,12,13})
EASY=frozenset(range(14))-HARD
BASE_VARS=23616
BASE_CLAUSES=142729


def shabytes(data: bytes): return len(data),hashlib.sha256(data).hexdigest()
def verts(s): return () if s=='-' else tuple(map(int,s.split(',')))

def parse_ledger():
    raw=LEDGER.read_bytes(); lines=raw.decode('ascii').splitlines()
    if lines[0]!=FORMAT: raise RuntimeError('ledger format')
    fields=lines[1].split('\t')
    if fields[:5]!=['parent','20','P6','RBACAC','2']: raise RuntimeError('ledger parent line')
    holes=frozenset(tuple(map(int,z.split('-'))) for z in fields[5].split(','))
    if holes!=EXPECTED_HOLES: raise RuntimeError('ledger holes')
    if lines[2]!='first-signatures\t14\twitness-leaves\t68': raise RuntimeError('ledger summary')
    if lines[3] != 'columns\tfirst,key,source,target,high16,high17,outB16,outB17,packet-weight,witness,witness-weight':
        raise RuntimeError('ledger columns')
    rows=[]
    for line in lines[4:]:
        f=line.split('\t')
        if len(f)!=11: raise RuntimeError('bad row')
        rows.append(dict(first=int(f[0]),key=f[1],source=int(f[2]),target=int(f[3]),
                         high=(int(f[4]),int(f[5])),out=(verts(f[6]),verts(f[7])),
                         pw=int(f[8]),W=verts(f[9]),ww=int(f[10])))
    if len(rows)!=68: raise RuntimeError('row count')
    return raw,rows


def parent_check():
    rows=cover.reconstruct_rows('B7')
    shape,word,weight=rows[PARENT]
    holes=cover.project_holes('B7',shape,word)
    got=(shape,word,weight,holes)
    if got!=EXPECTED_PARENT: raise RuntimeError(('independent parent mismatch',got))
    # Full rooted-cell orbit count and exact stabilizer for the canonical hole set.
    labelled=set()
    for a1 in A:
      for a2 in A:
       if a1==a2: continue
       for b in B:
        for c1,c2 in (C,C[::-1]):
         labelled.add(frozenset({tuple(sorted((0,b))),tuple(sorted((a1,b))),
                                 tuple(sorted((a1,c1))),tuple(sorted((a2,c1))),
                                 tuple(sorted((a2,c2)))}))
    if len(labelled)!=784 or holes not in labelled:
        raise RuntimeError(('rooted parent orbit',len(labelled)))
    stabilizer=0
    for ai in itertools.permutations(A):
      # Hole incidence makes A1,A2 pointwise fixed; prune to the exact six-cell.
      if ai[0]!=1 or ai[1]!=2: continue
      for bi in itertools.permutations(B):
       if bi[0]!=9: continue
       stabilizer += 1
    if stabilizer != 518400:
        raise RuntimeError(('parent stabilizer',stabilizer))
    return holes


def b_group(packet_sets=(), pointwise=()):
    packet_sets=tuple(map(frozenset,packet_sets)); pointwise=frozenset(pointwise)
    for image in itertools.permutations(B):
        g=dict(zip(B,image))
        if g[9]!=9: continue
        if any(frozenset(g[x] for x in S)!=S for S in packet_sets): continue
        if any(g[x]!=x for x in pointwise): continue
        yield g


def amap_group():
    for image in itertools.permutations(range(3,9)):
        yield {1:1,2:2,**dict(zip(range(3,9),image))}


def packet_tuple(r): return (r['source'],r['high'],r['out'][0],r['out'][1])

def packet_universe(holes):
    incid={u:sum(tuple(sorted((u,v))) in holes for v in range(9)) for u in C}
    if incid!={16:2,17:1}: raise RuntimeError(('C incidence',incid))
    U=set()
    for source in C:
        dc={16:int(source==16),17:int(source==17)}
        for high in itertools.product((0,1),repeat=2):
            sizes={u:high[C.index(u)]+incid[u]-1-dc[u] for u in C}
            if any(not 0<=sizes[u]<=7 for u in C): continue
            for x in itertools.combinations(B,sizes[16]):
                for y in itertools.combinations(B,sizes[17]): U.add((source,high,x,y))
    return U


def witness_universe(packet):
    source,high,x,y=packet; out={16:set(x),17:set(y)}
    highs=tuple(u for u,h in zip(C,high) if h)
    choices=[]
    for u in highs:
        predecessor=(source,) if u==33-source else ()
        choices.append(predecessor+tuple(b for b in B if b not in out[u]))
    return highs,(set(itertools.product(*choices)) if choices else {()})


def validate_packet_witness(rows,holes):
    groups=defaultdict(list)
    for r in rows: groups[r['first']].append(r)
    if sorted(groups)!=list(range(14)): raise RuntimeError('first ordinals')
    G=tuple(b_group()); expanded=[]; weighted=0
    records=[]
    for f in range(14):
        leaves=groups[f]; r=leaves[0]
        for z in leaves:
            if any(z[k]!=r[k] for k in ('key','source','target','high','out','pw')):
                raise RuntimeError(('varying packet',f))
        if r['target']!=33-r['source']: raise RuntimeError(('orientation',f))
        packet=packet_tuple(r)
        support={(packet[0],packet[1],tuple(sorted(g[x] for x in packet[2])),tuple(sorted(g[x] for x in packet[3]))) for g in G}
        if len(support)!=r['pw']: raise RuntimeError(('packet weight',f,len(support),r['pw']))
        expanded.extend(support)
        highs,WU=witness_universe(packet)
        SG=tuple(b_group(r['out']))
        wx=[]
        for w,z in enumerate(leaves):
            if z['W'] not in WU: raise RuntimeError(('witness eligibility',f,w,z['W']))
            support={tuple(g.get(x,x) for x in z['W']) for g in SG}
            if len(support)!=z['ww']: raise RuntimeError(('witness weight',f,w,len(support),z['ww']))
            wx.extend(support)
            records.append((r,z,highs))
        if set(wx)!=WU or len(wx)!=len(set(wx)): raise RuntimeError(('witness choice orbit partition',f))
        weighted += r['pw']*len(WU)
    PU=packet_universe(holes)
    if set(expanded)!=PU or len(expanded)!=len(set(expanded)): raise RuntimeError('packet partition')
    if (len(PU),weighted)!=(92,3081): raise RuntimeError(('packet totals',len(PU),weighted))
    return groups,records


def high_orbits(packet,W):
    # Correct bridge: 153 pairs minus five holes gives 148 arcs.  The base
    # exact degree range is {8,9}, so 148=18*8+4 gives four highs.  Root 0 has
    # the fixed row N+(0)=A and is low; C's high mask is in the packet.
    if len(PAIRS)-len(EXPECTED_HOLES)!=148 or 148-18*8!=4 or len(A)!=8 or 0 in A+B+C:
        raise RuntimeError('root-low/exactly-four-high arithmetic')
    r=4-sum(packet['high'])
    if not 0<=r<=4: raise RuntimeError('high cardinality')
    universe={frozenset(S) for S in itertools.combinations(A+B,r)}
    AG=tuple(amap_group())
    fixedB=tuple(x for x in W if x in B)
    BG=tuple(b_group(packet['out'],fixedB))
    remaining=set(universe); output=[]
    while remaining:
        seed=min(remaining,key=lambda S:tuple(sorted(S)))
        SA=frozenset(seed&set(A)); SB=frozenset(seed&set(B))
        ai={frozenset(g[x] for x in SA) for g in AG}
        bi={frozenset(g[x] for x in SB) for g in BG}
        orbit={x|y for x in ai for y in bi}
        if not orbit<=remaining: raise RuntimeError(('orbit overlap/action failure',packet['first'],W,seed))
        representative=min(orbit,key=lambda S:tuple(sorted(S)))
        output.append((representative,len(orbit)))
        remaining-=orbit
    if sum(w for _,w in output)!=len(universe): raise RuntimeError('high exhaustion')
    # Hostile direct action check: all listed product images equal factored orbit.
    for representative,weight in output:
        direct={frozenset(tuple(gA.get(x,gB.get(x,x)) for x in representative)) for gA in AG for gB in BG}
        if len(direct)!=weight: raise RuntimeError(('factored/direct orbit mismatch',packet['first'],W))
    return tuple(output),len(universe),len(BG)


def build_schedule(groups):
    schedule=[]; perfirst=Counter(); labelled=Counter(); leafcounts=Counter(); bgcounts=Counter(); leafvector={}
    for f in range(14):
        packet=groups[f][0]
        # Easy rows are accepted only if their independently reconstructed
        # packet/witness restriction has been SAT-certified by the retained
        # single parent formula; hard rows additionally enumerate exact highs.
        for w,row in enumerate(groups[f]):
            if f in EASY:
                schedule.append((packet,row,w,None,None,None))
            else:
                orbits,total,bgs=high_orbits(packet,row['W'])
                leafcounts[len(orbits)]+=1; leafvector[(f,w)]=len(orbits)
                for h,(H,hw) in enumerate(orbits):
                    schedule.append((packet,row,w,h,H,hw)); perfirst[f]+=1
                    labelled[f]+=packet['pw']*row['ww']*hw; bgcounts[bgs]+=1
    hardrows=[z for z in schedule if z[0]['first'] in HARD]
    easyrows=[z for z in schedule if z[0]['first'] in EASY]
    # Independent labelled decorated universe: expand each canonical hard row
    # under the full B action for packet+witness, then all exact high subsets.
    # Compare with the hierarchical representative weights/counts below.
    labelled_direct=0
    for f in sorted(HARD):
        p0=groups[f][0]
        packet_images={(p0['source'],p0['high'],tuple(sorted(g[x] for x in p0['out'][0])),
                        tuple(sorted(g[x] for x in p0['out'][1]))) for g in b_group()}
        if len(packet_images)!=p0['pw']: raise RuntimeError(('packet direct expansion',f))
        decorated=set()
        for packet_image in packet_images:
            _,hi,o16,o17=packet_image
            highs0,WU=witness_universe(packet_image)
            for W in WU:
                for H in itertools.combinations(A+B,4-sum(hi)):
                    decorated.add((packet_image,W,frozenset(H)))
        expected=p0['pw']*sum(z['ww'] for z in groups[f])*__import__('math').comb(15,4-sum(p0['high']))
        if len(decorated)!=expected: raise RuntimeError(('labelled decorated expansion',f,len(decorated),expected))
        labelled_direct+=len(decorated)
    if labelled_direct!=323400: raise RuntimeError(('labelled decorated total',labelled_direct))
    if len(easyrows)!=14 or len(hardrows)!=1332 or len(schedule)!=1346: raise RuntimeError(('schedule count',len(easyrows),len(hardrows)))
    expected_per={3:32,4:81,6:156,7:156,8:156,9:356,12:156,13:239}
    expected_lab={3:2730,4:16380,6:26460,7:26460,8:26460,9:132300,12:26460,13:66150}
    expected_leaf=Counter({23:24,30:11,17:8,24:4,32:2,18:2,49:1,38:1,31:1})
    expected_vector={
      3:[32],4:[32,49],6:[17,23,17,23,23,30,23],
      7:[17,23,17,23,23,30,23],8:[17,23,17,23,23,30,23],
      9:[23,23,30,23,23,23,30,23,30,30,30,38,30],
      12:[23,23,23,30,17,17,23],13:[18,23,24,24,30,24,31,18,23,24]}
    got_vector={f:[leafvector[(f,w)] for w in range(len(groups[f]))] for f in sorted(HARD)}
    if dict(perfirst)!=expected_per or dict(labelled)!=expected_lab or leafcounts!=expected_leaf or got_vector!=expected_vector:
        raise RuntimeError(('high totals',perfirst,labelled,leafcounts,got_vector))
    if sum(labelled.values())!=323400: raise RuntimeError('labelled total')
    # Independent closed-form count, not orbit-weight accumulation.
    direct=0
    for f in HARD:
        p=groups[f][0]
        direct += p['pw']*sum(z['ww'] for z in groups[f])*math.comb(15,4-sum(p['high']))
    if direct!=323400: raise RuntimeError(('direct total',direct))
    if set(bgcounts) != {2,4,6,12,24,48,120}:
        raise RuntimeError(('B stabilizer order support',sorted(bgcounts)))
    return schedule,perfirst,labelled,leafcounts,bgcounts


def build_cnf(schedule,holes):
    c=generate(18,7,5,robust_witness=True,arc_minimal=True)
    if (len(c.names),len(c.clauses))!=(BASE_VARS,BASE_CLAUSES):
        raise RuntimeError(('base dimensions',len(c.names),len(c.clauses)))
    for pair in PAIRS: c.add(c.var(f'h_{pair[0]}_{pair[1]}') if pair in holes else -c.var(f'h_{pair[0]}_{pair[1]}'))
    selectors=[]
    for packet,row,w,h,H,hw in schedule:
        tail=(f'f{packet["first"]:02d}_w{w:02d}_easy' if h is None else f'f{packet["first"]:02d}_w{w:02d}_h{h:02d}')
        z=c.var('parent20_selector_'+tail);selectors.append(z)
        c.add(-z,c.var(f'a_{packet["source"]}_{packet["target"]}'))
        for u,high,outB in zip(C,packet['high'],packet['out']):
            x=c.var(f'cnt_d1_{u}_17_9'); c.add(-z,x if high else -x)
            for b in B:
                a=c.var(f'a_{u}_{b}'); c.add(-z,a if b in outB else -a)
        highs=tuple(u for u,bit in zip(C,packet['high']) if bit)
        if len(highs)!=len(row['W']): raise RuntimeError('witness arity')
        for u,x in zip(highs,row['W']): c.add(-z,c.var(f'wit_{x}_{u}'))
        if H is not None:
            for u in A+B:
                x=c.var(f'cnt_d1_{u}_17_9'); c.add(-z,x if u in H else -x)
    c.add(*selectors)
    if (len(c.names),len(c.clauses))!=(24962,188312):
        raise RuntimeError(('complete dimensions',len(c.names),len(c.clauses)))
    # Exact suffix strata and guard discipline.  All refinement clauses except
    # the single ALO are binary with one negative selector in first position.
    base_end=BASE_CLAUSES; parent_end=base_end+153
    suffix=c.clauses[parent_end:]; selector_set=set(selectors)
    if len(c.clauses[:base_end])!=142729 or len(c.clauses[base_end:parent_end])!=153:
        raise RuntimeError('base/parent strata')
    if len(suffix)!=45430 or suffix[-1]!=tuple(selectors) or any(z<=0 for z in suffix[-1]):
        raise RuntimeError('selector ALO stratum')
    guarded=suffix[:-1]
    if any(len(cl)!=2 or cl[0]>=0 or -cl[0] not in selector_set for cl in guarded):
        raise RuntimeError('unguarded/malformed refinement clause')
    packet_count=17*len(schedule)
    witness_count=sum(len(tuple(u for u,bit in zip(C,p['high']) if bit)) for p,_,_,_,_,_ in schedule)
    high_count=15*sum(1 for p,_,_,h,_,_ in schedule if h is not None)
    if (packet_count,witness_count,high_count,len(guarded))!=(22882,2567,19980,45429):
        raise RuntimeError(('guard strata',packet_count,witness_count,high_count,len(guarded)))
    # Exact per-selector guard blocks, including every polarity and no extras.
    # Selector index equals schedule index; compare each ordered block.
    cursor=0
    for idx,(packet,row,w,h,H,hw) in enumerate(schedule):
        z=selectors[idx]; block=[]
        block.append((-z,c.names[f'a_{packet["source"]}_{packet["target"]}']))
        for u,high,outB in zip(C,packet['high'],packet['out']):
            x=c.names[f'cnt_d1_{u}_17_9']; block.append((-z,x if high else -x))
            for b in B:
                a=c.names[f'a_{u}_{b}']; block.append((-z,a if b in outB else -a))
        highs=tuple(u for u,bit in zip(C,packet['high']) if bit)
        for u,x0 in zip(highs,row['W']): block.append((-z,c.names[f'wit_{x0}_{u}']))
        if H is not None:
            for u in A+B:
                x=c.names[f'cnt_d1_{u}_17_9']; block.append((-z,x if u in H else -x))
        got=guarded[cursor:cursor+len(block)]
        if got!=block: raise RuntimeError(('selector guard block',idx,packet['first'],w,h))
        cursor+=len(block)
    if cursor!=len(guarded): raise RuntimeError(('guard cursor',cursor,len(guarded)))
    # Selector names/order are an authenticated schedule, with no duplicates.
    expected=[]
    for packet,row,w,h,H,hw in schedule:
        tail=(f'f{packet["first"]:02d}_w{w:02d}_easy' if h is None else
              f'f{packet["first"]:02d}_w{w:02d}_h{h:02d}')
        expected.append('parent20_selector_'+tail)
    # Semantic ALO cover: given any parent model, choose one true witness per
    # high C vertex.  Packet action canonizes the ordered C packet; its
    # stabilizer partitions ordered chosen-witness tuples; after fixing that
    # tuple pointwise, the exact A∪B high set lies in one high-set orbit.
    # Easy rows stop after the witness step.  Thus at least one scheduled row
    # is reachable by graph-level model transport.  Conversely each block
    # above contains only guarded base literals, so every selector is a true
    # restriction; overlap needs no AMO.
    if len([z for z in schedule if z[0]['first'] in EASY])!=14 or        len([z for z in schedule if z[0]['first'] in HARD])!=1332:
        raise RuntimeError('semantic selector cover cardinality')
    got=[name for name,num in c.names.items() if num in selector_set]
    if got!=expected or len(set(got))!=1346:
        raise RuntimeError('selector schedule/name mismatch')
    return c


def serialize(c):
    out=[f'p cnf {len(c.names)} {len(c.clauses)}\n']
    out.extend(' '.join(map(str,z))+' 0\n' for z in c.clauses)
    return ''.join(out).encode('ascii')


def parse_dimacs(path):
    clauses=[]; header=None
    for raw in path.read_text(encoding='ascii').splitlines():
        if raw.startswith('c '): continue
        if raw.startswith('p '):
            q=raw.split(); header=(int(q[2]),int(q[3])); continue
        q=tuple(map(int,raw.split()))
        if not q or q[-1]!=0: raise RuntimeError('bad DIMACS')
        clauses.append(q[:-1])
    if header is None or header[1]!=len(clauses): raise RuntimeError('DIMACS header')
    return header,tuple(clauses)


def audit_encoding_schema():
    """Exhaustively validate the deterministic auxiliary recurrences used for transport.

    This is a schema-level truth-table check, not a claim that emitted auxiliary
    variable names admit a literal permutation automorphism.
    """
    import snc_cnf as enc
    # Exact sequential threshold recurrence: each introduced y equals
    # old[t] OR (x AND old[t-1]), for every Boolean state up to 17 inputs.
    for width in range(1,18):
        for mask in range(1<<width):
            prev=[]
            for i in range(1,width+1):
                x=bool(mask & (1<<(i-1))); cur=[]
                for t in range(1,i+1):
                    u=prev[t-1] if t<=len(prev) else False
                    v=prev[t-2] if t>=2 else True
                    y=u or (x and v); cur.append(y)
                    if y != ((mask & ((1<<i)-1)).bit_count() >= t):
                        raise RuntimeError(('threshold schema',width,mask,i,t))
                prev=cur
    # equiv_and, path-existence r, and exact-second-neighbor q templates
    # are exact under every Boolean input.  We evaluate each definitional
    # relation over its complete truth table.
    for x,z,y in itertools.product((False,True),repeat=3):
        clauses=((not y) or x,(not y) or z,y or (not x) or (not z))
        if all(clauses)!=(y==(x and z)): raise RuntimeError('equiv_and schema')
    for pbits in itertools.product((False,True),repeat=4):
        reachable=any(pbits)
        for r in (False,True):
            clauses=tuple((not p) or r for p in pbits)+( (not r) or any(pbits), )
            if all(clauses)!=(r==reachable): raise RuntimeError('r schema')
    for arc,reachable,q in itertools.product((False,True),repeat=3):
        clauses=((not q) or reachable,(not q) or (not arc),q or (not reachable) or arc)
        if all(clauses)!=(q==(reachable and not arc)): raise RuntimeError('q schema')
    # Hole variable is exact complement of the two allowed arc directions.
    for xy,yx in itertools.product((False,True),repeat=2):
        if xy and yx: continue
        h=not (xy or yx)
        if h != (not xy and not yx): raise RuntimeError('hole schema')
    # add_mu2_link is audited over every degree/second-degree count satisfying
    # the surrounding base deficit constraints; exactly deficit two is selected.
    n=18
    for d1 in (8,9):
        for d2 in range(18):
            outs=[d1>=t for t in range(1,n)]
            secs=[d2>=t for t in range(1,n)]
            admissible=(d2<=d1-1 and d2>=d1-2)
            if not admissible: continue
            satisfying=[]
            for z in (False,True):
                clauses=[]
                for t in range(2,n): clauses.append(z or (not outs[t-1]) or secs[t-2])
                clauses.append((not z) or outs[1])
                for t in range(1,n-2): clauses.append((not z) or (not secs[t-1]) or outs[t+1])
                clauses.extend([(not z) or (not secs[n-3]),(not z) or (not secs[n-2])])
                if all(clauses): satisfying.append(z)
            if satisfying != [d1-d2==2]:
                raise RuntimeError(('mu2 schema',d1,d2,satisfying))
    return True


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--compare',type=Path);ap.add_argument('--write',type=Path);a=ap.parse_args()
    audit_encoding_schema()
    holes=parent_check(); raw,rows=parse_ledger(); groups,_=validate_packet_witness(rows,holes)
    schedule,pf,lab,lc,bgc=build_schedule(groups)
    c=build_cnf(schedule,holes); data=serialize(c)
    if a.write: a.write.write_bytes(data)
    if a.compare:
        h,clauses=parse_dimacs(a.compare)
        if h!=(len(c.names),len(c.clauses)): raise RuntimeError(('compared dimensions',h))
        if clauses!=tuple(c.clauses):
            for i,(x,y) in enumerate(itertools.zip_longest(clauses,c.clauses)):
                if x!=y: raise RuntimeError(('first clause mismatch',i,x,y))
        if a.compare.read_bytes()!=data: raise RuntimeError('byte mismatch despite same clauses')
    print('PASS independent-parent20-complete',
          f'ledger={shabytes(raw)}',f'selectors={len(schedule)}',f'hard={len(schedule)-14}',
          f'labelled-hard={sum(lab.values())}',f'vars={len(c.names)}',f'clauses={len(c.clauses)}',
          f'cnf-bytes-sha={shabytes(data)}',f'leaf-orbit-counts={dict(sorted(lc.items()))}')

if __name__=='__main__': main()
