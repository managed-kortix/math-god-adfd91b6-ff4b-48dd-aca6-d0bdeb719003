# Cycle 213: bidirectional high-mode Euler packet screen

## Scope and method

This is floating numerical screening only. It is not an interval enclosure, a
full-PDE certificate, a factor-two falsifier, or a Millennium result.

`cycle213_packet_screen.cpp` extends the Cycle 212 pseudospectral integrator to
general real Fourier streamfunctions and zero-viscosity evolution in both time
directions. Each sample combines a cellular strain with a randomized coherent
packet supported on `2 <= |k|_2 <= kmax`. Packet coefficients have a common
spatial phase, Gaussian phase jitter, and an exponentially tapered spectrum.
The search randomizes packet scale and spectral slope. This moves beyond the
frozen five-frequency integer family and targets perturbations near hyperbolic
stagnation regions.

The Euler nonlinearity is integrated with either sign. At zero viscosity this
is equivalent to forward and backward time screening. The solver uses a
dealiased Fourier pseudospectral convolution and integrating-factor AB2 (whose
factor is one at zero viscosity), with `L^3` sampled every `1/16` time unit.

## Recorded run

The deterministic run

```bash
g++ -O3 -march=native -std=c++20 cycle213_packet_screen.cpp -o cycle213_packet_screen
./cycle213_packet_screen --samples 500 --n 32 --steps 512 \
  --fine-n 64 --fine-steps 1024 --kmax 9 --fine-keep 12 \
  --final-time 3 --seed 213 --output cycle213-packet-screen.json
python3 -m unittest -q test_cycle212_screen.py test_cycle213_packet_screen.py
```

screened 500 packets in both directions. The largest finite fine-grid ratio was
`1.0354217355` at `T=3`, in the positive time direction, with packet seed
`1723589130019637560`, packet scale `0.4770400392`, and spectral slope
`0.2819489630`. No fine rerun exceeded `2.2`.

The coarse and fine rankings are recorded in `cycle213-packet-screen.json`.
This negative result retires only this random distribution, resolution, and
sample budget. The best trajectory peaks at the final time and coarse/fine
values differ, so even its small gain is not a certification candidate.

## Interpretation

The packet screen gives no evidence for the requested high-margin crossing.
Random coherent high modes around a fixed cellular strain mostly preserve the
velocity `L^3` norm over the tested horizon. A stronger continuation should use
a discrete adjoint or automatic differentiation to optimize every retained
Fourier coefficient and terminal time, with conserved energy enforced and
separate resolution reruns before interval work.
