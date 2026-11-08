# PLAN-01: Platform and operational foundation

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Status:** future specification, not an existing production deployment.

<a id="english"></a>
## English

### Goal and scope

Prepare the service for a controlled pilot/production deployment that can be operated, monitored, backed up, restored and upgraded safely. Existing PostgreSQL/Redis TLS checks, allowed-host validation and health endpoints are necessary controls, but they do not constitute a tested production operating model.

The initiative covers deployment and trust boundaries; environment separation; secrets and certificate lifecycle; immutable-image releases and migration gates; PostgreSQL backup and restore; audit/privacy/retention policy; baseline observability, alert ownership and incident runbooks.

### Explicit non-goals without a separate ADR

No default cloud provider, Kubernetes, service mesh, managed product, active-active multi-region, zero-downtime guarantee, automatic certificate rotation, legal-compliance certification or numeric SLO/RPO/RTO/retention target is assumed.

### Proposed release flow

~~~mermaid
flowchart TD
    A["PR: tests, architecture, API and security gates"] --> B["Build immutable image from reviewed commit"]
    B --> C["Deploy to staging with production-like configuration"]
    C --> D["Migrate forward and run smoke/health/security checks"]
    D --> E{"Approval and stop conditions satisfied?"}
    E -->|Yes| F["Controlled pilot / rollout"]
    E -->|No| G["Stop rollout; investigate and recover"]
    F --> H["Observe, record evidence and review"]
~~~

Migration planning must separate expand, backfill, validate and contract for long-running changes. Do not promise automatic downgrade for destructive or irreversible migrations.

### Work packages and exit evidence

| Package | Work | Exit evidence |
| --- | --- | --- |
| 01-A Inventory | Deployment scenario, data classification, owners and threat model | Approved ADRs and trust-boundary diagram |
| 01-B Operating model | Secrets, TLS, networks, releases, access and support ownership | Repeatable deployment/runbook with no production secrets |
| 01-C Recovery | Backup scope, RPO/RTO and restore procedure | Witnessed restore drill and remediation list |
| 01-D Audit/privacy | Events, fields, access and retention | Approved policy and implementation plan |
| 01-E Signals | Baseline, SLI/SLO, alerts and cardinality controls | Owned signals and validated playbooks |
| 01-F Release gate | Staging release and migration exercise | Repeatable release with stop/rollback criteria |

### Acceptance criteria

Every environment, data set, secret class and production incident has an owner. Secrets and production data are absent from Git, images, CI logs and telemetry. Proxy/TLS/network trust boundaries are documented. Migrations run against a representative copy. Backups are accepted only after restore and validation of schema revision, data invariants, authentication and critical API flows. Audit retention is not automated until a privacy policy is approved. Each alert has an owner and evidence-based threshold. Staging can be stopped without undocumented data mutation. Security, architecture, observability and deployment docs are updated with implementation.

### Open decisions and risks

Deployment platform, secret manager, telemetry destination, audit retention, backup destination and on-call model remain undecided. Redis is currently ephemeral: loss invalidates sessions and resets rate counters; recovery instructions must cover safe reauthentication. Production readiness must not be inferred from local Compose.

---

<a id="russian"></a>
## Русский

### Цель и scope

Подготовить сервис к контролируемому pilot/production-развёртыванию, которое можно безопасно эксплуатировать, наблюдать, резервировать, восстанавливать и обновлять. Существующие проверки TLS PostgreSQL/Redis, allowed hosts и health endpoints необходимы, но сами по себе не образуют проверенную production-модель.

Инициатива охватывает deployment и границы доверия; разделение сред; lifecycle secrets и сертификатов; immutable-image releases и migration gates; backup/restore PostgreSQL; политику audit/privacy/retention; baseline observability, владельцев alert и incident runbooks.

### Явные не-цели без отдельного ADR

Не предполагается выбор cloud-провайдера, Kubernetes, service mesh, managed-продукта, active-active multi-region, гарантии zero downtime, автоматической ротации сертификатов, юридической сертификации или численных SLO/RPO/RTO/retention.

### Предлагаемый release flow

~~~mermaid
flowchart TD
    A["PR: tests, architecture, API и security gates"] --> B["Сборка immutable image из reviewed commit"]
    B --> C["Staging с production-like конфигурацией"]
    C --> D["Forward migration и smoke/health/security checks"]
    D --> E{"Approval и stop conditions выполнены?"}
    E -->|Да| F["Контролируемый pilot / rollout"]
    E -->|Нет| G["Остановить rollout, расследовать и восстановить"]
    F --> H["Наблюдать, фиксировать evidence и пересматривать"]
~~~

План длительных миграций должен разделять expand, backfill, validate и contract. Не обещайте автоматический downgrade для destructive или необратимых изменений.

### Пакеты работ и доказательства выхода

| Пакет | Работа | Доказательство выхода |
| --- | --- | --- |
| 01-A Inventory | Сценарий deployment, классификация данных, владельцы и threat model | Утверждённые ADR и схема границ доверия |
| 01-B Operating model | Secrets, TLS, сети, releases, доступ и поддержка | Повторяемый deployment/runbook без production-секретов |
| 01-C Recovery | Backup scope, RPO/RTO и restore | Проверенное упражнение restore и список исправлений |
| 01-D Audit/privacy | События, поля, доступ и retention | Утверждённая политика и план реализации |
| 01-E Signals | Baseline, SLI/SLO, alerts и cardinality controls | Сигналы с владельцами и проверенные playbook |
| 01-F Release gate | Staging release и миграционное упражнение | Повторяемый выпуск со stop/rollback критериями |

### Критерии приёмки

Для каждой среды, набора данных, класса секретов и production-инцидента назначен владелец. Секреты и production-данные отсутствуют в Git, images, CI logs и telemetry. Proxy/TLS/network trust boundaries документированы. Миграции проходят на репрезентативной копии. Backup принимается только после restore и проверки schema revision, инвариантов данных, аутентификации и критичных API flows. Retention audit не автоматизируется до утверждения privacy policy. У каждого alert есть владелец и основанный на evidence порог. Staging rollout можно остановить без недокументированного изменения данных. Security, architecture, observability и deployment docs обновляются вместе с реализацией.

### Открытые решения и риски

Платформа deployment, secret manager, место telemetry, audit retention, backup destination и модель on-call пока не выбраны. Redis сейчас эфемерен: потеря сбрасывает сессии и rate counters; инструкция восстановления должна описывать безопасную повторную аутентификацию. Production readiness нельзя выводить из локального Compose.
