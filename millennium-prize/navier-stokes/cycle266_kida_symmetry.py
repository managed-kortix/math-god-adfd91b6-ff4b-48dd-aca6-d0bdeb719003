#!/usr/bin/env python3
"""Exact Kida--Pelz symmetry reduction for the C266 Fourier cubes.

The action used here is

    (A, h) u:  u_hat[A k] = (-1)**((A k).h) A u_hat[k],

where ``A`` is a signed permutation matrix and ``h`` is a vector of half-period
translations.  Signed permutations preserve every cubic Galerkin set, and the
characters multiply under convolution.  Consequently the Euler convolution,
the Leray projector, and cubic truncation are equivariant.  A fixed-point
space of any subgroup returned by :func:`stabilizer` is therefore closed under
the exact truncated Euler vector field.

Frequency orbit representatives reduce the Kida--Pelz C266 states without
changing the frozen family or its manifest.  The reduced convolution computes
only representative outputs; input modes are reconstructed by their exact
orbit action.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product

from cycle266_3dde1 import ZV, cmul, euler_rhs, kida_pelz, profile_field


@dataclass(frozen=True, order=True)
class KidaSymmetry:
    """A signed coordinate permutation followed by half-period translation."""

    permutation: tuple[int, int, int]
    signs: tuple[int, int, int]
    half_shift: tuple[int, int, int]

    def wave(self, k):
        return tuple(self.signs[j] * k[self.permutation[j]] for j in range(3))

    def phase(self, output_wave):
        return -1 if sum(a * b for a, b in zip(output_wave, self.half_shift)) % 2 else 1


def candidate_symmetries():
    """Return the 384 cube-preserving signed-permutation/half-shift actions."""
    return tuple(
        KidaSymmetry(p, s, h)
        for p in permutations(range(3))
        for s in product((-1, 1), repeat=3)
        for h in product((0, 1), repeat=3)
    )


def transform_vector(symmetry, output_wave, vector):
    phase = symmetry.phase(output_wave)
    return tuple(
        (phase * symmetry.signs[j] * vector[symmetry.permutation[j]][0],
         phase * symmetry.signs[j] * vector[symmetry.permutation[j]][1])
        for j in range(3)
    )


def stabilizer(field):
    """Find the exact Kida symmetry subgroup fixing a Gaussian-rational field."""
    result = []
    for symmetry in candidate_symmetries():
        fixed = True
        for k, vector in field.items():
            output = symmetry.wave(k)
            if field.get(output, ZV) != transform_vector(symmetry, output, vector):
                fixed = False
                break
        if fixed:
            result.append(symmetry)
    return tuple(result)


def c266_profile_field(a, b, phase):
    """Construct one frozen profile without reading or changing the manifest."""
    base = kida_pelz()
    return profile_field(base, euler_rhs(base), a, Fraction(b), phase)


class KidaOrbitLayout:
    """Frequency orbits and a representative-only Euler convolution."""

    def __init__(self, cutoff, symmetries):
        self.cutoff = int(cutoff)
        self.symmetries = tuple(symmetries)
        if not self.symmetries:
            raise ValueError("a symmetry group must be nonempty")
        self.modes = tuple(
            k for k in product(range(-cutoff, cutoff + 1), repeat=3) if k != (0, 0, 0)
        )
        unassigned = set(self.modes)
        representatives = []
        lookup = {}
        while unassigned:
            representative = min(unassigned)
            orbit = {symmetry.wave(representative) for symmetry in self.symmetries}
            if not orbit <= unassigned | set(lookup):
                raise ValueError("actions do not partition the Fourier cube")
            index = len(representatives)
            representatives.append(representative)
            for output in sorted(orbit):
                choices = [s for s in self.symmetries if s.wave(representative) == output]
                lookup[output] = (index, choices[0])
                unassigned.discard(output)
        self.representatives = tuple(representatives)
        self.lookup = lookup
        self.width = 2 * cutoff + 1
        self.zero_index = cutoff

    @property
    def full_mode_count(self):
        return len(self.modes)

    @property
    def reduced_mode_count(self):
        return len(self.representatives)

    @property
    def reduction_factor(self):
        return self.full_mode_count / self.reduced_mode_count

    @staticmethod
    def _matrix(symmetry):
        import numpy as np

        matrix = np.zeros((3, 3))
        for row in range(3):
            matrix[row, symmetry.permutation[row]] = symmetry.signs[row]
        return matrix

    def expand(self, coefficients):
        """Expand representative coefficients to a centered full Fourier cube."""
        import numpy as np

        coefficients = np.asarray(coefficients, dtype=np.complex128)
        if coefficients.shape != (self.reduced_mode_count, 3):
            raise ValueError("reduced coefficients have the wrong shape")
        full = np.zeros((3, self.width, self.width, self.width), dtype=np.complex128)
        for output, (index, symmetry) in self.lookup.items():
            value = symmetry.phase(output) * self._matrix(symmetry).dot(coefficients[index])
            full[(slice(None),) + tuple(x + self.cutoff for x in output)] = value
        return full

    def compress(self, full, tolerance=2e-12):
        """Compress an invariant full cube, rejecting symmetry-breaking input."""
        import numpy as np

        full = np.asarray(full, dtype=np.complex128)
        expected = (3, self.width, self.width, self.width)
        if full.shape != expected:
            raise ValueError("full coefficients have the wrong shape")
        reduced = np.empty((self.reduced_mode_count, 3), dtype=np.complex128)
        for index, k in enumerate(self.representatives):
            reduced[index] = full[(slice(None),) + tuple(x + self.cutoff for x in k)]
        defect = np.linalg.norm(full - self.expand(reduced))
        scale = max(np.linalg.norm(full), 1.0)
        if defect > tolerance * scale:
            raise ValueError(f"field is outside the invariant subspace: defect={defect / scale:.3e}")
        return reduced

    def project(self, full):
        """Average a full cube over the finite symmetry group."""
        import numpy as np

        full = np.asarray(full, dtype=np.complex128)
        projected = np.zeros_like(full)
        for symmetry in self.symmetries:
            matrix = self._matrix(symmetry)
            for k in self.modes:
                output = symmetry.wave(k)
                source_value = full[(slice(None),) + tuple(x + self.cutoff for x in k)]
                projected[(slice(None),) + tuple(x + self.cutoff for x in output)] += (
                    symmetry.phase(output) * matrix.dot(source_value)
                )
        return projected / len(self.symmetries)

    def rhs(self, coefficients):
        """Evaluate the cubic-Galerkin Euler RHS only at orbit representatives."""
        import numpy as np

        full = self.expand(coefficients)
        result = np.zeros_like(np.asarray(coefficients, dtype=np.complex128))
        mode_array = np.asarray(self.modes, dtype=int)
        p_values = full[
            :, mode_array[:, 0] + self.cutoff,
            mode_array[:, 1] + self.cutoff,
            mode_array[:, 2] + self.cutoff,
        ].T
        for index, k in enumerate(self.representatives):
            remainder = np.asarray(k) - mode_array
            valid = np.all(np.abs(remainder) <= self.cutoff, axis=1)
            r = remainder[valid]
            vp = p_values[valid]
            vr = full[
                :, r[:, 0] + self.cutoff,
                r[:, 1] + self.cutoff,
                r[:, 2] + self.cutoff,
            ].T
            raw = -1j * np.sum(np.einsum("ij,ij->i", vp, r)[:, None] * vr, axis=0)
            wave = np.asarray(k, dtype=float)
            result[index] = raw - wave * np.dot(wave, raw) / np.dot(wave, wave)
        return result


def profile_reduction_table(cutoffs=(7, 10)):
    """Return exact orbit counts for the two phase-stabilizer classes in C266."""
    rows = []
    for phase in ((0, 0, 0), (0, 0, 1), (1, 1, 1)):
        group = stabilizer(c266_profile_field(-2, Fraction(1, 4), phase))
        row = {"phase": phase, "group_order": len(group), "levels": {}}
        for cutoff in cutoffs:
            layout = KidaOrbitLayout(cutoff, group)
            row["levels"][cutoff] = {
                "full_modes": layout.full_mode_count,
                "orbit_classes": layout.reduced_mode_count,
                "reduction_factor": layout.reduction_factor,
            }
        rows.append(row)
    return rows
