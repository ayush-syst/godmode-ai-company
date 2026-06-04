# 00 — Architecture (operational)

> **Scope.** This is the operational expansion of [`00-MASTER-BLUEPRINT.md`](../00-MASTER-BLUEPRINT.md)
> Parts 3 (org chart) and 4 (communication). The blueprint says *what* the three layers are; this file
> says *how* they interact, *how* a unit of work moves through them, and *what schema* every division file
> ([[01-executive]]…[[11-finance-token-optimizer]]) must follow so the whole vault is consistent.
>
> Companion specs: [[12-company-brain]] (memory) · [[13-model-router]] (which model runs what).

---

## 1. The three layers, operationally

```
┌─ LAYER 0 ─ FOUNDER + COMPANY BRAIN ────────────────────────────────────────┐
│  You set direction and own taste. The Brain (Obsidian ⇄ Cognee ⇄ Mem0/Zep   │
│  ⇄ ruflo AgentDB) is the shared, versioned memory every layer reads/writes. │
│  See [[12-company-brain]].                                                   │
└────────────────────────────────────────────────────────────────────────────┘
            │ direction, approvals (gates)            ▲ artifacts, decisions, retros
            ▼                                         │
┌─ LAYER 1 ─ HUMAN-GATED SPINE  (gstack on Claude) ──────────────────────────┐
│  Executive · Product · Design · Engineering-review · Security · QA · Ship.  │
│  Implemented as gstack **skills you trigger**. This is where quality,       │
│  taste, and cost control live. Runs on Claude (your $20 sub).               │
└────────────────────────────────────────────────────────────────────────────┘
            │ task contracts (specs)                  ▲ artifacts + confidence + provenance
            ▼                                         │
┌─ LAYER 2 ─ AUTONOMOUS SWARM  (ruflo · OpenHands · CrewAI) ─────────────────┐
│  Research, codegen, test-writing, scraping, content drafts, lead lists.     │
│  Parallel, sandboxed, cheap/free models (see [[13-model-router]]).          │
│  Output is ALWAYS returned to a Layer-1 gate before it ships.               │
└────────────────────────────────────────────────────────────────────────────┘

SERVICES (cross-cutting, consumed by all layers):
  Token Optimizer [[13-model-router]] · Security scanners [[09-security]] ·
  Infra/CI [[10-infrastructure]] · n8n automation · The Brain [[12-company-brain]]
```

**The one rule that makes this safe:** information flows *down* as **task contracts** (specs with
acceptance criteria) and *up* as **artifacts + a self-assessed confidence score + provenance**. A gate
(Layer 1, a human-triggered gstack skill) stands between every "up" flow and anything that ships, gets
deployed, or touches a customer.

**Why not a flat swarm of 100 agents:** reliability compounds multiplicatively. A 100-step autonomous
chain at 95% per-step reliability succeeds ~0.6% of the time (`0.95¹⁰⁰`). Gates break the chain into
short, independently-verified segments — that's the entire architectural thesis.

---

## 2. The unit of work: the Task Contract

Everything that crosses a layer boundary is a **Task Contract** — a markdown file (files are the bus; see
§4). It is the single source of truth for one unit of work. Layer 1 emits it; Layer 2 fulfills it; the
gate checks the result against it.

```markdown
---
id: TASK-2026-0042
title: Draft 5 competitor teardowns for <product>
issued_by: 01-executive (CEO /office-hours)
assigned_to: 02-research (CrewAI competitor crew)
layer: 2
model_tier: free          # routed per [[13-model-router]]
created: 2026-06-04
gate: CEO review          # the Layer-1 skill that will accept/reject this
status: in_progress       # queued | in_progress | returned | accepted | rejected
---

## Goal
One sentence. What done looks like.

## Inputs
- Links to Brain docs / specs / prior artifacts (Obsidian paths, git refs).

## Acceptance criteria   ← THE CONTRACT. The gate decides correctness against THIS.
- [ ] Criterion 1 (objective, checkable)
- [ ] Criterion 2
- [ ] Provenance cited for every claim

## Constraints
- Budget / model tier / time box / tools allowed (allow-list).

## Return format
- Exactly what artifact(s) to produce and where to write them.
```

