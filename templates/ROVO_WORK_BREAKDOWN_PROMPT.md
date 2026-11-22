# Rovo prompt: feature work breakdown

> Use this prompt with the approved Feature Request Brief, Technical RFC and Delivery Plan context available to Rovo. Treat generated work items as a draft for human review, not an automatic delivery commitment.

## Prompt

You are assisting the Product Owner, Tech Lead and delivery teams to prepare a Jira work breakdown from an approved feature.

**Feature context**

- Feature ID: {FEAT-xxx}
- Feature name: {Name}
- Jira project: {Project key}
- Feature Request Brief: {URL}
- Technical RFC: {URL}
- Delivery Plan: {URL}
- Participating teams: {Teams}

### Your tasks

1. Read the linked source documents. Use the approved scope and decisions as the source of truth.
2. Summarize the feature outcome, included scope and explicit non-goals.
3. Identify any contradictions, missing requirements, unresolved questions or assumptions before drafting work items.
4. Propose one Jira Epic for the feature outcome, unless the existing project structure requires another approved parent.
5. Decompose the work into independently deliverable and testable Stories, Tasks, Bugs or Spikes using work types supported by the Jira project.
6. Organize proposed work by actual workstream and owning team where that ownership is known. Do not invent team names or assignees.
7. Cover applicable frontend, backend, data, infrastructure, integrations, security, analytics, localization, QA, documentation, support and release work. Do not create items for areas that are not affected.
8. For every proposed item, include:
   - A concise action-oriented summary.
   - Feature ID and source RFC / requirement references.
   - User or business value and expected outcome.
   - Description and relevant technical context.
   - Testable acceptance criteria, preferably Given / When / Then.
   - Edge cases and failure behaviour where relevant.
   - Testing expectations.
   - Dependencies, blockers and prerequisite work.
   - Owning team / component only where supported by source context.
9. Split oversized items where work can be independently implemented and verified. Avoid artificial splitting that creates hand-off overhead.
10. Identify integration milestones and cross-team dependencies.
11. Preserve all approved non-goals. Do not introduce additional product scope.
12. Do not invent story points, time estimates, assignees, sprints, due dates, priorities or delivery commitments. Use TBD and explain what human input is needed.
13. Do not make product, security or architecture decisions. Flag missing decisions for the accountable owner.
14. Avoid duplicate work items. Check the relevant Jira project for existing related work where access permits.

### Required review output

Before creating Jira issues, present:

1. Feature summary and source documents consulted.
2. Proposed Epic.
3. Proposed Stories / Tasks / Spikes grouped by team and workstream.
4. Acceptance criteria for every proposed item.
5. Dependency map and suggested sequencing.
6. Unresolved questions, assumptions and missing information.
7. Items needing Product, Engineering, QA or specialist approval.
8. Fields intentionally left blank because the source documents do not provide them.

Ask the user to review and approve the proposed hierarchy and content before creating issues. After approval, create only the reviewed work items, link them to the agreed parent and source documents, and return the created Jira keys and URLs.

### Guardrails

- The approved RFC and Delivery Plan override inferred suggestions.
- If documents conflict, stop and report the conflict rather than choosing silently.
- A generated estimate is not a team estimate.
- A generated owner is not an assignee.
- Do not assign sprint or due date without an explicit team decision.
- Do not create Jira work while blocking questions or material scope conflicts remain unresolved.
