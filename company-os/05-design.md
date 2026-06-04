# 05 — Design Division

> **Mission.** Produce UI/UX that feels genuinely world-class — surprising, tasteful, and obviously not
> a shadcn-default template — within the constraints of what a solo founder can ship quickly.
> Blueprint source: Parts 3 & 7 (stage 5). **Layer: 1 (design gates) + 2 (inspiration scraping +
> variant generation).** Powered by: **gstack `/design-*` skills for all gates; a CrewAI scraping crew
> for inspiration; v0/Aceternity/Magic UI for generation.**

---

## 1. Roles

| Role | One-line job |
|---|---|
| **Design Researcher** | Scrape Mobbin/Awwwards/Dribbble/Behance/godly.website for patterns that match the product's tone |
| **UI Ideation Agent** | Generate N design variants from the brief (anti-generic; "what would win an Awwwards Site of the Day?") |
| **Motion / Animation Specialist** | Spec the micro-interactions and hero animations using Framer Motion / GSAP primitives |
| **Visual Identity Agent** | Derive color system, type scale, spacing, and brand-consistent component overrides |
| **Design Reviewer** | Gate: does this meet the taste bar? (this is you + `/design-review`) |

---

## 2. Layer mapping

| Role | Layer | Implementation |
|---|---|---|
| Design Researcher | **2 (worker)** | CrewAI agent + browser-use + Firecrawl |
| UI Ideation | **2 (worker)** | gstack `/design-shotgun` (variant explosion) + v0 for generation |
| Motion Specialist | **2 (worker)** | CrewAI agent — outputs an animation spec (not code yet) |
| Visual Identity | **1+2** | gstack `/design-consultation` (you + Claude) for the system; cheap model for component overrides |
| **Design review gate** | **1 (gate)** | gstack `/design-review` — you trigger |
| **HTML mockup gate** | **1 (gate)** | gstack `/design-html` — Claude produces a live HTML preview for your approval |

---

## 3. Inputs

| From | What |
|---|---|
| [[03-product]] | Design brief: problem, user, visual constraints, "wow factor" goal, mobile-first flag |
| [[12-company-brain]] | `brain/brand/` — voice, naming, any prior design system decisions |
| [[02-research]] | Competitor UI patterns (what to avoid looking like) |
| [[01-executive]] | Any aesthetic direction set in `/office-hours` |

---

## 4. Outputs

| To | What | Written where |
|---|---|---|
| [[04-engineering]] | Design system (colors, typography, spacing, component spec), hi-fi screens, animation spec | `brain/specs/<product>-design-system.md` + referenced assets |
| [[01-executive]] | Design review submission | `tasks/<id>/design-review.md` with live HTML preview |
| [[12-company-brain]] | Approved design system (after gate) | `brain/brand/<product>-design-system.md` |

---

## 5. Tools

| Tool | Purpose |
|---|---|
| **gstack `/design-shotgun`** | Variant explosion: generate N very different design directions from one brief |
| **gstack `/design-consultation`** | Design system: define and interrogate the full visual language |
| **gstack `/design-html`** | Produce a live, styled HTML prototype for review — not wireframes |
| **gstack `/design-review`** | Gate: critique the design against the brief and the taste bar |
| **v0 (Vercel)** | AI-generated React/Next.js UI — fast scaffolding for components |
| **browser-use + Firecrawl** | Scrape Mobbin, Awwwards, Dribbble, Behance, godly.website, land-book |
| **shadcn/ui** | The base component system — start here for interactive elements |
| **Aceternity UI** | Animated, "wow" components (spotlight, 3D cards, parallax) |
| **Magic UI** | Micro-animation components for delight moments |
| **21st.dev** | Modern design system library and component browser |
| **tweakcn** | Theme customizer on top of shadcn — avoid the default look |
| **Framer Motion** | React animation library for fluid transitions |
| **GSAP** | High-performance animation for hero/scroll effects |

---

## 6. Quality gates

| Gate | Trigger | Pass criteria | Fail action |
|---|---|---|---|
| **`/design-review`** | After variant selection and before HTML mockup | Design doesn't look like a generic shadcn template; typography hierarchy is clear; mobile layout works; color contrast is AA-accessible; the "wow" moment is present | Return with specific tasteful critique; re-run `/design-shotgun` or iterate |
| **HTML mockup review (you)** | After `/design-html` produces the live preview | You would be proud to show this to a stranger; it matches the brand brief; interactions feel polished | Return; rework the specific weak areas |

