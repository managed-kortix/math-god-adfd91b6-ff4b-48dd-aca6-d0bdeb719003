#include <algorithm>
#include <array>
#include <cmath>
#include <complex>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

#include <gmpxx.h>

using BigInt = mpz_class;
using Complex = std::complex<double>;

constexpr double PI = 3.141592653589793238462643383279502884;

struct Rational {
    BigInt numerator = 0;
    BigInt denominator = 1;

    Rational() = default;
    Rational(long long value) : numerator(long(value)) {}
    Rational(BigInt n, BigInt d) : numerator(std::move(n)), denominator(std::move(d)) {
        reduce();
    }

    static BigInt gcd(BigInt a, BigInt b) {
        if (a < 0) a = -a;
        if (b < 0) b = -b;
        while (b != 0) {
            BigInt remainder = a % b;
            a = b;
            b = remainder;
        }
        return a;
    }

    void reduce() {
        if (denominator == 0) throw std::runtime_error("zero rational denominator");
        if (denominator < 0) {
            numerator = -numerator;
            denominator = -denominator;
        }
        BigInt divisor = gcd(numerator, denominator);
        if (divisor != 0) {
            numerator /= divisor;
            denominator /= divisor;
        }
    }

    std::string str() const {
        if (denominator == 1) return numerator.get_str();
        return numerator.get_str() + "/" + denominator.get_str();
    }

    double value() const { return numerator.get_d() / denominator.get_d(); }
};

static Rational operator+(const Rational &a, const Rational &b) {
    BigInt divisor = Rational::gcd(a.denominator, b.denominator);
    BigInt left_scale = b.denominator / divisor;
    BigInt right_scale = a.denominator / divisor;
    return {a.numerator * left_scale + b.numerator * right_scale,
            a.denominator * left_scale};
}
static Rational operator-(const Rational &a, const Rational &b) {
    BigInt divisor = Rational::gcd(a.denominator, b.denominator);
    BigInt left_scale = b.denominator / divisor;
    BigInt right_scale = a.denominator / divisor;
    return {a.numerator * left_scale - b.numerator * right_scale,
            a.denominator * left_scale};
}
static Rational operator*(const Rational &a, const Rational &b) {
    BigInt left_divisor = Rational::gcd(a.numerator, b.denominator);
    BigInt right_divisor = Rational::gcd(b.numerator, a.denominator);
    return {(a.numerator / left_divisor) * (b.numerator / right_divisor),
            (a.denominator / right_divisor) * (b.denominator / left_divisor)};
}
static Rational operator/(const Rational &a, const Rational &b) {
    if (b.numerator == 0) throw std::runtime_error("division by zero rational");
    BigInt left_divisor = Rational::gcd(a.numerator, b.numerator);
    BigInt right_divisor = Rational::gcd(b.denominator, a.denominator);
    return {(a.numerator / left_divisor) * (b.denominator / right_divisor),
            (a.denominator / right_divisor) * (b.numerator / left_divisor)};
}
static bool operator<(const Rational &a, const Rational &b) {
    return a.numerator * b.denominator < b.numerator * a.denominator;
}
static bool operator>(const Rational &a, const Rational &b) { return b < a; }
static bool operator==(const Rational &a, const Rational &b) {
    return a.numerator == b.numerator && a.denominator == b.denominator;
}

static Rational power(Rational base, int exponent) {
    Rational result(1);
    while (exponent > 0) {
        if (exponent & 1) result = result * base;
        base = base * base;
        exponent >>= 1;
    }
    return result;
}

struct Options {
    int n = 64;
    int steps_per_unit = 2048;
    std::string output = "cycle255-screen-N64.json";
    std::string checkpoint = "cycle255-screen-N64.checkpoint.tsv";
    std::uint64_t max_members = 149952;
    std::uint64_t stop_after_feasible = std::numeric_limits<std::uint64_t>::max();
    int shard_count = 1;
    int shard_index = 0;
};

struct FamilyMember {
    std::uint64_t index = 0;
    std::array<int, 5> a{};
    Rational sigma;
    Rational epsilon;
    Rational time;
};

struct Feasibility {
    Rational q0;
    Rational m;
    Rational alpha;
    Rational low_contribution;
    Rational tail_contribution;
    Rational initial_l2_square;
};

