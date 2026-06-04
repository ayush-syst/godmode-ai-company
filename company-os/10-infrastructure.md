# 10 — Infrastructure Division

> **Mission.** Keep every product running, observable, and deployable — at the right cost tier for the
> current scale. Blueprint source: Parts 3 & 10. **Layer: 1 (ship/deploy gates) + 2 (monitoring
> automation).** Powered by: **gstack `/ship`, `/land-and-deploy`, `/canary` for deploy gates;
> Coolify → k3s for the platform; Grafana/Prometheus/Sentry/Uptime-Kuma for observability.**

---

## 1. Roles

| Role | One-line job |
|---|---|
| **Platform Engineer** | Own Docker, Coolify, CI/CD pipelines, environment configs |
| **Reliability Monitor** | Watch uptime, error rate, latency — alert before users notice |
| **Scaling Agent** | Detect capacity needs and implement horizontal/vertical scaling |
| **Cost Optimizer** | Track cloud/infra spend; right-size resources; alert on anomalies |
| **Backup & Recovery** | Ensure DB backups run and are restorable; own the rollback procedure |

---

## 2. Layer mapping

| Role | Layer | Implementation |
|---|---|---|
| **Ship gate** | **1 (gate)** | gstack `/ship` + `/land-and-deploy` — you trigger |
| **Canary gate** | **1 (gate)** | gstack `/canary` — you trigger post-deploy |
| Platform Engineer | **2 (worker)** | Claude Code / OpenHands for IaC changes; Coolify for deploy |
| Reliability Monitor | **2 (automated)** | Uptime-Kuma + Grafana/Prometheus alerts; n8n notifications |
| Scaling Agent | **2 (assisted)** | Coolify autoscale config or k3s HPA; manual approval for tier changes |
| Cost Optimizer | **2 (automated)** | Cloud provider + [[11-finance-token-optimizer]] integration |
| Backup & Recovery | **2 (automated)** | Supabase PITR + pg_dump cron via n8n; Coolify volume backups |

---

## 3. Inputs

| From | What |
|---|---|
| [[04-engineering]] | Passing build artifact (Docker image, static export) ready to deploy |
| [[09-security]] | Security clearance (pre-ship `/cso` pass) |
| [[11-finance-token-optimizer]] | Cloud budget status; cost anomaly alerts |
| Product metrics | Usage load, traffic patterns (Plausible/Umami → Grafana) |

---

## 4. Outputs

| To | What | Written where |
|---|---|---|
| [[04-engineering]] | Deploy success/failure + canary health | git deploy record + Founder Dashboard |
| [[01-executive]] | Uptime, latency, error rate, infra cost | Founder Dashboard |
| [[09-security]] | Infra security scan results (Trivy) | PR checks + security findings |
| [[12-company-brain]] | Infrastructure Decision Records (e.g., "moved to k3s at X users") | `brain/decisions/` |

---

## 5. Tools

| Tool | Purpose |
|---|---|
| **gstack `/ship`** | Deploy gate: builds, tests, pushes |
| **gstack `/land-and-deploy`** | Full deploy-to-production flow |
| **gstack `/canary`** | Post-deploy health check: error rate, latency, key flows |
| **Docker** | Containerize everything — no bare-metal deploys |
| **Coolify** (`coollabsio/coolify`, ~30k⭐) | Self-host PaaS: Heroku-like deploys, free, MIT; start here |
| **Dokploy** | Alternative to Coolify if you prefer its UI |
| **k3s** | Lightweight Kubernetes — only when Coolify's single-VPS model is the bottleneck |
| **Supabase** | DB + auth + storage + PITR backups; free tier to start |
| **Cloudflare** | CDN, WAF, DDoS protection, SSL, tunnels (Cloudflare Tunnel replaces public-IP exposure) |
| **Vercel / Netlify** | Static/Edge deploy for frontend-only products (free tier) |
| **Grafana + Prometheus** | Metrics dashboards and alerting |
| **Sentry** | Error tracking with stack traces; free tier for 1 product |
| **Uptime-Kuma** | Self-hosted uptime monitoring; simple, MIT licensed |
| **n8n** | Alert routing: monitoring events → Founder Dashboard → you |
| **Hetzner / OVH** | Recommended VPS providers (cheap, EU-based); start with 1 small node |

---

## 6. Quality gates

| Gate | Trigger | Pass criteria | Fail action |
|---|---|---|---|
| **Ship gate (`/ship`)** | After security clearance, before production deploy | Build passes all tests; no pending critical security issues; Docker image is signed (Sigstore); env vars are set | Block deploy; investigate |
| **Canary (`/canary`)** | Immediately after production deploy (first 15 minutes) | Error rate ≤ baseline; P99 latency ≤ threshold; key user path returns 2xx | **Auto-rollback** (Coolify) + notify you |
| **Scaling decision (you)** | Cost optimizer flags a tier change (e.g., single VPS → 2 VPS → k3s) | You review the cost/reliability trade-off and approve the change | Hold on current tier |

