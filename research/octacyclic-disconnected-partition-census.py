from fractions import Fraction


def partitions(t, d, minimum=(0, 0)):
    result = []
    for a in range(t + 1):
        for b in range(d + 1):
            part = (a, b)
            if a + b == 0 or part < minimum:
                continue
            if part == (t, d):
                result.append((part,))
                continue
            for rest in partitions(t - a, d - b, part):
                result.append((part,) + rest)
    return result


def triangle_bound(t):
    bounds = {
        1: (Fraction(0), True),
        2: (Fraction(1), True),
        3: (Fraction(2), True),
        4: (Fraction(3), True),
        5: (Fraction(2), True),
        6: (Fraction(1), True),
        7: (Fraction(0), True),
    }
    return bounds[t]


def t7q_bound(part):
    t, q = part
    rank = t + q
    if q == 0:
        return triangle_bound(t)
    if part == (0, 1):
        return Fraction(-1), False
    if part == (1, 1):
        return Fraction(0), True
    if rank in (2, 3):
        return Fraction(0), False
    return Fraction(0), True


def t6pp_bound(part):
    t, p = part
    rank = t + p
    if p == 0:
        return triangle_bound(t)
    if part == (0, 1):
        return Fraction(-1, 4), False
    if part == (1, 1):
        return Fraction(3, 4), True
    if part == (0, 2):
        return Fraction(0), True
    if part == (1, 2):
        return Fraction(3, 2), True
    if rank in (2, 3):
        return Fraction(0), False
    return Fraction(0), True


def name(partition, distinguished):
    letter = "Q" if distinguished == 1 else "P"
    return "|".join("T" * t + letter * d for t, d in partition)


def audit(t, d, bound):
    all_rows = partitions(t, d)
    proper = [row for row in all_rows if len(row) > 1]
    residual = []
    for row in proper:
        packet_bounds = [bound(part) for part in row]
        lower = sum((value for value, _ in packet_bounds), Fraction(0))
        strict = any(is_strict for _, is_strict in packet_bounds)
        if not (lower > 0 or (lower == 0 and strict)):
            residual.append(name(row, d))
    return all_rows, proper, residual


t7q_all, t7q_proper, t7q_residual = audit(7, 1, t7q_bound)
t6pp_all, t6pp_proper, t6pp_residual = audit(6, 2, t6pp_bound)

assert len(t7q_all) == 45
assert len(t7q_proper) == 44
assert t7q_residual == ["Q|T|T|T|T|T|T|T", "Q|TTTTTTT"]

assert len(t6pp_all) == 77
assert len(t6pp_proper) == 76
assert t6pp_residual == [
    "P|P|T|T|T|T|T|T",
    "P|T|T|T|T|TTP",
    "P|T|T|T|TTTP",
    "P|T|T|TTTTP",
    "P|T|TTTTTP",
    "P|TTTTTTP",
]

print("T^7Q colored partitions including one cluster:", len(t7q_all))
print("T^7Q proper colored partitions:", len(t7q_proper))
print("T^7Q direct packet rows:", len(t7q_proper) - len(t7q_residual))
print("T^7Q structural rows:", len(t7q_residual))
for row in t7q_residual:
    print(" ", row)

print("T^6PP colored partitions including one cluster:", len(t6pp_all))
print("T^6PP proper colored partitions:", len(t6pp_proper))
print("T^6PP direct packet rows:", len(t6pp_proper) - len(t6pp_residual))
print("T^6PP structural rows:", len(t6pp_residual))
for row in t6pp_residual:
    print(" ", row)