struct ScreenResult {
    FamilyMember member;
    Feasibility feasibility;
    double initial_l3 = 0.0;
    double final_l3 = 0.0;
    double forward_ratio = 0.0;
    double reverse_ratio = 0.0;
    double both_directions_ratio = 0.0;
    double energy_relative_drift = 0.0;
    double enstrophy_relative_drift = 0.0;
};

struct CheckpointData {
    std::uint64_t last_index = 0;
    std::uint64_t feasible_count = 0;
    std::vector<ScreenResult> promoted;
};

static const std::array<Rational, 4> Q0_VALUES = {
    Rational(33, 32), Rational(17, 16), Rational(9, 8), Rational(5, 4)};
static const std::array<Rational, 2> SIGMA_VALUES = {Rational(1, 16), Rational(1, 24)};
static const std::array<Rational, 3> EPSILON_VALUES = {
    Rational(1, 256), Rational(1, 512), Rational(1, 1024)};

static std::vector<std::array<int, 5>> profiles() {
    std::vector<std::array<int, 5>> result;
    for (int first = 0; first < 5; ++first) {
        std::array<int, 5> a{};
        a[first] = 1;
        std::uint64_t combinations = 1;
        for (int i = first + 1; i < 5; ++i) combinations *= 5;
        for (std::uint64_t code = 0; code < combinations; ++code) {
            std::uint64_t remaining = code;
            for (int i = 4; i > first; --i) {
                a[i] = int(remaining % 5) - 2;
                remaining /= 5;
            }
            result.push_back(a);
        }
    }
    if (result.size() != 781) throw std::runtime_error("internal profile count failure");
    return result;
}

template <class Callback>
static void enumerate_members(Callback callback) {
    std::uint64_t index = 0;
    for (const auto &a : profiles()) {
        for (const Rational &sigma : SIGMA_VALUES) {
            for (const Rational &epsilon : EPSILON_VALUES) {
                for (int m = 1; m <= 32; ++m) {
                    FamilyMember member{++index, a, sigma, epsilon, Rational(m, 16)};
                    if (!callback(member)) return;
                }
            }
        }
    }
    if (index != 149952) throw std::runtime_error("internal family count failure");
}

static Rational low_analytic_contribution(const std::array<int, 5> &a,
                                          const Rational &q) {
    static constexpr int terms[5][2][3] = {
        {{1, 0, 1}, {0, 1, 2}},
        {{1, 0, 1}, {0, 1, -2}},
        {{1, 1, 1}, {2, -1, 1}},
        {{1, -2, 1}, {2, 1, 1}},
        {{3, 1, 1}, {1, -3, -1}},
    };
    Rational total;
    for (int packet = 0; packet < 5; ++packet) {
        for (int term = 0; term < 2; ++term) {
            int kx = terms[packet][term][0];
            int ky = terms[packet][term][1];
            int coefficient = terms[packet][term][2];
            int magnitude = std::abs(a[packet] * coefficient) * (kx * kx + ky * ky);
            total = total + Rational(magnitude, 64) * power(q, std::abs(kx) + std::abs(ky));
        }
    }
    return total;
}

static Rational tail_analytic_contribution(const Rational &sigma,
                                           const Rational &epsilon,
                                           const Rational &q) {
    Rational r = q * sigma;
    Rational all = power((Rational(1) + r) / (Rational(1) - r), 2);
    Rational box;
    for (int kx = -4; kx <= 4; ++kx)
        for (int ky = -4; ky <= 4; ++ky)
            box = box + power(r, std::abs(kx) + std::abs(ky));
    return epsilon * (all - box);
}

static Rational initial_l2_square(const FamilyMember &member) {
    static constexpr int terms[5][2][3] = {
        {{1, 0, 1}, {0, 1, 2}}, {{1, 0, 1}, {0, 1, -2}},
        {{1, 1, 1}, {2, -1, 1}}, {{1, -2, 1}, {2, 1, 1}},
        {{3, 1, 1}, {1, -3, -1}},
    };
    Rational result;
    for (int packet = 0; packet < 5; ++packet) {
        for (int term = 0; term < 2; ++term) {
            int kx = terms[packet][term][0], ky = terms[packet][term][1];
            int coefficient = member.a[packet] * terms[packet][term][2];
            result = result + Rational(coefficient * coefficient * (kx * kx + ky * ky), 8192);
        }
    }
    return result;
}

