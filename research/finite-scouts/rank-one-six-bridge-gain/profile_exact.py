#!/usr/bin/env python3
"""Exact certificates for one representative/minimum per observed atlas block profile."""
import json
from certify import certify,graph6_candidate
from pathlib import Path

def main():
 cs=[]
 specs=[
  ('profile (6): FreRW root 1', 'FreRW',1,[('sigma_G','>',(23,4)),('F','>',(23,4))]),
  ('profile (5,1): F{e[o root 3','F{e[o',3,[('sigma_G','>',(10,1)),('F','>',(10,1))]),
  ('profile (3,3): FK|ko root 4','FK|ko',4,[('sigma_G','>',(10,1)),('F','>',(10,1))]),
 ]
 for name,r,v,claims in specs:
  cs.append(certify(name,graph6_candidate('Fhe?G',5,r,v),claims))
 out={'scope':'exact certificates for numerical profile minima among graph-atlas rank-six sides for fixed C5-P2 root 5; finite nonexhaustive evidence','certificates':cs}
 Path(__file__).with_name('profile-exact-certificates.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 for c in cs:
  print(c['name']);print(' charpoly G:',c['charpoly']['G']);print(' sigma_G',c['values']['sigma_G']);print(' F',c['values']['F'])
if __name__=='__main__':main()
