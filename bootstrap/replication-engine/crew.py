"""
The Startup Replication Engine — the CrewAI crew (blueprint Part 8).

Pipeline:  Source candidates -> Score (8-dim rubric) -> India-fit review -> Synthesize JSON
Then run.py ranks deterministically (rubric.py) and a focused LLM call writes the
build brief for the winner.

All model calls go through the LiteLLM proxy (company-os/13-model-router.md), using
task-class ALIASES, never raw provider model names. Research/scoring runs on the cheap
`research-free` alias; the final build brief uses `claude-gate-light` (a little more
quality for the artifact that seeds the Product Factory).
"""
from __future__ import annotations

import os
from typing import List, Optional

from rubric import rubric_as_prompt

# LiteLLM proxy connection (defaults match bootstrap/litellm-config.yaml)
PROXY_BASE = os.getenv("LITELLM_BASE_URL") or os.getenv("OPENAI_API_BASE") or "http://localhost:4000"
PROXY_KEY = os.getenv("LITELLM_MASTER_KEY") or os.getenv("OPENAI_API_KEY") or "sk-no-key-set"

INDIA_LENS = (
    "Apply India-specific lenses throughout: UPI/payments, pricing in ₹ (often 10–50× lower "
    "than US), regional languages, mobile-first/low-bandwidth users, GST + DPDP-Act compliance, "
    "and distribution via WhatsApp/YouTube/SEO."
)


def _make_llm(alias: str = "research-free"):
    """Build a CrewAI LLM bound to the LiteLLM proxy using a task-class alias."""
    from crewai import LLM
    return LLM(model=f"openai/{alias}", base_url=PROXY_BASE, api_key=PROXY_KEY)


def _search_tools() -> List:
    """Attach a web-search tool only if a key is present; otherwise agents reason from knowledge."""
    tools: List = []
    if os.getenv("SERPER_API_KEY"):
        try:
            from crewai_tools import SerperDevTool
            tools.append(SerperDevTool())
        except Exception as e:  # noqa: BLE001
            print(f"  [!] SerperDevTool unavailable ({e}); continuing without live search.")
    return tools


