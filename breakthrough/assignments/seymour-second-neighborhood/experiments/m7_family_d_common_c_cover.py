#!/usr/bin/env python3
"""Independent labelled-state/orbit cover for common-C t=8 root overlaps.

Only the two rooted first-layer sets are considered here.  It does not build a
completion and does not use SAT.  The labels r,q,C are fixed, u,v are ordered,
and both selected witness arcs u->r and v->q are required.  States also obey
the exact root-pair restriction forced by rooted distance layers: v is in A_u
iff u is not in A_v; otherwise each root lies in the other's B-layer.
"""
import itertools

N=18
U,V,R,Q=0,3,1,2
C=frozenset((16,17))
VERTICES=frozenset(range(N))
TYPES=("oriented-both","oriented-one","root-hole")


def classify(au,av):
    """Classify a labelled state modulo exchanging (u,r) with (v,q)."""
    uv=V in au
    vu=U in av
    if uv and vu:
        raise ValueError("digon root pair")
    if not uv and not vu:
        kind="root-hole"
        signature=(int(Q in au),int(R in av))
        if signature!=(1,1):
            raise ValueError("root-hole t=8 forces both cross highs in the intersection")
        return kind
    # Canonically orient the unique root arc from u to v.
    if vu:
        au,av=swap_state(au,av)
    cross=(int(Q in au),int(R in av))
    if cross==(1,1): return "oriented-both"
    if cross in ((0,1),(1,0)): return "oriented-one"
    raise ValueError("oriented t=8 cannot omit both cross highs")


def swap_state(au,av):
    """Apply (u,r)<->(v,q), retaining the ordered labels U,V,R,Q."""
    perm={U:V,V:U,R:Q,Q:R}
    def image(s): return frozenset(perm.get(x,x) for x in s)
    # Old A_v becomes new A_u and old A_u becomes new A_v.
    return image(av),image(au)


def valid(au,av):
    au=frozenset(au);av=frozenset(av)
    if len(au)!=8 or len(av)!=8:return False
    if U in au or V in av or C&(au|av):return False
    if R not in au or Q not in av:return False
    su={U}|set(au);sv={V}|set(av)
    if len(su&sv)!=8:return False
    uv=V in au;vu=U in av
    # Exact root-pair status: one orientation, or no orientation with each root
    # in the other's exact second layer.  Membership in B is the coarse rooted
    # layer statement; actual two-walk support is supplied by the CNF.
    if uv and vu:return False
    if not vu and U not in (VERTICES-({V}|av|C)):return False
    if not uv and V not in (VERTICES-({U}|au|C)):return False
    return True


def states():
    """Enumerate every labelled A_u,A_v pair satisfying the coarse axioms."""
    # t=8 means |S_u union S_v|=10.  Choose that union first; then choose the
    # two size-nine rooted sets inside it.  This is exactly the labelled state
    # universe and avoids scanning irrelevant pairs of 8-subsets.
    ordinary=sorted(VERTICES-({U,V,R,Q}|C))
    for extra in itertools.combinations(ordinary,6):
        union=frozenset((U,V,R,Q,*extra))
        for su in itertools.combinations(sorted(union),9):
            su=frozenset(su)
            if U not in su or R not in su or C&su:continue
            au=su-{U}
            for sv in itertools.combinations(sorted(union),9):
                sv=frozenset(sv)
                if V not in sv or Q not in sv or C&sv:continue
                av=sv-{V}
                if valid(au,av):yield au,av


def key(state):return tuple(sorted(state[0])),tuple(sorted(state[1]))


def orbit(state):
    other=swap_state(*state)
    return frozenset((key(state),key(other)))


def relabel_key(state):
    """Complete orbit key under ordinary-low permutations and root exchange."""
    ordinary=VERTICES-({U,V,R,Q}|C)
    def structural(s):
        au,av=s
        profile=tuple(sum((x in au)==i and (x in av)==j for x in ordinary)
                      for i,j in ((False,False),(False,True),(True,False),(True,True)))
        return (V in au,U in av,Q in au,R in av,profile)
    return min(structural(state),structural(swap_state(*state)))


