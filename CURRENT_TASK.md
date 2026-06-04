# CURRENT_TASK.md

> What is actively being worked on right now. Keep this short and live. Companion: `PROJECT_CONTEXT.md`
> (permanent knowledge), `NEXT_STEPS.md` (queue).
> **Last updated:** 2026-06-04

## Active phase
**Authoring the deliverables** (the blueprint document + the runnable bootstrap kit) into
`C:\Users\Ayush\OneDrive\Desktop\GOD\`.

## Right now
**BUILD phase — Task #2 (company-os/ core) COMPLETE & pushed.** Authored the four core specs:
`company-os/_INDEX.md`, `00-architecture.md` (3-layer model + Task Contract + the role-spec schema every
division file must follow + conflict-resolution ladder + gate definitions), `12-company-brain.md` (4-store
memory, write/read policy, doc schemas), `13-model-router.md` (difficulty→model routing, fallback chains,
quota rotation, caching, budget guards).

## Right now
**BUILD phase — Tasks #2 & #3 (full company-os/) COMPLETE & pushed.**

`company-os/` is fully authored (15 files total):
- Core: `_INDEX`, `00-architecture`, `12-company-brain`, `13-model-router`
- Divisions: `01-executive` through `11-finance-token-optimizer` (all 11, all following the §3 schema)

⏭️ **NEXT: Task #4 — the `bootstrap/` kit.** This is the *runnable* half of the project:
- `0-enable-wsl.ps1` — PowerShell script to enable WSL2 + Docker Desktop
- `install.sh` — Ubuntu install script (Claude Code, gstack, ruflo, OpenHands, CrewAI, n8n, scanners)
- `CLAUDE.md` — gstack project configuration for Claude Code
- `litellm-config.yaml` — the Token Optimizer router config (implements `13-model-router`)
- `.env.example` — template for all API keys (never committed with real values)
And then Task #5: `bootstrap/replication-engine/` (CrewAI Python + run.py) + `bootstrap/90-DAY-PLAN.md`.

**MODEL ESCALATION NOTE:** Tasks #4–5 involve real code (bash scripts, Python/CrewAI, YAML config,
security-sensitive .env patterns) → **recommend switching back to Opus 4.8** before starting them.
Flag the user before Task #4 begins.

Git remote `origin` is already set and credentials are cached.

## Build order
1. ✅ `00-MASTER-BLUEPRINT.md`
2. ✅ `company-os/` core (4 files)
3. ✅ `company-os/` division files (11 files)
4. ⬜ `bootstrap/` scripts + configs (Task #4)
5. ⬜ `bootstrap/replication-engine/` + `bootstrap/90-DAY-PLAN.md` (Task #5)
6. ✅ top-level `README.md`

## Task IDs (in the session task list)
- #1 Master blueprint
- #2 company-os core files
- #3 company-os division files
- #4 bootstrap install + config
(Replication engine, 90-day plan, and README are folded into the build order above; add tasks if resuming.)

## Notes for whoever continues
- Update the file-status table in `PROJECT_CONTEXT.md` §1 as files get created.
- After a meaningful chunk is done (a "milestone"), refresh all three handoff files and offer the user a
  fresh chat.
- Give the model-escalation heads-up before each big/difficult chunk.
