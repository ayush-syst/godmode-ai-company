# 09 — Cybersecurity Division

> **Mission.** Make the system a hard target, keep it observable, and respond fast when something goes
> wrong. Blueprint source: Parts 3, 9. The goal is **hard target + observable + fast recovery** — not
> "unhackable," which doesn't exist. **Layer: 1 (CSO gate) + 2 (automated scanners).**
> Powered by: **gstack `/cso` for the judgment gate; Semgrep, Trivy, gitleaks, CodeQL, OWASP ZAP,
> Syft/Grype for automated scanning.** Security is woven into every stage of the Product Factory — it is
> not a one-time audit.

---

## 1. Roles

| Role | One-line job |
|---|---|
| **CSO (Chief Security Officer)** | Own the threat model, make the pre-ship security call, own incident response |
| **SAST Scanner** | Static analysis of every code change on every PR |
| **DAST Scanner** | Dynamic analysis of the running application before each ship |
| **Dependency Auditor** | Track and alert on vulnerable or outdated dependencies |
| **Infra Security Agent** | Scan container images, IaC configs, and cloud settings |
| **Supply Chain Auditor** | Produce and verify the SBOM; check for typosquatting and tampered packages |
| **Secrets Detective** | Scan every commit for accidentally committed secrets |

---

## 2. Layer mapping

| Role | Layer | Implementation |
|---|---|---|
| **CSO gate (`/cso`)** | **1 (gate)** | gstack `/cso` — OWASP/STRIDE reasoning on Claude; you trigger before every ship |
| SAST Scanner | **2 (CI, automated)** | Semgrep + CodeQL in GitHub Actions / CI pipeline |
| DAST Scanner | **2 (automated)** | OWASP ZAP (can be driven by gstack `/cso`); run against staging |
| Dependency Auditor | **2 (automated)** | Dependabot / Renovate (auto PRs) + Grype |
| Infra Security Agent | **2 (automated)** | Trivy (containers + IaC) in CI |
| Supply Chain Auditor | **2 (automated)** | Syft (SBOM generation) + Grype (vuln scan against SBOM) |
| Secrets Detective | **2 (pre-commit + CI)** | gitleaks (pre-commit hook + CI) |

---

## 3. Inputs

| From | What |
|---|---|
| [[04-engineering]] | Every PR, every Docker image build, every IaC change |
| [[10-infrastructure]] | Cloud config changes, new environment variables |
| [[01-executive]] | Strategic risk questions (e.g., "is using OpenClaw safe?") |
| External | CVE feeds, security advisories (Dependabot/Renovate surface these) |

---

## 4. Outputs

| To | What | Written where |
|---|---|---|
| [[04-engineering]] | SAST/DAST findings with remediation guidance | PR comments + `tasks/<id>/security-findings.md` |
| [[01-executive]] | Pre-ship security clearance ("pass") or a block with specific findings | Gate verdict in `brain/decisions/` |
| [[10-infrastructure]] | Infra hardening recommendations | `tasks/<id>/infra-security.md` |
| [[12-company-brain]] | Incident post-mortems, security decisions, threat model | `brain/decisions/` + `brain/retros/` |

---

## 5. Tools

| Tool | Purpose | Where it runs |
|---|---|---|
| **gstack `/cso`** | OWASP/STRIDE threat-model reasoning; CSO gate | You trigger, runs on Claude |
| **Semgrep** | SAST: language-aware pattern matching; catches OWASP Top 10 | CI on every PR |
| **CodeQL** (GitHub) | Deep SAST: data-flow analysis; free on public repos | GitHub Actions |
| **gitleaks** | Secret scanning: API keys, tokens in commits/history | Pre-commit hook + CI |
| **Trivy** (`aquasecurity/trivy`) | Container image + IaC scanning | CI on every Docker build |
| **OWASP ZAP** | DAST: crawl and attack the running app | Staging environment, pre-ship |
| **Dependabot / Renovate** | Auto-PR for vulnerable/outdated deps | GitHub (Dependabot) or self-hosted (Renovate) |
| **Syft** (`anchore/syft`) | Generate SBOM for every release | CI on every deploy |
| **Grype** (`anchore/grype`) | Vuln scan against the SBOM | CI, paired with Syft |
| **Sigstore / cosign** | Sign container images for supply chain verification | CI deploy step |
| **Infisical / Doppler** | Secrets vault (alternative to raw .env) | Self-hostable; recommended for prod |

---

## 6. Quality gates

| Gate | Trigger | Pass criteria | Fail action |
|---|---|---|---|
| **CSO gate (`/cso`)** | Before every production deploy, every new external-facing feature | Zero critical/high SAST findings; STRIDE threats have mitigations; no secrets in code; DAST shows no critical vulns | **Block deploy**; file remediation Task Contracts to [[04-engineering]] |
| **Pre-commit (gitleaks)** | Every `git commit` | No secrets detected | Commit blocked; remove the secret; rotate the key |
| **CI security scan** | Every PR | Semgrep + Trivy: zero critical/high findings | PR blocked from merge |
| **Dependency audit** | Dependabot/Renovate PR | Vuln is patched; test suite still passes | Review the patch; if no patch exists, document the risk and mitigate |
| **SBOM verification** | Every release | SBOM is generated and stored; no unknown packages | Investigate the unknown; update or remove it |

