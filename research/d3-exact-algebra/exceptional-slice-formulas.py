#!/usr/bin/env python3
import importlib.util
P=str(__import__('pathlib').Path(__file__).with_name('r31-s-d3-full-sachs-diagnostic.py'));sp=importlib.util.spec_from_file_location('d3',P);d3=importlib.util.module_from_spec(sp);sp.loader.exec_module(d3)
def conv(a,b):
 o=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):o[i+j]+=x*y
 return o
def sub(a,b):
 n=max(len(a),len(b));return [(a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0) for i in range(n)]
def eu(c):return [c[2*i] for i in range((len(c)+1)//2)]
def ou(c):return [c[2*i+1] for i in range(len(c)//2)]
def fmt(c,var='u'):
 a=[]
 for k,x in enumerate(c):
  if not x:continue
  m='' if k==0 else var if k==1 else f'{var}^{k}'
  q=str(abs(x)) if not m else ('' if abs(x)==1 else str(abs(x))+'*')+m
  a.append((x,q))
 o=''
 for i,(x,q) in enumerate(a):o+=('-' if i==0 and x<0 else '' if i==0 else ' - ' if x<0 else ' + ')+q
 return o or '0'
for rec,(v,(A,B),(Pp,Q)) in sorted(d3.bare_defect_formulas().items(),key=lambda z:repr(z[0])):
 a,b,p,q=eu(A),ou(B),ou(Pp),eu(Q);h=sub(conv(a,q),[0]+conv(b,p));
 while h and not h[-1]:h.pop()
 print(rec,'defect',v);print(' A=',fmt(a));print(' B=t*(',fmt(b),')');print(' P=t*(',fmt(p),')');print(' Q=',fmt(q));print(' H=',fmt(h))
