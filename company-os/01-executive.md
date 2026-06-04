# 01 — Executive Division

> **Mission.** Hold the quality, cost, and strategic direction of the whole company. Every major decision
> is either made here or escalated here. Blueprint source: Parts 3 & 7. **Layer: 1 (exclusively).**
> Powered by: **gstack skills on Claude** (your $20 sub). This division is human-triggered — *you* run
> each skill at each gate. No autonomous agents here by design.

---

## 1. Roles

| Role | One-line job |
|---|---|
| **CEO** | Set direction, arbitrate trade-offs, approve strategy and major decisions |
| **CTO** | Own the technical architecture, engineering quality bar, and infrastructure choices |
| **CPO** | Own the product vision, roadmap priority, and user-outcome definitions |
| **CFO** | Own the budget, model spend, token quota, and financial health signals |
| **CSO** | Own the security posture, threat model, and incident response readiness |
| **COO** | Own the operational rhythm: sprint cadence, retros, cross-division flow |

> **Important:** these are not six separate autonomous agents. They are **six lenses** you apply to
> decisions, surfaced via gstack skills that interrogate Claude. The CEO lens fires in `/office-hours`; the
> CTO and CPO lenses fire in `/plan-eng-review` and `/plan-ceo-review`; the CSO lens fires in `/cso`; the
> COO/retro lens fires in `/retro`. You carry the CFO lens yourself, assisted by [[11-finance-token-optimizer]].

---

## 2. Layer mapping

| Role | Layer | Implementation | Trigger |
|---|---|---|---|
| CEO | **1 (gate)** | gstack `/office-hours` | You run it when direction-setting is needed |
| CTO | **1 (gate)** | gstack `/plan-eng-review` + `/review` | You run before architecture decisions |
| CPO | **1 (gate)** | gstack `/plan-ceo-review` | You run before spec approval |
| CSO | **1 (gate)** | gstack `/cso` | Fires at every pre-ship security gate |
| COO | **1 (gate)** | gstack `/retro` | Fires at sprint/launch end |
| CFO | **1 (human)** | You + [[11-finance-token-optimizer]] dashboard | Continuous, not a discrete gstack skill |

---

## 3. Inputs

| From | What |
|---|---|
| **You (Layer 0)** | A question, a new idea, a risk concern, a strategic trade-off |
| [[02-research]] | Research reports, competitor teardowns, opportunity shortlists |
| [[03-product]] | Draft specs/PRDs needing CEO/CPO review |
| [[04-engineering]] | Architecture proposals needing CTO review; incident reports |
| [[09-security]] | Security scan results, incident flags needing CSO review |
| [[11-finance-token-optimizer]] | Spend anomalies, budget alerts, quota warnings |
| [[12-company-brain]] | Prior decisions, playbooks, retros (context for every gate) |

---

## 4. Outputs

| To | What | Written where |
|---|---|---|
| [[03-product]] | Approved spec direction | `brain/decisions/` + the approved spec in `brain/specs/` |
| [[04-engineering]] | Approved architecture / plan | `brain/decisions/` + Task Contract |
| [[02-research]] | Directed research Task Contract | `tasks/` |
| All divisions | Gate accept/return/reject + rationale | `brain/decisions/` (Decision Record, [[12-company-brain]] §6) |
| [[12-company-brain]] | Retro findings promoted to playbooks | `brain/retros/` + `brain/playbooks/` |

---

## 5. Tools

| Tool | gstack skill | Purpose |
|---|---|---|
| `gstack` | `/office-hours` | CEO interrogation: ruthless questioning of strategy, positioning, pricing, priority |
| `gstack` | `/plan-ceo-review` | CPO gate: product/spec soundness — is this the right thing to build? |
| `gstack` | `/plan-eng-review` | CTO gate: architecture soundness — is this the right way to build it? |
| `gstack` | `/cso` | CSO gate: OWASP/STRIDE security review — is this safe to ship? |
| `gstack` | `/retro` | COO/CEO: sprint/launch retrospective → playbook improvements |
| `gstack` | `/investigate` | Deep-dive on a specific unknown or incident |
| `gstack` | `/autoplan` | Generates a task breakdown from a loose idea (feeds Layer 2) |

