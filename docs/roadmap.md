# Project roadmap and decision gates

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Status:** proposals only. No target date, budget or delivery commitment is approved.

<a id="english"></a>
## English

### Current baseline

User Service is currently an administrator-only profile API with local administrator credentials, PostgreSQL, Redis-backed sessions, HTTPS ingress and a same-origin web console. It does not currently provide tenant isolation, public registration, user self-service, MFA, SSO/OIDC, account recovery, user-media uploads or a production deployment with approved SLOs.

The roadmap is deliberately conditional. Its purpose is to expose decisions, migration risks and acceptance evidence before implementation, not to turn every possible feature into a commitment.

### Principles

- **Deny by default:** missing or ambiguous identity, role, tenant scope or dependency state never expands access.
- **Separate profile, identity and access:** a profile does not automatically become a login account; roles do not replace resource ownership.
- **Security before convenience:** privileged actions require explicit authorization and auditable flows.
- **Measure before scaling:** no new cache, queue, database, broker or orchestrator without a confirmed workload and failure model.
- **Operations are part of completion:** backup/restore, monitoring, runbooks, ownership and rollback accompany production-facing features.
- **Compatibility is intentional:** API and schema changes need a migration and client-support strategy.

### Initiative map

| ID | Priority | Initiative | Condition / dependency | Specification |
| --- | --- | --- | --- | --- |
| PLAN-00 | P0 | Product scope, threat model and launch criteria | Required before major product expansion | This page |
| PLAN-01 | P0 | Production operations, recovery, audit and observability | After PLAN-00 decisions | [Platform foundation](roadmap/01-platform-foundation.md) |
| PLAN-02 | P1, conditional | Organizations, tenant isolation and scoped RBAC | Only if multi-organization use is confirmed | [Multi-tenancy](roadmap/02-multi-tenancy-rbac.md) |
| PLAN-03 | P1/P2, conditional | MFA, OIDC, verification and account recovery | Only for approved identity workflows | [Identity lifecycle](roadmap/03-identity-lifecycle.md) |
| PLAN-04 | P2/P3, conditional | Measured reliability and capacity improvement | After operational baseline and real workload | [Reliability and scale](roadmap/04-reliability-scale.md) |
| PLAN-05 | P1, conditional | Safe media ingestion and isolated processing | Only if user uploads become a product requirement | [Media pipeline](roadmap/05-media-pipeline.md) |

### Proposed sequence

~~~mermaid
flowchart TD
    A["PLAN-00: product and threat-model decisions"] --> B["PLAN-01: operational foundation"]
    B --> C{"Multi-organization demand?"}
    C -->|Confirmed| D["PLAN-02: tenant-aware access"]
    C -->|Not required| E["Keep single-operator model"]
    D --> F{"Identity workflows required?"}
    E --> G["PLAN-04: measured improvement only when justified"]
    F -->|Yes| H["PLAN-03: identity lifecycle"]
    F -->|No| G
    B --> I{"User media ingestion required?"}
    I -->|Yes| J["PLAN-05: isolated media pipeline"]
    I -->|No| K["Keep operator-managed read-only catalog"]
~~~

The sequence is a decision model, not a schedule. PLAN-02 and PLAN-03 may be excluded entirely if the service remains a single-operator internal API. PLAN-04 should not start because traffic might grow someday. PLAN-05 remains independent and must not weaken the existing read-only media boundary.

### Decisions required before implementation

| Decision | Question | Why it matters |
| --- | --- | --- |
| ADR-001 | One operator or multiple organizations? | Defines ownership, tenant boundaries and API design |
| ADR-002 | Is identity/profile global or organization-specific? Can one person join multiple organizations? | Defines keys, membership and email uniqueness |
| ADR-003 | Who invites users? Is public registration needed? | Changes abuse model and public attack surface |
| ADR-004 | Local credentials, OIDC, MFA, or a combination? | Defines authentication, session and recovery design |
| ADR-005 | Which profile data is allowed, who controls/processes it, and where may it live? | Defines privacy, retention and deletion |
| ADR-006 | Who operates the service and manages TLS, secrets and databases? | Defines deployment and incident ownership |
| ADR-007 | What availability, latency, RPO/RTO and maintenance targets are actually needed? | Prevents invented SLOs |
| ADR-008 | Which audit events and source IP fields are necessary, and for how long? | Defines privacy and audit retention |
| ADR-009 | Is a versioned external API required, and how long is compatibility kept? | Defines client migration |
| ADR-010 | Are external events/webhooks needed, with what delivery guarantees? | Prevents premature broker adoption |

### Definition of Ready

An initiative is ready for implementation only after it has an owner, confirmed user problem, bounded scope and non-goals, approved ADRs for disputed data/access/deployment decisions, threat model, data classification, versioned contracts, migration plan, measurable acceptance criteria, failure tests, operational ownership, rollout/rollback plan and support documentation.

