# Examples

The RFC examples use **Acme Retail**, a fictional online grocery and household store with a web app, Android and iOS apps, and a partner API. The company, people and numbers are invented.

| RFC | Change | Shape |
|---|---|---|
| [RFC-101](rfc-101-customer-order-cancellation.md) | Customers can cancel their own orders | Full stack |
| [RFC-102](rfc-102-partner-api-rate-limiting.md) | Rate limiting for the partner API | Backend and infrastructure |
| [RFC-103](rfc-103-dark-mode.md) | Dark mode for web and app | Frontend only |
| [RFC-104](rfc-104-postgres-16-upgrade.md) | Upgrade the orders database from PostgreSQL 13 to 16 | Infrastructure only |
| [RFC-105](rfc-105-marathi-and-tamil-languages.md) | Add Marathi and Tamil to the app | Localization-led |

The additional [Peer Field Intelligence cross-team delivery plan](CROSS_TEAM_DELIVERY_PLAN.md) illustrates work decomposition across Product, Frontend, Backend, Data/GIS, Platform, QA and Analytics.

Assumed stack for the Acme examples: React web app, React Native mobile app, Node.js and TypeScript services on Kubernetes (EKS), PostgreSQL on Amazon RDS, Redis, SNS and SQS, Terraform, Datadog, Amplitude, Lokalise and a feature-flag service.
