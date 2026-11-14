#!/usr/bin/env python3
"""Exact CAD/QE attempts for D3 boundary implications on selected faces/slices."""
import sympy as s
import importlib.util,json,time
P=str(__import__('pathlib').Path(__file__).with_name('r31-s-d3-full-sachs-diagnostic.py'));sp=importlib.util.spec_from_file_location('d3',P);d3=importlib.util.module_from_spec(sp);sp.loader.exec_module(d3)
# Exact one-dimensional defect lines: test Q>0 => AQ-BP<0 over t>0.
t=s.symbols('t',positive=True)
out=[]
for rec,(v,(aa,bb),(pp,qq)) in sorted(d3.bare_defect_formulas().items(),key=lambda z:repr(z[0])):
 def f(c):return s.Poly(sum(x*t**i for i,x in enumerate(c)),t)
 A,B,Pp,Q=map(f,(aa,bb,pp,qq));H=s.Poly(A.as_expr()*Q.as_expr()-B.as_expr()*Pp.as_expr(),t)
 # Symbolic reduction: all even/odd. Set u=t^2 and isolate exact roots.
 u=s.symbols('u',positive=True)
 Hu=s.Poly(s.expand(H.as_expr()).subs(t,s.sqrt(u)),u)
 Qu=s.Poly(Q.as_expr().subs(t,s.sqrt(u)),u)
 rootsQ=s.polys.polytools.intervals(Qu,eps=s.Rational(1,10)**12)
 rootsH=s.polys.polytools.intervals(Hu,eps=s.Rational(1,10)**12)
 # prove H<0 over interval Q>0 using exact roots. Q has unique positive root; check H has no positive roots and H(0)<0 if so.
 qpos=[(iv,m) for iv,m in rootsQ if (iv if not isinstance(iv,tuple) else iv[1])>0]
 hpos=[(iv,m) for iv,m in rootsH if (iv if not isinstance(iv,tuple) else iv[1])>0]
 row={'record':repr(rec),'defect':v,'Q_u':str(Qu.as_expr()),'H_u':str(Hu.as_expr()),'Q_positive_roots':[[str(iv),int(m)] for iv,m in qpos], 'H_positive_roots':[[str(iv),int(m)] for iv,m in hpos], 'H0':int(Hu.eval(0))}
 # H may have positive roots outside Q>0, compare algebraic intervals.
 out.append(row)
 print(rec,'Q+',qpos,'H+',hpos,'H0',Hu.eval(0))
open(str(__import__('pathlib').Path(__file__).with_name('defect-line-root-isolation.json')),'w').write(json.dumps(out,indent=2)+'\n')
