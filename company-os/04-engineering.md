# 04 — Engineering Division

> **Mission.** Turn approved specs into production-quality, tested, secure code — as fast as possible
> without compounding technical debt. Blueprint source: Parts 3, 7 (stages 6–8). **Layer: 1 (gates) +
> 2 (workers).** Powered by: **gstack skills for all gates; OpenHands + Claude Code for coding;
> ruflo workers for parallel/bulk tasks.**

---

## 1. Roles

| Role | One-line job |
|---|---|
| **Architect** | Own the system design, data model, stack choices, and API contracts |
| **Backend Engineer** | Implement server-side logic, APIs, DB queries, background jobs |
| **Frontend Engineer** | Implement UI (following [[05-design]] output), client-side logic, performance |
| **DevOps / Platform** | Own CI/CD, Docker, deploy, infra-as-code, and the [[10-infrastructure]] setup |
| **DB Engineer** | Design schemas, migrations, query optimization, data integrity |
| **Test Engineer** | Write and maintain unit/integration/e2e test suites; own coverage gate |
| **Technical Writer** | Produce inline docs, API docs, and README-level documentation |

---

## 2. Layer mapping

| Role / action | Layer | Implementation |
|---|---|---|
| **Architecture review** | **1 (gate)** | gstack `/plan-eng-review` — you trigger |
| **Code review** | **1 (gate)** | gstack `/review` — you trigger on every PR |
| **QA (live browser)** | **1 (gate)** | gstack `/qa` — Playwright / Chromium; you trigger |
| **Ship / deploy** | **1 (gate)** | gstack `/ship`, `/land-and-deploy`, `/canary` |
| Bulk code generation | **2 (worker)** | OpenHands (sandboxed Docker) or Claude Code |
| Test writing | **2 (worker)** | OpenHands or ruflo workers (cheap model) |
| DB migrations | **2 (worker)** | OpenHands; migration plan reviewed in Layer 1 first |
| Documentation | **2 (worker)** | ruflo worker on cheap model |
| Parallel refactors | **2 (worker)** | ruflo workers (cheap model, coordinated by queen) |

---

## 3. Inputs

| From | What |
|---|---|
| [[03-product]] | Approved PRD with objective acceptance criteria |
| [[05-design]] | Design system, hi-fi screens, component specs, animation brief |
| [[09-security]] | Security requirements, threat model, pre-build constraints |
| [[10-infrastructure]] | Target environment, Docker base images, env var schema |
| [[12-company-brain]] | Architecture decisions, API contracts, prior tech decisions |

---

## 4. Outputs

| To | What | Written where |
|---|---|---|
| [[01-executive]] | PR ready for `/review` gate + code diff | git PR |
| [[09-security]] | Code and infra submitted for `/cso` scan | git PR + scan task |
| [[10-infrastructure]] | Passing build for deploy | CI artifacts / Docker image |
| [[12-company-brain]] | Architecture Decision Records (ADRs) | `brain/decisions/` |
| [[03-product]] | If acceptance criteria can't be met → escalation | `tasks/<id>/` with blocker noted |

---

## 5. Tools

| Tool | Purpose |
|---|---|
| **Claude Code** | The primary coding harness (you drive, or agents drive via Claude Code SDK) |
| **gstack `/review`** | Staff-engineer-level code review gate (bug hunt + reuse + simplification) |
| **gstack `/qa`** | Live browser QA with Playwright / Chromium |
| **gstack `/plan-eng-review`** | Architecture / plan soundness gate |
| **gstack `/ship`**, `/land-and-deploy`** | Deployment gate + Coolify/Vercel push |
| **gstack `/canary`** | Canary deploy health check |
| **gstack `/benchmark`** | Performance benchmarking |
| **gstack `/document-*`** | Auto-docs generation |
| **OpenHands** (`OpenHands/OpenHands`) | Autonomous SWE agent in sandboxed Docker; write code, run tests, open PRs |
| **ruflo** | Parallel workers for bulk test-writing, refactors, scaffolding |
| **Semgrep** | SAST in CI (also owned by [[09-security]]) |
| **Playwright** | Browser automation for QA (`/qa` wraps it) |

---

## 6. Quality gates

| Gate | Trigger | Pass criteria | Fail action |
|---|---|---|---|
| **Architecture (`/plan-eng-review`)** | Before any significant build starts | No fundamental design flaws; stack matches constraints; data model handles edge cases; performance path clear | Return to Architect; rework |
| **Code review (`/review`)** | Every PR before merge | No correctness bugs; no obvious security issues; idiomatic; no dead code | Return PR with specific comments |
| **QA (`/qa`)** | After code review passes | All acceptance criteria pass in live browser; no visual regressions; mobile-responsive (if applicable) | Return to Engineering; fix list |
| **Security (`/cso`)** | Before every deploy (see [[09-security]]) | Zero critical/high SAST/DAST findings; no leaked secrets; STRIDE threats addressed | Block deploy; file security Task Contracts |
| **Canary (`/canary`)** | Immediately after deploy | Error rate normal; latency normal; key user path works | Roll back; investigate |

