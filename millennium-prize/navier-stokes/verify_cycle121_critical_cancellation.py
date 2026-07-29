#!/usr/bin/env python3
"""Exact arithmetic certificate for Cycle 121 critical-flux cancellation."""
from fractions import Fraction as F

radii=(3,4,5,14,15)
rates=(F(-48),F(-64),F(898,7),F(-20,7),F(-94,7))
assert sum(rates,F(0))==0
assert sum((F(r)*e for r,e in zip(radii,rates)),F(0))==0
forward=3*F(-48)+4*F(-64)+5*F(112)
back=14*F(-20,7)+15*F(-94,7)+5*F(114,7)
assert forward==160 and back==-160
print("ordinary nonlinear energy derivative = 0")
print("forward critical contribution = 160")
print("backscatter critical contribution = -160")
print("total nonlinear H^(1/2) derivative = 0")
print("all exact checks passed")
