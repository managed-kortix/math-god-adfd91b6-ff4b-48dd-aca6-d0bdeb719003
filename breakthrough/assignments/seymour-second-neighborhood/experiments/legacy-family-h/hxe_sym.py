import sys
sys.path.insert(0,'/tmp');import h_qrow_exact as h
case=sys.argv[1];rob=bool(int(sys.argv[2]));out=sys.argv[3]
c,info=h.build(case,rob);R,G1,G2,rows=info
# Canonical status O<I<H along each root-layer group and C pair.
def sorted_status(group):
 for u,v in zip(group,group[1:]):
  # status(u) <= status(v): v=O implies u=O
  c.add(-c.var(f'a_1_{v}'),c.var(f'a_1_{u}'))
  # v=I implies u not H (i.e. q->u or u->q)
  c.add(-c.var(f'a_{v}_1'),c.var(f'a_1_{u}'),c.var(f'a_{u}_1'))
sorted_status(G1);sorted_status(G2);sorted_status((16,17))
with open(out,'w')as f:
 f.write(f'p cnf {len(c.names)} {len(c.clauses)}\n')
 for z in c.clauses:f.write(' '.join(map(str,z))+' 0\n')
print(case,'rob',rob,'vars',len(c.names),'clauses',len(c.clauses),'symclauses',2*((len(G1)-1)+(len(G2)-1)+1))
