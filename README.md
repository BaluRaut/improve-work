# improve-work

A practical feature request-to-delivery toolkit for Product, Business and Engineering teams.

**Browse the current published site:** https://baluraut.github.io/improve-work/

The workflow connects a business request to refined requirements, an engineering RFC, a team-reviewed delivery plan and Jira work items. It is designed to create shared clarity without requiring every feature to complete every specialist review.

## Recommended workflow

1. **Request / Intake** – a business requestor explains the problem, evidence and intended outcome.
2. **Triage** – Product and Engineering assess value, fit, impact and complexity.
3. **Discovery** – clarify users, scope, requirements and acceptance criteria.
4. **Technical RFC** – document the proposed solution, decisions, risks and operational impact.
5. **Work breakdown** – engineering teams decompose and estimate independently testable work.
6. **Jira handoff** – use Rovo to draft Jira work items, review them and create approved items.
7. **Delivery and outcome review** – implement, release and measure the result.

See [guides/WORKFLOW.md](guides/WORKFLOW.md) for roles, statuses, gates and complexity levels.

## Start here

| Audience | Start with | Purpose |
|---|---|---|
| Business requestor | [Feature Request Brief](intake/FEATURE_REQUEST_TEMPLATE.md) | Describe the problem and desired outcome without prescribing the technical solution |
| Product / Engineering | [Technical RFC](RFC_TEMPLATE.md) | Refine requirements and document the proposed technical approach |
| Tech lead / delivery teams | [Delivery Plan](templates/DELIVERY_PLAN_TEMPLATE.md) | Break scope into workstreams, deliverables, dependencies and team estimates |
| Product / Engineering | [Definition of Ready](guides/DEFINITION_OF_READY.md) | Decide whether the feature and its stories are ready for development |
| Delivery teams | [Jira Story Template](templates/JIRA_STORY_TEMPLATE.md) | Keep individual Jira work items consistent |
| Rovo users | [Rovo Work Breakdown Prompt](templates/ROVO_WORK_BREAKDOWN_PROMPT.md) | Draft a reviewed Epic / Story / Task hierarchy from approved documents |

## Templates and guides

### Templates
- [Feature Request Brief](intake/FEATURE_REQUEST_TEMPLATE.md)
- [Technical RFC](RFC_TEMPLATE.md)
- [Delivery Plan](templates/DELIVERY_PLAN_TEMPLATE.md)
- [Jira Story / Task](templates/JIRA_STORY_TEMPLATE.md)
- [Rovo Work Breakdown Prompt](templates/ROVO_WORK_BREAKDOWN_PROMPT.md)

### Guides
- [End-to-end workflow](guides/WORKFLOW.md)
- [Definition of Ready](guides/DEFINITION_OF_READY.md)
- [Definition of Done](guides/DEFINITION_OF_DONE.md)
- [Review and approval matrix](guides/REVIEW_AND_APPROVAL.md)
- [Estimation guidelines](guides/ESTIMATION_GUIDELINES.md)

## Complexity levels

| Level | Typical use | Minimum documentation |
|---|---|---|
| Lite | Small, low-risk change contained within one team | Brief context, scope, acceptance criteria, test notes and Jira work |
| Standard | Normal feature needing technical refinement or coordination | Brief, relevant RFC sections, Delivery Plan and readiness checks |
| Full | Cross-team, architecture, security, data, compliance or operationally high-risk change | Complete brief, RFC, Delivery Plan, relevant specialist reviews and release / rollback plan |

Risk overrides size. A small authentication or production data migration change may still need Full review.

## Examples

Existing RFC examples demonstrate different technical change shapes. [Browse the examples](examples/README.md).

A new [cross-team Peer Field Intelligence delivery example](examples/CROSS_TEAM_DELIVERY_PLAN.md) demonstrates decomposition across Product, Frontend, Backend, Data/GIS, Platform, QA and Analytics.

## Source of truth

- **Feature Request Brief:** business problem, expected outcome and request context.
- **Technical RFC:** approved requirements, architecture, risks and technical decisions.
- **Delivery Plan:** reviewed work breakdown, dependencies, estimates and Jira mapping.
- **Jira:** execution status, team ownership, sprint allocation and delivery progress.

Use one Feature ID across all artifacts. Link rather than copy large sections between documents.

## Rovo and Jira

Rovo can help draft a work breakdown, but it must not silently decide product scope, architecture, estimates, owners, sprint allocation or delivery dates. Review the proposed hierarchy and each work item's acceptance criteria before creating Jira issues. Follow your organization's Jira issue types, fields, permissions and workflow.

## Validation and generated site

Markdown files are the source of truth. The Python build script generates the styled HTML pages and validates example RFC section usage.

After editing any Markdown file, rebuild:

```sh
uv run --with markdown python build.py
```

The build writes the HTML pages next to their Markdown sources and refreshes `index.html`.
