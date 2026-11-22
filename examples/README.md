# Example RFCs

Five RFCs for **Acme Retail**, a fictional online grocery and household store with a web app, Android and iOS apps, and a partner API. The company, people and numbers are invented, but each RFC is written the way a real one would be.

Each example uses only the sections its change needs, and lists the rest under "Sections not included" with a reason.

| RFC | Change | Shape | Sections used |
|---|---|---|---|
| [RFC-101](rfc-101-customer-order-cancellation.md) | Customers can cancel their own orders | Full stack: UI, API, queue, refunds, data, infra, events, translations, monitors | 23 of 25 |
| [RFC-102](rfc-102-partner-api-rate-limiting.md) | Rate limiting for the partner API | Backend and infrastructure, no UI | 18 of 25 |
| [RFC-103](rfc-103-dark-mode.md) | Dark mode for web and app | Frontend only | 14 of 25 |
| [RFC-104](rfc-104-postgres-16-upgrade.md) | Upgrade the orders database from PostgreSQL 13 to 16 | Infrastructure only | 18 of 25 |
| [RFC-105](rfc-105-marathi-and-tamil-languages.md) | Add Marathi and Tamil to the app | Translations-led, small backend part | 19 of 25 |

Assumed stack, for context: React web app, React Native mobile app, Node.js and TypeScript services on Kubernetes (EKS), PostgreSQL on Amazon RDS, Redis, SNS and SQS, Terraform, Datadog, Amplitude, Lokalise and a feature-flag service.
