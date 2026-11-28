#!/usr/bin/env python3
"""Read-only floating diagnostic for the Cycle-50 source split.

This is NOT an interval certificate.  It uses IEEE-754 binary64 and a
cotangent Vasyunin evaluator.  It writes nothing and makes no asymptotic claim.
"""
from __future__ import annotations
import hashlib
import math
import sys
import time
from pathlib import Path

EULER = 0.577215664901532860606512090082402431
C0 = math.log(2.0 * math.pi) - EULER
C = 6.0 / 5.0
TAU = C - 1.0
SCALES = (32, 64, 128)


def dot(x, y):
    return math.fsum(a * b for a, b in zip(x, y))


def norm(x):
    return math.sqrt(max(0.0, dot(x, x)))


def sub(x, y):
    return [a - b for a, b in zip(x, y)]


def axpy(a, x, y):
    return [a * u + v for u, v in zip(x, y)]


def sieve(limit):
    mu = [0] * (limit + 1)
    composite = [False] * (limit + 1)
    primes = []
    mu[1] = 1
    for n in range(2, limit + 1):
        if not composite[n]:
            primes.append(n)
            mu[n] = -1
        for p in primes:
            if n * p > limit:
                break
            composite[n * p] = True
            if n % p == 0:
                mu[n * p] = 0
                break
            mu[n * p] = -mu[n]
    von_mangoldt = [0.0] * (limit + 1)
    for p in primes:
        x = p
        logp = math.log(p)
        while x <= limit:
            von_mangoldt[x] = logp
            x *= p
    return mu, von_mangoldt


class RestrictedGram:
    """Restricted <rho_a,rho_b> on [1,infinity), including -1/(ab)."""
    def __init__(self):
        self.v_cache = {}
        self.cot_cache = {}
        self.g_cache = {}

    def vasyunin(self, p, q):
        if q == 1:
            return 0.0
        p %= q
        sign = 1
        if p > q // 2:
            p = q - p
            sign = -1
        key = (p, q)
        if key not in self.v_cache:
            row = self.cot_cache.get(q)
            if row is None:
                row = [0.0] + [
                    math.cos(math.pi * k / q) /
                    math.sin(math.pi * k / q) / q
                    for k in range(1, q)
                ]
                self.cot_cache[q] = row
            self.v_cache[key] = math.fsum(
                ((k * p) % q) * row[k] for k in range(1, q)
            )
        return sign * self.v_cache[key]

    def entry(self, a, b):
        key = (min(a, b), max(a, b))
        if key in self.g_cache:
            return self.g_cache[key]
        aa, bb = key
        d = math.gcd(aa, bb)
        p, q = aa // d, bb // d
        lcm = aa * bb // d
        full = (
            (q - p) * math.log(p / q) + (p + q) * C0
            - math.pi * (self.vasyunin(p, q) + self.vasyunin(q, p))
        ) / (2.0 * lcm)
        answer = full - 1.0 / (aa * bb)
        self.g_cache[key] = answer
        return answer

    @staticmethod
    def chi_cross(a):
        return (math.log(a) + 1.0 - EULER) / a


def orthonormal_pair(x, y):
    nx = norm(x)
    if not nx:
        raise ArithmeticError("zero first vector")
    q1 = [v / nx for v in x]
    coeff = dot(q1, y)
    yp = axpy(-coeff, q1, y)
    nyp = norm(yp)
    if not nyp:
        raise ArithmeticError("rank-one pair")
    q2 = [v / nyp for v in yp]
    return q1, q2, nyp / norm(y)


