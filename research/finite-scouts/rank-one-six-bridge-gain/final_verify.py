#!/usr/bin/env python3
"""Fail-closed bounded replay for the corrected finite scout packet.

The complete Atlas side/root census and persisted extremal/certificate graphs
are rebuilt from adjacency.  Selected spectral receipts use integer
characteristic polynomials, exact Sturm isolation, and rational interval
arithmetic.  Broad kernel/unit-star/structured all-row counts remain persisted
numerical census data; this program does not recompute every row.  Python
assertions are deliberately not used.
"""
from __future__ import annotations
import hashlib, json, subprocess, sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
import networkx as nx
import sympy as sp

HERE=Path(__file__).resolve().parent
X=sp.symbols('x')
DELTA_LO=Fraction(2236067977499,10**12)-2
DELTA_HI=Fraction(2236067977500,10**12)-2

class VerificationError(RuntimeError): pass
def require(c,m):
 if not c: raise VerificationError(m)
def load(name):
 raw=(HERE/name).read_bytes();require(raw and raw.endswith(b'\n'),f'{name}: empty/non-newline JSON')
 try:return json.loads(raw.decode('utf-8'))
 except Exception as e:raise VerificationError(f'{name}: malformed JSON: {e}')
def beta(g):return g.number_of_edges()-len(g)+nx.number_connected_components(g)
def g6(g):return nx.to_graph6_bytes(nx.convert_node_labels_to_integers(g),header=False).decode().strip()
def graph(s):return nx.from_graph6_bytes(s.encode())
def join(U,u,R,v):
 require(u in U and v in R,'bad marked vertex')
 G=nx.disjoint_union(U,R);G.add_edge(u,len(U)+v);return G
def charpoly(g):
 A=sp.Matrix(nx.to_numpy_array(g,dtype=int).tolist())
 return sp.Poly(A.charpoly(X).as_expr(),X,domain=sp.ZZ)
def poly_text(P):return str(P.as_expr())
def iv(d):return Fraction(d['lo']),Fraction(d['hi'])
def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[1],a[1]-b[0]
def overlap(a,b):return max(a[0],b[0])<min(a[1],b[1])
def exact_energy(g,digits=10):
 P=charpoly(g); out=[];scale=10**digits
 _,factors=sp.factor_list(P.as_expr(),X)
 for fac,mult in factors:
  F=sp.Poly(fac,X,domain=sp.ZZ)
  for (a,b),one in F.intervals(eps=sp.Rational(1,10**(digits+2))):
   if b<=0 or (a,b)==(0,0):continue
   require(one==1 and a>0,'bad positive-root isolation')
   lo=sp.Rational(sp.floor(a*scale)-1,scale);hi=sp.Rational(sp.ceiling(b*scale)+1,scale)
   require(F.count_roots(lo,hi)==1,'Sturm interval does not isolate one root')
   out.extend([(lo,hi)]*mult)
 out.sort(key=lambda z:z[0])
 E=(sum(Fraction(a)**2 for a,b in out),sum(Fraction(b)**2 for a,b in out))
 return P,out,E
def profile(g):
 ranks=[]
 for C in nx.biconnected_components(g):
  h=g.subgraph(C);r=h.number_of_edges()-len(h)+1
  if r:ranks.append(r)
 require(sum(ranks)==beta(g),'block profile does not sum to beta')
 return tuple(sorted(ranks,reverse=True))
def actual_eligible(G):
 require(nx.is_connected(G) and beta(G)==7,'eligibility graph not connected rank seven')
 bridges=list(nx.bridges(G));H=G.copy();H.remove_edges_from(bridges)
 comps=list(nx.connected_components(H));where={v:i for i,C in enumerate(comps) for v in C}
 T=nx.Graph();T.add_nodes_from(range(len(comps)));w={i:beta(G.subgraph(C)) for i,C in enumerate(comps)}
 for a,b in bridges:T.add_edge(where[a],where[b])
 require(nx.is_tree(T) and sum(w.values())==7,'bridge quotient is not a rank-seven weighted tree')
 cuts=[]
 for a,b in list(T.edges()):
  T.remove_edge(a,b);S=nx.node_connected_component(T,a);q=sum(w[i] for i in S);T.add_edge(a,b)
  cuts.append(tuple(sorted((q,7-q))))
 return all(c in ((0,7),(1,6)) for c in cuts),tuple(sorted(cuts))
