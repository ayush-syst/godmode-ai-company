# CURRENT_TASK.md

> What is actively being worked on right now. Keep this short and live. Companion: `PROJECT_CONTEXT.md`
> (permanent knowledge), `NEXT_STEPS.md` (queue).
> **Last updated:** 2026-06-13

## Active phase
✅ **PHASE 0 WEEK 1 COMPLETE** — stack live on WSL2/Ubuntu.
✅ **WEEK 2 COMPLETE** — Replication Engine run live; **first product chosen.**

🏁 **DECISION (2026-06-13): GOD's first product = GST Bill Assistant** — not the engine's pick.
See the Decision Record: `brain/decisions/2026-06-13-first-product-gst-bill-assistant.md`.

⏭️ **NOW: Week 3 — drive GST Bill Assistant from ~6/10 to a paying CA firm.**
Plan: `products/gst-bill-assistant/LAUNCH-PLAN.md`. **Phase A underway:** firsthand reconciliation
assessment done (`products/gst-bill-assistant/PHASE-A-ASSESSMENT.md`); **P0-1 (line-aware tolerance)
shipped to GST App v3.7.1** (commit `54e1c1c`, 35 tests green).

---

## What happened in Week 2 (DONE ✅)
- Started LiteLLM proxy (`litellm-config-simple.yaml`) and ran the **Replication Engine live**
  (Gemini via the proxy) on "clone a US startup for India". Shortlist:
  Calendly 76 · Punchh 76 · **BillKaro (Invoice Simple) 75** · Thumbtack 68 · Skillshare 68 · Fat Llama 48.
  (Preserved in `brain/research/2026-06-13-replication-engine-shortlist.md`.)
- Fixed a brief-generator bug in `crew.py` (the `litellm.completion` model needed the `openai/`
  prefix to route via the proxy); regenerated the top-3 build briefs.
- Ran a CEO interrogation (office-hours equivalent) on the top pick, **BillKaro**. It flagged a
  competition graveyard (Vyapar/Khatabook/Zoho/Tally) and a weak "why you".
- **Founder surfaced an existing mature product — GST Bill Assistant** (GSTR-2B reconciliation for
  CA firms, ~v3.7.0, AGPL-3.0). Its launch-blockers map 1:1 onto the layers GOD provides, and it's
  the fastest path to revenue → **chosen as the first product.** BillKaro demoted to backlog/feeder.

## The first product (context for a fresh chat)
- **GST Bill Assistant** — browser-only, local-first GSTR-2B reconciliation + purchase-bill review
  desk for Indian CA firms. **Its own repo:** https://github.com/ayush-syst/gst-bill-assistant
  (AGPL-3.0, separate from GOD's MIT). Handoff docs live in that repo under `docs/`.
- GOD operates on it as the company OS. Operating workspace: `products/gst-bill-assistant/`
  (operating docs only — **never copy GBA's AGPL code into this MIT repo**).
- Founder's own rating: *8.5/10 MVP, ~6/10 launch-ready — gap is architectural.*
  Four blockers: (1) localStorage-only/no team, (2) browser AI key/can't bill, (3) 2B accuracy
  must be bulletproof, (4) DPDP security posture.

## The immediate next action (Week 3, Phase A — continued)
P0-1 (tolerance) is shipped (GST App v3.7.1). Next, per `products/gst-bill-assistant/PHASE-A-ASSESSMENT.md`:
1. **P0-2 — Wave 14 book-side split consolidation** (`groupBookSplits()` + a `reconcile()` pre-pass;
   reuse `effectiveTolerance` with the combined line count).
2. **Inspect the 2B import path** (`app.js` + how a real GST-portal export becomes `rows`) — the
   "known unknown" to close before calling reconciliation bulletproof.
3. Then the P1 items (deterministic tier-4 assignment, date disambiguation, ambiguous-fallback flagging).
4. **In parallel:** recruit 3–5 small CA-firm design partners (GTM thread).

> Code work lives in the GST App repo (`C:\Users\Ayush\OneDrive\Desktop\GST App`, AGPL-3.0). Commit +
> push from **Windows git** (WSL push hangs — see memory `god-git-push-from-windows-not-wsl`). Pushing
> to either repo's `main` needs explicit founder authorization each time (Auto Mode gate).

## Critical operational notes (carried from Week 1)
- **LiteLLM start:** `cd /mnt/c/Users/Ayush/OneDrive/Desktop/GOD && source .venv/bin/activate && unset DATABASE_URL && set -a && source .env && set +a && litellm --config bootstrap/litellm-config-simple.yaml`
  (the proxy must be running in another terminal before the engine / metered AI calls).
- **Why `-simple` config:** full config needs Redis + Langfuse (not set up yet); simple has no external deps.
- **Python venv:** `.venv` in project root (Python 3.11; system 3.14 is too new for litellm deps).
- **`crew.py` proxy calls** need the `openai/<alias>` model prefix (fixed this week).
- **Playwright/QA:** not yet working on Ubuntu 26.04 — may affect `/qa`. All other gstack skills work.

## Notes for whoever continues
- Weeks 1–2 are fully done — do not redo them.
- **Stay on Opus 4.8** for Week 3 (reconciliation logic, backend, security architecture are the
  hard/important work). Use cheap tiers only for bulk (fixtures, routine refactors).
- Never commit `.env` (real API keys; gitignored). GOD is public MIT; GBA is public AGPL-3.0 — keep them separate.