static bool feasible(const FamilyMember &member, Feasibility &result) {
    Rational l2_square = initial_l2_square(member);
    if (!(Rational(0) < l2_square)) return false;
    for (const Rational &q0 : Q0_VALUES) {
        Rational low = low_analytic_contribution(member.a, q0);
        Rational tail = tail_analytic_contribution(member.sigma, member.epsilon, q0);
        Rational analytic_norm = low + tail;
        for (int m_index = 1; m_index <= 256; ++m_index) {
            Rational m(m_index, 64);
            if (analytic_norm > m) continue;
            for (int alpha_index = 1; alpha_index <= 256; ++alpha_index) {
                Rational alpha(alpha_index, 64);
                if (alpha < m) continue;
                if (q0 * (Rational(1) - alpha * member.time) > Rational(1)) {
                    result = {q0, m, alpha, low, tail, l2_square};
                    return true;
                }
            }
        }
    }
    return false;
}

class EulerScreen {
  public:
    explicit EulerScreen(int n)
        : n_(n), size_(n * n), cutoff_(n / 3), a_(size_), b_(size_), c_(size_),
          d_(size_), physical_(size_), column_(n), k1_(size_), k2_(size_),
          k3_(size_), k4_(size_), work_(size_) {
        if (n < 8 || (n & (n - 1)))
            throw std::runtime_error("N must be a power of two at least 8");
    }

