# 02 — Research Division

> **Mission.** Produce high-quality, sourced intelligence — market signals, competitor teardowns,
> opportunity scores — that the Executive and Product divisions base decisions on. This division
> *generates evidence*, it does not make decisions. Blueprint source: Parts 3 & 8.
> **Layer: 2 (autonomous swarm).** Powered by: **CrewAI + browser-use + Firecrawl + free models.**
> All output returns to a **Layer-1 gate** ([[01-executive]]) before any decision is made on it.

---

## 1. Roles

| Role | One-line job |
|---|---|
| **Market Analyst** | Size markets (TAM/SAM/SOM), identify demand signals, track India-specific trends |
| **Competitor Scout** | Map the competitive landscape: incumbents, features, pricing, weaknesses |
| **Opportunity Finder** | Source startup candidates for the Replication Engine (YC, ProductHunt, Crunchbase, G2) |
| **Trend Watcher** | Monitor technology and consumer behavior shifts relevant to active products |
| **Regulation Analyst** | Flag India-specific compliance requirements (DPDP Act, GST, fintech, health) |

---

## 2. Layer mapping

| Role | Layer | Implementation |
|---|---|---|
| All five | **2 (swarm workers)** | CrewAI role-based agents |
| Orchestrator | **2** | CrewAI Crew manager (dispatched by a Task Contract from Layer 1) |
| **Synthesis review** | **1 (gate)** | You + `/office-hours` review the final research report |

Layer-2 agents do parallel sourcing, scraping, and summarizing. The synthesized report hits a Layer-1
gate before any strategic decision is made on it. Raw scrapes never go into `brain/` — only curated
findings do ([[12-company-brain]] §2).

---

## 3. Inputs

