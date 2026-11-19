#!/usr/bin/env python3
"""Ensure the standalone SAT semantic checker remains fail-closed under -O."""
import json,subprocess,tempfile
from pathlib import Path
from m7_family_s_badness_pilot import canonical_rows

HERE=Path(__file__).resolve().parent
CHECKER=HERE/'m7_family_s_badness_check.py'


def require(condition,message):
    if not condition:
        raise RuntimeError(message)


def run(graph,row):
    return subprocess.run(['python3','-O',str(CHECKER),'--graph',str(graph),'--row',row],
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)


def main():
    row=json.dumps(canonical_rows(False,4)[0],separators=(',',':'))
    with tempfile.TemporaryDirectory(prefix='m7h4-semantic-') as td:
        graph=Path(td)/'hostile.graph'
        graph.write_text('18\n0 1\n1 0\n',encoding='ascii')
        result=run(graph,row)
        require(result.returncode!=0,f'optimized semantic checker accepted hostile graph:\n{result.stdout}')
    print('PASS h4 semantic checker python-O hostile_graph=1')


if __name__=='__main__':
    main()
