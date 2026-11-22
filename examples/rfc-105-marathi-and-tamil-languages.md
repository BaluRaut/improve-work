# RFC: Add Marathi and Tamil to the app

> Example RFC for **Acme Retail** (fictional). A translations-led change with a small backend part; no new infrastructure or data model changes.

| Field | Value |
|---|---|
| RFC ID | RFC-105 |
| Title | Add Marathi and Tamil to the app |
| Feature owner | Nisha Bhat, Localization |
| Other authors | Arjun Mehta (mobile), Deepak R. (notifications) |
| Reviewers | Engineering lead, Product, Design, QA, Data, Localization |
| Status | In review |
| Created | 2026-10-20 |
| Last updated | 2026-10-27 |
| Target release | App 7.16 (mid-December 2026) |
| Links | Ticket: L10N-92 · Research: Regional language survey, September 2026 |
| Sections not included | 9 Data model: `users.locale` already accepts any language tag · 10 Infrastructure: fonts are bundled or downloaded by the OS; nothing new to host · 11 Security: no new personal data · 15 Performance: font size impact covered in 7 · 20 Alternatives: covered in 3 · 24 Launch checklist: in release ticket L10N-99 |

---

## 1. Summary

Offer the Android and iOS apps, push notifications, SMS and order emails in Marathi and Tamil, alongside English and Hindi. Customers can pick the language in Settings; new users get their phone's language automatically. Product names and descriptions stay as merchants wrote them for now.

## 2. Background and problem

- 31% of our customers in Maharashtra and 22% in Tamil Nadu have their phone set to Marathi or Tamil.
- When we launched Hindi last year, 30-day retention for customers with Hindi phones rose by 4 percentage points.
- Support handles about 900 calls a month from customers who struggle with English screens, mostly in checkout and order tracking.

## 3. Goals and non-goals

**Goals**

- Full app interface in Marathi (mr) and Tamil (ta).
- Push notifications, SMS and transactional emails in the chosen language.
- Language picker in Settings and on first launch.
- Correct fonts, line breaks and text length for both scripts.

**Non-goals**

- Translating product catalogue content (phase 2; needs merchant tooling).
- The web app (follows in RFC-112 once mobile has proven the workflow).
- Voice search.

Alternative considered: machine translation at runtime. Rejected for the interface because quality for checkout and payment wording must be reviewed by people; it may be used later as a first draft for catalogue content.

## 4. Success metrics

| Metric | Baseline | Target | Measured by | Review date |
|---|---|---|---|---|
| 30-day retention, customers using mr or ta | 34% (same users today, in English) | 37% | Amplitude cohort by `app_language` | 10 weeks after launch |
| Checkout completion, mr and ta users | 61% | 64% | Amplitude funnel | 6 weeks after launch |
| Support calls about language | about 900/month | under 500/month | Call tagging | 8 weeks after launch |

**Guardrail metrics:** crash rate unchanged; no increase in payment errors.

## 5. Users, requirements and use cases

- As a customer more comfortable in Marathi, I want the whole app in Marathi so that I understand prices, offers and order status.
- As a Tamil-speaking customer, I want delivery notifications in Tamil so that I know when my order arrives.
- As a customer in a family that shares a phone, I want to switch language easily.

## 6. Proposed solution

### 6.1 Overview

The app already uses i18next with Hindi, so the work is mostly content: about 1,850 strings (21,000 words) are translated in Lokalise by a vendor and reviewed by in-house native speakers against a glossary. The app sends the chosen language with every request (`Accept-Language`), and the notification service uses it to pick the right push, SMS and email templates.

### 6.2 User flow

1. First launch: if the phone language is mr or ta, the app starts in it and shows a one-time "Change language" chip.
2. Settings → Language → English / हिन्दी / मराठी / தமிழ், each shown in its own script.
3. Switching applies instantly without restarting the app.

## 7. Frontend changes

| Area | Change | Notes |
|---|---|---|
| Language picker | First-launch chip and Settings screen | Language names always in their own script |
| Fonts | Noto Sans Devanagari is already bundled; Noto Sans Tamil downloaded on demand on Android, system font on iOS | Avoids +1.1 MB in the app download |
| Layout | Tamil text is often 30 to 40% longer than English; buttons wrap to two lines instead of truncating | Fixed-width chips reviewed |
| Formatting | Dates, currency and plurals through `Intl` and i18next plural rules for mr and ta | Digits stay Latin (see open question) |
| Feature flag | `languages_mr_ta` | Off until review is complete |

## 8. Backend changes

### 8.1 Services and business logic

- `notification-service` adds mr and ta template variants for 46 templates (push, SMS, email) and selects by `users.locale`, falling back to English.
- SMS in Marathi and Tamil uses Unicode encoding, which fits 70 characters per message instead of 160; templates are rewritten to stay within two messages.

## 12. Event tracking and analytics

| Event name | Trigger (exactly when it fires) | Properties (name: type, example) | Platforms | Tool | New / Changed | Owner |
|---|---|---|---|---|---|---|
| language_changed | User picks a language in Settings or from the first-launch chip | from: string "en", to: string "mr", source: string "settings" | iOS, Android | Amplitude | New | Arjun |
| (user property) app_language | Set on app open and on change | value: "en", "hi", "mr" or "ta" | iOS, Android | Amplitude | New | Arjun |
| push_opened | Existing event | Adds language: string | iOS, Android | Amplitude | Changed | Deepak |

