#!/usr/bin/env python3
"""Regenerate and retain the sixteen historical final k=5 LRAT shards."""
import argparse,hashlib,json,lzma,os,subprocess,tempfile,time

EXPECTED={
(0,1):("9eed73ca7260c2f6724b7aa15401dda7cc42159446b4833f356904792ab63638","2a1bc3b8c5b6e34b9d9406d9b54617abfddf414c5c19d97e8d0a24d45e88e962"),(0,2):("266ac8d44462f221388dcc9c0a36380297f73711649845470dc7df0ab0ac0de7","5497e43faffc9e2d806dab32c009909a7ff0e0f0f7ea5c113abfb2b8cf7a473b"),
(1,1):("84f0720c4361ea447cb8dbf7033aca93509dce84d6d5a51214c7d929ac4b92bc","313d3a51a73df3c479b4f49e99e6aba6fa560ec9faf7c153b8733fb8f9cbf245"),(1,2):("f634cc0049b19fe8c469432b0adab409c50f8033b757c78d02f9f9fb29b6cf9b","d8ca60ab812d73a880bd4769e0336c07f11034ae89370b383a1638d8a67a3e9d"),
(0,0,0):("9683e9d85a0fa0e699ba6ef87f0519d50d6f7699f8253083b3ad49207659e753","38da538186a91f86326f8275f962807d8e6356ccd85d37ef599bb156464312e9"),(0,0,1):("24510ccc29202ab83d5caf32a5c5faaa351d6f1cfe39a61c1a916aed8c6bb16e","f62a99f4625273809a70b75f0a53acea31a3c805fa80942f9592eba01896c598"),(0,0,2):("64c04f0c725e8b30d62bc4218d5d458b3f070733c96af0164f91326f1401f4df","b78087e9f530fbc1e9abb5072929c19a63b5197e355d77af0ea9f192cbc26cdb"),(0,0,3):("25ee72b619ecbcec5a7047266919932708165c0f8e3504c0d894e7c9de71de40","75ae679f721b391fe3ffc7dd1b842085e3b0677e6d8eda425818bcb2ca252144"),(0,0,4):("05a0879660458bc56f64ffa02ede4c8ee9ba7810ccaa5822a2afc928679103ec","007cabbbf89a9c5b57c78cddbdb8e796fc78956a84da957ec9819884b841ff6a"),(0,0,5):("c76eabcf2e440369776f99d7b4be1b5ebea937077c2b380d51a8f523873142b0","bb0c4cd73c8345c9f5f15904f055b3ca465d7090bf0c3acdccbd7cedfb01d19c"),
(1,0,0):("cc2ed5a7001d6aff54c5067e900d621f25cd69b2995223f926525f1249ccda54","da6b8c386fbae5408f82dd6220c5896af24fb9894de5c42203595dd57a6e7f92"),(1,0,1):("0810309f31aad1a1a80d941ae86a5e815d7e38f7d89e4b457c3e49961ea4b532","47427cf0bde4a93b41f19c030d9b47fa138c1c8cdcc243632c7dc0176c6489c0"),(1,0,2):("87b9d8f54dabd7aaedca3a26944321fdbe6e9a7fee85cb7fc08842e0b5728a4f","b7d83be209d05b192f6e39b1288b0c750e632b300306a5c433690ffd693d0271"),(1,0,3):("53eb2a6059857ebc0f84f0fbb487ce1214cdba5ae1597ffd3feffd1e3a1e81d0","c2ae63eb25bd3cfcc7c1a0b9f47ace9e58f976f1e96934bd1defb17729c8cb27"),(1,0,4):("3d07cf206fcf36fdceb6f2b4da98b69eeaeaaff3ef95ddec9d63a3b203470f7c","79ce1ba162554a55dbd51a301bda05b64c4bae77e9fd99fac20d22304ab01e3f"),(1,0,5):("36ce7f65d36e124873e5b09dfb0be1ebb76967054ebec94725124c02f07f01a7","3867b06e9d02cda4eed3091c48bd04551bb2e67afc128b62713ac4c5a35b2452")}

def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()

def main():
 p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--cadical",required=True);p.add_argument("--checker",required=True);a=p.parse_args()
 for d in ("leaves","objects","work"):os.makedirs(os.path.join(a.root,d),exist_ok=True)
 for key,expected in EXPECTED.items():
  rho,g,*hb=key;name=f"rho{rho}-g{g}"+(f"-hB{hb[0]}" if hb else "");meta=os.path.join(a.root,"leaves",name+".json")
  if os.path.exists(meta):print(name,"SKIP",flush=True);continue
  with tempfile.TemporaryDirectory(dir=os.path.join(a.root,"work")) as d:
   cnf=os.path.join(d,"x.cnf");proof=os.path.join(d,"x.lrat");cmd=["python3",os.path.join(os.path.dirname(__file__),"m9-final-shards.py"),str(rho),"5",str(g),cnf]+(["--hB",str(hb[0])] if hb else []);subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL);assert sha(cnf)==expected[0]
   t=time.monotonic();r=subprocess.run([a.cadical,"--lrat","--no-binary","-q",cnf,proof]);secs=round(time.monotonic()-t,3);assert r.returncode==20
   q=subprocess.run([a.checker,cnf,proof],capture_output=True,text=True);assert q.returncode==0 and "c VERIFIED" in q.stdout;assert sha(proof)==expected[1]
   obj=os.path.join(a.root,"objects",expected[1]+".lrat.xz");tmp=obj+".partial"
   with open(proof,"rb") as src,lzma.open(tmp,"wb",preset=3) as dst:
    while b:=src.read(1<<20):dst.write(b)
   os.replace(tmp,obj);rec={"key":key,"name":name,"cnf_sha256":expected[0],"cnf_bytes":os.path.getsize(cnf),"lrat_sha256":expected[1],"lrat_bytes":os.path.getsize(proof),"object":os.path.basename(obj),"object_sha256":sha(obj),"object_bytes":os.path.getsize(obj),"seconds":secs,"status":"UNSAT_VERIFIED"}
   with open(meta+".partial","w") as f:json.dump(rec,f,sort_keys=True);f.write("\n")
   os.replace(meta+".partial",meta);print(name,rec["lrat_bytes"],rec["object_bytes"],secs,flush=True)

if __name__=="__main__":main()
