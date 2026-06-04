# 12 — The Company Brain (unified memory)

> **Scope.** Operational expansion of [`00-MASTER-BLUEPRINT.md`](../00-MASTER-BLUEPRINT.md) Part 5. The
> blueprint says *which* memory systems and *why*; this file says *what goes where*, *who may read/write
> each store*, the *exact document schemas*, and *how to seed and maintain it*. Governed by
> [[00-architecture]]; consumed by every division.
>
> **One sentence:** the Brain is how a one-person company gets the compounding memory of a 50-person one —
> a human-readable, git-versioned source of truth that agents can reason over.

---

## 1. The four stores (and the single source of truth)

```
            ┌──────────────────────────────────────────────┐
   YOU ───► │  OBSIDIAN VAULT  (brain/)  — SOURCE OF TRUTH  │ ◄─── agents read/write (via MCP)
            │  decisions · specs · playbooks · retros · brand│
            └───────────────┬──────────────────────────────┘
                            │ indexed into (read-only projection)
        ┌───────────────────▼───────────────────┐
        │  COGNEE / GraphRAG  (knowledge graph)  │  "why did we choose X?", cross-doc reasoning
        └───────────────────┬───────────────────┘
   ┌────────────────────────▼───────────┐   ┌──────────────────────────────────┐
   │  MEM0 / Zep  (per-agent memory)    │   │  ruflo AgentDB (swarm vectors +   │
   │  episodic runs + facts that change │   │  SONA "what worked" patterns)     │
   └────────────────────────────────────┘   └──────────────────────────────────┘
```

| Store | Role | Human-readable? | Authoritative? | Tech |
|---|---|---|---|---|
| **Obsidian vault** (`brain/`) | The truth: decisions, specs, playbooks, retros, brand | ✅ yes (markdown) | ✅ **yes** | Obsidian app + git |
| **Cognee / GraphRAG** | Reasoning layer: graph queries, decision tracing | partial | ❌ derived | Cognee (or MS GraphRAG) |
| **Mem0 / Zep** | Per-agent working & episodic memory; changing facts | ❌ | ❌ derived | Mem0 (general), Zep (bi-temporal) |
| **ruflo AgentDB** | Swarm shared scratch + SONA learned patterns | ❌ | ❌ derived | ruflo HNSW vectors |

> **The cardinal rule:** the **Obsidian vault is the only authoritative store.** Everything else is a
> *derived, rebuildable projection* of it (an index, a cache, a vector embedding). If the graph or a
> vector DB disagrees with the vault, the vault wins and the projection is re-indexed. This is what keeps
> the audit trail and human-readability that a solo founder needs to stay sane — never let a vector DB
> become the place a fact "really" lives.

---

## 2. What goes where (the write-policy table)

When an agent or gate produces durable knowledge, route it like this:

| Knowledge type | Lives in | Written by | Schema |
|---|---|---|---|
| A decision + its rationale | `brain/decisions/` (vault) | the gate that made it ([[00-architecture]] §6) | §6 Decision Record |
| A product/feature spec, PRD | `brain/specs/` (vault) | [[03-product]] gates | §7 Spec |
| A repeatable procedure | `brain/playbooks/` (vault) | any division, refined by `/retro` | §8 Playbook |
| Sprint/launch learnings | `brain/retros/` (vault) | `/retro` ([[01-executive]]) | §9 Retro |
| Brand voice, naming, pricing | `brain/brand/` (vault) | you + [[06-marketing]] | freeform + examples |
| An agent's working scratch | Mem0 (per-agent) | the agent, automatically | n/a (ephemeral) |
| Facts that change (CRM, support, finance state) | Zep (bi-temporal) | [[07-sales]], [[08-customer-success]], [[11-finance-token-optimizer]] | n/a |
| "This approach worked / failed" | ruflo AgentDB (SONA) | the swarm, automatically | n/a (vectors) |
| Cross-doc reasoning / "trace the why" | Cognee graph (read) | indexer (auto from vault) | n/a (graph) |

