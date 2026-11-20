#!/usr/bin/env python3
"""Hostile fail-closed mutation suite for the staged parent-20 package."""
from __future__ import annotations
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parents[1]
VERIFIER = Path("verifier/verify_parent20_package.py")


def run(root: Path, identity_only=True):
    cmd=[sys.executable,"-B",str(root/VERIFIER)]
    if identity_only: cmd.append("--identity-only")
    return subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)


def mutate_bytes(root, rel, offset=0):
    p=root/rel; b=bytearray(p.read_bytes()); b[offset % len(b)] ^= 1; p.write_bytes(b)


def mutate_json(root, fn):
    p=root/"metadata/certificate.json"; m=json.loads(p.read_text("ascii")); fn(m)
    p.write_text(json.dumps(m,sort_keys=True,indent=2,ensure_ascii=True)+"\n",encoding="ascii")


def case(name, fn, identity_only=True):
    with tempfile.TemporaryDirectory(prefix=f"p20-mut-{name}-") as td:
        root=Path(td)/"package"; shutil.copytree(PACKAGE,root,symlinks=True)
        fn(root)
        r=run(root,identity_only)
        if r.returncode == 0:
            raise RuntimeError(f"mutation escaped: {name}\n{r.stdout}")
        print(f"PASS reject {name}")


def main():
    clean=run(PACKAGE,True)
    if clean.returncode:
        raise RuntimeError(f"clean identity gate failed\n{clean.stdout}")
    cases=[
      ("extra-file",lambda r:(r/"EXTRA").write_text("x")),
      ("missing-artifact",lambda r:(r/"artifacts/parent20.cnf").unlink()),
      ("symlink-artifact",lambda r:((r/"artifacts/parent20.cnf").unlink(),os.symlink("../ledger/m5-b7-parent20-probe.tsv",r/"artifacts/parent20.cnf"))),
      ("cnf-byte",lambda r:mutate_bytes(r,"artifacts/parent20.cnf",200)),
      ("xz-byte",lambda r:mutate_bytes(r,"artifacts/parent20.lrat.xz",1000)),
      ("ledger-byte",lambda r:mutate_bytes(r,"ledger/m5-b7-parent20-probe.tsv",80)),
      ("checker-binary",lambda r:mutate_bytes(r,"tools/lrat-check",500)),
      ("checker-source",lambda r:mutate_bytes(r,"tools/lrat-check.c",100)),
      ("common-encoder",lambda r:mutate_bytes(r,"source-pins/snc_cnf.py",100)),
      ("cover-checker",lambda r:mutate_bytes(r,"source-pins/check_m5_selector_batch_cnf.py",100)),
      ("manifest-hash",lambda r:mutate_bytes(r,"metadata/SHA256SUMS",1)),
      ("unsafe-manifest-path",lambda r:(r/"metadata/SHA256SUMS").write_text((r/"metadata/SHA256SUMS").read_text().replace("  artifacts/parent20.cnf","  ../parent20.cnf",1))),
      ("mode-drift",lambda r:os.chmod(r/"artifacts/parent20.cnf",0o600)),
      ("root-low",lambda r:mutate_json(r,lambda m:m["bridge"].__setitem__("root_is_low",False))),
      ("high-count",lambda r:mutate_json(r,lambda m:m["bridge"].__setitem__("high_vertices",5))),
      ("transport-wording",lambda r:mutate_json(r,lambda m:m["bridge"].__setitem__("semantic_transport","literal CNF automorphism"))),
      ("packet-count",lambda r:mutate_json(r,lambda m:m["universes"].__setitem__("packet_labelled",91))),
      ("witness-count",lambda r:mutate_json(r,lambda m:m["universes"].__setitem__("witness_rows",67))),
      ("hard-labelled-count",lambda r:mutate_json(r,lambda m:m["universes"].__setitem__("hard_labelled_assignments",323399))),
      ("selector-count",lambda r:mutate_json(r,lambda m:m["cnf"].__setitem__("selectors",1345))),
      ("guard-stratum",lambda r:mutate_json(r,lambda m:m["cnf"]["strata"].__setitem__("guarded_hard_high_literals",19979))),
      ("alo-stratum",lambda r:mutate_json(r,lambda m:m["cnf"]["strata"].__setitem__("selector_alo",0))),
      ("independence-boundary",lambda r:mutate_json(r,lambda m:m["common_base"].__setitem__("independence_boundary","fully independent encoder"))),
      ("raw-proof-hash",lambda r:mutate_json(r,lambda m:m["proof"].__setitem__("raw_sha256","0"*64))),
      ("raw-proof-size",lambda r:mutate_json(r,lambda m:m["proof"].__setitem__("raw_bytes",m["proof"]["raw_bytes"]-1))),
      ("compressed-proof-hash",lambda r:mutate_json(r,lambda m:m["proof"].__setitem__("xz_sha256","0"*64))),
      ("cnf-identity",lambda r:mutate_json(r,lambda m:m["identities"]["cnf"].__setitem__("sha256","0"*64))),
      ("checker-identity",lambda r:mutate_json(r,lambda m:m["checker"].__setitem__("binary_sha256","0"*64))),
      ("solver-identity",lambda r:mutate_json(r,lambda m:m["producer"].__setitem__("binary_sha256","0"*64))),
      ("parent-hole",lambda r:mutate_json(r,lambda m:m["canonical_parent"]["holes"].__setitem__(0,[0,10]))),
      ("parent-ordinal",lambda r:mutate_json(r,lambda m:m["canonical_parent"].__setitem__("ordinal",19))),
      ("base-clause-hash",lambda r:mutate_json(r,lambda m:m["common_base"].__setitem__("clause_stream_sha256","0"*64))),
      ("compressed-cap",lambda r:mutate_json(r,lambda m:m.__setitem__("compression_cap_bytes",5_000_000))),
      ("solver-role",lambda r:mutate_json(r,lambda m:m["producer"].__setitem__("role","proof validity"))),
      ("checker-role",lambda r:mutate_json(r,lambda m:m["checker"].__setitem__("role","provenance only"))),
      ("ancestry",lambda r:mutate_json(r,lambda m:m["ancestry"].__setitem__("parent_cover_is_ancestor_of_ledger",False))),
    ]
    for name,fn in cases: case(name,fn)
    print(f"PASS hostile mutation suite cases={len(cases)}")

if __name__=="__main__":
    try: main()
    except Exception as exc:
        print(f"FAIL {exc}",file=sys.stderr); raise SystemExit(1)
