#define main cycle212_embedded_main
#include "cycle212_screen.cpp"
#undef main

#include <atomic>
#include <thread>

struct Cycle213Options {
    int reduced_n = 8;
    int reduced_steps = 16;
    double reduced_time = 0.25;
    int reduced_keep = 256;
    int candidate_keep = 32;
    int coarse_n = 64;
    int coarse_steps = 512;
    int fine_n = 128;
    int fine_steps = 1024;
    int fine_keep = 5;
    double final_time = 4.0;
    int threads = std::max(1u, std::thread::hardware_concurrency());
    int max_active = 0;
    std::string output = "cycle213-screen.json";
};

struct ScreenRow {
    Coeff c;
    double upper_proxy = 0.0;
    double reduced_mu = 0.0;
    RunResult reduced;
};

constexpr std::array<double, 7> SCREEN_MUS{{1, .5, .25, .125, .0625, .03125, .015625}};

static double predictor_upper_proxy(const Coeff &c, double mu, double horizon,
                                    SpectralSolver &norm_solver) {
    // The convolution coefficients are evaluated on exact integer support.
    // Triangle and Minkowski inequalities then give a floating upper proxy for
    // the first-order predictor u(0)+t u_t(0); this is not a PDE upper bound.
    struct Wave { int x, y; Complex psi; };
    std::vector<Wave> waves;
    for (int j = 0; j < 5; ++j) {
        Complex z(0.5 * c[2 * j], -0.5 * c[2 * j + 1]);
        waves.push_back({MODES[j][0], MODES[j][1], z});
        waves.push_back({-MODES[j][0], -MODES[j][1], std::conj(z)});
    }
    std::array<std::array<Complex, 9>, 9> rhs{};
    for (const auto &p : waves) for (const auto &q : waves) {
        int cross = p.x * q.y - p.y * q.x;
        int q2 = q.x * q.x + q.y * q.y;
        rhs[p.x + q.x + 4][p.y + q.y + 4] += double(cross * q2) * p.psi * q.psi;
    }
    for (const auto &p : waves) {
        int k2 = p.x * p.x + p.y * p.y;
        rhs[p.x + 4][p.y + 4] += mu * double(k2 * k2) * p.psi;
    }
    double velocity_l1 = 0.0;
    for (int x = -4; x <= 4; ++x) for (int y = -4; y <= 4; ++y) {
        int k2 = x * x + y * y;
        if (k2) velocity_l1 += std::abs(rhs[x + 4][y + 4]) / std::sqrt(double(k2));
    }
    double initial_l3 = norm_solver.l3(norm_solver.initial(c));
    return 1.0 + horizon * velocity_l1 / std::max(initial_l3, 1e-30);
}

static Cycle213Options parse_cycle213(int argc, char **argv) {
    Cycle213Options o;
    for (int i = 1; i < argc; ++i) {
        std::string key = argv[i];
        if (i + 1 >= argc) throw std::runtime_error("missing value for " + key);
        std::string value = argv[++i];
        if (key == "--reduced-n") o.reduced_n = std::stoi(value);
        else if (key == "--reduced-steps") o.reduced_steps = std::stoi(value);
        else if (key == "--reduced-time") o.reduced_time = std::stod(value);
        else if (key == "--reduced-keep") o.reduced_keep = std::stoi(value);
        else if (key == "--candidate-keep") o.candidate_keep = std::stoi(value);
        else if (key == "--coarse-n") o.coarse_n = std::stoi(value);
        else if (key == "--coarse-steps") o.coarse_steps = std::stoi(value);
        else if (key == "--fine-n") o.fine_n = std::stoi(value);
        else if (key == "--fine-steps") o.fine_steps = std::stoi(value);
        else if (key == "--fine-keep") o.fine_keep = std::stoi(value);
        else if (key == "--final-time") o.final_time = std::stod(value);
        else if (key == "--threads") o.threads = std::stoi(value);
        else if (key == "--max-active") o.max_active = std::stoi(value);
        else if (key == "--output") o.output = value;
        else throw std::runtime_error("unknown option " + key);
    }
    if (o.threads < 1 || o.reduced_keep < 1 || o.candidate_keep < 1)
        throw std::runtime_error("thread and retention counts must be positive");
    return o;
}

static double pearson(const std::vector<ScreenRow> &rows) {
    double sx = 0.0, sy = 0.0;
    size_t count = 0;
    for (const auto &r : rows) if (r.reduced.finite) {
        sx += r.upper_proxy; sy += r.reduced.maximum; ++count;
    }
    double mx = sx / count, my = sy / count;
    double xx = 0.0, yy = 0.0, xy = 0.0;
    for (const auto &r : rows) if (r.reduced.finite) {
        double x = r.upper_proxy - mx, y = r.reduced.maximum - my;
        xx += x * x; yy += y * y; xy += x * y;
    }
    return xy / std::sqrt(std::max(xx * yy, 1e-300));
}

