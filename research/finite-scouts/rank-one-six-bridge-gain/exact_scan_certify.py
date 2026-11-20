#!/usr/bin/env python3
"""Exact Sturm certificates for the corrected unit-star/kernel scan extrema."""
import json
from pathlib import Path
import networkx as nx
from certify import certify, graph6_candidate

HERE=Path(__file__).resolve().parent

def main():
 specs=[
  ('unit-star eligible profile 6 minimum F in Atlas+payload scan',
   'Ehe?',5,'GreR[?',1,
   [('sigma_G','>',(29,5)),('F','>',(57,10)),('Gamma','>',(9,10))]),
  ('unit-star eligible profile 5+1 minimum F in Atlas+payload scan',
   'Ehe?',5,'G{e[o_',4,
   [('sigma_G','>',(99,10)),('F','>',(989,100)),('Gamma','>',(3,4))]),
  ('unit-star eligible profile 3+3 minimum F in Atlas+payload scan',
   'Ehe?',5,'GK|koO',0,
   [('sigma_G','>',(106,10)),('F','>',(105,10)),('Gamma','>',(3,4))]),
  ('canonical shortest rank-six kernel minimum total sigma: Petersen center',
   'Dhc',0,'I?LRCecq?',6,
   [('sigma_G','>',(48,10)),('sigma_G','<',(49,10)),('F','>',(48,10)),('Gamma','>',(1,1))]),
  ('canonical shortest rank-six kernel minimum F: Petersen center',
   'XheCCA?_C?O?_?_?O?C??_?A??C??C??A???_??C???O???_???',0,'I?LRCecq?',9,
   [('sigma_G','>',(49,10)),('sigma_G','<',(5,1)),('F','>',(47,10)),('F','<',(24,5)),('Gamma','>',(1,1))]),
 ]
 cs=[]
 for name,ug,u,rg,r,claims in specs:
  cs.append(certify(name,graph6_candidate(ug,u,rg,r),claims))
 out={'scope':'exact certificates for numerical extrema in the stated bounded corrected unit-star/profile and canonical-shortest-kernel scans; not universal minima',
      'method':'integer characteristic polynomials, exact Sturm positive-root isolation, rational interval arithmetic',
      'certificates':cs}
 (HERE/'exact-scan-certificates.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 for c in cs:
  print(c['name'])
  print('  charpoly R:',c['charpoly']['H'])
  print('  charpoly G:',c['charpoly']['G'])
  for q in ('sigma_H','sigma_G','Gamma','F'):
   print(' ',q,c['values'][q]['lo_decimal'],c['values'][q]['hi_decimal'])
if __name__=='__main__':main()
