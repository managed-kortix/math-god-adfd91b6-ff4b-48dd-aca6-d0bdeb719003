#!/usr/bin/env python3
"""Exact synchronized C-incident row count for order-18 m=7 family S.

Family S fixes a low root w witnessing both highs r,q.  Its rooted layers have
|A|=8, |B|=7, |C|=2, with r,q in A.  This script counts every labelled state
of all pairs incident with C (holes and orientations), together with the number
h of residual holes wholly inside T={w} union A union B.  It quotients only by
swapping the two C labels.

It is an exact necessary projection, not a graph-completion cover.  In
particular it does not yet orient T or synchronize A--B row degrees.
"""
from collections import Counter
from math import comb

# Row data:
# m: C-pair is a hole; d0,d1: direction of the present C-pair;
# ai: holes from ci to {w} union A (nine labelled possible pairs);
# ri=ai-1-di: arcs ci->B, by exact degree eight;
# bi: holes from ci to B among the 7-ri labels not used by ci->B;
# h=7-(a0+a1+m+b0+b1): holes internal to T.


def labelled_weight(a0, a1, r0, r1, b0, b1):
    return (comb(9, a0) * comb(9, a1) *
            comb(7, r0) * comb(7-r0, b0) *
            comb(7, r1) * comb(7-r1, b1))


def fixed_weight(m, a, r, b):
    """States fixed by C-swap.

    A present C-pair direction is reversed by the swap, hence has no fixed
    state.  For m=1, both C rows must use identical labelled hole/out masks.
    """
    if not m:
        return 0
    return comb(9, a) * comb(7, r) * comb(7-r, b)


def main():
    labelled = Counter()
    fixed = Counter()
    scalar = Counter()

    for m in (0, 1):
        directions = ((0, 0),) if m else ((1, 0), (0, 1))
        for d0, d1 in directions:
            for a0 in range(10):
                r0 = a0 - 1 - d0
                if not 0 <= r0 <= 7:
                    continue
                for a1 in range(10):
                    r1 = a1 - 1 - d1
                    if not 0 <= r1 <= 7:
                        continue
                    for b0 in range(8-r0):
                        for b1 in range(8-r1):
                            h = 7-a0-a1-m-b0-b1
                            if h < 0:
                                continue
                            w = labelled_weight(a0,a1,r0,r1,b0,b1)
                            labelled[h] += w
                            scalar[h] += 1
                            if m and a0 == a1 and r0 == r1 and b0 == b1:
                                # Fixed states require the actual labelled masks
                                # to agree, counted by one rather than two mask
                                # choices.
                                fixed[h] += fixed_weight(m,a0,r0,b0)

    total = sum(labelled.values())
    fixed_total = sum(fixed.values())
    orbits = (total + fixed_total)//2
    by_h_orbits = {h:(labelled[h]+fixed[h])//2 for h in sorted(labelled)}

    # Frozen values independently reproduced by m7_family_s_exact_rows_check.py.
    expected_labelled = 138188079
    expected_fixed = 3789
    expected_by_h = {
        0: 61327035, 1: 7214130, 2: 532665, 3: 21735, 4: 369,
    }
    assert total == expected_labelled
    assert fixed_total == expected_fixed
    assert by_h_orbits == expected_by_h
    assert orbits == 69095934
    assert sum(scalar.values()) == 210

    print(f"PASS family-S exact-C labelled={total} fixed={fixed_total} orbits={orbits}")
    print(f"PASS by_T_holes_orbits={by_h_orbits}")
    print("PASS scalar margins=210 (the corrected epsilon=0 rows)")
    print("NOTE T orientations and A--B degree/robustness synchronization remain")


if __name__ == '__main__':
    main()
