#!/usr/bin/env bash
# math-god harness bootstrap — idempotent, safe to re-run on every resurrection.
# Installs the computational math stack + x-cli into the session sandbox.
set -euo pipefail

log() { echo "[setup-harness] $*"; }

# ── Python math env ───────────────────────────────────────────────────────────
if [ ! -x "$HOME/mathenv/bin/python" ]; then
  log "creating ~/mathenv venv"
  python3 -m venv "$HOME/mathenv"
fi
"$HOME/mathenv/bin/pip" install --quiet --upgrade sympy numpy mpmath
log "python env ok: $("$HOME/mathenv/bin/python" -c 'import sympy; print("sympy", sympy.__version__)')"

# ── PARI/GP (independent exact-arithmetic engine) ────────────────────────────
if ! command -v gp >/dev/null 2>&1; then
  log "installing pari-gp"
  if command -v apt-get >/dev/null 2>&1; then
    (sudo apt-get update -qq && sudo apt-get install -y -qq pari-gp) \
      || (apt-get update -qq && apt-get install -y -qq pari-gp) \
      || log "WARN: pari-gp install failed — continue without it"
  fi
fi
command -v gp >/dev/null 2>&1 && log "pari-gp ok: $(gp --version 2>&1 | head -1)"

# ── uv + x-cli (X/Twitter posting) ───────────────────────────────────────────
if ! command -v uv >/dev/null 2>&1; then
  log "installing uv"
  curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null
  export PATH="$HOME/.local/bin:$PATH"
fi
if ! command -v x-cli >/dev/null 2>&1 && ! "$HOME/.local/bin/x-cli" --help >/dev/null 2>&1; then
  log "installing x-cli"
  uv tool install x-cli >/dev/null 2>&1 \
    || uv tool install git+https://github.com/Infatoshi/x-cli >/dev/null \
    || log "WARN: x-cli install failed"
fi

# make sure uv tools (x-cli) are on PATH in every future shell
export PATH="$HOME/.local/bin:$PATH"
grep -qs 'HOME/.local/bin' "$HOME/.bashrc" 2>/dev/null \
  || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"

# x-cli config from the Kortix-injected TWITTER_* secrets
mkdir -p "$HOME/.config/x-cli"
if [ -n "${TWITTER_CONSUMER_KEY:-}" ]; then
  umask 077
  cat > "$HOME/.config/x-cli/.env" <<EOF
X_API_KEY=${TWITTER_CONSUMER_KEY}
X_API_SECRET=${TWITTER_CONSUMER_SECRET}
X_BEARER_TOKEN=${TWITTER_BEARER_TOKEN}
X_ACCESS_TOKEN=${TWITTER_ACCESS_TOKEN}
X_ACCESS_TOKEN_SECRET=${TWITTER_ACCESS_TOKEN_SECRET}
EOF
  log "x-cli configured from TWITTER_* env"
else
  log "WARN: TWITTER_CONSUMER_KEY not in env — x-cli NOT configured"
fi

# ── Lean 4 (elan) — on-demand heavy tool, best-effort ────────────────────────
if [ ! -x "$HOME/.elan/bin/lean" ]; then
  log "installing elan (Lean toolchain manager) — best effort"
  curl -sSf https://elan.lean-lang.org/elan-init.sh | sh -s -- -y --default-toolchain none >/dev/null 2>&1 \
    || log "WARN: elan install failed — install later if a formalization is needed"
fi

log "harness ready"
