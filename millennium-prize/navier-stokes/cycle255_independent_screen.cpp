#include <algorithm>
#include <array>
#include <cmath>
#include <complex>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

using Complex = std::complex<double>;

constexpr double PI = 3.141592653589793238462643383279502884;

struct Options {
    int n = 64;
    int steps_per_unit = 2048;
    int shortlist = 24;
    int report = 12;
    std::string output = "cycle255-independent-N64.json";
};

struct Member {
    int profile_index = 0;
    std::array<int, 5> a{};
    int sigma_denominator = 16;
    int epsilon_denominator = 256;
    double score = 0.0;
    int max_feasible_m = 0;
};

struct Result {
    Member member;
    int direction = 1;
    int best_m = 0;
    double best_ratio = 1.0;
    double endpoint_ratio = 1.0;
    double energy_drift = 0.0;
    double enstrophy_drift = 0.0;
};

struct Control {
    std::string name;
    double initial_l3 = 0.0;
    double expected_l3 = 0.0;
    double normalization_relative_error = 0.0;
    double rhs_relative_l2 = 0.0;
    double ratio = 0.0;
    double energy_drift = 0.0;
    double enstrophy_drift = 0.0;
};

class EulerSolver {
  public:
    explicit EulerSolver(int n)
        : n_(n), size_(n * n), cutoff_(n / 3), u_(size_), v_(size_),
          wx_(size_), wy_(size_), product_(size_) {
        if (n < 8 || (n & (n - 1)))
            throw std::runtime_error("N must be a power of two at least 8");
    }

    std::vector<Complex> initial(const Member &member) const {
        std::vector<Complex> omega(size_, 0.0);
        const double scale = double(size_) / 64.0;
        add_trig(omega, member.a[0], 1, 0, false, 1.0, scale);
        add_trig(omega, member.a[0], 0, 1, false, 2.0, scale);
        add_trig(omega, member.a[1], 1, 0, true, 1.0, scale);
        add_trig(omega, member.a[1], 0, 1, true, -2.0, scale);
        add_trig(omega, member.a[2], 1, 1, false, 1.0, scale);
        add_trig(omega, member.a[2], 2, -1, false, 1.0, scale);
        add_trig(omega, member.a[3], 1, -2, true, 1.0, scale);
        add_trig(omega, member.a[3], 2, 1, true, 1.0, scale);
        add_trig(omega, member.a[4], 3, 1, false, 1.0, scale);
        add_trig(omega, member.a[4], 1, -3, false, -1.0, scale);

        const double sigma = 1.0 / member.sigma_denominator;
        const double epsilon = 1.0 / member.epsilon_denominator;
        for (int kx = -cutoff_; kx <= cutoff_; ++kx) {
            for (int ky = -cutoff_; ky <= cutoff_; ++ky) {
                if ((kx == 0 && ky == 0) ||
                    (std::abs(kx) <= 4 && std::abs(ky) <= 4)) continue;
                omega[index(kx, ky)] += double(size_) * epsilon *
                    std::pow(sigma, std::abs(kx) + std::abs(ky));
            }
        }
        return omega;
    }

    std::vector<Complex> shear() const {
        std::vector<Complex> omega(size_, 0.0);
        omega[index(0, 1)] = -0.5 * size_;
        omega[index(0, -1)] = -0.5 * size_;
        return omega;
    }

    std::vector<Complex> equal_shell() const {
        std::vector<Complex> omega(size_, 0.0);
        omega[index(1, 0)] = omega[index(-1, 0)] = -0.5 * size_;
        omega[index(0, 1)] = omega[index(0, -1)] = -1.0 * size_;
        return omega;
    }

    double l3(const std::vector<Complex> &omega) {
        velocity(omega, u_, v_);
        fft2(u_, true);
        fft2(v_, true);
        double cube = 0.0;
        for (int i = 0; i < size_; ++i) {
            double speed = std::hypot(u_[i].real(), v_[i].real());
            cube += speed * speed * speed;
        }
        return std::cbrt(cube / size_);
    }

