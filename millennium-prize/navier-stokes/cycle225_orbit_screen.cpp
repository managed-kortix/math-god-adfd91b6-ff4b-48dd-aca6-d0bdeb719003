#include <algorithm>
#include <cmath>
#include <complex>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Complex = std::complex<double>;

constexpr double PI = 3.141592653589793238462643383279502884;

struct Options {
    int n = 128;
    int steps_per_unit = 1024;
    double final_time = 8.0;
    std::string output = "cycle225-orbit-N128.json";
};

struct Diagnostics {
    double endpoint_ratio = 0.0;
    double maximum_ratio = 1.0;
    double maximum_time = 0.0;
    double energy_relative_drift = 0.0;
    double enstrophy_relative_drift = 0.0;
};

class EulerScreen {
  public:
    explicit EulerScreen(int n)
        : n_(n), size_(n * n), cutoff_(n / 3), a_(size_), b_(size_),
          c_(size_), d_(size_), physical_(size_) {
        if (n < 8 || (n & (n - 1)))
            throw std::runtime_error("N must be a power of two at least 8");
    }

    std::vector<Complex> cycle225_packet() const {
        static constexpr int rails[8][2] = {
            {1, 1}, {2, 1}, {3, 2}, {5, 3},
            {8, 5}, {13, 8}, {21, 13}, {34, 21},
        };
        static constexpr double amplitudes[8] = {
            -0.001, -0.001, 1.0, 1.0, 1.0, -0.001, -0.001, -0.001,
        };
        std::vector<Complex> omega(size_, 0.0);
        for (int j = 0; j < 8; ++j) {
            int kx = rails[j][0], ky = rails[j][1];
            if (std::abs(kx) > cutoff_ || std::abs(ky) > cutoff_)
                throw std::runtime_error("Cycle 225 rail lies outside the cutoff");
            Complex value = amplitudes[j] * double(size_);
            omega[index(kx, ky)] = value;
            omega[index(-kx, -ky)] = value;
        }
        return omega;
    }

    Diagnostics run(std::vector<Complex> omega, int steps_per_unit,
                    double final_time) {
        if (steps_per_unit < 16 || steps_per_unit % 16 != 0)
            throw std::runtime_error("steps per unit must be divisible by 16");
        int steps = int(std::llround(final_time * steps_per_unit));
        if (steps < 1 || std::abs(steps - final_time * steps_per_unit) > 1e-10)
            throw std::runtime_error("T/dt must be integral");

        const double dt = 1.0 / steps_per_unit;
        const int checkpoint_stride = steps_per_unit / 16;
        const double initial_l3 = l3(omega);
        const auto [initial_energy, initial_enstrophy] = invariants(omega);
        std::vector<Complex> nonlinear, old_nonlinear;
        nonlinear_term(omega, nonlinear);
        old_nonlinear = nonlinear;

        Diagnostics result;
        for (int step = 1; step <= steps; ++step) {
            for (int i = 0; i < size_; ++i) {
                if (step == 1) omega[i] += dt * nonlinear[i];
                else omega[i] += dt * (1.5 * nonlinear[i] - 0.5 * old_nonlinear[i]);
            }
            old_nonlinear.swap(nonlinear);
            nonlinear_term(omega, nonlinear);
            if (step % checkpoint_stride == 0) {
                double ratio = l3(omega) / initial_l3;
                if (!std::isfinite(ratio))
                    throw std::runtime_error("non-finite orbit");
                result.endpoint_ratio = ratio;
                if (ratio > result.maximum_ratio) {
                    result.maximum_ratio = ratio;
                    result.maximum_time = step * dt;
                }
            }
        }
        const auto [final_energy, final_enstrophy] = invariants(omega);
        result.energy_relative_drift =
            std::abs(final_energy / initial_energy - 1.0);
        result.enstrophy_relative_drift =
            std::abs(final_enstrophy / initial_enstrophy - 1.0);
        return result;
    }

  private:
    int n_, size_, cutoff_;
    std::vector<Complex> a_, b_, c_, d_, physical_;

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

