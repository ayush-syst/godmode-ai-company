#!/usr/bin/env bash
# =============================================================================
# Godmode AI Company — Step 1: stack installer (Ubuntu / WSL2)
# -----------------------------------------------------------------------------
# Installs the full agent stack into a Ubuntu environment:
#   - Base toolchain (git, curl, build tools, Python, Node, Bun)
#   - Claude Code CLI            (Layer 1 driver)
#   - gstack                     (Layer 1 — the human-gated spine)
#   - ruflo                      (Layer 2 — swarm meta-harness)
#   - CrewAI + LiteLLM           (Layer 2 crews + the Token Optimizer)
#   - OpenHands, n8n             (Docker-based — pulled, run on demand)
#   - Security scanners          (semgrep, trivy, gitleaks, syft, grype)
#   - Playwright                 (for gstack /qa live-browser checks)
#
# Design goals: idempotent (safe to re-run), explicit (echoes every step),
# honest (skips what it can't safely auto-install and tells you).
#
# Usage:   bash bootstrap/install.sh
#          bash bootstrap/install.sh --minimal   # base + Claude + gstack only
# =============================================================================
set -euo pipefail

MINIMAL=false
[[ "${1:-}" == "--minimal" ]] && MINIMAL=true

# ── pretty output ───────────────────────────────────────────────────────────
c_reset='\033[0m'; c_cyan='\033[36m'; c_green='\033[32m'; c_yellow='\033[33m'; c_gray='\033[90m'
step() { echo -e "\n${c_cyan}=== $* ===${c_reset}"; }
ok()   { echo -e "  ${c_green}[OK]${c_reset} $*"; }
warn() { echo -e "  ${c_yellow}[!]${c_reset}  $*"; }
info() { echo -e "  ${c_gray}-${c_reset}    $*"; }
have() { command -v "$1" >/dev/null 2>&1; }

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
info "Repo root: $REPO_ROOT"

# ── 0. Sanity: are we on Linux? ─────────────────────────────────────────────
step "Environment check"
if [[ "$(uname -s)" != "Linux" ]]; then
  warn "This script targets Linux (WSL2/Ubuntu). On Windows, run bootstrap/0-enable-wsl.ps1 first."
  exit 1
fi
ok "Linux detected: $(uname -sr)"
if grep -qi microsoft /proc/version 2>/dev/null; then ok "Running under WSL."; fi

# ── 1. Base system packages ─────────────────────────────────────────────────
step "Base toolchain (apt)"
sudo apt-get update -y
sudo apt-get install -y \
  curl wget git unzip ca-certificates gnupg build-essential \
  python3 python3-pip python3-venv pipx jq
ok "Base packages installed."

# ── 2. Node.js (LTS) via nvm + Bun (gstack needs Bun) ───────────────────────
step "Node.js + Bun"
export NVM_DIR="$HOME/.nvm"
if [[ ! -d "$NVM_DIR" ]]; then
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
fi
# shellcheck disable=SC1091
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
if ! have node; then nvm install --lts && nvm use --lts; fi
ok "Node: $(node -v 2>/dev/null || echo 'pending shell reload')"

if ! have bun; then
  curl -fsSL https://bun.sh/install | bash
  export BUN_INSTALL="$HOME/.bun"; export PATH="$BUN_INSTALL/bin:$PATH"
fi
ok "Bun: $(bun -v 2>/dev/null || echo 'pending shell reload')"

# ── 3. Claude Code CLI (the Layer-1 driver) ─────────────────────────────────
step "Claude Code CLI"
if ! have claude; then
  npm install -g @anthropic-ai/claude-code
fi
ok "Claude Code: $(claude --version 2>/dev/null || echo 'installed (run: claude)')"
info "You'll authenticate Claude Code on first run with your Anthropic account/sub."

# ── 4. gstack — the human-gated spine (Layer 1) ─────────────────────────────
# gstack ships as Claude Code skills. We clone it and surface its skills.
step "gstack (Layer 1 spine)"
GSTACK_DIR="$HOME/.godmode/gstack"
if [[ ! -d "$GSTACK_DIR" ]]; then
  git clone --depth 1 https://github.com/garrytan/gstack.git "$GSTACK_DIR"
else
  git -C "$GSTACK_DIR" pull --ff-only || warn "Could not update gstack; using existing checkout."
fi
ok "gstack at $GSTACK_DIR"
info "Install its skills per gstack's README (Claude Code skills dir or /plugin)."
info "Skills you'll use: /office-hours /plan-*-review /design-shotgun /review /cso /qa /ship /retro"