**On return, the worker appends:**

```markdown
## Result
- artifact: <path or git ref>
- confidence: 0.0–1.0   (worker's self-assessment)
- provenance: [sources, tools used, models used]
- open questions / risks: ...
```

The **confidence score** is not decoration — it routes attention. Low-confidence returns get a heavier
gate (more human scrutiny, or a second worker via consensus, §5). See [[13-model-router]] for how tier and
confidence interact.

---

## 3. The role-spec schema (every division file MUST follow this)

This is the contract that keeps `01`–`11` consistent. When you write or extend a division file, fill in
**every** section. Divisions differ in content, never in shape.

```markdown
# NN — <Division name>

> One-line mission. Blueprint source: Part N. Layer(s): 0/1/2. Powered by: <repos/skills>.

## Roles            — the named "agents" in this division and the one-line job of each.
## Layer mapping    — which roles are Layer-1 gates (gstack skills) vs Layer-2 workers (ruflo/CrewAI).
## Inputs           — what this division consumes (from which other division / the Brain).
## Outputs          — what it produces, and which division/gate consumes it next.
## Tools            — exact repos, skills, MCP servers, scanners, APIs.
## Quality gates    — the Layer-1 checkpoint(s); pass/fail criteria; who/what triggers them.
## Model routing    — default tier per role (links to [[13-model-router]]).
## Memory           — what this division reads/writes in the Brain ([[12-company-brain]]).
## Escalation       — when this division must stop and ask the founder (the human-in-the-loop triggers).
## Playbooks        — 1–3 concrete, runnable end-to-end procedures (the "do this, then this").
## KPIs / signals   — how we know this division is working.
```

> **Why a fixed schema:** it makes the vault queryable (a graph in Obsidian/Cognee), it makes a fresh-chat
> Claude productive in minutes, and it forces every division to declare its **gates** and **escalations** —
> the two things that keep autonomy from becoming liability.

---

## 4. Communication: files as the bus

The simplest reliable channel is the one we already trust for code: **versioned markdown files + git +
the Obsidian vault.** Agents communicate by reading and writing files, not by chatty message-passing.

| Protocol | Used for | Where |
|---|---|---|
| **MCP (Model Context Protocol)** | agents calling tools & reading/writing the Brain | ruflo MCP server; gstack skills are Claude/MCP-native |
| **Task Contracts** (A2A-style) | Layer-1 → Layer-2 handoff (§2) | markdown files under `tasks/` (git-tracked) |
| **Files as the bus** | everything durable: specs, artifacts, decisions | the git repo + the Obsidian vault |
| **n8n events** | time/webhook triggers, CRM, outreach, cron | n8n (self-hosted), see [[10-infrastructure]] |

**Why files, not a message queue:** auditability and diff-ability. Every handoff is a commit; every
decision is a file you (or a future agent) can read. For a one-person company, the audit trail *is* the
team's shared memory. Reserve real queues (NATS/Kafka) for the Scale tier only (blueprint Part 10).

---

## 5. Conflict resolution (the precedence ladder)

When two agents disagree, or a worker's output is questionable, resolve in this fixed order:

1. **Spec is law.** The Task Contract's acceptance criteria decide correctness. Not vibes, not seniority.
2. **Gates beat workers.** A Layer-1 review skill (`/review`, `/cso`, `/qa`, design review) overrides any
   Layer-2 output, always.
3. **Consensus for parallel duplicates.** When N workers produced N drafts, ruflo's queen/consensus
   (Raft/Byzantine/Gossip) or a Layer-1 skill picks the winner — typically the highest-confidence draft
   that passes the criteria.
4. **Human breaks ties.** Anything ambiguous, irreversible, legal/financial, or taste-dependent escalates
   to **you**. This is *by design* (the gate firing correctly), not a failure.

---

## 6. What a "gate" actually is (operational definition)

A **gate** is a Layer-1 checkpoint — almost always a **gstack skill you run** — that:

- takes a Layer-2 artifact + its Task Contract,
- checks it against the acceptance criteria (and against taste, which is yours),
- and emits one of: **accept** (artifact proceeds), **return** (back to the worker with notes), or
  **reject** (kill it).

Every gate **writes a decision record** to the Brain ([[12-company-brain]] §6) so the *why* is never lost.
The canonical gates, mapped to gstack skills:

| Gate | gstack skill | Division | Blocks until |
|---|---|---|---|
| Strategy / idea | `/office-hours` | [[01-executive]] | CEO accepts the direction |
| Plan review | `/plan-ceo-review`, `/plan-eng-review` | [[01-executive]] / [[04-engineering]] | plan is sound |
| Design review | `/design-review` | [[05-design]] | UI clears the taste bar |
| Code review | `/review` | [[04-engineering]] | no staff-eng-level bugs |
| Security | `/cso` | [[09-security]] | scanners clean + STRIDE pass |
| QA | `/qa` | [[04-engineering]] | live Chromium checks pass |
| Ship | `/ship`, `/land-and-deploy` | [[10-infrastructure]] | canary healthy |
| Retro | `/retro` | [[01-executive]] | learnings written to the Brain |

**Rule:** an artifact may not skip a gate. It may *fast-pass* a gate (you glance and accept) but the gate
must fire and leave a record. No silent merges to anything customer-facing.

---

## 7. Directory map of the running system

```
GOD/
├── company-os/              ← you are here (the operating manuals)
├── bootstrap/               ← the runnable kit (install, configs, replication engine)
│   ├── litellm-config.yaml  ← implements [[13-model-router]]
│   └── replication-engine/  ← implements blueprint Part 8
├── tasks/                   ← Task Contracts (§2), git-tracked, the Layer-1↔2 bus
├── brain/                   ← the Obsidian vault (see [[12-company-brain]] for its inner structure)
│   ├── decisions/  specs/  retros/  playbooks/  brand/
└── products/                ← one folder per product the factory builds
    └── <product>/           ← its own repo, gated by the Product Factory (blueprint Part 7)
```

> `tasks/` and `brain/` are created during bootstrap, not now. They're listed here so the data-flow in
> §2–§4 has a concrete home. Secrets never live in any of these (see [[09-security]]); `.env` is
> git-ignored.

---

## 8. The standard task lifecycle (putting it together)

```
You (Layer 0) ── direction ──►  /office-hours (Layer 1 gate, [[01-executive]])
                                      │ emits Task Contract(s) (§2)
                                      ▼
                              ruflo dispatches to Layer-2 workers (parallel)
                                      │ workers pull model tier per [[13-model-router]]
                                      │ read context from the Brain [[12-company-brain]]
                                      ▼
                              artifacts + confidence + provenance returned (§2)
                                      │
                                      ▼
                              Layer-1 gate (§6): accept / return / reject
                                      │ writes a decision record to the Brain
                          ┌───────────┴───────────┐
                       accept                    return/reject
                          │                         │
                          ▼                         ▼
                  next stage in the          back to worker with notes
                  Product Factory             (or escalate to you, §5.4)
                  (blueprint Part 7)
```

This loop is the company. Divisions `01`–`11` are specializations of the boxes; [[12-company-brain]] is
the memory the arrows read/write; [[13-model-router]] decides which model powers each Layer-2 box.

---

## 9. Design principles (the invariants)

- **Gates over autonomy.** Every "up" flow hits a human gate before it ships. Non-negotiable.
- **Files over chatter.** Durable work is a versioned file, not an ephemeral message.
- **Cheap by default, premium on the critical path.** Free/cheap models do volume; Claude does gates and
  hard reasoning ([[13-model-router]]).
- **The Brain is the team.** A one-person company's leverage is compounding memory ([[12-company-brain]]).
- **Sandbox the autonomous; never give it secrets.** The OpenClaw lesson (blueprint Part 9, [[09-security]]).
- **Consistency is a feature.** Every division file follows §3 so the whole thing stays operable by one
  person and resumable by a fresh chat.
