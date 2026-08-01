#include <algorithm>
#include <array>
#include <cmath>
#include <complex>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <queue>
#include <stdexcept>
#include <string>
#include <vector>

using Complex = std::complex<double>;
using Coeff = std::array<int, 10>;

constexpr double PI = 3.141592653589793238462643383279502884;
constexpr std::array<std::array<int, 2>, 5> MODES{{
    {{1, 0}}, {{0, 1}}, {{1, 1}}, {{2, 1}}, {{1, 2}}
}};

struct Options {
    int proxy_keep = 2048;
    int candidate_keep = 8;
    int coarse_n = 64;
    int coarse_steps_per_unit = 512;
    int fine_n = 128;
    int fine_steps_per_unit = 1024;
    int fine_keep = 3;
    double final_time = 4.0;
    std::string output = "cycle212-screen.json";
};

struct RankedCoeff {
    double score;
    Coeff c;
    bool operator<(const RankedCoeff &other) const { return score > other.score; }
};

struct RunResult {
    double maximum = 1.0;
    double time = 0.0;
    bool finite = true;
    std::array<double, 64> checkpoints{};
};

struct FourierPsiMode {
    int kx;
    int ky;
    Complex coefficient;
};

static int gcd_coeff(const Coeff &c) {
    int g = 0;
    for (int x : c) g = std::gcd(g, std::abs(x));
    return g;
}

static Coeff transform(const Coeff &c, int tx, int ty, bool invert, bool swap) {
    Coeff out{};
    for (int j = 0; j < 5; ++j) {
        int source = j;
        if (swap) {
            static constexpr std::array<int, 5> SW{{1, 0, 2, 4, 3}};
            source = SW[j];
        }
        int phase = (tx * MODES[j][0] + ty * MODES[j][1]) & 3;
        int a = c[2 * source], b = invert ? -c[2 * source + 1] : c[2 * source + 1];
        int ar = 0, br = 0;
        if (phase == 0) { ar = a; br = b; }
        if (phase == 1) { ar = b; br = -a; }
        if (phase == 2) { ar = -a; br = -b; }
        if (phase == 3) { ar = -b; br = a; }
        int sign = swap ? -1 : 1; // Streamfunction is a pseudoscalar under reflection.
        out[2 * j] = sign * ar;
        out[2 * j + 1] = sign * br;
    }
    return out;
}

static Coeff canonical(Coeff c) {
    int g = gcd_coeff(c);
    if (g > 1) for (int &x : c) x /= g;
    Coeff best = c;
    for (int tx = 0; tx < 4; ++tx)
        for (int ty = 0; ty < 4; ++ty)
            for (int inv = 0; inv < 2; ++inv)
                for (int sw = 0; sw < 2; ++sw)
                    best = std::min(best, transform(c, tx, ty, inv, sw));
    return best;
}

static bool nonlinear(const Coeff &c) {
    // For 2D Fourier vorticity, a pair interacts iff it is nonparallel and
    // has unequal squared lengths. This test is exact for this five-mode set.
    for (int i = 0; i < 5; ++i) {
        if (c[2 * i] == 0 && c[2 * i + 1] == 0) continue;
        for (int j = i + 1; j < 5; ++j) {
            if (c[2 * j] == 0 && c[2 * j + 1] == 0) continue;
            int cross = MODES[i][0] * MODES[j][1] - MODES[i][1] * MODES[j][0];
            int ni = MODES[i][0] * MODES[i][0] + MODES[i][1] * MODES[i][1];
            int nj = MODES[j][0] * MODES[j][0] + MODES[j][1] * MODES[j][1];
            if (cross != 0 && ni != nj) return true;
        }
    }
    return false;
}