    double log_l3_derivative(const std::vector<Complex> &omega) {
        std::vector<Complex> f;
        rhs(omega, f);
        velocity(omega, u_, v_);
        velocity(f, wx_, wy_);
        fft2(u_, true); fft2(v_, true);
        fft2(wx_, true); fft2(wy_, true);
        double cube = 0.0, derivative = 0.0;
        for (int i = 0; i < size_; ++i) {
            double ux = u_[i].real(), uy = v_[i].real();
            double speed = std::hypot(ux, uy);
            cube += speed * speed * speed;
            derivative += speed * (ux * wx_[i].real() + uy * wy_[i].real());
        }
        return derivative / std::max(cube, 1e-300);
    }

    double rhs_relative_l2(const std::vector<Complex> &omega) {
        std::vector<Complex> f;
        rhs(omega, f);
        double numerator = 0.0, denominator = 0.0;
        for (int i = 0; i < size_; ++i) {
            numerator += std::norm(f[i]);
            denominator += std::norm(omega[i]);
        }
        return std::sqrt(numerator / std::max(denominator, 1e-300));
    }

    Result run(const Member &member, int direction, int steps_per_unit) {
        auto omega = initial(member);
        const double initial_l3 = l3(omega);
        const auto initial_invariants = invariants(omega);
        const int total_steps = member.max_feasible_m * steps_per_unit / 16;
        const int checkpoint_stride = steps_per_unit / 16;
        const double dt = double(direction) / steps_per_unit;
        Result result;
        result.member = member;
        result.direction = direction;
        std::vector<Complex> k1, k2, k3, k4, stage(size_);
        for (int step = 1; step <= total_steps; ++step) {
            rhs(omega, k1);
            for (int i = 0; i < size_; ++i) stage[i] = omega[i] + 0.5 * dt * k1[i];
            rhs(stage, k2);
            for (int i = 0; i < size_; ++i) stage[i] = omega[i] + 0.5 * dt * k2[i];
            rhs(stage, k3);
            for (int i = 0; i < size_; ++i) stage[i] = omega[i] + dt * k3[i];
            rhs(stage, k4);
            for (int i = 0; i < size_; ++i)
                omega[i] += (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]);
            if (step % checkpoint_stride == 0) {
                const int m = step / checkpoint_stride;
                const double ratio = l3(omega) / initial_l3;
                result.endpoint_ratio = ratio;
                if (ratio > result.best_ratio) {
                    result.best_ratio = ratio;
                    result.best_m = m;
                }
            }
        }
        const auto final_invariants = invariants(omega);
        result.energy_drift = std::abs(final_invariants.first / initial_invariants.first - 1.0);
        result.enstrophy_drift = std::abs(final_invariants.second / initial_invariants.second - 1.0);
        return result;
    }

    Control run_control(const std::string &name, std::vector<Complex> omega,
                        double expected_l3, int steps_per_unit) {
        Control control;
        control.name = name;
        control.initial_l3 = l3(omega);
        control.expected_l3 = expected_l3;
        if (expected_l3 > 0.0)
            control.normalization_relative_error =
                std::abs(control.initial_l3 / expected_l3 - 1.0);
        control.rhs_relative_l2 = rhs_relative_l2(omega);
        const auto before = invariants(omega);
        const double dt = 1.0 / steps_per_unit;
        std::vector<Complex> k1, k2, k3, k4, stage(size_);
        for (int step = 0; step < steps_per_unit / 16; ++step) {
            rhs(omega, k1);
            for (int i = 0; i < size_; ++i) stage[i] = omega[i] + 0.5 * dt * k1[i];
            rhs(stage, k2);
            for (int i = 0; i < size_; ++i) stage[i] = omega[i] + 0.5 * dt * k2[i];
            rhs(stage, k3);
            for (int i = 0; i < size_; ++i) stage[i] = omega[i] + dt * k3[i];
            rhs(stage, k4);
            for (int i = 0; i < size_; ++i)
                omega[i] += (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]);
        }
        control.ratio = l3(omega) / control.initial_l3;
        const auto after = invariants(omega);
        control.energy_drift = std::abs(after.first / before.first - 1.0);
        control.enstrophy_drift = std::abs(after.second / before.second - 1.0);
        return control;
    }

  private:
    int n_, size_, cutoff_;
    std::vector<Complex> u_, v_, wx_, wy_, product_;

    int index(int kx, int ky) const {
        int x = (kx % n_ + n_) % n_;
        int y = (ky % n_ + n_) % n_;
        return x * n_ + y;
    }

    std::pair<int, int> wave(int i) const {
        int x = i / n_, y = i % n_;
        if (x > n_ / 2) x -= n_;
        if (y > n_ / 2) y -= n_;
        return {x, y};
    }

    void add_trig(std::vector<Complex> &omega, int profile_coefficient,
                  int kx, int ky, bool sine, double packet_coefficient,
                  double scale) const {
        if (!profile_coefficient) return;
        const int k2 = kx * kx + ky * ky;
        const double amplitude = profile_coefficient * packet_coefficient;
        Complex plus = sine ? Complex(0.0, -0.5 * amplitude)
                            : Complex(0.5 * amplitude, 0.0);
        omega[index(kx, ky)] += -k2 * scale * plus;
        omega[index(-kx, -ky)] += -k2 * scale * std::conj(plus);
    }

    void fft1(Complex *values, bool inverse) const {
        for (int i = 1, j = 0; i < n_; ++i) {
            int bit = n_ >> 1;
            for (; j & bit; bit >>= 1) j ^= bit;
            j ^= bit;
            if (i < j) std::swap(values[i], values[j]);
        }
        for (int length = 2; length <= n_; length <<= 1) {
            const double angle = (inverse ? 2.0 : -2.0) * PI / length;
            const Complex root(std::cos(angle), std::sin(angle));
            for (int start = 0; start < n_; start += length) {
                Complex phase = 1.0;
                for (int j = 0; j < length / 2; ++j) {
                    Complex even = values[start + j];
                    Complex odd = values[start + j + length / 2] * phase;
                    values[start + j] = even + odd;
                    values[start + j + length / 2] = even - odd;
                    phase *= root;
                }
            }
        }
        if (inverse)
            for (int i = 0; i < n_; ++i) values[i] /= n_;
    }

    void fft2(std::vector<Complex> &values, bool inverse) const {
        for (int x = 0; x < n_; ++x) fft1(values.data() + x * n_, inverse);
        std::vector<Complex> column(n_);
        for (int y = 0; y < n_; ++y) {
            for (int x = 0; x < n_; ++x) column[x] = values[x * n_ + y];
            fft1(column.data(), inverse);
            for (int x = 0; x < n_; ++x) values[x * n_ + y] = column[x];
        }
    }

    void velocity(const std::vector<Complex> &omega,
                  std::vector<Complex> &u, std::vector<Complex> &v) const {
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            const int k2 = kx * kx + ky * ky;
            if (!k2) { u[i] = 0.0; v[i] = 0.0; continue; }
            u[i] = Complex(0.0, ky) * omega[i] / double(k2);
            v[i] = Complex(0.0, -kx) * omega[i] / double(k2);
        }
    }

    void rhs(const std::vector<Complex> &omega, std::vector<Complex> &out) {
        velocity(omega, u_, v_);
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            wx_[i] = Complex(0.0, kx) * omega[i];
            wy_[i] = Complex(0.0, ky) * omega[i];
        }
        fft2(u_, true); fft2(v_, true);
        fft2(wx_, true); fft2(wy_, true);
        for (int i = 0; i < size_; ++i)
            product_[i] = -(u_[i].real() * wx_[i].real() +
                            v_[i].real() * wy_[i].real());
        fft2(product_, false);
        out = product_;
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            if (std::abs(kx) > cutoff_ || std::abs(ky) > cutoff_) out[i] = 0.0;
        }
        out[0] = 0.0;
    }

    std::pair<double, double> invariants(const std::vector<Complex> &omega) const {
        double energy = 0.0, enstrophy = 0.0;
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            const int k2 = kx * kx + ky * ky;
            if (!k2) continue;
            energy += std::norm(omega[i]) / k2;
            enstrophy += std::norm(omega[i]);
        }
        return {energy, enstrophy};
    }
};

