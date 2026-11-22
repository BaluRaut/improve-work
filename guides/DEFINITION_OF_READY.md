# Definition of Ready

## Feature-level readiness

A feature is **Ready for Development** when its scope is understood well enough for teams to plan and deliver it safely. It does not mean every implementation detail is predetermined.

- [ ] Feature ID, requestor, business sponsor and Product owner are identified.
- [ ] Business problem, evidence and desired outcome are documented.
- [ ] Goals, non-goals and in-scope / out-of-scope boundaries are agreed.
- [ ] Affected users, applications, regions and teams are identified.
- [ ] Functional requirements have unique IDs and testable acceptance criteria.
- [ ] Important edge cases and error/empty/loading/permission states are considered.
- [ ] UX designs or prototypes are linked, or explicitly marked not applicable.
- [ ] Relevant non-functional requirements are assessed: security, privacy, accessibility, performance, reliability, localization and operability.
- [ ] Technical approach and material alternatives are documented in the RFC.
- [ ] Data, API, integration and infrastructure impacts are identified, or marked not applicable with a reason.
- [ ] Cross-team dependencies have an owner, required-by date and status.
- [ ] Open questions that block implementation are resolved; remaining questions have owners and due dates.
- [ ] Risks and mitigations are recorded.
- [ ] Testing, rollout, monitoring and rollback approaches are understood at a level appropriate to the change.
- [ ] Work is broken into independently testable items; team estimates and confidence are recorded or explicitly pending.
- [ ] Required product, engineering and specialist reviews are complete.
- [ ] Delivery Plan and source documents are linked.

## Story / task-level readiness

Each Jira work item entering a sprint should have:

- [ ] A clear title and one primary outcome.
- [ ] Context and user/business value.
- [ ] Testable acceptance criteria.
- [ ] Dependencies and blockers identified.
- [ ] Owning team / component identified.
- [ ] UX, API contract, schema, sample data or technical references linked where relevant.
- [ ] Testing expectations described.
- [ ] Sized by the team using its agreed estimation approach, or explicitly treated as a spike / discovery item.
- [ ] Small enough to complete and verify within the team's normal delivery cadence.

## Handling incomplete information

Do not turn unknowns into assumptions silently.

- Mark unknowns explicitly and assign an owner and due date.
- If an unknown blocks safe implementation or acceptance, the item is not Ready.
- If discovery itself is the work, create a time-boxed Spike with a question, expected evidence and decision output.
- Product and Engineering may approve a documented exception for urgent work. Record the risk accepted, approver, compensating control and follow-up date.

## Readiness decision

| Decision | Meaning |
|---|---|
| Ready | All applicable checks are satisfied |
| Ready with action | Only non-blocking actions remain; each has an owner and date |
| Not ready | One or more blocking requirements are unresolved |

**Readiness is a shared Product and Engineering decision.** Sprint selection and capacity commitment remain with the delivery team.
