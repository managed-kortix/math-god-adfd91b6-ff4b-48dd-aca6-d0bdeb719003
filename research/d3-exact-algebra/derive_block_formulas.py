#!/usr/bin/env python3
"""Emit collision-safe compact direct formulas for all six direct D+T^3 records."""
import itertools
owners=('A','B','x')
def dd(S):return 'D'+('_{'+','.join(S)+'}' if S else '')
def direct(roots):
 out=[]
 for bits in range(8):
  S=[i for i in range(3) if bits>>i&1]
  selected=[roots[i] for i in S]
  # Two Sachs components cannot both occupy one shared cut vertex.
  if len(selected)!=len(set(selected)):continue
  dels=tuple(sorted(set(selected)))
  coeff=' '.join(f'q{i+1}' if i in S else f'd{i+1}' for i in range(3))
  out.append((coeff,dd(dels)))
 return out
for roots in itertools.combinations_with_replacement(owners,3):
 if 'x' not in roots:continue
 print('direct',roots,':',' + '.join(c+' '+h for c,h in direct(roots)))