## 13. Translations and localization

| Item | Plan |
|---|---|
| Scope | 1,850 app strings, 46 notification templates, 12 email layouts, app-store listing |
| Languages | Marathi (mr), Tamil (ta); fallback English |
| Workflow | Lokalise; vendor translates; one in-house native reviewer per language checks every string in context with screenshots |
| Glossary | 120 terms fixed before translation starts (cart, delivery slot, wallet, cash on delivery…) so wording is consistent |
| Context | Every key has a screenshot and a note; maximum lengths set for buttons and chips |
| Plurals and variables | ICU messages for counts and amounts; translators never edit variable names |
| Testing | Pseudo-localization build (expanded, accented text) run before real translations arrive; final linguistic QA on devices |
| Cost and time | About ₹2.5 per word per language: roughly ₹1.05 lakh for both, plus review time; 3 weeks |
| Ongoing process | New strings go to translation in the same sprint; release blocked if mr or ta coverage drops below 100% for checkout and orders |

Example keys:

| Key | Default text (en) | Context for translators | Max length |
|---|---|---|---|
| checkout.place_order | Place order | Main checkout button | 20 |
| order.status.out_for_delivery | Out for delivery | Order tracking status | 28 |
| push.order_arriving | Your order will arrive in {minutes} minutes | Push notification title | 60 |
| cart.items_count | {count, plural, one {# item} other {# items}} | Cart header | 16 |

## 14. Observability and monitoring

### 14.3 Datadog monitors

| Monitor name | Type | Query / metric | Warn | Critical | Window | Priority | Notify | Runbook |
|---|---|---|---|---|---|---|---|---|
| [app] missing translation keys | Log | "i18n_missing_key" lang:(mr OR ta) | above 20 | above 200 | 1 h | P3 | @slack-l10n | runbooks/l10n/missing-keys |
| [notifications] template fallback to English | Metric | notifications.template_fallback{locale:mr OR locale:ta} | above 50 | above 500 | 1 h | P3 | @slack-notifications | runbooks/notifications/fallback |

## 16. Testing strategy

| Level | Scope | Owner | Automated |
|---|---|---|---|
| Pseudo-localization | Every screen in an expanded fake language; no truncation or overlap | QA | Partly |
| Screenshot tests | 60 key screens in mr and ta on a small and a large phone | QA | Yes |
| Linguistic QA | Native reviewers on real devices, checkout and orders first | Localization | No |
| Notifications | Each template renders and fits SMS length | Deepak | Yes |

## 17. Rollout plan

| Phase | Audience | Flag setting | Duration | Go / no-go criteria |
|---|---|---|---|---|
| 0 | Staff and 40 volunteer customers | on | 1 week | Native reviewers sign off checkout and orders |
| 1 | 20% of customers with mr or ta phones | 20% | 2 weeks | Crash rate and payment errors flat |
| 2 | Everyone | 100% | — | Remove flag after 1 month |

- **Kill switch:** turn off `languages_mr_ta`; affected users fall back to English (or Hindi if they chose it before).
- **Communication:** app-store "What's new" in all four languages; push announcement to mr and ta phone users at phase 2.

## 18. Rollback plan

| Step | How to roll back | Data impact | Time needed |
|---|---|---|---|
| Feature flag | Turn off | Saved language kept; app shows English | 1 min |
| Notification templates | Selection falls back to English automatically when the flag is off | None | 1 min |

## 19. Dependencies and impact on other teams

| Team / system | What we need or what changes for them | Contact | Status |
|---|---|---|---|
| Support | Agents who speak Marathi and Tamil on the language queue | Meera | Agreed |
| Marketing | App-store listing translations | Pooja | Pending |
| SMS provider | Unicode templates registered under DLT regulations before launch | Deepak | In progress |

## 21. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Wrong wording on payment screens | Medium | High | In-house review in context; checkout reviewed twice | Nisha |
| Long Tamil text breaks layouts | High | Medium | Pseudo-localization early; buttons wrap instead of truncating | Arjun |
| SMS template approval delays launch | Medium | Medium | Submit templates in week 1; push and email can launch first | Deepak |

## 22. Open questions, assumptions and decisions

| Question | Owner | Due | Answer |
|---|---|---|---|
| Latin digits (1, 2, 3) or native digits (१, २, ३ / ௧, ௨, ௩)? | Design and Localization | 2026-11-05 | Survey suggests Latin for prices; decide after volunteer test |

## 23. Milestones and delivery plan

| Milestone | Estimate | Target date |
|---|---|---|
| Glossary and pseudo-localization fixes | 1 week | 2026-11-06 |
| Translation and review | 3 weeks | 2026-11-27 |
| Notification templates and SMS approval | 2 weeks, in parallel | 2026-11-27 |
| Phase 0 volunteers | 1 week | 2026-12-04 |
| Release 7.16 | — | 2026-12-15 |

## 25. Approvals

| Role | Name | Decision | Date |
|---|---|---|---|
| Engineering lead | Vikram Rao | Pending | |
| Product manager | Anjali Deshpande | Approve | 2026-10-27 |
| Design | Kavya N. | Approve | 2026-10-26 |
| QA | Imran S. | Pending | |
| Data | Rohan G. | Approve | 2026-10-26 |
| Localization | Nisha B. | Owner | — |
