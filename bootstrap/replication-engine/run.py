#!/usr/bin/env python3
"""
The Startup Replication Engine — entry point (blueprint Part 8).

Usage:
    python run.py "clone a US startup for India"          # free-form brief
    python run.py --category "developer tools" --n 8       # explicit category
    python run.py --demo                                   # offline: uses bundled sample data

What it does:
    1. (live) Runs the CrewAI crew to source + score candidates, OR (--demo) loads samples.
    2. Ranks them DETERMINISTICALLY with the weighted rubric (rubric.py) — not the LLM.
    3. Writes a ranked shortlist + a build brief for the winner into ./out/<timestamp>/.

The build brief feeds Product Factory stage 4 (gstack /office-hours), where YOU make the
final human call. This engine narrows the field; it does not decide for you.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import rubric

# Make stdout robust on non-UTF8 consoles (e.g. Windows cp1252) so ₹/emoji never crash.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).parent


# ── tolerant JSON extraction ────────────────────────────────────────────────
def extract_json_array(text: str) -> Optional[list]:
    """Pull the first JSON array out of an LLM response (handles fences/prose)."""
    # 1. straight parse
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass
    # 2. fenced ```json ... ```
    fence = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
    if fence:
        try:
            return json.loads(fence.group(1))
        except json.JSONDecodeError:
            pass
    # 3. first '[' to last ']'
    start, end = text.find("["), text.rfind("]")
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    return None


# ── reporting ───────────────────────────────────────────────────────────────
def render_shortlist(ranked: List[dict], category: str) -> str:
    lines = [
        f"# Replication Engine — shortlist", "",
        f"**Category/brief:** {category}  ",
        f"**Generated:** {datetime.now(timezone.utc).isoformat(timespec='seconds')}  ",
        f"**Scoring:** weighted rubric (blueprint Part 8), max {rubric.MAX_WEIGHTED}.", "",
        "| # | Candidate | Score | % | One-liner |",
        "|---|---|---|---|---|",
    ]
    for i, c in enumerate(ranked, 1):
        flag = " ⚠️" if c.get("score_problems") else ""
        lines.append(
            f"| {i} | **{c.get('name','?')}**{flag} | {c['weighted_total']:.0f} | {c['pct']} | "
            f"{c.get('one_liner','').replace('|', '/')} |"
        )
    lines += ["", "### Per-dimension scores", "",
              "| Candidate | " + " | ".join(d.label for d in rubric.RUBRIC) + " |",
              "|---|" + "|".join("---" for _ in rubric.RUBRIC) + "|"]
    for c in ranked:
        s = c.get("scores", {})
        lines.append("| " + c.get("name", "?") + " | " +
                     " | ".join(str(s.get(d.key, "–")) for d in rubric.RUBRIC) + " |")
    return "\n".join(lines) + "\n"


def print_table(ranked: List[dict]) -> None:
    print("\n" + "=" * 64)
    print("  RANKED SHORTLIST (weighted, deterministic)")
    print("=" * 64)
    for i, c in enumerate(ranked, 1):
        print(f"  {i}. {c.get('name','?'):<28} {c['weighted_total']:>5.0f} / {rubric.MAX_WEIGHTED}  ({c['pct']}%)")
        if c.get("score_problems"):
            print(f"       ⚠️  {'; '.join(c['score_problems'])}")
    print("=" * 64 + "\n")


# ── main ─────────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description="Startup Replication Engine (clone-a-US-startup-for-India).")
    ap.add_argument("brief", nargs="?", default="", help='Free-form brief, e.g. "clone a US startup for India".')
    ap.add_argument("--category", default="", help="Explicit category (overrides brief for sourcing).")
    ap.add_argument("--n", type=int, default=6, help="Number of candidates to source (default 6).")
    ap.add_argument("--demo", action="store_true", help="Offline mode: use bundled sample_candidates.json.")
    ap.add_argument("--out", default=str(HERE / "out"), help="Output directory root.")
    args = ap.parse_args()

    try:
        from dotenv import load_dotenv
        # load repo-root .env if present (engine is two levels under the root)
        load_dotenv(HERE.parents[1] / ".env")
    except ImportError:
        pass

    category = args.category or args.brief or "any high-potential SaaS category"
    print(f"\n🧬 Startup Replication Engine\n   brief: {category}\n   mode:  {'DEMO (offline)' if args.demo else 'LIVE (CrewAI via LiteLLM)'}")

    # 1. get candidates ------------------------------------------------------
    if args.demo:
        sample = HERE / "sample_candidates.json"
        if not sample.exists():
            print(f"  [x] sample data not found at {sample}")
            return 1
        candidates = json.loads(sample.read_text(encoding="utf-8"))
        print(f"   loaded {len(candidates)} sample candidates.")
    else:
        try:
            import crew
        except ImportError as e:
            print(f"  [x] Could not import the crew ({e}). Install deps: pip install -r requirements.txt")
            print("      Or try offline:  python run.py --demo")
            return 1
        print("   running crew (source → score → regulation → synthesize)...\n")
        try:
            raw = crew.run_crew(category, args.n)
        except Exception as e:  # noqa: BLE001
            print(f"  [x] Crew run failed: {e}")
            print("      Is the LiteLLM proxy up?  litellm --config bootstrap/litellm-config.yaml")
            print("      To preview output format without keys:  python run.py --demo")
            return 1
        candidates = extract_json_array(raw)
        if not candidates:
            print("  [x] Could not parse a JSON array from the crew output. Raw output below:\n")
            print(raw[:2000])
            return 1
        print(f"   parsed {len(candidates)} candidates from crew output.")

    # 2. rank deterministically ---------------------------------------------
    ranked = rubric.rank(candidates)
    print_table(ranked)

    # 3. write outputs -------------------------------------------------------
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.out) / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "shortlist.md").write_text(render_shortlist(ranked, category), encoding="utf-8")
    (out_dir / "candidates.json").write_text(json.dumps(ranked, indent=2), encoding="utf-8")

    winner = ranked[0]
    print(f"🏆 Winner: {winner.get('name')}  ({winner['pct']}%)")

    if not args.demo:
        try:
            import crew
            print("   writing build brief for the winner...")
            brief_md = crew.generate_build_brief(winner, category)
            (out_dir / f"build-brief-{_slug(winner.get('name','winner'))}.md").write_text(brief_md, encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            print(f"  [!] Build brief generation skipped ({e}). Scores + shortlist still written.")
    else:
        print("   (demo mode: skipping LLM build brief — run live to generate it.)")

    print(f"\n✅ Outputs written to: {out_dir}")
    print("   Next: review shortlist.md, then take the build brief into gstack /office-hours")
    print("   for the final human call (Product Factory stage 4).\n")
    return 0


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "winner"


if __name__ == "__main__":
    sys.exit(main())