| From | What |
|---|---|
| [[01-executive]] | A Task Contract with: topic, question to answer, depth (quick/deep), time-box, sources to prefer |
| [[12-company-brain]] | Prior research in `brain/research/` (so agents don't duplicate) |
| [[03-product]] | User/ICP questions for demand validation |
| [[11-finance-token-optimizer]] | Daily free-tier quota available (governs how many parallel web calls to make) |

---

## 4. Outputs

| To | What | Written where |
|---|---|---|
| [[01-executive]] | Curated research report with provenance + confidence score | `tasks/<id>/research-report.md` (proposal) |
| [[12-company-brain]] | Promoted, curated findings after gate approval | `brain/research/<topic>-<date>.md` |
| [[bootstrap/replication-engine]] | Scored startup candidates (the rubric output, blueprint Part 8) | `tasks/<id>/replication-candidates.md` |

---

## 5. Tools

| Tool | Purpose |
|---|---|
| **CrewAI** (`crewAIInc/crewAI`) | Role-based agent crews; easy to instantiate five agents with one config |
| **browser-use** | Agents drive a real browser: scrape live pages, read dynamic content |
| **Firecrawl** (`mendableai/firecrawl`) | Clean web→markdown for bulk URL-to-text conversion (no JS needed) |
| **Google AI Studio — Gemini Flash** | Free, 1M context, multimodal — the default model for all five roles |
| **Groq — Llama 3.3 70B** | Fallback for fast text synthesis when Gemini quota is thin |
| **Cerebras** | Highest free throughput — use for classification/triage passes |
| **OpenRouter** | Aggregator fallback for the long tail |
| **Ruflo MCP server** | Reads the Brain (prior research, decisions) for context-injection into each agent |
| **n8n** | Scheduled research runs (weekly trend watch, monthly competitor refresh) |

---

## 6. Quality gates

| Gate | Trigger | Pass criteria | Fail action |
|---|---|---|---|
| **CEO review (`/office-hours`)** | Research report submitted in `tasks/` | Every claim has a cited source; TAM numbers are triangulated (at least 2 independent sources); confidence score ≥ 0.7; no hallucinated data | Return to crew with specific gaps; re-run targeted sub-tasks |
| **Promotion gate (you)** | After CEO accepts the report | Finding is non-obvious AND sourced → enters `brain/research/` | Raw dump stays in `tasks/` only |

> **Provenance rule (non-negotiable):** every statistic, quote, or competitive claim must cite its source
> URL and date accessed. Research without provenance is not accepted. This is enforced by the acceptance
> criteria in every Task Contract issued to this division.

---

## 7. Model routing

| Role | Default tier | Rationale |
|---|---|---|
| Market Analyst | Free (Gemini Flash) | Long context, good reasoning, 1,500 req/day |
| Competitor Scout | Free (Gemini Flash) | Browser-use results are long; need 1M ctx |
| Opportunity Finder | Free (Gemini Flash) | Volume over quality for sourcing passes |
| Trend Watcher | Free (Groq / Cerebras) | Fast, short summaries |
| Regulation Analyst | Cheap (DeepSeek) | Regulatory text is specialized; worth a small spend |
| Synthesis (final report) | Cheap (DeepSeek / Qwen) | One call; high quality needed for the gate |

See [[13-model-router]] §3 for the full table. The gate review runs on Claude (premium), per the gate
exception.

---

## 8. Memory

| Read | Write |
|---|---|
| `brain/research/` — prior findings (avoid duplicating) | `brain/research/` — promoted curated findings (after gate) |
| `brain/decisions/` — strategic choices the research must serve | `tasks/<id>/` — raw outputs (proposals, never authoritative) |
| `brain/brand/` — ICP definition, target market | (raw scraped data stays in `tasks/` only) |
| ruflo AgentDB — SONA patterns for "which source type yielded best results" | ruflo AgentDB — update SONA after each crew run |

---

## 9. Escalation triggers

Research agents escalate to [[01-executive]] (you) when:

- A competitor or regulatory finding materially changes the product strategy (e.g., a strong incumbent
  just launched the exact same idea, or a new law makes the product non-compliant).
- Confidence on a core assumption (TAM, demand) can't exceed 0.5 after two crew runs.
- A data source requires payment, signup, or access that the agent can't do autonomously.
- A research question can't be answered from public sources alone and needs founder input or network.

---

## 10. Playbooks

### PLAY-R1: Competitor teardown

```
1. Receive Task Contract: target = <competitor name/URL>, depth = shallow | deep.
2. Crew: Competitor Scout runs browser-use + Firecrawl over the target's site, G2/Trustpilot reviews, job postings, pricing page, changelog.
3. Synthesize: pricing, feature set, positioning, growth signals, weaknesses, customer complaints.
4. Trend Watcher adds context: is this space growing or stagnating?
5. Write teardown report in tasks/<id>/ with confidence + provenance.
6. Submit to [[01-executive]] for CEO gate.
7. If accepted: promote to brain/research/<competitor>-teardown-<date>.md.
```

### PLAY-R2: Startup Replication Engine sourcing (blueprint Part 8)

```
1. Receive Task Contract: "Find US startups in <category> suitable for India replication."
2. Opportunity Finder: scrape YC (last 3 cohorts), ProductHunt (top of <category>), Crunchbase, G2.
3. Market Analyst: for each candidate, score the 8-dimension rubric (TAM ×3, demand evidence ×3, competition gap ×2, build feasibility ×3, regulatory load ×2 inverse, distribution path ×3, monetization ×2, moat potential ×1).
4. Regulation Analyst: flag any that carry DPDP Act / GST / fintech / health compliance load.
5. Produce a ranked shortlist (top 5) with weighted scores + a one-paragraph build brief for #1.
6. Submit to [[01-executive]] CEO gate.
7. If accepted: write to brain/research/replication-candidates-<date>.md and feed to [[03-product]].
```

### PLAY-R3: Scheduled market pulse (weekly/monthly via n8n)

```
1. n8n cron triggers a lightweight CrewAI crew (Trend Watcher + Market Analyst).
2. Agents check: Google Trends for key terms, HackerNews "Ask HN" / "Show HN" for signal, Reddit communities for target ICP, ProductHunt for new entrants.
3. If a significant signal is found → write a brief note to tasks/ and notify [[01-executive]] via the Founder Dashboard.
4. No gate needed for routine pulses; only promoted to brain/ if it changes strategy.
```

---

## 11. KPIs / signals

| Signal | What it means | Bad state |
|---|---|---|
| Gate acceptance rate | % of research reports accepted on first submission | < 60% = agents are producing low-quality / unsourced work |
| Sourcing latency | Time from Task Contract to report submission | > 4 hours for a shallow teardown = tool or quota issue |
| Provenance coverage | % of claims with cited sources | < 100% = not acceptable |
| Brain promotion rate | % of accepted reports promoted to `brain/research/` | < 50% = research isn't being captured for compounding |
| Replication Engine throughput | Candidates scored per run | < 3 = scraping is blocked; increase sources or fix browser-use |
