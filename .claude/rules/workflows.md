---
paths: [".github/workflows/**"]
---

# Regeln fuer GitHub Actions

- `update.yml` nicht aendern. Cron-Zeit, Rechte und der Commit auf main sind so gewollt.
- Neue Workflows bekommen minimale `permissions` (Standard `contents: read`, mehr nur wenn noetig und dann pro Job).
- Immer `timeout-minutes` setzen, damit ein haengender Lauf kein Kontingent frisst.
- `concurrency` mit `cancel-in-progress` bei allem, was pro Branch oder PR laeuft.
- Actions auf Major-Tags pinnen (`actions/checkout@v4`, `actions/setup-python@v5`), Dependabot haelt sie aktuell.
- Python im CI ist 3.12, lokal 3.11. Keine Syntax verwenden, die es nur in 3.12 gibt.
- Kein Workflow darf Secrets brauchen, solange keins eingerichtet ist. Sonst ist jeder PR rot.
