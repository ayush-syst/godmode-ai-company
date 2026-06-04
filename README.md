<div align="center">

# 🦾 Godmode AI Company

### An open-source blueprint + buildable kit for running a software company as a (near) one-person, agent-operated org.

*Assembled from the best existing open-source projects — not built from scratch.*

`gstack` (human-gated spine) · `ruflo` (autonomous swarm) · free-model routing · startup-replication engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Status](https://img.shields.io/badge/status-building-orange)
![Built for](https://img.shields.io/badge/built%20for-solo%20founders-blue)

</div>

---

## What is this?

A complete, **honest** system for operating a software company where most roles are performed by AI
agents, designed for a **solo founder on a ~$20/month budget**. It is two things:

1. **A master blueprint** ([`00-MASTER-BLUEPRINT.md`](00-MASTER-BLUEPRINT.md)) — a 13-part plan covering
   vision, the open-source ecosystem (ranked), the agent org chart, memory, model routing, the product
   factory, security, infrastructure, a 5-year roadmap, and a no-BS reality check.
2. **A runnable bootstrap kit** (`bootstrap/`) — scripts + configs that stand the system up on your
   machine, plus a **Startup Replication Engine** that picks your first product.

> ⚠️ **This is not "100 autonomous agents will make you a billionaire."** It's the realistic, strong
> version: a **semi-autonomous, human-gated product studio** that lets one person operate like a 20–50
> person company and credibly target **$1M–$10M ARR**. Read [Part 13 — Reality Check](00-MASTER-BLUEPRINT.md#part-13--brutal-reality-check-read-this-one) first.

## The core idea: 3 layers, not a flat swarm

```
LAYER 0  YOU + COMPANY BRAIN      Obsidian vault ⇄ Cognee/GraphRAG ⇄ Mem0 ⇄ ruflo AgentDB
LAYER 1  HUMAN-GATED SPINE        gstack on Claude: /office-hours → design → review → /cso → /qa → /ship
LAYER 2  AUTONOMOUS SWARM         ruflo + OpenHands + CrewAI: research, codegen, tests, content, leads
SERVICES Token Optimizer (LiteLLM) · Security scanners · Infra/CI · n8n automation
```

**Why:** quality, cost, and security live at the **human gates** (Layer 1); the **swarm** (Layer 2) does
cheap parallel volume on free models; the **brain** (Layer 0) makes it compound. A flat chain of 100
autonomous agents fails multiplicatively (0.95¹⁰⁰ ≈ 0.6%). Gates are the point.

## The stack (all open source unless noted)

| Concern | Tool |
|---|---|
| Human-gated spine | **gstack** (107k⭐) on Claude Code |
| Autonomous swarm | **ruflo** (57.7k⭐) + **OpenHands** + **CrewAI** |
| Company brain / memory | Obsidian + **Cognee**/GraphRAG + **Mem0** + ruflo AgentDB |
| Model routing / cost | **LiteLLM** + OpenRouter + **Langfuse** |
| Free model engine | Gemini Flash · Groq · Cerebras · DeepSeek · Qwen |
| Design (anti-generic) | gstack `/design-shotgun` + shadcn/Aceternity/Magic UI + Mobbin/Awwwards |
| Security | Semgrep · Trivy · gitleaks · CodeQL · OWASP ZAP · Syft |
| Infra | Docker → **Coolify**/Dokploy → k3s · Supabase · Cloudflare |
| Automation glue | **n8n** |

## Quick start

> 🚧 **Status:** the blueprint is complete; the `bootstrap/` kit is being built (see [Roadmap](#project-status--roadmap)).
> Target environment is **WSL2 / Ubuntu** on Windows (or any Linux/macOS).

```bash
# 1. (Windows only) enable WSL2 + Docker — run in PowerShell
./bootstrap/0-enable-wsl.ps1

# 2. In Ubuntu: install the stack (gstack, ruflo, OpenHands, CrewAI, n8n, scanners)
./bootstrap/install.sh

# 3. Add your keys (Claude sub + free tiers) and start the Token-Optimizer
cp bootstrap/.env.example .env   # then edit .env
litellm --config bootstrap/litellm-config.yaml

# 4. Pick your first product
python bootstrap/replication-engine/run.py "clone a US startup for India"

# 5. Build it with gstack → ship → get users (follow bootstrap/90-DAY-PLAN.md)
```

## Repository structure

```
GOD/
├── 00-MASTER-BLUEPRINT.md     # The full 13-part plan (start here)
├── company-os/                # Operational specs: one file per division/role  🚧
├── bootstrap/                 # Runnable kit: install, configs, replication engine  🚧
├── PROJECT_CONTEXT.md         # Self-contained project memory (for fresh-chat handoff)
├── CURRENT_TASK.md            # What's being worked on now
├── NEXT_STEPS.md              # The forward queue
├── LICENSE                    # MIT
└── README.md                  # You are here
```

## Project status / roadmap

- [x] Master blueprint (13 parts + reality check)
- [x] Open-source repo + MIT license + context-handoff system
- [ ] `company-os/` — division/role operational specs
- [ ] `bootstrap/` — WSL enable, install script, `CLAUDE.md`, LiteLLM token-optimizer config
- [ ] `bootstrap/replication-engine/` — the clone-a-US-startup-for-India workflow
- [ ] `bootstrap/90-DAY-PLAN.md` — the execution checklist

## Philosophy

- **Leverage, don't reinvent.** Every component is a battle-tested open-source project.
- **Human gates over blind autonomy.** Taste and quality are the moat; agents are the horsepower.
- **Free for building, paid for serving.** Free model tiers power development; production gets real SLAs.
- **Honesty over hype.** Probabilities are stated. The reality check is Part 13, not a footnote.

## ⚠️ Disclaimers

- Third-party star counts, free-tier limits, and model capabilities are **verified as of June 2026** and
  change frequently — re-verify before relying on them.
- Free API tiers have rate limits and Terms of Service; some are China-hosted (data/privacy
  considerations). They are for **building**, not for serving production users at scale.
- "Self-improving" autonomous agents are a known security risk (see the OpenClaw incident in Part 9).
  **Sandbox them; never give them production secrets.**
- This repo contains **no secrets** by design (`.env` and keys are git-ignored). Keep it that way.

## License

[MIT](LICENSE) © 2026 Ayush ([@ayush-syst](https://github.com/ayush-syst)). Use it, fork it, build with it.

---

<div align="center"><i>Build for the realistic win. Treat godmode as the upside, not the plan.</i></div>
