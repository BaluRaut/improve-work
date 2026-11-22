# RFC: Customers can cancel their own orders

> Example RFC for **Acme Retail**, a fictional online grocery and household store (web, Android and iOS). This one is a full-stack change, so it uses almost every section.

| Field | Value |
|---|---|
| RFC ID | RFC-101 |
| Title | Customers can cancel their own orders |
| Feature owner | Priya Kulkarni, Orders team |
| Other authors | Arjun Mehta (mobile), Sneha Iyer (payments) |
| Complexity | Full: automatic refunds touch money, and several teams ship together |
| Reviewers | Engineering lead, Product, Design, QA, SRE, Security, Data, Localization |
| Status | Approved |
| Created | 2026-10-06 |
| Last updated | 2026-10-20 |
| Target release | App 7.14, web release 2026-11-10 |
| Links | Ticket: ORD-1182 · PRD: Self-serve cancellation · Designs: Figma "Order detail v3" |
| Sections not included | 15 Performance: one extra write per cancellation, a few hundred a day, no measurable load · 24 Launch checklist: tracked in release ticket ORD-1190 |

---

## 1. Summary

Customers will be able to cancel an order from the order page within 30 minutes of placing it, as long as packing has not started. Prepaid orders are refunded automatically to the original payment method; cash-on-delivery orders are simply cancelled. Today every cancellation goes through support, which is slow for customers and expensive for us.

## 2. Background and problem

- Cancellation requests are 18% of all support tickets: about 4,200 a month.
- Median time from request to cancellation is 6 hours, because tickets wait in the queue.
- 9% of requests arrive after packing has started. Each of those costs about ₹45 in reverse logistics, and some customers refuse delivery instead.
- In the last customer survey, "could not cancel easily" was the third most common complaint.

## 3. Goals and non-goals

**Goals**

- Self-serve cancellation from the order page on web, Android and iOS, within 30 minutes and before packing.
- Automatic refund for prepaid orders, with a clear refund date shown to the customer.
- Warehouse stops picking a cancelled order within 60 seconds.

**Non-goals**

- Cancelling individual items (planned as RFC-118).
- Cancelling after dispatch; that stays in the returns flow.
- Changing the support team's own cancellation tool.

## 4. Success metrics

| Metric | Baseline | Target | Measured by | Review date |
|---|---|---|---|---|
| Cancellation support tickets per month | 4,200 | below 1,500 | Zendesk tag `cancel_request` | 6 weeks after 100% |
| Median time from request to cancellation | 6 h | under 2 min | `order_cancelled.minutes_since_placed` vs ticket time | 6 weeks after 100% |
| Cancellations after packing started | 9% of requests | below 3% | Warehouse system report | 6 weeks after 100% |

**Guardrail metrics:** overall cancellation rate must not rise more than 0.5 percentage points from 3.2%; refund failure rate must stay below 0.5%.

## 5. Users, requirements and use cases

- As a customer who ordered the wrong item, I want to cancel straight away so that I can reorder correctly.
- As a customer who found a better slot, I want to cancel without waiting for support.
- As a cash-on-delivery customer, I want to cancel so that the delivery partner does not come.
- Edge cases: the 30-minute window ends while the customer is on the confirm screen; packing starts while the customer is cancelling; poor network on the success screen.

## 6. Proposed solution

### 6.1 Overview

```text
App / Web ──POST /v1/orders/{id}/cancel──▶ orders-service ──(transaction: check window + state, mark cancelled)
                                              │
                                              └─ publish order.cancelled ─▶ SNS ─┬─▶ warehouse-consumer (stop picking)
                                                                                 └─▶ SQS order-refunds ─▶ refund-worker ─▶ payment provider refunds API
```

The order page shows a "Cancel order" button with a countdown while the order is eligible. The customer picks a reason and confirms. `orders-service` checks the window and fulfilment state inside a row lock, marks the order cancelled and publishes `order.cancelled`. The warehouse stops picking; for prepaid orders the refund worker creates a refund and stores its status.

### 6.2 User flow

1. Order page shows "Cancel order · 24 min left" if the order is eligible.
2. Tapping it opens a reason sheet with five reasons.
3. Confirm dialog: "Cancel this order? ₹1,249 will be refunded to your UPI account in 3 to 5 days."
4. Success state shows the refund amount and date. Errors: window expired, packing started, network error with retry.

## 7. Frontend changes

