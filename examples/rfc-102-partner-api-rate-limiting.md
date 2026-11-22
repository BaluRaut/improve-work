# RFC: Rate limiting for the partner API

> Example RFC for **Acme Retail** (fictional). A backend and infrastructure change with no UI, so frontend, translations and product analytics are left out.

| Field | Value |
|---|---|
| RFC ID | RFC-102 |
| Title | Rate limiting for the partner API |
| Feature owner | Karthik Subramanian, Platform team |
| Reviewers | Engineering lead, SRE, Security, Partner Success |
| Status | In review |
| Created | 2026-10-13 |
| Last updated | 2026-10-21 |
| Target release | 2026-11-17 (enforcement) |
| Links | Incident: INC-2291 · Ticket: PLAT-640 |
| Sections not included | 5 Users: partners only, covered in 2 and 3 · 7 Frontend: no UI · 12 Event tracking: no product analytics; usage is in Datadog metrics (14) · 13 Translations: API errors stay in English, as documented · 20 Alternatives: covered briefly in 3 · 23 Timeline: single sprint · 24 Launch checklist: covered by the rollout gates in 17 |

---

## 1. Summary

Add per-API-key rate limits to the partner API, so one misbehaving partner cannot slow the API for everyone. Requests over the limit get `429 Too Many Requests` with clear headers telling the partner when to retry. Limits roll out in shadow mode first, then are enforced after partners are notified.

## 2. Background and problem

- 140 partners (marketplaces and B2B buyers) call `/v2/catalog` and `/v2/orders`.
- On 2026-10-02, two partners' sync scripts sent bursts of about 2,500 requests per second. p95 latency for all partners rose from 180 ms to 2.1 s for 23 minutes (INC-2291), and 4% of orders from other partners failed.
- There is no limit today besides Cloudflare's per-IP DDoS protection, which does not help when traffic comes from a few legitimate IPs.

## 3. Goals and non-goals

**Goals**

- Limits per API key, using a token bucket: steady rate plus a short burst.
- Two tiers: Standard 50 requests/s, burst 100; Premium 200 requests/s, burst 400.
- Standard response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`.
- Added latency at most 2 ms p99.

**Non-goals**

- Per-IP or DDoS protection (Cloudflare WAF already does this).
- Usage-based billing.
- Limits on the customer apps' private API.

Alternatives briefly: a fixed-window counter was rejected because it allows double bursts at window edges; limiting in Cloudflare was rejected because it cannot see API keys without a paid add-on.

## 4. Success metrics

| Metric | Baseline | Target | Measured by | Review date |
|---|---|---|---|---|
| Incidents caused by a single partner's traffic | 3 in last quarter | 0 per quarter | Incident tracker | End of Q1 2027 |
| Partner API p95 latency during bursts | up to 2.1 s | under 300 ms | Datadog APM | 4 weeks after enforcement |

**Guardrail metrics:** legitimate partners should almost never hit the limit; 429s under 1% of all partner requests.

## 6. Proposed solution

### 6.1 Overview

```text
Partner ─▶ Cloudflare ─▶ api-gateway ──▶ rate-limit middleware ──(Lua token bucket, 1 round trip)──▶ Redis
                                    │                │
                                    │                ├─ allowed  ─▶ catalog / orders services
                                    │                └─ limited  ─▶ 429 + Retry-After
