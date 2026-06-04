# 00 — MASTER BLUEPRINT

### The Godmode AI Company: a realistic plan for a (near) one-person, agent-run company

> **What this is:** an open-source blueprint + buildable system for operating a software company as a
> solo founder, using AI agents for most roles — assembled from the best existing open-source projects
> rather than built from scratch.
>
> **How to read it:** Part 13 (the Reality Check) is the most important section — read it first if you
> only read one. The rest is the build. Tables are rankings; ⭐ counts are verified as of **June 2026**.
>
> **The one-sentence thesis:** Don't build a flat swarm of 100 autonomous agents. Build a **3-layer
> company** — *you + a Company Brain* (Layer 0), a *human-gated executive/product spine* powered by
> **gstack on Claude** (Layer 1), and an *autonomous swarm of cheap workers* powered by **ruflo + OpenHands**
> (Layer 2) — and point it first at **cloning a proven US startup for India**.

---

## Table of contents
1. Vision analysis — can one person build a billion-dollar company?
2. Open-source ecosystem research (rankings + Ruflo vs GStack vs the field)
3. The agent org chart (3 layers, every division)
4. Agent communication architecture
5. The Company Brain (unified memory)
6. AI model strategy & routing (free → cheap → premium)
7. The Product Factory workflow (idea → scale)
8. The Startup Replication Engine (clone-a-US-startup-for-India)
9. Security blueprint
10. Infrastructure blueprint (MVP → million users)
11. The Founder Dashboard
12. Five-year roadmap
13. **Brutal reality check** (read this)
- Appendix A: immediate next actions · Appendix B: repo index · Appendix C: sources

---

## PART 1 — Vision Analysis

**The question:** can a one-person company reach a billion-dollar valuation, run mostly by AI agents?

**Honest answer:** *Mostly by agents* — increasingly yes. *Literally one human, zero employees, $1B* —
not yet, and pretending otherwise will cause you to build the wrong system. Calibrate to the evidence:

| Company | People | Outcome | Lesson |
|---|---|---|---|
| WhatsApp | ~55 | $19B acquisition | Tiny teams *can* reach huge value — but not 1 person |
| Instagram | 13 | $1B acquisition | Distribution + timing > headcount |
| Midjourney | ~tiny | ~$200M+/yr, profitable, no VC | Solo-ish + AI-native + a hit product = real money |
| Telegram | ~30 core | ~$30B+ valuations | Lean infra teams scale to hundreds of millions of users |
| Solo SaaS (many) | 1 | $1M–$10M ARR | **This is the realistic, repeatable target in 2026** |

**What changed by 2026 (the tailwinds):**
- Coding is ~80% compressible by agents (OpenHands, Claude Code, gstack) — building is no longer the bottleneck.
- Frontier-grade reasoning is available cheaply or free (DeepSeek, Qwen, Gemini Flash, Groq).
- Distribution primitives (SEO, short-form video, programmatic outreach) are partially automatable.
- Open-source has *already built* the hard parts: orchestration, memory, swarms, security tooling.

**The limitations (the headwinds) — these define the real design constraints:**
- **Distribution doesn't automate well.** Getting customers still needs judgment, taste, trust, and often a human face.
- **Reliability compounds badly.** Agent chains degrade multiplicatively; full autonomy at scale = quiet failure.
- **Taste/judgment is the moat.** *What* to build and *whether it's good* is still human-led.
- **Trust & liability.** Customers, payments, and security incidents land on a human.

**The opportunity (where a solo founder wins):** small, focused, well-designed products in underserved
markets (e.g., India-localized versions of proven US SaaS), shipped fast, marketed with AI leverage,
operated by a small agent org. Target **$1M–$10M ARR per product**, run a **portfolio**, and treat
"billion-dollar" as a low-probability upside that the *same system* gives you a free option on.

**Verdict:** Build for the realistic win; keep the moonshot as a north star. The architecture in this
document is designed to make the $10k–$1M ARR path likely and the $1B path *possible*.

---

## PART 2 — Open-Source Ecosystem Research

Ranked by usefulness **to this specific goal** (solo founder, $20/mo budget, free-first, ship products).
Stars verified June 2026.

### 2.1 Your two anchors — and why they're complementary, not competing