---

## 7. Model routing

| Task | Default tier | Notes |
|---|---|---|
| Bulk codegen (tests, CRUD, boilerplate) | Cheap (DeepSeek / Qwen Coder) | Best coding models per dollar |
| Hard bugs, architecture reasoning | **Premium (Claude)** | Reserve for things that really need judgment |
| Documentation | Cheap or free | Volume; quality checked at gate |
| `/review` gate | **Premium (Claude)** | Gate exception — no downgrade |
| `/qa` gate | **Premium (Claude)** | Gate exception |
| Parallel refactors | Cheap (DeepSeek → Groq fallback) | Volume; reviewed in `/review` |

See [[13-model-router]] for the full routing algorithm and fallback chains.

---

## 8. Memory

| Read | Write |
|---|---|
| `brain/decisions/` — prior tech choices, ADRs | `brain/decisions/` — new ADRs after architecture choices |
| `brain/specs/` — the approved PRD to build to | (code lives in git, not brain/) |
| `brain/playbooks/` — how we deploy, how we write migrations | `brain/playbooks/` — improvements from `/retro` |
| ruflo AgentDB — SONA patterns from prior coding runs | ruflo AgentDB — update what worked/failed per sprint |

---

## 9. Escalation triggers

Engineering escalates to [[01-executive]] (you) when:

- A core requirement is technically infeasible in the current stack without a large rewrite.
- A security finding from `/cso` is critical and blocks the ship gate — needs your go/no-go.
- A dependency has a known vulnerability with no patch yet (supply chain risk).
- An irreversible action is required: prod DB migration with no rollback, breaking API change with live users.
- Test coverage is below threshold and increasing it would delay the sprint significantly.

---

## 10. Playbooks

### PLAY-ENG1: Feature build (the standard loop)

```
1. Receive approved PRD from [[03-product]] (in brain/specs/).
2. Run /plan-eng-review on the spec — get the architecture blessing or fix issues first.
3. Write an ADR for any non-obvious stack/design choices (brain/decisions/).
4. Dispatch OpenHands Task Contract: "Implement <spec> to these acceptance criteria. Use existing stack (see brain/decisions/). Write tests. Do not touch unrelated files."
5. OpenHands returns: code diff + test results + confidence.
6. Run gstack /review on the PR. Return if needed; accept when clean.
7. Run gstack /qa — live browser check against all acceptance criteria.
8. Submit to [[09-security]] for /cso scan.
9. On security pass: gstack /ship → Coolify deploy → /canary health check.
10. Merge to main. Write a short retro note for the next /retro.
```

### PLAY-ENG2: DB schema migration

```
1. Write migration in a branch. Include: up, down (rollback), test for data integrity.
2. /plan-eng-review gate with focus on: "is the down migration safe? does this break any queries?"
3. Test in a local replica (Docker Compose with Supabase image).
4. Run Semgrep over the migration SQL (check for injection, privilege escalation).
5. Gate: you approve the migration plan before it touches any prod-adjacent environment.
6. Deploy with a maintenance window or zero-downtime pattern (additive migrations only; no destructive without a phased plan).
7. Write an ADR capturing: schema change, why, rollback tested.
```

### PLAY-ENG3: Hotfix (production incident)

```
1. Triage: severity? (data loss / security breach → PLAY-S3 in [[09-security]] takes over).
2. Reproduce in a local Docker environment first — never debug in prod.
3. Write the minimal fix (one change → one PR). No refactoring alongside a hotfix.
4. Fast-track /review (flag as hotfix; still runs the gate).
5. /qa on the specific broken path only.
6. /cso: does the fix introduce any new surface?
7. /ship → /canary.
8. Post-mortem → retro note → update the relevant playbook.
```

---

## 11. KPIs / signals

| Signal | What it means | Bad state |
|---|---|---|
| Gate pass rate (first attempt) | % of PRs passing `/review` without returns | < 60% = agents or you are shipping low-quality code |
| `/qa` pass rate (first attempt) | % of builds passing QA without fixes | < 70% = spec-to-code translation is lossy |
| Test coverage | % lines/branches covered | < 70% = confidence in the canary is low |
| Deploy frequency | Deploys per week | < 1/week = flow is blocked somewhere |
| Mean time to recovery (MTTR) | Time from incident detection to resolution | > 4h = incident response is not practiced |
| Security findings per sprint | New critical/high findings from `/cso` | > 0 critical/sprint = security hygiene is slipping |