def build_crew(category: str, n_candidates: int = 6):
    """Assemble the 4-agent crew for one replication run."""
    from crewai import Agent, Task, Crew, Process

    research_llm = _make_llm("research-free")
    tools = _search_tools()

    # ── Agents ───────────────────────────────────────────────────────────────
    scout = Agent(
        role="Opportunity Scout",
        goal=f"Source promising US startups in '{category}' that a solo founder could replicate for India.",
        backstory=(
            "You comb YC batches, Product Hunt, Crunchbase, and G2 for proven US startups with clear "
            "traction whose model could be localized for India. You prefer simple, focused products over "
            "sprawling platforms."
        ),
        llm=research_llm, tools=tools, verbose=True, allow_delegation=False,
    )
    analyst = Agent(
        role="India Market Analyst",
        goal="Score each candidate on the 8-dimension replication rubric for the Indian market.",
        backstory=(
            "You size Indian markets and judge demand, competition, feasibility, distribution, "
            "monetization, and moat with a brutally realistic eye. You never inflate scores. " + INDIA_LENS
        ),
        llm=research_llm, tools=tools, verbose=True, allow_delegation=False,
    )
    regulator = Agent(
        role="Regulation & Localization Analyst",
        goal="Assess India regulatory burden and localization fit; correct the regulatory-lightness score.",
        backstory=(
            "You know the DPDP Act, GST, RBI/fintech rules, and health-data regulation. You flag heavy "
            "compliance burdens and note exactly what localization (payments, language, pricing) each "
            "candidate needs. " + INDIA_LENS
        ),
        llm=research_llm, tools=tools, verbose=True, allow_delegation=False,
    )
    synthesizer = Agent(
        role="Chief of Staff",
        goal="Consolidate everything into one strict JSON array the ranking engine can parse.",
        backstory="You turn messy analysis into clean, machine-readable JSON. You output JSON and nothing else.",
        llm=research_llm, verbose=True, allow_delegation=False,
    )

    # ── Tasks (sequential; each sees prior outputs as context) ────────────────
    t_source = Task(
        description=(
            f"Find {n_candidates} US startups in '{category}' suitable for India replication. "
            "For each give: name, one-line description, the US traction signal (funding/users/revenue if "
            "known), and why it might fit India. Prefer focused products an agent-run solo team could MVP fast."
        ),
        expected_output=f"A numbered list of {n_candidates} candidates, each with the 4 fields above.",
        agent=scout,
    )
    t_score = Task(
        description=(
            "For EACH candidate from the scout, score the replication rubric.\n\n"
            + rubric_as_prompt()
            + "\n\nBe realistic and discriminating — do not give everything 4s and 5s."
        ),
        expected_output="Per candidate: the 8 integer scores (0–5) and a one-line rationale for each.",
        agent=analyst,
        context=[t_source],
    )
    t_reg = Task(
        description=(
            "Review each candidate's India regulatory burden and localization needs. Correct the "
            "'reg_lightness' score if the analyst under/over-rated compliance load (fintech, lending, "
            "health, and data-heavy products are HEAVY = low lightness). Add a 2–3 sentence 'india_fit' note "
            "covering payments, language, pricing, and the main compliance flag."
        ),
        expected_output="Per candidate: a corrected reg_lightness score (if needed) and an india_fit note.",
        agent=regulator,
        context=[t_source, t_score],
    )
    t_synth = Task(
        description=(
            "Consolidate the scout + analyst + regulator outputs into a STRICT JSON array. Output ONLY the "
            "JSON (no prose, no markdown fences). Each element MUST be:\n"
            "{\n"
            '  "name": str,\n'
            '  "one_liner": str,\n'
            '  "us_signal": str,\n'
            '  "scores": {"tam":int, "demand":int, "competition":int, "feasibility":int,\n'
            '             "reg_lightness":int, "distribution":int, "monetization":int, "moat":int},\n'
            '  "rationale": {"<dim>": str, ...},\n'
            '  "india_fit": str\n'
            "}\n"
            "All 8 score keys are required, integers 0–5."
        ),
        expected_output="A single JSON array of candidate objects. No text outside the JSON.",
        agent=synthesizer,
        context=[t_source, t_score, t_reg],
    )

    return Crew(
        agents=[scout, analyst, regulator, synthesizer],
        tasks=[t_source, t_score, t_reg, t_synth],
        process=Process.sequential,
        verbose=True,
    )


def run_crew(category: str, n_candidates: int = 6) -> str:
    """Execute the crew and return the synthesizer's raw output (expected: a JSON array)."""
    crew = build_crew(category, n_candidates)
    result = crew.kickoff()
    return str(result)


def generate_build_brief(winner: dict, category: str) -> str:
    """
    Write a build brief (markdown) for the winning candidate via a focused LLM call.
    This is the artifact that seeds Product Factory stage 4 (gstack /office-hours).
    Uses `claude-gate-light` for a bit more quality on the hand-off document.
    """
    import litellm

    sys_prompt = (
        "You are a product strategist writing a build brief for a solo, agent-assisted founder targeting "
        "India. Be concrete, realistic, and honest about risks. " + INDIA_LENS
    )
    user_prompt = (
        f"Category: {category}\n"
        f"Winning candidate: {winner.get('name')}\n"
        f"One-liner: {winner.get('one_liner')}\n"
        f"US signal: {winner.get('us_signal')}\n"
        f"Rubric scores (0–5): {winner.get('scores')}\n"
        f"Weighted score: {winner.get('weighted_total')} / 95 ({winner.get('pct')}%)\n"
        f"India fit notes: {winner.get('india_fit')}\n\n"
        "Write a build brief with these sections (markdown):\n"
        "1. The bet (1 paragraph: what we're building and why it can work in India)\n"
        "2. Target user & job-to-be-done\n"
        "3. MVP scope (explicit IN and OUT — shippable in <90 days by a solo+agent team)\n"
        "4. Localization plan (payments, language, ₹ pricing, distribution channel)\n"
        "5. Top 3 risks and how we'd de-risk each\n"
        "6. First 3 build steps (feeding gstack /office-hours)\n"
    )
    resp = litellm.completion(
        model="openai/claude-gate-light",
        api_base=PROXY_BASE,
        api_key=PROXY_KEY,
        messages=[{"role": "system", "content": sys_prompt},
                  {"role": "user", "content": user_prompt}],
    )
    return resp["choices"][0]["message"]["content"]