| | **garrytan/gstack** | **ruvnet/ruflo** |
|---|---|---|
| Stars | **107k ⭐** (15.9k forks) | **57.7k ⭐** (6.6k forks) |
| What it is | 23 opinionated **Claude Code skills** = a virtual eng team as slash-commands | The `claude-flow` rebrand: a multi-agent **swarm meta-harness** |
| Model | **Human-gated** — *you* run a command at each stage | **Autonomous swarm** — topologies, consensus, self-organizing |
| Killer features | `/office-hours` (CEO interrogation), `/design-shotgun` (anti-generic UI), `/cso` (OWASP/STRIDE), `/qa` (live Chromium), `/ship`, `/retro` | HNSW vector memory (AgentDB), SONA self-learning, RAG, MCP server, queen-led consensus |
| Needs | Claude Code + Anthropic key, Bun, Playwright; optional Supabase "GBrain" | `npx ruflo@latest init`; Claude/OpenAI/Gemini/Cohere/**Ollama** |
| License | MIT | MIT |
| **Role here** | **Layer 1 — the quality spine** (org-chart-as-skills, product factory) | **Layer 2 — the horsepower** (parallel grunt work + persistent memory + self-learning) |

> **Decision: use BOTH, as layers.** gstack gives you *gate-by-gate quality and taste*; ruflo gives you
> *cheap parallel volume and memory*. They are not alternatives — gstack is how *you* drive, ruflo is the
> engine room. This single insight reframes the entire build.

### 2.2 Orchestration / swarm / autonomous agents

| Repo | ⭐ | Purpose | Pros | Cons | Use? |
|---|---|---|---|---|---|
| **ruvnet/ruflo** | 57.7k | Swarm meta-harness for Claude | Memory + self-learning + MCP; built for Claude Code | Heavy; can over-engineer simple tasks | ✅ **Core (Layer 2)** |
| **OpenHands** | 65k | Autonomous SWE agent (sandboxed Docker) | Writes code, runs tests, opens PRs; free-model friendly | Needs Docker; supervise it | ✅ **Heavy-coding worker** |
| **MetaGPT** | 50k | "Code = SOP(Team)"; software-company-in-a-box | Great PRD→design→API→code SOPs | Rigid; older patterns | 🟡 Mine its SOPs/prompts |
| **CrewAI** | 45k | Role-based agent crews | Easiest multi-agent; huge community | Less control for prod | ✅ **Research/content/ops crews** |
| **LangGraph** | 13k | Graph-based stateful agents | Durable, auditable, human-in-loop | More code to write | ✅ **When you need custom prod agents** |
| **AutoGen** | 54k | Conversation framework (MS) | Mature | **Maintenance-only**, folded into MS Agent Framework | ❌ Don't anchor |
| **OpenClaw** | ~250k | Self-hosted personal-AI + omnichannel router | Omnichannel (WhatsApp/TG/Discord), "self-improving" | **Caused 2026's first major agent security crisis** | 🟥 Sandbox-only, ops/notifications |

### 2.3 Memory / knowledge ("Company Brain")

| Repo | ⭐ | Best at | Use? |
|---|---|---|---|
| **Mem0** | 41k | General per-agent memory (AWS Agent SDK default); cheap | ✅ Agent working memory |
| **Cognee** | — | GraphRAG + ontology; reasoning over docs/code | ✅ Knowledge graph / "why did we decide X" |
| **Letta (MemGPT)** | — | OS-style paging memory for long-running "AI employees" | 🟡 For persistent agent personas |
| **Zep** | — | Bi-temporal memory + fact invalidation | 🟡 CRM/finance/support where facts change |
| **Obsidian** (app) | — | Human-readable vault; your interface + source of truth | ✅ The founder's brain & the agents' shared docs |
| **Microsoft GraphRAG** | — | Graph extraction over a corpus | 🟡 Alt to Cognee |

### 2.4 Coding agents / harnesses
Claude Code (+ **gstack**) = your driver. OpenHands = autonomous worker. **aider**, **Cline**, **OpenClaw/OpenCode** = alternates if you ever drop the Claude sub.

### 2.5 Browser / research / automation
- **browser-use** — agents drive a real browser (research, scraping, QA). gstack `/browse` + `/qa` wrap Chromium already.
- **n8n** (self-hosted) — the automation glue: cron, webhooks, CRM, outreach, connecting agents to the world.
- **Firecrawl / Crawl4AI** — clean web→markdown for research crews.

### 2.6 Design (anti-generic UI)
- gstack `/design-shotgun` (variant explosion) + `/design-consultation` (design system).
- Component libraries: **shadcn/ui**, **Aceternity UI**, **Magic UI**, **21st.dev**, **tweakcn** (themes).
- Inspiration sources the agents should scrape: Dribbble, Behance, **Awwwards**, **Mobbin** (real app UIs), **godly.website**, **land-book**.
- **v0** for generation; **Motion (Framer Motion)** / **GSAP** for the "wow" animation layer.

### 2.7 Security
Semgrep (SAST), Trivy (containers/IaC), gitleaks (secrets), CodeQL, OWASP ZAP (DAST), Dependabot/Renovate (deps), Syft+Grype (SBOM/vulns), Sigstore (supply chain). gstack `/cso` orchestrates much of this.

### 2.8 Infra / deploy
Docker → **Coolify** or **Dokploy** (open-source self-host PaaS, your Heroku/Vercel replacement) → **k3s** at scale. **Supabase** (DB/auth/storage), **Cloudflare** (CDN/WAF/tunnels), **Grafana+Prometheus**, **Sentry**, **Uptime-Kuma**.

---

## PART 3 — The Agent Org Chart

**The overlay first (this is the key mental model):**

```
LAYER 0  YOU (Founder) + COMPANY BRAIN  ── set direction, approve gates, own taste
LAYER 1  HUMAN-GATED SPINE (gstack/Claude) ── exec, product, design, review, security, QA, ship
LAYER 2  AUTONOMOUS SWARM (ruflo/OpenHands/CrewAI) ── research, codegen, tests, content, leads
SERVICES Token Optimizer · Security scanners · Infra/CI · n8n automation · The Brain
```

Every "agent" below is a **role**, implemented as either a **gstack skill** (Layer 1, you trigger it) or a
**ruflo/CrewAI worker** (Layer 2, dispatched in parallel). The detailed per-role spec lives in
`company-os/` (one file per division). Summary:

| Division | Key agent roles | Layer | Powered by |
|---|---|---|---|
| **Executive** | CEO, COO, CTO, CFO, CPO, CSO (strategy) | 1 | gstack `/office-hours`, `/plan-*-review`; you arbitrate |
| **Research** | Market, Industry, Competitor, Opportunity, Trend | 2 | CrewAI crew + browser-use + Firecrawl |
| **Product** | PM, Requirements, UX, Customer-Journey | 1→2 | gstack planning skills + ruflo workers |
| **Engineering** | Architect, Backend, Frontend, DevOps, DB, Testing, Docs | 1+2 | gstack build/review + OpenHands swarm |
| **Design** | Design-Research, Animation, UI-Inspiration, Visual-Identity | 1+2 | gstack `/design-*` + scraping crew |
| **Marketing** | SEO, Content, Copy, Social, Video, Growth | 2 | CrewAI + n8n; you approve brand voice |
| **Sales** | Lead-Discovery, Qualification, Outreach, CRM, Follow-up | 2 | CrewAI + n8n + a CRM (e.g., Twenty/Supabase) |
| **Customer Success** | Support, Feedback, Churn | 2 | n8n + LLM triage; you handle escalations |
| **Cybersecurity** | Threat, Vuln-Scan, Dependency-Audit, Pentest, Infra-Sec | 1+2 | gstack `/cso` + Semgrep/Trivy/ZAP/gitleaks |
| **Infrastructure** | Cloud, Monitoring, Scaling, Reliability | 1+2 | Coolify/k3s + Grafana/Prometheus/Sentry |
| **Finance** | Revenue, Cost-Optimization, **Token-Optimizer**, API-Usage | service | LiteLLM + OpenRouter + Langfuse |

> **Rule:** Layer-2 output is *never* trusted blindly — it always returns to a Layer-1 gate (a gstack
> review/QA/security skill) before it ships. That gate is where your taste and the quality live.

---

## PART 4 — Agent Communication Architecture

**Hierarchy:** Founder → Executive gates (Layer 1) → division leads → swarm workers (Layer 2). Information
flows down as *tasks/specs*, up as *artifacts + confidence scores*.

**Protocols:**
- **MCP (Model Context Protocol)** — how agents call tools and read/write the Brain. ruflo ships an MCP server; gstack skills are MCP/Claude-native.
- **A2A-style task handoff** — Layer 1 emits a task spec (markdown contract: goal, inputs, acceptance criteria) → ruflo dispatches to workers → workers return artifacts + a self-assessed confidence + provenance.
- **Files as the bus** — the simplest reliable channel: shared markdown specs + the git repo + the Obsidian vault. Agents communicate by reading/writing versioned files (auditable, diff-able).

**Memory tiers (what each agent can see):**
- **Short-term / working** — the current task context window + Mem0 scratch.
- **Episodic** — recent runs, retros, decisions (Mem0/Zep).
- **Long-term / semantic** — the knowledge graph (Cognee/GraphRAG) over the Obsidian vault + codebase.
- **Swarm memory** — ruflo AgentDB (HNSW vectors) shared across workers; SONA patterns for "what worked."

**Conflict resolution:**
1. **Spec is law** — the task contract's acceptance criteria decide correctness.
2. **Gates beat workers** — a Layer-1 review skill overrides Layer-2 output.
3. **Consensus for parallel duplicates** — ruflo's queen/consensus picks among N worker drafts.
4. **Human breaks ties** — anything ambiguous or irreversible escalates to you (by design, not by failure).

---

## PART 5 — The Company Brain (unified memory)

**Architecture (4 stores, 1 source of truth):**

```
            ┌──────────────────────────────────────────────┐
   YOU ───► │  OBSIDIAN VAULT  (source of truth, human)     │ ◄─── agents read/write
            │  decisions, specs, playbooks, retros, brand   │
            └───────────────┬──────────────────────────────┘
                            │ indexed into
        ┌───────────────────▼───────────────────┐
        │  COGNEE / GraphRAG  (knowledge graph)  │  "why did we choose X?", cross-doc reasoning
        └───────────────────┬───────────────────┘
        ┌───────────────────▼───────────────────┐   ┌──────────────────────────────┐
        │  MEM0 / Zep  (per-agent memory)        │   │  ruflo AgentDB (swarm vectors │
        │  episodic + facts that change          │   │  + SONA "what worked")        │
        └────────────────────────────────────────┘   └──────────────────────────────┘
```

**Why this split:** the Obsidian vault is the human-readable, git-versioned *truth*; Cognee makes it
*reasonable over* (graph queries, decision tracing); Mem0/Zep give each agent *working memory*; ruflo's
AgentDB is the swarm's *shared scratch + learning*. Don't centralize everything in one vector DB — you'll
lose the human-readability and the audit trail that keep a one-person company sane.

**Evaluation of the candidates you listed:**
- **Obsidian** — ✅ yes, as the human vault + interface (markdown = git-friendly = agent-friendly).
- **GraphRAG** — ✅ yes (or Cognee) for the reasoning layer; not as the only store.
- **Vector DBs** — ✅ but *inside* Mem0/ruflo; don't hand-roll one.
- **Knowledge graphs** — ✅ via Cognee/GraphRAG.
- **Local memory systems / agent frameworks** — ✅ Mem0 (general), Letta (personas), Zep (changing facts).

---

## PART 6 — AI Model Strategy & Routing

**Principle:** the **critical path runs on Claude** (your $20 sub, via gstack) for quality; **everything
parallel/cheap runs on free tiers**, routed by difficulty. A **Token-Credit Optimizer** (LiteLLM +
OpenRouter) enforces this automatically.

### 6.1 Model tiers (June 2026)

**Premium (critical path / hard reasoning):**
| Model | Why | Note |
|---|---|---|
| Claude (Opus/Sonnet) via your sub | Best agentic coding + judgment; native to gstack/Claude Code | The spine. Spend Opus budget on architecture/security/hard bugs |
| Gemini 2.5 Pro | Long context, strong reasoning, cheap | Good escalation target |

**Cheap (bulk reasoning / coding workers):**
| Model | Cost | Strength |
|---|---|---|
| DeepSeek V3/R1 | very low PAYG (5M free at signup) | strong coding/reasoning per dollar |
| Qwen 2.5/3 Coder | 1M free (90-day), cheap PAYG | coding, multilingual |
| GLM (Zhipu) | cheap | solid general/coding |

**Free (high-volume swarm / research / drafts):**
| Provider | Free allowance | Best for |
|---|---|---|
| Google AI Studio — Gemini 2.5 Flash | ~1,500 req/day, 1M ctx, multimodal, no card | research, long-context, vision |
| Groq — Llama 3.3 70B | 300+ tok/s, ~1,000 req/day | fast cheap inference |
| Cerebras | ~60k tok/min, ~1,700 req/day | highest free throughput |
| OpenRouter (free models) | 50–200 req/day; $10 one-time → 1,000/day | aggregation + auto-routing |
| SambaNova | free via email | Llama/Qwen |
| Ollama (local) | unlimited (your hardware) | offline drafts, privacy |

### 6.2 The routing table (difficulty → model)

| Task class | Route to | Fallback |
|---|---|---|
| Architecture, security review, gnarly bugs, final ship | **Claude (sub)** | Gemini 2.5 Pro |
| Routine code, tests, refactors (bulk) | DeepSeek / Qwen Coder | Groq Llama |
| Research, summarization, scraping triage | Gemini 2.5 Flash (free) | Cerebras / Groq |
| Content drafts, copy, social | Free tier (Flash/Llama) | DeepSeek |
| Embeddings / memory | local (bge/nomic) or cheap API | — |
| Classification / cheap glue | Groq 8B / Haiku | local |

### 6.3 Implementation
- **LiteLLM proxy** in front of everything: one OpenAI-compatible endpoint, per-key budgets, fallbacks, retries, cost logging. (`bootstrap/litellm-config.yaml`.)
- **OpenRouter** as the aggregator behind LiteLLM for the long tail of free/cheap models + auto-routing.
- **Langfuse** (self-host) for cost/latency observability per agent/task.
- **Caching:** prompt caching (Claude) + semantic cache (LiteLLM/Redis) to kill repeat spend.
- **Quota rotation:** the Token-Optimizer tracks each free tier's daily limit and rotates keys/providers before hitting walls (see `company-os/11-finance-token-optimizer.md`).

> **Honest note:** free tiers are for *building*. When a product serves real users, its production
> inference moves to paid/self-hosted with real SLAs. Budget for that the moment you have revenue.

---

## PART 7 — The Product Factory Workflow

End-to-end, with the **responsible agent · inputs · outputs · tools · quality gate** for each stage.
Layer-1 gates are **bold**; Layer-2 swarm work is *italic*.

| # | Stage | Agent(s) | Inputs | Outputs | Tools | Quality gate |
|---|---|---|---|---|---|---|
| 1 | **Idea / Discovery** | *Opportunity + Trend (research crew)* | market signals, your thesis | ranked idea list | CrewAI, browser-use, Firecrawl | **CEO `/office-hours`** |
| 2 | **Validation** | *Market + Competitor* | top idea | TAM, competitors, demand evidence | Replication Engine (Part 8) | **CEO review** |
| 3 | **Market research** | *Industry crew* | validated idea | positioning, ICP, pricing | research crew | **you approve ICP** |
| 4 | **Product spec** | **PM + Requirements** | research | PRD, user stories, scope | gstack `/plan-*-review` | **`/plan-ceo-review`** |
| 5 | **UI design** | **Design** + *inspiration crew* | PRD | design system, hi-fi screens, "wow" anim | gstack `/design-shotgun`,`/design-html`; Mobbin/Awwwards scrape | **`/design-review`** |
| 6 | **Architecture** | **Architect** | PRD + design | system design, data model, stack | gstack `/plan-eng-review` | **eng review** |
| 7 | **Development** | *OpenHands + ruflo workers* | spec + architecture | working code | OpenHands, Claude Code, cheap models | **gstack `/review`** |
| 8 | **Testing** | *Testing workers* + **QA** | code | tests, live browser QA | gstack `/qa` (Chromium), Playwright | **`/qa` must pass** |
| 9 | **Security** | **CSO** + *scanners* | code + infra | vuln report, fixes | gstack `/cso`, Semgrep/Trivy/ZAP/gitleaks | **`/cso` clean** |
| 10 | **Deployment** | **DevOps** | passing build | live app | Coolify/Dokploy, Cloudflare, gstack `/ship` `/land-and-deploy` | **canary `/canary`** |
| 11 | **Marketing** | *SEO/Content/Social crew* | live product | content, landing, posts | CrewAI + n8n | **you approve voice** |
| 12 | **Sales** | *Lead + Outreach crew* | ICP | lead lists, sequences | n8n + CRM | **you approve outreach** |
| 13 | **Support** | *Support/Feedback* | user messages | answers, tickets, insights | n8n + LLM triage | **you handle escalations** |
| 14 | **Improvement** | **`/retro`** + *analytics* | usage + feedback | next sprint backlog | gstack `/retro`, analytics | **CEO prioritization** |
| 15 | **Scale** | **Infra** | growth metrics | scaled infra | k3s, autoscale, Part 10 | **reliability SLO** |

> The loop is **1→14→back to 4**. Stage 15 only triggers when a product earns it.

---

## PART 8 — The Startup Replication Engine (your first move)

**Input:** `"Find a successful US startup and build the Indian equivalent."` (or a category).
**Output:** a ranked shortlist + a **build brief** for the winner, fed straight into Product Factory stage 4.

**Pipeline:**
```
Source candidates ─► Score ─► Localize-analysis ─► Rank ─► Build brief
(YC/Crunchbase/    (rubric)  (India fit:        (weighted)  (PRD seed for
 ProductHunt/                 payments, lang,                gstack /office-hours)
 G2 scraping)                 regulation, GTM)
```

**Scoring rubric (0–5 each, weighted):**
| Dimension | Weight | Question |
|---|---|---|
| TAM (India) | ×3 | Is the Indian market big & growing? |
| Demand evidence | ×3 | Are people already paying for this (US or India)? |
| Competition gap | ×2 | Is the India space underserved / weak incumbents? |
| Build feasibility (solo) | ×3 | Can a 1-person + agent org ship an MVP in <90 days? |
| Regulatory load | ×2 (inverse) | Low compliance burden (fintech/health = high)? |
| Distribution path | ×3 | Is there a cheap, automatable channel to first users? |
| Monetization | ×2 | Clear willingness-to-pay, sane pricing? |
| Moat potential | ×1 | Can localization/quality create durable advantage? |

**Agents:** *Opportunity Discovery* (sourcing) → *Competitor + Market* (scoring) → *Industry/Regulation*
(India-fit) → **CEO `/office-hours`** (final human pick). Implementation lives in
`bootstrap/replication-engine/` (CrewAI crew + n8n flow + the rubric as a prompt).

**India-specific lenses the engine must apply:** UPI/payments, pricing in ₹ (10–50× lower than US), regional
languages, mobile-first/low-bandwidth, GST/DPDP-Act compliance, and distribution via WhatsApp/YouTube/SEO.

---

## PART 9 — Security Blueprint

Goal = **hard target + observable + fast recovery** (not "unhackable" — that's a myth). Defense in depth:

| Domain | Practice | Tools |
|---|---|---|
| **Secrets** | Never in code/repo; vault them; rotate | gitleaks (pre-commit + CI), Doppler/Infisical, `.gitignore` `.env` |
| **Dependencies** | Pin + auto-update + scan | Dependabot/Renovate, Grype, `npm/pip audit` |
| **SAST** | Scan code on every PR | Semgrep, CodeQL |
| **DAST** | Scan the running app | OWASP ZAP (gstack `/cso` can drive) |
| **Containers/IaC** | Scan images + terraform | Trivy |
| **Supply chain** | SBOM + signing | Syft (SBOM), Sigstore/cosign |
| **Access** | Least privilege, MFA, scoped tokens | per-service keys; no root agents |
| **Agent-specific** | **Sandbox autonomous agents**; no prod creds in agent context; allow-list tools; human approval for irreversible actions | Docker isolation, MCP tool allow-lists |
| **Monitoring** | Logs, alerts, anomaly | Sentry, Grafana, Cloudflare WAF, Uptime-Kuma |
| **Incident response** | Runbook + backups + rollback | documented in `company-os/09-security.md` |

> **The OpenClaw lesson (2026's first major agent security crisis):** "self-improving" agents that write
> and run their own code are the highest-risk component you can deploy. If you use that pattern at all,
> **sandbox it, give it no secrets, and gate its actions.** Treat every autonomous agent as a potential
> insider threat. This is why Layer 1 (human gates) exists.

CI/CD security: branch protection, required reviews (a gstack `/review` + `/cso` pass), signed commits,
least-privilege deploy keys, and no secrets in CI logs.

---

## PART 10 — Infrastructure Blueprint (MVP → million users)

| Tier | Users | Hosting | DB | Compute | Observability | Monthly $ |
|---|---|---|---|---|---|---|
| **MVP** | 0–1k | Vercel/Netlify free + Coolify on 1 VPS | Supabase free | 1 small VPS | Sentry free, Uptime-Kuma | ~$0–10 |
| **Growth** | 1k–50k | Coolify/Dokploy on 1–2 VPS, Cloudflare | Supabase Pro / managed PG | 2–4 VPS, Docker | Grafana+Prometheus, Sentry | ~$50–200 |
| **Scale** | 50k–500k | **k3s** cluster (Hetzner/OVH), Cloudflare WAF | PG + read replicas, Redis | autoscaling nodes | full Grafana stack, alerting | ~$300–1.5k |
| **Million-user** | 1M+ | Multi-node k8s, CDN, queue (NATS/Kafka) | sharded/managed PG, cache tiers | autoscale + spot | SLOs, on-call, tracing | $2k+ |

**Principles:** start on a **single cheap VPS with Coolify** (it gives you Heroku-like deploys, free); move
to **k3s** only when reliability/scale demand it; keep **Cloudflare** in front from day one (free CDN/WAF/
tunnels); automate everything with n8n + IaC. Don't pre-build for a million users you don't have — but
*do* write the path down (this table) so scaling is a checklist, not a panic.

---

## PART 11 — The Founder Dashboard

Your single command center. Build it last and cheaply (a small Next.js app, or start with a Notion/Obsidian
dashboard + n8n pushing data). It surfaces:

| Panel | Shows | Source |
|---|---|---|
| **Company health** | products live, uptime, error rate | Uptime-Kuma, Sentry |
| **Revenue** | MRR, new/churned, by product | Stripe/Razorpay API |
| **Product status** | sprint stage, open gates awaiting *you* | gstack state, git |
| **Agent status** | running swarms, queue, failures | ruflo, n8n |
| **Security alerts** | new vulns, scan results, incidents | Semgrep/Trivy/ZAP, Sentry |
| **Infra alerts** | CPU/mem, scaling events, costs | Grafana/Prometheus |
| **Growth** | traffic, signups, funnel, SEO ranks | Plausible/Umami, Search Console |
| **Opportunities** | new ideas from the research crew | Replication Engine output |
| **Token/cost** | spend by model/agent, quota left | Langfuse, LiteLLM |
| **Daily report** | one-paragraph "state of the company" | n8n cron → LLM summary → you |

The most important panel is **"gates awaiting you"** — the dashboard's job is to tell you the few human
decisions that unblock the whole agent org today.

---

## PART 12 — Five-Year Roadmap

| Year | Goal | Skills to learn | Repos/systems to master | Revenue target | Hiring |
|---|---|---|---|---|---|
| **Y1** | 1 profitable product + the core system | Claude Code/gstack, ruflo, Docker/WSL, basic security, LiteLLM | gstack, ruflo, OpenHands, Coolify, Supabase, n8n | $1k→$10k MRR | none (agents) |
| **Y2** | Productize the factory across 2–3 products | k3s basics, growth/SEO, CRM ops, observability | Replication Engine at scale, Cognee brain, Grafana | $10k→$50k MRR | 1 freelancer (design/support) as needed |
| **Y3** | Scale infra + paid model tier + first hire | hiring/managing, finance, advanced security | k3s, CI/CD hardening, SOC-style monitoring | $50k→$150k MRR | first FT contractor/eng |
| **Y4** | Portfolio / platform; pick a breakout | platform thinking, fundraising (optional) | multi-tenant infra, data moat | $150k→$500k MRR | 2–4 people around the breakout |
| **Y5** | Double down on the winner; optional venture scale | leadership, GTM at scale | full prod stack, compliance | $500k MRR→$1M+ ARR; *option* on the moonshot | small team |

Revenue numbers are **targets, not promises** — see Part 13.

---

## PART 13 — BRUTAL REALITY CHECK  *(read this one)*

**What's realistically possible today (2026):**
- A solo founder can use this stack to **design, build, secure, deploy, and market a real SaaS product in weeks**, mostly with agents. ✅
- You can run **research, content, lead-gen, and support** largely on autopilot with human gates. ✅
- You can operate at the *output* of a 20–50 person company on a **~$20/mo + free-tier budget** for the build phase. ✅
- Reaching **$1k–$10k MRR in 6–12 months** with disciplined execution: **~40–60% likely.** ✅

**What is hype:**
- "100s of fully autonomous agents building a billion-dollar company with no humans." ❌ Reliability compounds against you; autonomy at scale produces *confident slop*. The systems that actually ship (gstack) are **human-gated** for exactly this reason.
- "Self-learning/self-improving agents that get smarter on their own." Mostly ❌ today — it's memory + retrieval + retros + prompt tuning, not the agent rewriting itself into genius. The one repo that really self-modifies (OpenClaw) became a **security disaster**.
- "Unhackable security." ❌ Doesn't exist.
- "Free API keys forever, unlimited." ❌ Rate-limited, expiring, ToS-bound; fine for building, not for serving users at scale.

**What cannot (yet) be automated / still needs you:**
- **Judgment & taste** — what to build, whether it's good, brand voice, pricing.
- **Distribution & trust** — getting the first 100 customers, partnerships, a human face.
- **Irreversible/▶ legal/financial decisions** — payments, contracts, incident response.
- **Final quality gates** — the buck stops at a human review.

**Biggest risks:** (1) building the system instead of a product (the trap), (2) shipping AI slop that
nobody wants, (3) a security incident from an over-trusted autonomous agent, (4) free-tier dependency
breaking under real load, (5) founder burnout from being the only gate.

**Biggest bottlenecks:** distribution > judgment > agent reliability > your own operating capacity. **Not**
the agents' ability to write code.

**Probability estimates (honest):**
| Outcome | Horizon | Probability |
|---|---|---|
| First paying users | 1–3 months | high (60–75%) if you ship |
| $1k–$10k MRR | 6–12 months | **40–60%** |
| $1M ARR (one product or portfolio) | 2–3 years | **10–20%** |
| $10M ARR | 3–5 years | low (a few %) |
| Billion-dollar outcome | 5+ years | **low single digits %** |

**The point:** the *same system* that makes the small wins likely is the one that buys you a cheap lottery
ticket on the big one. Build for the realistic win. Treat godmode as the upside, not the plan.

---

## Appendix A — Immediate next actions
1. Stand up WSL2 + the stack: `bootstrap/0-enable-wsl.ps1` then `bootstrap/install.sh`.
2. Add keys to `.env`; start the LiteLLM Token-Optimizer (`bootstrap/litellm-config.yaml`).
3. **Run the Startup Replication Engine** (`bootstrap/replication-engine/`) → pick your first product.
4. Run the Product Factory (Part 7) via gstack → ship the MVP → get first users.
5. Follow `bootstrap/90-DAY-PLAN.md`.

## Appendix B — Repo index (clone list)
- Spine: `garrytan/gstack` · Swarm: `ruvnet/ruflo` · Worker: `OpenHands/OpenHands` · Crews: `crewAIInc/crewAI`
- Memory: `mem0ai/mem0` · `topoteretes/cognee` · Obsidian (app)
- Routing: `BerriAI/litellm` · OpenRouter · `langfuse/langfuse`
- Automation: `n8n-io/n8n` · Browser: `browser-use/browser-use` · Scrape: `mendableai/firecrawl`
- Design libs: shadcn/ui · Aceternity · Magic UI · 21st.dev
- Security: Semgrep · `aquasecurity/trivy` · `gitleaks/gitleaks` · CodeQL · OWASP ZAP · `anchore/syft`
- Infra: `coollabsio/coolify` · k3s · Supabase · Grafana/Prometheus · `getsentry/sentry` · Uptime-Kuma

## Appendix C — Sources (verified June 2026)
Star counts and capabilities verified via GitHub and ecosystem reviews in June 2026. Free-tier limits per
provider docs and 2026 round-ups (TokenMix, awesome-free-llm-apis, provider docs). Memory comparison per
2026 reviews (Mem0/Zep/Letta/Cognee). Treat all third-party limits as subject to change — re-verify before
relying on them in production.

---

*This is a living document. It is updated as the system is built and as reality teaches us. Companion
operational specs live in `company-os/`; the runnable kit lives in `bootstrap/`.*
