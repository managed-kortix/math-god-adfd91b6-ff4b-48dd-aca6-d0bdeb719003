#include <algorithm>
#include <cmath>
#include <complex>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Complex = std::complex<double>;
constexpr double PI = 3.141592653589793238462643383279502884;

struct Options {
    int max_wave = 5;
    int grid = 48;
    int starts = 12;
    int iterations = 120;
    double step = 0.04;
    std::vector<double> rho = {4.0, 8.0, 12.0, 16.0, 20.0};
    std::string output = "cycle257-initial-l3-candidates.json";
};

struct Evaluation {
    double objective = 0.0;
    double cube = 0.0;
    double numerator = 0.0;
    double energy = 0.0;
    double enstrophy = 0.0;
    std::vector<double> gradient;
};

struct Candidate {
    double rho = 0.0;
    double objective = -std::numeric_limits<double>::infinity();
    double check_objective = 0.0;
    double gradient_error = 0.0;
    int start = -1;
    std::vector<double> x;
};

class InitialL3Functional {
  public:
    InitialL3Functional(int max_wave, int grid)
        : k_(max_wave), n_(grid), points_(grid * grid) {
        if (k_ < 2 || n_ < 4 * k_ + 1)
            throw std::runtime_error("need max-wave >= 2 and grid >= 4*max-wave+1");
        for (int kx = 0; kx <= k_; ++kx) {
            for (int ky = -k_; ky <= k_; ++ky) {
                if (kx == 0 && ky <= 0) continue;
                modes_.push_back({kx, ky});
            }
        }
        const int p = parameter_count();
        ux_.assign(p, std::vector<double>(points_));
        uy_.assign(p, std::vector<double>(points_));
        ox_.assign(p, std::vector<double>(points_));
        oy_.assign(p, std::vector<double>(points_));
        energy_weight_.resize(p);
        enstrophy_weight_.resize(p);
        for (int j = 0; j < int(modes_.size()); ++j) {
            const auto [kx, ky] = modes_[j];
            const double k2 = kx * kx + ky * ky;
            for (int phase = 0; phase < 2; ++phase) {
                const int parameter = 2 * j + phase;
                energy_weight_[parameter] = 0.5 * k2;
                enstrophy_weight_[parameter] = 0.5 * k2 * k2;
                for (int ix = 0; ix < n_; ++ix) {
                    for (int iy = 0; iy < n_; ++iy) {
                        const int z = ix * n_ + iy;
                        const double angle = 2.0 * PI * (kx * ix + ky * iy) / n_;
                        const double derivative = phase == 0 ? -std::sin(angle) : std::cos(angle);
                        ux_[parameter][z] = -ky * derivative;
                        uy_[parameter][z] = kx * derivative;
                        ox_[parameter][z] = -k2 * kx * derivative;
                        oy_[parameter][z] = -k2 * ky * derivative;
                    }
                }
            }
        }
        for (int kx = -2 * k_; kx <= 2 * k_; ++kx) {
            for (int ky = -2 * k_; ky <= 2 * k_; ++ky) {
                if (kx || ky) output_modes_.push_back({kx, ky});
            }
        }
        exponent_.assign(output_modes_.size(), std::vector<Complex>(points_));
        for (int m = 0; m < int(output_modes_.size()); ++m) {
            const auto [kx, ky] = output_modes_[m];
            for (int ix = 0; ix < n_; ++ix) {
                for (int iy = 0; iy < n_; ++iy) {
                    double angle = 2.0 * PI * (kx * ix + ky * iy) / n_;
                    exponent_[m][ix * n_ + iy] = Complex(std::cos(angle), std::sin(angle));
                }
            }
        }
    }

    int parameter_count() const { return 2 * int(modes_.size()); }
    const std::vector<std::pair<int, int>> &modes() const { return modes_; }