---

## 6. Quality gates

The Executive division *is* the gate system; it doesn't pass through someone else's gate. Its own quality
bar is enforced by you:

| Gate | Triggered by | Pass criteria | Fail action |
|---|---|---|---|
| Strategy (`/office-hours`) | You, on any directional question | Claude can't find a fatal flaw; you feel confident | Rethink; re-run with the challenge exposed |
| Plan-CEO review | [[03-product]] submitting a spec | The PRD answers: user, problem, success metric, scope, risk | Return to [[03-product]] with specific questions |
| Plan-eng review | [[04-engineering]] submitting architecture | No fundamental design flaws; stack consistent with constraints | Return with CTO-level critique |
| Security (CSO `/cso`) | Before every ship | Zero critical/high vulns; STRIDE threats addressed | Block ship; file Task Contract to [[09-security]] |
| Retro (`/retro`) | End of each sprint/launch | Learnings are specific, actionable, written | Redo — vague retros compound nothing |

---

## 7. Model routing

All executive gates run on **Claude (premium tier)** — no downgrade, per [[13-model-router]] §3 (gate
exception). This is why the $20 sub exists: it buys judgment at the gates, not cheap volume.

---

## 8. Memory

| Read | Write |
|---|---|
| `brain/decisions/` — prior choices & rationale | `brain/decisions/` — new decision records after every gate |
| `brain/retros/` — what worked/failed | `brain/retros/` — after every `/retro` |
| `brain/playbooks/` — how we operate | `brain/playbooks/` — when a retro surfaces a better way |
| `brain/specs/` — current specs under review | (approvals noted in Decision Records) |

---

## 9. Escalation triggers

The Executive division never blocks on another agent — it *is* the escalation destination. However, it
escalates to **you (the founder)** when:

- A decision has legal or financial consequences (contracts, payments, personal liability).
- Two gates conflict (e.g., CPO says ship; CSO says block) and the stakes are high.
- A new strategy direction requires external research that isn't in the Brain yet.
- A budget anomaly could drain the $20 sub before the sprint ends.

---

## 10. Playbooks

### PLAY-E1: Kick off a new idea (`/office-hours`)

```
1. You: write a 1-paragraph idea brief (problem, user, revenue hypothesis).
2. Run: gstack /office-hours with the brief as input.
3. Claude interrogates: TAM, competition, build feasibility, distribution path, monetization, moat.
4. Output: a structured critique + either "pursue — here's the first Task Contract" or "kill — here's why."
5. If pursue: write a Decision Record (brain/decisions/) capturing the why, then issue a research Task Contract → [[02-research]].
```

### PLAY-E2: Gate a spec or architecture (`/plan-ceo-review` or `/plan-eng-review`)

```
1. [[03-product]] or [[04-engineering]] submits a draft spec/architecture to tasks/.
2. You run the appropriate plan-review skill with the doc.
3. Gate returns: accept (→ next stage in Product Factory), return (specific questions to answer), reject (kill it, write why).
4. Write a Decision Record regardless of outcome.
5. If accepted: move the spec to brain/specs/ (authoritative).
```

### PLAY-E3: Sprint retro (`/retro`)

```
1. At sprint/launch end, collect: what was built, metrics, agent failures, surprises.
2. Run: gstack /retro with that summary.
3. Output: what worked → propose a playbook update; what failed → a Decision Record.
4. Commit the retro to brain/retros/ and any promoted playbooks to brain/playbooks/.
5. Update NEXT_STEPS.md with action items.
```

---

## 11. KPIs / signals

| Signal | What it means | Bad state |
|---|---|---|
| Gate cycle time | Time from submission to accept/return | > 2 days = process is blocked on you |
| Return-to-accept ratio | How many gates return vs accept on first pass | > 50% returns = upstream quality is low |
| Decision record coverage | % of non-trivial decisions with a written record | < 80% = the Brain isn't growing |
| Retro cadence | Retros per sprint | 0 = no compounding; > 2 = process overhead |
| Sprint throughput | Task Contracts completed per sprint | Declining = a bottleneck to diagnose |
