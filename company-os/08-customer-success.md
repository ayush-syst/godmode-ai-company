# 08 — Customer Success Division

> **Mission.** Keep paying customers happy, turn their feedback into product improvements, and catch
> churn before it happens — with minimal manual effort from you. Blueprint source: Part 3 (stage 13).
> **Layer: 2 (autonomous triage) + 1 (you handle escalations).**
> Powered by: **n8n + LLM triage + CrewAI feedback synthesis.** You handle every escalation personally.

---

## 1. Roles

| Role | One-line job |
|---|---|
| **Support Triage Agent** | Classify incoming support requests: type, urgency, sentiment, suggested response |
| **Auto-Responder** | Send templated or LLM-drafted answers for common/known issues |
| **Feedback Synthesizer** | Aggregate user feedback (support tickets, reviews, in-app, surveys) into themes and insights |
| **Churn Risk Monitor** | Detect early warning signals (low usage, cancellation intent, negative sentiment) |
| **Knowledge Base Agent** | Keep the public FAQ / help docs current as new questions arrive |

---

## 2. Layer mapping

| Role | Layer | Implementation |
|---|---|---|
| Support Triage | **2 (worker)** | n8n workflow + LLM classifier |
| Auto-Responder | **2 (worker)** | n8n + Groq/Gemini Flash (templated + LLM-drafted) |
| Feedback Synthesizer | **2 (worker)** | CrewAI agent; runs weekly |
| Churn Risk Monitor | **2 (worker)** | n8n cron + Supabase query on usage signals |
| Knowledge Base Agent | **2 (worker)** | CrewAI + n8n; adds FAQ entries after repeated questions |
| **Escalation handling** | **1 (you)** | All angry/complex/billing/refund cases come directly to you |

---

## 3. Inputs

| From | What |
|---|---|
| Users | Emails, in-app chat, support forms, app-store reviews |
| Supabase / product analytics | Usage events: login frequency, feature adoption, cancellation signals |
| [[06-marketing]] | Social mentions, community feedback |
| [[12-company-brain]] | `brain/brand/` voice; known issue list; FAQ content |

---

## 4. Outputs

| To | What | Written where |
|---|---|---|
| Users | Timely, helpful responses | Direct reply (email / in-app) |
| [[01-executive]] | Weekly feedback digest: top issues, churn signals, sentiment trend | Founder Dashboard + `tasks/<id>/feedback-digest.md` |
| [[03-product]] | User-validated pain points for next sprint | `brain/research/user-feedback-<date>.md` |
| [[12-company-brain]] | Promoted user language (gold for copy/marketing), FAQ updates | `brain/research/` + help docs |
| [[06-marketing]] | "What users love" — angles for marketing copy | `brain/brand/copy-patterns.md` |

---

## 5. Tools

| Tool | Purpose |
|---|---|
| **n8n** | Core automation: route tickets, trigger responses, schedule digests, fire churn alerts |
| **Supabase** | Usage data queries; power the churn risk monitor |
| **Groq / Gemini Flash** | LLM for response drafting and feedback classification |
| **Crisp / Chatwoot** (optional, self-hostable) | In-app chat widget with an API n8n can read/write |
| **CrewAI** | Weekly feedback synthesis crew |
| **Sentry** | Error monitoring — proactively catch and fix bugs before users report them |
| **Uptime-Kuma** | Uptime monitoring — alert you before users notice downtime |

---

## 6. Quality gates

| Gate | Trigger | Pass criteria | Fail action |
|---|---|---|---|
| **Auto-response quality (you, weekly sample)** | Every week, you spot-check 5 auto-responses | Accurate, empathetic, on-brand, not robotic | Improve the response templates / prompts |
| **Escalation routing** | Triage classifies a ticket as escalation | Lands in your inbox within 15 minutes | Fix the n8n routing rule |
| **Feedback digest review (you)** | Weekly digest arrives | You read it; anything product-critical gets a Task Contract to [[03-product]] | — |

---

## 7. Model routing

