#include <algorithm>
#include <cmath>
#include <complex>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Complex = std::complex<double>;

constexpr double PI = 3.141592653589793238462643383279502884;

struct Options {
    int seeds = 32;
    uint64_t seed = 214;
    int max_wave = 2;
    int n32 = 32;
    int n64 = 64;
    int steps = 128;
    int iterations32 = 30;
    int iterations64 = 20;
    double learning_rate = 0.03;
    double time_learning_rate = 0.02;
    double initial_time = 1.0;
    double min_time = 0.05;
    double max_time = 4.0;
    double promote = 1.2;
    double target = 2.0;
    std::string output = "cycle214-gradient-screen.json";
};

struct Evaluation {
    double ratio = 0.0;
    std::vector<double> gradient;
    double time_gradient = 0.0;
    bool finite = true;
};

struct Candidate {
    int seed = 0;
    double ratio32 = 0.0;
    double ratio64 = 0.0;
    double time = 0.0;
    std::vector<double> coefficients;
};

class DifferentiableEuler {
  public:
    DifferentiableEuler(int n, int max_wave)
        : n_(n), size_(n * n), cutoff_(n / 3) {
        if (n < 8 || (n & (n - 1)))
            throw std::runtime_error("N must be a power of two at least 8");
        if (max_wave < 1 || max_wave > cutoff_)
            throw std::runtime_error("max-wave must lie in the dealiased range");
        for (int kx = 0; kx <= max_wave; ++kx) {
            for (int ky = -max_wave; ky <= max_wave; ++ky) {
                if ((kx == 0 && ky <= 0) || (kx == 0 && ky == 0)) continue;
                modes_.push_back({kx, ky});
            }
        }
    }

    int parameter_count() const { return 2 * int(modes_.size()); }

    Evaluation evaluate(const std::vector<double> &parameters, double terminal_time,
                        int steps, bool gradient) const {
        if (int(parameters.size()) != parameter_count())
            throw std::runtime_error("wrong coefficient count");
        if (steps < 1 || !(terminal_time > 0.0))
            throw std::runtime_error("steps and terminal time must be positive");

        int pcount = gradient ? parameter_count() + 1 : 0;
        std::vector<Complex> state(size_, 0.0);
        std::vector<std::vector<Complex>> tangent(
            pcount, std::vector<Complex>(size_, 0.0));
        for (size_t j = 0; j < modes_.size(); ++j) {
            int kx = modes_[j].first, ky = modes_[j].second;
            int k2 = kx * kx + ky * ky;
            Complex psi(0.5 * parameters[2 * j], -0.5 * parameters[2 * j + 1]);
            Complex omega = -double(k2 * size_) * psi;
            state[index(kx, ky)] += omega;
            state[index(-kx, -ky)] += std::conj(omega);
            if (gradient) {
                Complex da = -0.5 * double(k2 * size_);
                Complex db(0.0, 0.5 * double(k2 * size_));
                tangent[2 * j][index(kx, ky)] += da;
                tangent[2 * j][index(-kx, -ky)] += std::conj(da);
                tangent[2 * j + 1][index(kx, ky)] += db;
                tangent[2 * j + 1][index(-kx, -ky)] += std::conj(db);
            }
        }

        std::vector<double> initial_derivative;
        double initial_norm = norm_and_derivative(state, tangent, initial_derivative);
        double h = terminal_time / steps;
        for (int step = 0; step < steps; ++step) {
            std::vector<Complex> k1, k2, k3, k4, stage(size_);
            std::vector<std::vector<Complex>> dk1, dk2, dk3, dk4;
            std::vector<std::vector<Complex>> dstage(
                pcount, std::vector<Complex>(size_));
            rhs(state, tangent, k1, dk1);
            for (int i = 0; i < size_; ++i) stage[i] = state[i] + 0.5 * h * k1[i];
            for (int p = 0; p < pcount; ++p) {
                double dh = p == pcount - 1 ? 1.0 / steps : 0.0;
                for (int i = 0; i < size_; ++i)
                    dstage[p][i] = tangent[p][i] + 0.5 * (dh * k1[i] + h * dk1[p][i]);
            }
            rhs(stage, dstage, k2, dk2);
            for (int i = 0; i < size_; ++i) stage[i] = state[i] + 0.5 * h * k2[i];
            for (int p = 0; p < pcount; ++p) {
                double dh = p == pcount - 1 ? 1.0 / steps : 0.0;
                for (int i = 0; i < size_; ++i)
                    dstage[p][i] = tangent[p][i] + 0.5 * (dh * k2[i] + h * dk2[p][i]);
            }
            rhs(stage, dstage, k3, dk3);
            for (int i = 0; i < size_; ++i) stage[i] = state[i] + h * k3[i];
            for (int p = 0; p < pcount; ++p) {
                double dh = p == pcount - 1 ? 1.0 / steps : 0.0;
                for (int i = 0; i < size_; ++i)
                    dstage[p][i] = tangent[p][i] + dh * k3[i] + h * dk3[p][i];
            }
            rhs(stage, dstage, k4, dk4);
            for (int i = 0; i < size_; ++i)
                state[i] += h * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0;
            for (int p = 0; p < pcount; ++p) {
                double dh = p == pcount - 1 ? 1.0 / steps : 0.0;
                for (int i = 0; i < size_; ++i) {
                    Complex weighted = k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i];
                    Complex dweighted = dk1[p][i] + 2.0 * dk2[p][i]
                        + 2.0 * dk3[p][i] + dk4[p][i];
                    tangent[p][i] += (dh * weighted + h * dweighted) / 6.0;
                }
            }
        }