static double activity_proxy(const Coeff &c) {
    // Exact-support quadratic vorticity activity, evaluated in complex Fourier
    // arithmetic. It is only a cheap ranking proxy, not a PDE bound.
    struct Wave { int x, y; Complex psi; };
    std::vector<Wave> w;
    for (int j = 0; j < 5; ++j) {
        Complex plus(0.5 * c[2 * j], -0.5 * c[2 * j + 1]);
        w.push_back({MODES[j][0], MODES[j][1], plus});
        w.push_back({-MODES[j][0], -MODES[j][1], std::conj(plus)});
    }
    std::array<std::array<Complex, 9>, 9> out{};
    for (const auto &p : w) for (const auto &q : w) {
        int cross = p.x * q.y - p.y * q.x;
        int q2 = q.x * q.x + q.y * q.y;
        out[p.x + q.x + 4][p.y + q.y + 4] += double(cross * q2) * p.psi * q.psi;
    }
    double sum = 0.0, energy = 0.0;
    int occupied = 0;
    for (const auto &row : out) for (Complex z : row) sum += std::norm(z);
    for (int j = 0; j < 5; ++j) {
        if (c[2 * j] != 0 || c[2 * j + 1] != 0) ++occupied;
        int k2 = MODES[j][0] * MODES[j][0] + MODES[j][1] * MODES[j][1];
        energy += k2 * (c[2 * j] * c[2 * j] + c[2 * j + 1] * c[2 * j + 1]);
    }
    return std::sqrt(sum) * std::sqrt(double(occupied)) / std::max(energy, 1e-30);
}

class SpectralSolver {
  public:
    explicit SpectralSolver(int n) : n_(n), size_(n * n), a_(size_), b_(size_),
                                     c_(size_), d_(size_), physical_(size_) {
        if (n < 8 || (n & (n - 1))) throw std::runtime_error("N must be a power of two >= 8");
    }

    std::vector<Complex> initial(const Coeff &coef) const {
        std::vector<Complex> omega(size_, 0.0);
        for (int j = 0; j < 5; ++j) {
            int x = MODES[j][0], y = MODES[j][1], k2 = x * x + y * y;
            Complex psi(0.5 * coef[2 * j], -0.5 * coef[2 * j + 1]);
            omega[index(x, y)] = -double(k2 * size_) * psi;
            omega[index(-x, -y)] = -double(k2 * size_) * std::conj(psi);
        }
        return omega;
    }

    std::vector<Complex> initial(const std::vector<FourierPsiMode> &modes) const {
        std::vector<Complex> omega(size_, 0.0);
        for (const auto &mode : modes) {
            int k2 = mode.kx * mode.kx + mode.ky * mode.ky;
            if (!k2 || std::abs(mode.kx) >= n_ / 3 || std::abs(mode.ky) >= n_ / 3)
                throw std::runtime_error("initial mode outside dealiased range");
            omega[index(mode.kx, mode.ky)] += -double(k2 * size_) * mode.coefficient;
            omega[index(-mode.kx, -mode.ky)] +=
                -double(k2 * size_) * std::conj(mode.coefficient);
        }
        return omega;
    }

    double l3(const std::vector<Complex> &omega) {
        velocity(omega, a_, b_);
        fft2(a_, true); fft2(b_, true);
        double total = 0.0;
        for (int i = 0; i < size_; ++i) {
            double speed2 = a_[i].real() * a_[i].real() + b_[i].real() * b_[i].real();
            total += speed2 * std::sqrt(speed2);
        }
        return std::cbrt(total / size_);
    }

