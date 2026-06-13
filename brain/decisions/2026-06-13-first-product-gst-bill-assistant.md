---
type: decision
id: DEC-2026-0001
title: First product = GST Bill Assistant (override the replication engine's greenfield pick)
date: 2026-06-13
status: accepted
decided_by: 01-executive (/office-hours, founder-gated)
supersedes: null
tags: [product, strategy, phase-0, gst]
---

## Context

Phase-0 Week 2's task was: run the Startup Replication Engine live → pick GOD's first product
(PROJECT_CONTEXT §2, locked decision #3). The engine ran **live** on 2026-06-13 (Gemini 2.5 Flash
via the LiteLLM proxy) on the brief *"clone a US startup for India"* and produced a ranked
shortlist — see [[2026-06-13-replication-engine-shortlist]]. Top *greenfield* pick: **BillKaro**, a
GST-invoicing + UPI app for MSMEs (75/95).

A CEO interrogation (office-hours equivalent) of BillKaro surfaced two serious problems:

1. **Competition graveyard.** MSME invoicing is crowded with funded incumbents (Vyapar, Khatabook,
   Zoho, Tally) — a category where well-capitalised players have struggled to monetise.
2. **"Why you."** A solo founder had no obvious edge entering GST cold.

During the decision the founder surfaced an existing, mature product they had already built:
**GST Bill Assistant** (`github.com/ayush-syst/gst-bill-assistant`) — a browser-only, local-first
**GSTR-2B reconciliation** + purchase-bill review desk for Indian CA firms. AGPL-3.0, ~v3.7.0,
13+ build waves, 32 tests. Founder's own honest rating (in its docs): **"8.5/10 as an MVP;
~6/10 launch-ready — the gap is architectural, not features."**

## Options considered

1. **BillKaro greenfield** (the engine's pick) — a 90-day build from a blank repo into the MSME
   invoicing graveyard. Slowest to revenue; weakest "why you".
2. **GST Bill Assistant as the first product** — take an existing ~6/10-launch product the rest of
   the way. Better wedge (CA firms have tool budgets; GSTR-2B reconciliation is the niche
   competitors charge for), a real domain edge, and the fastest path to revenue.
3. **GST ecosystem** — GBA first, BillKaro later as the MSME feeder (MSME invoices → CA reconciles
   them in GBA).

## Decision

**GST Bill Assistant is GOD's first product.** BillKaro is demoted to a recorded backlog /
potential-feeder idea (preserved in [[2026-06-13-replication-engine-shortlist]]), not built now.
GBA keeps its own AGPL-3.0 repo as the source of truth; GOD operates on it as the company OS
(gates + infra + swarm) and drives it to launch. The product workspace lives at
`products/gst-bill-assistant/` and holds **GOD's operating docs only — not a copy of GBA's AGPL
code** (the two repos and licenses stay separate on purpose).

## Rationale

- **GOD's founding philosophy is "ship something real fast; assemble what exists; don't build from
  scratch"** (PROJECT_CONTEXT §0). Building BillKaro greenfield while a near-launch product sits
  undeployed would contradict the project's own thesis.
- **GBA's four launch-blockers map 1:1 onto the exact layers GOD provides:** backend + team
  accounts → infra layer; browser AI key / metering → the LiteLLM proxy as a metered AI backend;
  bulletproof 2B accuracy → the quality spine (`/review`, `/qa`, tests); DPDP posture → the
  security gate (`/cso`). GBA is the *ideal* product for this system to operate on.
- It closes the **"why you"** gap the engine's pick could not: 13 waves of GST domain depth is the
  edge.
- **Better wedge:** CA firms pay for tools; price-sensitive MSMEs resist. GSTR-2B reconciliation is
  exactly the niche incumbents charge for.

## Consequences

- Week 3+ becomes *"drive GBA from ~6/10 to launch + first paying CA firm,"* not a greenfield
  build. See [[../products/gst-bill-assistant/LAUNCH-PLAN]].
- The replication engine is reframed as a **portfolio-discovery** tool for *future* products, not
  the sole source of the first one. Its output is preserved, not wasted.
- Two repos, two licenses (GOD = MIT, GBA = AGPL-3.0) — kept independent deliberately.
- **Revisit trigger:** if a firsthand code review shows the gap to launch is materially larger than
  "architectural," re-sequence (and reconsider option 1/3).

Links: [[../company-os/01-executive]] · [[../products/gst-bill-assistant/LAUNCH-PLAN]] · [[2026-06-13-replication-engine-shortlist]] · [[../company-os/13-model-router]]
