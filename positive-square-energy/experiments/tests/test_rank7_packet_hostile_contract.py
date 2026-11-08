#!/usr/bin/env python3
"""Dependency-free exact hostile tests of the inherited packet verifier."""
import ast
from fractions import Fraction
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'rank6_order10_cubic_exact_rational.py'
names = {'require', 'dot', 'rational_unit', 'exact_step_cost', 'audit_parameters', 'verify_shared'}
tree = ast.parse(p.read_text())
ns = {'Fraction': Fraction, 'DIMENSION': 8, 'ORDER': 8, 'PATH_COUNT': 14, 'BUDGET': Fraction(6)}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names], type_ignores=[]), str(p), 'exec'), ns)
z = (Fraction(0),) * 7
# A synthetic even-path ledger isolates dimensions and acceptance from census.
ns['path_ledger'] = lambda *_: [(i, 0, 0, 1, 2) for i in range(14)]
w = (1, (z,) * 8, ((z,),) * 14, ((z,z,z),) * 14)
ns['verify_shared'](None, None, w)
for j in range(1, 30):
    row = tuple(Fraction(j-i, j+i+1) for i in range(7))
    v = ns['rational_unit'](row)
    assert len(v) == 8 and sum(x*x for x in v) == 1
    assert ns['exact_step_cost'](v,v) == 0
bad = [
    (1, (z[:-1],) + w[1][1:], w[2], w[3]),
    (1, w[1], ((z[:-1],),) + w[2][1:], w[3]),
    (1, w[1], w[2], ((z,z),) + w[3][1:]),
    (1, w[1][:-1], w[2], w[3]),
    (1, w[1], w[2][:-1], w[3]),
    (0, *w[1:]),
]
for witness in bad:
    try:
        ns['verify_shared'](None, None, witness)
    except (RuntimeError, ZeroDivisionError):
        pass
    else:
        raise AssertionError('malformed witness accepted')
# Tree extension: antipodal original vectors give DNN edge cost exactly one.
v = ns['rational_unit'](tuple(Fraction(i,11) for i in range(7)))
r = sum(a*(-a) for a in v)
assert r == -1 and Fraction(2)/(1-r) == 1
print('PASS: exact units, six malformed witnesses rejected, tree edge cost one')
