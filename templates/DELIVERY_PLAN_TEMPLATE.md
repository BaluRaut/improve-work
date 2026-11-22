# Delivery Plan: {Feature name}

> **Purpose:** Convert an approved scope and technical approach into a team-reviewed plan of independently testable work. This document complements the Feature Request Brief and Technical RFC; it does not replace either.
>
> **Guidance:** Work items listed here are proposals until the owning teams review them. Do not invent assignees, estimates, sprint allocations or committed dates.

| Field | Value |
|---|---|
| Feature ID | FEAT-{number} |
| Feature name | {Name} |
| Business owner | {Name} |
| Product owner | {Name} |
| Engineering lead | {Name} |
| Feature owner | {Engineer who leads the feature and writes this plan} |
| Participating teams | {Teams} |
| Complexity | Lite / Standard / Full |
| Feature Request Brief | {URL} |
| Technical RFC | {URL} |
| Status | Draft / In review / Approved / Ready for Jira / In delivery / Superseded |
| Last updated | {YYYY-MM-DD} |

## 1. Delivery objective and scope baseline

**Expected outcome**

{What outcome will be delivered?}

**Included scope**

- {Capability / outcome}

**Excluded scope**

- {Explicit non-goal}

**Acceptance criteria reference**

{Link to feature-level requirements and acceptance criteria in the RFC}

## 2. Work breakdown summary

| Work ID | Workstream | Type | Deliverable / outcome | Owning team | Depends on | Estimate | Confidence | Jira key |
|---|---|---|---|---|---|---|---|---|
| WB-01 | {Frontend} | Story | {User-visible outcome} | {Team} | — | {Team estimate / TBD} | {H/M/L} | {FEAT-123} |
| WB-02 | {Backend} | Story | {API capability} | {Team} | — | {Team estimate / TBD} | {H/M/L} | {FEAT-124} |
| WB-03 | {Platform} | Task | {Infrastructure outcome} | {Team} | WB-02 | {Team estimate / TBD} | {H/M/L} | {FEAT-125} |
| WB-04 | {QA} | Task | {Verification outcome} | {Team} | WB-01, WB-02 | {Team estimate / TBD} | {H/M/L} | {FEAT-126} |

> Work types must match your Jira configuration. Typical types are Epic, Story, Task, Bug and Spike. Do not create a Story solely because a row exists; choose the smallest useful work item type supported by your workflow.

## 3. Work item details

Repeat this block for each work item.

### WB-{ID}: {Title}

| Field | Value |
|---|---|
| Workstream | {Frontend / Backend / Data / Platform / QA / Analytics / Localization / Documentation / Release} |
| Type | {Story / Task / Spike / Bug} |
| Owning team | {Team} |
| Outcome | {What is independently delivered or learned?} |
| Dependencies | {Work IDs and reason, or none} |
| Estimate | {Team estimate or TBD} |
| Confidence | High / Medium / Low |
| RFC / requirement references | {FR-01, Section 8.2, etc.} |
| Jira key | {Added after creation} |

**Description and technical notes**

{Context, expected behaviour, interfaces and constraints. Avoid prescribing implementation beyond what the approved RFC requires.}

**Acceptance criteria**

- Given {context}, when {action}, then {observable result}.
- Given {edge condition}, when {action}, then {expected result}.

**Testing and evidence**

{Unit, integration, E2E, manual, accessibility, security, performance or other verification required.}

**Risks / assumptions**

{Known assumptions, open questions and owner.}

## 4. Dependencies and sequencing

| Dependency | Blocking work | Required output | Owner team | Needed by | Status |
|---|---|---|---|---|---|
| {Dependency} | {WB-ID} | {Output} | {Team} | {Date / phase} | Open / In progress / Resolved |

Describe the intended sequence. Identify parallel work and integration points. Make external dependencies visible; do not treat a dependency as resolved until its owner confirms it.

## 5. Milestones (forecast, not commitment)

| Milestone | Included work | Entry criteria | Exit criteria | Forecast / confidence | Owner |
|---|---|---|---|---|---|
| Design / contract agreed | {IDs} | {Criteria} | {Criteria} | {TBD} | {Role} |
| Integration in test environment | {IDs} | {Criteria} | {Criteria} | {TBD} | {Role} |
| QA and readiness sign-off | {IDs} | {Criteria} | {Criteria} | {TBD} | {Role} |
| Release and outcome review | {IDs} | {Criteria} | {Criteria} | {TBD} | {Role} |

## 6. Risks and unresolved questions

| Item | Type | Impact | Owner | Due / review date | Resolution |
|---|---|---|---|---|---|
| {Item} | Risk / Question / Assumption | {Impact} | {Name / role} | {Date} | {Status / answer} |

## 7. Jira handoff

| Jira field | Planned value |
|---|---|
| Jira project | {Project key} |
| Parent Epic | {Epic summary / key after creation} |
| Work item types | {Configured types} |
| Components / labels | {Team conventions} |
| RFC / Feature ID reference | {Link and ID} |
| Rovo used? | Yes / No |
| Rovo output reviewed by | {Names / roles} |
| Jira creation approved by | {Name / role} |

**Creation checklist**

- [ ] One Epic represents the agreed feature outcome.
- [ ] Work items map to the approved breakdown; no duplicates or invented scope.
- [ ] Each item has a clear outcome and testable acceptance criteria.
- [ ] Parent-child relationships and cross-team links match the Jira configuration.
- [ ] Dependencies and blockers are represented.
- [ ] Owning team / component is populated using existing conventions.
- [ ] Estimates were supplied or validated by the owning team.
- [ ] No assignee, sprint or committed due date was invented by automation.
- [ ] Feature ID, RFC and Delivery Plan links are present.
- [ ] Product and Engineering have approved the proposed Jira set.

## 8. Plan approval

| Role | Name | Decision | Date | Comments |
|---|---|---|---|---|
| Product owner | | Approve / Changes requested | | |
| Engineering lead | | Approve / Changes requested | | |
| Owning team representatives | | Reviewed | | |
| QA representative | | Reviewed | | |
| Specialist teams, where applicable | | Approve / N/A | | |

## 9. Change log

| Date | Author | Change |
|---|---|---|
| {YYYY-MM-DD} | {Name} | Initial plan |
