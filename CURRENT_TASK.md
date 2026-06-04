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

⏭️ **NEXT: Task #3 — the 11 division files** (`01-executive` → `11-finance-token-optimizer`). They all
follow the **role-spec schema defined in `00-architecture.md` §3** (Roles · Layer mapping · Inputs ·
Outputs · Tools · Quality gates · Model routing · Memory · Escalation · Playbooks · KPIs). This step is
templated/repetitive → a good candidate for **Sonnet 4.6** to conserve Opus quota (flag the user first).

Git remote `origin` is already set and credentials are cached, so `git add -A && git commit && git push`
works directly. `gh` CLI is NOT installed (use git + the GitHub integration).

## Build order (author these, in order)
1. ✅ `00-MASTER-BLUEPRINT.md` — full 13-part merged report (reality-check first)
2. ✅ `company-os/_INDEX.md` + `00-architecture.md` + `12-company-brain.md` + `13-model-router.md`
3. ⬜ `company-os/` division files (executive → finance/token-optimizer) — use `00-architecture.md` §3 schema
4. ⬜ `bootstrap/0-enable-wsl.ps1`, `install.sh`, `CLAUDE.md`, `litellm-config.yaml`, `.env.example`
5. ⬜ `bootstrap/replication-engine/` + `bootstrap/90-DAY-PLAN.md`
6. ✅ top-level `README.md` (open-source front door + quick start) — done early

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
