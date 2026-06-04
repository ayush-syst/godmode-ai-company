# NEXT_STEPS.md

> The forward queue. Permanent knowledge lives in `PROJECT_CONTEXT.md`; the active step in
> `CURRENT_TASK.md`.
> **Last updated:** 2026-06-04

## A. Finish authoring — ✅ COMPLETE (all pushed)
- [x] `00-MASTER-BLUEPRINT.md` (13 parts)
- [x] `README.md`
- [x] `company-os/` **core** (`_INDEX`, `00-architecture`, `12-company-brain`, `13-model-router`)
- [x] `company-os/` **division files** (`01-executive` … `11-finance-token-optimizer`) — all 11 complete
- [x] `bootstrap/` scripts + configs: `0-enable-wsl.ps1`, `install.sh`, `CLAUDE.md`, `litellm-config.yaml`, `.env.example`
- [x] `bootstrap/replication-engine/` (CrewAI Python crew + `run.py`) + `bootstrap/90-DAY-PLAN.md` — **demo verified**
- [x] Milestone checkpoint: handoff docs refreshed; fresh chat offered

> **➡️ The forward queue now starts at Section B (stand up the system). This is the live next step.**
- [ ] Milestone checkpoint: refresh handoff docs, offer fresh chat

## B. Stand up the system (Phase 0, after authoring) — runs in WSL2/Ubuntu
- [ ] Run `bootstrap/0-enable-wsl.ps1` in PowerShell (enable WSL2 + Docker Desktop integration)
- [ ] In Ubuntu: run `bootstrap/install.sh` (Claude Code + gstack + ruflo + OpenHands + CrewAI + n8n + scanners)
- [ ] Add API keys to `.env` (Claude sub key; free tiers: Gemini, Groq, Cerebras, DeepSeek, Qwen, OpenRouter)
- [ ] Start LiteLLM proxy with `litellm-config.yaml`; confirm the Token Optimizer routes + reports cost
- [ ] Smoke test: a "hello-swarm" ruflo task runs end-to-end on free models; a gstack `/office-hours` runs on Claude

## C. Pick & build the first product
- [ ] Run the **Startup Replication Engine** → get ranked US-startup-for-India shortlist + build brief
- [ ] Founder picks the winner
- [ ] gstack flow: `/office-hours` → plan reviews → `/design-shotgun` → build (swarm assists) → `/review`
      → `/cso` (security) → `/qa` → `/ship` → deploy (Coolify/Vercel) → `/retro`
- [ ] Wire basic analytics + Uptime-Kuma + Sentry
- [ ] Get first users / first dollar

## D. Compounding (post-first-product)
- [ ] Populate the Company Brain (Obsidian + Cognee) with decisions/specs/retros
- [ ] Add marketing/sales swarm flows (SEO/content/outreach via n8n + CrewAI)
- [ ] Harden security baseline; turn scanners into CI gates
- [ ] Only then expand the agent org toward the full org chart

## Open questions to revisit later (not blocking)
- Which specific US startup category to clone first? (Decide via the Replication Engine output.)
- Self-host vs. managed for production serving once there's traction (cost vs. ops).
- When to introduce the first human contractor (per 5-year roadmap, ~Y3).
