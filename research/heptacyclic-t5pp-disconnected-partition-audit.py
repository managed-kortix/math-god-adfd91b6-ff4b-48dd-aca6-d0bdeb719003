from fractions import Fraction


def partitions(t, p, minimum=(0, 1)):
    result = []
    for a in range(t + 1):
        for b in range(p + 1):
            part = (a, b)
            if a + b == 0 or part < minimum:
                continue
            if part == (t, p):
                result.append((part,))
                continue
            for rest in partitions(t - a, p - b, part):
                result.append((part,) + rest)
    return result


def packet_bound(part):
    t, p = part
    rank = t + p
    if part == (1, 0):
        return Fraction(0), True, "T"
    if part == (0, 1):
        return Fraction(-1, 2), False, "P"
    if part == (2, 0):
        return Fraction(1), True, "TT"
    if part == (1, 1):
        return Fraction(1, 2), True, "TP"
    if part == (0, 2):
        return Fraction(0), True, "PP"
    if part == (3, 0):
        return Fraction(2), True, "TTT"
    if part == (1, 2):
        return Fraction(3, 2), True, "TPP"
    if rank in (2, 3):
        return Fraction(0), False, "rank <= 3"
    if part == (4, 0):
        return Fraction(3), True, "TTTT"
    if part == (5, 0):
        return Fraction(2), True, "TTTTT"
    if part == (6, 0):
        return Fraction(1), True, "TTTTTT"
    if rank >= 4:
        return Fraction(0), True, "rank >= 4"
    raise AssertionError(part)


def name(partition):
    return "|".join("T" * t + "P" * p for t, p in partition)


all_partitions = partitions(5, 2)
proper = [partition for partition in all_partitions if len(partition) > 1]
assert len(all_partitions) == 47
assert len(proper) == 46

non_direct = []
for partition in proper:
    bounds = [packet_bound(part) for part in partition]
    lower = sum((bound for bound, _, _ in bounds), Fraction(0))
    strict = any(is_strict for _, is_strict, _ in bounds)
    if not (lower > 0 or (lower == 0 and strict)):
        non_direct.append(name(partition))

expected = [
    "P|P|T|T|T|T|T",
    "P|T|T|T|TTP",
    "P|T|T|TTTP",
    "P|T|TTTTP",
    "P|TTTTTP",
]
assert non_direct == expected

print("colored partitions including one cluster:", len(all_partitions))
print("proper colored partitions:", len(proper))
print("direct packet rows:", len(proper) - len(non_direct))
print("topology/entry rows:", len(non_direct))
for row in non_direct:
    print(" ", row)
