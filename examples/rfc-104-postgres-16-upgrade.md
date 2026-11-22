# RFC: Upgrade the orders database from PostgreSQL 13 to 16

> Example RFC for **Acme Retail** (fictional). An infrastructure-only change: no product, UI, API or analytics changes.

| Field | Value |
|---|---|
| RFC ID | RFC-104 |
| Title | Upgrade the orders database from PostgreSQL 13 to 16 |
| Feature owner | Tejas Patil, SRE |
| Reviewers | Engineering lead, SRE, Orders team, Data, Security |
| Status | Approved |
| Created | 2026-09-15 |
| Last updated | 2026-10-01 |
| Target release | Production switchover Sunday 2026-11-08, 02:00 IST |
| Links | Ticket: SRE-877 · AWS RDS blue/green deployment documentation |
| Sections not included | 5 Users: no user-facing change · 7 Frontend: none · 8 Backend: no code changes; driver compatibility is covered in 16 · 12 Event tracking: none · 13 Translations: none · 20 Alternatives: covered in 6.1 · 24 Launch checklist: the runbook ops/pg16-runbook.md is the checklist for the night |

---

## 1. Summary

Upgrade the `orders-prod` Amazon RDS database from PostgreSQL 13 to 16 using RDS blue/green deployments, with about one minute of write downtime in a low-traffic window. PostgreSQL 13 is past community support and now costs us an RDS extended-support fee; version 16 is supported for years and is faster for our workload.

## 2. Background and problem

- PostgreSQL 13 reached community end of life in November 2025, and RDS standard support for it has ended. We now pay the RDS extended-support fee, about $580 a month for this instance at the current per-vCPU price (to be re-checked against AWS pricing).
- No more security patches from the community for version 13.
- Version 16 improves the queries we run most (parallel aggregates, better `IN` lists, faster `VACUUM`), and staging tests show p95 query time down 12%.

## 3. Goals and non-goals

**Goals**

- Production on PostgreSQL 16 with write downtime under 2 minutes.
- No data loss; no application code changes.
- Remove the extended-support fee.

**Non-goals**

- Changing instance size or storage type (separate cost review).
- Upgrading the analytics replica cluster (RFC-110).

## 4. Success metrics

| Metric | Baseline | Target | Measured by | Review date |
|---|---|---|---|---|
| Write downtime during switchover | — | under 2 min | Orders API error and synthetic monitors | Night of switchover |
| p95 query latency (top 20 queries) | 38 ms | at most 38 ms | Datadog Database Monitoring | 2 weeks after |
| Extended-support fee | about $580/month | $0 | AWS Cost Explorer | Next invoice |

## 6. Proposed solution

### 6.1 Overview

Use **RDS blue/green deployments**. RDS creates a green copy of the database kept in sync by logical replication, we upgrade the green copy to 16 and test it, and then RDS switches over: it blocks writes briefly, waits for the green copy to catch up, and renames the endpoints so applications reconnect without config changes.

Alternatives considered: an in-place major version upgrade means 20 to 40 minutes of downtime; a hand-built logical replication setup gives the same result with much more manual work.

### 6.2 Steps

1. Staging rehearsal of every step below, timed.
2. Check extensions in use (`pg_stat_statements`, `pgcrypto`, `uuid-ossp`) are available on 16; remove the unused `postgis` extension.
3. Create the blue/green deployment; upgrade green to 16 with a new parameter group carrying our current settings.
4. On green: `ANALYZE` all tables, compare query plans for the top 50 queries, run read-only smoke tests from a canary pod.
5. Switchover in the maintenance window; applications reconnect through the same endpoint.
6. Keep the old (blue) instance for 48 hours, then delete it.

## 9. Data model and migrations

| Table / collection | Change | Migration type | Backfill needed | Reversible |
|---|---|---|---|---|
| All | No schema change; major version upgrade | Blue/green | No | See 18 |

- **Prerequisites:** every table must have a primary key for logical replication. Two tables (`legacy_sessions`, `tmp_import_rows`) do not; the first gets a primary key, the second is dropped as unused.
- **Statistics:** planner statistics are not carried over, so `ANALYZE` runs on green before switchover.
- **Collation:** no change, because both versions use the same operating-system collation library on RDS.

## 10. Infrastructure changes

| Change | Environments | IaC location / PR | Owner | Monthly cost | Reversible |
|---|---|---|---|---|---|
| Parameter group `orders-pg16` (copy of current settings, family `postgres16`) | staging, prod | terraform/rds/orders.tf, PR #2188 | Tejas P. | — | Yes |
| Enable logical replication on the current parameter group (`rds.logical_replication = 1`), needs one reboot | staging, prod | same PR | Tejas P. | — | Yes |
| Blue/green deployment (temporary green instance during the cut-over) | staging, prod | Created by script `ops/pg16-bluegreen.sh`, then imported into Terraform | Tejas P. | about $90 for 3 days | Yes |
| Engine version `16.x` in the Terraform resource after switchover | prod | terraform/rds/orders.tf | Tejas P. | saves about $580 | — |

**Capacity and scaling:** same instance class; green is created at the same size.

**Disaster recovery:** a manual snapshot is taken right before switchover; automated backups and 7-day point-in-time recovery continue on the new instance.

