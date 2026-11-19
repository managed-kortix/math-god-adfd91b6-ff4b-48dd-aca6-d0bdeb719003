#!/usr/bin/env python3
"""Independent Burnside/dynamic-program check of family-S C type rows."""
from collections import Counter,defaultdict
from itertools import combinations_with_replacement,product

A_TYPES=((0,0),(0,1),(1,0),(1,1))
STATES=(('M',0,0,1),('01',1,0,0),('10',0,1,0))
SW={'M':'M','01':'10','10':'01'}

def hist(word,k):return tuple(word.count(i) for i in range(k))
def swap(row):
 s,d,a,b,h=row
 sa=(0,2,1,3)
 return (SW[s],tuple(sa[x]for x in d),tuple(a[sa[x]]for x in range(4)),
         tuple(b[3*(x%3)+(x//3)]for x in range(9)),h)

def main():
 # Build multisets independently via combinations_with_replacement, rather
 # than the production weak-composition recursion.
 U=defaultdict(list)
 for d in product(range(4),repeat=3):
  for word in combinations_with_replacement(range(4),6):
   a=hist(word,4)
   a0=sum(A_TYPES[x][0]for x in d)+sum(A_TYPES[x][0]for x in word)
   a1=sum(A_TYPES[x][1]for x in d)+sum(A_TYPES[x][1]for x in word)
   U[a0,a1].append((d,a))
 B=defaultdict(list)
 for word in combinations_with_replacement(range(9),7):
  b=hist(word,9)
  r0=sum(x//3==0 for x in word);r1=sum(x%3==0 for x in word)
  h0=sum(x//3==2 for x in word);h1=sum(x%3==2 for x in word)
  B[r0,r1].append((h0,h1,b))
 rows=[]
 for s,d0,d1,m in STATES:
  for (a0,a1),us in U.items():
   r0,r1=a0-1-d0,a1-1-d1
   for d,a in us:
    for b0,b1,b in B.get((r0,r1),()):
     h=7-a0-a1-m-b0-b1
     if h>=0:rows.append((s,d,a,b,h))
 fixed=sum(x==swap(x)for x in rows)
 by=Counter(min(x,swap(x))[-1]for x in rows)
 # Counting canonical keys via a set guards against accidental multiplicity.
 can={min(x,swap(x))for x in rows}
 assert len(rows)==26060 and fixed==174 and len(can)==13117
 assert Counter(x[-1]for x in can)=={0:8764,1:3093,2:999,3:218,4:43}
 print(f"PASS independent family-S type rows={len(rows)} fixed={fixed} orbits={len(can)}")
 print(f"PASS independent by_h={dict(sorted(Counter(x[-1]for x in can).items()))}")

if __name__=='__main__':main()
