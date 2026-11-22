# Jira work item template

> Use this structure for Stories and Tasks. Keep the description focused on one independently verifiable outcome.

## Summary

{Action + object + outcome}

## Context and value

**Feature ID:** {FEAT-xxx}

**RFC / Delivery Plan:** {Links}

**Why this work is needed:** {User or business value}

## Description

{What needs to change and relevant context. Include approved design, API, schema or technical links.}

## Acceptance criteria

- Given {starting context}, when {action}, then {observable result}.
- Given {edge case}, when {action}, then {expected result}.

## Dependencies

- Blocks / is blocked by: {Jira keys or none}
- External dependency owner: {Team / person or none}

## Technical notes

{Constraints, implementation considerations, relevant architecture references. Avoid duplicating the entire RFC.}

## Testing

- Unit: {Expected coverage}
- Integration / contract: {Expected coverage}
- End-to-end / manual: {Scenarios}
- Accessibility / localization / security / performance: {When applicable}

## Delivery metadata

| Field | Value |
|---|---|
| Owning team / component | {Team} |
| Estimate | {Team-agreed value / TBD} |
| Confidence | High / Medium / Low |
| Priority | {Product / team-agreed priority} |
| Assignee | {Set by team} |
| Sprint | {Set during team planning} |
