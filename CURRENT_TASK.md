# CURRENT_TASK.md

> What is actively being worked on right now. Keep this short and live. Companion: `PROJECT_CONTEXT.md`
> (permanent knowledge), `NEXT_STEPS.md` (queue).
> **Last updated:** 2026-06-04

## Active phase
✅ **PHASE 0 WEEK 1 COMPLETE** (2026-06-13). Stack is live on WSL2/Ubuntu.

⏭️ **Next = Week 2: Run Replication Engine live → pick ONE product.**

## What's done (all pushed)
- ✅ `00-MASTER-BLUEPRINT.md` — 13 parts + reality check
- ✅ `README.md` + `LICENSE` (MIT) + `.gitignore` + 3 handoff files
- ✅ `company-os/` — `_INDEX`, `00-architecture`, `12-company-brain`, `13-model-router` + 11 division files
- ✅ `bootstrap/` — `0-enable-wsl.ps1`, `install.sh`, `CLAUDE.md`, `litellm-config.yaml`, `.env.example`
- ✅ `bootstrap/replication-engine/` — `run.py`, `crew.py`, `rubric.py`, `sample_candidates.json`,
  `requirements.txt`, `README.md` — **`python run.py --demo` verified working** (ranks the sample set;
  CreatorKit 81/95 → HealthLog 49/95)
- ✅ `bootstrap/90-DAY-PLAN.md` — the Phase-0 execution checklist

## Week 1 — DONE ✅
- ✅ WSL2 + Ubuntu 26.04
- ✅ Claude Code 2.1.172 authenticated
- ✅ gstack installed + `/office-hours` works
- ✅ LiteLLM proxy running on :4000 (use `bootstrap/litellm-config-simple.yaml` + comment out DATABASE_URL in .env)
- ✅ Replication Engine demo: CreatorKit 81/95 wins

## The immediate next action (Phase 0, Week 2)
Get a free Gemini or Groq API key, add it to `.env`, then run the engine live:
1. Get `GEMINI_API_KEY` free at https://aistudio.google.com or `GROQ_API_KEY` at https://console.groq.com
2. Add key to `.env`
3. Start LiteLLM: `unset DATABASE_URL && litellm --config bootstrap/litellm-config-simple.yaml`
4. Run live: `python bootstrap/replication-engine/run.py "clone a US startup for India"`
5. Review `out/<ts>/shortlist.md` → run `/office-hours` on the winner → DECIDE

See `bootstrap/90-DAY-PLAN.md` for the full week-by-week plan.

## ⚠️ Decision point for the user (before execution)
The execution phase is **interactive and machine-specific** (installs software, reboots, needs your API
keys, runs in your Ubuntu). A few things to know:
- It may be better done **hands-on by you** following `90-DAY-PLAN.md`, with Claude assisting per-step,
  rather than fully agent-driven.
- It needs **real keys** (never committed) and a **WSL2 reboot**.
- Consider whether to **start a fresh chat** here (authoring context is large; execution is a clean phase
  that resumes cleanly from `PROJECT_CONTEXT.md`).

## Notes for whoever continues
- Authoring is done — do not re-author. If extending, keep `company-os/` files on the `00-architecture.md`
  §3 schema and keep everything consistent with the blueprint.
- Keep maintaining the 3 handoff files at every milestone; never commit secrets (public MIT repo).
- Model-escalation: Opus for architecture/security/hard code; Sonnet/Haiku for routine/bulk.