    Evaluation evaluate(const std::vector<double> &x, bool with_gradient) const {
        if (int(x.size()) != parameter_count()) throw std::runtime_error("wrong parameter count");
        std::vector<double> u(points_ * 2, 0.0), grad_omega(points_ * 2, 0.0);
        double energy = 0.0, enstrophy = 0.0;
        for (int p = 0; p < parameter_count(); ++p) {
            energy += energy_weight_[p] * x[p] * x[p];
            enstrophy += enstrophy_weight_[p] * x[p] * x[p];
            for (int z = 0; z < points_; ++z) {
                u[2 * z] += x[p] * ux_[p][z];
                u[2 * z + 1] += x[p] * uy_[p][z];
                grad_omega[2 * z] += x[p] * ox_[p][z];
                grad_omega[2 * z + 1] += x[p] * oy_[p][z];
            }
        }
        std::vector<double> forcing(points_);
        for (int z = 0; z < points_; ++z)
            forcing[z] = -(u[2 * z] * grad_omega[2 * z] +
                           u[2 * z + 1] * grad_omega[2 * z + 1]);
        std::vector<double> b;
        apply_biot_savart(forcing, b);
        double cube = 0.0, numerator = 0.0;
        std::vector<double> q(points_ * 2);
        for (int z = 0; z < points_; ++z) {
            double ux = u[2 * z], uy = u[2 * z + 1];
            double speed = std::hypot(ux, uy);
            cube += speed * speed * speed;
            numerator += speed * (ux * b[2 * z] + uy * b[2 * z + 1]);
            q[2 * z] = speed * ux;
            q[2 * z + 1] = speed * uy;
        }
        cube /= points_;
        numerator /= points_;
        Evaluation out;
        out.cube = cube;
        out.numerator = numerator;
        out.energy = energy;
        out.enstrophy = enstrophy;
        out.objective = numerator / (cube * std::sqrt(energy));
        if (!with_gradient) return out;

        std::vector<double> adjoint;
        apply_biot_savart_adjoint(q, adjoint);
        out.gradient.assign(parameter_count(), 0.0);
        for (int p = 0; p < parameter_count(); ++p) {
            double dn = 0.0, df = 0.0;
            for (int z = 0; z < points_; ++z) {
                double vx = ux_[p][z], vy = uy_[p][z];
                double ux = u[2 * z], uy = u[2 * z + 1];
                double bx = b[2 * z], by = b[2 * z + 1];
                double speed = std::hypot(ux, uy);
                double uv = ux * vx + uy * vy;
                df += 3.0 * speed * uv;
                double direct = speed * (vx * bx + vy * by);
                if (speed > 1e-14) direct += uv * (ux * bx + uy * by) / speed;
                double dforce = -(vx * grad_omega[2 * z] + vy * grad_omega[2 * z + 1]
                    + u[2 * z] * ox_[p][z] + u[2 * z + 1] * oy_[p][z]);
                dn += direct + adjoint[z] * dforce;
            }
            dn /= points_;
            df /= points_;
            const double de = 2.0 * energy_weight_[p] * x[p];
            out.gradient[p] = dn / (cube * std::sqrt(energy))
                - out.objective * (df / cube + 0.5 * de / energy);
        }
        return out;
    }

    void retract(std::vector<double> &x, double rho) const {
        double min_k2 = std::numeric_limits<double>::infinity(), max_k2 = 0.0;
        for (int p = 0; p < parameter_count(); ++p) {
            double k2 = enstrophy_weight_[p] / energy_weight_[p];
            if (x[p] != 0.0) { min_k2 = std::min(min_k2, k2); max_k2 = std::max(max_k2, k2); }
        }
        if (!(rho > min_k2 && rho < max_k2))
            throw std::runtime_error("rho must be strictly inside active spectral range");
        auto ratio = [&](double beta) {
            double e = 0.0, z = 0.0;
            for (int p = 0; p < parameter_count(); ++p) {
                double k2 = enstrophy_weight_[p] / energy_weight_[p];
                double y = x[p] * std::exp(beta * (k2 - rho));
                e += energy_weight_[p] * y * y;
                z += enstrophy_weight_[p] * y * y;
            }
            return z / e;
        };
        double lo = -1.0, hi = 1.0;
        while (ratio(lo) > rho) lo *= 2.0;
        while (ratio(hi) < rho) hi *= 2.0;
        for (int i = 0; i < 80; ++i) {
            double mid = 0.5 * (lo + hi);
            if (ratio(mid) < rho) lo = mid; else hi = mid;
        }
        double beta = 0.5 * (lo + hi), e = 0.0;
        for (int p = 0; p < parameter_count(); ++p) {
            double k2 = enstrophy_weight_[p] / energy_weight_[p];
            x[p] *= std::exp(beta * (k2 - rho));
            e += energy_weight_[p] * x[p] * x[p];
        }
        for (double &value : x) value /= std::sqrt(e);
    }

