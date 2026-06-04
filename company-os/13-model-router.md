# 13 — The Model Router (token-credit optimizer)

> **Scope.** Operational expansion of [`00-MASTER-BLUEPRINT.md`](../00-MASTER-BLUEPRINT.md) Part 6. The
> blueprint sets the *principle* (critical path on Claude, everything else on free/cheap, routed by
> difficulty); this file is the *routing logic, the fallback chains, the quota-rotation and caching
> mechanics, and the budget guards*. The **implementation** is `bootstrap/litellm-config.yaml`; the
> **finance/ownership** side is [[11-finance-token-optimizer]]. Governed by [[00-architecture]].
>
> **One sentence:** one OpenAI-compatible endpoint (LiteLLM) in front of every model, routing each task to
> the *cheapest model that can do it well*, with Claude reserved for gates and hard reasoning.

---

## 1. The prime directive

> **The critical path runs on Claude (your $20 sub, via gstack). Everything parallel, cheap, or
> high-volume runs on free/cheap tiers, routed by difficulty.** A human gate ([[00-architecture]] §6) is
> the only thing that spends premium budget by default.

This is both a *quality* rule (Claude does the judgment that ships) and a *cost* rule (free tiers do the
volume that would otherwise bankrupt a $20/mo budget). The router enforces it mechanically so you don't
have to think about it per-task.

---

## 2. Model tiers (June 2026 — re-verify before relying)

**Premium — critical path / hard reasoning (spend deliberately):**

| Model | Why | Reserve for |
|---|---|---|
| **Claude (Opus/Sonnet)** via your sub | best agentic coding + judgment; native to gstack | gates, architecture, security review, gnarly bugs, final ship |
| Gemini 2.5 Pro | long context, strong reasoning, cheap PAYG | escalation target when Claude budget is tight |

**Cheap — bulk reasoning / coding workers (low PAYG):**

| Model | Cost | Strength |
|---|---|---|
| DeepSeek V3/R1 | very low (5M free at signup) | coding/reasoning per dollar |
| Qwen 2.5/3 Coder | 1M free (90-day), cheap | coding, multilingual |
| GLM (Zhipu) | cheap | solid general/coding |

**Free — high-volume swarm / research / drafts (rate-limited):**

| Provider | Free allowance | Best for |
|---|---|---|
| Google AI Studio — Gemini 2.5 Flash | ~1,500 req/day, 1M ctx, multimodal, no card | research, long-context, vision |
| Groq — Llama 3.3 70B | 300+ tok/s, ~1,000 req/day | fast cheap inference |
| Cerebras | ~60k tok/min, ~1,700 req/day | highest free throughput |
| OpenRouter (free models) | 50–200 req/day; $10 once → 1,000/day | aggregation + auto-routing |
| SambaNova | free via email | Llama/Qwen |
| Ollama (local) | unlimited (your hardware) | offline drafts, embeddings, privacy |

> **Honest note (blueprint Part 6 & 13):** free tiers are for *building*. The moment a product serves real
> users, its **production inference moves to paid/self-hosted with real SLAs** — budget for it as soon as
> there's revenue. "Free keys forever, unlimited" is a fantasy; the router plans around limits, it doesn't
> pretend they're absent.

---

## 3. The routing table (difficulty → model)

This is the table the router implements. A task's **class** (set in its Task Contract, [[00-architecture]]
§2) maps to a primary model + an ordered fallback chain.

