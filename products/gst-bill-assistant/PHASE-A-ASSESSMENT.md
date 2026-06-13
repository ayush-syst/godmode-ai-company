# Phase A — Reconciliation Gap Assessment (firsthand)

> Firsthand read of the GST App repo's reconciliation core (`assets/js/core.mjs` + `tests/core.test.mjs`)
> on 2026-06-13. GST App HEAD now `7b9cc99` (v3.8.0); both P0 fixes shipped. 39/39 tests green (Node v24).
> This is the make-or-break layer (founder's own note + NEXT_STEPS). Drives the Phase-A work in
> [LAUNCH-PLAN.md](LAUNCH-PLAN.md).

## Verdict
The reconciliation **core is strong** — pure/DOM-free, documented, well-tested; the claimed-once
cascade is the right design for ITC safety. The "~6/10 launch-ready" gap is the **product shell**
(multi-user, billing, hosting), not the matching logic. The logic's gap to "bulletproof" is a
focused list below.

## What's solid (don't churn)
- Claimed-once tiered cascade (exact → leading-zero → OCR → GSTIN+amount); looser tiers can't steal
  an exact match; risky tiers flagged "Probable — verify".
- GSTIN mod-36 checksum (correct vs official vector). CSV parser handles quotes/CRLF/doubled-quotes.
- Wave 13 split-2B consolidation with clear notes.

## Prioritized gaps

### P0 — can produce wrong results on real data
- [x] **P0-1 — flat ₹2 tolerance too rigid.** ✅ DONE (v3.7.1, GST App `54e1c1c`). Replaced with
      `effectiveTolerance(lines) = ₹2 + ₹1·(lines−1)` so consolidated-line rounding no longer causes
      false Mismatches; single-line behavior unchanged. 3 tests added.
- [x] **P0-2 — book-side split consolidation (Wave 14).** ✅ DONE (v3.8.0, GST App `7b9cc99`). New pure
      `groupBookSplits()`; `reconcile()` now matches book groups vs consolidated 2B rows and writes the
      result back to each member row; tolerance widens with lines summed on both sides. 4 tests (39 total).

### P1 — robustness
- [ ] **Tier-4 (GSTIN+amount) is order-dependent greedy** (`core.mjs` tier-4 loop). An early bill can
      grab a row better suited to a later bill → false "Missing in 2B". Make it deterministic
      global-best; add a two-bill/two-row test.
- [ ] **Date unused in matching.** `parseInvoiceMonth` exists but `reconcile` ignores it. Same vendor
      + same invoice no across periods can mis-match. Use month as a tie-breaker / cross-period warning.
- [ ] **Silent fallback-key collisions.** Loose/OCR index is "first row wins"; if a fuzzy key maps to
      2+ distinct invoices, downgrade to "ambiguous — verify" instead of taking the first.

### P2 — trust polish
- [ ] **No GSTIN-level fuzziness** — one OCR error in the book GSTIN drops the bill to "Missing in 2B".
      Consider a PAN-level (chars 3–12) fallback, flagged.
- [ ] **OCR folding applied to both sides** — but 2B is portal-clean (not OCR'd). Scope folding to the
      book side; document the asymmetry.
- [ ] **Numeric match-confidence score** (exact=100 → amount=60, minus drift/cross-period penalties) so
      the UI can triage "verify" items.

## Known unknown (inspect before calling reconciliation "bulletproof")
Not yet read: the **2B import path** (how a real GST-portal export — Excel/JSON, its actual column
names — becomes `rows`) and `app.js` integration. The nastiest real-world bugs in these tools hide
there (column-alias drift, GSTIN/invoice extraction). Inspect next.

## Recommended sequence
P0-1 ✅ → P0-2 ✅ → **inspect the 2B import path (next)** → expand fixtures (large-value, multi-line both
sides, cross-period) → P1 items.

## Gate note
P0-1 shipped with unit/integration tests (the right gate for pure DOM-free logic) + a self-review.
The gstack `/review` + browser `/qa` gates live in the WSL/GST-App environment and have not fired.
