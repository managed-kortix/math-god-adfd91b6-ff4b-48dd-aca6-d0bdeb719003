#define main cycle212_embedded_main
#include "cycle212_screen.cpp"
#undef main

#include <random>

struct PacketOptions {
    int samples = 240;
    int n = 32;
    int steps = 256;
    int fine_n = 64;
    int fine_steps = 512;
    int kmax = 9;
    int fine_keep = 8;
    double final_time = 3.0;
    uint64_t seed = 213;
    std::string output = "cycle213-packet-screen.json";
};

struct PacketResult {
    uint64_t seed;
    double packet_scale;
    double slope;
    int direction;
    RunResult run;
    std::vector<FourierPsiMode> modes;
};

static PacketOptions packet_options(int argc, char **argv) {
    PacketOptions o;
    for (int i = 1; i < argc; ++i) {
        if (i + 1 >= argc) throw std::runtime_error("missing option value");
        std::string key = argv[i], value = argv[++i];
        if (key == "--samples") o.samples = std::stoi(value);
        else if (key == "--n") o.n = std::stoi(value);
        else if (key == "--steps") o.steps = std::stoi(value);
        else if (key == "--fine-n") o.fine_n = std::stoi(value);
        else if (key == "--fine-steps") o.fine_steps = std::stoi(value);
        else if (key == "--kmax") o.kmax = std::stoi(value);
        else if (key == "--fine-keep") o.fine_keep = std::stoi(value);
        else if (key == "--final-time") o.final_time = std::stod(value);
        else if (key == "--seed") o.seed = std::stoull(value);
        else if (key == "--output") o.output = value;
        else throw std::runtime_error("unknown option " + key);
    }
    return o;
}

static std::vector<FourierPsiMode> make_packet(uint64_t seed, int kmax,
                                                double scale, double slope) {
    std::mt19937_64 rng(seed);
    std::normal_distribution<double> normal;
    std::uniform_real_distribution<double> phase(-PI, PI);
    std::vector<FourierPsiMode> modes;

    // A stationary cellular strain supplies hyperbolic points. The broadband
    // perturbation is localized there by a common phase plus randomized jitter.
    modes.push_back({1, 1, Complex(0.0, -0.25)});
    modes.push_back({1, -1, Complex(0.0, 0.25)});
    double x0 = phase(rng), y0 = phase(rng);
    for (int kx = 0; kx <= kmax; ++kx) for (int ky = -kmax; ky <= kmax; ++ky) {
        if (kx == 0 && ky <= 0) continue;
        int k2 = kx * kx + ky * ky;
        if (k2 < 4 || k2 > kmax * kmax) continue;
        double k = std::sqrt(double(k2));
        double envelope = scale * std::exp(-slope * k) / std::max(k2, 1);
        double coherent = -(kx * x0 + ky * y0);
        double jitter = 0.42 * normal(rng);
        double amplitude = envelope * (0.35 + std::abs(normal(rng)));
        modes.push_back({kx, ky, std::polar(amplitude, coherent + jitter)});
    }
    return modes;
}

static double score(const RunResult &run) {
    return run.finite ? run.maximum : 0.0;
}

int main(int argc, char **argv) try {
    PacketOptions o = packet_options(argc, argv);
    if (o.kmax >= o.n / 3 || o.kmax >= o.fine_n / 3)
        throw std::runtime_error("kmax must be below both dealiased cutoffs");
    SpectralSolver coarse(o.n);
    std::mt19937_64 rng(o.seed);
    std::uniform_real_distribution<double> log_scale(std::log(0.02), std::log(0.65));
    std::uniform_real_distribution<double> slopes(0.04, 0.30);
    std::vector<PacketResult> ranked;
    for (int sample = 0; sample < o.samples; ++sample) {
        uint64_t packet_seed = rng();
        double scale = std::exp(log_scale(rng)), slope = slopes(rng);
        auto modes = make_packet(packet_seed, o.kmax, scale, slope);
        for (int direction : {-1, 1}) {
            auto initial = coarse.initial(modes);
            RunResult run = coarse.run(std::move(initial), 0.0, o.steps,
                                       o.final_time, double(direction));
            ranked.push_back({packet_seed, scale, slope, direction, run, modes});
        }
    }
    std::sort(ranked.begin(), ranked.end(), [](const auto &a, const auto &b) {
        return score(a.run) > score(b.run);
    });

    SpectralSolver fine(o.fine_n);
    std::vector<PacketResult> reruns;
    for (int i = 0; i < std::min(o.fine_keep, int(ranked.size())); ++i) {
        PacketResult r = ranked[i];
        r.run = fine.run(fine.initial(r.modes), 0.0, o.fine_steps,
                         o.final_time, double(r.direction));
        reruns.push_back(std::move(r));
    }
    std::sort(reruns.begin(), reruns.end(), [](const auto &a, const auto &b) {
        return score(a.run) > score(b.run);
    });

    std::ofstream f(o.output);
    f << std::setprecision(17);
    f << "{\n  \"status\": \"NUMERICS_SCREENING_ONLY\",\n"
      << "  \"rigorous_interval_certificate\": false,\n"
      << "  \"method\": {\"family\": \"random_high_mode_hyperbolic_packets\", "
      << "\"samples\": " << o.samples << ", \"directions\": 2, \"seed\": " << o.seed
      << ", \"kmax\": " << o.kmax << ", \"coarse_n\": " << o.n
      << ", \"coarse_steps_per_unit\": " << o.steps << ", \"fine_n\": " << o.fine_n
      << ", \"fine_steps_per_unit\": " << o.fine_steps << "},\n";
    auto write = [&](const char *name, const std::vector<PacketResult> &v, int count) {
        f << "  \"" << name << "\": [\n";
        count = std::min(count, int(v.size()));
        for (int i = 0; i < count; ++i) {
            const auto &r = v[i];
            f << "    {\"packet_seed\": " << r.seed << ", \"packet_scale\": "
              << r.packet_scale << ", \"spectral_slope\": " << r.slope
              << ", \"time_direction\": " << r.direction << ", \"max_ratio\": "
              << r.run.maximum << ", \"max_time\": " << r.run.time
              << ", \"finite\": " << (r.run.finite ? "true" : "false") << "}"
              << (i + 1 == count ? "\n" : ",\n");
        }
        f << "  ]";
    };
    write("coarse_ranked", ranked, 16); f << ",\n";
    write("fine_reruns", reruns, int(reruns.size()));
    double best = reruns.empty() ? score(ranked.front().run) : score(reruns.front().run);
    f << ",\n  \"best_fine_ratio\": " << best
      << ",\n  \"observed_over_2_2\": " << (best > 2.2 ? "true" : "false") << "\n}\n";
    std::cout << o.output << " best=" << best << "\n";
    return 0;
} catch (const std::exception &e) {
    std::cerr << "error: " << e.what() << "\n";
    return 2;
}
