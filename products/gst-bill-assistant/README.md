# Product: GST Bill Assistant — GOD's first product

This folder is GOD's **operating workspace** for its first product. It holds GOD's own process
artifacts (operating manual, launch plan) — **not** the product's source code.

## The product

**GST Bill Assistant** — a browser-only, local-first **GSTR-2B reconciliation** + purchase-bill
review desk for Indian CA firms. Turns messy purchase invoices (PDF / image / Excel / WhatsApp)
into voucher-ready accounting entries and reconciles them against GSTR-2B before claiming Input
Tax Credit.

- **Repo (source of truth):** https://github.com/ayush-syst/gst-bill-assistant
- **License:** AGPL-3.0 — **kept separate from GOD's MIT.** The two repos stay independent on
  purpose; GBA's AGPL code is never copied into this MIT repo.
- **State** (per the product's own handoff docs): ~v3.7.0, 13+ build waves, 32 tests, ~40
  features, browser-only/local-first, **undeployed**. Founder's rating: *8.5/10 MVP, ~6/10
  launch-ready — the gap is architectural, not features.*
- **Stack:** plain HTML + CSS + vanilla JS, no build step; `assets/js/core.mjs` = pure domain
  logic; PDF.js + Tesseract.js via CDN; Anthropic API called direct from the browser (user's own
  key in localStorage).

## Why it's the first product

See the Decision Record:
[`brain/decisions/2026-06-13-first-product-gst-bill-assistant.md`](../../brain/decisions/2026-06-13-first-product-gst-bill-assistant.md).
Short version: GBA's launch-blockers (backend + team accounts, metered AI, bulletproof
reconciliation, DPDP security, CA-firm GTM) map almost exactly onto the layers GOD provides — so
it's the ideal product for this system to operate on, and the fastest path to GOD's Phase-0 goal
(first users / first dollar).

## How we drive it

- **Operating manual:** [`CLAUDE.md`](CLAUDE.md) (copied from `bootstrap/CLAUDE.md`).
- **Plan:** [`LAUNCH-PLAN.md`](LAUNCH-PLAN.md) — the path from ~6/10 to first paying CA firm.
- All model calls route through the **LiteLLM proxy**; gates (`/review`, `/cso`, `/qa`, `/ship`)
  fire per the operating manual. Decisions are recorded in `brain/decisions/`.
