# 07 — Sales Division

> **Mission.** Find the right people, start the right conversations, and move them to paying customers —
> without a sales team and without cold-calling vibes. Blueprint source: Part 3 (stage 12).
> **Layer: 2 (autonomous swarm).** Powered by: **CrewAI + n8n + a lightweight CRM.**
> You approve every outreach sequence before it sends. You handle every non-template conversation.

---

## 1. Roles

| Role | One-line job |
|---|---|
| **Lead Discovery Agent** | Find potential customers who match the ICP across LinkedIn, communities, directories, and inbound signals |
| **Qualification Agent** | Score each lead: company size, role fit, signal strength, India-market relevance |
| **Outreach Writer** | Craft personalized cold messages (email/LinkedIn/WhatsApp) — non-spammy, specific, short |
| **CRM Manager** | Maintain the lead pipeline: stage, last contact, next action, notes |
| **Follow-up Agent** | Time and draft follow-up sequences based on engagement signals |

---

## 2. Layer mapping

| Role | Layer | Implementation |
|---|---|---|
| Lead Discovery | **2 (worker)** | CrewAI agent + browser-use + LinkedIn scraping (within ToS) |
| Qualification | **2 (worker)** | CrewAI agent; scoring rubric on cheap model |
| Outreach Writer | **2 (worker)** | CrewAI agent — drafts, you approve |
| CRM Manager | **2 (worker)** | CrewAI agent + n8n (reads/writes Twenty or a Supabase table) |
| Follow-up | **2 (worker)** | CrewAI + n8n scheduler |
| **Outreach approval** | **1 (gate — you)** | You review and approve every sequence before it goes live |
| **Non-template replies** | **1 (you)** | You write or approve all real conversation replies |

---

## 3. Inputs

| From | What |
|---|---|
| [[03-product]] | ICP definition: role, company size, pain signal, India geography |
| [[12-company-brain]] | `brain/brand/` — messaging, positioning, pricing |
| [[08-customer-success]] | Churn signals and "what users love" — gold for outreach angles |
| [[06-marketing]] | High-intent inbound leads (from content / ProductHunt / directories) |

---

## 4. Outputs

| To | What | Written where |
|---|---|---|
| You (for approval) | Draft outreach sequences | `tasks/<id>/outreach-draft.md` |
| CRM | Enriched lead records + pipeline stage | CRM (Twenty / Supabase `leads` table) |
| [[01-executive]] | Conversion rate, pipeline health, deal signals | Founder Dashboard |
| [[12-company-brain]] | Winning messages, ICP refinements (after real feedback) | `brain/brand/outreach-patterns.md` |

---

## 5. Tools

| Tool | Purpose |
|---|---|
| **CrewAI** | Orchestrate the five-role sales crew |
| **n8n** | Sequence scheduling; CRM update webhooks; inbound lead routing |
| **browser-use** | Find leads on LinkedIn, communities, IndieHackers, Twitter/X |
| **Twenty** (open-source CRM, ~14k⭐) | Self-hosted CRM with a clean API; free, MIT licensed |
| **Supabase** | Alt: a `leads` table in your existing Supabase instance |
| **Groq / Gemini Flash** | Drafting outreach — cheap and fast |
| **Apollo.io free tier** | 50 free email enrichments/month — use for the best qualified leads |
| **Hunter.io free tier** | Email finder (25 free/month) |

---

## 6. Quality gates

| Gate | Trigger | Pass criteria | Fail action |
|---|---|---|---|
| **Outreach sequence review (you)** | Outreach Writer submits a draft | Specific to the recipient (not obviously templated); accurate claim about their pain; one clear ask; no spam trigger words; consistent with `brain/brand/` voice | Rewrite; update the prompts |
| **Qualification threshold** | Qualification agent scores a lead | Score ≥ threshold (e.g., ≥ 3/5) before any outreach is attempted | Discard or hold for a later quarter |
| **Non-template reply review (you)** | Any substantive reply from a prospect | You read it; you decide; you reply or approve the drafted reply | Hold; escalate to you |

---

## 7. Model routing

| Task | Default tier | Notes |
|---|---|---|
| Lead discovery | Free (Gemini Flash + browser-use) | Volume search |
| Lead qualification scoring | Free (Groq / Cerebras) | Structured rubric, short output |
| Outreach drafting | Free (Groq / Gemini Flash) | Reviewed by you before sending; quality bar is your gate |
| CRM updates | n8n (no LLM needed) | Simple field updates from structured data |

---

## 8. Memory

| Read | Write |
|---|---|
| `brain/brand/` — messaging, ICP, voice | `brain/brand/outreach-patterns.md` — what copy got replies |
| CRM — existing leads, pipeline stages | CRM — new leads, stage updates, notes |
| ruflo AgentDB — SONA patterns for outreach angles | ruflo AgentDB — update SONA after each campaign result |

---

## 9. Escalation triggers

Sales agents escalate to you when:

- A prospect replies with anything substantive (interest, objection, negotiation).
- A potential deal is above a meaningful revenue threshold (you take all calls personally at this stage).
- A prospect's use case doesn't fit the ICP but seems valuable anyway (product discovery opportunity).
- Legal/contract questions arise (pricing, terms, data handling).
- A channel (cold email, WhatsApp, LinkedIn) is getting flagged as spam or hits a platform limit.

---

## 10. Playbooks

### PLAY-S1: ICP lead list build

```
1. Receive ICP from [[03-product]]: role (e.g., "founder or head of ops"), company size (1–50), geography (India), pain signal (e.g., "using spreadsheets for <workflow>").
2. Lead Discovery Agent: scrape LinkedIn (Sales Navigator if available; public search otherwise), IndieHackers, Twitter/X lists, relevant Slack/Discord communities.
3. Qualification Agent: score each lead (role match, company fit, signal strength, estimated budget).
4. Filter to top 20–50 qualified leads → write to CRM.
5. Report to you: "20 leads ready for outreach — here's the list." You approve the list before any outreach.
```

### PLAY-S2: Cold outreach sequence

```
1. Receive: list of qualified leads from CRM.
2. Outreach Writer: for each lead, draft a 3-touch sequence:
   - Message 1: "here's a specific thing I noticed about you + one-sentence value prop + one ask."
   - Message 2 (4 days later): short follow-up with a different angle or social proof.
   - Message 3 (7 days later): "last ping — here's a quick demo or a relevant case study."
3. You review the full sequence for lead #1 (representative sample). Approve, edit, or block.
4. If approved: n8n schedules and sends via email or LinkedIn. Auto-pause when a reply comes in.
5. CRM Manager updates stages and notes automatically via n8n webhook.
6. After each campaign: measure reply rate; update SONA patterns.
```

### PLAY-S3: Inbound lead handling

```
1. n8n detects inbound signal (form fill, demo request, a mention on social).
2. Qualification Agent scores the lead.
3. If qualified: notify you immediately (Founder Dashboard / push notification).
4. You respond personally within 24 hours. This is not delegated.
5. CRM Manager logs the conversation and next action.
```

---

## 11. KPIs / signals

| Signal | What it means | Bad state |
|---|---|---|
| Reply rate | % of outreach sequences getting any reply | < 5% = messaging is off or list is unqualified |
| Qualified lead → demo rate | % of qualified leads who book a call | < 10% = outreach copy is weak |
| Demo → paid conversion | % of demos that convert | < 20% = product/pricing fit issue, not a sales issue |
| Pipeline size | Qualified leads in active pipeline | < 20 = lead generation needs a sprint |
| CRM hygiene | % of leads with an up-to-date stage and next action | < 80% = the CRM Manager is falling behind |
