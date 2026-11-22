# RFC: Dark mode for web and app

> Example RFC for **Acme Retail** (fictional). A frontend-only change: no backend, data, infrastructure or new server monitoring.

| Field | Value |
|---|---|
| RFC ID | RFC-103 |
| Title | Dark mode for web and app |
| Feature owner | Ananya Joshi, Design Systems |
| Reviewers | Engineering lead, Design, QA, Accessibility champion, Data |
| Status | Approved |
| Created | 2026-09-29 |
| Last updated | 2026-10-08 |
| Target release | App 7.13, web 2026-10-27 |
| Links | Ticket: DS-301 · Designs: Figma "Theme tokens v2" |
| Sections not included | 8 Backend: preference is stored on the device only · 9 Data model: nothing stored on the server · 10 Infrastructure: none · 11 Security: no personal data or permissions involved · 14 Observability: no new server paths; existing RUM error tracking covers the UI · 15 Performance: CSS variables add no runtime cost; bundle impact noted in 7 · 19 Dependencies: none outside the frontend teams · 20 Alternatives: none seriously considered; tokens are the standard approach · 22 Open questions: none left · 23 Milestones: fits in the current sprint · 24 Launch checklist: in the release ticket |

---

## 1. Summary

Add a dark theme to the web app and the Android and iOS apps, with a Settings choice of System default, Light or Dark. Colours move to design tokens so both themes come from one source, and contrast meets WCAG AA in both.

## 2. Background and problem

- Dark mode is the most requested feature in app-store reviews: 37 mentions last quarter.
- 41% of our app sessions start between 8 pm and midnight, when a bright white screen is uncomfortable.
- Colours are hard-coded in about 1,100 places today, which also slows every redesign.

## 3. Goals and non-goals

**Goals**

- System, Light and Dark options; System is the default.
- No flash of the wrong theme when the web page loads.
- All screens pass WCAG AA contrast in both themes.
- Colours defined once as design tokens.

**Non-goals**

- Syncing the choice across devices.
- Dark versions of marketing emails.
- Redesigning any screen beyond colours.

## 4. Success metrics

| Metric | Baseline | Target | Measured by | Review date |
|---|---|---|---|---|
| Share of active users on dark (explicit or via system) | 0% | at least 20% | Amplitude user property `theme_effective` | 8 weeks after launch |
| App-store reviews requesting dark mode | 37 per quarter | under 5 per quarter | Review tagging | Next quarter |

**Guardrail metrics:** zero new accessibility contrast violations; no change in checkout conversion.

## 5. Users, requirements and use cases

- As a customer shopping late at night, I want a dark screen so that it does not hurt my eyes.
- As a customer whose phone is already in dark mode, I want the app to follow it automatically.
- As a customer with low vision, I want enough contrast in either theme.

## 6. Proposed solution

### 6.1 Overview

Colours become semantic tokens (`color.bg.surface`, `color.text.primary`, `color.border.subtle`, and so on, about 60 tokens) with light and dark values. On web they are CSS custom properties switched by `data-theme` on `<html>` and by `prefers-color-scheme`. In React Native a `ThemeProvider` uses `useColorScheme()` and the saved choice. A codemod replaces hard-coded colours with tokens; the remaining cases are fixed by hand.

### 6.2 User flow

1. Settings → Appearance → System default / Light / Dark.
2. The choice applies immediately and is remembered on this device.
3. On first launch the app follows the device setting.

## 7. Frontend changes

| Area | Change | Notes |
|---|---|---|
| Design tokens | 60 semantic colour tokens with light and dark values, generated for CSS and React Native from one JSON file | Style Dictionary |
| Web | Tokens as CSS variables; small inline script in `<head>` reads the saved choice before first paint | Prevents flash of the wrong theme |
| App | `ThemeProvider` and `useTheme()`; status bar and navigation bar colours follow the theme | Android and iOS |
| Images and illustrations | Logo and 14 illustrations get dark variants; product photos unchanged | |
| Charts | Order-history charts read colours from tokens | |
| Feature flag | `dark_mode` | Hides the Settings option while off |
| Accessibility | Every token pair checked for AA contrast; focus rings visible in both themes | Automated check in CI |
| Bundle size impact | Web +3 KB CSS; app +40 KB for dark illustrations | |

## 12. Event tracking and analytics

| Event name | Trigger (exactly when it fires) | Properties (name: type, example) | Platforms | Tool | New / Changed | Owner |
|---|---|---|---|---|---|---|
| theme_changed | User picks an option in Settings → Appearance | from: string "system", to: string "dark" | Web, iOS, Android | Amplitude | New | Ananya |
| (user property) theme_effective | Set on app open and on change | value: "light" or "dark" (what is actually shown) | Web, iOS, Android | Amplitude | New | Ananya |

## 13. Translations and localization

| Key | Default text (en) | Context for translators | Max length | Languages | Status |
|---|---|---|---|---|---|
| settings.appearance.title | Appearance | Settings section title | 24 | hi, mr | Done |
| settings.appearance.system | System default | Option: follow the phone's setting | 24 | hi, mr | Done |
| settings.appearance.light | Light | Option | 16 | hi, mr | Done |
| settings.appearance.dark | Dark | Option | 16 | hi, mr | Done |

## 16. Testing strategy

| Level | Scope | Owner | Automated |
|---|---|---|---|
| Visual regression | Chromatic snapshots of 180 stories in both themes | Ananya | Yes |
| Accessibility | axe-core contrast check on 25 key pages in both themes | QA | Yes |
| End-to-end | Switching themes; no flash on reload; system change while app is open | QA | Yes |
| Manual | Low-end Android devices; OLED screens | QA | No |

## 17. Rollout plan

| Phase | Audience | Flag setting | Duration | Go / no-go criteria |
|---|---|---|---|---|
| 0 | Staff | on | 1 week | All screens reviewed by Design in dark |
| 1 | 25% | 25% | 1 week | No contrast bugs reported; conversion flat |
| 2 | 100% | 100% | — | Remove flag after 2 sprints |

- **Kill switch:** turn off `dark_mode`; the option disappears and everyone sees Light.

## 18. Rollback plan

| Step | How to roll back | Data impact | Time needed |
|---|---|---|---|
| Feature flag | Turn off | Saved choice ignored, kept on device | 1 min |
| Tokens migration | Light token values are identical to today's colours, so no visual rollback is needed | None | — |

## 21. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| A screen keeps a hard-coded white background | High | Low | Lint rule bans raw colour values; visual snapshots | Ananya |
| Third-party payment page stays light | Certain | Low | Accept; it opens in its own sheet | Product |

## 25. Approvals

| Role | Name | Decision | Date |
|---|---|---|---|
| Engineering lead | Vikram Rao | Approve | 2026-10-08 |
| Design | Kavya N. | Approve | 2026-10-07 |
| QA | Imran S. | Approve | 2026-10-08 |
| Accessibility | Joseph M. | Approve | 2026-10-07 |
| Data | Rohan G. | Approve | 2026-10-07 |
