# Feature request-to-delivery workflow

## Purpose

Create one understandable path from a business request to an approved technical approach, an actionable delivery plan and tracked Jira work. The process should improve clarity without creating approval overhead for small changes.

## Working principles

1. **Business owns the problem and intended outcome.** Product clarifies user needs and scope. Engineering owns technical options and implementation design.
2. **Decisions are explicit.** Record assumptions, unresolved questions, trade-offs and decision owners.
3. **Right-size the process.** Apply Lite, Standard or Full documentation based on impact and risk, not just estimated effort.
4. **No silent commitments.** A requested deadline, AI-generated estimate or draft Jira item is not a team commitment.
5. **Keep one source of truth per concern.** The RFC records approved requirements and technical decisions; the Delivery Plan records planned work; Jira records execution status.
6. **Human review stays in the loop.** Rovo may draft analysis and work items, but accountable people approve scope, estimates, owners and Jira creation.
7. **The feature owner writes; the tech lead approves.** The engineer leading a feature writes its RFC and Delivery Plan. The tech lead coaches and approves rather than writing, so the whole team learns to design features and the tech lead does not become a bottleneck.

## End-to-end stages

| Stage | Accountable roles | Inputs | Activities | Exit / output |
|---|---|---|---|---|
| 1. Request / Intake | Requestor; Business sponsor | Business need, evidence, desired outcome | Complete Feature Request Brief; identify sponsor and urgency | Submitted request with a unique Feature ID |
| 2. Initial triage | Product owner; Engineering lead | Intake brief | Check value, duplication, fit, urgency, affected products and likely complexity; name the feature owner | Accept for discovery, reject, defer, duplicate or request information; feature owner named |
| 3. Discovery and refinement | Product; Feature owner; Design; QA; relevant SMEs | Accepted brief | Clarify users, workflows, functional requirements, acceptance criteria, constraints and success measures | Agreed scope, non-goals and testable requirements |
| 4. Technical RFC | Feature owner (writes); Tech lead (coaches and approves); relevant engineering owners | Refined requirements | Evaluate options, architecture, interfaces, data, security, operations, risks and rollout | Reviewed technical proposal with decisions and open questions |
| 5. Work breakdown and estimation | Feature owner (writes); delivery teams; QA; Tech lead (approves) | Approved scope and technical approach | Identify workstreams, independently testable stories/tasks, dependencies, sequencing and team estimates | Reviewed Delivery Plan and readiness assessment |
| 6. Jira handoff and planning | Product owner; Feature owner; team representatives | Approved Delivery Plan | Use Rovo or manual entry to draft Jira items; validate hierarchy, fields and dependencies; create and link issues | Jira Epic and agreed work items, ready for team planning |
| 7. Delivery and outcome review | Delivery teams; Feature owner; Product; Engineering lead | Jira plan and approved RFC | Implement, verify, release, monitor and measure outcomes | Released feature, actual results, follow-up actions and closed documentation |

## Complexity levels

Choose the lightest level that safely covers the change. Escalate when risk, impact or uncertainty warrants it.

| Level | Use when | Minimum artifacts |
|---|---|---|
| Lite | Small, low-risk change contained within one team; no material architecture, data, security or operational impact | Short request/context, scope, acceptance criteria, test notes and Jira items |
| Standard | Meaningful feature or service change needing technical refinement, multiple work items or coordination within a product area | Feature Request Brief, relevant RFC sections, Delivery Plan, Definition of Ready and Jira links |
| Full | Cross-team or cross-product change; material architecture, data migration, security/privacy, compliance, reliability, cost or operational risk | Complete Feature Request Brief, RFC, Delivery Plan, review matrix, rollout/rollback and outcome review |

**Risk overrides size:** a small authentication, payment, personal-data or production-migration change may require Full review.

## Workflow statuses