    double initial_log_derivative(const Coeff &coef, double mu) {
        auto omega = initial(coef);
        std::vector<Complex> rhs;
        nonlinear_term(omega, rhs);
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            rhs[i] -= mu * double(kx * kx + ky * ky) * omega[i];
        }
        velocity(omega, a_, b_); velocity(rhs, c_, d_);
        fft2(a_, true); fft2(b_, true); fft2(c_, true); fft2(d_, true);
        double norm3 = 0.0, deriv = 0.0;
        for (int i = 0; i < size_; ++i) {
            double ux = a_[i].real(), uy = b_[i].real();
            double speed = std::hypot(ux, uy);
            norm3 += speed * speed * speed;
            deriv += 3.0 * speed * (ux * c_[i].real() + uy * d_[i].real());
        }
        return deriv / std::max(3.0 * norm3, 1e-30);
    }

    RunResult run(const Coeff &coef, double mu, int steps_per_unit, double final_time) {
        return run(initial(coef), mu, steps_per_unit, final_time, 1.0);
    }

    RunResult run(std::vector<Complex> omega, double mu, int steps_per_unit,
                  double final_time, double time_direction) {
        std::vector<Complex> nl, old_nl;
        nonlinear_term(omega, nl);
        old_nl = nl;
        double dt = 1.0 / steps_per_unit;
        int steps = int(std::llround(final_time * steps_per_unit));
        int checkpoint_stride = steps_per_unit / 16;
        if (checkpoint_stride < 1 || steps_per_unit % 16)
            throw std::runtime_error("steps per unit must be divisible by 16");
        double initial_norm = l3(omega);
        RunResult result;
        int cp = 0;
        for (int step = 1; step <= steps; ++step) {
            for (int i = 0; i < size_; ++i) {
                auto [kx, ky] = wave(i);
                double e = std::exp(-mu * (kx * kx + ky * ky) * dt);
                double e2 = e * e;
                if (step == 1) omega[i] = e * (omega[i] + time_direction * dt * nl[i]);
                else omega[i] = e * omega[i] + time_direction * dt *
                    (1.5 * e * nl[i] - 0.5 * e2 * old_nl[i]);
            }
            old_nl.swap(nl);
            nonlinear_term(omega, nl);
            bool all_finite = true;
            for (Complex z : omega) all_finite = all_finite && std::isfinite(std::abs(z));
            if (!all_finite) {
                result.finite = false;
                break;
            }
            if (step % checkpoint_stride == 0 && cp < 64) {
                double ratio = l3(omega) / initial_norm;
                if (!std::isfinite(ratio)) {
                    result.finite = false;
                    break;
                }
                result.checkpoints[cp++] = ratio;
                if (ratio > result.maximum) {
                    result.maximum = ratio;
                    result.time = double(step) / steps_per_unit;
                }
            }
        }
        return result;
    }

  private:
    int n_, size_;
    std::vector<Complex> a_, b_, c_, d_, physical_;

    int index(int kx, int ky) const {
        int x = (kx % n_ + n_) % n_, y = (ky % n_ + n_) % n_;
        return x * n_ + y;
    }
    std::pair<int, int> wave(int i) const {
        int x = i / n_, y = i % n_;
        if (x > n_ / 2) x -= n_;
        if (y > n_ / 2) y -= n_;
        return {x, y};
    }
    void fft1(Complex *p, bool inverse) {
        for (int i = 1, j = 0; i < n_; ++i) {
            int bit = n_ >> 1;
            for (; j & bit; bit >>= 1) j ^= bit;
            j ^= bit;
            if (i < j) std::swap(p[i], p[j]);
        }
        for (int len = 2; len <= n_; len <<= 1) {
            double angle = (inverse ? 2.0 : -2.0) * PI / len;
            Complex root(std::cos(angle), std::sin(angle));
            for (int i = 0; i < n_; i += len) {
                Complex w = 1.0;
                for (int j = 0; j < len / 2; ++j) {
                    Complex u = p[i + j], v = p[i + j + len / 2] * w;
                    p[i + j] = u + v; p[i + j + len / 2] = u - v; w *= root;
                }
            }
        }
        if (inverse) for (int i = 0; i < n_; ++i) p[i] /= n_;
    }
    void fft2(std::vector<Complex> &v, bool inverse) {
        for (int x = 0; x < n_; ++x) fft1(v.data() + x * n_, inverse);
        std::vector<Complex> column(n_);
        for (int y = 0; y < n_; ++y) {
            for (int x = 0; x < n_; ++x) column[x] = v[x * n_ + y];
            fft1(column.data(), inverse);
            for (int x = 0; x < n_; ++x) v[x * n_ + y] = column[x];
        }
    }
    void velocity(const std::vector<Complex> &omega, std::vector<Complex> &u,
                  std::vector<Complex> &v) const {
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i); int k2 = kx * kx + ky * ky;
            Complex psi = k2 ? -omega[i] / double(k2) : 0.0;
            u[i] = Complex(0.0, -ky) * psi;
            v[i] = Complex(0.0, kx) * psi;
        }
    }
    void nonlinear_term(const std::vector<Complex> &omega, std::vector<Complex> &out) {
        velocity(omega, a_, b_);
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            c_[i] = Complex(0.0, kx) * omega[i];
            d_[i] = Complex(0.0, ky) * omega[i];
        }
        fft2(a_, true); fft2(b_, true); fft2(c_, true); fft2(d_, true);
        for (int i = 0; i < size_; ++i)
            physical_[i] = -(a_[i].real() * c_[i].real() + b_[i].real() * d_[i].real());
        fft2(physical_, false);
        out = physical_;
        int cutoff = n_ / 3;
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            if (std::abs(kx) > cutoff || std::abs(ky) > cutoff) out[i] = 0.0;
        }
        out[0] = 0.0;
    }
};