def orbits(g):
 nodes=list(g);left=set(nodes);out=[];tri=nx.triangles(g);ecc=nx.eccentricity(g) if len(g)>1 else {v:0 for v in g}
 while left:
  a=min(left);ga=g.copy();nx.set_node_attributes(ga,False,'r');ga.nodes[a]['r']=True;orb=[]
  for b in sorted(left):
   if (g.degree(a),tri[a],ecc[a])!=(g.degree(b),tri[b],ecc[b]):continue
   gb=g.copy();nx.set_node_attributes(gb,False,'r');gb.nodes[b]['r']=True
   if nx.is_isomorphic(ga,gb,node_match=nx.algorithms.isomorphism.categorical_node_match('r',False)):orb.append(b)
  require(orb,'empty orbit')
  left.difference_update(orb);out.append(orb)
 return out

def verify_exact_record(c,label):
 require(set(c['graph6'])=={'U','H','G'},label+': graph6 keys')
 U=graph(c['graph6']['U']);R=graph(c['graph6']['H']);G=graph(c['graph6']['G'])
 require(nx.is_connected(U) and nx.is_connected(R) and nx.is_connected(G),label+': disconnected graph')
 require((beta(U),beta(R),beta(G))==(1,6,7),label+': wrong betas')
 # Certificate graph G must be a one-bridge join of U,R at some marks; graph6
 # isomorphism plus exactly one interpart bridge is independently checked by
 # deleting every bridge and finding components isomorphic to U,R.
 witnessed=False
 for a,b in nx.bridges(G):
  H=G.copy();H.remove_edge(a,b);cs=list(nx.connected_components(H))
  if len(cs)==2 and ((nx.is_isomorphic(G.subgraph(cs[0]),U) and nx.is_isomorphic(G.subgraph(cs[1]),R)) or (nx.is_isomorphic(G.subgraph(cs[1]),U) and nx.is_isomorphic(G.subgraph(cs[0]),R))):witnessed=True
 require(witnessed,label+': G is not certified U--R join')
 values={}
 energies={}
 for key,g in [('U',U),('H',R),('G',G)]:
  P,roots,E=exact_energy(g);energies[key]=E
  require(poly_text(P)==c['charpoly'][key],label+f': {key} charpoly mismatch')
  stored=[(Fraction(a),Fraction(b)) for a,b in c['positive_root_intervals'][key]]
  require(len(stored)==len(roots),label+f': {key} root count mismatch')
  _,facs=sp.factor_list(P.as_expr(),X)
  for a,b in stored:
   aa=sp.Rational(a.numerator,a.denominator);bb=sp.Rational(b.numerator,b.denominator)
   require(sum(mult*sp.Poly(fac,X,domain=sp.ZZ).count_roots(aa,bb) for fac,mult in facs)>=1,label+f': {key} stored Sturm interval invalid')
 sig={k:sub(E,(len(g),len(g))) for k,E,g in [('U',energies['U'],U),('H',energies['H'],R),('G',energies['G'],G)]}
 values.update({'sigma_U':sig['U'],'sigma_H':sig['H'],'sigma_G':sig['G']})
 values['Gamma']=sub(energies['G'],add(energies['U'],energies['H']))
 values['payment']=sub(sig['G'],sig['H'])
 values['F']=sub(add(values['Gamma'],sig['H']),(DELTA_LO,DELTA_HI))
 for q,A in values.items():
  if q in c['values']:require(overlap(A,iv(c['values'][q])),label+f': {q} exact replay misses stored interval')
 for claim in c.get('proved',[]):
  q,op,rhs=claim.split();r=Fraction(rhs);A=values[q]
  require({'>':A[0]>r,'>=':A[0]>=r,'<':A[1]<r,'<=':A[1]<=r}[op],label+': failed claim '+claim)
 return G

