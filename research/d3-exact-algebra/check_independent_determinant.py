#!/usr/bin/env python3
"""Independent exact subset-DP determinant cross-check of all 14 raw Sachs polynomials."""
import importlib.util
from collections import defaultdict
P=str(__import__('pathlib').Path(__file__).with_name('r31-s-d3-full-sachs-diagnostic.py'));sp=importlib.util.spec_from_file_location('d3',P);d3=importlib.util.module_from_spec(sp);sp.loader.exec_module(d3)
def determinant(V,E):
 n=len(V);ix={v:i for i,v in enumerate(V)};adj={tuple(sorted((ix[a],ix[b]))) for a,b in E}
 # State after rows 0..i-1: (used columns, diagonal support)->Gaussian coeff.
 # Gaussian coefficients stay in Z[i]; represent them as exact integer pairs.
 dp={(0,0):(1,0)}
 for i in range(n):
  nd=defaultdict(lambda:(0,0))
  for (used,mask),c in dp.items():
   for j in range(n):
    if used>>j&1:continue
    if i==j:entry=(0,1);nmask=mask|(1<<i)
    elif tuple(sorted((i,j))) in adj:entry=(-1,0);nmask=mask
    else:continue
    # Number of earlier chosen columns greater than j gives new inversions.
    inv=(used >> (j+1)).bit_count();sign=-1 if inv&1 else 1
    ar,ai=c;br,bi=entry;prod=(sign*(ar*br-ai*bi),sign*(ar*bi+ai*br))
    old=nd[(used|1<<j,nmask)];nd[(used|1<<j,nmask)]=(old[0]+prod[0],old[1]+prod[1])
  dp=nd
 # Multiply by i^(-n), exactly one of {1,-i,-1,i}.
 factor=((1,0),(0,-1),(-1,0),(0,1))[n%4]
 gauss={}
 for (used,mask),(ar,ai) in dp.items():
  br,bi=factor;gauss[mask]=(ar*br-ai*bi,ar*bi+ai*br)
 assert all(used==(1<<n)-1 for used,mask in dp)
 R={m:c[0] for m,c in gauss.items() if c[0]};I={m:c[1] for m,c in gauss.items() if c[1]}
 return R,I
for rec in sorted(d3.records(),key=repr):
 V,E=d3.graph_for(rec);R,I,_=d3.full_sachs_polynomial(V,E);Dr,Di=determinant(V,E);assert R==Dr and I==Di,(rec,len(R),len(Dr),len(I),len(Di));print('PASS',repr(rec),len(R),len(I))