    std::vector<Complex> initial_state(const FamilyMember &member) const {
        static constexpr int terms[5][2][3] = {
            {{1, 0, 1}, {0, 1, 2}}, {{1, 0, 1}, {0, 1, -2}},
            {{1, 1, 1}, {2, -1, 1}}, {{1, -2, 1}, {2, 1, 1}},
            {{3, 1, 1}, {1, -3, -1}},
        };
        std::vector<Complex> omega(size_, 0.0);
        for (int packet = 0; packet < 5; ++packet) {
            for (int term = 0; term < 2; ++term) {
                int kx = terms[packet][term][0], ky = terms[packet][term][1];
                int coefficient = member.a[packet] * terms[packet][term][2];
                double laplacian_amplitude = -double(kx * kx + ky * ky) * coefficient / 64.0;
                Complex fourier;
                if (packet == 1 || packet == 3)
                    fourier = Complex(0.0, -0.5 * laplacian_amplitude);
                else
                    fourier = 0.5 * laplacian_amplitude;
                omega[index(kx, ky)] += fourier * double(size_);
                omega[index(-kx, -ky)] += std::conj(fourier) * double(size_);
            }
        }
        double sigma = member.sigma.value(), epsilon = member.epsilon.value();
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            if ((kx || ky) && std::max(std::abs(kx), std::abs(ky)) > 4 &&
                std::abs(kx) <= cutoff_ && std::abs(ky) <= cutoff_) {
                omega[i] += epsilon * std::pow(sigma, std::abs(kx) + std::abs(ky)) * double(size_);
            }
        }
        return omega;
    }

    ScreenResult run(const FamilyMember &member, const Feasibility &feasibility,
                     int steps_per_unit) {
        if (steps_per_unit < 16 || steps_per_unit % 16 != 0)
            throw std::runtime_error("steps per unit must be divisible by 16");
        std::vector<Complex> initial = initial_state(member);
        Rational rational_steps = member.time * Rational(steps_per_unit);
        BigInt integer_steps = rational_steps.numerator / rational_steps.denominator;
        int steps = int(integer_steps.get_si());
        if (!(member.time * Rational(steps_per_unit) == Rational(steps)))
            throw std::runtime_error("T/dt must be integral");
        const double dt = 1.0 / steps_per_unit;
        double initial_l3 = l3(initial);
        auto [initial_energy, initial_enstrophy] = invariants(initial);
        if (!(initial_l3 > 0.0)) throw std::runtime_error("nonpositive initial L3");

        auto integrate = [&](double signed_dt) {
            std::vector<Complex> omega = initial;
            for (int step = 0; step < steps; ++step) {
                nonlinear_term(omega, k1_);
                for (int i = 0; i < size_; ++i)
                    work_[i] = omega[i] + (0.5 * signed_dt) * k1_[i];
                nonlinear_term(work_, k2_);
                for (int i = 0; i < size_; ++i)
                    work_[i] = omega[i] + (0.5 * signed_dt) * k2_[i];
                nonlinear_term(work_, k3_);
                for (int i = 0; i < size_; ++i) work_[i] = omega[i] + signed_dt * k3_[i];
                nonlinear_term(work_, k4_);
                for (int i = 0; i < size_; ++i)
                    omega[i] += (signed_dt / 6.0) *
                        (k1_[i] + 2.0 * k2_[i] + 2.0 * k3_[i] + k4_[i]);
            }
            return omega;
        };
        std::vector<Complex> forward = integrate(dt);
        std::vector<Complex> reverse = integrate(-dt);
        double final_l3 = l3(forward);
        double reverse_l3 = l3(reverse);
        auto [forward_energy, forward_enstrophy] = invariants(forward);
        auto [reverse_energy, reverse_enstrophy] = invariants(reverse);
        ScreenResult result;
        result.member = member;
        result.feasibility = feasibility;
        result.initial_l3 = initial_l3;
        result.final_l3 = final_l3;
        result.forward_ratio = final_l3 / initial_l3;
        result.reverse_ratio = reverse_l3 / initial_l3;
        result.both_directions_ratio = std::max(result.forward_ratio, result.reverse_ratio);
        result.energy_relative_drift = std::max(
            std::abs(forward_energy / initial_energy - 1.0),
            std::abs(reverse_energy / initial_energy - 1.0));
        result.enstrophy_relative_drift = std::max(
            std::abs(forward_enstrophy / initial_enstrophy - 1.0),
            std::abs(reverse_enstrophy / initial_enstrophy - 1.0));
        if (!std::isfinite(result.both_directions_ratio))
            throw std::runtime_error("non-finite orbit diagnostic");
        return result;
    }

  private:
    int n_, size_, cutoff_;
    std::vector<Complex> a_, b_, c_, d_, physical_, column_;
    std::vector<Complex> k1_, k2_, k3_, k4_, work_;

    int index(int kx, int ky) const {
        return ((kx % n_ + n_) % n_) * n_ + ((ky % n_ + n_) % n_);
    }
    std::pair<int, int> wave(int i) const {
        int x = i / n_, y = i % n_;
        if (x > n_ / 2) x -= n_;
        if (y > n_ / 2) y -= n_;
        return {x, y};
    }
    void fft1(Complex *values, bool inverse) const {
        for (int i = 1, j = 0; i < n_; ++i) {
            int bit = n_ >> 1;
            for (; j & bit; bit >>= 1) j ^= bit;
            j ^= bit;
            if (i < j) std::swap(values[i], values[j]);
        }
        for (int length = 2; length <= n_; length <<= 1) {
            double angle = (inverse ? 2.0 : -2.0) * PI / length;
            Complex root(std::cos(angle), std::sin(angle));
            for (int i = 0; i < n_; i += length) {
                Complex factor = 1.0;
                for (int j = 0; j < length / 2; ++j) {
                    Complex u = values[i + j], v = values[i + j + length / 2] * factor;
                    values[i + j] = u + v;
                    values[i + j + length / 2] = u - v;
                    factor *= root;
                }
            }
        }
        if (inverse)
            for (int i = 0; i < n_; ++i) values[i] /= n_;
    }
    void fft2(std::vector<Complex> &values, bool inverse) {
        for (int x = 0; x < n_; ++x) fft1(values.data() + x * n_, inverse);
        for (int y = 0; y < n_; ++y) {
            for (int x = 0; x < n_; ++x) column_[x] = values[x * n_ + y];
            fft1(column_.data(), inverse);
            for (int x = 0; x < n_; ++x) values[x * n_ + y] = column_[x];
        }
    }
    void velocity(const std::vector<Complex> &omega,
                  std::vector<Complex> &u, std::vector<Complex> &v) const {
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            int k2 = kx * kx + ky * ky;
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
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            if (std::abs(kx) > cutoff_ || std::abs(ky) > cutoff_) out[i] = 0.0;
        }
        out[0] = 0.0;
    }
    double l3(const std::vector<Complex> &omega) {
        velocity(omega, a_, b_);
        fft2(a_, true); fft2(b_, true);
        double cube = 0.0;
        for (int i = 0; i < size_; ++i) {
            double speed = std::hypot(a_[i].real(), b_[i].real());
            cube += speed * speed * speed;
        }
        return std::cbrt(cube / size_);
    }
    std::pair<double, double> invariants(const std::vector<Complex> &omega) const {
        double energy = 0.0, enstrophy = 0.0;
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            int k2 = kx * kx + ky * ky;
            if (!k2) continue;
            energy += std::norm(omega[i]) / k2;
            enstrophy += std::norm(omega[i]);
        }
        return {energy, enstrophy};
    }
};

