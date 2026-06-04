# company-os/ — The Operating System of the Godmode AI Company

> **What this folder is.** [`00-MASTER-BLUEPRINT.md`](../00-MASTER-BLUEPRINT.md) is the *strategy* — the
> why and the what. **`company-os/` is the *operating manual*** — the how, at the level of detail an agent
> (or a fresh-chat Claude) can execute against. One file per division/role, plus three cross-cutting
> system specs. This is an **Obsidian-ready vault**: open the `GOD/` folder in Obsidian and the
> `[[wikilinks]]` below become a navigable graph.
>
> **Last updated:** 2026-06-04 · **Status:** core specs in progress (see table).

---

## How to read this vault

1. **Start with [[00-architecture]]** — it defines the 3-layer model operationally and, crucially, the
   **standard role-spec schema** that every division file (`01`–`11`) follows. Read it once and every
   other file becomes predictable.
2. **Then the two system specs you'll touch constantly:** [[12-company-brain]] (where knowledge lives and
   who may read/write it) and [[13-model-router]] (which model runs which task, and how cost stays sane).
3. **Then the division files** as you need them — each is a self-contained operating manual for one part
   of the company.

> **The golden rule (from the blueprint, Part 3):** Layer-2 swarm output is *never* trusted blindly. It
> always returns to a **Layer-1 human gate** before it ships. Every division file names its gates
> explicitly. If a file has no gate, it's not finished.

---

## File map & status

### Core system specs

| # | File | What it specifies | Blueprint source | Status |
|---|---|---|---|---|
| — | [[_INDEX]] | This file — the vault index & conventions | — | ✅ |
| 00 | [[00-architecture]] | The 3-layer model, the task contract, the role-spec schema, conflict resolution | Parts 3 & 4 | ✅ |
| 12 | [[12-company-brain]] | Unified memory: Obsidian + Cognee + Mem0/Zep + ruflo AgentDB; read/write policy; schemas | Part 5 | ✅ |
| 13 | [[13-model-router]] | Difficulty→model routing, LiteLLM/OpenRouter, quota rotation, caching, budget guards | Part 6 | ✅ |

### Division files (one per org-chart division)

| # | File | Division | Layer | Powered by | Status |
|---|---|---|---|---|---|
| 01 | [[01-executive]] | Executive (CEO/COO/CTO/CFO/CPO/CSO) | 1 | gstack `/office-hours`, `/plan-*-review` | ✅ |
| 02 | [[02-research]] | Research (market/competitor/opportunity/trend) | 2 | CrewAI + browser-use + Firecrawl | ✅ |
| 03 | [[03-product]] | Product (PM/requirements/UX/journey) | 1→2 | gstack planning + ruflo workers | ✅ |
| 04 | [[04-engineering]] | Engineering (architect/BE/FE/DevOps/DB/test/docs) | 1+2 | gstack build/review + OpenHands | ✅ |
| 05 | [[05-design]] | Design (research/animation/inspiration/identity) | 1+2 | gstack `/design-*` + scrape crew | ✅ |
| 06 | [[06-marketing]] | Marketing (SEO/content/copy/social/video/growth) | 2 | CrewAI + n8n | ✅ |
| 07 | [[07-sales]] | Sales (lead-disc/qualify/outreach/CRM/follow-up) | 2 | CrewAI + n8n + CRM | ✅ |
| 08 | [[08-customer-success]] | Customer Success (support/feedback/churn) | 2 | n8n + LLM triage | ✅ |
| 09 | [[09-security]] | Cybersecurity (threat/scan/deps/pentest/infra-sec) | 1+2 | gstack `/cso` + Semgrep/Trivy/ZAP/gitleaks | ✅ |
| 10 | [[10-infrastructure]] | Infrastructure (cloud/monitoring/scaling/reliability) | 1+2 | Coolify/k3s + Grafana/Prometheus/Sentry | ✅ |
| 11 | [[11-finance-token-optimizer]] | Finance (revenue/cost/**token-optimizer**/API-usage) | service | LiteLLM + OpenRouter + Langfuse | ✅ |

> When you finish a file, flip its status here **and** in [`PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md) §1.

---

## Numbering convention

- **`00`** = the architecture that governs everything.
- **`01`–`11`** = the eleven divisions, in the exact order of the org-chart table in the blueprint
  (Part 3). This is why security is `09` and finance is `11` — the blueprint already references
  `company-os/09-security.md` and `company-os/11-finance-token-optimizer.md`.
- **`12`–`13`** = cross-cutting *system* specs (the Brain, the Router) that every division consumes but no
  single division owns.
- **`_INDEX`** sorts to the top (underscore) so it's always the first thing you see.

---

## The relationship between the three artifacts

```
00-MASTER-BLUEPRINT.md   →  WHY + WHAT   (strategy, rankings, reality check)   — read once
company-os/              →  HOW          (per-division operating manuals)      — reference daily
bootstrap/               →  RUN IT       (scripts, configs, replication engine)— execute
```

Each layer is *derived from and consistent with* the one above it. If `company-os/` ever contradicts the
blueprint, the blueprint wins and the spec gets fixed (and vice-versa once reality teaches us — these are
living documents). The chain of custody for any decision is: **blueprint → company-os spec → bootstrap
implementation → a decision record in [[12-company-brain]]**.

---

## For a fresh-chat Claude resuming here

You do **not** need the prior conversation. Read, in order: [`PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md)
→ [`CURRENT_TASK.md`](../CURRENT_TASK.md) → [[00-architecture]] → the specific division file you're
extending. Honor the standing rules in `PROJECT_CONTEXT.md` §8 (auto-maintain the handoff files; give the
model-escalation heads-up before big chunks; commit + push at milestones; never commit secrets).
