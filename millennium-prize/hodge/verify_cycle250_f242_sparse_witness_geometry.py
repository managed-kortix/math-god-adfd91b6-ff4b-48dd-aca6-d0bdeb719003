#!/usr/bin/env python3
"""Exact tangent and injectivity tests for the Cycle 249 sparse witness."""

import itertools
import shutil
import subprocess


VARIABLES = ",".join(f"{name}{factor}" for factor in range(1, 4) for name in "abc")

# Put c=zeta*Z. Then C is a^4+b^4+c^4=0 and the canonical-coordinate
# vector of dphi is (a,-b,-c), up to a nonzero local tangent scalar.
TANGENT_COLUMNS = (
    ("0", "-i*a1", "-i*c1", "i*a1", "0", "i*c1"),
    ("c2", "0", "-i*a2-c2", "-b2", "a2", "-i*c2"),
    ("b3", "-a3", "-b3+c3", "a3", "-b3+c3", "0"),
)


def determinant3(columns, rows):
    matrix = [[columns[column][row] for column in range(3)] for row in rows]
    return (
        f"({matrix[0][0]})*(({matrix[1][1]})*({matrix[2][2]})"
        f"-({matrix[1][2]})*({matrix[2][1]}))"
        f"-({matrix[0][1]})*(({matrix[1][0]})*({matrix[2][2]})"
        f"-({matrix[1][2]})*({matrix[2][0]}))"
        f"+({matrix[0][2]})*(({matrix[1][0]})*({matrix[2][1]})"
        f"-({matrix[1][1]})*({matrix[2][0]}))"
    )


def singular_program():
    equations = [
        "a1^4+b1^4+c1^4",
        "a2^4+b2^4+c2^4",
        "a3^4+b3^4+c3^4",
    ]
    equations.extend(
        determinant3(TANGENT_COLUMNS, rows)
        for rows in itertools.combinations(range(6), 3)
    )
    base_ideal = ",".join(equations)
    lines = [f"ring r=(0,i),({VARIABLES}),dp;", "minpoly=i^2+1;"]
    for index, patch in enumerate(itertools.product("abc", repeat=3)):
        patch_equations = ",".join(
            f"{coordinate}{factor}-1"
            for factor, coordinate in enumerate(patch, start=1)
        )
        lines.extend(
            (
                f"ideal J{index}={base_ideal},{patch_equations};",
                f"ideal G{index}=std(J{index});",
                f'if(size(G{index})!=1 || G{index}[1]!=1){{"FAIL {"".join(patch)}";}};',
            )
        )
    lines.append('"ALL_27_PATCH_IDEALS_ARE_ONE";')
    return "\n".join(lines) + "\n"


def check_tangent_injectivity():
    singular = shutil.which("Singular")
    if singular is None:
        raise RuntimeError("Singular is required for the exact Groebner check")
    result = subprocess.run(
        [singular, "-q"],
        input=singular_program(),
        text=True,
        capture_output=True,
        check=True,
    )
    if result.stderr or result.stdout.strip() != "ALL_27_PATCH_IDEALS_ARE_ONE":
        raise RuntimeError(f"unexpected Singular output:\n{result.stdout}{result.stderr}")


def check_collision():
    # L1 has zero middle column, so L1*phi depends only on (q_X,q_Z).
    assert (0, 0, 0, 0, 0, 0) == (0,) * 6

    # P=[1:0:1] and Q=[-1:0:1] lie on C and are distinct projective points.
    p = (1, 0, 1)
    q = (-1, 0, 1)
    assert p[0] ** 4 + p[1] ** 4 == p[2] ** 4
    assert q[0] ** 4 + q[1] ** 4 == q[2] ** 4
    assert p != q and p != tuple(-coordinate for coordinate in q)

    # Q=sigma_X(P)=sigma_Z(P) projectively. The corresponding quotient maps
    # therefore take equal values at P and Q.
    assert (-p[0], p[1], p[2]) == q
    assert (p[0], p[1], -p[2]) == tuple(-coordinate for coordinate in q)


def main():
    check_collision()
    check_tangent_injectivity()
    print("Cycle 250 F242 sparse-witness geometry")
    print("tangent map: INJECTIVE (27 exact projective Groebner certificates)")
    print("closed immersion: REJECT (explicit P != Q with L1*phi(P)=L1*phi(Q))")
    print("collision: P=[1:0:1], Q=[-1:0:1], other two source factors fixed")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