```

A middleware in `api-gateway` runs an atomic Lua script in Redis keyed by `rl:{api_key_id}`. The script refills tokens based on elapsed time and takes one token per request. If Redis is unavailable, the middleware fails open: it lets the request through and records a metric, because blocking all partners is worse than a temporary lack of limits.

### 6.2 Modes

- `off`: middleware does nothing.
- `shadow`: computes the decision and logs would-be 429s, but never blocks.
- `enforce`: returns 429 when over the limit.

## 8. Backend changes

### 8.1 Services and business logic

New middleware in `api-gateway`. The tier comes from the partner record, cached in memory for 60 seconds. Health-check and auth endpoints are exempt.

### 8.2 API changes

| Method | Path / operation | Auth | Request | Response | Errors | New / Changed / Breaking |
|---|---|---|---|---|---|---|
| All | /v2/* | Partner API key | unchanged | Adds `X-RateLimit-Limit`, `X-RateLimit-Remaining` headers | New 429 with `Retry-After` and body `{ "error": "rate_limited", "retry_after_seconds": 2 }` | Changed; 429 is new behaviour for partners |

**Backward compatibility:** 429 is a standard status most HTTP clients already retry. Partners get 2 weeks' notice and the shadow-mode report of how often they would have been limited.

## 9. Data model and migrations

| Table / collection | Change | Migration type | Backfill needed | Reversible |
|---|---|---|---|---|
| partners | Add `rate_tier varchar(16) not null default 'standard'` | Online; default is a constant, so no table rewrite | No; 12 premium partners updated by script | Yes |

## 10. Infrastructure changes

| Change | Environments | IaC location / PR | Owner | Monthly cost | Reversible |
|---|---|---|---|---|---|
| ElastiCache Redis 7, `cache.r7g.large`, primary plus one replica, Multi-AZ | staging, prod | terraform/modules/redis-ratelimit, PR #2231 | Karthik S. | about $260 (prod) | Yes |
| Security group: allow api-gateway pods to Redis port 6379 only | staging, prod | same PR | Karthik S. | — | Yes |

**Configuration, environment variables and secrets**

| Name | Purpose | Environments | Stored in | Default | Rotation |
|---|---|---|---|---|---|
| RATE_LIMIT_MODE | off / shadow / enforce | all | Config service | off | n/a |
| RATE_LIMIT_REDIS_URL | Redis endpoint with auth token | staging, prod | AWS Secrets Manager | — | 90 days |

**Capacity and scaling:** peak partner traffic is about 1,800 requests/s; one Redis call each is well within a single `r7g.large` node (over 100,000 operations/s).

## 11. Security, privacy and compliance

| Topic | Answer |
|---|---|
| Authentication and authorization | Unchanged; limits are keyed by the authenticated API key id, never by the raw key |
| Personal data | None stored; Redis holds counters only, with a 10-minute expiry |
| Abuse | Limits stop one key from exhausting shared capacity; Cloudflare still handles network floods |
| Secrets handling | Redis auth token in Secrets Manager; TLS in transit |

## 14. Observability and monitoring

### 14.1 Logs, metrics and traces

| Signal | What we add | Where |
|---|---|---|
| Metrics | `ratelimit.decision` counter tagged `partner_id`, `tier`, `result:allowed/limited/fail_open`, `mode` | Datadog |
| Logs | One structured log per limited request (sampled at 10%) with partner id and route | Datadog Logs |
| Traces | Span `ratelimit.check` inside the gateway request | Datadog APM |

### 14.3 Datadog monitors

| Monitor name | Type | Query / metric | Warn | Critical | Window | Priority | Notify | Runbook |
|---|---|---|---|---|---|---|---|---|
| [platform] rate limiter failing open | Metric | sum:ratelimit.decision{result:fail_open} | above 0 | above 100 | 5 min | P2 | @slack-platform-alerts | runbooks/platform/ratelimit-fail-open |
| [platform] ratelimit Redis latency | Metric | p99 ratelimit.check duration | over 3 ms | over 10 ms | 10 min | P3 | @slack-platform-alerts | runbooks/platform/redis-latency |
| [platform] partner heavily limited | Metric | limited / total by partner_id | over 10% | over 30% | 15 min | P4 | @slack-partner-success | runbooks/platform/partner-limited |
| [platform] partner API p95 latency | APM | p95 trace.http.request.duration, service:api-gateway | over 300 ms | over 800 ms | 10 min | P2 | @pagerduty-platform | runbooks/platform/gateway-latency |

- **Dashboard:** "Partner API · Rate limits": decisions by partner, top limited partners, Redis health.

## 15. Performance and scalability

| Item | Expectation |
|---|---|
| Added latency | One Redis round trip, under 1 ms p50 and 2 ms p99 inside the VPC |
| Load test | k6 at 3,000 requests/s across 50 keys in staging; pass if p99 overhead ≤ 2 ms and limits are exact within 5% |

## 16. Testing strategy

| Level | Scope | Owner | Automated |
|---|---|---|---|
| Unit | Token refill maths, headers, exempt routes | Karthik | Yes |
| Integration | Lua script against real Redis; fail-open when Redis is stopped | Karthik | Yes |
| Load | k6 scenario above | SRE | Yes |

## 17. Rollout plan

| Phase | Audience | Setting | Duration | Go / no-go criteria |
|---|---|---|---|---|
| 0 | Staging | enforce | 3 days | Load test passed |
| 1 | Production | shadow | 1 week | Report of would-be 429s per partner sent to Partner Success |
| 2 | Production | enforce at 3× the final limits | 1 week | Under 0.1% of requests limited; no partner escalations |
| 3 | Production | enforce at final limits | — | Under 1% limited |

- **Kill switch:** set `RATE_LIMIT_MODE=off` in the config service; takes effect within 30 seconds, no deploy.
- **Communication:** email and developer-portal notice to all partners 2 weeks before phase 2, including the shadow report for their key.

## 18. Rollback plan

| Step | How to roll back | Data impact | Time needed |
|---|---|---|---|
| Enforcement | `RATE_LIMIT_MODE=shadow` or `off` | None | 30 s |
| Middleware | Redeploy previous gateway version | None | 10 min |
| Redis cluster | Keep until the feature is stable; delete with Terraform later | Counters only | — |

## 19. Dependencies and impact on other teams

| Team / system | What we need or what changes for them | Contact | Status |
|---|---|---|---|
| Partner Success | Send notices and shadow reports; field partner questions | Lakshmi | Agreed |
| Developer portal | Document limits, headers and retry guidance | Docs team | Pending |

## 21. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| A large partner's normal sync exceeds Standard | Medium | High | Shadow week identifies them; move to Premium before enforcement | Lakshmi |
| Redis outage | Low | Medium | Fail open, alert, Multi-AZ replica | Karthik |
| Clock or refill bug limits everyone | Low | High | Shadow mode first; kill switch in 30 s | Karthik |

## 22. Open questions

| Question | Owner | Due | Answer |
|---|---|---|---|
| Separate, stricter limit for `/v2/orders` writes? | Product | 2026-10-28 | Open |

## 25. Approvals

| Role | Name | Decision | Date |
|---|---|---|---|
| Engineering lead | Vikram Rao | Approve | 2026-10-21 |
| SRE | Tejas P. | Approve | 2026-10-21 |
| Security | Farah A. | Approve | 2026-10-20 |
| Partner Success | Lakshmi V. | Pending | |
