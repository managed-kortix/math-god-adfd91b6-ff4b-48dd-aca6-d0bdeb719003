#!/usr/bin/env python3
"""Mutation tests bypass pins intentionally and never write artifacts."""
import copy
import importlib.util
import lzma
from pathlib import Path
H=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('v',H/'rank7_order8_structural_exact_verifier.py')
v=importlib.util.module_from_spec(s); s.loader.exec_module(v)
def reject(f):
    try:f()
    except (ValueError,TypeError,KeyError,IndexError):return
    raise RuntimeError('mutation accepted')
def main():
    o=v.decode(lzma.decompress((H/'rank7_order8_structural_cycle_gram_owners.jsonl.xz').read_bytes()).splitlines(keepends=True)[0]); v.replay(o)
    changes=[((1,5),[-1,1]),((1,3),[1,1]),((1,2),[0,1]),((1,0),o[0][0]),((1,0),True),((1,1),1),((0,3,0,2),True),((1,5),[0,2]),((3,0,0),999),((1,4,0,0,1),0)]
    n=0
    for path,value in changes:
        x=copy.deepcopy(o); z=x
        for k in path[:-1]:z=z[k]
        z[path[-1]]=value; reject(lambda:v.replay(x)); n+=1
    for bad in (b'{"a":1,"a":1}\n',b'[1, 2]\n',b'[NaN]\n',b'[1]\n\n'):
        reject(lambda:v.decode(bad)); n+=1
    p=[[v.F(i==j) for j in range(14)] for i in range(14)];p[0][1]=1
    reject(lambda:v.check_projector(p,[[v.F(0)]*14 for _ in range(7)]));n+=1
    sr=(v.canonical(o[0])+'\n').encode();r=copy.deepcopy(o[0]);r[0]+=1;r[1]+=1;rr=(v.canonical(r)+'\n').encode()
    v.partition([sr,rr],[o],[rr])
    for source,owners,rem in (([sr,rr],[o,o],[rr]),([sr,rr],[o],[]),([sr,rr],[],[rr,sr]),([rr],[o],[rr]),([sr,sr],[o],[])):
        reject(lambda:v.partition(source,owners,rem));n+=1
    print('structural hostile mutation tests: PASS cases='+str(n))
if __name__=='__main__':main()