        std::vector<double> final_derivative;
        double final_norm = norm_and_derivative(state, tangent, final_derivative);
        Evaluation out;
        out.ratio = final_norm / initial_norm;
        out.finite = std::isfinite(out.ratio);
        if (gradient) {
            out.gradient.resize(parameter_count());
            for (int p = 0; p < parameter_count(); ++p)
                out.gradient[p] = final_derivative[p] / initial_norm -
                    final_norm * initial_derivative[p] / (initial_norm * initial_norm);
            out.time_gradient = final_derivative.back() / initial_norm;
            for (double x : out.gradient) out.finite = out.finite && std::isfinite(x);
            out.finite = out.finite && std::isfinite(out.time_gradient);
        }
        return out;
    }

  private:
    int n_, size_, cutoff_;
    std::vector<std::pair<int, int>> modes_;

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
                    Complex u = p[i + j], v = p[i + j + len / 2] * w;
                    p[i + j] = u + v;
                    p[i + j + len / 2] = u - v;
                    w *= root;
                }
            }
        }
        if (inverse) for (int i = 0; i < n_; ++i) p[i] /= n_;
    }

    void fft2(std::vector<Complex> &v, bool inverse) const {
        for (int x = 0; x < n_; ++x) fft1(v.data() + x * n_, inverse);
        std::vector<Complex> column(n_);
        for (int y = 0; y < n_; ++y) {
            for (int x = 0; x < n_; ++x) column[x] = v[x * n_ + y];
            fft1(column.data(), inverse);
            for (int x = 0; x < n_; ++x) v[x * n_ + y] = column[x];
        }
    }

    void fields(const std::vector<Complex> &omega, std::vector<Complex> &u,
                std::vector<Complex> &v, std::vector<Complex> &wx,
                std::vector<Complex> &wy) const {
        u.resize(size_); v.resize(size_); wx.resize(size_); wy.resize(size_);
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            int k2 = kx * kx + ky * ky;
            Complex psi = k2 ? -omega[i] / double(k2) : 0.0;
            u[i] = Complex(0.0, -ky) * psi;
            v[i] = Complex(0.0, kx) * psi;
            wx[i] = Complex(0.0, kx) * omega[i];
            wy[i] = Complex(0.0, ky) * omega[i];
        }
        fft2(u, true); fft2(v, true); fft2(wx, true); fft2(wy, true);
    }

    void rhs(const std::vector<Complex> &state,
             const std::vector<std::vector<Complex>> &tangent,
             std::vector<Complex> &out,
             std::vector<std::vector<Complex>> &dout) const {
        std::vector<Complex> u, v, wx, wy;
        fields(state, u, v, wx, wy);
        out.resize(size_);
        for (int i = 0; i < size_; ++i)
            out[i] = -(u[i].real() * wx[i].real() + v[i].real() * wy[i].real());
        fft2(out, false);
        dealias(out);
        dout.assign(tangent.size(), std::vector<Complex>(size_));
        for (size_t p = 0; p < tangent.size(); ++p) {
            std::vector<Complex> du, dv, dwx, dwy;
            fields(tangent[p], du, dv, dwx, dwy);
            for (int i = 0; i < size_; ++i) {
                dout[p][i] = -(du[i].real() * wx[i].real() + u[i].real() * dwx[i].real()
                    + dv[i].real() * wy[i].real() + v[i].real() * dwy[i].real());
            }
            fft2(dout[p], false);
            dealias(dout[p]);
        }
    }

    void dealias(std::vector<Complex> &values) const {
        for (int i = 0; i < size_; ++i) {
            auto [kx, ky] = wave(i);
            if (std::abs(kx) > cutoff_ || std::abs(ky) > cutoff_) values[i] = 0.0;
        }
        values[0] = 0.0;
    }

    double norm_and_derivative(const std::vector<Complex> &state,
            const std::vector<std::vector<Complex>> &tangent,
            std::vector<double> &derivative) const {
        std::vector<Complex> u, v, wx, wy;
        fields(state, u, v, wx, wy);
        double cube = 0.0;
        for (int i = 0; i < size_; ++i) {
            double speed = std::hypot(u[i].real(), v[i].real());
            cube += speed * speed * speed;
        }
        cube /= size_;
        double norm = std::cbrt(cube);
        derivative.assign(tangent.size(), 0.0);
        for (size_t p = 0; p < tangent.size(); ++p) {
            std::vector<Complex> du, dv, dummy1, dummy2;
            fields(tangent[p], du, dv, dummy1, dummy2);
            double sum = 0.0;
            for (int i = 0; i < size_; ++i) {
                double ux = u[i].real(), uy = v[i].real();
                sum += std::hypot(ux, uy) * (ux * du[i].real() + uy * dv[i].real());
            }
            derivative[p] = sum / (size_ * norm * norm);
        }
        return norm;
    }
};

