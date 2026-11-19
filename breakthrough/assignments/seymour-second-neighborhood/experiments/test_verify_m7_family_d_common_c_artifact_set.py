#!/usr/bin/env python3
"""Regression tests for the common-C verifier's in-tree artifact-set contract."""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PACKAGE=ROOT/"certificates"/"m7-family-d-common-c"
VERIFY=HERE/"verify_m7_family_d_common_c_campaign.py"
CHECK=HERE/"check_m7_family_d_common_c_cnf.py"


def require(condition,message):
    if not condition:raise RuntimeError(message)


def invoke(package,drat_trim):
    return subprocess.run([
        sys.executable,str(VERIFY),"--manifest",str(package/"manifest.json"),
        "--proof-dir",str(package),"--drat-trim",str(drat_trim),
        "--cnf-checker",str(CHECK)],stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,text=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--drat-trim",type=Path,required=True)
    x=parser.parse_args()
    require(PACKAGE.is_dir(),"in-tree package is absent")

    # Natural in-tree invocation: manifest and all nine proofs share one
    # directory.  This is the documented package layout and must replay.
    good=invoke(PACKAGE,x.drat_trim)
    require(good.returncode==0 and
            good.stdout.splitlines().count(
                "PASS authenticated_regenerated_replayed common-C leaves=9")==1,
            "natural in-tree invocation failed:\n"+good.stdout[-2000:])

    # An otherwise identical package with unexpected junk must fail before
    # replay acceptance.  Copy rather than mutate the committed package.
    with tempfile.TemporaryDirectory(prefix="m7d-common-c-artifact-set-") as td:
        clone=Path(td)/"package"
        shutil.copytree(PACKAGE,clone)
        (clone/"unexpected-junk.txt").write_text("junk\n",encoding="ascii")
        bad=invoke(clone,x.drat_trim)
        require(bad.returncode!=0,"verifier accepted unexpected package junk")
        require("artifact-set mismatch" in bad.stdout,
                "junk rejection did not report artifact-set mismatch:\n"+bad.stdout[-2000:])
    print("PASS common-C natural_in_tree_invocation=1 unexpected_junk_rejected=1")

if __name__=="__main__":main()
