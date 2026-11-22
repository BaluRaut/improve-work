# RFC: {Feature name}

> **How to use this template.** Copy this file to `rfc-{number}-{short-name}.md` and fill it in, deleting the guidance lines (the quoted text) as you go. Placeholders look like `{this}`; replace each one.
>
> **Start with a Feature Request Brief.** Business requestors should describe the problem and desired outcome in `intake/FEATURE_REQUEST_TEMPLATE.md`; they do not need to design the technical solution. Product and Engineering then refine the request and prepare this RFC. Use `guides/WORKFLOW.md` to follow the request-to-delivery stages. The Jira and Rovo steps apply if your team uses them; the rest works with any tracker.
>
> **Include only the sections your change needs.** Sections 1, 2, 3, 6, 17, 18, 21 and 25 are required in every RFC. Remove any other section that does not apply, keep the original section numbers for the rest, and list what you removed in the "Sections not included" row below with a one-line reason each. That way reviewers know an omission was deliberate. See `examples/` for five RFCs that each use a different subset.

**When to include each section**

| Section | Include when the change… |
|---|---|
| 4 Success metrics | is meant to move a product, business or reliability number; record actual results after release |
| 5 Users, requirements and use cases | changes what users see or do; 5.2 when users or systems need specific, testable behaviour |
| 7 Frontend | touches web or mobile UI |
| 8 Backend | adds or changes services, APIs, jobs or integrations |
| 9 Data model | changes schemas, migrations, retention or stored personal data |
| 10 Infrastructure | adds or changes cloud resources, config, secrets, scaling or cost |
| 11 Security and privacy | touches auth, personal data, money, external input or permissions |
| 12 Event tracking | adds or changes analytics events, funnels or dashboards |
| 13 Translations | adds or changes any user-facing text |
| 14 Observability | adds or changes anything that runs in production and can fail |
| 15 Performance | can change latency, throughput, load or bundle size |
| 16 Testing | always recommended; keep it short for small changes |
| 19 Dependencies | another team, vendor, system or decision affects delivery |
| 20 Alternatives | there was a real choice between approaches |
| 22 Questions, assumptions and decisions | there are open questions, or meaningful options and decisions need traceability |
| 23 Milestones and delivery plan | the work spans more than one milestone or team; detail lives in the Delivery Plan |
| 24 Launch checklist | recommended for user-facing changes |

| Field | Value |
|---|---|
| Feature ID | FEAT-{number} |
| RFC ID | RFC-{number} |
| Title | {Feature name} |
| Requestor | {Name, role, team} |
| Business sponsor / decision owner | {Name, role} |
| Product owner | {Name, team} |
| Feature owner | {Engineering owner, team} |
| Other authors | {Names} |
| Impacted teams | {Teams} |
| Complexity | Lite / Standard / Full |
| Reviewers | {Select by impact; see guides/REVIEW_AND_APPROVAL.md} |
| Status | Draft / In review / Approved / Rejected / Superseded by RFC-{n} |
| Created | {YYYY-MM-DD} |
| Last updated | {YYYY-MM-DD} |
| Target release | {Version or date} |
| Links | Intake brief: {link} · Delivery plan: {link} · Jira Epic: {link} · Designs: {link} · Prior RFCs: {link} |
| Sections not included | {e.g. 7 Frontend: no UI change; 13 Translations: no user-facing text} |

---

## 1. Summary

> Three to five sentences. What are we building, for whom, and why now? A reader who stops here should understand the change.

{Summary}

## 2. Background and problem

> The current situation, the user or business pain, and evidence (data, support tickets, user research). Link to sources.

{Background}

## 3. Goals and non-goals

**Goals**

- {Goal 1}
- {Goal 2}

**Non-goals** (explicitly out of scope for this RFC)

- {Non-goal 1}
- {Non-goal 2}

## 4. Success metrics

