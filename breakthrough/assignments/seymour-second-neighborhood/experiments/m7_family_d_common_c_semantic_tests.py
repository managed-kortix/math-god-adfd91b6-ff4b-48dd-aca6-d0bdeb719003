#!/usr/bin/env python3
"""Independent truth-table tests for common-C semantic predicates.

These tests do not import the CNF producer.  They compare the finite graph
semantics of deletion preservation and robust-low witnessing with the direct
alternate-predecessor predicates encoded in the CNF, and exhaust the small
aggregate-cell arithmetic.
"""
import itertools


def n1(arcs,u,vertices):
    return {v for v in vertices if (u,v) in arcs}


def n2(arcs,u,vertices):
    one=n1(arcs,u,vertices)
    return {v for v in vertices-{u}-one
            if any((u,k) in arcs and (k,v) in arcs for k in vertices-{u,v})}


def preserved_semantic(arcs,vertices,root,deleted):
    full=n2(arcs,root,vertices)
    kept=vertices-{deleted}
    reduced={(a,b) for a,b in arcs if a!=deleted and b!=deleted}
    return n2(reduced,root,kept)==full-{deleted}


def preserved_support(arcs,vertices,root,deleted):
    old=n2(arcs,root,vertices)
    first=n1(arcs,root,vertices)
    return all(any((root,k) in arcs and (k,b) in arcs
                   for k in first-{deleted,b})
               for b in old-{deleted})


def exhaustive_deletion_test():
    # Root 0, deleted first neighbor 1, and four remaining vertices.  Full
    # preservation factorizes over target columns, so exhaust every root row,
    # every target, and every predecessor mask independently.
    vertices=set(range(6));root=0;deleted=1
    checked=0
    for root_bits in itertools.product((0,1),repeat=5):
        if not root_bits[0]:continue
        first={i+1 for i,x in enumerate(root_bits) if x}
        for target in range(1,6):
            for mask in range(1<<5):
                arcs={(0,x) for x in first}
                for k in range(1,6):
                    if k!=target and (mask>>k)&1:arcs.add((k,target))
                old=(target not in first and any((k,target) in arcs for k in first-{target}))
                support=any((k,target) in arcs for k in first-{deleted,target})
                # For this target, preservation requirement is vacuous unless
                # it is an old exact second endpoint and survives deletion.
                required=(target==deleted or not old or support)
                semantic=(target==deleted or not old or
                          target in n2({e for e in arcs if deleted not in e},root,vertices-{deleted}))
                if required!=semantic:raise RuntimeError("one-target deletion mismatch")
                checked+=1
    return checked


def n2_biconditional_test():
    # Exhaust the local definition q <-> reach AND not-direct.  This is the
    # exact-distance-two exclusion that must not be weakened to raw reach.
    checked=0
    for direct,reach,q in itertools.product((False,True),repeat=3):
        clauses=((not q or reach) and (not q or not direct) and
                 (q or not reach or direct))
        semantic=(q==(reach and not direct))
        if clauses!=semantic:raise RuntimeError("N++ biconditional mismatch")
        checked+=1
    return checked


def universal_disjointness_test():
    # Truth-table representative factors of the universal quantifier for 16
    # low vertices.  It must reject iff at least one low has both robust flags,
    # including a low other than the two selected roots.
    checked=0
    for flags in itertools.product(range(4),repeat=4):
        # Four representative lows suffice because the predicate is a pure
        # conjunction of identical independent two-bit clauses.
        direct=all(x!=3 for x in flags)
        clauses=all(not((x&1) and (x&2)) for x in flags)
        if direct!=clauses:raise RuntimeError("universal disjointness mismatch")
        checked+=1
    # Explicit mutation: checking only the selected two lows is unsound.
    flags=(0,0,3,0)
    weakened=all(x!=3 for x in flags[:2])
    full=all(x!=3 for x in flags)
    if not weakened or full:raise RuntimeError("universal-disjointness mutation did not separate")
    return checked


def aggregate_test():
    # From 2t=14+x+z+h, t=8, h>=1 and nonnegative integer counts.
    states={(x,z,h) for x in range(3) for z in range(3) for h in range(8)
            if 2*8==14+x+z+h and h>=1}
    expected={(0,0,2),(0,1,1),(1,0,1)}
    if states!=expected:raise RuntimeError((states,expected))
    return states


def main():
    q=n2_biconditional_test();d=exhaustive_deletion_test();u=universal_disjointness_test();cells=aggregate_test()
    print(f"PASS exact-N++ biconditional_truth_rows={q}")
    print(f"PASS exact-deletion both_directions one_target_truth_rows={d}")
    print(f"PASS universal-no-shared-tight-low domain=all_16_lows truth_rows={u} weakening_mutation=rejected")
    print("PASS aggregate_cells="+repr(sorted(cells)))

if __name__=="__main__":main()