def principal_data(src_basis, yv_basis, complete):
    qs = orthonormal_pair(*src_basis)
    qy = orthonormal_pair(*yv_basis)
    svec = qs[:2]
    yvec = qy[:2]
    m00, m01 = dot(svec[0], yvec[0]), dot(svec[0], yvec[1])
    m10, m11 = dot(svec[1], yvec[0]), dot(svec[1], yvec[1])
    aa = m00 * m00 + m10 * m10
    bb = m00 * m01 + m10 * m11
    dd = m01 * m01 + m11 * m11
    disc = math.sqrt(max(0.0, (aa - dd) ** 2 + 4.0 * bb * bb))
    ev_hi = min(1.0, max(0.0, (aa + dd + disc) / 2.0))
    ev_lo = min(1.0, max(0.0, (aa + dd - disc) / 2.0))
    sig_hi, sig_lo = math.sqrt(ev_hi), math.sqrt(ev_lo)
    theta_min = math.acos(min(1.0, max(-1.0, sig_hi)))
    theta_max = math.acos(min(1.0, max(-1.0, sig_lo)))
    proj_src = [0.0] * len(complete)
    proj_yv = [0.0] * len(complete)
    for qv in svec:
        proj_src = axpy(dot(qv, complete), qv, proj_src)
    for qv in yvec:
        proj_yv = axpy(dot(qv, complete), qv, proj_yv)
    return {
        "theta_min": theta_min,
        "theta_max": theta_max,
        "proj_op_diff": math.sin(theta_max),
        "proj_frob_diff": math.sqrt(2.0 * (
            math.sin(theta_min) ** 2 + math.sin(theta_max) ** 2
        )),
        "projected_C_diff_rel": norm(sub(proj_src, proj_yv)) / norm(complete),
        "src_qr_res": qs[2],
        "yv_qr_res": qy[2],
        "Q_yv": dot(proj_yv, proj_yv),
    }


