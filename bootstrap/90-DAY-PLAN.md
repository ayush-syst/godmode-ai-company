# 🗓️ The 90-Day Plan — Phase 0: ship one real thing

> **The only goal of these 90 days:** stand up the system, pick one product, build it through the gates,
> launch it, and get your **first users / first dollar**. Not a portfolio. Not the full agent org. **One
> shipped, real product** that a stranger can use. Everything in `company-os/` exists to make this happen.
>
> **Honest framing (blueprint Part 13):** first paying users in 1–3 months is *high probability (60–75%)*
> **if you ship**. The failure mode is not the agents — it's building the system forever and never
> shipping a product. This plan is biased toward shipping.

---

## The shape of the 90 days

```
Week 1      FOUNDATION   stand up the stack, prove it runs
Week 2      CHOOSE       run the Replication Engine → pick ONE product
Weeks 3–8   BUILD        Product Factory loop: spec → design → build → review → QA
Weeks 9–11  HARDEN+SHIP  security gate → deploy → launch
Weeks 12–13 DISTRIBUTE   marketing + first users + first dollar + first retro
```

> The biggest risk is slipping Build into Week 12. **Protect the ship date.** Cut scope, not the launch.

---

## Week 1 — Foundation (stand up the system)

**Outcome:** the stack runs; a free-model swarm task and a Claude gate both work end-to-end.

- [ ] **Enable WSL2 + Docker** — run `bootstrap/0-enable-wsl.ps1` in an elevated PowerShell; reboot; finish Ubuntu user setup.
- [ ] **Install the stack** — in Ubuntu: `bash bootstrap/install.sh` (use `--minimal` first if you want to start with just Claude Code + gstack).
- [ ] **Authenticate Claude Code** — run `claude`, sign in with your $20 sub.
- [ ] **Add keys** — `cp bootstrap/.env.example .env`; fill in `ANTHROPIC_API_KEY` + at least one free key (`GEMINI_API_KEY` or `GROQ_API_KEY`). **Never commit `.env`.**
- [ ] **Start the Token Optimizer** — `litellm --config bootstrap/litellm-config.yaml`; confirm it serves on `:4000` and logs to Langfuse.
- [ ] **Seed the Company Brain** — create `brain/` (Obsidian vault) and drop in the blueprint + `company-os/` + the first Decision Records for the locked choices (see `company-os/12-company-brain.md` §12).
- [ ] **Smoke test — swarm:** run the Replication Engine offline: `python bootstrap/replication-engine/run.py --demo` (proves Python + rubric path).
- [ ] **Smoke test — gate:** run gstack `/office-hours` on any throwaway idea (proves Claude Code + gstack + the gate workflow).
- [ ] **Milestone:** commit + push. Refresh the handoff files.

> ⚠️ If something here takes more than a few days, **drop to `--minimal`** and proceed with just gstack +
> one free model. You do not need the full swarm to ship your first MVP.

---

## Week 2 — Choose (pick ONE product)

**Outcome:** one product chosen, with a build brief, via a human decision.

- [ ] **Run the Replication Engine live** — `python bootstrap/replication-engine/run.py "clone a US startup for India"` (or a category you have a thesis about). Requires the LiteLLM proxy + a free key.
- [ ] **Review the shortlist critically** — open `out/<ts>/shortlist.md`. The engine narrows; it does not decide. Sanity-check the top 3 against your own knowledge (`company-os/02-research.md` provenance rule).
- [ ] **`/office-hours` on the winner** — take `build-brief-<winner>.md` into gstack `/office-hours`. Let Claude interrogate TAM, competition, feasibility, distribution, monetization.
- [ ] **DECIDE** — pick the product. Write a Decision Record to `brain/decisions/` (this is the most important decision of the 90 days).
- [ ] **Create the product repo** — `products/<name>/`, copy `bootstrap/CLAUDE.md` into it.
- [ ] **Milestone:** commit + push. Refresh handoff files.

> **Pick for distribution, not just for TAM.** The rubric weights distribution ×3 for a reason — a product
> you can't cheaply get in front of users will starve no matter how big the market.

---

## Weeks 3–8 — Build (the Product Factory loop)

**Outcome:** a working, reviewed, QA'd MVP — feature-complete for launch, nothing more.

Run the loop from `company-os/00-architecture.md` §8 and the Product Factory (blueprint Part 7):

- [ ] **Spec** (`company-os/03-product.md`) — write the PRD with **objective acceptance criteria**. Gate: `/plan-ceo-review` → `/plan-eng-review`. Scope ruthlessly: what is explicitly **OUT** for v1?
- [ ] **Design** (`company-os/05-design.md`) — `/design-shotgun` → pick a direction → `/design-html` → **`/design-review`** gate. Clear the taste bar; don't ship a default template.
- [ ] **Architecture** (`company-os/04-engineering.md`) — `/plan-eng-review`; write ADRs for non-obvious choices.
- [ ] **Build** — dispatch Task Contracts to the swarm (OpenHands / ruflo on `bulk-code`). Keep PRs small.
- [ ] **Review gate** — **`/review`** on every PR. No staff-eng-level bugs merge.
- [ ] **QA gate** — **`/qa`** (live Chromium) against the spec's acceptance criteria.
- [ ] **Weekly:** a `/retro` (`company-os/01-executive.md`) → update a playbook → refresh handoff files + commit.