def atlas_section():
 d=load('atlas-exact-exhaustive-minima.json');Us=[];Rs=[]
 for g in nx.graph_atlas_g():
  if not g or not nx.is_connected(g):continue
  b=beta(g)
  if b==1:
   _,_,E=exact_energy(g);s=sub(E,(len(g),len(g)))
   if s[1]<0:
    for o in orbits(g):Us.append((g,o[0]))
  if b==6:
   for o in orbits(g):Rs.append((g,o[0]))
 require((len(Us),len(Rs),len(Us)*len(Rs))==(22,678,14916),'Atlas census mismatch')
 pc=Counter(profile(g) for g,r in Rs);require(pc==Counter({(6,):668,(5,1):8,(3,3):2}),'Atlas profile census mismatch')
 require(all(actual_eligible(join(nx.cycle_graph(5),0,R,v))[0] for R,v in Rs),'Atlas root fails actual eligibility')
 require(d['counts']['joins']==14916 and d['counts']['rooted_U']==22 and d['counts']['rooted_R']==678,'stored Atlas counts mismatch')
 require(d['all_R_roots_actual_unit_star_eligible'] is True,'stored Atlas eligibility changed')
 expected={((3,3),'F'):('Fpa?g',1,'FK|ko',4),((3,3),'Gamma'):('Fpa?g',1,'FK|ko',4),((3,3),'sigma_G'):('FPq?g',1,'FK|ko',4),((5,1),'F'):('Fpa?g',1,'F{e[o',3),((5,1),'Gamma'):('Ehd?',5,'Fn}CG',1),((5,1),'sigma_G'):('Ehd?',5,'F{e[o',3),((6,),'F'):('Ehd?',5,'FreRW',1),((6,),'Gamma'):('Ehd?',5,'D~{',0),((6,),'sigma_G'):('FPq?g',4,'FreRW',1)}
 require(len(d['minima'])==9,'Atlas minima count mismatch')
 for r in d['minima']:
  k=(tuple(r['profile']),r['metric']);require(k in expected,'unexpected Atlas extremum')
  require((r['U_g6'],r['U_root'],r['R_g6'],r['R_root'])==expected[k],'Atlas extremum identity changed')
  U=graph(r['U_g6']);R=graph(r['R_g6']);G=join(U,r['U_root'],R,r['R_root'])
  Ps={z:charpoly(g) for z,g in [('U',U),('R',R),('G',G)]}
  for z in Ps:require(poly_text(Ps[z])==r[z+'_P'],f'Atlas {k} {z} charpoly mismatch')
  Es={z:exact_energy(g)[2] for z,g in [('U',U),('R',R),('G',G)]};sigU=sub(Es['U'],(len(U),len(U)));sigR=sub(Es['R'],(len(R),len(R)));sigG=sub(Es['G'],(len(G),len(G)));ga=sub(Es['G'],add(Es['U'],Es['R']));F=sub(add(ga,sigR),(DELTA_LO,DELTA_HI));vals={'sigma_G':sigG,'Gamma':ga,'F':F}
  require(overlap(vals[r['metric']],iv(r[r['metric']])),f'Atlas {k} interval mismatch')
 return 'atlas rooted_U=22 rooted_R=678 joins=14916 profiles=3 exact_extrema=9 actual_eligible=678'

def realize(n,code):
 g=nx.Graph();g.add_nodes_from(range(n));nxt=n
 pairs=((u,v) for u in range(n) for v in range(u+1,n))
 for mult,(u,v) in zip(code,pairs):
  for j in range(mult):
   if j==0:g.add_edge(u,v)
   else:g.add_edges_from(((u,nxt),(nxt,v)));nxt+=1
 return g
def kernel_section():
 d=load('kernel-results.json');require(d['counts']=={'arms':45,'joins':515070,'kernels':1198,'negative_sigma_G_or_F':0},'kernel result counts mismatch')
 fixture=json.loads((HERE/'rank-six-kernels.json').read_text())
 require(hashlib.sha256((HERE/'rank-six-kernels.json').read_bytes()).hexdigest()=='5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476','kernel fixture digest mismatch')
 require(len(fixture['kernels'])==1198,'kernel fixture count mismatch')
 for row in fixture['kernels']:
  R=realize(row['n'],row['code']);require(nx.is_connected(R) and beta(R)==6 and not list(nx.bridges(R)),'bad canonical kernel realization')
 # Bind the persisted numerical extrema to independently reconstructed
 # fixture realizations and then replay the dedicated exact receipts.
 expected={'sigma_G':(1147,6,'C5'),'F':(1147,9,'C5+S20-hub'),'Gamma':(109,2,'C5+S20-leaf')}
 for metric,(ki,root,arm) in expected.items():
  z=d['tops'][metric][0];require((z['kernel_index'],z['R_root'],z['U_label'])==(ki,root,arm),f'kernel {metric} extremum identity changed')
  R=realize(fixture['kernels'][ki]['n'],fixture['kernels'][ki]['code']);require(g6(R)==z['R_g6'],f'kernel {metric} reconstructed graph6 mismatch')
 c=load('exact-scan-certificates.json');require(len(c['certificates'])==5,'exact-scan receipt count mismatch')
 for i,z in enumerate(c['certificates']):verify_exact_record(z,'exact-scan['+str(i)+']')
 require(c['certificates'][3]['graph6']['H']==d['tops']['sigma_G'][0]['R_g6'],'kernel sigma exact receipt not bound to result')
 require(c['certificates'][4]['graph6']['H']==d['tops']['F'][0]['R_g6'],'kernel F exact receipt not bound to result')
 return 'kernels fixture=1198 arms=45 joins=515070 exact_receipts=5'

