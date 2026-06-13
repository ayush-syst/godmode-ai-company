# GST Bill Assistant — Launch Plan

> GOD's plan for its first product: take it from ~6/10 to a **paying CA firm**. Owner: founder
> (Layer-1 gate driver). All model calls route through the LiteLLM proxy; gates fire per
> [`CLAUDE.md`](CLAUDE.md). **Created:** 2026-06-13 · supersedes the BillKaro validation sprint
> (which was never started — see [the Decision Record](../../brain/decisions/2026-06-13-first-product-gst-bill-assistant.md)).

## Definition of "launched"

At least **one small CA firm using it on real client data and paying** (or in a committed paid
pilot). Not "feature-complete" — *revenue-validated*. This is the GOD Phase-0 goal: first users /
first dollar.

## Where it stands

From the product's handoff docs + the founder's own rating:

- ✅ ~40 features, 13+ waves, v3.7.0, 32 tests, browser-only / local-first, AGPL-3.0.
- ✅ Niche locked: best-in-class **GSTR-2B reconciliation** for small/mid CA firms (~20–300
  bills/month) who live in Excel + manual Tally today.
- ❌ Four launch-blockers (the founder's own list):
  1. localStorage-only → no team sharing / cloud backup
  2. browser AI key → can't meter or bill end users
  3. GSTR-2B matching accuracy must be **bulletproof** (make-or-break)
  4. DPDP-Act data-security posture before firms will trust it

## The plan (sequenced — GTM runs in parallel from Day 1)

### Phase A — Firsthand baseline + harden reconciliation  *(the make-or-break)*
- [ ] Read the actual repo (`core.mjs`, the 4-pass reconcile cascade, the 32 tests) and replace
      the secondhand gap assessment with a firsthand one.
- [ ] Build a real-world-messy fixture set: leading zeros, OCR-confusable chars, split lines,
      ₹1–2 paise rounding, GSTIN-level grouping, many-to-one. (Swarm drafts fixtures; the gate
      verifies.)
- [ ] Drive reconcile accuracy + match-confidence to "bulletproof"; every fallback flagged + a
      Verify action raised.
- **Gates:** `/review` (staff-eng bug hunt) · `/qa` (acceptance criteria) · `npm test` green.
- **Model:** Opus (`claude-gate`) for the matching logic; cheap tiers for fixture bulk.

### Phase B — Backend + metered AI  *(unblocks billing & teams)*
- [ ] Minimal AI backend: route Claude calls through a serverless proxy (the LiteLLM-proxy
      pattern) so end users don't need their own key → usage can be metered / billed.
- [ ] Opt-in cloud sync + team accounts (Supabase). **Keep local-only mode as the default.**
- **Gates:** `/plan-eng-review` (architecture) · `/cso` (security of the new surface).
- **Model:** Opus for architecture.

### Phase C — Security & trust posture  *(DPDP)*
- [ ] DPDP-Act data-security posture; privacy model for any cloud data; secrets handling.
- [ ] Security scan (Semgrep / Trivy / gitleaks) → **critical/high findings block launch.**
- **Gate:** `/cso` (blocking).

### Phase D — Deploy + first CA firms
- [ ] Deploy (flip the ready GitHub Pages workflow, or Vercel/Cloudflare — no build, trivial).
      `/ship` → `/canary`.
- [ ] Pricing for small CA firms; analytics + uptime (Uptime-Kuma) + error monitoring (Sentry).
- [ ] Convert design-partner CAs (see GTM) into a paid pilot → **first dollar.**

### GTM thread — starts Day 1, not after Phase D
- [ ] Recruit 3–5 small CA-firm **design partners** now. They shape what "10/10" actually means
      and de-risk willingness-to-pay (the office-hours lesson: don't polish in a vacuum).
- [ ] Focused niche: small/mid firms doing ~20–300 bills/month, in Excel + manual Tally.
- [ ] Win on **speed + price + AI-assist + WhatsApp-friendliness** — *not* head-on vs ClearTax.

## Risks carried forward

- **Reconciliation accuracy is existential** — a wrong CGST/IGST split breaks a client's ITC claim
  and torches trust. Phase A is non-negotiable and gated hard.
- **Crowded market** (ClearTax / GSTHero / IRIS / Cygnet) — win the niche; don't fight incumbents
  head-on.
- **Solo capacity** — sequence ruthlessly, one phase at a time; the swarm does volume, the gates
  protect quality.

## The two repos

GBA stays its own AGPL-3.0 repo (the source of truth). This GOD workspace holds operating docs
only. GBA *may* later be added as a git submodule under this folder — deferred, not required.