> How we will know it worked. Every metric needs a baseline, a target and a source. The events that feed these metrics belong in section 12.

| Metric | Baseline | Target | Measured by | Review date |
|---|---|---|---|---|
| {e.g. Checkout conversion} | {3.1%} | {3.6%} | {Amplitude funnel "checkout_v2"} | {4 weeks after 100% rollout} |
| {e.g. p95 page load} | {2.4 s} | {≤ 1.8 s} | {Datadog RUM} | {2 weeks after launch} |

**Guardrail metrics** (must not get worse): {e.g. error rate, refund rate, support tickets}

### 4.1 Post-release outcome review

> Complete this after the agreed review window. Record actual results, explain material gaps and assign follow-up actions. Do not mark a metric as achieved without a measured result.

| Metric | Baseline | Target | Actual | Result / explanation | Data source | Reviewed on |
|---|---|---|---|---|---|---|
| {Metric} | {Value} | {Value} | {Value / Not yet measured} | {Achieved / Partial / Not achieved; context} | {Dashboard / report} | {Date} |

**Outcome owner:** {Name, role}

**Follow-up actions:** {Action, owner, due date, or none}

## 5. Users, requirements and use cases

### 5.1 Users and use cases

> Who uses this and what they are trying to do. Include important scenarios and edge cases (new users, power users, low bandwidth, accessibility needs).

- As a {user type}, I want {action} so that {outcome}.
- As a {user type}, I want {action} so that {outcome}.

### 5.2 Functional requirements and acceptance criteria

> Give each requirement a stable ID. Acceptance criteria must describe observable behaviour and be testable by Product, Engineering and QA. Use Given / When / Then where it helps. Link to detailed designs or test cases rather than duplicating them.

| ID | Requirement / expected behaviour | Priority | Acceptance criteria | Owner / source |
|---|---|---|---|---|
| FR-01 | {Requirement} | Must / Should / Could | Given {context}, when {action}, then {result} | {Product / source} |
| FR-02 | {Requirement} | Must / Should / Could | Given {edge case}, when {action}, then {result} | {Product / source} |

**Out of scope:** {Explicitly excluded behaviour; align with section 3}

**Requirement notes:** {Business rules, permissions, validations, empty/loading/error states, boundary conditions, audit needs}

## 6. Proposed solution

### 6.1 Overview

> The approach in plain words, then a diagram. Show the main components and the data flow between them.

{Overview}

```text
{Architecture or sequence diagram, or a link to one (Excalidraw, Mermaid, draw.io)}
```

### 6.2 User flow

> Step-by-step flow, including empty, loading, error and permission-denied states. Link the designs.

1. {Step}
2. {Step}

## 7. Frontend changes

> Web and/or mobile. Name the screens and components touched, how state is managed, and how the feature is switched on.

| Area | Change | Notes |
|---|---|---|
| Screens / routes | {New or changed pages} | {Deep links, SEO, redirects} |
| Components | {New or changed components} | {Design-system components reused or added} |
| State and data fetching | {Store, cache, query keys} | {Invalidation, optimistic updates} |
| Feature flag | {Flag name} | {Default off; targeting rules} |
| Accessibility | {Keyboard, screen reader, contrast, focus management} | {WCAG 2.2 AA target} |
| Responsive / devices | {Breakpoints, mobile, tablet, low-end Android} | |
| Offline / poor network | {Behaviour} | |
| Bundle size impact | {+ n KB} | {Code-split? Lazy-loaded?} |

## 8. Backend changes

### 8.1 Services and business logic

> Which services change, what new logic is added, and where it lives.

{Description}

### 8.2 API changes

> One row per endpoint (REST, GraphQL, gRPC or events). Mark breaking changes clearly and describe versioning.

| Method | Path / operation | Auth | Request | Response | Errors | New / Changed / Breaking |
|---|---|---|---|---|---|---|
| {POST} | {/v1/orders} | {User token, scope `orders:write`} | {Body schema link} | {201 + schema link} | {400, 401, 403, 409, 429} | {New} |