static void normalize(std::vector<double> &x) {
    double norm = 0.0;
    for (double value : x) norm += value * value;
    norm = std::sqrt(norm);
    if (!(norm > 0.0)) throw std::runtime_error("zero coefficient vector");
    for (double &value : x) value /= norm;
}

static Evaluation optimize(DifferentiableEuler &solver, std::vector<double> &x,
                           double &time, int steps, int iterations,
                           double learning_rate, double time_learning_rate,
                           double min_time, double max_time) {
    std::vector<double> m(x.size(), 0.0), v(x.size(), 0.0);
    double mt = 0.0, vt = 0.0;
    Evaluation best;
    std::vector<double> best_x = x;
    double best_time = time;
    for (int iteration = 1; iteration <= iterations; ++iteration) {
        Evaluation current = solver.evaluate(x, time, steps, true);
        if (!current.finite) break;
        if (current.ratio > best.ratio) {
            best = current; best_x = x; best_time = time;
        }
        double radial = 0.0;
        for (size_t i = 0; i < x.size(); ++i) radial += current.gradient[i] * x[i];
        for (size_t i = 0; i < x.size(); ++i) {
            double g = current.gradient[i] - radial * x[i];
            m[i] = 0.9 * m[i] + 0.1 * g;
            v[i] = 0.999 * v[i] + 0.001 * g * g;
            double mh = m[i] / (1.0 - std::pow(0.9, iteration));
            double vh = v[i] / (1.0 - std::pow(0.999, iteration));
            x[i] += learning_rate * mh / (std::sqrt(vh) + 1e-8);
        }
        normalize(x);
        double gt = current.time_gradient;
        mt = 0.9 * mt + 0.1 * gt;
        vt = 0.999 * vt + 0.001 * gt * gt;
        double mth = mt / (1.0 - std::pow(0.9, iteration));
        double vth = vt / (1.0 - std::pow(0.999, iteration));
        time = std::clamp(time + time_learning_rate * mth / (std::sqrt(vth) + 1e-8),
                          min_time, max_time);
    }
    Evaluation last = solver.evaluate(x, time, steps, false);
    if (last.finite && last.ratio > best.ratio) {
        best = last; best_x = x; best_time = time;
    }
    x = best_x; time = best_time;
    return best;
}