static std::string encode_a(const std::array<int, 5> &a, char separator) {
    std::ostringstream stream;
    for (int i = 0; i < 5; ++i) {
        if (i) stream << separator;
        stream << a[i];
    }
    return stream.str();
}

static void append_checkpoint(const std::string &path, const ScreenResult &result) {
    bool header = !std::filesystem::exists(path) || std::filesystem::file_size(path) == 0;
    std::ofstream output(path, std::ios::app);
    if (!output) throw std::runtime_error("cannot append checkpoint");
    if (header)
        output << "cycle255-floating-screen-checkpoint-v1\n"
               << "index\ta\tsigma\tepsilon\tT\tq0\tM\talpha\tinitial_l3\tfinal_l3"
                  "\tforward_ratio\treverse_ratio\tboth_directions_ratio\tenergy_drift"
                  "\tenstrophy_drift\n";
    output << std::setprecision(17) << result.member.index << '\t'
           << encode_a(result.member.a, ',') << '\t' << result.member.sigma.str() << '\t'
           << result.member.epsilon.str() << '\t' << result.member.time.str() << '\t'
           << result.feasibility.q0.str() << '\t' << result.feasibility.m.str() << '\t'
           << result.feasibility.alpha.str() << '\t' << result.initial_l3 << '\t'
           << result.final_l3 << '\t' << result.forward_ratio << '\t' << result.reverse_ratio
           << '\t' << result.both_directions_ratio << '\t' << result.energy_relative_drift
           << '\t' << result.enstrophy_relative_drift << '\n';
    output.flush();
    if (!output) throw std::runtime_error("checkpoint write failure");
}

static CheckpointData read_checkpoint(const std::string &path) {
    CheckpointData data;
    if (!std::filesystem::exists(path)) return data;
    std::ifstream input(path);
    std::string line;
    if (!std::getline(input, line) || line != "cycle255-floating-screen-checkpoint-v1")
        throw std::runtime_error("unknown checkpoint format");
    if (!std::getline(input, line) || line.rfind("index\t", 0) != 0)
        throw std::runtime_error("invalid checkpoint header");
    while (std::getline(input, line)) {
        if (line.empty()) continue;
        std::vector<std::string> fields;
        std::stringstream stream(line);
        std::string field;
        while (std::getline(stream, field, '\t')) fields.push_back(field);
        if (fields.size() != 15) throw std::runtime_error("invalid checkpoint row");
        std::uint64_t index = std::stoull(fields[0]);
        if (index <= data.last_index) throw std::runtime_error("unordered checkpoint rows");
        data.last_index = index;
        ++data.feasible_count;
        double ratio = std::stod(fields[12]);
        if (ratio >= 1.5) {
            ScreenResult result;
            result.member.index = index;
            std::stringstream a_stream(fields[1]);
            for (int i = 0; i < 5; ++i) {
                std::getline(a_stream, field, ',');
                result.member.a[i] = std::stoi(field);
            }
            result.initial_l3 = std::stod(fields[8]);
            result.final_l3 = std::stod(fields[9]);
            result.forward_ratio = std::stod(fields[10]);
            result.reverse_ratio = std::stod(fields[11]);
            result.both_directions_ratio = ratio;
            result.energy_relative_drift = std::stod(fields[13]);
            result.enstrophy_relative_drift = std::stod(fields[14]);
            data.promoted.push_back(result);
        }
    }
    return data;
}