static std::string coeff_json(const Coeff &c) {
    std::string s = "[";
    for (int i = 0; i < 10; ++i) { if (i) s += ','; s += std::to_string(c[i]); }
    return s + "]";
}

static Options parse_options(int argc, char **argv) {
    Options o;
    for (int i = 1; i < argc; ++i) {
        std::string key = argv[i];
        if (i + 1 >= argc) throw std::runtime_error("missing value for " + key);
        std::string value = argv[++i];
        if (key == "--proxy-keep") o.proxy_keep = std::stoi(value);
        else if (key == "--candidate-keep") o.candidate_keep = std::stoi(value);
        else if (key == "--coarse-n") o.coarse_n = std::stoi(value);
        else if (key == "--coarse-steps") o.coarse_steps_per_unit = std::stoi(value);
        else if (key == "--fine-n") o.fine_n = std::stoi(value);
        else if (key == "--fine-steps") o.fine_steps_per_unit = std::stoi(value);
        else if (key == "--fine-keep") o.fine_keep = std::stoi(value);
        else if (key == "--final-time") o.final_time = std::stod(value);
        else if (key == "--output") o.output = value;
        else throw std::runtime_error("unknown option " + key);
    }
    return o;
}

int main(int argc, char **argv) try {
    Options options = parse_options(argc, argv);
    if (options.proxy_keep <= 0 || options.candidate_keep <= 0 || options.fine_keep < 0)
        throw std::runtime_error("retention counts must be positive (fine-keep may be zero)");
    if (!(options.final_time > 0.0) || options.final_time > 4.0 ||
        !std::isfinite(options.final_time))
        throw std::runtime_error("final time must be finite and in (0, 4]");
    std::priority_queue<RankedCoeff> proxy;
    uint64_t raw_nonzero = 0, primitive = 0, canonical_count = 0, active = 0;
    constexpr uint64_t TOTAL = 9765625; // 5^10
    for (uint64_t code = 0; code < TOTAL; ++code) {
        uint64_t q = code; Coeff c{};
        for (int i = 0; i < 10; ++i) { c[i] = int(q % 5) - 2; q /= 5; }
        int g = gcd_coeff(c);
        if (g == 0) continue;
        ++raw_nonzero;
        if (g != 1) continue;
        ++primitive;
        if (canonical(c) != c) continue;
        ++canonical_count;
        if (!nonlinear(c)) continue;
        ++active;
        double score = activity_proxy(c);
        proxy.push({score, c});
        if (int(proxy.size()) > options.proxy_keep) proxy.pop();
    }
    std::vector<RankedCoeff> proxies;
    while (!proxy.empty()) { proxies.push_back(proxy.top()); proxy.pop(); }
    std::reverse(proxies.begin(), proxies.end());
    std::cerr << "primitive=" << primitive << " canonical=" << canonical_count
              << " active=" << active << " proxy_retained=" << proxies.size() << "\n";

    constexpr std::array<double, 7> MUS{{1, .5, .25, .125, .0625, .03125, .015625}};
    SpectralSolver derivative_solver(32);
    std::priority_queue<RankedCoeff> derivative_rank;
    for (const auto &item : proxies) {
        double score = -1e100;
        for (double mu : MUS)
            score = std::max(score, derivative_solver.initial_log_derivative(item.c, mu));
        derivative_rank.push({score, item.c});
        if (int(derivative_rank.size()) > options.candidate_keep) derivative_rank.pop();
    }
    std::vector<RankedCoeff> candidates;
    while (!derivative_rank.empty()) { candidates.push_back(derivative_rank.top()); derivative_rank.pop(); }
    std::reverse(candidates.begin(), candidates.end());

    struct Record { Coeff c; double mu; RunResult run; };
    std::vector<Record> coarse;
    SpectralSolver coarse_solver(options.coarse_n);
    for (const auto &candidate : candidates) for (double mu : MUS) {
        RunResult run = coarse_solver.run(candidate.c, mu, options.coarse_steps_per_unit,
                                          options.final_time);
        std::cerr << "coarse c=" << coeff_json(candidate.c) << " mu=" << mu
                  << " max=" << run.maximum << " t=" << run.time
                  << " finite=" << run.finite << "\n";
        coarse.push_back({candidate.c, mu, run});
    }
    std::sort(coarse.begin(), coarse.end(), [](const Record &x, const Record &y) {
        if (x.run.finite != y.run.finite) return x.run.finite > y.run.finite;
        return x.run.maximum > y.run.maximum;
    });

    std::vector<Record> fine;
    SpectralSolver fine_solver(options.fine_n);
    for (int i = 0; i < std::min(options.fine_keep, int(coarse.size())); ++i) {
        auto &r = coarse[i];
        RunResult run = fine_solver.run(r.c, r.mu, options.fine_steps_per_unit, options.final_time);
        std::cerr << "fine c=" << coeff_json(r.c) << " mu=" << r.mu
                  << " max=" << run.maximum << " t=" << run.time
                  << " finite=" << run.finite << "\n";
        fine.push_back({r.c, r.mu, run});
    }

    std::ofstream f(options.output);
    f << std::setprecision(17);
    f << "{\n  \"status\": \"NUMERICS_SCREENING_ONLY\",\n"
      << "  \"rigorous_interval_certificate\": false,\n"
      << "  \"enumeration\": {\"raw_nonzero\": " << raw_nonzero
      << ", \"primitive\": " << primitive << ", \"canonical\": " << canonical_count
      << ", \"nonlinear\": " << active << "},\n"
      << "  \"method\": {\"proxy_retained\": " << proxies.size()
      << ", \"trajectory_candidates\": " << candidates.size()
      << ", \"coarse_n\": " << options.coarse_n
      << ", \"coarse_steps_per_unit\": " << options.coarse_steps_per_unit
      << ", \"fine_n\": " << options.fine_n
      << ", \"fine_steps_per_unit\": " << options.fine_steps_per_unit << "},\n";
    auto write_records = [&](const char *name, const std::vector<Record> &records) {
        f << "  \"" << name << "\": [\n";
        for (size_t i = 0; i < records.size(); ++i) {
            const auto &r = records[i];
            f << "    {\"coefficients\": " << coeff_json(r.c) << ", \"mu\": " << r.mu
              << ", \"max_ratio\": " << r.run.maximum << ", \"max_time\": " << r.run.time
              << ", \"finite\": " << (r.run.finite ? "true" : "false") << "}";
            f << (i + 1 == records.size() ? "\n" : ",\n");
        }
        f << "  ]";
    };
    write_records("coarse_ranked", coarse); f << ",\n"; write_records("fine_reruns", fine);
    auto observed_over_two = [](const std::vector<Record> &records) {
        return std::any_of(records.begin(), records.end(), [](const Record &record) {
            return record.run.finite && record.run.maximum > 2.0;
        });
    };
    f << ",\n  \"observed_over_two\": "
      << (observed_over_two(coarse) || observed_over_two(fine) ? "true" : "false")
      << "\n}\n";
    std::cout << options.output << "\n";
    return 0;
} catch (const std::exception &e) {
    std::cerr << "error: " << e.what() << "\n";
    return 2;
}