## 11. Security, privacy and compliance

| Topic | Answer |
|---|---|
| Access | Same database users, roles and IAM authentication carried over; verified on green |
| Encryption | Same KMS key at rest; TLS required in transit, unchanged |
| Audit | `pgaudit` settings carried over in the new parameter group |

## 14. Observability and monitoring

### 14.3 Datadog monitors

These are temporary monitors for the migration, plus checks that existing ones still point at the right instance after the endpoint swap.

| Monitor name | Type | Query / metric | Warn | Critical | Window | Priority | Notify | Runbook |
|---|---|---|---|---|---|---|---|---|
| [db] blue/green replica lag | Metric | aws.rds.replica_lag, dbinstanceidentifier:orders-prod-green | over 30 s | over 300 s | 5 min | P2 | @slack-sre-alerts | runbooks/db/pg16-upgrade |
| [db] orders connections | Metric | aws.rds.database_connections, orders-prod | over 80% of max | over 95% | 5 min | P2 | @slack-sre-alerts | runbooks/db/connections |
| [db] orders CPU | Metric | aws.rds.cpuutilization, orders-prod | over 70% | over 90% | 15 min | P3 | @slack-sre-alerts | runbooks/db/cpu |
| [orders] API 5xx (existing) | APM | errors / hits, service:orders-service | over 1% | over 3% | 5 min | P1 | @pagerduty-orders | runbooks/orders/errors |

- **Dashboard:** "Orders DB · PG16 upgrade": lag, connections, CPU, top queries before and after (Database Monitoring).
- After switchover, confirm the Datadog integration reports the instance as version 16 and Database Monitoring still collects query samples.

## 15. Performance and scalability

| Item | Expectation |
|---|---|
| Query plans | Top 50 queries compared on green; any plan regression over 20% blocks the switchover |
| Load | Replay 1 hour of production traffic (pgreplay) against staging on 16; p95 not worse than on 13 |

## 16. Testing strategy

| Level | Scope | Owner | Automated |
|---|---|---|---|
| Driver compatibility | Node `pg` 8.x and the Java JDBC driver tested against 16 in staging | Orders team | Yes |
| Integration | Full orders test suite against staging on 16 | Orders team | Yes |
| Rehearsal | End-to-end blue/green in staging, timed | SRE | No |
| Load | pgreplay as in 15 | SRE | Partly |

## 17. Rollout plan

| Phase | Audience | Setting | Duration | Go / no-go criteria |
|---|---|---|---|---|
| 0 | Staging | Blue/green and switchover | 1 week before | Rehearsal under 2 min downtime; tests green |
| 1 | Production green created and upgraded | — | 2 days before | Replica lag under 30 s; plans checked |
| 2 | Production switchover | — | Sunday 02:00 to 03:00 IST | Lag 0 at switchover; smoke tests pass within 5 min |
| 3 | Delete old blue instance | — | 48 hours after | No issues reported |

- **Communication:** status page notice 3 days ahead; on-call for Orders and SRE online during the window; support informed.
- **Kill switch:** before switchover, simply delete the green environment.

## 18. Rollback plan

| Step | How to roll back | Data impact | Time needed |
|---|---|---|---|
| Before switchover | Delete the green environment; nothing changed for users | None | 10 min |
| After switchover, problem found within minutes | Fix forward (parameter or index change), since the old instance stops receiving writes after switchover | None | Varies |
| After switchover, severe failure | Restore from the pre-switchover snapshot or point-in-time recovery to a new instance; repoint the endpoint | Up to 5 minutes of writes lost; would be reconciled from event logs | about 45 min |

## 19. Dependencies and impact on other teams

| Team / system | What we need or what changes for them | Contact | Status |
|---|---|---|---|
| Orders team | Run test suite on staging 16; be on call during the window | Priya K. | Agreed |
| Data | Change-data-capture pipeline (Debezium) reconnects after switchover; verify no gap | Rohan G. | Agreed |

## 21. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Query plan regression on 16 | Medium | High | Plan comparison gate; `ANALYZE` first; parameter rollback ready | Tejas |
| Table without primary key breaks replication | Known | High | Fix the two tables before creating blue/green | Tejas |
| CDC pipeline misses events at switchover | Low | Medium | Pause consumers during switchover; replay from Kafka offsets | Rohan |

## 22. Open questions, assumptions and decisions

| Question | Owner | Due | Answer |
|---|---|---|---|
| 16 or 17? | SRE | 2026-09-25 | 16: longest track record on RDS for our extensions; revisit 17 next year |

## 23. Milestones and delivery plan

| Milestone | Target date |
|---|---|
| Primary-key fixes and parameter changes in prod | 2026-10-20 |
| Staging rehearsal | 2026-10-30 |
| Production switchover | 2026-11-08 |
| Old instance deleted | 2026-11-10 |

## 25. Approvals

| Role | Name | Decision | Date |
|---|---|---|---|
| Engineering lead | Vikram Rao | Approve | 2026-10-01 |
| SRE | Tejas P. | Owner | — |
| Orders team | Priya K. | Approve | 2026-09-30 |
| Data | Rohan G. | Approve | 2026-09-30 |
| Security | Farah A. | Approve | 2026-09-29 |
