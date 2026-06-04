# 03 — Product Division

> **Mission.** Turn a validated idea into a precise, buildable spec — a PRD with acceptance criteria
> sharp enough that [[04-engineering]] can act on it without ambiguity. Blueprint source: Parts 3 & 7
> (Product Factory stages 1–4). **Layer: 1 (spec gates) + 2 (user research workers).**
> Powered by: **gstack `/plan-*-review` for gates; ruflo/CrewAI workers for user research and journey
> mapping.**

---

## 1. Roles

| Role | One-line job |
|---|---|
| **Product Manager (PM)** | Own the PRD from idea to approved spec; be the user's advocate in every trade-off |
| **Requirements Analyst** | Turn fuzzy "we should build X" into objective, testable acceptance criteria |
| **UX Researcher** | Gather user signals — jobs-to-be-done, pain points, existing workflow — from swarm research |
| **Customer Journey Mapper** | Map the full experience (awareness → onboarding → habit → referral) to find gaps |

---

## 2. Layer mapping

| Role | Layer | Implementation |
|---|---|---|
| **PM gate (plan reviews)** | **1 (gate)** | gstack `/plan-ceo-review` (is this the right thing?) + `/plan-eng-review` (can we build it?) |
| UX Researcher | **2 (worker)** | CrewAI crew: pulls user signals from Reddit/G2/AppStore/HN |
| Requirements Analyst | **2 → 1** | Draft on cheap model; you refine acceptance criteria before gate |
| Customer Journey Mapper | **2 (worker)** | CrewAI agent mapping the journey from research data |

The PM role is *you* (or Claude in the `/plan-ceo-review` interrogation). The spec itself is authored by
you with Claude, not by a fully autonomous agent — because specification quality is a quality gate, not a
volume task.

---

## 3. Inputs

| From | What |
|---|---|
| [[01-executive]] | Approved direction + research Task Contract results |
| [[02-research]] | Market research, competitor teardowns, Replication Engine output |
| [[12-company-brain]] | ICP definition, prior specs, brand/voice, decisions |
| [[05-design]] | Early design research or inspiration brief (sometimes feeds back into spec) |

---

## 4. Outputs

| To | What | Written where |
|---|---|---|
| [[01-executive]] | Draft PRD for plan-ceo-review gate | `tasks/<id>/prd-draft.md` |
| [[04-engineering]] | Approved PRD + acceptance criteria | `brain/specs/<product>-<feature>-<date>.md` |
| [[05-design]] | Design brief (problem, user, visual constraints, "wow" goal) | `tasks/<id>/design-brief.md` |
| [[12-company-brain]] | Approved spec (after gate) | `brain/specs/` |

---

## 5. Tools

| Tool | Purpose |
|---|---|
| **gstack `/plan-ceo-review`** | Gate: is this the right product/feature? |
| **gstack `/plan-eng-review`** | Gate: is this buildable as described? |
| **gstack `/autoplan`** | Generates an initial task breakdown from a loose idea (scaffolding for the PRD) |
| **CrewAI** | User research crew (UX Researcher + Journey Mapper agents) |
| **Firecrawl + browser-use** | Scrape app-store reviews, Reddit, G2, forums for user language and pain points |
| **ruflo MCP server** | Read `brain/` for ICP, prior specs, decisions |
| **n8n** | Route UX research Task Contracts to the swarm; collect results |

---

## 6. Quality gates

| Gate | Trigger | Pass criteria | Fail action |
|---|---|---|---|
| **`/plan-ceo-review`** | PM submits a PRD draft | Problem clearly defined; user & job-to-be-done named; success metric is measurable; scope has explicit "out" list; risk row filled in | Return with specific questions; rework |
| **`/plan-eng-review`** | After CEO review passes | Acceptance criteria are objective & checkable (no "fast", "good UX"); data model sketched; stack consistent with existing choices; no magic | Return with technical red flags; rework |
| **Acceptance criteria audit** (you) | Before emitting to [[04-engineering]] | Every user story has at least one acceptance criterion that a test can verify | Rewrite until testable |

---

## 7. Model routing

| Task | Default tier | Notes |
|---|---|---|
| UX research (scraping, Reddit/G2 synthesis) | Free (Gemini Flash) | Long context, high volume |
| Journey mapping | Free (Gemini Flash / Groq) | Structured output |
| PRD drafting (you + Claude) | **Premium (Claude)** | Spec quality = gate quality |
| `/plan-ceo-review` gate | **Premium (Claude)** | Always, per [[13-model-router]] gate exception |
| `/plan-eng-review` gate | **Premium (Claude)** | Always |

---

## 8. Memory

| Read | Write |
|---|---|
| `brain/specs/` — prior specs (patterns, anti-patterns) | `brain/specs/` — approved PRDs (after gate) |
| `brain/research/` — ICP, market context | `tasks/<id>/` — draft PRDs, research raw output |
| `brain/decisions/` — strategic choices that constrain scope | `brain/decisions/` — spec trade-offs captured |
| `brain/brand/` — voice, pricing norms, UX principles | |

---

## 9. Escalation triggers

Product agents / you escalate when:

- User research produces contradictory signals (can't agree on the core job-to-be-done).
- A scope decision has meaningful revenue implications (e.g., adding a feature that delays launch by
  3 weeks vs. shipping without it and possibly losing users).
- A regulatory finding from [[02-research]] changes what the product can legally do (India: DPDP Act,
  fintech rules).
- Engineering says a core requirement is technically infeasible within the budget/timeline.

---

## 10. Playbooks

### PLAY-P1: PRD from scratch

```
1. Receive approved direction from [[01-executive]] (a rough idea + research findings).
2. Run gstack /autoplan to scaffold the problem-solution-scope structure.
3. Dispatch UX research Task Contract to [[02-research]] if user signal is thin: "What do users say about <problem>?" (Firecrawl + Reddit + G2).
4. Write the PRD draft:
   - Problem / user / job-to-be-done
   - Success metric (one, measurable)
   - Scope: explicit IN and OUT
   - User stories (each → acceptance criteria)
   - Non-functional: perf, security (link to [[09-security]]), a11y
   - Open questions (escalation list)
5. Submit to /plan-ceo-review. Iterate until accepted.
6. Submit to /plan-eng-review. Iterate until accepted.
7. Promote to brain/specs/. Issue design brief to [[05-design]] and engineering Task Contract to [[04-engineering]].
```

### PLAY-P2: Feature addition to an existing product

```
1. Trigger: a retro action item, user feedback from [[08-customer-success]], or a growth finding from [[06-marketing]].
2. Read the existing product spec from brain/specs/ to understand the current contract.
3. Write an addendum spec (same schema, scoped to the change only).
4. /plan-ceo-review gate: is this the highest-value thing to build next?
5. /plan-eng-review gate: does this break existing contracts?
6. If accepted: update brain/specs/ and issue a scoped Task Contract to [[04-engineering]].
```

---

## 11. KPIs / signals

| Signal | What it means | Bad state |
|---|---|---|
| Spec acceptance rate (first pass) | % of PRD drafts that pass /plan-ceo-review without rework | < 50% = research-to-spec translation is weak |
| Acceptance criteria completeness | % of user stories with checkable criteria | < 100% = unacceptable (untestable spec) |
| Spec-to-build cycle time | Days from approved spec to engineering start | > 3 days = handoff friction |
| Scope creep rate | Features added post-approval / sprint | > 20% = spec discipline is breaking down |