static Options parse(int argc, char **argv) {
    Options o;
    for (int i = 1; i < argc; ++i) {
        std::string key = argv[i];
        if (i + 1 >= argc) throw std::runtime_error("missing value for " + key);
        std::string value = argv[++i];
        if (key == "--seeds") o.seeds = std::stoi(value);
        else if (key == "--seed") o.seed = std::stoull(value);
        else if (key == "--max-wave") o.max_wave = std::stoi(value);
        else if (key == "--n32") o.n32 = std::stoi(value);
        else if (key == "--n64") o.n64 = std::stoi(value);
        else if (key == "--steps") o.steps = std::stoi(value);
        else if (key == "--iterations32") o.iterations32 = std::stoi(value);
        else if (key == "--iterations64") o.iterations64 = std::stoi(value);
        else if (key == "--learning-rate") o.learning_rate = std::stod(value);
        else if (key == "--time-learning-rate") o.time_learning_rate = std::stod(value);
        else if (key == "--initial-time") o.initial_time = std::stod(value);
        else if (key == "--min-time") o.min_time = std::stod(value);
        else if (key == "--max-time") o.max_time = std::stod(value);
        else if (key == "--promote") o.promote = std::stod(value);
        else if (key == "--target") o.target = std::stod(value);
        else if (key == "--output") o.output = value;
        else throw std::runtime_error("unknown option " + key);
    }
    if (o.seeds < 1 || o.steps < 1 || o.iterations32 < 1 || o.iterations64 < 0)
        throw std::runtime_error("seed, step, and iteration counts are invalid");
    if (!(o.min_time > 0.0 && o.initial_time >= o.min_time &&
          o.initial_time <= o.max_time))
        throw std::runtime_error("invalid time interval");
    return o;
}

static void write_vector(std::ostream &out, const std::vector<double> &x) {
    out << '[';
    for (size_t i = 0; i < x.size(); ++i) {
        if (i) out << ',';
        out << x[i];
    }
    out << ']';
}