| Area | Change | Notes |
|---|---|---|
| Screens / routes | Order detail page gains the cancel entry point; new reason sheet and confirm dialog | Same flow on web and React Native app |
| Components | `CancelOrderButton` with live countdown, `ReasonSheet`, `CancelResult` | Reuses design-system `BottomSheet` and `Dialog` |
| State and data fetching | `useCancelOrder` mutation; invalidates `order:{id}` and `orders:list` | No optimistic update; wait for server result |
| Feature flag | `order_self_cancel` | Default off; targeted by user percentage |
| Accessibility | Countdown announced politely, not every second; dialog traps focus | WCAG 2.2 AA |
| Offline / poor network | Button disabled offline; on timeout, refetch order status before allowing retry | Avoids double cancel |
| Bundle size impact | +6 KB web, lazy-loaded with the order page | |

## 8. Backend changes

### 8.1 Services and business logic

`orders-service` gets a cancel use case. An order is eligible when `now < placed_at + 30 min` and `fulfilment_state = 'pending'`. The check and the update run in one transaction with `SELECT … FOR UPDATE` on the order row, so a cancellation and the warehouse's "start packing" cannot both win.

### 8.2 API changes

| Method | Path / operation | Auth | Request | Response | Errors | New / Changed / Breaking |
|---|---|---|---|---|---|---|
| POST | /v1/orders/{id}/cancel | Customer token, must own the order | `{ "reason_code": "ordered_by_mistake" }`, header `Idempotency-Key` | 200 `{ "status": "cancelled", "refund": { "id": "rf_123", "amount": 1249.00, "eta_days": 5 } }` | 403 not owner, 404, 409 `window_expired` / `packing_started` / `already_cancelled`, 429 | New |
| GET | /v1/orders/{id} | Customer token | — | Adds `cancellable_until` (ISO time or null) | — | Changed, additive |

**Backward compatibility:** additive only; old app versions ignore the new field.

**Idempotency, pagination, rate limits:** repeated requests with the same `Idempotency-Key` return the first result for 24 hours. Limit: 5 cancellations per customer per hour.

### 8.3 Background jobs, queues and scheduled tasks

| Job / consumer | Trigger or schedule | Queue / topic | Retries and dead-letter | Expected volume |
|---|---|---|---|---|
| refund-worker | `order.cancelled` for prepaid orders | SQS `order-refunds` | 5 retries, exponential backoff up to 15 min, DLQ `order-refunds-dlq` | about 250 a day |
| warehouse-consumer (existing) | `order.cancelled` | SQS `warehouse-orders` | existing policy | about 350 a day |
| refund-reconciler | every hour | — | alerts on refunds pending over 2 hours | — |

### 8.4 Third-party integrations

| Provider | Purpose | Auth / keys | Limits and cost | Failure behaviour |
|---|---|---|---|---|
| Payment provider refunds API | Create and track refunds | Existing key, refund scope added; stored in Secrets Manager | No extra fee for refunds | Retry on 5xx and timeouts; after 5 failures, DLQ plus support ticket created automatically |

## 9. Data model and migrations

| Table / collection | Change | Migration type | Backfill needed | Reversible |
|---|---|---|---|---|
| orders | Add `cancelled_at timestamptz null`, `cancel_reason varchar(32) null`, `cancelled_by varchar(16) null` | Online, nullable columns, no lock | No | Yes |
| refunds (new) | `id, order_id, provider_refund_id, amount_paise, status, attempts, created_at, updated_at`; unique on `order_id` | New table | No | Yes |

- **Migration order:** add columns and table → deploy service → enable flag.
- **Data volume and duration:** new columns are nullable with no default, so the change is instant on the 48 million row table.
- **Retention and deletion:** refunds kept 8 years for accounting; follows the existing order retention policy.
- **Personal data fields:** none new. `cancel_reason` is a fixed code, never free text.

## 10. Infrastructure changes

| Change | Environments | IaC location / PR | Owner | Monthly cost | Reversible |
|---|---|---|---|---|---|
| SQS `order-refunds` and `order-refunds-dlq`, subscribed to SNS `order-events` | dev, staging, prod | terraform/modules/orders-queues, PR #2210 | Priya K. | under $5 | Yes |
| `refund-worker` deployment, 2 replicas, 0.25 vCPU and 256 MB each | dev, staging, prod | helm/refund-worker | Priya K. | about $20 | Yes |

**Configuration, environment variables and secrets**

