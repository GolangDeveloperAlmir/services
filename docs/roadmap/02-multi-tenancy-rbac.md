# PLAN-02: Organizations, tenant isolation and RBAC

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Status:** conditional future specification. Current API and database do not implement tenant isolation.

<a id="english"></a>
## English

### Goal and candidate model

Prevent a member of one organization from reading, listing, changing, deleting or indirectly discovering another organization's data. A role describes **what action** is allowed; tenant scope describes **which resources** are in bounds. Both checks are required on every path.

A candidate model for review is a global user/profile, organizations, memberships and role assignments scoped to membership. It is not an accepted product decision.

~~~mermaid
erDiagram
    ORGANIZATIONS ||--o{ MEMBERSHIPS : contains
    USERS ||--o{ MEMBERSHIPS : joins
    MEMBERSHIPS ||--o{ MEMBERSHIP_ROLES : receives
    ROLES ||--o{ MEMBERSHIP_ROLES : grants
    ORGANIZATIONS ||--o{ ORGANIZATION_AUDIT_EVENTS : scopes
~~~

| Entity | Candidate constraints | Decision required |
| --- | --- | --- |
| organizations | UUID, name, status and timestamps | Lifecycle, archive/delete, ownership transfer |
| memberships | Unique organization/user pair, status and inviter | Reinvite, expiry, revoke and rejoin |
| roles | Stable identifier and limited catalog | Tenant vs system roles; who manages definitions |
| membership_roles | Unique membership/role pair | Multiple roles and assignment authority |
| organization-owned records | Explicit tenant FK and scoped constraints | Which existing records belong to an organization |
| audit events | Actor, action, target, organization scope and timestamp | Minimum fields and retention alignment |

### Decisions before implementation

Resolve whether identity/profile is global or tenant-specific; whether a person can join multiple organizations; whether email uniqueness stays global or becomes tenant-scoped; who owns email changes; how invitations and organization lifecycle work; and whether a separately audited system-operator boundary is required.

Do not weaken the existing unique-email constraint or assign existing profiles to a default organization before an owner mapping and collision report are approved.

### Authorization invariants

- Tenant scope comes from a validated principal/membership or explicitly selected resource that is then authorized. A client-supplied organization ID is not proof of permission.
- Repository methods require an explicit typed tenant scope. Missing scope must not return a global result.
- List, count, pagination, filters, sorting, search and export use the same tenant predicate.
- Update/delete use tenant-scoped lookup and mutation; never perform a global fetch followed by a separate non-atomic permission check.
- Define a consistent 404/403 anti-enumeration policy for cross-tenant resources.
- CLI, migrations, background tasks and system jobs use explicit narrow system context, not an implicit HTTP principal.
- Database constraints reinforce authorization but never replace it.

### Migration and security tests

~~~mermaid
flowchart LR
    A["Inventory owners and data"] --> B["Expand compatible schema"]
    B --> C["Backfill approved mappings"]
    C --> D["Validate counts, FKs and ownership"]
    D --> E["Shadow/dual-read outside production"]
    E --> F["Enforce tenant scope"]
    F --> G["Contract legacy API after support window"]
~~~

Never silently move all legacy records to a default tenant. Backfill must be idempotent and auditable; ambiguous records require owner resolution. Test cross-tenant denial for direct reads, list/count/pagination, filters, sorting, updates, deletes, exports, nested resources, CLI and jobs. Include absent/revoked membership, altered tenant IDs, concurrent role changes, race conditions, orphan records and partial backfills. Verify both SQL/repository scope and HTTP behaviour.

### Acceptance criteria

ADRs define profile/identity ownership, membership, email uniqueness, lifecycle and system-operator boundary. Every tenant-owned entity has explicit validated ownership. No read/write/list/count/export/background path accesses tenant data without scope and permission. Cross-tenant negative tests pass at database and HTTP layers, including concurrency. Backfill is repeatable and never auto-assigns ambiguous records. Compatibility and client migration are published before rollout. Audit and operations follow approved privacy policy.

---

<a id="russian"></a>
## Русский

### Цель и кандидатная модель

Не допустить, чтобы участник одной организации мог читать, перечислять, менять, удалять или косвенно обнаруживать данные другой организации. Роль описывает **какое действие** разрешено; tenant scope определяет **какие ресурсы** доступны. Обе проверки обязательны в каждом пути.

Кандидатная модель для обсуждения: глобальный user/profile, organizations, memberships и назначения ролей внутри membership. Это пока не принятое продуктовое решение.

~~~mermaid
erDiagram
    ORGANIZATIONS ||--o{ MEMBERSHIPS : contains
    USERS ||--o{ MEMBERSHIPS : joins
    MEMBERSHIPS ||--o{ MEMBERSHIP_ROLES : receives
    ROLES ||--o{ MEMBERSHIP_ROLES : grants
    ORGANIZATIONS ||--o{ ORGANIZATION_AUDIT_EVENTS : scopes
~~~

| Сущность | Кандидатные ограничения | Что требуется решить |
| --- | --- | --- |
| organizations | UUID, name, status и timestamps | Lifecycle, archive/delete, передача владения |
| memberships | Уникальная пара organization/user, status и inviter | Повторное приглашение, expiry, revoke и rejoin |
| roles | Стабильный идентификатор и ограниченный каталог | Tenant или system roles; кто управляет определениями |
| membership_roles | Уникальная пара membership/role | Несколько ролей и полномочия назначения |
| organization-owned records | Явный tenant FK и scoped constraints | Какие существующие записи принадлежат организации |
| audit events | Actor, action, target, organization scope и timestamp | Минимальные поля и связь с retention |

### Решения до реализации

Определить, является identity/profile глобальной или tenant-specific; может ли человек состоять в нескольких организациях; остаётся ли email глобально уникальным или становится tenant-scoped; кто владеет изменением email; как работают приглашения и lifecycle организации; нужна ли отдельная audited-граница системного оператора.

Не ослаблять unique-email constraint и не назначать профили в default organization до утверждения owner mapping и отчёта о коллизиях.

### Инварианты авторизации

- Tenant scope берётся из проверенного principal/membership либо из явно выбранного ресурса, после чего проверяется авторизация. Переданный клиентом organization ID не доказывает наличие прав.
- Repository methods требуют явный типизированный tenant scope. При его отсутствии глобальный результат не возвращается.
- List, count, pagination, filters, sorting, search и export используют одинаковый tenant predicate.
- Update/delete выполняются через tenant-scoped lookup и mutation; нельзя сначала глобально получить запись, а потом отдельным неатомарным шагом проверять права.
- Нужно определить согласованную anti-enumeration политику 404/403 для межтенантных ресурсов.
- CLI, migrations, background tasks и system jobs используют явный ограниченный system context, а не неявный HTTP principal.
- Constraints БД усиливают авторизацию, но не заменяют её.

### Миграция и security-тесты

~~~mermaid
flowchart LR
    A["Инвентаризация владельцев и данных"] --> B["Расширение совместимой схемы"]
    B --> C["Backfill утверждённых связей"]
    C --> D["Проверка counts, FKs и ownership"]
    D --> E["Shadow/dual-read вне production"]
    E --> F["Обязательный tenant scope"]
    F --> G["Удаление legacy API после периода поддержки"]
~~~

Нельзя молча переносить все legacy-записи в default tenant. Backfill должен быть идемпотентным и аудируемым; неоднозначные записи требуют решения владельца. Проверять отказ межтенантного доступа для direct reads, list/count/pagination, filters, sorting, update, delete, exports, nested resources, CLI и jobs. Включить отсутствующий/отозванный membership, подменённые tenant IDs, конкурентные изменения ролей, race conditions, orphan records и частичные backfills. Проверять и SQL/repository scope, и HTTP-поведение.

### Критерии приёмки

ADR определяют владение profile/identity, membership, уникальность email, lifecycle и границу system operator. Каждая tenant-owned сущность имеет явное и проверяемое владение. Ни один read/write/list/count/export/background path не работает с tenant-данными без scope и permission. Cross-tenant negative tests проходят на уровне БД и HTTP, включая concurrency. Backfill повторяем и не назначает неоднозначные записи автоматически. Совместимость и миграция клиентов опубликованы до rollout. Audit и эксплуатация соответствуют утверждённой privacy policy.
