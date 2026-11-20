#!/usr/bin/env python3
"""Exact characteristic-polynomial/Sturm certificates for discovered extrema.

No floating-point value is accepted in a proof.  For each named candidate we:
* build integer adjacency matrices and verify connectedness/cyclomatic ranks;
* compute exact characteristic polynomials and positive-root counts;
* isolate every positive root in explicit decimal rational intervals using
  SymPy's exact Sturm machinery;
* derive outward-rounded rational intervals for s+, sigma, Gamma, and
  payment=Gamma+sigma(U)=sigma(G)-sigma(H);
* prove the claimed signs/rational comparisons from those intervals.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import networkx as nx
import sympy as sp

HERE=Path(__file__).resolve().parent
x=sp.symbols('x')

def beta(g):return g.number_of_edges()-g.number_of_nodes()+nx.number_connected_components(g)
def join(U,u,H,v):
 g=nx.disjoint_union(U,H);g.add_edge(u,len(U)+v);return g

def c5_leaf_k5():
 U=nx.cycle_graph(5);U.add_edge(0,5)
 H=nx.complete_graph(5)
 return U,5,H,0,join(U,5,H,0)

def c5_k5():
 U=nx.cycle_graph(5);H=nx.complete_graph(5)
 return U,1,H,0,join(U,1,H,0)

def c5_bouquet6():
 U=nx.cycle_graph(5)
 H=nx.Graph();H.add_node(0);n=1
 for _ in range(6):
  vs=[0]+list(range(n,n+4));n+=4
  H.add_edges_from(zip(vs,vs[1:]+vs[:1]))
 return U,1,H,0,join(U,1,H,0)

def graph6_candidate(Ug6,u,Rg6,v):
 def build():
  U=nx.from_graph6_bytes(Ug6.encode());R=nx.from_graph6_bytes(Rg6.encode())
  return U,u,R,v,join(U,u,R,v)
 return build

def adjacency(g):return sp.Matrix(nx.to_numpy_array(g,dtype=int).tolist())
def charpoly(g):return sp.Poly(adjacency(g).charpoly(x).as_expr(),x,domain=sp.ZZ)

def isolate_positive(P,digits=10):
 """Disjoint rational intervals, listed once per root multiplicity.

 We first square-free factor over Z. Sturm isolation is then performed on each
 square-free factor, avoiding the pathological cost of count_roots on a high-
 multiplicity full polynomial. Multiplicities are restored in the energy sum.
 """
 coeff, factors=sp.factor_list(P.as_expr(),x)
 ans=[]; scale=10**digits
 for fac,mult in factors:
  F=sp.Poly(fac,x,domain=sp.ZZ)
  # Strictly positive roots only. SymPy count_roots(0,oo) includes a
  # zero endpoint for factors x, so derive the count from exact isolations.
  allints=F.intervals(eps=sp.Rational(1,10**(digits+2)))
  ints=[entry for entry in allints if entry[0][1]>0 and entry[0] != (0,0)]
  pos=len(ints)
  for (a,b),one in ints:
   assert one==1 and a>0
   lo=sp.Rational(sp.floor(a*scale)-1,scale)
   hi=sp.Rational(sp.ceiling(b*scale)+1,scale)
   while not (lo>=0 and F.count_roots(lo,hi)==1):
    scale*=10
    lo=sp.Rational(sp.floor(a*scale)-1,scale);hi=sp.Rational(sp.ceiling(b*scale)+1,scale)
   ans.extend([(lo,hi)]*mult)
 # SymPy count_roots counts distinct roots for non-square-free P here.
 assert len(ans)==sum(mult*sum(1 for I,m in sp.Poly(fac,x).intervals() if I[1]>0 and I != (0,0)) for fac,mult in factors)
 ans.sort(key=lambda I:I[0])
 return ans

def sq_interval(intervals):
 return (sum(a*a for a,b in intervals),sum(b*b for a,b in intervals))
def add(A,B):return A[0]+B[0],A[1]+B[1]
def sub(A,B):return A[0]-B[1],A[1]-B[0]
def dec(q,n=12):return str(sp.N(q,n))
def pack_interval(A):return {'lo':str(A[0]),'hi':str(A[1]),'lo_decimal':dec(A[0],15),'hi_decimal':dec(A[1],15)}
def pack_roots(I):return [[str(a),str(b)] for a,b in I]

def certify(name,builder,claims):
 U,u,H,v,G=builder()
 assert nx.is_connected(U) and nx.is_connected(H) and nx.is_connected(G)
 assert beta(U)==1 and beta(H)==6 and beta(G)==7
 Ps={z:charpoly(g) for z,g in [('U',U),('H',H),('G',G)]}
 Is={z:isolate_positive(P) for z,P in Ps.items()}
 Es={z:sq_interval(Is[z]) for z in Ps}
 sig={z:sub(Es[z],(len(g),len(g))) for z,g in [('U',U),('H',H),('G',G)]}
 gamma=sub(Es['G'],add(Es['U'],Es['H']))
 payment=sub(sig['G'],sig['H'])
 # F = Gamma + sigma(H) - delta_5, with delta_5=sqrt(5)-2.
 # Enclose sqrt(5) by exact 10^-12 rationals, certified by squaring.
 sqrt5=(sp.Rational(2236067977499,10**12),sp.Rational(2236067977500,10**12))
 assert sqrt5[0]**2<5<sqrt5[1]**2
 delta5=(sqrt5[0]-2,sqrt5[1]-2)
 F=sub(add(gamma,sig['H']),delta5)
 # Redundant identity interval direct forms overlap; exact quantities agree.
 assert max(gamma[0]+sig['U'][0],payment[0]) < min(gamma[1]+sig['U'][1],payment[1])
 values={'sigma_U':sig['U'],'sigma_H':sig['H'],'sigma_G':sig['G'],'Gamma':gamma,'payment':payment,'F':F}
 passed=[]
 for quantity,op,rhs in claims:
  rhs=sp.Rational(rhs[0],rhs[1])
  A=values[quantity]
  ok={'>':A[0]>rhs,'>=':A[0]>=rhs,'<':A[1]<rhs,'<=':A[1]<=rhs}[op]
  assert ok,(quantity,A,op,rhs)
  passed.append(f'{quantity} {op} {rhs}')
 return {'name':name,'orders':{'U':len(U),'H':len(H),'G':len(G)},
         'edges':{'U':U.number_of_edges(),'H':H.number_of_edges(),'G':G.number_of_edges()},
         'betas':{'U':beta(U),'H':beta(H),'G':beta(G)},
         'positive_roots_counted_with_multiplicity':{z:len(Is[z]) for z in Ps},
         'charpoly':{z:str(Ps[z].as_expr()) for z in Ps},
         'positive_root_intervals':{z:pack_roots(Is[z]) for z in Ps},
         'values':{z:pack_interval(A) for z,A in values.items()},'proved':passed,
         'graph6':{z:nx.to_graph6_bytes(g,header=False).decode().strip() for z,g in [('U',U),('H',H),('G',G)]}}

def main():
 certs=[
  certify('atlas payment/gain extremizer: pendant-rooted C5 joined to K5',c5_leaf_k5,
          [('sigma_G','>',(11,1)),('payment','>',(1,2)),('payment','<',(27,50)),
           ('Gamma','>',(17,25)),('Gamma','<',(69,100)),('sigma_U','<',(0,1))]),
  certify('smallest sigma_G in generated set: C5 joined to six-C5 bouquet',c5_bouquet6,
          [('sigma_G','>',(5,1)),('sigma_G','<',(11,2)),('payment','>',(3,4)),('sigma_U','<',(0,1))]),
  certify('bare C5 joined to K5 baseline',c5_k5,
          [('sigma_G','>',(11,1)),('payment','>',(59,100)),('payment','<',(3,5)),('sigma_U','<',(0,1))]),
  certify('low-sigma 2-connected rank-six center H_p?ikTW with C5-P2 hostile arm',
          graph6_candidate('Fhe?G',5,'Hp?ikTW',1),
          [('sigma_G','>',(49,10)),('sigma_G','<',(5,1)),('Gamma','>',(1,1)),('F','>',(24,5))]),
  certify('atlas-order-seven minimum-sigma rank-six center FreRW with bare C5',
          graph6_candidate('Dhc',0,'FreRW',0),
          [('sigma_G','>',(23,4)),('sigma_G','<',(6,1)),('Gamma','>',(1,1)),('F','>',(23,4))]),
 ]
 out={'method':'integer characteristic polynomials + exact SymPy Sturm count_roots + rational intervals; decimals diagnostic only',
      'certificates':certs}
 (HERE/'exact-certificates.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 for c in certs:
  print(c['name'])
  for q in ['sigma_U','sigma_H','sigma_G','Gamma','payment','F']:
   a=c['values'][q];print(f"  {q}: ({a['lo_decimal']}, {a['hi_decimal']})")
  print('  proved:',', '.join(c['proved']))
if __name__=='__main__':main()
