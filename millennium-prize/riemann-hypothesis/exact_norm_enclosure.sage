from sage.all import *

def enclosure(N, Q, bits=256):
    """Certified ball enclosure from Notebook Lemma 1."""
    assert N >= 3 and Q >= N
    R = RealBallField(bits)
    logN = R(N).log()
    c = {a: R(moebius(a)) * (R(N).log() - R(a).log()) / logN
         for a in range(1, N + 1)}
    A = sum(c[a] / R(a) for a in range(1, N + 1))
    points = {QQ(1)/Q, QQ(1)}
    for a in range(1, N + 1):
        for k in range(1, Q//a + 1):
            points.add(QQ(1)/(a*k))
    points = sorted(x for x in points if QQ(1)/Q <= x <= 1)
    S = A*A
    for left, right in zip(points[:-1], points[1:]):
        mid = (left + right)/2
        B = R(1) - sum(c[a] * floor(QQ(1)/(a*mid))
                       for a in range(1, N + 1))
        l, r = R(left), R(right)
        S += A*A*(1/l - 1/r) + 2*A*B*(r/l).log() + B*B*(r-l)
    M = R(1) + sum(abs(c[a]) for a in range(1, N + 1))
    return S, S + M*M/R(Q)

if __name__ == '__main__':
    for N, Q in [(3, 1000), (5, 5000), (10, 20000)]:
        lo, hi = enclosure(N, Q)
        print(N, Q, lo, hi, "normalized", RIF(log(N))*RIF(hi))