| Status | Meaning |
|---|---|
| Submitted | Request received; no commitment made |
| Triage | Product and Engineering are assessing value, fit and next action |
| Discovery | Requirements and scope are being clarified |
| RFC In Progress | Technical proposal is being prepared |
| In Review | Relevant stakeholders are reviewing the proposal |
| Approved for Breakdown | Scope and proposed solution are agreed; work decomposition can proceed |
| Ready for Development | Definition of Ready met; work items reviewed and estimable |
| In Delivery | Work is being implemented through normal team planning |
| Released | Change is deployed to the intended audience |
| Outcome Review | Actual results and guardrails are being assessed |
| Closed | Outcome review is complete and follow-ups are recorded |
| On Hold | Temporarily paused with a reason, owner and review date |
| Rejected / Duplicate / Deferred | Terminal or parked triage decision with rationale |

A feature can move backwards when new evidence invalidates assumptions or scope. Record why; do not hide the change.

## Responsibility boundaries

| Role | Owns | Does not unilaterally decide |
|---|---|---|
| Requestor | Problem context, evidence and stakeholder needs | Technical design or team estimates |
| Business sponsor | Business value, business priority and business trade-offs | Engineering capacity or technical feasibility |
| Product owner | User needs, product scope, priority and acceptance intent | Detailed implementation choices |
| Feature owner | Writing the RFC (Product writes sections 1–5) and the Delivery Plan; technical options, rollout and rollback; engineering point of contact from discovery to release | Approving their own RFC, or scope changes without Product |
| Tech lead / Engineering lead | Naming and coaching the feature owner; approving the technical approach and Delivery Plan; stepping in on high-risk decisions | Writing the RFC on the owner's behalf, business value or unapproved scope changes |
| Developers | Technical discovery, implementation details, estimates and delivery risks | Product policy without Product agreement |
| Design | Interaction model, usability and design specifications | Backend architecture |
| QA | Testability, coverage, quality risks and validation strategy | Acceptance of product scope on behalf of Product |
| Platform / Security / Data / Localization | Specialist review within their domain | Unrelated product or delivery decisions |

## Feature owner

Every Standard or Full feature has one feature owner: the engineer who leads it. The tech lead or engineering lead names them at triage.

- **The owner writes.** The feature owner writes the RFC and the Delivery Plan. The product owner writes RFC sections 1–5, and other engineers contribute the sections for their own areas.
- **Kick off together.** Before writing, the feature owner and tech lead spend about 30 minutes agreeing the options and constraints.
- **Review section 6 early.** The tech lead reviews the proposed solution before the remaining sections are written, so a late objection does not waste a week of work.
- **Coach through comments.** The tech lead asks questions and comments; they do not rewrite sections.
- **Match the feature to the person.** Anyone can own a Lite change, and Standard features suit mid-level engineers and above. On a Full feature, a less experienced owner pairs with a senior engineer on rollback, migration and security.
- **Plan the time.** Writing the RFC is a task in the sprint, not evening work.
- **Rotate.** Spread ownership across the team so everyone gets the practice.

The tech lead stays accountable for the engineering approval in RFC section 25.

## Handoffs and decision gates

- **Intake to discovery:** a requestor and business sponsor are identified; the problem and desired outcome are understandable.
- **Discovery to RFC:** scope, non-goals, users and acceptance criteria are sufficiently clear; unknowns have owners.
- **RFC to breakdown:** relevant technical reviewers have reviewed the approach; major risks and decisions are visible.
- **Breakdown to Jira:** each work item has an outcome, acceptance criteria, owning team, dependencies and estimate or an explicit reason why it is not estimated yet.
- **Jira to development:** feature-level and story-level Definition of Ready checks are satisfied; team capacity and sprint selection remain team decisions.
- **Release to closure:** release checks are complete and outcome review has an owner and date.

## Traceability

Use one Feature ID across the Feature Request Brief, RFC, Delivery Plan and Jira Epic. Link each Jira work item to the Epic and reference the RFC / Delivery Plan. Update links when documents move; do not copy entire documents into Jira descriptions.

## Exceptions

An urgent incident or regulatory deadline may need an expedited path. Record the reason, accountable decision-maker, minimum safety checks, and any deferred review with an owner and due date. An exception is not a reason to omit security, privacy or data-integrity controls.
