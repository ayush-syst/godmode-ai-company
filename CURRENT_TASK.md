# CURRENT_TASK.md

> What is actively being worked on right now. Keep this short and live. Companion: `PROJECT_CONTEXT.md`
> (permanent knowledge), `NEXT_STEPS.md` (queue).
> **Last updated:** 2026-06-13

## Active phase
✅ **PHASE 0 WEEK 1 COMPLETE.** Stack is live on WSL2/Ubuntu. All smoke tests passed.

⏭️ **NOW: Week 2 — run the Replication Engine live → pick ONE product.**

---

## Week 1 — DONE ✅ (2026-06-13)
- ✅ WSL2 + Ubuntu 26.04 installed and running
- ✅ Claude Code 2.1.172 installed + authenticated (2389ayush@gmail.com, Claude Pro)
- ✅ gstack v1.57.10 installed at `~/.claude/skills/gstack/`; `/office-hours` verified working
- ✅ LiteLLM proxy running on `:4000` — use `bootstrap/litellm-config-simple.yaml`
- ✅ Replication Engine demo smoke test passed (CreatorKit 81/95 wins)
- ✅ Gemini API key added to `.env` (GEMINI_API_KEY)
- ✅ Milestone committed + pushed to GitHub

## Critical operational notes (for fresh chat)
- **LiteLLM start command:** `cd /mnt/c/Users/Ayush/OneDrive/Desktop/GOD && source .venv/bin/activate && unset DATABASE_URL && litellm --config bootstrap/litellm-config-simple.yaml`
- **Why `litellm-config-simple.yaml`:** The full config requires Redis + Langfuse (not set up yet). Simple config has no external deps.
- **Why `unset DATABASE_URL`:** `.env` had DATABASE_URL set which triggered Prisma (not needed). It's now commented out in `.env`.
- **Python venv:** `.venv` in project root, built with Python 3.11 (system Python 3.14 is too new for litellm deps).
- **gstack skills location:** `~/.claude/skills/gstack/` (symlinked from `~/.gstack`)
- **Playwright/QA:** Not working (Ubuntu 26.04 not yet supported). All other gstack skills work fine.

## The immediate next action (Week 2)

Run the Replication Engine **live** (LiteLLM must be running in another terminal first):

```bash
cd /mnt/c/Users/Ayush/OneDrive/Desktop/GOD
source .venv/bin/activate
pip install -r bootstrap/replication-engine/requirements.txt -q
python bootstrap/replication-engine/run.py "clone a US startup for India"
```

Then:
1. Review `bootstrap/replication-engine/out/<timestamp>/shortlist.md`
2. Open Claude Code → run `/office-hours` on the top candidate
3. **DECIDE** — pick the product. Write Decision Record to `brain/decisions/`.
4. Create `products/<name>/` repo, copy `bootstrap/CLAUDE.md` into it.
5. Commit + push. Refresh handoff files.

## Notes for whoever continues
- Week 1 is fully done — do not redo anything from it.
- Sonnet 4.6 is fine for Week 2 (running engine + decision). Switch to Opus for Week 3+ (architecture/security).
- Never commit `.env` — it has real API keys. It is gitignored.
- Public MIT repo — keep it clean.