**Read policy:** any agent may *read* the vault and the derived stores it's scoped to. **Write to the
vault is gated** — only a Layer-1 gate or the founder commits authoritative docs; Layer-2 workers *propose*
(write a draft into `tasks/` or a PR), they don't commit to `brain/` directly. This mirrors
[[00-architecture]] §5 (gates beat workers).

---

## 3. The Obsidian vault structure (`brain/`)

```
brain/
├── decisions/        # one file per decision (ADR-style, §6). The "why" of the company.
│   └── 2026-06-04-use-coolify-not-render.md
├── specs/            # PRDs, feature specs, API contracts (§7)
├── playbooks/        # repeatable procedures: "how we ship", "how we do SEO" (§8)
├── retros/           # sprint/launch retrospectives (§9), source of playbook improvements
├── brand/            # voice, tone, naming, pricing, visual identity refs
├── products/         # per-product knowledge (links into ../products/<name>/)
├── research/         # market/competitor findings from [[02-research]] (curated, not raw dumps)
└── _moc/             # "maps of content" — Obsidian index notes that organize the above
```

Conventions: **kebab-case, date-prefixed filenames**; **frontmatter on every note** (so Cognee/Dataview
can query it); **`[[wikilinks]]` liberally** (the graph *is* the value); raw scrapes stay in `tasks/`,
only *curated* findings get promoted to `brain/research/`.

---

## 4. Memory tiers (what each agent can see)

From [`00-MASTER-BLUEPRINT.md`](../00-MASTER-BLUEPRINT.md) Part 4, made concrete:

| Tier | Horizon | Store | Example |
|---|---|---|---|
| **Working** | this task | context window + Mem0 scratch | the current Task Contract + pulled context |
| **Episodic** | recent runs | Mem0 / Zep | "last sprint we tried X, it failed" |
| **Semantic / long-term** | the whole company | Cognee graph over the vault + code | "why did we choose Coolify over Render?" |
| **Swarm** | shared, cross-worker | ruflo AgentDB + SONA | "this scraping pattern beats that one" |

An agent's **context-assembly** for a task = (Task Contract) + (relevant vault docs via graph search) +
(its own Mem0 episodic memory) + (relevant SONA patterns). [[13-model-router]] decides which *model* then
processes that context; the Brain decides *what's in it*.

---

## 5. How agents access the Brain (MCP)

