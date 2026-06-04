"""
The Startup Replication Engine — scoring rubric (blueprint Part 8).

Design principle (matches the company's "determinism where it matters" rule):
the LLM *judges* each dimension on a 0–5 scale; THIS module does the weighted
arithmetic. Keeping the math in code — not in the model — makes the ranking
reproducible, auditable, and immune to an LLM "feeling" that one candidate
should win. The crew supplies opinions; Python supplies the verdict.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Dimension:
    key: str            # machine key used in the scores dict
    label: str          # human label for reports
    weight: int         # multiplier from the blueprint rubric
    question: str       # the question the LLM answers (framed so 5 = best)
    note: str = ""      # extra guidance / blueprint nuance


# All questions are framed so that a HIGHER score is always BETTER.
# The blueprint marks "Regulatory load" as inverse-weighted; we implement that
# by scoring it positively as "regulatory lightness" (5 = minimal burden), so the
# weighted sum stays a simple higher-is-better total. Same outcome, no sign bugs.
RUBRIC: List[Dimension] = [
    Dimension("tam",           "TAM (India)",              3, "Is the Indian market big and growing?"),
    Dimension("demand",        "Demand evidence",          3, "Are people already paying for this (US or India)?"),
    Dimension("competition",   "Competition gap",          2, "Is the India space underserved / are incumbents weak?"),
    Dimension("feasibility",   "Build feasibility (solo)", 3, "Can a 1-person + agent org ship an MVP in <90 days?"),
    Dimension("reg_lightness", "Regulatory lightness",     2, "Is the compliance burden LOW? (5=low, fintech/health=0–1)",
              note="Blueprint inverse dimension, scored positively."),
    Dimension("distribution",  "Distribution path",        3, "Is there a cheap, automatable channel to first users?"),
    Dimension("monetization",  "Monetization",             2, "Clear willingness-to-pay and sane ₹ pricing?"),
    Dimension("moat",          "Moat potential",           1, "Can localization/quality create durable advantage?"),
]

DIM_KEYS: List[str] = [d.key for d in RUBRIC]
TOTAL_WEIGHT: int = sum(d.weight for d in RUBRIC)   # 19
MAX_RAW: int = 5
MAX_WEIGHTED: int = MAX_RAW * TOTAL_WEIGHT           # 95


def weighted_total(scores: Dict[str, float]) -> float:
    """Weighted sum of the 8 dimension scores. Missing dims count as 0."""
    return float(sum(float(scores.get(d.key, 0)) * d.weight for d in RUBRIC))


def normalized_pct(scores: Dict[str, float]) -> float:
    """Weighted total as a 0–100% of the theoretical maximum (95)."""
    return round(100.0 * weighted_total(scores) / MAX_WEIGHTED, 1)


def validate_scores(scores: Dict[str, float]) -> List[str]:
    """Return a list of human-readable problems with a scores dict (empty = OK)."""
    problems: List[str] = []
    for d in RUBRIC:
        if d.key not in scores:
            problems.append(f"missing dimension '{d.key}'")
            continue
        try:
            v = float(scores[d.key])
        except (TypeError, ValueError):
            problems.append(f"'{d.key}' is not a number: {scores[d.key]!r}")
            continue
        if not (0 <= v <= 5):
            problems.append(f"'{d.key}' out of range 0–5: {v}")
    return problems


def rubric_as_prompt() -> str:
    """The rubric rendered for an LLM scoring prompt."""
    lines = ["Score each dimension 0–5 (5 = best). Dimensions and weights:"]
    for d in RUBRIC:
        extra = f" — {d.note}" if d.note else ""
        lines.append(f"  - {d.key} (×{d.weight}): {d.question}{extra}")
    lines.append(
        "\nReturn ONLY a JSON object mapping each key to an integer 0–5, "
        "plus a 'rationale' object mapping each key to a one-sentence reason."
    )
    return "\n".join(lines)


def rank(candidates: List[dict]) -> List[dict]:
    """
    Given candidates [{name, scores, ...}], attach weighted_total + pct and
    return them sorted best-first. Pure function; does not mutate inputs.
    """
    ranked = []
    for c in candidates:
        scores = c.get("scores", {})
        ranked.append({
            **c,
            "weighted_total": weighted_total(scores),
            "pct": normalized_pct(scores),
            "score_problems": validate_scores(scores),
        })
    ranked.sort(key=lambda c: c["weighted_total"], reverse=True)
    return ranked


if __name__ == "__main__":
    import sys
    # Make stdout robust on non-UTF8 consoles (e.g. Windows cp1252) so ₹/emoji never crash.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    # Smoke test: a perfect candidate scores 95 / 100%.
    perfect = {d.key: 5 for d in RUBRIC}
    assert weighted_total(perfect) == MAX_WEIGHTED, "weighted math is wrong"
    assert normalized_pct(perfect) == 100.0
    assert validate_scores(perfect) == []
    print(f"Rubric OK. {len(RUBRIC)} dimensions, total weight {TOTAL_WEIGHT}, max {MAX_WEIGHTED}.")
    print(rubric_as_prompt())
