# 🧬 The Startup Replication Engine

> **Your first move** (blueprint [Part 8](../../00-MASTER-BLUEPRINT.md#part-8--the-startup-replication-engine-your-first-move)).
> Input: *"clone a successful US startup and build the Indian equivalent."* Output: a **ranked shortlist**
> of candidates + a **build brief** for the winner, ready to hand to gstack `/office-hours` (Product
> Factory stage 4). It narrows the field with a weighted rubric; **you** make the final call.

## How it works

```
 Source candidates ─►  Score (8-dim rubric)  ─►  India-fit review  ─►  Synthesize JSON
 (Opportunity Scout)    (India Market Analyst)    (Regulation Analyst)   (Chief of Staff)
        └─────────────────────── CrewAI crew, via the LiteLLM proxy ───────────────────┘
                                          │
                                          ▼
                       rubric.py ranks DETERMINISTICALLY (not the LLM)
                                          │
                                          ▼
                    out/<timestamp>/  shortlist.md · candidates.json · build-brief-<winner>.md
```

The LLM *judges* each dimension 0–5; **Python does the weighted arithmetic** (`rubric.py`). That keeps the
ranking reproducible and auditable — the crew supplies opinions, code supplies the verdict.

## The rubric (blueprint Part 8)

| Dimension | Weight | Scored as (5 = best) |
|---|---|---|
| TAM (India) | ×3 | Is the Indian market big and growing? |
| Demand evidence | ×3 | Are people already paying for this? |
| Competition gap | ×2 | Is the space underserved / incumbents weak? |
| Build feasibility (solo) | ×3 | MVP shippable in <90 days by a solo+agent team? |
| Regulatory lightness | ×2 | Is compliance burden LOW? (fintech/health = 0–1) |
| Distribution path | ×3 | Cheap, automatable channel to first users? |
| Monetization | ×2 | Clear willingness-to-pay, sane ₹ pricing? |
| Moat potential | ×1 | Can localization/quality create durable advantage? |

Max weighted score = **95** (5 × total weight 19). Reported as a 0–100%.

## Quick start

```bash
# From the repo root, with the Python venv active (see bootstrap/install.sh):
cd bootstrap/replication-engine
pip install -r requirements.txt

# 1. Offline demo — no API keys needed, shows the output format + ranking:
python run.py --demo

# 2. Live run — needs the LiteLLM proxy up (litellm --config bootstrap/litellm-config.yaml):
python run.py "clone a US startup for India"
python run.py --category "developer tools for SMBs" --n 8
```

### Prerequisites for a live run
- The **LiteLLM proxy** running (`litellm --config bootstrap/litellm-config.yaml`) with at least one free
  key set in the repo-root `.env` (e.g. `GEMINI_API_KEY`). The crew uses the `research-free` alias.
- *(Optional)* `SERPER_API_KEY` in `.env` to give the scout live web search; without it, agents reason
  from model knowledge (fine for a first pass, less current).

## Output

Each run writes a timestamped folder under `out/`:
- **`shortlist.md`** — the ranked table + a per-dimension score matrix.
- **`candidates.json`** — full machine-readable results (scores, rationale, india_fit, weighted totals).
- **`build-brief-<winner>.md`** — the bet, target user, MVP scope, localization plan, top risks, and the
  first 3 build steps. *This is the artifact you take into `/office-hours`.*

## Files

| File | Role |
|---|---|
| `run.py` | CLI entry: orchestrates, ranks deterministically, writes outputs (`--demo` for offline) |
| `crew.py` | The 4-agent CrewAI crew + the build-brief generation call |
| `rubric.py` | The weighted 8-dimension rubric + ranking math (run it directly for a self-test) |
| `sample_candidates.json` | Bundled demo data so `--demo` works with zero keys |
| `requirements.txt` | Dependencies (live mode) |

## Honest caveats

- **This narrows, it doesn't decide.** The human gate (`/office-hours`) is the point — the engine is a
  funnel, not an oracle. Garbage sourcing → garbage ranking; review the shortlist critically.
- **CrewAI and LiteLLM APIs move fast.** If a live run errors on an import or model string, check the
  current library versions (the demo path is pure-stdlib and stable for testing the rest).
- **Free-tier sourcing is only as current as the model's knowledge** unless you wire in live search.
  Re-verify any traction/market claim before betting on it.
- The bundled samples are **illustrative**, not investment advice — note how the rubric correctly
  penalizes the high-regulation fintech/health candidates despite their large TAM.