int main(int argc, char **argv) try {
    Cycle213Options o = parse_cycle213(argc, argv);
    constexpr uint64_t TOTAL = 9765625;
    uint64_t primitive = 0, canonical_count = 0, active = 0;
    std::vector<ScreenRow> rows;
    for (uint64_t code = 1; code < TOTAL; ++code) {
        uint64_t q = code; Coeff c{};
        for (int i = 0; i < 10; ++i) { c[i] = int(q % 5) - 2; q /= 5; }
        if (gcd_coeff(c) != 1) continue;
        ++primitive;
        if (canonical(c) != c) continue;
        ++canonical_count;
        if (!nonlinear(c)) continue;
        ++active;
        rows.push_back({c});
        if (o.max_active && int(rows.size()) >= o.max_active) break;
    }
    std::cerr << "enumerated active rows=" << rows.size() << "\n";

    std::atomic<size_t> next{0}, done{0};
    auto worker = [&]() {
        SpectralSolver reduced(o.reduced_n), proxy_norm(16);
        while (true) {
            size_t i = next.fetch_add(1);
            if (i >= rows.size()) break;
            rows[i].upper_proxy = predictor_upper_proxy(rows[i].c, SCREEN_MUS.back(),
                                                        o.reduced_time, proxy_norm);
            for (double mu : SCREEN_MUS) {
                RunResult run = reduced.run(rows[i].c, mu, o.reduced_steps, o.reduced_time);
                if (run.maximum > rows[i].reduced.maximum) {
                    rows[i].reduced = run;
                    rows[i].reduced_mu = mu;
                }
            }
            size_t count = done.fetch_add(1) + 1;
            if (count % 10000 == 0) std::cerr << "reduced integrated=" << count << "\n";
        }
    };
    std::vector<std::thread> pool;
    for (int i = 0; i < o.threads; ++i) pool.emplace_back(worker);
    for (auto &thread : pool) thread.join();

    double proxy_correlation = pearson(rows);
    std::sort(rows.begin(), rows.end(), [](const ScreenRow &a, const ScreenRow &b) {
        if (a.reduced.finite != b.reduced.finite) return a.reduced.finite > b.reduced.finite;
        return a.reduced.maximum > b.reduced.maximum;
    });
    ScreenRow reduced_best = rows.front();
    if (int(rows.size()) > o.reduced_keep) rows.resize(o.reduced_keep);

    struct Record { Coeff c; double mu; RunResult run; };
    std::vector<Record> coarse;
    SpectralSolver coarse_solver(o.coarse_n);
    int candidate_count = std::min(o.candidate_keep, int(rows.size()));
    for (int i = 0; i < candidate_count; ++i) for (double mu : SCREEN_MUS)
        coarse.push_back({rows[i].c, mu, coarse_solver.run(rows[i].c, mu, o.coarse_steps,
                                                           o.final_time)});
    std::sort(coarse.begin(), coarse.end(), [](const Record &a, const Record &b) {
        if (a.run.finite != b.run.finite) return a.run.finite > b.run.finite;
        return a.run.maximum > b.run.maximum;
    });
    std::vector<Record> fine;
    SpectralSolver fine_solver(o.fine_n);
    for (int i = 0; i < std::min(o.fine_keep, int(coarse.size())); ++i)
        fine.push_back({coarse[i].c, coarse[i].mu,
                        fine_solver.run(coarse[i].c, coarse[i].mu, o.fine_steps, o.final_time)});
    std::sort(fine.begin(), fine.end(), [](const Record &a, const Record &b) {
        if (a.run.finite != b.run.finite) return a.run.finite > b.run.finite;
        return a.run.maximum > b.run.maximum;
    });

    std::ofstream f(o.output);
    f << std::setprecision(17);
    f << "{\n  \"status\": \"FLOATING_FINITE_FAMILY_SCREEN\",\n"
      << "  \"rigorous_interval_certificate\": false,\n"
      << "  \"enumeration\": {\"raw_nonzero\": " << TOTAL - 1
      << ", \"primitive\": " << primitive << ", \"canonical\": " << canonical_count
      << ", \"nonlinear\": " << active << ", \"integrated\": " << done << "},\n"
      << "  \"method\": {\"screen_viscosities\": 7"
      << ", \"reduced_n\": " << o.reduced_n << ", \"reduced_steps_per_unit\": " << o.reduced_steps
      << ", \"reduced_time\": " << o.reduced_time << ", \"reduced_retained\": " << rows.size()
      << ", \"trajectory_candidates\": " << candidate_count << ", \"coarse_n\": " << o.coarse_n
      << ", \"coarse_steps_per_unit\": " << o.coarse_steps << ", \"fine_n\": " << o.fine_n
      << ", \"fine_steps_per_unit\": " << o.fine_steps << "},\n"
      << "  \"proxy\": {\"name\": \"first_order_fourier_l1_upper\", \"pde_bound\": false, "
      << "\"pearson_all_rows\": " << proxy_correlation << "},\n"
      << "  \"reduced_floating_maximum\": {\"coefficients\": " << coeff_json(reduced_best.c)
      << ", \"mu\": " << reduced_best.reduced_mu << ", \"max_ratio\": "
      << reduced_best.reduced.maximum << ", \"max_time\": " << reduced_best.reduced.time << "},\n";
    auto write = [&](const char *name, const std::vector<Record> &records) {
        f << "  \"" << name << "\": [\n";
        for (size_t i = 0; i < records.size(); ++i) {
            const auto &r = records[i];
            f << "    {\"coefficients\": " << coeff_json(r.c) << ", \"mu\": " << r.mu
              << ", \"max_ratio\": " << r.run.maximum << ", \"max_time\": " << r.run.time
              << ", \"finite\": " << (r.run.finite ? "true" : "false") << "}"
              << (i + 1 == records.size() ? "\n" : ",\n");
        }
        f << "  ]";
    };
    write("coarse_ranked", coarse); f << ",\n"; write("fine_reruns", fine);
    const Record &best = fine.empty() ? coarse.front() : fine.front();
    f << ",\n  \"floating_maximum\": {\"coefficients\": " << coeff_json(best.c)
      << ", \"mu\": " << best.mu << ", \"max_ratio\": " << best.run.maximum
      << ", \"max_time\": " << best.run.time << "},\n"
      << "  \"observed_over_two\": " << (best.run.maximum > 2.0 ? "true" : "false") << "\n}\n";
    std::cout << o.output << "\n";
    return 0;
} catch (const std::exception &e) {
    std::cerr << "error: " << e.what() << "\n";
    return 2;
}