**Scope discipline (the make-or-break of this phase):**
- One core job-to-be-done, done well. No settings sprawl, no "while we're here."
- If a feature isn't needed for a stranger to get value on day one, it's **v1.1**, not v1.
- Build on free/cheap models; spend Claude budget on the **gates and the hard bugs only** (`company-os/13-model-router.md`).

---

## Weeks 9–11 — Harden + Ship

**Outcome:** the MVP is live on the internet, secured, and monitored.

- [ ] **Security gate** (`company-os/09-security.md`) — CI runs Semgrep + Trivy + gitleaks + Syft; then **`/cso`** (OWASP/STRIDE). **Critical/high findings block the ship — no exceptions.**
- [ ] **Payments** — wire Razorpay (UPI/cards for India) if the product charges money. Test the full flow.
- [ ] **Deploy** (`company-os/10-infrastructure.md`) — `/ship` → Coolify on one cheap VPS (or Vercel for a static frontend) → **`/canary`** health check. Cloudflare in front from day one.
- [ ] **Observability** — Sentry (errors), Uptime-Kuma (uptime), Plausible/Umami (analytics). You should *know* when something breaks before a user tells you.
- [ ] **Backups** — confirm Supabase PITR / a `pg_dump` cron actually restores. An untested backup is not a backup.
- [ ] **Milestone:** the product is live. Commit + push. Refresh handoff files. Write a launch Decision Record.

---

## Weeks 12–13 — Distribute (first users, first dollar)

**Outcome:** real humans use it; at least one pays (or a strong signal that they will).

- [ ] **Landing page** (`company-os/06-marketing.md`) — copy that passes the brand-voice + honesty gate (you approve). Clear value prop, one CTA.
- [ ] **Launch posts** — ProductHunt, IndieHackers, relevant subreddits/communities, Twitter/X, LinkedIn. Drafted by the swarm, **approved by you**.
- [ ] **SEO seed** — 2–3 founding blog posts targeting high-intent, low-competition India keywords.
- [ ] **Outreach** (`company-os/07-sales.md`) — a small, qualified lead list; a 3-touch sequence **you approve**; reply to every human personally.
- [ ] **Support** (`company-os/08-customer-success.md`) — n8n triage live; you handle every escalation. Turn user words into the next backlog.
- [ ] **Final retro** — `/retro` on the whole 90 days. What worked → playbooks. What failed → decisions. Promote learnings to the Brain.
- [ ] **Milestone:** commit + push. **Refresh `PROJECT_CONTEXT.md` for the post-Phase-0 chapter.**

---

## The weekly rhythm (every week, all 90 days)

| Cadence | Do | Why |
|---|---|---|
| **Daily** | Clear the "gates awaiting you" queue first | You're the only human gate — unblock the org |
| **Daily** | Glance at the Founder Dashboard (errors, cost, signups) | Catch problems early |
| **Weekly** | One `/retro` → update one playbook | Compounding > heroics |
| **Weekly** | Refresh the 3 handoff files + commit/push | Fresh-chat resumability; milestone discipline |
| **Weekly** | Check token spend in Langfuse vs. the $15 fence | Don't drain the sub (`company-os/11-finance-token-optimizer.md`) |

---

## Success criteria (honest)

| By day | Target | Honest probability (blueprint Part 13) |
|---|---|---|
| 7 | Stack runs; a gate + a swarm task both work | very high if you follow Week 1 |
| 14 | One product chosen with a build brief | high |
| 60 | MVP feature-complete, reviewed, QA-passed | moderate — scope discipline decides this |
| 80 | Live, secured, monitored, payments working | moderate |
| 90 | First real users; first dollar or a strong buy signal | **60–75% if you actually ship** |

> $1k–$10k MRR is a **6–12 month** target (40–60%), **not** a 90-day one. These 90 days buy you the thing
> that makes that possible: **a shipped product and a working factory.**

---

## The traps to avoid (from the Reality Check)

1. **Building the system instead of a product.** The system is *done enough* — this repo is the system. Go build the product.
2. **Shipping AI slop.** The gates exist to stop this. Don't skip `/review`, `/design-review`, `/cso`.
3. **Over-trusting an autonomous agent.** Sandbox the swarm; never give it secrets; gate its output.
4. **Scope creep.** Every "wouldn't it be cool if" past Week 8 is a threat to the launch. Write it down for v1.1.
5. **Founder burnout.** You are the only gate. Use the retros and playbooks to make the *next* product cheaper. Protect your attention; automate the rest.

---

*When Phase 0 is done, return to `NEXT_STEPS.md` §C–D and the 5-year roadmap (blueprint Part 12). But not
before something real is live. Build for the realistic win.*
