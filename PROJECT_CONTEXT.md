# PROJECT_CONTEXT.md — GOD (Godmode AI Company)

> **Purpose of this file:** Self-contained project memory. If you are a fresh Claude chat, read this
> top-to-bottom and you have everything needed to continue without the prior conversation history.
> Keep this file updated at every milestone. Companion files: `CURRENT_TASK.md` (what's happening now),
> `NEXT_STEPS.md` (future work).
> **Last updated:** 2026-06-04

---

## 0. TL;DR

Solo founder (Ayush) is building a **(near) one-person "AI company"** — a system of specialized AI agents
that can discover/validate ideas, build products, design world-class UIs, market, sell, support, secure,
scale, and optimize its own token/credit spend. Philosophy: **assemble the best existing open-source
repos, don't build from scratch.** Deliverable = a **master blueprint document + a runnable bootstrap
kit**. We are currently in the **authoring phase** (writing the blueprint + kit files into this folder).

**Honesty mandate (core to this project):** We build the *realistic* strong version — a semi-autonomous,
human-gated AI product studio that lets one person operate like a 20–50 person company, targeting
**$1M–$10M ARR**, with "billion-dollar / 100 fully-autonomous-agents" as a north star, **not** the base
case. We do not over-promise full autonomy or "unhackable" security.

---

## 1. Current project state

- **Phase:** Authoring the deliverables (blueprint + bootstrap kit). No code has been executed yet.
- **Working directory / project root:** `C:\Users\Ayush\OneDrive\Desktop\GOD\`
- **OS / shell:** Windows 11 Home, PowerShell. **Target runtime for the agent stack = WSL2 / Ubuntu.**
- **Git:** Not a git repo yet (will `git init` during bootstrap).
- **Approved plan file:** `C:\Users\Ayush\.claude\plans\c-users-ayush-downloads-ai-company-blue-fluffy-valley.md`
- **Source prompt:** `C:\Users\Ayush\Downloads\ai_company_blueprint.md` (the user's original 13-part "GODMODE Architect" brief — we keep all 13 parts and merge our own architecture in).

### Files that should exist in the project root (status)
| File | Purpose | Status |
|---|---|---|
| `PROJECT_CONTEXT.md` | This file — permanent knowledge | ✅ created |
| `CURRENT_TASK.md` | What we're doing right now | ✅ created |
| `NEXT_STEPS.md` | Ordered future tasks | ✅ created |
| `LICENSE` | MIT license (open source) | ✅ created |
| `.gitignore` | Excludes secrets/env/local settings | ✅ created |
| `00-MASTER-BLUEPRINT.md` | Full 13-part merged report | ⬜ to write |
| `README.md` | Overview + first 5 commands | ⬜ to write |
| `company-os/` | Obsidian-ready vault (divisions/roles) | ⬜ to write |
| `bootstrap/` | Runnable install + config + replication engine | ⬜ to write |

> When you create/finish any of these, update the table.

---

## 2. Important decisions (LOCKED with the user)

1. **Scope:** Deliver the **blueprint document + a runnable bootstrap kit** (not doc-only, not a full
   product build yet).
2. **Budget / harness:** User has/will get **one ~$20/mo Claude subscription**. Therefore **Claude Code +
   gstack is the human-gated "quality spine"** on the critical path. **Free model tiers power the swarm
   only** — they never touch the critical path. (Free tiers are for *building*, not for serving
   production users at scale.)
3. **First move:** **Run the Startup Replication Engine first** — "clone a successful US startup and build
   the India equivalent." It shortlists candidates, scores TAM/competition/regulation/revenue/difficulty,
   and outputs a ranked pick + build brief. That pick becomes the first product.
4. **Environment:** **WSL2 / Ubuntu** on the Windows 11 PC. Bootstrap targets bash; one PowerShell step
   enables WSL2 + Docker Desktop integration.
5. **Tone/standard:** Architect, not hype man. Brutal reality check is Part 13 of the blueprint and frames
   the whole thing. Quality bar is "the ultimate project" — no compromise on depth/accuracy.

---

## 3. Architecture — the 3-layer "GOD" company

Not a flat swarm of 100 agents. Three layers + cross-cutting services:

```
LAYER 0 — YOU (Founder) + COMPANY BRAIN
  Obsidian vault (decisions/specs/playbooks) ⇄ Cognee/GraphRAG knowledge graph
  ⇄ Mem0 per-agent memory ⇄ ruflo AgentDB (swarm memory) ⇄ Founder Dashboard

LAYER 1 — HUMAN-GATED EXECUTIVE / PRODUCT SPINE  (gstack on Claude)
  /office-hours(CEO) → plan reviews(CTO/CPO/Design) → /design-* → build
  → /review → /cso(security) → /qa → /ship → /retro
  YOU approve at each gate. Quality + taste + cost control live here.

LAYER 2 — AUTONOMOUS SWARM WORKERS  (ruflo + OpenHands + CrewAI)
  Parallel grunt work dispatched by Layer 1: research crews, codegen,
  test-writing, scraping, content drafts, lead lists, dependency audits.
  Sandboxed. Cheap/free models. Output is ALWAYS reviewed by Layer 1.

CROSS-CUTTING SERVICES
  • Token-Credit Optimizer: LiteLLM proxy + OpenRouter; route by task
    difficulty → cheapest capable model; quota-rotate free tiers; prompt +
    semantic caching; budget alerts; Langfuse cost dashboard.
  • Security: Semgrep, Trivy, gitleaks, CodeQL, OWASP ZAP, Dependabot,
    Syft SBOM, sandboxing — wired into gstack /cso + CI.
  • Infra: Docker → Coolify/Dokploy (self-host PaaS) → k3s at scale;
    Supabase + Cloudflare + Vercel free tiers; Grafana/Prometheus/Sentry.
  • Automation glue: n8n (self-hosted) for cron/webhooks/CRM/outreach.
```

**Why this shape:** quality/cost/security live at the human gates (Layer 1); the swarm (Layer 2) does
cheap parallel volume; the brain (Layer 0) makes it compound. Operable by one person. Reliability math is
why we don't trust a flat 100-agent chain (0.95^100 ≈ 0.6% success).

---

## 4. Verified research (June 2026 — so a fresh chat need not re-research)

### Anchor repos (both real, massive, COMPLEMENTARY — not competitors)
- **garrytan/gstack — 107k★, 15.9k forks, MIT.** 23 opinionated **Claude Code skills** = a virtual eng
  team as slash-commands: `/office-hours` (CEO), `/plan-*-review`, `/design-consultation`,
  `/design-shotgun`, `/design-html`, `/design-review`, `/review` (staff eng bug-hunt), `/investigate`,
  `/codex` (OpenAI cross-review), `/cso` (OWASP/STRIDE security), `/qa` (live Chromium), `/benchmark`,
  `/canary`, `/ship`, `/land-and-deploy`, `/document-*`, `/browse`, `/autoplan`, `/retro`, `/pair-agent`.
  Needs Claude Code + ANTHROPIC_API_KEY, Bun, Playwright. Optional Supabase "GBrain" knowledge base.
  **Role = the product-factory workflow + org-chart-as-skills (Layer 1).** Human-driven, gate-by-gate.
- **ruvnet/ruflo — 57.7k★, 6.6k forks, MIT.** The `claude-flow` rebrand. Multi-agent **swarm
  meta-harness**: hierarchical/mesh/adaptive topologies, queen-led consensus (Raft/Byzantine/Gossip),
  HNSW vector memory (**AgentDB**), **SONA** self-learning patterns, RAG, MCP server. Install:
  `npx ruflo@latest init wizard` or Claude Code plugin `/plugin install ruflo-core@ruflo`. Supports
  Claude/OpenAI/Gemini/Cohere/Ollama. **Role = the autonomous swarm engine + persistent memory +
  self-learning (Layer 2).**

### Broader ecosystem (verified star counts)
- **OpenClaw** (openclaw/openclaw) ~250k★ — self-hosted personal-AI runtime + omnichannel router
  (WhatsApp/Telegram/Discord/…), "self-improving" (writes its own skills). **⚠ Became 2026's first major
  AI-agent security crisis.** Use selectively for omnichannel ops/automation, **sandboxed** — NOT the
  trusted core. Living proof that "self-improving autonomous agent" ≠ safe/reliable.
- **OpenHands** ~65k★ (ex-OpenDevin) — autonomous SWE agent in sandboxed Docker (code, tests, PRs). Best
  free heavy-coding worker.
- **MetaGPT** ~50k★ — "Code = SOP(Team)"; software-company-in-a-box (PRD→design→API→code).
- **CrewAI** ~45k★, 5.2M monthly downloads — easiest role-based crews (research/content/ops).
- **AutoGen** ~54k★ — **maintenance-only**, folded into Microsoft Agent Framework. Don't anchor on it.
- **LangGraph** ~13k★ — graph-based, stateful, durable, human-in-the-loop. Use when you need *custom*
  production agents with audit/rollback.

### Memory / "Company Brain" (verified)
- **Mem0** 41k★, 14M downloads, AWS Agent SDK default — best general per-agent memory; cheap. (single
  timeline / current-state).
- **Letta (MemGPT)** — OS-style paging memory; best for long-running "AI employees."
- **Cognee** — GraphRAG + ontology; knowledge-graph *reasoning* over docs/code (traces "why we picked X").
- **Zep** — bi-temporal memory + fact-invalidation; best where facts change (CRM/finance/support).
- **Obsidian** — human-readable vault; the founder's interface + source of truth agents read/write.
- **Recommended stack:** Obsidian (human) + Cognee or GraphRAG (knowledge graph) + Mem0 (agent memory) +
  ruflo AgentDB (swarm memory).

### Free / cheap model APIs (the "no-budget" swarm engine)
| Provider | Free allowance | Best for |
|---|---|---|
| Google AI Studio (Gemini 2.5 Flash) | ~1,500 req/day, 1M ctx, multimodal, no card | High-volume reasoning, long context, vision |
| Groq (Llama 3.3 70B) | 300+ tok/s, ~1,000 req/day (70B), 14,400 (8B) | Fast cheap inference |
| Cerebras | ~60k tok/min, ~1,700 req/day | Highest free throughput |
| DeepSeek | 5M tokens at signup (30-day), then very cheap PAYG | Strong coding/reasoning, low cost |
| Qwen (Alibaba) | 1M tokens/model on signup (90-day) | Coding, multilingual |
| OpenRouter | free models 50–200 req/day; $10 one-time → 1,000 req/day | Aggregation + auto-routing across all |
| SambaNova | free via email | Llama/Qwen access |

**Caveat:** free tiers are rate-limited, trial-expiring, ToS-restricted, some China-hosted (data/privacy
considerations). Great for building; **not** for serving production users at scale → graduate to
paid/self-hosted there. "Free keys forever, no limits" is a fantasy.

### Concrete tool stack (condensed)
- **Harness (LOCKED):** Claude Code + gstack (the gated spine, on the $20 Claude sub).
- **Swarm:** ruflo (primary) + OpenHands (heavy coding) + CrewAI (simple research/content crews).
- **Brain:** Obsidian + Cognee/GraphRAG + Mem0 + ruflo AgentDB.
- **Token Optimizer:** LiteLLM proxy + OpenRouter + Langfuse/Helicone cost observability.
- **Design (anti-generic):** gstack `/design-shotgun` + `/design-consultation`; sources Dribbble/Behance/
  Awwwards/Mobbin/godly.website; libs shadcn/ui, Aceternity, Magic UI, 21st.dev; v0 for generation.
- **Security:** Semgrep + Trivy + gitleaks + CodeQL + OWASP ZAP + Dependabot + Syft SBOM → gstack `/cso` + CI.
- **Infra:** Docker → Coolify/Dokploy → k3s; Supabase + Cloudflare + Vercel free tiers; Grafana/Prometheus/
  Sentry/Uptime-Kuma.
- **Automation glue:** n8n (self-hosted).

---

## 5. Brutal reality check (the calibration — Part 13 of the blueprint)

1. **One-person *billion-dollar* company has never happened.** WhatsApp ~$19B/55 ppl; Instagram $1B/13;
   Midjourney ~tiny team. Solo → **$1M–$10M ARR is real in 2026**; solo → $1B with *zero* humans is not.
2. **"100s of fully autonomous agents, no humans" = slop at scale, not revenue.** Reliability compounds
   badly. What ships products = a few strong agents + human-gated checkpoints (exactly why gstack is
   slash-commands you trigger).
3. **"Self-learning" ≈ persistent memory + retrieval + retrospectives + prompt/skill refinement**, not
   weight-level learning. True self-modifying agents (OpenClaw) are bleeding-edge AND the top cause of
   2026 agent security incidents → sandbox + distrust them.
4. **"Unhackable" doesn't exist.** Aim = hard target + observable + fast incident response.
5. **Real bottlenecks = distribution (customers), taste/judgment (what to build), agent reliability, and
   the founder's own operating capacity.** AI compresses *building*, not *distribution* or *judgment* →
   over-invest there.
6. **Honest probabilities:** $1k–$10k MRR in 6–12 mo ≈ **40–60%**; $1M ARR in 2–3 yr ≈ **10–20%**;
   billion-dollar outcome ≈ **low single digits %**. The same system that wins the small bets buys the
   lottery ticket on the big one.

---

## 6. Open tasks (authoring) — mirror of the task list

1. **Write `00-MASTER-BLUEPRINT.md`** — full 13-part merged report (reality-check first).
2. **Write `company-os/` core files** — `_INDEX`, architecture, company-brain, model-router.
3. **Write `company-os/` division role files** — exec, research, product, engineering, design, marketing,
   sales, customer-success, security, infrastructure, finance/token-optimizer.
4. **Write `bootstrap/`** — `0-enable-wsl.ps1`, `install.sh`, `CLAUDE.md`, `litellm-config.yaml`,
   `.env.example`, `replication-engine/`, `90-DAY-PLAN.md`.
5. **Write top-level `README.md`** — overview + exact first 5 commands.

---

## 7. Future roadmap (post-authoring)

- **90-Day Phase 0 (ship something real):** (1) Stand up WSL2 + Layers 0/1 via bootstrap. (2) **Run the
  Startup Replication Engine** to pick the product. (3) Build that MVP with gstack on Claude → security
  scan → deploy. (4) Get first users/$ before expanding the swarm.
- **5-Year skeleton:** Y1 one profitable product + the core system; Y2 productize the factory across 2–3
  products; Y3 scale infra + paid model tier + first contractor/human; Y4–5 portfolio/platform;
  billion-dollar swing only if a product earns it.

---

## 8. Constraints & operating rules

- **Solo founder, limited budget, free-first**; exactly **one ~$20/mo Claude sub** is the paid anchor.
- **Windows 11 + WSL2/Ubuntu**; agent stack runs in Ubuntu. Use bash for the stack, PowerShell only for
  the WSL/Docker enablement step.
- **gstack/Claude = critical path; free models = swarm only.**
- **Security:** sandbox autonomous/self-modifying agents; never put real secrets in agent-readable files;
  scanners in CI.
- **Honesty over hype**, always. Surface tradeoffs and probabilities.

### Workflow rules the user explicitly asked for (carry these forward)
- **Context-handoff workflow (AUTOMATIC):** Maintain `PROJECT_CONTEXT.md` + `CURRENT_TASK.md` +
  `NEXT_STEPS.md` **automatically — without being asked.** Update them as work progresses and refresh at
  every milestone so the user can **start a fresh chat from `PROJECT_CONTEXT.md`** instead of carrying
  500k tokens of history (~10–20k-token summary is far cheaper). The user typically switches conversations
  at **~50% context-quota used** — proactively refresh and offer a handoff as that approaches.
- **GitHub repo (OPEN SOURCE / PUBLIC):** Public, **MIT-licensed** open-source project at
  https://github.com/ayush-syst/godmode-ai-company. Commit at milestones with clear messages. **No secrets
  are ever committed** — `.env`/keys and `.claude/` local settings are git-ignored (critical now that the
  repo is public). Build the project so others can clone, understand, and fork it (clear README + license).
- **Model-escalation protocol:** **Before starting anything big or difficult, tell the user first and
  recommend which model to use**, then let them switch before you proceed. Opus 4.8 is already the most
  capable model → recommend staying on it (optionally `/fast` off for max deliberation) for
  architecture/security/complex-code; recommend Sonnet 4.6 / Haiku 4.5 for routine/bulk work to conserve
  Opus quota on the $20 plan. (Also stored in persistent memory.)

---

## 9. How to resume in a fresh chat

1. Upload **this file** (`PROJECT_CONTEXT.md`).
2. Read `CURRENT_TASK.md` for the exact in-progress step and `NEXT_STEPS.md` for the queue.
3. Continue the authoring tasks in Section 6, or, if authoring is done, execute the 90-Day plan in
   `bootstrap/90-DAY-PLAN.md`.
4. Honor the workflow rules in Section 8 (handoff updates + model-escalation heads-ups).
