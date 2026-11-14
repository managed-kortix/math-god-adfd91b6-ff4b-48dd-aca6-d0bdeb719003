#!/usr/bin/env python3
"""Export every exact raw and activity-expanded R/I polynomial for 14 D3 records."""
import importlib.util,json,hashlib,os
P=str(__import__('pathlib').Path(__file__).with_name('r31-s-d3-full-sachs-diagnostic.py'))
sp=importlib.util.spec_from_file_location('d3',P);d3=importlib.util.module_from_spec(sp);sp.loader.exec_module(d3)
OUT=str(__import__('pathlib').Path(__file__).with_name('exact-polynomials'));os.makedirs(OUT,exist_ok=True)
README='''# D3 exact polynomial export

Normalization: `Psi_G(z)=i^{-|V(G)|} det(i diag(z)-A(G))=R_G(z)+i I_G(z)`.

Each record has complete `R_raw`, `I_raw`, `R_activity`, and `I_activity`, with `z_v=t+y_v`, `t>0`, `y_v>=0`; no coefficient is omitted. `manifest.json` records counts and per-record SHA-256 hashes. Regenerate with `../export_exact_polynomials.py`; cross-check with the independent determinant and compact-formula checkers.
'''
open(os.path.join(OUT,'README.md'),'w').write(README)

def mono_raw(mask,V):return '*'.join('z_'+v for i,v in enumerate(V) if mask>>i&1) or '1'
def mono_act(k,V):
 mask,tp=k;a=[('y_'+v) for i,v in enumerate(V) if mask>>i&1];a += ['t']*tp;return '*'.join(a) or '1'
def expr(poly,fmt):
 items=sorted(poly.items(),key=lambda kv:(fmt(kv[0]),kv[1]))
 out=[]
 for k,c in items:
  m=fmt(k);term=str(abs(c)) if m=='1' else ((str(abs(c))+'*') if abs(c)!=1 else '')+m
  if not out:out.append(('-' if c<0 else '')+term)
  else:out.append((' - ' if c<0 else ' + ')+term)
 return ''.join(out) if out else '0'
def slug(rec):
 s=repr(rec)
 for a,b in [("'",''),('(','_'),(')',''),(',','_'),(' ','')]:s=s.replace(a,b)
 return s.strip('_').replace('+','plus')
manifest={'schema':'D3-exact-polynomials-v1','normalization':'Psi=i^(-n)det(i diag(z)-A)=R+iI; z_v=t+y_v','records':[]}
for rec in sorted(d3.records(),key=repr):
 V,E=d3.graph_for(rec);R,I,C=d3.full_sachs_polynomial(V,E);Ra,Ia=d3.activity_expansion(R),d3.activity_expansion(I)
 name=slug(rec)+'.txt';path=os.path.join(OUT,name)
 text=(f'record = {rec!r}\nvertices = {V!r}\nedges = {sorted(E)!r}\n'
       f'R_raw = {expr(R,lambda k:mono_raw(k,V))}\nI_raw = {expr(I,lambda k:mono_raw(k,V))}\n'
       f'R_activity = {expr(Ra,lambda k:mono_act(k,V))}\nI_activity = {expr(Ia,lambda k:mono_act(k,V))}\n')
 open(path,'w').write(text)
 h=hashlib.sha256(text.encode()).hexdigest()
 manifest['records'].append({'record':repr(rec),'file':name,'vertices':list(V),'edges':[list(e) for e in sorted(E)],'cycles':len(C),'raw_R_terms':len(R),'raw_I_terms':len(I),'activity_R_terms':len(Ra),'activity_I_terms':len(Ia),'raw_R_signs':d3.signs(R),'raw_I_signs':d3.signs(I),'activity_R_signs':d3.signs(Ra),'activity_I_signs':d3.signs(Ia),'sha256':h})
open(os.path.join(OUT,'manifest.json'),'w').write(json.dumps(manifest,indent=2)+'\n')
# Re-read and lock aggregate hash.
h=hashlib.sha256()
for f in sorted(os.listdir(OUT)):
 if f not in ('SHA256SUMS','aggregate.sha256'):h.update(f.encode()+b'\0'+open(os.path.join(OUT,f),'rb').read())
open(os.path.join(OUT,'aggregate.sha256'),'w').write(h.hexdigest()+'\n')
print('records',len(manifest['records']),'R activity',sum(x['activity_R_terms'] for x in manifest['records']),'I activity',sum(x['activity_I_terms'] for x in manifest['records']))
print('aggregate',open(os.path.join(OUT,'aggregate.sha256')).read().strip())