### Definition of Done

A future initiative is complete only when its acceptance criteria are verified; migrations and recovery paths are tested; API and architecture docs match the implementation; authorization/privacy regressions are covered; operational signals and runbooks have owners; compatibility changes are approved; CI and target staging/pilot checks pass; and known limitations are recorded.

### Principal risks

| Risk | Consequence | Control |
| --- | --- | --- |
| Multi-tenancy without a data ownership model | Cross-tenant data exposure or costly migration | Resolve ADR-001–003 and require negative isolation tests |
| Treating a global admin role as tenant authorization | Excessive access | Scope every resource query and mutation |
| Assigning all legacy users to a default tenant | Unintended data aggregation | Require owner mapping; never silently create a default tenant |
| Linking OIDC accounts by matching email alone | Account takeover | Require verified linking and stable issuer/subject identity |
| Automating audit deletion without a policy | Loss of evidence or privacy violation | Approve purpose, fields, retention and legal hold first |
| Publishing SLOs without measurements | False reliability claims | Establish baseline, then approve objectives |
| Premature infrastructure expansion | More failure modes and operating cost | Require a reproducible bottleneck and cost/benefit decision |
| Large non-atomic migration | Downtime or inconsistent data | Expand/backfill/validate/contract and rehearse recovery |

### Detailed specifications

1. [PLAN-01 — Platform and operations foundation](roadmap/01-platform-foundation.md)
2. [PLAN-02 — Organizations, tenant isolation and RBAC](roadmap/02-multi-tenancy-rbac.md)
3. [PLAN-03 — Identity and account lifecycle](roadmap/03-identity-lifecycle.md)
4. [PLAN-04 — Reliability, performance and scale](roadmap/04-reliability-scale.md)
5. [PLAN-05 — Secure media ingestion and processing](roadmap/05-media-pipeline.md)

---

<a id="russian"></a>
## Русский

### Текущее состояние

Сейчас User Service — административный API профилей с локальными credentials администраторов, PostgreSQL, сессиями в Redis, HTTPS ingress и веб-панелью на том же origin. В текущей реализации нет изоляции арендаторов, публичной регистрации, пользовательского self-service, MFA, SSO/OIDC, восстановления аккаунта, загрузки пользовательских медиа или production-развёртывания с утверждёнными SLO.

Roadmap носит условный характер. Его задача — показать необходимые решения, риски миграции и критерии приёмки до начала разработки, а не превратить все возможные функции в обещания.

### Принципы

- **Deny by default:** отсутствие или неоднозначность identity, роли, tenant scope или состояния зависимости не расширяет доступ.
- **Разделять профиль, identity и доступ:** профиль не становится учётной записью автоматически, а роль не заменяет владение ресурсом.
- **Безопасность прежде удобства:** привилегированные действия требуют явной авторизации и проверяемого аудита.
- **Измерять до масштабирования:** не добавлять cache, queue, database, broker или orchestrator без подтверждённого workload и модели отказов.
- **Эксплуатация входит в готовность:** backup/restore, мониторинг, runbook, владельцы и rollback сопровождают production-функции.
- **Совместимость проектируется:** изменения API и схемы требуют стратегии миграции и поддержки клиентов.

### Карта инициатив

| ID | Приоритет | Инициатива | Условие / зависимость | Спецификация |
| --- | --- | --- | --- | --- |
| PLAN-00 | P0 | Продуктовый scope, threat model и критерии запуска | Требуется до крупных расширений продукта | Эта страница |
| PLAN-01 | P0 | Production-эксплуатация, восстановление, аудит и наблюдаемость | После решений PLAN-00 | [Платформенная основа](roadmap/01-platform-foundation.md) |
| PLAN-02 | P1, условно | Организации, tenant isolation и scoped RBAC | Только при подтверждённом multi-organization сценарии | [Мультитенантность](roadmap/02-multi-tenancy-rbac.md) |
| PLAN-03 | P1/P2, условно | MFA, OIDC, подтверждение и восстановление аккаунта | Только для утверждённых identity-сценариев | [Lifecycle identity](roadmap/03-identity-lifecycle.md) |
| PLAN-04 | P2/P3, условно | Измеряемая надёжность и развитие capacity | После operational baseline и появления реальной нагрузки | [Надёжность и масштаб](roadmap/04-reliability-scale.md) |
| PLAN-05 | P1, условно | Безопасная загрузка и изолированная обработка медиа | Только если пользовательские загрузки станут требованием продукта | [Media pipeline](roadmap/05-media-pipeline.md) |

### Предлагаемая последовательность

