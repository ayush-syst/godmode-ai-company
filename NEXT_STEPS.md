# NEXT_STEPS.md

> The forward queue. Permanent knowledge lives in `PROJECT_CONTEXT.md`; the active step in
> `CURRENT_TASK.md`.
> **Last updated:** 2026-06-13

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

## B. Stand up the system (Phase 0, after authoring) — ✅ WEEK 1 COMPLETE (2026-06-13)
- [x] WSL2 + Ubuntu 26.04 installed
- [x] Claude Code 2.1.172 installed + authenticated
- [x] gstack installed + `/office-hours` working
- [x] LiteLLM proxy running on :4000 (`litellm-config-simple.yaml`; DATABASE_URL commented out in .env)
- [x] Replication Engine demo verified (CreatorKit 81/95)
- [x] Add free API key (Gemini) to `.env` → run engine live (Week 2, 2026-06-13)
- [ ] Install Docker Desktop + enable WSL integration (needed for OpenHands/n8n later)

## C. Pick & build the first product — ✅ PICKED (2026-06-13)
- [x] Run the **Startup Replication Engine** live → ranked shortlist + build briefs
      (`brain/research/2026-06-13-replication-engine-shortlist.md`)
- [x] Founder picks the winner → **GST Bill Assistant** (own repo, AGPL-3.0), *not* the engine's
      greenfield pick (BillKaro, now a backlog/feeder idea).
      Decision Record: `brain/decisions/2026-06-13-first-product-gst-bill-assistant.md`
- [ ] **Drive it to launch** — `products/gst-bill-assistant/LAUNCH-PLAN.md`:
      - [ ] Phase A: firsthand code read + harden GSTR-2B reconciliation (`/review`, `/qa`, `npm test`)
      - [ ] Phase B: backend + metered AI via the proxy; opt-in cloud sync/team accounts (`/plan-eng-review`)
      - [ ] Phase C: 🔴 DPDP security posture + scan (`/cso` — critical/high block launch)
      - [ ] Phase D: deploy (`/ship` → `/canary`) + analytics/Uptime-Kuma/Sentry
- [ ] GTM (parallel, from Day 1): recruit 3–5 small CA-firm design partners → paid pilot → **first dollar**

## D. Compounding (post-first-product)
- [ ] Populate the Company Brain (Obsidian + Cognee) with decisions/specs/retros
- [ ] Add marketing/sales swarm flows (SEO/content/outreach via n8n + CrewAI)
- [ ] Harden security baseline; turn scanners into CI gates
- [ ] Only then expand the agent org toward the full org chart

## Open questions to revisit later (not blocking)
- Which specific US startup category to clone first? (Decide via the Replication Engine output.)
- Self-host vs. managed for production serving once there's traction (cost vs. ops).
- When to introduce the first human contractor (per 5-year roadmap, ~Y3).