int main(int argc, char **argv) try {
    Options o = parse(argc, argv);
    DifferentiableEuler coarse(o.n32, o.max_wave), fine(o.n64, o.max_wave);
    if (coarse.parameter_count() != fine.parameter_count())
        throw std::runtime_error("resolution parameterizations disagree");
    std::mt19937_64 random(o.seed);
    std::normal_distribution<double> normal;
    std::vector<Candidate> candidates;
    int promoted = 0, crossed = 0;
    for (int seed_index = 0; seed_index < o.seeds; ++seed_index) {
        std::vector<double> x(coarse.parameter_count());
        for (double &value : x) value = normal(random);
        normalize(x);
        double time = o.initial_time;
        Evaluation e32 = optimize(coarse, x, time, o.steps, o.iterations32,
                                  o.learning_rate, o.time_learning_rate,
                                  o.min_time, o.max_time);
        Candidate candidate{seed_index, e32.ratio, 0.0, time, x};
        if (e32.ratio > o.promote) {
            ++promoted;
            Evaluation e64 = optimize(fine, candidate.coefficients, candidate.time,
                                      2 * o.steps, o.iterations64,
                                      0.5 * o.learning_rate, 0.5 * o.time_learning_rate,
                                      o.min_time, o.max_time);
            candidate.ratio64 = e64.ratio;
            if (e64.ratio > o.target) ++crossed;
        }
        candidates.push_back(candidate);
        std::cerr << "seed=" << seed_index << " ratio32=" << candidate.ratio32
                  << " ratio64=" << candidate.ratio64 << " T=" << candidate.time << '\n';
    }
    std::sort(candidates.begin(), candidates.end(), [](const Candidate &a, const Candidate &b) {
        double ar = a.ratio64 > 0.0 ? a.ratio64 : a.ratio32;
        double br = b.ratio64 > 0.0 ? b.ratio64 : b.ratio32;
        return ar > br;
    });
    const Candidate &best = candidates.front();
    Evaluation best_coarse_steps = coarse.evaluate(
        best.coefficients, best.time, o.steps, false);
    Evaluation best_coarse_half_step = coarse.evaluate(
        best.coefficients, best.time, 2 * o.steps, false);
    Evaluation best_fine_steps = fine.evaluate(
        best.coefficients, best.time, o.steps, false);
    Evaluation best_fine_half_step = fine.evaluate(
        best.coefficients, best.time, 2 * o.steps, false);
    std::ofstream out(o.output);
    out << std::setprecision(17);
    out << "{\n  \"status\": \"FLOATING_AUTOMATIC_GRADIENT_SCREEN\",\n"
        << "  \"rigorous_interval_certificate\": false,\n"
        << "  \"method\": {\"gradient\": \"forward_tangent_discrete_rk4\","
        << " \"n32\": " << o.n32 << ", \"n64\": " << o.n64
        << ", \"max_wave\": " << o.max_wave << ", \"parameters\": "
        << coarse.parameter_count() << ", \"steps32\": " << o.steps
        << ", \"steps64\": " << 2 * o.steps << ", \"seeds\": " << o.seeds << "},\n"
        << "  \"thresholds\": {\"promote\": " << o.promote
        << ", \"target\": " << o.target << "},\n"
        << "  \"counts\": {\"promoted\": " << promoted
        << ", \"crossed_target\": " << crossed << "},\n"
        << "  \"best_resolution_checks\": {\"seed\": " << best.seed
        << ", \"T\": " << best.time
        << ", \"n" << o.n32 << "_steps" << o.steps << "\": "
        << best_coarse_steps.ratio
        << ", \"n" << o.n32 << "_steps" << 2 * o.steps << "\": "
        << best_coarse_half_step.ratio
        << ", \"n" << o.n64 << "_steps" << o.steps << "\": "
        << best_fine_steps.ratio
        << ", \"n" << o.n64 << "_steps" << 2 * o.steps << "\": "
        << best_fine_half_step.ratio << "},\n"
        << "  \"candidates\": [\n";
    for (size_t i = 0; i < candidates.size(); ++i) {
        const Candidate &c = candidates[i];
        out << "    {\"seed\": " << c.seed << ", \"ratio32\": " << c.ratio32
            << ", \"ratio64\": " << c.ratio64 << ", \"T\": " << c.time
            << ", \"coefficients\": ";
        write_vector(out, c.coefficients);
        out << '}' << (i + 1 == candidates.size() ? "\n" : ",\n");
    }
    out << "  ],\n  \"observed_over_two\": " << (crossed ? "true" : "false") << "\n}\n";
    std::cout << o.output << '\n';
    return 0;
} catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
}
