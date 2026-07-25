#!/usr/bin/env python3
import os, subprocess, tempfile

HERE = os.path.dirname(__file__)
V = [["python3", os.path.join(HERE,"verify_set.py")], ["node", os.path.join(HERE,"verify_matrix.js")]]
CASES = {
 "single": ("1\n", 1),
 "one_arc": ("2\n0 1\n", 1),
 "cycle3": ("3\n0 1\n1 2\n2 0\n", 1),
 "transitive": ("3\n0 1\n0 2\n1 2\n", 1),
 "path3": ("4\n0 1\n1 2\n2 3\n", 1),
 "two_paths": ("4\n0 1\n0 2\n1 3\n2 3\n", 1),
 "loop": ("1\n0 0\n", 2), "digon": ("2\n0 1\n1 0\n", 2),
 "duplicate": ("2\n0 1\n0 1\n", 2), "unsorted": ("3\n1 2\n0 1\n", 2),
 "zero": ("0\n", 2), "junk": ("2\n0 1 x\n", 2),
}
with tempfile.TemporaryDirectory() as d:
    for name,(text,expected) in CASES.items():
        path=os.path.join(d,name); open(path,"wb").write(text.encode())
        outputs=[]
        for command in V:
            p=subprocess.run(command+[path],capture_output=True,text=True)
            assert p.returncode == expected, (name,command,p.returncode,p.stdout,p.stderr)
            outputs.append((p.stdout,p.stderr))
        print(f"PASS {name}")
print("PASS hostile suite")