def main():
    labelled=list(states())
    keys=[key(s) for s in labelled]
    if len(keys)!=len(set(keys)):raise RuntimeError("duplicate labelled state")
    classes={k:0 for k in TYPES}
    orbits={k:set() for k in TYPES}
    signatures={k:set() for k in TYPES}
    for s in labelled:
        kind=classify(*s);classes[kind]+=1;orbits[kind].add(orbit(s))
        uv=V in s[0];vu=U in s[1]
        signatures[kind].add((uv,vu,Q in s[0],R in s[1]))
        swapped=swap_state(*s)
        if not valid(*swapped):raise RuntimeError("root exchange does not preserve validity")
        if classify(*swapped)!=kind:raise RuntimeError("root exchange changes overlap type")
        # C, T=V\\C, the common union, and W are transported by the exchange;
        # hence x=e(C,W), z=h(C,W), h=h(T) are invariant for every graph.
        su={U}|set(s[0]);sv={V}|set(s[1]);union=su|sv
        tu={U}|set(swapped[0]);tv={V}|set(swapped[1]);union2=tu|tv
        perm={U:V,V:U,R:Q,Q:R}
        image={perm.get(x,x) for x in union}
        if image!=union2:raise RuntimeError("root exchange changes transported union")
    if set().union(*orbits.values()) != {orbit(s) for s in labelled}:
        raise RuntimeError("root-exchange orbit partition is not exact")
    if any(orbits[a]&orbits[b] for i,a in enumerate(TYPES) for b in TYPES[i+1:]):
        raise RuntimeError("overlap-type orbit classes overlap")
    expected_signatures={
        "oriented-both":{(True,False,True,True),(False,True,True,True)},
        "oriented-one":{(True,False,False,True),(False,True,True,False)},
        "root-hole":{(False,False,True,True)},
    }
    if signatures!=expected_signatures:
        raise RuntimeError(f"unexpected signature partition {signatures!r}")
    # One independently written representative for each producer type.  The
    # equality below is exact set equality of complete orbit invariants, not a
    # comparison of counts.
    representatives={
        "oriented-both":(frozenset(range(1,9)),frozenset((1,2,4,5,6,7,8,9))),
        "oriented-one":(frozenset((1,3,4,5,6,7,8,9)),frozenset((1,2,4,5,6,7,8,9))),
        "root-hole":(frozenset((1,2,4,5,6,7,8,9)),frozenset((1,2,4,5,6,7,8,9))),
    }
    expected_full={relabel_key(s) for s in representatives.values()}
    actual_full={relabel_key(s) for s in labelled}
    if actual_full!=expected_full or len(expected_full)!=3:
        raise RuntimeError(f"full relabelling orbit mismatch {actual_full!r} != {expected_full!r}")
    for kind,state in representatives.items():
        if not valid(*state) or classify(*state)!=kind:
            raise RuntimeError(f"invalid independent representative for {kind}")
    # Explicitly exercise the opposite one-cross-high placement.  It must be
    # a different labelled state but the same full orbit under rooted exchange.
    one=representatives["oriented-one"];one_swap=swap_state(*one)
    if key(one)==key(one_swap) or relabel_key(one)!=relabel_key(one_swap):
        raise RuntimeError("one-cross-high exchange mutation not covered")
    print(f"PASS labelled_states={len(labelled)} root_exchange_orbits={sum(map(len,orbits.values()))} full_relabel_exchange_orbits={len(actual_full)}")
    print("PASS labelled_by_type="+repr(classes))
    print("PASS orbits_by_type="+repr({k:len(v) for k,v in orbits.items()}))
    print("PASS exact_signatures="+repr(signatures))
    print("PASS exact_full_orbit_keys="+repr(actual_full))
    print("PASS opposite_one_cross_high_placement=same_full_orbit")

if __name__=="__main__":main()