    void project_tangent(std::vector<double> &gradient, const std::vector<double> &x) const {
        std::vector<double> ge(parameter_count()), gz(parameter_count());
        for (int p = 0; p < parameter_count(); ++p) {
            ge[p] = 2.0 * energy_weight_[p] * x[p];
            gz[p] = 2.0 * enstrophy_weight_[p] * x[p];
        }
        double aa = dot(ge, ge), ab = dot(ge, gz), bb = dot(gz, gz);
        double ag = dot(ge, gradient), bg = dot(gz, gradient);
        double determinant = aa * bb - ab * ab;
        double lambda = (ag * bb - bg * ab) / determinant;
        double mu = (bg * aa - ag * ab) / determinant;
        for (int p = 0; p < parameter_count(); ++p)
            gradient[p] -= lambda * ge[p] + mu * gz[p];
    }

  private:
    int k_, n_, points_;
    std::vector<std::pair<int, int>> modes_, output_modes_;
    std::vector<std::vector<double>> ux_, uy_, ox_, oy_;
    std::vector<double> energy_weight_, enstrophy_weight_;
    std::vector<std::vector<Complex>> exponent_;

    static double dot(const std::vector<double> &a, const std::vector<double> &b) {
        double value = 0.0;
        for (int i = 0; i < int(a.size()); ++i) value += a[i] * b[i];
        return value;
    }

    void apply_biot_savart(const std::vector<double> &f, std::vector<double> &out) const {
        out.assign(points_ * 2, 0.0);
        for (int m = 0; m < int(output_modes_.size()); ++m) {
            Complex coefficient = 0.0;
            for (int z = 0; z < points_; ++z) coefficient += f[z] * std::conj(exponent_[m][z]);
            coefficient /= points_;
            const auto [kx, ky] = output_modes_[m];
            const double k2 = kx * kx + ky * ky;
            Complex mx(0.0, double(ky) / k2), my(0.0, -double(kx) / k2);
            for (int z = 0; z < points_; ++z) {
                out[2 * z] += (mx * coefficient * exponent_[m][z]).real();
                out[2 * z + 1] += (my * coefficient * exponent_[m][z]).real();
            }
        }
    }

    void apply_biot_savart_adjoint(const std::vector<double> &q, std::vector<double> &out) const {
        out.assign(points_, 0.0);
        for (int m = 0; m < int(output_modes_.size()); ++m) {
            Complex qx = 0.0, qy = 0.0;
            for (int z = 0; z < points_; ++z) {
                Complex e = std::conj(exponent_[m][z]);
                qx += q[2 * z] * e;
                qy += q[2 * z + 1] * e;
            }
            qx /= points_; qy /= points_;
            const auto [kx, ky] = output_modes_[m];
            const double k2 = kx * kx + ky * ky;
            Complex coefficient = Complex(0.0, -double(ky) / k2) * qx
                                + Complex(0.0, double(kx) / k2) * qy;
            for (int z = 0; z < points_; ++z)
                out[z] += (coefficient * exponent_[m][z]).real();
        }
    }
};

static std::vector<double> deterministic_start(int count, int start) {
    std::vector<double> x(count);
    for (int j = 0; j < count; ++j) {
        double a = double((start + 1) * (j + 1));
        x[j] = std::sin(a * 1.4142135623730951) + 0.5 * std::cos(a * 0.7548776662466927);
    }
    return x;
}

static Candidate optimize(const InitialL3Functional &functional, double rho,
                          int start, int iterations, double step) {
    Candidate best;
    best.rho = rho; best.start = start;
    std::vector<double> x = deterministic_start(functional.parameter_count(), start);
    functional.retract(x, rho);
    for (int iteration = 0; iteration < iterations; ++iteration) {
        Evaluation value = functional.evaluate(x, true);
        if (value.objective > best.objective) { best.objective = value.objective; best.x = x; }
        std::vector<double> gradient = value.gradient;
        functional.project_tangent(gradient, x);
        double norm = std::sqrt(std::inner_product(gradient.begin(), gradient.end(), gradient.begin(), 0.0));
        double local_step = step / std::sqrt(1.0 + 0.03 * iteration);
        if (norm > 0.0)
            for (int p = 0; p < int(x.size()); ++p) x[p] += local_step * gradient[p] / norm;
        functional.retract(x, rho);
    }
    Evaluation last = functional.evaluate(x, false);
    if (last.objective > best.objective) { best.objective = last.objective; best.x = x; }
    return best;
}