    void fft1(Complex *p, bool inverse) const {
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
                    Complex u = p[i + j];
                    Complex v = p[i + j + len / 2] * w;
                    p[i + j] = u + v;
                    p[i + j + len / 2] = u - v;
                    w *= root;
                }
            }
        }
        if (inverse)
            for (int i = 0; i < n_; ++i) p[i] /= n_;
    }

    void fft2(std::vector<Complex> &values, bool inverse) const {
        for (int x = 0; x < n_; ++x)
            fft1(values.data() + x * n_, inverse);
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
            int k2 = kx * kx + ky * ky;
            Complex psi = k2 ? -omega[i] / double(k2) : 0.0;
            u[i] = Complex(0.0, -ky) * psi;
            v[i] = Complex(0.0, kx) * psi;
        }
    }

    void nonlinear_term(const std::vector<Complex> &omega,
                        std::vector<Complex> &out) {
        velocity(omega, a_, b_);
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            c_[i] = Complex(0.0, kx) * omega[i];
            d_[i] = Complex(0.0, ky) * omega[i];
        }
        fft2(a_, true);
        fft2(b_, true);
        fft2(c_, true);
        fft2(d_, true);
        for (int i = 0; i < size_; ++i)
            physical_[i] = -(a_[i].real() * c_[i].real()
                           + b_[i].real() * d_[i].real());
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
        fft2(a_, true);
        fft2(b_, true);
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
            double value = std::norm(omega[i]);
            energy += value / k2;
            enstrophy += value;
        }
        return {energy, enstrophy};
    }
};

static Options parse_options(int argc, char **argv) {
    Options options;
    for (int i = 1; i < argc; ++i) {
        if (i + 1 >= argc) throw std::runtime_error("missing option value");
        std::string key = argv[i], value = argv[++i];
        if (key == "--n") options.n = std::stoi(value);
        else if (key == "--steps-per-unit") options.steps_per_unit = std::stoi(value);
        else if (key == "--final-time") options.final_time = std::stod(value);
        else if (key == "--output") options.output = value;
        else throw std::runtime_error("unknown option " + key);
    }
    return options;
}

int main(int argc, char **argv) try {
    Options options = parse_options(argc, argv);
    EulerScreen solver(options.n);
    Diagnostics result = solver.run(solver.cycle225_packet(),
                                    options.steps_per_unit, options.final_time);
    std::ofstream output(options.output);
    if (!output) throw std::runtime_error("cannot open output");
    output << std::setprecision(17)
           << "{\n"
           << "  \"status\": \"FLOATING_GALERKIN_SCREEN_ONLY\",\n"
           << "  \"pde_certificate\": false,\n"
           << "  \"floating_label\": \"N" << options.n << " dt1/"
           << options.steps_per_unit << " T" << options.final_time << "\",\n"
           << "  \"packet\": \"cycle225_fibonacci_epsilon_1_over_1000\",\n"
           << "  \"method\": \"square_two_thirds_pseudospectral_euler_ab2\",\n"
           << "  \"n\": " << options.n << ",\n"
           << "  \"cutoff\": " << options.n / 3 << ",\n"
           << "  \"dt\": \"1/" << options.steps_per_unit << "\",\n"
           << "  \"final_time\": " << options.final_time << ",\n"
           << "  \"checkpoint_spacing\": \"1/16\",\n"
           << "  \"endpoint_l3_ratio\": " << result.endpoint_ratio << ",\n"
           << "  \"maximum_checkpoint_l3_ratio\": " << result.maximum_ratio << ",\n"
           << "  \"maximum_checkpoint_time\": " << result.maximum_time << ",\n"
           << "  \"energy_relative_drift\": " << result.energy_relative_drift << ",\n"
           << "  \"enstrophy_relative_drift\": " << result.enstrophy_relative_drift << "\n"
           << "}\n";
    std::cout << std::setprecision(17)
              << "N=" << options.n << " dt=1/" << options.steps_per_unit
              << " T=" << options.final_time
              << " endpoint_ratio=" << result.endpoint_ratio
              << " max_ratio=" << result.maximum_ratio
              << " energy_drift=" << result.energy_relative_drift
              << " enstrophy_drift=" << result.enstrophy_relative_drift << "\n";
    return 0;
} catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << "\n";
    return 2;
}