def run_scale(a, mu, lam, logs, psi, csum, mertens_recip, ell, psi_weight):
    start = time.time()
    M = 2 * a - 1
    rows = [q for q in range(a, 3 * a // 2 + 1) if mu[q] != 0]
    squarefree = [d for d in range(1, M + 1) if mu[d] != 0]
    gram = RestrictedGram()

    B_closed = []
    B_alt = []
    O_direct = []
    # O below is the exact residual comparator B-U; O_direct is the genuinely
    # independent old-source contraction from the one-source kernel.
    O = []
    U = []
    Y = []
    V = []
    H = []
    Complete = []
    U_reorder_residual = []

    for q in rows:
        lq = logs[q]
        spatial_u = 0.0
        spatial_d = 0.0
        source_index = 0
        gq = gram.chi_cross(q)
        b_closed_q = b_alt_q = y_q = v_q = h_q = complete_q = 0.0
        u_temporal_q = 0.0
        o_direct_q = 0.0
        current_packet = [0.0] * (M + 2)

        for n in range(q, M + 1):
            while source_index < len(squarefree) and squarefree[source_index] <= n:
                d = squarefree[source_index]
                gqd = gram.entry(q, d)
                spatial_u += mu[d] * gqd
                spatial_d += mu[d] * logs[d] * gqd
                source_index += 1

            ln = logs[n]
            w = 1.0 - ln / logs[n + 1]
            A = C - w
            eta = TAU / A
            alpha = w * A * (lq / ln - eta)
            aterm = n / q - math.log((n + 1) / q)
            jterm = math.log((n + 1) / q) - (
                psi_weight[n] - psi_weight[q - 1]
            )
            E = csum[n + 1] - n
            sterm = ell[n] / ln - eta * mertens_recip[n]
            Rterm = sterm + 1.0 / ln
            ppacket = csum[n + 1] / q - (
                psi_weight[n] - psi_weight[q - 1]
            )

            cell_closed = aterm * Rterm + (E / q + jterm) / ln
            cell_alt = aterm * sterm + ppacket / ln
            Kfull = spatial_d / ln - eta * (gq + spatial_u)

            b_closed_q += alpha * cell_closed
            b_alt_q += alpha * cell_alt
            y_q += alpha * E / (q * ln)
            v_q += alpha * (aterm * Rterm + jterm / ln)
            h_q += alpha * (Kfull - cell_alt)
            complete_q += alpha * Kfull

            # Independent direct old-source contraction from Kscr.  For m<a,
            # Kscr(m)=sum_{r<=n/m} Lambda(r) P(q,mr)+eta*ln*aterm/m.
            # The inner convolution is evaluated from exact-in-index restricted
            # Gram prefixes P(q,d) = integral_[1,n+1] rho_q rho_d dt/t^2.
            # Here n<2q, so P has a closed two-cell formula.
            for m in range(1, a):
                if mu[m] == 0:
                    continue
                kscr = eta * ln * aterm / m
                for r in range(1, n // m + 1):
                    if lam[r] != 0.0:
                        d = m * r
                        # P_{q,n}(d), direct finite integral for q,d<=n.
                        # General cell-by-cell formula is used to avoid relying
                        # on the Cycle-48 arithmetic collapse.
                        pint = 0.0
                        for k in range(1, n + 1):
                            fq, fd = k // q, k // d
                            Aqd = 1.0 / (q * d)
                            Bqd = -(fq / d + fd / q)
                            Cqd = fq * fd
                            pint += Aqd + Bqd * math.log((k+1)/k) + Cqd * (1.0/k - 1.0/(k+1))
                        kscr += lam[r] * pint
                o_direct_q -= mu[m] * alpha * kscr / ln

            current_packet[n] = alpha * eta * aterm
            u_temporal_q -= current_packet[n] * (
                mertens_recip[n] - mertens_recip[a - 1]
            )

        # Independent summation order for the current one-source block.
        suffix = [0.0] * (M + 2)
        for n in range(M, q - 1, -1):
            suffix[n] = suffix[n + 1] + current_packet[n]
        u_source_q = -math.fsum(
            mu[m] * suffix[max(q, m)] / m for m in range(a, M + 1)
        )
        o_q = b_alt_q - u_source_q

        B_closed.append(b_closed_q)
        B_alt.append(b_alt_q)
        O.append(o_q)
        O_direct.append(o_direct_q)
        U.append(u_source_q)
        Y.append(y_q)
        V.append(v_q)
        H.append(h_q)
        Complete.append(complete_q)
        U_reorder_residual.append(u_temporal_q - u_source_q)

    oo, ou, uu = dot(O, O), dot(O, U), dot(U, U)
    norm_O, norm_U = math.sqrt(oo), math.sqrt(uu)
    norm_ratio_minmax = min(norm_O, norm_U) / max(norm_O, norm_U)
    cos_OU = ou / (norm_O * norm_U)
    tr = oo + uu
    det = oo * uu - ou * ou
    disc = math.sqrt(max(0.0, (oo - uu) ** 2 + 4.0 * ou * ou))
    lam_max = (tr + disc) / 2.0
    lam_min = (tr - disc) / 2.0
    zO, zU = dot(O, Complete), dot(U, Complete)
    Qsrc = (uu * zO * zO - 2.0 * ou * zO * zU + oo * zU * zU) / det

    b_decomp_res = [b - (o + u) for b, o, u in zip(B_closed, O, U)]
    old_direct_res = sub(O_direct, O)
    c_decomp_res = [c - (b + h) for c, b, h in zip(
        Complete, B_closed, H
    )]
    yv_res = [b - (y + v) for b, y, v in zip(B_closed, Y, V)]
    scale_B = max(norm(B_closed), 1e-300)
    scale_C = max(norm(Complete), 1e-300)
    scale_U = max(norm(U), 1e-300)

    pdata = principal_data((O, U), (Y, V), Complete)
    D = dot(Complete, Complete)
    L = math.log(a)
    # Direct line projection, for orientation only.
    BC = dot(B_closed, Complete)
    Qcp = BC * BC / dot(B_closed, B_closed)
    sin_OU = math.sqrt(max(0.0, det / (oo * uu)))

    return {
        "a": a, "rows": len(rows), "D": D, "Qsrc": Qsrc,
        "Qcp": Qcp, "L3Qsrc": L ** 3 * Qsrc,
        "delta": det / (tr * tr), "gram_cond": lam_max / lam_min,
        "column_cond": math.sqrt(lam_max / lam_min),
        "lambda_min_over_tr": lam_min / tr, "sin_OU": sin_OU,
        "cos_OU": cos_OU, "norm_ratio_minmax": norm_ratio_minmax,
        "src_qr_res": pdata["src_qr_res"],
        "det_factor_res": abs(det - oo * uu * sin_OU * sin_OU) / (tr * tr),
        "B_res_abs": max(map(abs, b_decomp_res)),
        "B_res_rel": norm(b_decomp_res) / scale_B,
        "C_res_abs": max(map(abs, c_decomp_res)),
        "C_res_rel": norm(c_decomp_res) / scale_C,
        "YV_res_rel": norm(yv_res) / scale_B,
        "U_reorder_abs": max(map(abs, U_reorder_residual)),
        "U_reorder_rel": norm(U_reorder_residual) / scale_U,
        "O_direct_abs": max(map(abs, old_direct_res)),
        "O_direct_rel": norm(old_direct_res) / max(norm(O), 1e-300),
        **pdata,
        "elapsed": time.time() - start,
    }


def main():
    maximum = 2 * max(SCALES) + 2
    mu, lam = sieve(maximum)
    logs = [0.0] + [math.log(n) for n in range(1, maximum + 1)]
    psi = [0.0] * (maximum + 1)
    csum = [0.0] * (maximum + 1)
    mertens_recip = [0.0] * (maximum + 1)
    ell = [0.0] * (maximum + 1)
    psi_weight = [0.0] * (maximum + 1)
    for n in range(1, maximum + 1):
        psi[n] = psi[n - 1] + lam[n]
        mertens_recip[n] = mertens_recip[n - 1] + mu[n] / n
        ell[n] = ell[n - 1] + mu[n] * logs[n] / n
        psi_weight[n] = psi_weight[n - 1] + psi[n] / (n * (n + 1))
        if n >= 2:
            csum[n] = csum[n - 1] + psi[n - 1] * (logs[n] - logs[n - 1])

    print("scope=binary64 finite diagnostic only; no interval/asymptotic/RH inference")
    print("theta=2/5 C=6/5 I0=[1,3/2] M=2a-1")
    for a in SCALES:
        r = run_scale(
            a, mu, lam, logs, psi, csum, mertens_recip, ell, psi_weight
        )
        fields = [
            f"a={a}", f"rows={r['rows']}", f"D={r['D']:.17e}",
            f"Qsrc={r['Qsrc']:.17e}", f"Qsrc_over_D={r['Qsrc']/r['D']:.17e}",
            f"Qcp_over_D={r['Qcp']/r['D']:.17e}", f"L3Qsrc={r['L3Qsrc']:.17e}",
            f"delta={r['delta']:.17e}", f"gram_cond={r['gram_cond']:.17e}",
            f"column_cond={r['column_cond']:.17e}",
            f"lambda_min_over_tr={r['lambda_min_over_tr']:.17e}",
            f"norm_ratio_minmax={r['norm_ratio_minmax']:.17e}",
            f"cos_OU={r['cos_OU']:.17e}", f"sin_OU={r['sin_OU']:.17e}",
            f"src_qr_res={r['src_qr_res']:.17e}",
            f"det_factor_res={r['det_factor_res']:.3e}",
            f"B_res_abs={r['B_res_abs']:.3e}", f"B_res_rel={r['B_res_rel']:.3e}",
            f"C_res_abs={r['C_res_abs']:.3e}", f"C_res_rel={r['C_res_rel']:.3e}",
            f"YV_res_rel={r['YV_res_rel']:.3e}",
            f"U_reorder_abs={r['U_reorder_abs']:.3e}",
            f"U_reorder_rel={r['U_reorder_rel']:.3e}",
            f"O_direct_abs={r['O_direct_abs']:.3e}",
            f"O_direct_rel={r['O_direct_rel']:.3e}",
            f"theta_min_deg={math.degrees(r['theta_min']):.17e}",
            f"theta_max_deg={math.degrees(r['theta_max']):.17e}",
            f"proj_op_diff={r['proj_op_diff']:.17e}",
            f"proj_frob_diff={r['proj_frob_diff']:.17e}",
            f"projected_C_diff_rel={r['projected_C_diff_rel']:.17e}",
            f"Qyv_over_D={r['Q_yv']/r['D']:.17e}",
            f"yv_qr_res={r['yv_qr_res']:.17e}",
        ]
        print(" ".join(fields), flush=True)


if __name__ == "__main__":
    main()