static double gradient_check(const InitialL3Functional &functional, const Candidate &candidate) {
    Evaluation value = functional.evaluate(candidate.x, true);
    std::vector<double> direction = deterministic_start(functional.parameter_count(), 997 + candidate.start);
    functional.project_tangent(direction, candidate.x);
    double norm = std::sqrt(std::inner_product(direction.begin(), direction.end(), direction.begin(), 0.0));
    for (double &v : direction) v /= norm;
    const double h = 1e-6;
    std::vector<double> plus = candidate.x, minus = candidate.x;
    for (int p = 0; p < int(plus.size()); ++p) { plus[p] += h * direction[p]; minus[p] -= h * direction[p]; }
    functional.retract(plus, candidate.rho);
    functional.retract(minus, candidate.rho);
    double finite = (functional.evaluate(plus, false).objective - functional.evaluate(minus, false).objective) / (2 * h);
    double exact = std::inner_product(value.gradient.begin(), value.gradient.end(), direction.begin(), 0.0);
    return std::abs(finite - exact) / std::max({1.0, std::abs(finite), std::abs(exact)});
}

static Options parse(int argc, char **argv) {
    Options options;
    for (int i = 1; i < argc; ++i) {
        if (i + 1 >= argc) throw std::runtime_error("missing option value");
        std::string key = argv[i], value = argv[++i];
        if (key == "--max-wave") options.max_wave = std::stoi(value);
        else if (key == "--grid") options.grid = std::stoi(value);
        else if (key == "--starts") options.starts = std::stoi(value);
        else if (key == "--iterations") options.iterations = std::stoi(value);
        else if (key == "--step") options.step = std::stod(value);
        else if (key == "--rho") { options.rho.clear(); options.rho.push_back(std::stod(value)); }
        else if (key == "--output") options.output = value;
        else throw std::runtime_error("unknown option " + key);
    }
    return options;
}

int main(int argc, char **argv) try {
    Options options = parse(argc, argv);
    InitialL3Functional functional(options.max_wave, options.grid);
    std::vector<Candidate> candidates;
    for (double rho : options.rho) {
        Candidate best;
        for (int start = 0; start < options.starts; ++start) {
            Candidate candidate = optimize(functional, rho, start, options.iterations, options.step);
            if (candidate.objective > best.objective) best = std::move(candidate);
        }
        best.gradient_error = gradient_check(functional, best);
        InitialL3Functional check(options.max_wave, 2 * options.grid);
        best.check_objective = check.evaluate(best.x, false).objective;
        candidates.push_back(std::move(best));
        std::cerr << "rho=" << rho << " objective=" << candidates.back().objective
                  << " check=" << candidates.back().check_objective << '\n';
    }
    std::ofstream out(options.output);
    out << std::setprecision(17)
        << "{\n  \"format\": \"cycle257-initial-l3-candidate-v1\",\n"
        << "  \"status\": \"FLOATING_CANDIDATE_BOXES_ONLY\",\n"
        << "  \"pde_certificate\": false,\n"
        << "  \"objective\": \"(d/dt log ||u||_3 at zero)/||u||_2\",\n"
        << "  \"constraints\": \"energy=1,enstrophy=rho\",\n"
        << "  \"max_wave\": " << options.max_wave << ",\n"
        << "  \"grid\": " << options.grid << ",\n"
        << "  \"starts\": " << options.starts << ",\n"
        << "  \"iterations\": " << options.iterations << ",\n"
        << "  \"modes\": [";
    for (int j = 0; j < int(functional.modes().size()); ++j) {
        if (j) out << ',';
        out << '[' << functional.modes()[j].first << ',' << functional.modes()[j].second << ']';
    }
    out << "],\n  \"candidates\": [\n";
    for (int c = 0; c < int(candidates.size()); ++c) {
        const Candidate &candidate = candidates[c];
        out << "    {\"rho\": " << candidate.rho << ", \"start\": " << candidate.start
            << ", \"objective\": " << candidate.objective
            << ", \"double_grid_objective\": " << candidate.check_objective
            << ", \"directional_gradient_relative_error\": " << candidate.gradient_error
            << ", \"coefficient_box_radius\": 5e-12, \"coefficients\": [";
        for (int p = 0; p < int(candidate.x.size()); ++p) {
            if (p) out << ',';
            out << candidate.x[p];
        }
        out << "]}" << (c + 1 == int(candidates.size()) ? "\n" : ",\n");
    }
    out << "  ]\n}\n";
    std::cout << options.output << '\n';
    return 0;
} catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
}
