# 11 — Finance & Token-Credit Optimizer

> **Mission.** Keep the company financially sane — track revenue, watch costs, and (critically) enforce
> the token/model-routing budget so a $20/mo Claude subscription powers a company-grade AI stack without
> running out mid-sprint. Blueprint source: Parts 3 & 6. **Layer: service** (cross-cutting, owned by
> no single division but consumed by all). Powered by: **LiteLLM + OpenRouter + Langfuse + Stripe/
> Razorpay webhooks + n8n.** You are the CFO; this division gives you the numbers.

---

## 1. Roles

| Role | One-line job |
|---|---|
| **CFO (you)** | Own the financial strategy: pricing, runway, when to upgrade/downgrade |
| **Token Budget Controller** | Enforce per-division, per-key, per-day model spend limits via LiteLLM |
| **Cost Attribution Agent** | Tag every LLM call with division + product + task id for cost-by-product reporting |
| **Quota Rotation Manager** | Track free-tier daily limits per provider; rotate keys proactively before hitting walls |
| **Revenue Tracker** | Aggregate MRR/ARR from Stripe/Razorpay; push to Founder Dashboard |
| **Financial Health Monitor** | Alert on anomalies: sudden cost spike, declining revenue, quota wall hit |

---

## 2. Layer mapping

| Role | Layer | Implementation |
|---|---|---|
| CFO | **1 (you)** | Weekly dashboard review; strategic decisions |
| Token Budget Controller | **service (automated)** | LiteLLM per-key budget limits |
| Cost Attribution Agent | **service (automated)** | LiteLLM + Langfuse tags per call |
| Quota Rotation Manager | **service (automated)** | Redis/SQLite counter + n8n logic |
| Revenue Tracker | **service (automated)** | n8n + Stripe/Razorpay webhooks → Supabase → Dashboard |
| Financial Health Monitor | **service (automated)** | n8n + threshold alerts → you |

---

## 3. Inputs

| From | What |
|---|---|
| LiteLLM proxy | Every model call: model, tokens, cost, latency, division tag |
| Langfuse | Trace-level cost data: per task, per agent, per session |
| Stripe / Razorpay | Payment events: new subscription, cancellation, upgrade, chargeback |
| Cloud provider (Hetzner/OVH, Supabase) | Infrastructure spend |
| Free-tier providers | Daily quota status (polled by Quota Rotation Manager) |

---

## 4. Outputs

| To | What | Written where |
|---|---|---|
| [[13-model-router]] | Today's remaining quota per provider | Redis/SQLite counter (read by LiteLLM) |
| All divisions | Budget status (are we near a wall?) | LiteLLM enforced limits (requests fail → route fallback) |
| [[01-executive]] | Weekly financial summary: MRR, infra cost, LLM cost, % budget used | Founder Dashboard + `tasks/<id>/finance-report.md` |
| [[12-company-brain]] | Financial decisions (pricing changes, budget increases) | `brain/decisions/` |

---

## 5. Tools

| Tool | Purpose |
|---|---|
| **LiteLLM** (`BerriAI/litellm`) | The router and budget-enforcement layer; one endpoint for all models |
| **OpenRouter** | Aggregator for free/cheap models; sits behind LiteLLM |
| **Langfuse** (`langfuse/langfuse`, self-hosted) | Cost + latency observability; per-task attribution |
| **Redis** (or SQLite) | Quota counters per provider; fast read/write by the rotation manager |
| **n8n** | Alert routing; revenue webhook processing; scheduled quota checks |
| **Stripe** | International payments (if product targets non-India or accepts cards) |
| **Razorpay** | India-first payments: UPI, cards, netbanking, EMI — required for India market |
| **Supabase** | Persist revenue events and cost history for the Dashboard |

---

## 6. LiteLLM configuration overview

The full config lives in `bootstrap/litellm-config.yaml`. The spec here captures the *logic*:

```yaml
# Routing: maps model aliases to real endpoints
# Budget enforcement: per-key daily caps
# Fallbacks: the fallback chains from [[13-model-router]] §5
# Caching: prompt cache (Claude) + semantic cache (Redis)
# Callbacks: Langfuse for every call

model_list:
  - model_name: claude-gate        # alias for Layer-1 gates
    litellm_params:
      model: claude-opus-4-8
      api_key: $ANTHROPIC_API_KEY

  - model_name: bulk-code          # alias for Layer-2 coding workers
    litellm_params:
      model: deepseek/deepseek-coder
      api_key: $DEEPSEEK_API_KEY

  - model_name: research-free      # alias for research workers
    litellm_params:
      model: gemini/gemini-2.5-flash
      api_key: $GEMINI_API_KEY

  # ... (full list in bootstrap/litellm-config.yaml)

budget_manager:
  total_budget: 15.00              # $15/mo of the $20 Claude sub reserved for this
  max_budget: 0.50                 # max $0.50 per gate call
  budget_duration: monthly

success_callback: ["langfuse"]
failure_callback: ["langfuse"]
```

> The **$15 total** is a guideline: the remaining $5 is the buffer for overruns and admin. Re-calibrate
> monthly based on Langfuse actuals. If all gates are running within budget, you can raise the
> budget; if you're hitting walls, first check whether non-gate work is accidentally routing to Claude.

---

## 7. Quota rotation (operational)

Governed by [[13-model-router]] §6. The operational piece here:

- **Counter store:** a tiny Redis instance (or a Supabase table if Redis is overkill) holds:
  `{provider: {requests_today: N, tokens_today: N, reset_at: <timestamp>}}`.
