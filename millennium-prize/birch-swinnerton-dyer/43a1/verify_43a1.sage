# Run with: sage verify_43a1.sage
E = EllipticCurve(QQ, [0, 1, 1, 0, 0])
P = E(0, 0)
print("MODEL", E.ainvs())
print("CONDUCTOR", E.conductor())
print("DISCRIMINANT", E.discriminant())
print("TAMAGAWA_NUMBERS", E.tamagawa_numbers())
print("TORSION", E.torsion_subgroup())
print("RANK", E.rank(proof=True))
print("GENS", E.gens(proof=True))
print("P_SATURATION", E.gens(proof=True)[0] == P or E.gens(proof=True)[0] == -P)
print("TWO_SELMER_RANK_BOUND", E.rank_bounds())
rho = E.galois_representation()
print("NON_SURJECTIVE_PRIMES", rho.non_surjective())
print("IMAGE_TYPES_TO_47", [(p, rho.image_type(p)) for p in prime_range(2, 48)])
print("ANALYTIC_RANK_NUMERICAL", E.analytic_rank())
assert E.conductor() == 43 and E.discriminant() == -43
assert E.rank(proof=True) == 1 and E.torsion_order() == 1
assert rho.non_surjective() == []