| Task | Default tier | Notes |
|---|---|---|
| Ticket classification | Free (Groq / Cerebras) | Fast, short output |
| Auto-response drafting | Free (Groq / Gemini Flash) | Reviewed by template; quality gate is your spot-check |
| Feedback synthesis | Free (Gemini Flash) | Long context; 1M ctx handles a month of tickets |
| Churn alert generation | n8n (rule-based) | No LLM needed — threshold triggers |

---

## 8. Memory

| Read | Write |
|---|---|
| `brain/brand/` — tone for responses | `brain/research/user-feedback-<date>.md` — synthesized themes |
| Known issues list (`brain/specs/` or a simple `brain/known-issues.md`) | `brain/brand/copy-patterns.md` — user language gold |
| Zep (bi-temporal) — per-user context, prior tickets | Zep — update user facts as they evolve (plan, satisfaction state) |

> **Zep's bi-temporal model is the right fit here**: a user's plan, satisfaction, and issues *change* over
> time; Zep invalidates stale facts rather than stacking contradictions. Use it for per-user context, not
> Mem0 (which is better for static per-agent memory). See [[12-company-brain]] §4.

---

## 9. Escalation triggers

All the following go directly to you:

- Any user expressing strong anger, threatening a chargeback, or threatening a public complaint.
- A billing or refund request of any size.
- A bug that results in data loss or a security concern.
- A question requiring a product commitment (roadmap promise, custom feature, SLA).
- A churn signal from a high-value user (top 20% by ARR).
- A support ticket that reveals a previously unknown product bug.

> **Rule: the triage agent must never say "we promise to ship X by Y."** Those responses are escalated
> to you. Feature commitments are product decisions, not support decisions.

---

## 10. Playbooks

### PLAY-CS1: Daily support triage

```
1. n8n polls support inbox / chat every 30 minutes.
2. Triage Agent classifies each ticket: type (bug / question / billing / feedback / churn-signal), urgency (low / medium / high / escalate).
3. Escalate-class: immediate notification to you.
4. Question/bug with a known answer: Auto-Responder drafts a reply from the FAQ/knowledge base and sends (or queues for you to approve, based on your confidence setting).
5. Unanswered bug: log to `brain/known-issues.md`, notify [[04-engineering]] if confirmed.
6. Feedback: queue for weekly synthesis run.
7. Knowledge Base Agent: if the same question appeared 3+ times this week, it auto-drafts a new FAQ entry for your review.
```

### PLAY-CS2: Weekly feedback digest

```
1. n8n triggers CrewAI Feedback Synthesizer at week end.
2. Agent reads: all support tickets + any app-store reviews + in-app feedback (if wired) from the past 7 days.
3. Produces: top 3 themes with counts, sentiment trend, one "user said it perfectly" quote per theme, churn signals flagged.
4. Digest pushed to Founder Dashboard and emailed to you.
5. You decide: which themes become Task Contracts for [[03-product]].
```

### PLAY-CS3: Churn intervention

```
1. Churn Risk Monitor detects: user hasn't logged in for 14 days, or a usage-drop signal, or a cancellation-page visit.
2. n8n notifies you immediately for high-value users. Auto-drafts a check-in message for low-value.
3. For high-value: you write a personal reply ("noticed you haven't been in — anything we can help with?").
4. If they respond with a problem: route to support triage + fast-track to [[03-product]] if it's a fixable issue.
5. Outcome logged in Zep and CRM.
```

---

## 11. KPIs / signals

| Signal | What it means | Bad state |
|---|---|---|
| Median first response time | Speed of triage + auto-response | > 4 hours = routing is broken |
| Resolution rate (auto) | % of tickets resolved without you | < 50% = FAQ/templates are incomplete |
| CSAT (if measured) | User satisfaction with support | < 4/5 = quality or empathy issue |
| Churn rate (monthly) | % of paying users cancelling | > 5%/month = retention crisis |
| Feedback → product conversion | % of synthesized themes turned into a Task Contract | < 20% = feedback is not informing product |
| Bug report → fix latency | Time from user-reported bug to fix in prod | > 1 week for a P1 = engineering pipeline is blocked |