~~~mermaid
flowchart TD
    A["PLAN-00: продуктовые решения и threat model"] --> B["PLAN-01: эксплуатационная основа"]
    B --> C{"Нужны несколько организаций?"}
    C -->|Да, подтверждено| D["PLAN-02: tenant-aware доступ"]
    C -->|Нет| E["Сохранить single-operator модель"]
    D --> F{"Нужны identity workflows?"}
    E --> G["PLAN-04: измеренные улучшения только по необходимости"]
    F -->|Да| H["PLAN-03: lifecycle identity"]
    F -->|Нет| G
    B --> I{"Нужна загрузка пользовательских медиа?"}
    I -->|Да| J["PLAN-05: изолированный media pipeline"]
    I -->|Нет| K["Сохранить read-only каталог оператора"]
~~~

Это модель принятия решений, а не расписание. PLAN-02 и PLAN-03 можно полностью исключить, если сервис останется внутренним API одного оператора. PLAN-04 не следует начинать из-за гипотетического будущего роста трафика. PLAN-05 независим и не должен ослаблять существующую read-only границу каталога.

### Решения до реализации

| Решение | Вопрос | Почему важно |
| --- | --- | --- |
| ADR-001 | Один оператор или несколько организаций? | Определяет владение данными, tenant boundaries и API |
| ADR-002 | Identity/profile глобальны или принадлежат организации? Может ли человек состоять в нескольких организациях? | Определяет ключи, membership и уникальность email |
| ADR-003 | Кто приглашает пользователей? Нужна ли публичная регистрация? | Меняет abuse model и публичную поверхность атаки |
| ADR-004 | Локальные credentials, OIDC, MFA или комбинация? | Определяет аутентификацию, сессии и recovery |
| ADR-005 | Какие данные профиля допустимы, кто controller/processor и где они могут храниться? | Определяет privacy, retention и удаление |
| ADR-006 | Кто эксплуатирует сервис и управляет TLS, secrets и БД? | Определяет deployment и владельцев инцидентов |
| ADR-007 | Какие availability, latency, RPO/RTO и maintenance targets действительно нужны? | Не позволяет выдумывать SLO |
| ADR-008 | Какие audit-события и source IP необходимы и как долго их хранить? | Определяет privacy и retention |
| ADR-009 | Нужен ли версионируемый внешний API и как долго поддерживать совместимость? | Определяет миграцию клиентов |
| ADR-010 | Нужны ли внешние события/webhooks и какие гарантии доставки? | Предотвращает преждевременное внедрение broker |

### Definition of Ready

Инициатива готова к реализации только после назначения владельца, подтверждения пользовательской проблемы, ограничения scope и не-целей, утверждения ADR для спорных решений о данных/доступе/deployment, threat model, классификации данных, версионируемых контрактов, плана миграции, измеримых критериев приёмки, тестов отказов, эксплуатационных владельцев, rollout/rollback и документации поддержки.

### Definition of Done

Инициатива завершена только после проверки критериев приёмки; тестирования миграций и восстановления; согласования API/архитектурной документации с реализацией; регрессионных тестов авторизации и privacy; назначения владельцев сигналов и runbook; утверждения изменений совместимости; успешных CI и staging/pilot проверок; фиксации известных ограничений.

### Основные риски

| Риск | Последствие | Контроль |
| --- | --- | --- |
| Мультитенантность без модели владения данными | Межтенантная утечка или дорогая миграция | Решить ADR-001–003 и обязать negative isolation tests |
| Глобальная admin-роль как tenant-авторизация | Избыточный доступ | Scope для каждого query и mutation |
| Автоматическое назначение legacy-пользователей в default tenant | Непреднамеренное объединение данных | Требовать owner mapping; не создавать tenant по умолчанию молча |
| Связывание OIDC по одному email | Захват аккаунта | Подтверждённый linking и устойчивая issuer/subject identity |
| Автоудаление audit без политики | Потеря доказательств или нарушение privacy | Сначала утвердить цель, поля, retention и legal hold |
| Публикация SLO без измерений | Ложные обещания надёжности | Снять baseline, затем согласовать цели |
| Преждевременное расширение инфраструктуры | Больше отказов и эксплуатационных затрат | Требовать воспроизводимое узкое место и оценку затрат/пользы |
| Большая неатомарная миграция | Downtime или неконсистентные данные | Expand/backfill/validate/contract и проверка восстановления |

### Подробные спецификации

1. [PLAN-01 — Платформенная и эксплуатационная основа](roadmap/01-platform-foundation.md)
2. [PLAN-02 — Организации, tenant isolation и RBAC](roadmap/02-multi-tenancy-rbac.md)
3. [PLAN-03 — Identity и жизненный цикл аккаунта](roadmap/03-identity-lifecycle.md)
4. [PLAN-04 — Надёжность, производительность и масштабирование](roadmap/04-reliability-scale.md)
5. [PLAN-05 — Безопасный импорт и обработка медиа](roadmap/05-media-pipeline.md)