if [[ "$MINIMAL" == true ]]; then
  step "Minimal install complete"
  ok "Base + Claude Code + gstack ready. Re-run without --minimal for the full swarm."
  exit 0
fi

# ── 5. Python venv: CrewAI + LiteLLM + replication engine deps ──────────────
step "Python stack (CrewAI + LiteLLM + Langfuse client)"
VENV="$REPO_ROOT/.venv"
[[ -d "$VENV" ]] || python3 -m venv "$VENV"
# shellcheck disable=SC1091
source "$VENV/bin/activate"
pip install --upgrade pip wheel
pip install \
  "crewai[tools]" \
  "litellm[proxy]" \
  langfuse \
  openai \
  python-dotenv \
  pyyaml \
  firecrawl-py
ok "Python stack installed in $VENV"
info "Replication engine deps also covered (see bootstrap/replication-engine/requirements.txt)."

# ── 6. ruflo — the swarm meta-harness (Layer 2) ─────────────────────────────
step "ruflo (Layer 2 swarm)"
# ruflo runs via npx; we warm the cache and print the init command.
npx --yes ruflo@latest --version >/dev/null 2>&1 || warn "ruflo warm-up will complete on first real run."
ok "ruflo available via: npx ruflo@latest init wizard"
info "Or as a Claude Code plugin: /plugin install ruflo-core@ruflo"

# ── 7. Security scanners ────────────────────────────────────────────────────
step "Security scanners (semgrep, trivy, gitleaks, syft, grype)"
have semgrep || pipx install semgrep || pip install semgrep
ok "semgrep: $(semgrep --version 2>/dev/null || echo installed)"

if ! have trivy; then
  curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \
    | sudo sh -s -- -b /usr/local/bin
fi
ok "trivy: $(trivy --version 2>/dev/null | head -n1 || echo installed)"

if ! have gitleaks; then
  GL_VER="$(curl -s https://api.github.com/repos/gitleaks/gitleaks/releases/latest | jq -r .tag_name | tr -d v)"
  curl -sSL "https://github.com/gitleaks/gitleaks/releases/download/v${GL_VER}/gitleaks_${GL_VER}_linux_x64.tar.gz" \
    | sudo tar -xz -C /usr/local/bin gitleaks
fi
ok "gitleaks: $(gitleaks version 2>/dev/null || echo installed)"

if ! have syft;  then curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh  | sudo sh -s -- -b /usr/local/bin; fi
if ! have grype; then curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin; fi
ok "syft + grype installed (SBOM + vuln scanning)."

# ── 8. Playwright (for gstack /qa) ──────────────────────────────────────────
step "Playwright (live-browser QA)"
npx --yes playwright install --with-deps chromium || warn "Playwright deps need 'sudo'; re-run if it failed."
ok "Chromium ready for /qa."

# ── 9. Docker-based services: OpenHands + n8n (pulled, run on demand) ────────
step "Docker services (OpenHands, n8n)"
if have docker; then
  ok "Docker present: $(docker --version)"
  info "Pull OpenHands when needed:  docker pull docker.all-hands.dev/all-hands-ai/openhands:latest"
  info "Run n8n:  docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n"
else
  warn "Docker not reachable from WSL. Install Docker Desktop + enable WSL integration (see step 0)."
  info "OpenHands (heavy-coding worker) and n8n (automation) both need Docker."
fi

# ── 10. Token Optimizer: install the LiteLLM proxy config hint ──────────────
step "Token Optimizer (LiteLLM proxy)"
ok "Config lives at bootstrap/litellm-config.yaml (implements company-os/13-model-router.md)."
info "Start it (after filling .env):  litellm --config bootstrap/litellm-config.yaml"
info "Then point gstack/ruflo/CrewAI at the proxy endpoint (default http://localhost:4000)."

# ── 11. Summary ─────────────────────────────────────────────────────────────
step "Install complete — summary"
ok "Layer 1 driver: Claude Code + gstack"
ok "Layer 2 swarm:  ruflo + CrewAI (+ OpenHands via Docker)"
ok "Token Optimizer: LiteLLM + Langfuse"
ok "Scanners: semgrep, trivy, gitleaks, syft, grype"
echo
info "NEXT:"
info "  1. cp bootstrap/.env.example .env   # then fill in your keys"
info "  2. litellm --config bootstrap/litellm-config.yaml   # start the router"
info "  3. python bootstrap/replication-engine/run.py \"clone a US startup for India\""
info "  4. Follow bootstrap/90-DAY-PLAN.md"
echo
warn "Re-open your shell (or 'source ~/.bashrc') so PATH changes for nvm/bun/pipx take effect."