> **The taste bar (non-negotiable):** the standard is *"would a design-conscious user think this was made
> by a professional agency, not a bootstrapper with a template?"* gstack's `/design-shotgun` and
> `/design-review` are calibrated to this. If a design feels generic, it fails the gate, every time.

---

## 7. Model routing

| Task | Default tier | Notes |
|---|---|---|
| Design inspiration scraping + synthesis | Free (Gemini Flash) | Long context; pattern extraction |
| Variant generation (brief → concepts) | **Premium (Claude)** | `/design-shotgun` uses Claude for taste |
| HTML mockup (live prototype) | **Premium (Claude)** | `/design-html` — quality critical |
| `/design-review` gate | **Premium (Claude)** | Gate exception |
| Animation spec writing | Cheap (DeepSeek) | Structured output; not taste-critical |
| Component override generation (colors, themes) | Cheap (Qwen / DeepSeek) | Mechanical; reviewed at gate |

---

## 8. Memory

| Read | Write |
|---|---|
| `brain/brand/` — voice, existing design system, prior design decisions | `brain/brand/<product>-design-system.md` — approved design system |
| `brain/specs/` — the PRD with user/UX constraints | `brain/decisions/` — design trade-offs (e.g., "chose Framer Motion over CSS for hero because…") |
| ruflo AgentDB — SONA patterns (what visual styles won in prior reviews) | ruflo AgentDB — update after each accepted design |

---

## 9. Escalation triggers

Design agents escalate to [[01-executive]] when:

- The brief is too vague to produce a meaningful variant (no user, no "wow" direction, no competitive
  reference to differentiate from).
- All generated variants pass `/design-review` but feel homogeneous — a direction decision is needed from
  you before spending more on iteration.
- A visual identity choice has significant brand or business implications (e.g., a name or color that
  might conflict with a competitor's trademark).
- Engineering says a proposed design requires a library or animation technique that materially increases
  bundle size or breaks the performance budget.

---

## 10. Playbooks

### PLAY-D1: Design a new product UI from scratch

```
1. Receive design brief from [[03-product]] (problem, user, constraints, "wow" goal).
2. Dispatch research Task Contract to Design Researcher: "Find 5–10 UI patterns from Mobbin/Awwwards that match <tone> for <use-case>. Include: color palettes, typography choices, micro-interaction examples."
3. Run gstack /design-consultation to establish the design system: color scale, type scale, spacing, iconography, component decisions.
4. Run gstack /design-shotgun with the brief + research output: produce 3 radically different directions.
5. You pick one (or blend two). Note the choice in brain/decisions/.
6. Run gstack /design-html: produce a live HTML prototype of the key screen(s).
7. Gate: gstack /design-review. Return / iterate until it passes your taste bar.
8. Write the approved design system to brain/brand/<product>-design-system.md.
9. Issue the design handoff to [[04-engineering]]: component list + specs + animation brief.
```

### PLAY-D2: Redesign a specific screen or flow

```
1. Trigger: a /retro finding that a specific screen has low conversion, high drop-off, or user complaints.
2. Pull: current design from brain/brand/ + user feedback from brain/research/.
3. Run /design-shotgun scoped to the problem screen only (3 variants).
4. Run /design-html for the winning variant.
5. /design-review gate.
6. If accepted: issue a scoped engineering Task Contract to [[04-engineering]].
7. After ship: A/B test if possible; write result to brain/retros/.
```

---

## 11. KPIs / signals

| Signal | What it means | Bad state |
|---|---|---|
| `/design-review` pass rate | % accepted on first submission | < 50% = brief is too vague or variants are too generic |
| Variant round-trips | Iterations before a design is accepted | > 3 = the brief needs more constraints, or research is weak |
| "Wow factor" (you) | Gut feel: would you be proud to show this? | No = stop; don't ship it |
| Engineering complaint rate | # times engineers say "we can't build this" | > 1/sprint = design is ignoring technical constraints |
| User onboarding completion rate | % of new users reaching first key action | < target = UX flow has a gap; trigger PLAY-D2 |
