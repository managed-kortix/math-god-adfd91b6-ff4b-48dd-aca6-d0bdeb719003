#!/usr/bin/env python3
import importlib.util,json
P=str(__import__('pathlib').Path(__file__).with_name('r31-s-d3-full-sachs-diagnostic.py'));sp=importlib.util.spec_from_file_location('d3',P);d3=importlib.util.module_from_spec(sp);sp.loader.exec_module(d3)
def uni(poly):
 o={}
 for mask,c in poly.items():o[mask.bit_count()]=o.get(mask.bit_count(),0)+c
 return {k:v for k,v in sorted(o.items()) if v}
def fmt(P):
 out=[]
 for k,c in sorted(P.items()):
  m='1' if k==0 else ('t' if k==1 else f't^{k}')
  q=(str(abs(c)) if k==0 else (('' if abs(c)==1 else str(abs(c))+'*')+m))
  out.append((('' if not out and c>0 else '-' if not out else ' + ' if c>0 else ' - ')+q))
 return ''.join(out)
for rec in sorted(d3.records(),key=repr):
 V,E=d3.graph_for(rec);R,I,_=d3.full_sachs_polynomial(V,E)
 print(repr(rec))
 print(' R(t) =',fmt(uni(R)))
 print(' I(t) =',fmt(uni(I)))
