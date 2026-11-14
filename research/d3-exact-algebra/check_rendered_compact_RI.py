#!/usr/bin/env python3
"""Independently evaluate render_compact_RI formulas and compare all 14 to Sachs."""
import contextlib,io,runpy,importlib.util
HERE=__import__('pathlib').Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):g=runpy.run_path(str(HERE/'render_compact_RI.py'))
P=str(__import__('pathlib').Path(__file__).with_name('r31-s-d3-full-sachs-diagnostic.py'));sp=importlib.util.spec_from_file_location('d3',P);d3=importlib.util.module_from_spec(sp);sp.loader.exec_module(d3)
from collections import defaultdict

def add(*ps):
 o=defaultdict(int)
 for p in ps:
  for m,c in p.items():o[tuple(sorted(m))]+=c
 return {m:c for m,c in o.items() if c}
def mul(a,b):
 o=defaultdict(int)
 for m,c in a.items():
  for n,e in b.items():o[tuple(sorted(m+n))]+=c*e
 return {m:c for m,c in o.items() if c}
def expand_real(p):
 out={}
 for mon,c in p.items():
  cur={():c}
  for x in mon:
   if len(x)==2 and x[0]=='d' and x[1].isdigit():
    j=x[1];fac={():1,(f'T{j}a',f'T{j}b'):1}
   elif len(x)==2 and x[0]=='e' and x[1].isdigit():
    j=x[1];fac={(f'T{j}a',):1,(f'T{j}b',):1}
   elif x.startswith('a') and x[1:].isdigit():fac={(f'T{x[1:]}a',):1}
   elif x.startswith('b') and x[1:].isdigit():fac={(f'T{x[1:]}b',):1}
   else:fac={(x,):1}
   cur=mul(cur,fac)
  out=add(out,cur)
 return out
def host_state(name,V,E):
 # Synthetic host state is the explicit four-vertex diamond, not the full record.
 part=name.split('_',1);side=part[0];deleted=tuple(part[1]) if len(part)>1 else ()
 DV=('A','B','x','z');DE=frozenset({('A','B'),('A','x'),('B','x'),('A','z'),('B','z')})
 W=tuple(v for v in DV if v not in deleted);F=frozenset(e for e in DE if not(set(e)&set(deleted)))
 R,I,_=d3.full_sachs_polynomial(W,F);X=R if side=='R' else I
 return {tuple(W[i] for i in range(len(W)) if m>>i&1):c for m,c in X.items()}
def substitute_hosts(p,V,E):
 out={}
 for mon,c in p.items():
  cur={():c}
  for x in mon:
   if x=='R' or x=='I' or x.startswith('R_') or x.startswith('I_'):fac=host_state(x,V,E)
   else:fac={(x,):1}
   cur=mul(cur,fac)
  out=add(out,cur)
 return out
def rendered(rec):
 if rec[0]=='direct3':return g['direct'](rec[1])
 if rec[0]=='chain2+direct':return g['chain'](*rec[1:])
 if rec[0]=='fork':return g['fork'](rec[2])
 return g['chain3']()
for rec in sorted(d3.records(),key=repr):
 V,E=d3.graph_for(rec);R,I,_=d3.full_sachs_polynomial(V,E)
 exact=[]
 for X in (R,I):exact.append({tuple(V[k] for k in range(len(V)) if m>>k&1):c for m,c in X.items()})
 calc=tuple(substitute_hosts(expand_real(X),V,E) for X in rendered(rec))
 assert calc==tuple(exact),rec
 print('PASS',repr(rec),len(calc[0]),len(calc[1]))
