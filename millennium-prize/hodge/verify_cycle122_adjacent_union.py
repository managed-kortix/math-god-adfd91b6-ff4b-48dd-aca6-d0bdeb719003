#!/usr/bin/env python3
"""Exact W2 obstruction verifier for the adjacent Hermitian-plane union."""
MOD=0b100101; MASK=31; Z=(0,0,0,0)
def gm(a,b):
 r=0
 while b:
  if b&1:r^=a
  b>>=1;a<<=1
  if a&32:a^=MOD
 return r&MASK
def gp(a,n):
 r=1
 while n:
  if n&1:r=gm(r,a)
  a=gm(a,a);n//=2
 return r
def gi(a):return gp(a,30)
def wa(x,y):
 a,c=x;b,d=y;return a^b,c^d^gm(a,b)
def wn(x):a,c=x;return a,c^gm(a,a)
def wm(x,y):
 a,c=x;b,d=y;return gm(a,b),gm(gm(a,a),d)^gm(gm(b,b),c)
def wp(x,n):
 r=(1,0)
 while n:
  if n&1:r=wm(r,x)
  x=wm(x,x);n//=2
 return r
def ea(e,f):return tuple(a+b for a,b in zip(e,f))
def pa(p,q,add,zero):
 r=dict(p)
 for e,c in q.items():
  v=add(r.get(e,zero),c)
  if v==zero:r.pop(e,None)
  else:r[e]=v
 return r
def ps(p,c,mul,zero):return {e:v for e,a in p.items() if (v:=mul(a,c))!=zero}
def pm(p,q,add,mul,zero):
 r={}
 for e,a in p.items():
  for f,b in q.items():
   h=ea(e,f);v=add(r.get(h,zero),mul(a,b))
   if v==zero:r.pop(h,None)
   else:r[h]=v
 return r
def pp(p,n,add,mul,zero,one):
 r={Z:one}
 while n:
  if n&1:r=pm(r,p,add,mul,zero)
  p=pm(p,p,add,mul,zero);n//=2
 return r
def reduceq(p,U,add,mul,zero,one):
 mx=max((e[3] for e in p),default=0);pw=[{Z:one}]
 for _ in range(mx):pw.append(pm(pw[-1],U,add,mul,zero))
 r={}
 for e,c in p.items():
  n=e[3]
  if n<=1:r=pa(r,{e:c},add,zero)
  else:r=pa(r,{ea((e[0],e[1],e[2],1),f):mul(c,v) for f,v in pw[n-1].items()},add,zero)
 return r
def divq(F,U):
 w=dict(F);q={}
 while w:
  n=max(e[3] for e in w)
  if n<2:break
  for e,c in [(e,c) for e,c in w.items() if e[3]==n]:
   w=pa(w,{e:c},lambda a,b:a^b,0);h=(e[0],e[1],e[2],n-2);q=pa(q,{h:c},lambda a,b:a^b,0)
   w=pa(w,pm({(e[0],e[1],e[2],n-1):c},U,lambda a,b:a^b,gm,0),lambda a,b:a^b,0)
 assert not w;return q
def basis(d):
 r=[]
 for a in range(d+1):
  for b in range(d-a+1):r.append((a,b,d-a-b,0))
 for a in range(d):
  for b in range(d-a):r.append((a,b,d-1-a-b,1))
 return r
def cols(p,d,U):return [reduceq(pm(p,{e:1},lambda a,b:a^b,gm,0),U,lambda a,b:a^b,gm,0,1) for e in basis(d)]
def rank(cs,rows):
 ix={e:i for i,e in enumerate(rows)};piv={}
 for c in cs:
  v=dict(c)
  while v:
   j=min(ix[e] for e in v);e=rows[j];a=v[e]
   if j not in piv:piv[j]=ps(v,gi(a),gm,0);break
   v=pa(v,ps(piv[j],a,gm,0),lambda x,y:x^y,0)
 return len(piv)
def main():
 t=2;u=(1,t,t^1);A=((0,t,t^1),(t,gp(t,2)^1,gp(t,2)^t),(t^1,gp(t,2)^t,gp(t,2)))
 assert all((A[i][j]^(1 if i==j else 0))==gm(u[i],u[j]) for i in range(3) for j in range(3))
 xg=[{tuple(1 if j==i else 0 for j in range(4)):1} for i in range(4)]
 xw=[{tuple(1 if j==i else 0 for j in range(4)):(1,0)} for i in range(4)]
 Ug={};Uw={}
 for i in range(3):Ug=pa(Ug,ps(xg[i],u[i],gm,0),lambda a,b:a^b,0);Uw=pa(Uw,ps(xw[i],(u[i],0),wm,(0,0)),wa,(0,0))
 yg=[];yw=[]
 for i in range(3):
  yg.append(pa(xg[i],ps(xg[3],u[i],gm,0),lambda a,b:a^b,0))
  yw.append(pa(ps(xw[i],wn((1,0)),wm,(0,0)),ps(xw[3],(u[i],0),wm,(0,0)),wa,(0,0)))
 Fg={};Fw={}
 for i in range(3):
  Fg=pa(Fg,pp(xg[i],33,lambda a,b:a^b,gm,0,1),lambda a,b:a^b,0);Fg=pa(Fg,pp(yg[i],33,lambda a,b:a^b,gm,0,1),lambda a,b:a^b,0)
  Fw=pa(Fw,pp(xw[i],33,wa,wm,(0,0),(1,0)),wa,(0,0));Fw=pa(Fw,pp(yw[i],33,wa,wm,(0,0),(1,0)),wa,(0,0))
 rw=reduceq(Fw,Uw,wa,wm,(0,0),(1,0));assert all(c[0]==0 for c in rw.values())
 h={e:gp(c[1],16) for e,c in rw.items() if gp(c[1],16)}
 Q=reduceq(divq(Fg,Ug),Ug,lambda a,b:a^b,gm,0,1)
 y1=reduceq(pp(yg[1],32,lambda a,b:a^b,gm,0,1),Ug,lambda a,b:a^b,gm,0,1)
 y2=reduceq(pp(yg[2],32,lambda a,b:a^b,gm,0,1),Ug,lambda a,b:a^b,gm,0,1)
 C=cols(y1,1,Ug)+cols(y2,1,Ug)+cols(Q,2,Ug);R=basis(33)
 assert (len(h),len(y1),len(y2),len(Q),len(C),rank(C,R),rank(C+[h],R))==(245,244,244,243,17,17,18)
 print("A - I = u*u^T\nsupport(h) = 245\nsupport(reduce(y1^32)) = 244\nsupport(reduce(y2^32)) = 244\nsupport(reduce(Q)) = 243\nnormal columns = 17\nrank(M) = 17\nrank(M | h) = 18")
if __name__=="__main__":main()