**Backward compatibility:** {How old clients keep working; deprecation timeline}

**Idempotency, pagination, rate limits:** {Details}

### 8.3 Background jobs, queues and scheduled tasks

| Job / consumer | Trigger or schedule | Queue / topic | Retries and dead-letter | Expected volume |
|---|---|---|---|---|
| {Name} | {Event or cron} | {Topic} | {3 retries, exponential backoff, DLQ `x-dlq`} | {n per minute} |

### 8.4 Third-party integrations

| Provider | Purpose | Auth / keys | Limits and cost | Failure behaviour |
|---|---|---|---|---|
| {Provider} | {Purpose} | {Where the secret lives} | {Rate limit, price} | {Timeout, fallback} |

## 9. Data model and migrations

> Schema changes, how existing data is moved, and how long data is kept. Migrations must be safe to run while the old code is still serving traffic.

| Table / collection | Change | Migration type | Backfill needed | Reversible |
|---|---|---|---|---|
| {orders} | {Add column `channel` (nullable)} | {Online, expand then contract} | {Yes, batched job} | {Yes} |

- **Migration order:** {expand schema → deploy code that writes both → backfill → switch reads → contract}
- **Data volume and duration:** {rows, estimated run time, locking risk}
- **Retention and deletion:** {how long data is kept; deletion on user request}
- **Personal data fields:** {list fields that are PII; see section 11}

## 10. Infrastructure changes

> Everything that changes outside application code. Each change should be made through infrastructure-as-code and reviewed by SRE/Platform. Include cost.