| Name | Purpose | Environments | Stored in | Default | Rotation |
|---|---|---|---|---|---|
| REFUND_QUEUE_URL | Queue for the refund worker | all | Helm values | — | n/a |
| PAYMENT_API_KEY | Existing key, now with refund scope | staging, prod | AWS Secrets Manager | — | 90 days, existing |

**Capacity and scaling:** worker scales 2 to 6 replicas on queue depth over 100.

## 11. Security, privacy and compliance

| Topic | Answer |
|---|---|
| Authentication and authorization | Customer token; server checks the order belongs to the caller; support tool unchanged |
| Personal data | No new personal data; reason is a fixed code |
| Abuse and rate limiting | 5 cancellations per customer per hour; repeated cancel-and-reorder patterns flagged to the fraud dashboard |
| Money movement | Refunds only to the original payment method, for the exact captured amount; never to a new account |
| Audit logging | `cancelled_by`, actor, time and IP stored in the existing order audit log |
| Security review needed | Yes, because it moves money; completed by Security on 2026-10-18 |

## 12. Event tracking and analytics

| Event name | Trigger (exactly when it fires) | Properties (name: type, example) | Platforms | Tool | New / Changed | Owner |
|---|---|---|---|---|---|---|
| order_cancel_viewed | Cancel button first becomes visible on the order page | order_id: string, minutes_left: int 24 | Web, iOS, Android | Amplitude | New | Arjun |
| order_cancel_started | Customer taps "Cancel order" | order_id, minutes_left | Web, iOS, Android | Amplitude | New | Arjun |
| order_cancelled | Server commits the cancellation | order_id, reason_code: string, minutes_since_placed: int 7, value: number 1249, payment_method: string "upi" | Server | Amplitude | New | Priya |
| order_cancel_failed | Server rejects the request | order_id, error_code: string "packing_started" | Server | Amplitude | New | Priya |
| refund_completed | Provider confirms the refund | order_id, amount, hours_to_refund: number | Server | Amplitude | New | Sneha |

- **Dashboards:** new funnel viewed → started → cancelled; reasons breakdown; cancellation rate guardrail chart.
- **QA of events:** verified in Amplitude debug view on staging for each platform before phase 1.

## 13. Translations and localization

| Key | Default text (en) | Context for translators | Max length | Languages | Status |
|---|---|---|---|---|---|
| order.cancel.button | Cancel order · {minutes} min left | Button on order page; minutes is a number | 32 | hi, mr | Done |
| order.cancel.reason.mistake | Ordered by mistake | Reason option | 30 | hi, mr | Done |
| order.cancel.reason.slot | Delivery slot no longer works | Reason option | 30 | hi, mr | Done |
| order.cancel.reason.price | Found a better price | Reason option | 30 | hi, mr | Done |
| order.cancel.reason.change | Want to change items | Reason option | 30 | hi, mr | Done |
| order.cancel.reason.other | Other reason | Reason option | 30 | hi, mr | Done |
| order.cancel.confirm | Cancel this order? {amount} will be refunded in {days} days. | Confirm dialog; amount is formatted currency | 90 | hi, mr | Done |
| order.cancel.error.packing | Sorry, packing has already started, so this order can't be cancelled. | Error state | 90 | hi, mr | Done |

- **Formatting:** amount uses the locale currency formatter; plural rules for "day/days".
- **Workflow:** Lokalise; reviewed by in-house Hindi and Marathi reviewers.

## 14. Observability and monitoring

### 14.2 Service level objectives

| SLI | SLO target | Window |
|---|---|---|
| Share of cancel requests without 5xx | 99.9% | 30 days |
| Refunds completed within 2 hours | 99% | 30 days |

### 14.3 Datadog monitors

| Monitor name | Type | Query / metric | Warn | Critical | Window | Priority | Notify | Runbook |
|---|---|---|---|---|---|---|---|---|
| [orders] cancel endpoint 5xx | APM | errors / hits, service:orders-service, resource:POST /v1/orders/{id}/cancel | over 2% | over 5% | 5 min | P1 | @pagerduty-orders, @slack-orders-alerts | runbooks/orders/cancel-errors |
| [orders] refund DLQ not empty | Metric | aws.sqs.approximate_number_of_messages_visible, queue:order-refunds-dlq | — | above 0 | 5 min | P2 | @slack-payments-alerts | runbooks/payments/refund-dlq |
| [orders] refunds stuck | Metric | refunds.pending_over_2h (from reconciler) | above 5 | above 20 | 15 min | P2 | @slack-payments-alerts | runbooks/payments/stuck-refunds |
| [orders] refund provider errors | APM | errors / hits, service:refund-worker, peer.service:payments-provider | over 5% | over 15% | 10 min | P2 | @slack-payments-alerts | runbooks/payments/provider-down |

