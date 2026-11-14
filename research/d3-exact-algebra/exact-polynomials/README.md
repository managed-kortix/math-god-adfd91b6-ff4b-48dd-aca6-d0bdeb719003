# D3 exact polynomial export

Normalization: `Psi_G(z)=i^{-|V(G)|} det(i diag(z)-A(G))=R_G(z)+i I_G(z)`.

Each record has complete `R_raw`, `I_raw`, `R_activity`, and `I_activity`, with `z_v=t+y_v`, `t>0`, `y_v>=0`; no coefficient is omitted. `manifest.json` records counts and per-record SHA-256 hashes. Regenerate with `../export_exact_polynomials.py`; cross-check with the independent determinant and compact-formula checkers.