| Task class | Primary (route to) | Fallback chain |
|---|---|---|
| Architecture, security review, gnarly bugs, **final ship / any gate** | **Claude (sub)** | Gemini 2.5 Pro → (stop; gates don't silently downgrade) |
| Routine code, tests, refactors (bulk) | DeepSeek / Qwen Coder | Groq Llama → Gemini Flash |
| Research, summarization, scraping triage | Gemini 2.5 Flash (free) | Cerebras → Groq |
| Content drafts, copy, social | free tier (Flash / Llama) | DeepSeek |
| Embeddings / memory | local (bge / nomic via Ollama) | cheap API |
| Classification / cheap glue | Groq 8B / Haiku | local |

> **Gate exception (critical):** tasks classed as a **gate** ([[00-architecture]] §6) **do not auto-fall
> back to a weaker model.** If Claude is unavailable, the gate *waits* or escalates to you — it never
> silently ships work that a cheaper model "approved." Quality of gates is the whole thesis.

---

## 4. The routing decision (algorithm)

For each request hitting the LiteLLM proxy:

```
1. Read class + model_tier + confidence from the Task Contract (default: cheap).
2. Is this a GATE task?  ── yes ─►  route to Claude. No downgrade. If unavailable → escalate/wait.
                          └─ no ──►  continue.
3. Cache check:
     a. exact prompt cache hit?      → return cached (cost = 0).
     b. semantic cache hit (≥ threshold)? → return cached.
4. Pick primary model for the class (§3).
5. Quota check (§6): does the primary tier have budget/req-quota left today?
     ── yes ─► call it.
     └─ no ──► rotate to next provider in the fallback chain (§5) with quota.
6. On error/timeout/ratelimit → next in fallback chain (retry with backoff).
7. Log {task, class, model, tokens, $, latency, cache_hit} to Langfuse (§8).
8. If a low-confidence result returns on a cheap model AND the stakes are high →
   re-route once to a stronger tier OR flag for a heavier gate ([[00-architecture]] §2).
```

**Confidence × tier interaction:** a cheap model returning low confidence on a high-stakes task is the
one case where the router *spends up* automatically — better to burn a little budget than to feed a gate
junk. Everything else trends cheap.

---

## 5. Fallback chains (reliability without premium spend)

Each class has an **ordered chain**, not a single model. The router walks it on quota-exhaustion or error:

```
research:   Gemini Flash → Cerebras → Groq 70B → DeepSeek
bulk-code:  DeepSeek → Qwen Coder → Groq → Gemini Flash
glue:       Groq 8B → local (Ollama) → Haiku
gate:       Claude → (wait / escalate)        # no weak fallback, by design
```

Chains are defined declaratively in `bootstrap/litellm-config.yaml` (LiteLLM `fallbacks:` +
`context_window_fallbacks:`). OpenRouter sits *inside* a chain as an aggregator for the long tail of
free/cheap models and as a router-of-last-resort.

---

## 6. Quota rotation (making free tiers behave)

Free tiers are rate- and quota-limited; the router tracks each and rotates *before* hitting a wall:

- **Track per provider:** requests today, tokens today, reset window — held in a small Redis/SQLite
  counter that [[11-finance-token-optimizer]] owns.
- **Rotate proactively:** at ~80% of a tier's daily quota, the router prefers the next provider in the
  chain so you never get hard-blocked mid-sprint.
- **Multi-key:** where ToS permits, rotate among several keys for the same provider (e.g. OpenRouter
  $10-tier keys) to multiply effective quota. **Respect each provider's ToS** — this is rotation across
  *your own* legitimate keys, not abuse.
- **Local safety net:** Ollama (unlimited, your hardware) is the final fallback for glue/draft/embedding
  work so the swarm never fully stalls when every free tier is exhausted.

---

## 7. Caching (the cheapest token is the one you don't spend)

| Layer | What it kills | Tech |
|---|---|---|
| **Prompt caching** | repeated system prompts / long stable context on Claude | Anthropic prompt cache (native) |
| **Semantic cache** | near-duplicate requests across the swarm | LiteLLM + Redis (embedding similarity) |
| **Artifact reuse** | re-deriving things already in the Brain | read [[12-company-brain]] before calling a model |

Order of operations in §4 puts cache checks *before* model selection — a cache hit is a $0, ~0ms answer.
For a swarm doing high-volume repetitive work (scraping triage, lead enrichment), semantic caching is
often the single biggest cost lever.

---

## 8. Cost observability (you can't optimize what you can't see)

- **Langfuse (self-host)** receives a trace for every call: task id, division, class, model, tokens, $,
  latency, cache-hit. This powers the **Token/cost panel** of the Founder Dashboard (blueprint Part 11)
  and the cost reports owned by [[11-finance-token-optimizer]].
- **LiteLLM** also logs per-key spend and enforces per-key budgets natively.
- **Attribution:** every call carries the originating `division` + `task id` (from the Task Contract), so
  cost is attributable to a division and a product — essential for knowing which product actually pays for
  its own inference.

---

## 9. Budget guards (hard stops, not just dashboards)

- **Per-key daily budget** in LiteLLM — a key that hits its cap fails closed (routes to free/local or
  stops), it doesn't quietly overspend.
- **Alert thresholds** at 50/80/100% of a budget → n8n → your dashboard/notification ([[10-infrastructure]]).
- **Premium budget fence:** a separate, small daily cap on Claude spend so a runaway loop can't drain the
  $20 sub's value in an afternoon. Gates still get priority within that fence.
- **Kill switch:** [[11-finance-token-optimizer]] can globally force-route everything to free/local tiers
  (degraded but $0) if spend anomalies trip.

---

## 10. Division → default tier (quick reference)

How each division's work maps to tiers by default (overridable per Task Contract):

| Division | Default tier | Premium only when |
|---|---|---|
| [[01-executive]] | **Claude** (it *is* the gates) | always — these are gates |
| [[02-research]] | free (Flash/Cerebras) | synthesizing a final strategic call |
| [[03-product]] | cheap → Claude at the plan gate | `/plan-ceo-review` |
| [[04-engineering]] | cheap (DeepSeek/Qwen) for bulk; **Claude** for `/review`, architecture, hard bugs | gate or gnarly |
| [[05-design]] | cheap for drafts; **Claude** for `/design-review` | gate |
| [[06-marketing]] | free | brand-voice-defining pieces (you approve) |
| [[07-sales]] | free | — |
| [[08-customer-success]] | free (triage) | escalations (you) |
| [[09-security]] | **Claude** for `/cso` reasoning; scanners are non-LLM | always at the gate |
| [[10-infrastructure]] | cheap | ship/canary decisions |
| [[11-finance-token-optimizer]] | free/local | — (it runs the router itself) |

---

## 11. Worked example

> **Task:** "Write integration tests for the auth module." Class = `bulk-code`, tier = `cheap`, gate =
> `/review`.

1. Router sees class `bulk-code`, not a gate → cache miss → primary **DeepSeek**.
2. DeepSeek quota OK → generates tests; returns confidence 0.82 + provenance.
3. Logged to Langfuse: DeepSeek, 18k tokens, $0.01, 6s.
4. Artifact returns to the **`/review` gate** ([[04-engineering]]) — *that* call runs on **Claude** (gate
   exception, §3). Claude finds two missing edge cases → returns the task with notes.
5. Worker re-runs on DeepSeek (cheap) to fix; re-gates on Claude; accepted.

Net: ~90% of the tokens were cheap; Claude's premium budget bought only the *judgment* at the gate. That
ratio — cheap volume, premium judgment — is the router working correctly.

---

## 12. Implementation pointer

- Declarative config: **`bootstrap/litellm-config.yaml`** (model list, fallback chains, budgets, cache).
- Keys: **`bootstrap/.env`** (git-ignored — never committed; see [[09-security]]).
- Start: `litellm --config bootstrap/litellm-config.yaml`; point all agents (gstack, ruflo, OpenHands,
  CrewAI) at that one endpoint.
- Ownership, quotas, cost reporting, kill switch: [[11-finance-token-optimizer]].