def unit_section():
 d=load('unit-star-results.json');require(d['counts']=={'eligible_rows':90013,'negative_F':0,'negative_sigma_G':0,'rows':100401},'unit-star corrected counts mismatch')
 # Reconstruct eligibility from every persisted extremum graph, never row flag.
 for group in [d['minima'],list(d['global'].values())]:
  for r in group:
   U=graph(r['U_g6']);R=graph(r['R_g6']);G=join(U,r['U_root'],R,r['R_root']);ok,cuts=actual_eligible(G)
   require(ok,'unit-star persisted extremum fails adjacency eligibility')
   require(profile(R)==tuple(r['positive_block_rank_profile']),'unit-star profile mismatch')
 require(len(d['minima'])==27,'unit-star profile/metric minima count mismatch')
 ps={tuple(r['positive_block_rank_profile']) for r in d['minima']};require(len(ps)==9,'unit-star profile count mismatch')
 c=load('unit-star-exact-certificates.json');require(len(c['certificates'])==9,'unit-star F receipt count mismatch')
 for i,z in enumerate(c['certificates']):
  G=verify_exact_record(z,'unit-star['+str(i)+']');require(actual_eligible(G)[0],'unit-star exact receipt is ineligible')
 c=load('correct-global-unit-star-gamma-sigmaG-certificates.json');require(len(c['certificates'])==2,'unit-star global receipt count mismatch')
 for i,z in enumerate(c['certificates']):
  G=verify_exact_record(z,'unit-global['+str(i)+']');require(actual_eligible(G)[0],'unit global receipt is ineligible')
 return 'unit-star generated=100401 actual_eligible=90013 profiles=9 exact_receipts=11'

def structured_section():
 s=(HERE/'structured_scan.py').read_text();require('for n in [6,7,8,10,12]:' in s and 'for j in range(12):' in s,'structured 12-sample loop changed')
 d=load('structured-results.json');require(d['counts']=={'H':244,'U':763,'joins':186172,'negative':0},'structured persisted counts mismatch')
 require('nonexhaustive' in d['scope'],'structured scope lost nonexhaustive marker')
 return 'structured random_orders=6,7,8,10,12 samples_per_order=12 joins=186172 nonexhaustive=true'

def other_exact_receipts():
 total=0
 for name in ['exact-certificates.json','profile-exact-certificates.json']:
  d=load(name)
  for i,z in enumerate(d['certificates']):verify_exact_record(z,name+'['+str(i)+']');total+=1
 return f'additional_exact_receipts={total}'

def verify_manifest():
 lines=(HERE/'FINAL-MANIFEST.sha256').read_text().splitlines();seen=set()
 for line in lines:
  h,name=line.split('  ',1);require(name!='FINAL-MANIFEST.sha256' and name not in seen,'bad manifest member');seen.add(name)
  p=HERE/name;require(p.is_file() and p.stat().st_size>0,'missing/empty manifest artifact '+name);require(hashlib.sha256(p.read_bytes()).hexdigest()==h,'manifest hash mismatch '+name)
 actual={p.name for p in HERE.iterdir() if p.is_file() and p.name!='FINAL-MANIFEST.sha256'}
 require(seen==actual,'manifest does not cover every nonempty top-level final artifact')
 return len(seen)
def report():
 rows=[atlas_section(),kernel_section(),unit_section(),structured_section(),other_exact_receipts()]
 n=verify_manifest();return '\n'.join(['corrected finite bridge scout: PASS',*rows,f'manifest_artifacts={n}','theorem_status=FINITE_ONLY repo_touched=false'])+'\n'
def main():
 out=report()
 if sys.flags.optimize==0 and '--emit' not in sys.argv:
  p=subprocess.run([sys.executable,'-O',__file__,'--emit'],capture_output=True,text=True)
  require(p.returncode==0 and p.stderr=='','optimized replay failed: '+p.stderr);require(p.stdout==out,'normal/-O output mismatch')
 sys.stdout.write(out)
if __name__=='__main__':main()
