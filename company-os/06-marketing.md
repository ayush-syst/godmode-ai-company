# 06 — Marketing Division

> **Mission.** Generate discovery and demand for each product — through content, SEO, social, and
> programmatic outreach — on a near-zero budget, primarily with free models and automation.
> Blueprint source: Part 3 (stage 11). **Layer: 2 (autonomous swarm).** Powered by: **CrewAI crews +
> n8n automation.** All brand-voice-defining pieces and campaign launches require **your approval** before
> going out — that is the gate here.

---

## 1. Roles

| Role | One-line job |
|---|---|
| **SEO Strategist** | Find high-intent, low-competition keyword clusters; produce topic plans; track rank changes |
| **Content Writer** | Produce blog posts, landing copy, documentation, and long-form content |
| **Copywriter** | Write punchy, conversion-focused short copy: headlines, CTA, pricing page, ads |
| **Social Media Agent** | Draft and schedule posts for Twitter/X, LinkedIn, and relevant India communities |
| **Video Script Writer** | Write YouTube/Reels scripts for product demos and educational content |
| **Growth Hacker** | Identify and test distribution channels (communities, directories, cold outreach, Product Hunt) |

---

## 2. Layer mapping

| Role | Layer | Implementation |
|---|---|---|
| SEO Strategist | **2 (worker)** | CrewAI agent + free SEO APIs (Ahrefs free / DataForSEO / Google Search Console) |
| Content Writer | **2 (worker)** | CrewAI agent; drafts on free models |
| Copywriter | **2 (worker)** | CrewAI agent; shorter outputs |
| Social Media Agent | **2 (worker)** | CrewAI agent + n8n scheduler |
| Video Script Writer | **2 (worker)** | CrewAI agent |
| Growth Hacker | **2 (worker)** | CrewAI agent + browser-use for directory/community research |
| **Brand voice review** | **1 (gate — you)** | You review brand-defining pieces before first publish |
| **Campaign launch review** | **1 (gate — you)** | You approve every new channel / campaign before it runs |

---

## 3. Inputs

| From | What |
|---|---|
| [[03-product]] | Approved product spec, ICP definition, value proposition, pricing |
| [[12-company-brain]] | `brain/brand/` — voice, tone, naming, messaging guidelines |
| [[02-research]] | Competitor content gaps, keyword opportunities, India market language |
| [[01-executive]] | Approved brand voice decisions (from `/office-hours` or decisions/) |
| [[08-customer-success]] | User language (exact words customers use to describe their problem) — gold for copy |

---

## 4. Outputs

| To | What | Written where |
|---|---|---|
| You (for review) | Blog drafts, campaign plans, social calendars | `tasks/<id>/marketing-draft.md` |
| Publishing | Approved content → posted/scheduled via n8n | n8n queue → external platforms |
| [[12-company-brain]] | Accepted messaging, proven copy, voice decisions | `brain/brand/copy-patterns.md` |
| [[01-executive]] | Growth/traffic/conversion signals for CEO review | Founder Dashboard (n8n push) |

---

## 5. Tools

| Tool | Purpose |
|---|---|
| **CrewAI** | Role-based marketing crews — easy to run one-off or scheduled |
| **n8n** | Schedule social posts; automate newsletter sends; push to CMS; trigger content crews |
| **Firecrawl** | Scrape competitor blog structures, landing pages, keyword patterns |
| **browser-use** | Submit to directories (ProductHunt, IndieHackers, AppSumo marketplace, Saas directories) |
| **Google AI Studio (Gemini Flash)** | Default model for all content drafts — free, large context |
| **Groq (Llama 3.3 70B)** | Fast drafts for short-form copy |
| **Google Search Console** | SEO signal tracking (free, requires site ownership) |
| **Plausible / Umami** | Privacy-friendly analytics (self-hostable); feed into Founder Dashboard |
| **Buffer / n8n** | Social scheduling (n8n preferred — self-hosted, no SaaS dependency) |

---

## 6. Quality gates