static void write_json(const Options &options, std::uint64_t completed_index,
                       std::uint64_t feasible_count, std::vector<ScreenResult> promoted,
                       bool complete) {
    std::sort(promoted.begin(), promoted.end(), [](const auto &left, const auto &right) {
        if (left.both_directions_ratio != right.both_directions_ratio)
            return left.both_directions_ratio > right.both_directions_ratio;
        return left.member.index < right.member.index;
    });
    if (promoted.size() > 64) promoted.resize(64);
    std::string temporary = options.output + ".tmp";
    std::ofstream output(temporary);
    if (!output) throw std::runtime_error("cannot write JSON output");
    output << std::setprecision(17)
           << "{\n  \"format\": \"cycle255-floating-candidate-screen-v1\",\n"
           << "  \"status\": \"FLOATING_GALERKIN_SCREEN_ONLY\",\n"
           << "  \"pde_certificate\": false,\n"
           << "  \"complete\": " << (complete ? "true" : "false") << ",\n"
           << "  \"method\": \"square_two_thirds_pseudospectral_euler_rk4\",\n"
           << "  \"enumeration\": \"one_based_profile_sigma_epsilon_time\",\n"
           << "  \"n\": " << options.n << ",\n  \"cutoff\": " << options.n / 3
           << ",\n  \"dt\": \"1/" << options.steps_per_unit << "\",\n"
           << "  \"completed_enumeration_index\": " << completed_index << ",\n"
           << "  \"shard_count\": " << options.shard_count << ",\n"
           << "  \"shard_index\": " << options.shard_index << ",\n"
           << "  \"feasible_members_screened\": " << feasible_count << ",\n"
           << "  \"promotion_threshold\": 1.5,\n"
           << "  \"promoted_count_before_cap\": " << promoted.size() << ",\n"
           << "  \"promoted\": [";
    for (std::size_t i = 0; i < promoted.size(); ++i) {
        const auto &result = promoted[i];
        output << (i ? ",\n" : "\n") << "    {\"index\": " << result.member.index
               << ", \"a\": [" << encode_a(result.member.a, ',') << "]"
               << ", \"initial_l3\": " << result.initial_l3
               << ", \"final_l3\": " << result.final_l3
               << ", \"forward_ratio\": " << result.forward_ratio
               << ", \"reverse_ratio\": " << result.reverse_ratio
               << ", \"both_directions_ratio\": " << result.both_directions_ratio
               << ", \"energy_relative_drift\": " << result.energy_relative_drift
               << ", \"enstrophy_relative_drift\": " << result.enstrophy_relative_drift
               << "}";
    }
    output << (promoted.empty() ? "" : "\n") << "  ]\n}\n";
    output.close();
    if (!output) throw std::runtime_error("JSON output write failure");
    std::filesystem::rename(temporary, options.output);
}

static Options parse_options(int argc, char **argv) {
    Options options;
    for (int i = 1; i < argc; ++i) {
        if (i + 1 >= argc) throw std::runtime_error("missing option value");
        std::string key = argv[i], value = argv[++i];
        if (key == "--n") options.n = std::stoi(value);
        else if (key == "--steps-per-unit") options.steps_per_unit = std::stoi(value);
        else if (key == "--output") options.output = value;
        else if (key == "--checkpoint") options.checkpoint = value;
        else if (key == "--max-members") options.max_members = std::stoull(value);
        else if (key == "--stop-after-feasible") options.stop_after_feasible = std::stoull(value);
        else if (key == "--shard-count") options.shard_count = std::stoi(value);
        else if (key == "--shard-index") options.shard_index = std::stoi(value);
        else throw std::runtime_error("unknown option " + key);
    }
    if (options.shard_count < 1 || options.shard_index < 0 ||
        options.shard_index >= options.shard_count)
        throw std::runtime_error("invalid shard selection");
    return options;
}

int main(int argc, char **argv) try {
    Options options = parse_options(argc, argv);
    CheckpointData checkpoint = read_checkpoint(options.checkpoint);
    EulerScreen solver(options.n);
    std::uint64_t completed_index = checkpoint.last_index;
    std::uint64_t feasible_count = checkpoint.feasible_count;
    std::uint64_t screened_this_run = 0;
    bool reached_limit = false;
    enumerate_members([&](const FamilyMember &member) {
        if (member.index <= checkpoint.last_index) return true;
        if (member.index > options.max_members || screened_this_run >= options.stop_after_feasible) {
            reached_limit = true;
            return false;
        }
        if ((member.index - 1) % options.shard_count != std::uint64_t(options.shard_index)) {
            completed_index = member.index;
            return true;
        }
        Feasibility feasibility_result;
        if (feasible(member, feasibility_result)) {
            ScreenResult result = solver.run(member, feasibility_result, options.steps_per_unit);
            append_checkpoint(options.checkpoint, result);
            ++feasible_count;
            ++screened_this_run;
            if (result.both_directions_ratio >= 1.5) checkpoint.promoted.push_back(result);
        }
        completed_index = member.index;
        return true;
    });
    bool complete = !reached_limit && completed_index == 149952;
    write_json(options, completed_index, feasible_count, checkpoint.promoted, complete);
    std::cout << "FLOATING_GALERKIN_SCREEN_ONLY completed_index=" << completed_index
              << " feasible_screened=" << feasible_count
              << " complete=" << (complete ? "true" : "false") << "\n";
    return 0;
} catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << "\n";
    return 2;
}