| Change | Environments | IaC location / PR | Owner | Monthly cost | Reversible |
|---|---|---|---|---|---|
| {New queue `orders-events`} | {dev, staging, prod} | {terraform/modules/queues, PR #} | {Name} | {$x} | {Yes} |
| {Scale API from 4 to 6 pods} | {prod} | {helm/values-prod.yaml} | {Name} | {$x} | {Yes} |
| {New S3 bucket / CDN path / DNS record} | | | | | |

**Configuration, environment variables and secrets**

| Name | Purpose | Environments | Stored in | Default | Rotation |
|---|---|---|---|---|---|
| {ORDERS_V2_ENABLED} | {Feature switch} | {all} | {Config service} | {false} | {n/a} |
| {PAYMENT_API_KEY} | {Provider auth} | {staging, prod} | {Vault / Secrets Manager} | {none} | {90 days} |

**Capacity and scaling:** {expected load, autoscaling rules, limits, quotas to raise}

**Network and access:** {security groups, firewall rules, IAM roles, service-to-service permissions}

**Disaster recovery:** {backups, restore time, multi-region impact}

## 11. Security, privacy and compliance

| Topic | Answer |
|---|---|
| Authentication and authorization | {Who can call what; role and permission checks} |
| Personal data collected or exposed | {Fields, purpose, legal basis, consent} |
| Data protection laws | {DPDP Act (India), GDPR, children's data, data residency} |
| Input validation and output encoding | {Where and how} |
| Abuse and rate limiting | {Limits, bot protection} |
| Secrets handling | {No secrets in code or logs; storage location} |
| Audit logging | {What is logged, who can read it} |
| Threat model | {Main risks: e.g. IDOR, injection, replay; mitigations} |
| Security review needed | {Yes / No; reviewer} |

## 12. Event tracking and analytics

> Every event that feeds a success metric or dashboard. Use one naming convention, for example `object_action` in snake_case (`order_placed`, `filter_applied`). Never send personal data such as names, emails, phone numbers or free text in event properties.

| Event name | Trigger (exactly when it fires) | Properties (name: type, example) | Platforms | Tool | New / Changed | Owner |
|---|---|---|---|---|---|---|
| {order_placed} | {Server confirms the order} | {order_id: string, value: number 499, currency: "INR", items: int 3} | {Server} | {Amplitude} | {New} | {Name} |
| {filter_applied} | {User taps Apply in the filter sheet} | {filter: string "price", count: int 2} | {Web, iOS, Android} | {Amplitude} | {New} | {Name} |

- **User and session identity:** {how users are identified; anonymous vs logged in}
- **Consent and opt-out:** {how tracking respects consent, Do Not Track, children}
- **Dashboards and funnels to create or update:** {links}
- **QA of events:** {how events are verified before launch, e.g. debug view, test plan}
- **Removed or renamed events:** {list, and which dashboards they break}

## 13. Translations and localization

> All user-facing text, including errors, emails, push notifications and app-store copy. No hard-coded strings.

| Key | Default text (en) | Context for translators | Max length | Languages | Status |
|---|---|---|---|---|---|
| {checkout.button.place_order} | {Place order} | {Primary button on the payment screen} | {20} | {hi, mr, ta, …} | {Sent / Done} |

- **Languages in scope:** {list}; **fallback language:** {en}
- **Formatting:** dates, times, numbers, currency and plurals use locale-aware formatters
- **Layout:** long strings and different scripts (e.g. Devanagari) tested; right-to-left support if needed
- **Translation workflow and owner:** {tool (e.g. Lokalise, Crowdin), who translates, who reviews, deadline}
- **Testing:** {pseudo-locale run, screenshots per language}

## 14. Observability and monitoring

### 14.1 Logs, metrics and traces

| Signal | What we add | Where |
|---|---|---|
| Logs | {Structured logs for order creation, with request_id; no PII} | {Datadog Logs, index `orders`} |
| Metrics | {orders.created.count, orders.payment.latency} | {Datadog / StatsD} |
| Traces | {APM spans for checkout service and payment client} | {Datadog APM} |
| Frontend | {RUM views and errors for /checkout} | {Datadog RUM} |

### 14.2 Service level objectives

| SLI | SLO target | Window | Error budget policy |
|---|---|---|---|
| {Availability of POST /v1/orders (non-5xx share)} | {99.9%} | {30 days} | {Freeze risky releases if budget is spent} |
| {p95 latency of POST /v1/orders} | {≤ 400 ms} | {30 days} | |

### 14.3 Datadog monitors

> Every monitor needs a runbook. Critical alerts page someone; warnings go to the team channel.

| Monitor name | Type | Query / metric | Warn | Critical | Window | Priority | Notify | Runbook |
|---|---|---|---|---|---|---|---|---|
| {[orders] 5xx error rate high} | {APM} | {trace.http.request.errors / hits, service:orders} | {> 1%} | {> 3%} | {5 min} | {P1} | {@pagerduty-orders, @slack-orders-alerts} | {link} |
| {[orders] p95 latency high} | {APM} | {p95 trace.http.request.duration, resource:POST /v1/orders} | {> 400 ms} | {> 800 ms} | {10 min} | {P2} | {@slack-orders-alerts} | {link} |
| {[orders] queue backlog} | {Metric} | {aws.sqs.approximate_number_of_messages_visible, queue:orders-events} | {> 1,000} | {> 5,000} | {10 min} | {P2} | {@slack-orders-alerts} | {link} |
| {[orders] job failures} | {Log} | {status:error service:orders-worker} | {> 10} | {> 50} | {15 min} | {P3} | {@slack-orders-alerts} | {link} |
| {[orders] checkout synthetic} | {Synthetic} | {Browser test: place a test order} | {1 failure} | {2 consecutive failures} | {every 5 min} | {P1} | {@pagerduty-orders} | {link} |

- **Dashboards:** {new or updated dashboard links}
- **On-call impact:** {which rotation owns these alerts; handover notes}
- **Monitor management:** {monitors defined as code with the Terraform Datadog provider, in path/to/monitors}

## 15. Performance and scalability

| Item | Expectation |
|---|---|
| Expected traffic | {requests per second at peak; growth} |
| Latency budget | {p50 / p95 / p99 targets per endpoint or page} |
| Caching | {What, where, TTL, invalidation} |
| Heavy queries / N+1 risks | {Indexes added, query plans checked} |
| Load or stress test plan | {Tool, target, pass criteria} |
| Frontend performance | {Core Web Vitals targets: LCP, INP, CLS} |

## 16. Testing strategy

| Level | Scope | Owner | Automated |
|---|---|---|---|
| Unit | {Business logic, components} | {Dev} | {Yes} |
| Integration / contract | {API, database, third-party mocks} | {Dev} | {Yes} |
| End-to-end | {Critical user journeys} | {QA} | {Yes} |
| Accessibility | {axe checks, screen reader pass} | {QA} | {Partly} |
| Localization | {Each language, long strings} | {QA} | {Partly} |
| Event tracking | {Events fire once with correct properties} | {Dev / Data} | {Partly} |
| Manual exploratory | {Edge cases, devices} | {QA} | {No} |

**Test data and environments:** {seed data, staging setup, test accounts}

## 17. Rollout plan

| Phase | Audience | Flag setting | Duration | Go / no-go criteria |
|---|---|---|---|---|
| 0 | Internal team | {on for staff} | {2 days} | {No P1/P2 bugs; events verified} |
| 1 | {5% of users} | {5%} | {3 days} | {Error rate and latency within SLO; guardrails flat} |
| 2 | {50%} | {50%} | {3 days} | {Success metric trending to target} |
| 3 | {100%} | {100%} | — | {Remove flag within 2 sprints} |

- **Deployment order:** {infra → migrations (expand) → backend → frontend → flag on}
- **Kill switch:** {how to turn the feature off in under 5 minutes, and who can do it}
- **Communication:** {release notes, support team briefing, customer messaging}

## 18. Rollback plan

> How we undo each step safely, including data written by the new version.

| Step | How to roll back | Data impact | Time needed |
|---|---|---|---|
| {Feature flag} | {Turn off} | {None} | {1 min} |
| {Backend deploy} | {Redeploy previous version} | {New column ignored} | {10 min} |
| {Migration} | {Contract step is delayed until stable; down-migration script} | {Describe} | {n min} |

## 19. Dependencies and impact on other teams

| Team / system | Required input or impact | Dependency owner | Needed by | Status | Blocking? |
|---|---|---|---|---|---|
| {Payments team} | {New webhook} | {Name / role} | {Date / milestone} | {Open / Agreed / In progress} | {Yes / No} |
| {Support} | {New FAQ and macros} | {Name / role} | {Date / milestone} | {Pending} | {No} |

**Cross-team coordination:** {Integration points, hand-off expectations, meeting / async review, escalation path}

**External dependencies:** {Vendor, partner, data source or platform constraints; include service owner and contingency}

## 20. Alternatives considered

| Option | Pros | Cons | Why not chosen |
|---|---|---|---|
| {Option A} | | | |
| {Do nothing} | | | |

## 21. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| {Payment provider latency spikes} | {Medium} | {High} | {Timeout 3 s, retry once, show pending state} | {Name} |

## 22. Open questions, assumptions and decisions

### 22.1 Open questions

| Question | Blocks delivery? | Owner | Due | Answer / status |
|---|---|---|---|---|
| {Question} | {Yes / No} | {Name} | {Date} | {Open / Answer} |

### 22.2 Assumptions

| Assumption | Why it is needed | Validation method | Owner | Due | Status |
|---|---|---|---|---|---|
| {Assumption} | {Reason} | {Evidence / test} | {Name} | {Date} | {Unvalidated / Validated / Rejected} |

### 22.3 Decision log

| Decision ID | Date | Decision | Options considered | Rationale / trade-off | Decision owner |
|---|---|---|---|---|---|
| DEC-01 | {Date} | {Decision} | {Options} | {Why this option} | {Name / role} |

## 23. Milestones and delivery plan

> Keep this section short. The detailed work breakdown, estimates, dependencies and Jira handoff live in the Delivery Plan (`templates/DELIVERY_PLAN_TEMPLATE.md`); link it here rather than copying it. Dates and estimates are forecasts until the owning teams confirm them in planning.

| Milestone | Scope / exit criteria | Owner | Forecast / confidence | Target date |
|---|---|---|---|---|
| Requirements and RFC approved | {Scope and decisions agreed} | {Owner} | {TBD} | {Date / TBD} |
| Technical foundations ready | {API / data / platform contracts available} | {Owner} | {TBD} | {Date / TBD} |
| Feature integrated in test environment | {Critical end-to-end flow works} | {Owner} | {TBD} | {Date / TBD} |
| QA and readiness sign-off | {Acceptance criteria and release gates pass} | {Owner} | {TBD} | {Date / TBD} |
| Rollout and outcome review | {Release complete; metrics reviewed} | {Owner} | {TBD} | {Date / TBD} |

| Delivery link | Value |
|---|---|
| Delivery Plan | {URL} |
| Jira Epic | {Key / URL, once created} |
| Work breakdown reviewed by | {Tech lead, owning teams} |

## 24. Launch checklist

**Before development starts**

- [ ] RFC reviewed and approved by all required reviewers
- [ ] Designs final, including empty, loading and error states
- [ ] Success metrics have baselines and a dashboard plan
- [ ] Infra cost estimate approved

**Before release**

- [ ] Feature flag created, default off, kill switch tested
- [ ] Migrations tested on a production-sized copy
- [ ] Infrastructure changes applied through IaC in all environments
- [ ] Secrets stored in the secret manager; none in code or logs
- [ ] Events implemented and verified in the analytics debug view
- [ ] All strings externalized and translated; each language checked on screen
- [ ] Datadog monitors, dashboards and runbooks created and linked
- [ ] SLOs defined; on-call team briefed
- [ ] Accessibility checks passed
- [ ] Security review complete (if required)
- [ ] Load test passed (if required)
- [ ] Support team and documentation updated
- [ ] Rollback plan rehearsed in staging

**After release**

- [ ] Monitors quiet and SLOs met during each rollout phase
- [ ] Success and guardrail metrics reviewed on the review date
- [ ] Feature flag and dead code removed
- [ ] RFC status updated and lessons learned recorded

## 25. Approvals

> Select approvers and consulted reviewers according to the actual impact. Do not require every specialist to approve every change. See `guides/REVIEW_AND_APPROVAL.md`.

| Decision area / role | Name | Responsibility | Decision | Date | Conditions / comments |
|---|---|---|---|---|---|
| Business outcome / sponsor | | Approver | Approve / Changes requested / N/A | | |
| Product scope | | Approver | Approve / Changes requested / N/A | | |
| Engineering approach | | Approver | Approve / Changes requested / N/A | | |
| Design | | Consulted / Approver where applicable | Reviewed / Changes requested / N/A | | |
| QA | | Consulted | Reviewed / Changes requested / N/A | | |
| SRE / Platform | | Approver where infrastructure / operations affected | Approve / Changes requested / N/A | | |
| Security / Privacy | | Required where relevant | Approve / Changes requested / N/A | | |
| Data / Analytics | | Required where tracking / data definitions affected | Approve / Changes requested / N/A | | |
| Localization | | Required where user-facing language affected | Approve / Changes requested / N/A | | |
| Delivery readiness | | Product + Engineering | Ready / Not ready | | |

---

## Appendix

- **Glossary:** {terms and abbreviations used in this RFC}
- **References:** {links to research, prior RFCs, external docs}

**Change log**

| Date | Author | Change |
|---|---|---|
| {YYYY-MM-DD} | {Name} | {First draft} |