---

## 7. The scaling tiers (blueprint Part 10, operational)

| Tier | Trigger | Hosting | DB | Monthly $ |
|---|---|---|---|---|
| **MVP** | Launch → 1k users | 1 small VPS + Coolify; Vercel free for static | Supabase free | ~$0–10 |
| **Growth** | 1k–50k users | 1–2 VPS + Coolify + Cloudflare | Supabase Pro / managed PG | ~$50–200 |
| **Scale** | 50k–500k users | k3s cluster (Hetzner/OVH) + Cloudflare WAF | PG + read replicas + Redis | ~$300–1.5k |
| **Million-user** | 1M+ | Multi-node k8s + CDN + queue (NATS) | Sharded PG + cache tiers | $2k+ |

> **Rule: do not pre-build the next tier.** Only upgrade when the *current* tier is demonstrably the
> bottleneck (CPU/RAM consistently > 80%, latency increasing, errors under load). Write the upgrade as a
> Decision Record in `brain/decisions/`.

---

## 8. Model routing

| Task | Default tier | Notes |
|---|---|---|
| IaC / Docker config authoring | Cheap (DeepSeek / Qwen) | Mechanical; reviewed at gate |
| `/ship` + `/canary` gates | **Premium (Claude)** | Gate exception |
| Monitoring alert triage | Free (Groq) | Short classification output |
| Scaling analysis | Cheap (DeepSeek) | Data-driven; not judgment-critical |

---

## 9. Memory

| Read | Write |
|---|---|
| `brain/decisions/` — prior infra choices, scaling decisions | `brain/decisions/` — new infra ADRs |
| `brain/playbooks/` — deploy procedure, rollback procedure | `brain/playbooks/` — updates from incident post-mortems |
| `brain/retros/` — past incidents and their causes | `brain/retros/` — incident post-mortems |

---

## 10. Escalation triggers

Infrastructure alerts to you when:

- **Any downtime** (Uptime-Kuma fires a 5-minute consecutive failure alert).
- Error rate or latency spikes **≥ 2× baseline** for more than 5 minutes.
- A canary health check **fails** — you decide whether to roll back or hold.
- Monthly infra spend **exceeds budget** or is trending to do so.
- A tier upgrade decision is needed (requires your approval before execution).
- A Supabase backup or Coolify volume backup has failed (data risk).

---

## 11. Playbooks

### PLAY-I1: Deploy a new release

```
1. Trigger: engineer marks PR as "ready to deploy" after /review + /qa + /cso pass.
2. Run gstack /ship: build Docker image, tag it, run final test suite, push to registry.
3. Coolify: trigger a rolling deploy to the VPS (zero-downtime if set up correctly).
4. Run gstack /canary: check error rate, latency, and the 3 key user paths for 15 minutes.
5. If canary is green: merge to main; announce in Founder Dashboard.
6. If canary is red: Coolify rollback to the previous image. Notify you. Investigate.
```

### PLAY-I2: Add a new service

```
1. Write a Dockerfile and a Coolify service definition (or a k3s manifest at Scale tier).
2. Define env vars in .env.example (never hardcode); add them to the secrets vault.
3. Run Trivy against the image: zero critical findings before deploy.
4. Test in a local Docker Compose environment first.
5. /ship gate.
6. Wire Prometheus metrics and a Sentry DSN before marking the service production-ready.
7. Write a Decision Record: why this service, what it does, who owns it.
```

### PLAY-I3: Respond to a downtime incident

```
1. Uptime-Kuma fires → n8n notifies you immediately (Founder Dashboard + push).
2. Check Grafana: which service? CPU/mem/network? Database? External dependency?
3. If Coolify auto-rollback already ran: check if the previous version is healthy.
4. If no auto-rollback: manually rollback in Coolify to last known-good image.
5. If DB issue: check Supabase dashboard; restore from PITR if needed (you authorize).
6. Once stable: write a post-mortem → brain/retros/incident-<date>.md.
7. Update the affected playbook; file a Task Contract to [[04-engineering]] for the root cause fix.
```

---

## 12. KPIs / signals

| Signal | What it means | Bad state |
|---|---|---|
| Uptime | % availability over 30 days | < 99.5% = reliability issue |
| Deploy frequency | Deployments per week | < 1/week = flow is blocked |
| Mean time to recovery (MTTR) | Time from incident to resolution | > 1 hour = runbook is not practiced |
| Error rate (production) | % of requests returning 5xx | > 0.1% = engineering or infra issue |
| P99 latency | 99th percentile response time | Trending up = capacity or query issue |
| Monthly infra spend | $ vs. budget | > 110% of budget = alert; investigate |
| Backup success rate | % of scheduled backups succeeding | < 100% = data risk |