static std::vector<std::array<int, 5>> profiles() {
    std::vector<std::array<int, 5>> result;
    for (int first = 0; first < 5; ++first) {
        int combinations = 1;
        for (int j = first + 1; j < 5; ++j) combinations *= 5;
        for (int code = 0; code < combinations; ++code) {
            std::array<int, 5> a{};
            a[first] = 1;
            int value = code;
            for (int j = 4; j > first; --j) {
                a[j] = value % 5 - 2;
                value /= 5;
            }
            result.push_back(a);
        }
    }
    return result;
}

static double low_aq(const std::array<int, 5> &a, double q) {
    return (std::abs(a[0]) * 3.0 * q + std::abs(a[1]) * 3.0 * q +
            std::abs(a[2]) * (2.0 * q * q + 5.0 * q * q * q) +
            std::abs(a[3]) * 10.0 * q * q * q +
            std::abs(a[4]) * 20.0 * q * q * q * q) / 64.0;
}

static double tail_aq(int sigma_denominator, int epsilon_denominator, double q) {
    const double r = q / sigma_denominator;
    double inside = std::pow((1.0 + r) / (1.0 - r), 2);
    double square = 0.0;
    for (int kx = -4; kx <= 4; ++kx)
        for (int ky = -4; ky <= 4; ++ky)
            square += std::pow(r, std::abs(kx) + std::abs(ky));
    return (inside - square) / epsilon_denominator;
}