- **n8n cron (hourly):** polls each free-tier provider's usage endpoint (where available) or estimates
  from Langfuse data; updates the counters.
- **LiteLLM reads the counters** before routing: if a provider's quota is > 80% used, weight it down in
  the fallback chain for the remainder of the day.
- **Reset:** counters reset at midnight UTC (or per-provider reset window).

---

## 8. Revenue tracking (operational)

```
Stripe/Razorpay webhook → n8n → Supabase revenue table
  columns: event_type, product, amount_inr, amount_usd, user_id, timestamp

n8n daily cron: SELECT and compute:
  - MRR: sum of active subscriptions × monthly price
  - ARR: MRR × 12
  - New MRR, churned MRR, expansion MRR
  → push to Founder Dashboard panel "Revenue"
```

> Razorpay is the default for India products (UPI + cards + bank transfer). Add Stripe if you're selling
> internationally. Both have n8n nodes or webhook support.

---

## 9. Quality gates

| Gate | Trigger | Pass criteria | Fail action |
|---|---|---|---|
| **Monthly budget review (you)** | First of every month | Langfuse actuals match expectation; no division is egregiously over-budget; free-tier quota utilization is efficient | Adjust routing config; tighten per-division caps |
| **Cost anomaly alert** | Any call that's 10× the expected cost | Auto-alert via n8n; you investigate | Find the runaway loop; fix the routing |
| **Free-tier wall alert** | Any provider hits 90% of daily quota | LiteLLM automatically routes to fallback; n8n notifies you | Verify fallback is working; add a provider if needed |
| **Revenue anomaly alert** | MRR drops > 10% week-over-week | n8n alert to you | Check churn signals in [[08-customer-success]] |

---

## 10. Model routing

The Finance division *owns* the router; it doesn't consume Claude for most tasks. n8n workflows are
rule-based (no LLM). Langfuse analysis queries run locally or on free-tier.

| Task | Tier | Notes |
|---|---|---|
| Financial health monitoring | n8n (no LLM) | Threshold rules, not reasoning |
| Revenue report generation | Free (Gemini Flash) | Summarize structured data |
| Budget analysis for you | Cheap (DeepSeek) | Once-a-month; short analysis |
| Strategic pricing advice | **Premium (Claude)** | Via `/office-hours` in [[01-executive]] |

---

## 11. Memory

| Read | Write |
|---|---|
| `brain/decisions/` — prior pricing and budget decisions | `brain/decisions/` — pricing changes, budget increases |
| Langfuse data (external, not brain/) | Supabase revenue table (persistent cost/revenue history) |
| Zep — facts that change: current pricing, active plan per user | Zep — update when pricing or user plan changes |

---

## 12. Escalation triggers

Finance alerts you when:

- Claude budget is > 80% used for the month and there are > 10 days remaining.
- Any single LLM call costs > $1 (runaway loop or wrong model routing).
- A free-tier provider goes down or changes its limits (re-verify ToS + limits immediately).
- MRR declines two consecutive weeks.
- Infra spend exceeds the monthly budget by > 20%.
- A payment provider changes their India regulatory requirements (GST, TDS, DPDP Act compliance for
  payment data).

---

## 13. Playbooks

### PLAY-F1: Monthly financial review

```
1. n8n triggers on the 1st of each month.
2. Pull from Langfuse: total LLM spend by division, by model, by task class.
3. Pull from Supabase: MRR, new users, churned users, infra spend.
4. Pull from free-tier providers: quota usage averages for the past month.
5. Generate a 1-page report: where we spent, where we could have saved, routing efficiency.
6. Push to Founder Dashboard. You review and adjust litellm-config.yaml if needed.
7. Write a Decision Record if you make a routing change.
```

### PLAY-F2: Add a new free-tier API key

```
1. Sign up for the new provider (Gemini / Groq / Cerebras / etc.).
2. Check: daily quota, reset window, ToS (are they allowing this use case? is data sent to China?).
3. Add key to .env (never to git; never to brain/).
4. Add to litellm-config.yaml: model entry + fallback chain position + daily quota counter.
5. Test: run a lightweight request through the LiteLLM proxy; verify it routes correctly.
6. Update the quota rotation manager counter config.
7. Decision Record: which provider, what quota, what we use it for, any ToS notes.
```

### PLAY-F3: Respond to a Claude budget alert (> 80% with > 10 days left)

```
1. Open Langfuse: which division is consuming the most?
2. Check: is it a legitimate gate (Layer-1)? Or is non-gate work accidentally routing to Claude?
3. If accidental: fix the model_tier in the affected Task Contracts; update litellm-config.yaml routing.
4. If legitimate and budget is tight: temporarily lower the max_budget per call; accept slightly longer gate latency.
5. If truly over-budget for the month: consider which sprints can wait; don't spawn more gates than needed.
6. Note the adjustment in brain/decisions/ so you know why the config changed.
```

---

## 14. KPIs / signals

| Signal | What it means | Bad state |
|---|---|---|
| Claude spend vs. plan | % of $20 sub used by mid-month | > 60% at mid-month = over-spending on gates |
| Free-tier utilization | % of free-quota used per provider | < 40% = we're paying for things we could get free; > 90% = quota walls hit often |
| LLM cost per product | $ per product per month | Trending up without revenue growth = efficiency problem |
| Revenue vs. infra cost | Gross margin on infra | Negative at Scale tier = pricing or infra choice problem |
| MRR growth (monthly) | Revenue trajectory | Flat for 2+ months post-launch = growth problem |
| Budget alert frequency | # of anomaly alerts per month | > 2/month = routing config needs tightening |
