#!/usr/bin/env python3
"""Exact Sturm certificates for per-profile F minima in unit_star_scan.py."""
import json
from pathlib import Path
from certify import certify,graph6_candidate
HERE=Path(__file__).resolve().parent

def main():
 data=json.loads((HERE/'unit-star-results.json').read_text())
 if data.get('counts',{}).get('eligible_rows') != 90013: raise RuntimeError('corrected eligible-row census changed')
 rows=[r for r in data['minima'] if r['metric']=='F']
 certs=[]
 for r in rows:
  p='+'.join(map(str,r['positive_block_rank_profile']))
  claims=[('sigma_G','>',(4,1)),('F','>',(4,1)),('Gamma','>',(13,20))]
  certs.append(certify(f'actual unit-star profile {p} bounded-scan F minimum',
    graph6_candidate(r['U_g6'],r['U_root'],r['R_g6'],r['R_root']),claims))
 out={'scope':'one exact representative for each numerical F minimum by positive-block profile in unit_star_scan.py; bounded-family minima, not universal minima',
      'certificates':certs}
 (HERE/'unit-star-exact-certificates.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 for c in certs:
  print(c['name'])
  print(' R:',c['charpoly']['H'])
  print(' G:',c['charpoly']['G'])
  print(' sigma_G:',c['values']['sigma_G']['lo_decimal'],c['values']['sigma_G']['hi_decimal'])
  print(' Gamma:',c['values']['Gamma']['lo_decimal'],c['values']['Gamma']['hi_decimal'])
  print(' F:',c['values']['F']['lo_decimal'],c['values']['F']['hi_decimal'])
if __name__=='__main__':main()
