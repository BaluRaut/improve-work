# Example: Cross-team delivery plan – Peer Field Intelligence

> Fictional example showing how one feature can be decomposed across product, frontend, backend, geospatial/data, platform, QA and analytics teams. Names, estimates, systems and metrics are illustrative only.
>
> Unlike the five RFC examples in this folder (set in the fictional Acme Retail), this example shows only the Delivery Plan stage, for a fictional agriculture product. In real use it would sit alongside a Feature Request Brief and an RFC that use the same Feature ID.

| Field | Value |
|---|---|
| Feature ID | FEAT-EXAMPLE-006 |
| Feature name | Peer Field Intelligence |
| Business owner | Product |
| Engineering lead | Engineering |
| Participating teams | Product, Frontend, Backend, Data/GIS, Platform, QA, Analytics |
| Complexity | Full |
| Feature Request Brief | Not included in this worked example |
| Technical RFC | Not included in this worked example |
| Status | Example only |

## 1. Delivery objective and scope baseline

Enable an authorized user to view aggregated, privacy-protected comparisons between their selected field and eligible peer fields, with clear data freshness and sample-size context.

**Illustrative non-goals:** exposing identifiable farm or grower records; individual farmer messaging; predictive recommendations; public ranking of farms.

## 2. Work breakdown summary

| Work ID | Workstream | Type | Deliverable / outcome | Owning team | Depends on | Estimate |
|---|---|---|---|---|---|---|
| WB-01 | Product / Design | Story | Peer comparison journey, eligibility rules and UX approved | Product | — | Team estimate pending |
| WB-02 | Data / GIS | Spike | Validate peer cohort methodology, minimum sample size and spatial eligibility | Data/GIS | WB-01 | Time-boxed spike |
| WB-03 | Backend | Story | Authorized API returns aggregated peer cohort metrics | Backend | WB-02 | Team estimate pending |
| WB-04 | Data / GIS | Story | Implement aggregation pipeline and freshness metadata | Data/GIS | WB-02 | Team estimate pending |
| WB-05 | Platform | Task | Configure scheduled processing, storage, access and monitoring | Platform | WB-04 | Team estimate pending |
| WB-06 | Frontend | Story | Build peer comparison map and summary UI | Frontend | WB-01, WB-03 | Team estimate pending |
| WB-07 | Frontend | Story | Show loading, empty, insufficient-sample and stale-data states | Frontend | WB-03, WB-06 | Team estimate pending |
| WB-08 | Security / Privacy | Task | Review aggregation thresholds, access controls and re-identification risk | Security / Privacy | WB-02, WB-03 | Review required |
| WB-09 | QA | Task | Validate authorization, aggregation, map behaviour and edge cases | QA | WB-03, WB-04, WB-06, WB-07 | Team estimate pending |
| WB-10 | Analytics | Task | Instrument feature adoption and comparison usage without personal data | Analytics | WB-06 | Team estimate pending |
| WB-11 | Release | Task | Pilot rollout, support guidance and outcome review | Product / Engineering | WB-08, WB-09, WB-10 | Team estimate pending |

## 3. Example acceptance criteria

### WB-03 – Aggregated peer cohort API

- Given a user is authorized for a field, when they request peer comparison, then the API returns only aggregated values for an eligible cohort.
- Given the cohort is below the approved minimum sample size, when the API responds, then it does not expose the comparison values and returns an explicit insufficient-sample state.
- Given a user requests a field they do not have access to, when the API is called, then access is denied without disclosing whether another user's field exists.
- Given the aggregate data is stale, when the API responds, then the freshness timestamp or stale status is included.

### WB-06 – Peer comparison UI

- Given eligible comparison data is available, when the user opens the feature, then the map and summary show the same selected cohort and metric.
- Given no eligible cohort exists, when the page loads, then the UI explains why comparison is unavailable and does not show misleading zero values.
- Given the request fails, when the user retries, then the UI recovers without duplicating the request or showing stale results as current.

## 4. Dependencies and sequencing

- WB-02 must define cohort rules and privacy thresholds before WB-03 and WB-04 are finalized.
- WB-03 and WB-04 must agree on metric definitions, units, time window and freshness semantics.
- WB-05 depends on the agreed pipeline and storage design.
- WB-06 can begin layout work using approved design and mocked API contracts while WB-03 is in progress.
- WB-09 validates the integrated experience after frontend and data/API work is available.
- WB-11 is not ready until privacy review and release gates are complete.

## 5. Risks and questions

| Item | Type | Owner | Required resolution |
|---|---|---|---|
| Cohort size may be too small in some geographies | Risk | Data/GIS + Product | Define fallback behaviour and threshold |
| Aggregates may permit re-identification in sparse areas | Privacy risk | Security / Privacy | Review thresholds and suppression rules |
| Data freshness differs across sources | Risk | Data/GIS | Define freshness contract and stale-state UX |
| Metric definitions differ between regions | Question | Product + Data | Approve common definitions or document regional variance |

## 6. Jira handoff

Create one Epic for FEAT-EXAMPLE-006. Create the work items only after Product, Engineering, QA and required Privacy reviewers approve the scope and delivery breakdown. Replace illustrative work IDs with Jira keys and record dependency links after creation.

**No estimates, assignees, sprint allocation or delivery dates are supplied in this example.** The owning teams must provide them.