> **The hard rule:** a critical or high security finding **blocks the ship gate absolutely**. There is no
> "we'll fix it next sprint" for severity critical. The `/cso` gate and the CI pipeline enforce this without
> negotiation.

---

## 7. Model routing

| Task | Default tier | Notes |
|---|---|---|
| `/cso` STRIDE + OWASP reasoning | **Premium (Claude)** | Gate exception — security judgment cannot be downgraded |
| SAST/DAST scan triage (reading reports) | Cheap (DeepSeek) | Structured scan output → explanation draft |
| Dependency risk assessment | Free (Gemini Flash) | Pattern match across CVEs |
| Incident response drafting | **Premium (Claude)** | High stakes; needs precise language |

Automated scanners (Semgrep, Trivy, gitleaks, CodeQL, ZAP) are not LLM calls — they run as
deterministic tools. LLMs are only used to *reason about* findings, not to detect them.

---

## 8. Memory

| Read | Write |
|---|---|
| `brain/decisions/` — prior threat model, security choices | `brain/decisions/` — security decisions, risk-accepts |
| `brain/specs/` — what's being built (for threat modeling) | `brain/retros/` — incident post-mortems |
| Known vulnerabilities list (`brain/security/known-issues.md`) | `brain/security/` — threat model, SBOM archive, incident log |

---

## 9. Escalation triggers (all go to you immediately)

- Any **data breach or confirmed unauthorized access** to any system, account, or database.
- A **critical CVE** in a dependency that has no patch yet and affects production.
- A **secret leaked** to git history (even if caught by gitleaks — rotate the key first, then escalate).
- An agent (especially any Layer-2 autonomous agent) exhibiting unexpected behavior that suggests a
  **prompt injection** or **tool abuse** attempt.
- A **production incident** with potential security implications (vs. a plain bug).
- Any security finding that would require **shipping without fixing** to meet a deadline — that decision
  is yours alone; it may never be made by an agent.

---

## 10. Playbooks

### PLAY-SEC1: Pre-ship security check (standard)

```
1. PR passes /review and /qa.
2. CI automatically runs: Semgrep + CodeQL + Trivy + gitleaks + Syft → report in PR.
3. If CI is clean (no critical/high): proceed to step 4.
   If CI has findings: [[04-engineering]] files remediation Task Contracts; repeat.
4. Run OWASP ZAP against staging: spider + active scan.
5. You trigger gstack /cso with: the PR diff + the ZAP report + the SBOM.
6. /cso produces: STRIDE threat model pass/fail, any additional findings, clearance statement.
7. If pass: document clearance in brain/decisions/ (gate record). Proceed to /ship.
8. If fail: block. Specific findings → Task Contracts to [[04-engineering]]. Repeat cycle.
```

### PLAY-SEC2: New dependency assessment

```
1. Before adding any new dependency (library, SDK, API):
2. Check: stars, last commit date, known maintainer, license.
3. Run Grype against it (if a package).
4. Check OpenSSF scorecard (security health of the project).
5. For high-sensitivity deps (auth, crypto, payments): run /cso reasoning: "what's the blast radius if this library is compromised?"
6. Decision Record: why we added it, what we checked, what we accept.
```

### PLAY-SEC3: Security incident response

```
1. Detection: alert from Sentry / Cloudflare WAF / user report / your own discovery.
2. STOP and CONTAIN: if active breach — revoke credentials, take affected service offline if needed. Speed over elegance.
3. Assess: what was accessed? what was exfiltrated? what is the blast radius?
4. Notify: if user data is involved, legal obligation to notify users (India DPDP Act) — this is YOUR call, not an agent's.
5. Fix: [[04-engineering]] fast-tracks the patch under your direct supervision.
6. Post-mortem: honest write-up → brain/retros/incident-<date>.md. What happened, how it was missed, what changes.
7. Update: the threat model, the CI pipeline, the playbook.
```

---

## 11. KPIs / signals

| Signal | What it means | Bad state |
|---|---|---|
| CI security scan pass rate | % of PRs passing CI security gates on first attempt | < 80% = engineering is shipping insecure code regularly |
| Mean time to patch (MTTP) | Days from CVE alert to patch deployed | > 14 days for critical = dangerous lag |
| Secret leak incidents | # of times gitleaks catches a secret | > 0 = pre-commit hook is not installed everywhere |
| `/cso` block rate | % of pre-ship /cso runs that block the deploy | > 20% = security is being left to the last gate |
| Dependency freshness | % of deps within 2 major versions of current | < 70% = Dependabot is ignored |
| SBOM coverage | % of releases with a stored SBOM | < 100% = supply chain is blind |