static int max_feasible_m(const Member &member) {
    static constexpr std::array<double, 4> qs{{33.0/32.0, 17.0/16.0, 9.0/8.0, 5.0/4.0}};
    int maximum = 0;
    for (int m = 1; m <= 32; ++m) {
        const double t = m / 16.0;
        bool feasible = false;
        for (double q : qs) {
            const double aq = low_aq(member.a, q) +
                tail_aq(member.sigma_denominator, member.epsilon_denominator, q);
            const int mj = int(std::ceil(64.0 * aq - 1e-12));
            if (mj >= 1 && mj <= 256) {
                const double alpha = mj / 64.0;
                if (q * (1.0 - alpha * t) > 1.0 + 1e-14) {
                    feasible = true;
                    break;
                }
            }
        }
        if (feasible) maximum = m;
    }
    return maximum;
}

static Options parse_options(int argc, char **argv) {
    Options options;
    for (int i = 1; i < argc; ++i) {
        if (i + 1 >= argc) throw std::runtime_error("missing option value");
        std::string key = argv[i], value = argv[++i];
        if (key == "--n") options.n = std::stoi(value);
        else if (key == "--steps-per-unit") options.steps_per_unit = std::stoi(value);
        else if (key == "--shortlist") options.shortlist = std::stoi(value);
        else if (key == "--report") options.report = std::stoi(value);
        else if (key == "--output") options.output = value;
        else throw std::runtime_error("unknown option " + key);
    }
    if (options.steps_per_unit < 16 || options.steps_per_unit % 16)
        throw std::runtime_error("steps per unit must be divisible by 16");
    return options;
}

static void write_member(std::ostream &out, const Member &member) {
    out << "\"profile_index\":" << member.profile_index << ",\"a\":[";
    for (int i = 0; i < 5; ++i) out << (i ? "," : "") << member.a[i];
    out << "],\"sigma\":\"1/" << member.sigma_denominator
        << "\",\"epsilon\":\"1/" << member.epsilon_denominator << "\"";
}

