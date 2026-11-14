#!/usr/bin/env python3
import importlib.util,itertools,json
from collections import defaultdict
P=str(__import__('pathlib').Path(__file__).with_name('r31-s-d3-full-sachs-diagnostic.py'));sp=importlib.util.spec_from_file_location('d3',P);d3=importlib.util.module_from_spec(sp);sp.loader.exec_module(d3)

def fmt(key,V):
 s,tp=key; y='*'.join('y_'+V[i] for i in range(len(V)) if s>>i&1) or '1'; return y+(f'*t^{tp}' if tp else '')
for rec in sorted(d3.bare_defect_formulas(),key=repr):
 V,E=d3.graph_for(rec);R,I,_=d3.full_sachs_polynomial(V,E);Ra,Ia=d3.activity_expansion(R),d3.activity_expansion(I)
 pos=[(k,v) for k,v in Ia.items() if v>0]; bit=pos[0][0][0];j=bit.bit_length()-1
 A,B=d3.split_variable(Ra,bit);Pp,Q=d3.split_variable(Ia,bit)
 print('\n##',rec,'defect',V[j])
 for nm,X in [('A',A),('B',B),('P',Pp),('Q',Q)]:
  sg=d3.signs(X);print(nm,'terms',len(X),'signs',sg,'constant',X.get((0,0)), 't-only',sorted((k[1],v) for k,v in X.items() if k[0]==0))
  if nm in ('B','Q'):
   positives=sorted(((fmt(k,V),v) for k,v in X.items() if v>0))
   print(' positives',positives[:30], 'count',len(positives))
 # check if A<0 whenever Q>0 via crude coefficient pairing? list A positives and Q negatives supports
 print('A positives',len([1 for v in A.values() if v>0]),'B positives',len([1 for v in B.values() if v>0]))
