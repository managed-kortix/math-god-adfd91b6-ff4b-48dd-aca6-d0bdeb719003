#!/usr/bin/env python3
"""Exact six-bit audit of the P5 packet compatibility table."""
import itertools


def packets(A,B,C,D,E,F):
    return {
        "02": (not A) and B and (C == F),
        "03": A and (not B) and C and (not D),
        "12": (not A) and D and (E == F),
        "13": ((not B) and (D or E)) or (B and (not D) and E),
        "14": (not C) and D and E and (not F),
        "23": (not D) and F and (A == B),
        "24": (not E) and F and (A == C),
    }


def main():
    best=0; witnesses=[]
    for bits in itertools.product((False,True),repeat=6):
        active=tuple(k for k,v in packets(*bits).items() if v)
        if len(active)>best: best=len(active);witnesses=[(bits,active)]
        elif len(active)==best:witnesses.append((bits,active))
    assert best==2
    print(f"PASS assignments=64 maximum={best} maximizers={len(witnesses)}")


if __name__=="__main__":main()