int main(int argc, char **argv) try {
    const Options options = parse_options(argc, argv);
    EulerSolver solver(options.n);
    std::vector<Member> members;
    int feasible_base_members = 0;
    const auto all_profiles = profiles();
    for (int p = 0; p < int(all_profiles.size()); ++p) {
        for (int sigma : {16, 24}) for (int epsilon : {256, 512, 1024}) {
            Member member;
            member.profile_index = p;
            member.a = all_profiles[p];
            member.sigma_denominator = sigma;
            member.epsilon_denominator = epsilon;
            member.max_feasible_m = max_feasible_m(member);
            if (!member.max_feasible_m) continue;
            ++feasible_base_members;
            member.score = std::abs(solver.log_l3_derivative(solver.initial(member)));
            members.push_back(member);
        }
    }
    std::sort(members.begin(), members.end(), [](const Member &x, const Member &y) {
        if (x.score != y.score) return x.score > y.score;
        if (x.profile_index != y.profile_index) return x.profile_index < y.profile_index;
        if (x.sigma_denominator != y.sigma_denominator)
            return x.sigma_denominator < y.sigma_denominator;
        return x.epsilon_denominator < y.epsilon_denominator;
    });
    if (int(members.size()) > options.shortlist) members.resize(options.shortlist);

    std::vector<Result> results;
    for (const Member &member : members) {
        results.push_back(solver.run(member, 1, options.steps_per_unit));
        results.push_back(solver.run(member, -1, options.steps_per_unit));
    }
    std::sort(results.begin(), results.end(), [](const Result &x, const Result &y) {
        if (x.best_ratio != y.best_ratio) return x.best_ratio > y.best_ratio;
        if (x.member.profile_index != y.member.profile_index)
            return x.member.profile_index < y.member.profile_index;
        return x.direction > y.direction;
    });

    const double shear_expected = std::cbrt(4.0 / (3.0 * PI));
    std::vector<Control> controls;
    controls.push_back(solver.run_control("shear_psi_cos_y", solver.shear(),
                                          shear_expected, options.steps_per_unit));
    controls.push_back(solver.run_control("equal_shell_P1", solver.equal_shell(),
                                          0.0, options.steps_per_unit));

    std::ofstream output(options.output);
    if (!output) throw std::runtime_error("cannot open output");
    output << std::setprecision(17)
        << "{\n  \"status\":\"NUMERICAL_CANDIDATE_GENERATION_ONLY\",\n"
        << "  \"pde_certificate\":false,\n"
        << "  \"independent_method\":\"square_two_thirds_pseudospectral_euler_rk4\",\n"
        << "  \"n\":" << options.n << ",\"cutoff\":" << options.n / 3
        << ",\"dt\":\"1/" << options.steps_per_unit << "\",\n"
        << "  \"normalization\":\"unnormalized_forward_fft_normalized_haar_grid_l3\",\n"
        << "  \"family\":{\"profiles\":781,\"tail_variants\":6,\"terminal_times\":32,"
        << "\"feasible_base_members\":" << feasible_base_members
        << ",\"selection\":\"largest_absolute_initial_log_l3_derivative\","
        << "\"shortlist\":" << options.shortlist << "},\n"
        << "  \"controls\":[\n";
    for (int i = 0; i < int(controls.size()); ++i) {
        const auto &c = controls[i];
        output << "    {\"name\":\"" << c.name << "\",\"initial_l3\":" << c.initial_l3
               << ",\"expected_l3\":" << c.expected_l3
               << ",\"normalization_relative_error\":" << c.normalization_relative_error
               << ",\"rhs_relative_l2\":" << c.rhs_relative_l2
               << ",\"ratio_at_1_over_16\":" << c.ratio
               << ",\"energy_relative_drift\":" << c.energy_drift
               << ",\"enstrophy_relative_drift\":" << c.enstrophy_drift << "}"
               << (i + 1 == int(controls.size()) ? "\n" : ",\n");
    }
    output << "  ],\n  \"top_results\":[\n";
    const int report = std::min(options.report, int(results.size()));
    for (int i = 0; i < report; ++i) {
        const Result &r = results[i];
        output << "    {";
        write_member(output, r.member);
        const int family_index = (((r.member.profile_index * 2 +
            (r.member.sigma_denominator == 24)) * 3 +
            (r.member.epsilon_denominator == 256 ? 0 :
             r.member.epsilon_denominator == 512 ? 1 : 2)) * 32 + r.best_m - 1);
        output << ",\"direction\":" << r.direction
               << ",\"T\":\"" << r.best_m << "/16\",\"family_index_0based\":"
               << family_index << ",\"selection_score\":" << r.member.score
               << ",\"max_ratio\":" << r.best_ratio
               << ",\"ratio_at_max_feasible_T\":" << r.endpoint_ratio
               << ",\"max_feasible_T\":\"" << r.member.max_feasible_m << "/16\""
               << ",\"energy_relative_drift\":" << r.energy_drift
               << ",\"enstrophy_relative_drift\":" << r.enstrophy_drift << "}"
               << (i + 1 == report ? "\n" : ",\n");
    }
    output << "  ]\n}\n";
    std::cout << std::setprecision(17)
              << "screened=" << members.size() << " directional_runs=" << results.size()
              << " top_ratio=" << (results.empty() ? 1.0 : results.front().best_ratio)
              << " output=" << options.output << "\n";
    return 0;
} catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << "\n";
    return 2;
}