- **Read:** agents query via the **ruflo MCP server** (vector + graph search) and direct file reads of the
  vault. gstack skills read the vault natively (it's just files in the repo).
- **Write (gated):** Layer-1 gates and you write authoritative docs by **committing markdown to `brain/`**
  (a git commit = a durable, diffable memory write). Layer-2 workers write *proposals* into `tasks/`.
- **Re-index:** a post-commit hook (or n8n cron, [[10-infrastructure]]) re-indexes changed vault files into
  Cognee + the vector stores, so the derived projections never drift far from truth.

> Optional, per the blueprint: gstack's Supabase "GBrain" can back the vector store; ruflo's AgentDB is
> the default. Either is a *projection* of the vault, not a replacement for it.

---

## 6. Schema — Decision Record (the most important one)

Every gate that makes a non-trivial choice writes one of these to `brain/decisions/`. This is how a
one-person company never re-litigates a settled question and how a fresh chat learns *why*.

```markdown
---
type: decision
id: DEC-2026-0007
title: Use Coolify (not Render) for MVP hosting
date: 2026-06-04
status: accepted        # proposed | accepted | superseded
decided_by: 01-executive (/office-hours)   # the gate
supersedes: null
tags: [infra, cost]
---

## Context
What forced a choice. Constraints (budget, solo, WSL2).

## Options considered
1. Coolify (self-host PaaS) — pros / cons
2. Render — pros / cons
3. Vercel-only — pros / cons

## Decision
We chose **Coolify**. (One paragraph.)

## Rationale
Why, in terms of the blueprint's principles (free-first, self-host, [[10-infrastructure]]).

## Consequences
What this commits us to; what we'll revisit and when.

Links: [[10-infrastructure]] · [[specs/mvp-hosting]]
```

> Cognee ingests these and lets you (or an agent) ask *"why did we choose X over Y?"* and get the answer
> with provenance — the single highest-leverage thing the graph layer buys you.

---

## 7. Schema — Spec / PRD (`brain/specs/`)

```markdown
---
type: spec
id: SPEC-2026-0003
product: <name>
status: draft        # draft | approved | shipped
owner: 03-product
gate: /plan-ceo-review
---
## Problem / user & job-to-be-done
## Scope (in / explicitly out)
## User stories  (as a checklist)
## Acceptance criteria  (objective — becomes Task Contract criteria, [[00-architecture]] §2)
## Non-functional (perf, security ref [[09-security]], a11y)
## Open questions → (escalate per division Escalation rules)
```

---

## 8. Schema — Playbook (`brain/playbooks/`)

A playbook is a *runnable procedure* — the company's compounding operational knowledge. Each division's
file (§3 of [[00-architecture]]) lists its playbooks; the canonical version lives here.

```markdown
---
type: playbook
id: PLAY-ship-a-feature
owner: 04-engineering
last_improved_by: retro 2026-06-01
---
## When to use
## Preconditions
## Steps   (numbered, each with the gstack skill / tool / model tier)
## Gates   (which [[00-architecture]] §6 gates fire, in order)
## Failure modes & recovery
```

---

## 9. Schema — Retro (`brain/retros/`)

Written by `/retro` ([[01-executive]]). **Retros are the engine of "self-learning"** in the honest sense
(blueprint Part 13): not weight updates, but *better playbooks and prompts over time*.

```markdown
---
type: retro
id: RETRO-2026-W23
sprint: <name>
date: 2026-06-04
---
## What we set out to do
## What happened (facts, metrics)
## What worked → promote to / update a [[playbooks/...]]
## What failed → a [[decisions/...]] to change, or a guardrail
## Action items (each → a Task Contract or a spec change)
```

---

## 10. Retention, invalidation & hygiene

- **Vault = permanent** (it's git history; nothing is truly deleted, only `superseded`).
- **Mem0/Zep = decaying.** Use **Zep's bi-temporal model** for facts that change (a lead's status, a
  price) so superseded facts are *invalidated*, not silently overwritten. Mem0 holds general episodic
  memory; let it summarize/forget stale scratch.
- **ruflo AgentDB = prunable.** SONA patterns that stop winning get down-weighted; it's a cache, rebuildable.
- **Monthly hygiene (a playbook):** a `/retro`-adjacent pass that promotes proven patterns to playbooks,
  marks stale decisions `superseded`, and re-indexes the graph. Mirrors the founder's own memory
  consolidation discipline.

---

## 11. Security & privacy (hard rules)

- **No secrets in the Brain — ever.** API keys, tokens, customer PII beyond what a task needs: never in
  `brain/`, never in agent-readable context. `.env` is git-ignored; secrets live in a vault/manager (see
  [[09-security]]). The Brain is open-source-publishable by design.
- **Least-context.** A worker gets only the Brain slices its Task Contract needs (allow-list, not
  firehose). Reduces blast radius if a Layer-2 agent is compromised (the OpenClaw lesson, [[09-security]]).
- **Provenance always.** Every promoted fact cites its source. Unsourced "knowledge" doesn't enter the vault.

---

## 12. Seeding the Brain (bootstrap)

On first stand-up, seed `brain/` with: this blueprint + the `company-os/` specs (so the company knows its
own architecture), an initial `brand/` note (even a placeholder voice), and the first decision records for
the locked choices in `PROJECT_CONTEXT.md` §2 (scope, budget/harness, WSL2, replication-engine-first).
After that, the Brain grows by itself — one gate, one retro, one decision at a time.

> See [[13-model-router]] for how context pulled from the Brain is matched to the cheapest capable model,
> and [[00-architecture]] §8 for where Brain reads/writes sit in the task lifecycle.
