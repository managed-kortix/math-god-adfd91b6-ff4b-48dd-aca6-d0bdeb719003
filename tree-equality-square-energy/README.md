# Equality in positive square energy

This folder contains a self-contained proof of the theorem:

> If `G` is a connected graph on `n` vertices, then `s+(G) = n - 1` if and
> only if `G` is a tree.

Files:

- `paper.tex` - publication-style LaTeX manuscript.
- `README.md` - this overview and build instruction.

Build from the repository root with:

```sh
bash scripts/build-paper.sh tree-equality-square-energy
```

The manuscript cites Liu--Tang--Zhang (arXiv:2607.18031) for the doubly
nonnegative inequality and Akbari--Kumar--Mohar--Pragada--Zhang
(arXiv:2506.07264) for the equality conjecture.
