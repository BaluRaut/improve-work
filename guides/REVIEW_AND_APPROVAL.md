# Review and approval guide

## Review roles

Use role-based review rather than asking every department to approve every change.

- **Accountable approver:** owns the decision and confirms the proposal is acceptable in their domain.
- **Consulted reviewer:** provides required expertise or identifies impact; their feedback is resolved or documented.
- **Informed stakeholder:** receives visibility but does not block the decision unless new impact is identified.

One person may fill multiple roles, but the decision owner must be explicit.

## Suggested review matrix

| Change / impact | Product | Engineering / Tech lead | Design | QA | Platform / SRE | Security / Privacy | Data / Analytics | Localization |
|---|---|---|---|---|---|---|---|---|
| User-facing behaviour or scope | Approve scope | Review feasibility | Consult / approve UX | Consult | Inform if no ops impact | Consult if data/auth impact | Consult if metrics change | Consult if text/languages change |
| Frontend-only implementation | Consult | Approve technical approach | Consult | Consult | Inform | Consult only if relevant | Consult if tracking changes | Consult if text changes |
| API / service contract | Consult | Approve technical approach | Inform | Consult | Consult if service operations change | Consult if exposed data/auth changes | Consult if events change | Usually N/A |
| Database / data migration | Consult | Approve technical approach | N/A | Consult | Approve operational plan where owned | Consult for personal / sensitive data | Consult for data consumers | N/A |
| Cloud / network / production infrastructure | Inform | Approve service impact | N/A | Consult | Approve infrastructure and operations | Consult for access / exposure changes | Inform | N/A |
| Authentication, authorization or sensitive data | Consult | Approve technical approach | Consult if user flow changes | Consult | Consult | Required security / privacy review | Consult if data use changes | N/A |
| Analytics / event schema | Approve intended measures | Approve implementation ownership | Inform | Consult | Inform | Consult for personal data / consent | Approve event semantics and metrics | N/A |
| User-facing translations | Approve meaning | Approve integration | Consult | Consult | N/A | Consult where legal content applies | Inform | Approve language quality |

This is a starting point, not a substitute for company policy, regulatory obligations or service ownership rules.

## Approval record

For every required decision, record:

| Decision area | Approver | Decision | Date | Conditions / comments |
|---|---|---|---|---|
| Product scope | {Name / role} | Approve / Changes requested / N/A | {Date} | {Notes} |
| Technical approach | {Name / role} | Approve / Changes requested / N/A | {Date} | {Notes} |
| Specialist review | {Name / domain} | Approve / Changes requested / N/A | {Date} | {Notes} |
| Delivery readiness | {Name / role} | Ready / Not ready | {Date} | {Notes} |

## Rules

1. Reviewers are selected by impact, not copied from a fixed universal list.
2. A missing response is not an approval.
3. Resolve material objections or document the decision owner and accepted risk.
4. Scope approval, architecture approval and readiness for development are distinct decisions.
5. Small, low-risk changes can use lightweight review consistent with team policy.