| Gate | Trigger | Pass criteria | Fail action |
|---|---|---|---|
| **Brand voice review (you)** | Before first piece of each content type is published | Matches the voice in `brain/brand/`; not generic/corporate; India-localized where appropriate; no claims that contradict the blueprint's honesty mandate | Rewrite with specific notes; update the brand brief if the voice needs refining |
| **Campaign launch review (you)** | Before any new channel or campaign goes live | Distribution channel is legal and ToS-compliant; copy passes honest-marketing test; target audience is the defined ICP | Block; revise |
| **SEO plan review (you, light)** | Before content calendar is set | Keywords are in target difficulty range; plan covers the funnel (awareness → consideration → decision); India-language variants considered | Adjust targeting |

---

## 7. Model routing

| Task | Default tier | Notes |
|---|---|---|
| Long-form blog posts | Free (Gemini Flash) | 1M context; good quality for drafts |
| Short-form copy | Free (Groq / Cerebras) | Speed matters; reviewed before publish |
| SEO keyword analysis | Free (Gemini Flash) | Pattern matching over keyword lists |
| Social media calendar | Free (Groq / Llama) | Structured output |
| Video scripts | Free (Gemini Flash) | Long context helpful |
| Growth channel research | Free (Gemini Flash + browser-use) | Research, not judgment |

Marketing never touches Claude premium budget. If a piece is too important for a free model, it means you
should be writing it yourself (that's the judgment/voice gate in action).

---

## 8. Memory

| Read | Write |
|---|---|
| `brain/brand/` — voice, tone, approved messaging | `brain/brand/copy-patterns.md` — what copy worked (after publish + signal) |
| `brain/research/` — ICP, competitor gaps | `tasks/<id>/` — raw content drafts before approval |
| `brain/retros/` — what content/channel worked before | ruflo AgentDB — SONA update: which content angles drove clicks |

---

## 9. Escalation triggers

Marketing agents escalate to you when:

- A content idea requires making a factual claim about a competitor (legal risk).
- A distribution channel requires payment (directory fee, sponsored post).
- A channel is working exceptionally well and deserves more budget or time (growth exploit — needs CEO
  decision to double down).
- A piece of content could be perceived as misleading or over-promising (honesty mandate: blueprint Part 13).
- A partnership or collaboration opportunity comes up that has strategic implications.

---

## 10. Playbooks

### PLAY-M1: Launch content for a new product

```
1. Receive: approved ICP + value proposition + pricing from [[03-product]] / brain/brand/.
2. SEO Strategist: find 10 high-intent, low-competition keyword clusters for the product category. Prioritize India-specific search terms.
3. Copywriter: write the landing page headline, sub-headline, 3 feature bullets, 1 CTA. Voice-review gate (you) before HTML handoff to [[05-design]].
4. Content Writer: write 3 founding blog posts targeting the top keyword clusters.
5. Social agent: draft the launch announcement thread (Twitter/X + LinkedIn + Reddit relevant subreddits).
6. Growth Hacker: prep ProductHunt submission, 3 directories (SaasHub, AppSumo marketplace, etc.), IndieHackers project post.
7. You review everything in one pass. Approve, revise, or block.
8. n8n publishes on the launch date (scheduled).
9. Track: Plausible traffic + Search Console impressions for 2 weeks → retro note.
```

### PLAY-M2: Ongoing SEO content engine (monthly)

```
1. n8n triggers SEO crew on the 1st of each month.
2. SEO Strategist: check Google Search Console for new keyword opportunities and decaying rankings.
3. Content Writer: produce 2–4 blog posts targeting the freshest opportunities.
4. Light brand-voice check (you, async — 15 min review).
5. n8n publishes and pings Google Search Console for re-indexing.
6. After 30 days: SEO Strategist checks rank changes → update SONA patterns.
```

---

## 11. KPIs / signals

| Signal | What it means | Bad state |
|---|---|---|
| Organic traffic (monthly) | SEO is working | Flat for 3+ months = content is off-target or no backlinks |
| Signups from content | Content → conversion | < 1% = copy is not resonating or ICP is wrong |
| Social engagement rate | Distribution is resonating | < 1% → try different format / angle |
| Content velocity | Posts per month | < 4/month = crew is bottlenecked or prompts are bad |
| Brand voice consistency (you) | All public copy sounds like the brand | Violations = update the brand brief and tighten agent prompts |