- **Dashboard:** "Orders · Cancellations" with request rate, error rate, refund latency, DLQ depth.
- **Monitor management:** Terraform, `terraform/datadog/orders.tf`.

## 16. Testing strategy

| Level | Scope | Owner | Automated |
|---|---|---|---|
| Unit | Eligibility rules, including the window boundary and every fulfilment state | Priya | Yes |
| Integration | Race between cancel and "start packing" on the same row; idempotent retries | Priya | Yes |
| Contract | Refund worker against the provider sandbox | Sneha | Yes |
| End-to-end | Prepaid and COD cancellation on web, Android and iOS | QA | Yes |
| Localization | All strings in hi and mr on small screens | QA | Partly |
| Event tracking | Each event fires once with correct properties | Data | Partly |

## 17. Rollout plan

| Phase | Audience | Flag setting | Duration | Go / no-go criteria |
|---|---|---|---|---|
| 0 | Staff accounts | on for staff | 3 days | No P1 or P2 bugs; refunds reconcile |
| 1 | 10% of customers | 10% | 1 week | 5xx under 0.5%; cancellation rate up less than 0.5 pp |
| 2 | 50% | 50% | 1 week | Tickets trending down; refund failures under 0.5% |
| 3 | 100% | 100% | — | Remove flag within 2 sprints |

- **Deployment order:** Terraform queues → migration → orders-service and refund-worker → app and web releases → flag on.
- **Kill switch:** turn off `order_self_cancel`; the button disappears within a minute; support flow still works.
- **Communication:** support team briefed with a new macro; in-app "What's new" note at 100%.

## 18. Rollback plan

| Step | How to roll back | Data impact | Time needed |
|---|---|---|---|
| Feature flag | Turn off | None; refunds already started continue | 1 min |
| refund-worker | Scale to 0; queue keeps messages for 4 days | Refunds delayed, not lost | 2 min |
| orders-service | Redeploy previous version | New columns ignored | 10 min |

## 19. Dependencies and impact on other teams

| Team / system | What we need or what changes for them | Contact | Status |
|---|---|---|---|
| Warehouse | Consume `order.cancelled`; re-check status before printing a label | Rahul (WMS) | Agreed |
| Payments | Refund scope on the provider key | Sneha | Done |
| Support | New macro; ticket view shows self-cancelled orders | Meera | Agreed |

## 20. Alternatives considered

| Option | Pros | Cons | Why not chosen |
|---|---|---|---|
| "Request cancellation" button that creates a support ticket | No refund automation needed | Still slow; no ticket reduction | Does not solve the problem |
| Allow cancellation until dispatch | More flexible | Wasted picking and packing cost | Warehouse cost too high |

## 21. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Cancel and packing race | Medium | Medium | Row lock; warehouse re-checks status before labelling | Priya |
| Refund fails silently | Low | High | Reconciler every hour, DLQ alert, automatic support ticket | Sneha |
| Cancel-and-reorder abuse for coupons | Low | Medium | Coupon is returned only once per order; fraud dashboard flag | Priya |

## 22. Open questions, assumptions and decisions

| Question | Owner | Due | Answer |
|---|---|---|---|
| Should the window be 30 or 45 minutes? | Product | 2026-10-15 | 30 minutes; revisit after phase 2 data |

## 23. Milestones and delivery plan

| Milestone | Estimate | Target date |
|---|---|---|
| RFC approved | — | 2026-10-20 |
| Backend, queues and worker in staging | 6 days | 2026-10-29 |
| Web and app behind flag | 7 days | 2026-11-04 |
| QA sign-off | 3 days | 2026-11-07 |
| 100% rollout | 2 weeks of phases | 2026-11-24 |

## 25. Approvals

| Role | Name | Decision | Date |
|---|---|---|---|
| Engineering lead | Vikram Rao | Approve | 2026-10-20 |
| Product manager | Anjali Deshpande | Approve | 2026-10-19 |
| Design | Kavya N. | Approve | 2026-10-19 |
| QA | Imran S. | Approve | 2026-10-20 |
| SRE | Tejas P. | Approve | 2026-10-20 |
| Security | Farah A. | Approve | 2026-10-18 |
| Data | Rohan G. | Approve | 2026-10-19 |
| Localization | Nisha B. | Approve | 2026-10-19 |
