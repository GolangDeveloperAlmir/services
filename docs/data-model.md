# Data model and persistence

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Status:** current PostgreSQL model is implemented; the tenant model is a future design sketch.

<a id="english"></a>
## English

### Current PostgreSQL schema

~~~mermaid
erDiagram
    USERS ||--o| LOCAL_CREDENTIALS : authenticates
    USERS ||--o{ USER_ROLES : assigned
    AUTH_ROLES ||--o{ USER_ROLES : grants
    USERS o|--o{ USER_ROLES : assigns
    USERS o|--o{ SECURITY_AUDIT_EVENTS : acts
    USERS o|--o{ SECURITY_AUDIT_EVENTS : targets

    USERS {
        uuid id PK
        string email UK
        string full_name
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    LOCAL_CREDENTIALS {
        uuid user_id PK,FK
        string password_hash
        boolean is_enabled
        integer session_version
        datetime updated_at
    }
    AUTH_ROLES {
        string name PK
    }
    USER_ROLES {
        uuid user_id PK,FK
        string role_name PK,FK
        uuid assigned_by FK
        datetime assigned_at
    }
    SECURITY_AUDIT_EVENTS {
        uuid id PK
        uuid actor_user_id FK
        uuid target_user_id FK
        string event_type
        string source_ip
        datetime occurred_at
    }
~~~

The source of truth is the [shared SQLAlchemy profile model](../app/db/user_model.py), [authentication models](../app/auth/models.py), and [migrations 0001](../migrations/versions/0001_create_users.py) and [0002](../migrations/versions/0002_local_auth_rbac.py). PostgreSQL stores password hashes and role state. Raw bearer tokens and session payloads are not stored there.

### Entity responsibilities

| Entity | Responsibility | Important invariant |
| --- | --- | --- |
| <code>users</code> | Profile attributes and account-active flag | Email is normalized and unique; UUID is the identifier |
| <code>local_credentials</code> | Local password verifier, enabled state and session version | One-to-one with a profile; profile creation does not create it |
| <code>auth_roles</code> | Role vocabulary | Current built-in role is <code>admin</code> |
| <code>user_roles</code> | User-to-role assignment and assignment provenance | Composite key prevents duplicate assignment |
| <code>security_audit_events</code> | Security lifecycle events | Actor/target references can be cleared without deleting the event |

PostgreSQL is authoritative for active account and role state. Redis stores short-lived sessions and login rate counters. A session value contains the user UUID and credential version; its key derives from the token hash. Authorization still reads account, credential and role state from PostgreSQL, so deactivation or role changes take effect on the next authenticated request.

### Data and lifecycle rules

- <code>local_credentials.user_id</code> and <code>users.id</code> have a one-to-one relationship.
- <code>user_roles</code> uses a composite primary key; the current built-in role is <code>admin</code>.
- A profile is not an authentication account by itself. Local login requires a separate credential row and an active admin role.
- Profile CRUD stores normalized email casing. The unique database constraint is the final defence against concurrent duplicate writes.
- <code>assigned_by</code>, audit actor and audit target references are nullable and use <code>ON DELETE SET NULL</code>; deleting a user does not erase the audit event.
- Audit events include security mutations and successful authentication lifecycle events. Failed logins are represented by rate counters, not audit rows.
- Audit retention is not automated. Operators must define a privacy-compliant retention and deletion policy.
- Redis session state is ephemeral. Losing Redis invalidates sessions and resets counters; PostgreSQL remains authoritative for roles and credentials.
- Profile listing uses <code>created_at DESC, id ASC</code> with bounded <code>offset/limit</code>; this is query behaviour, not another entity.

### Future tenant model

Organizations, external identity-provider IDs, granular permissions and tenant-scoped records are **not implemented**. The sketch below is a design option only:

~~~mermaid
erDiagram
    ORGANIZATIONS ||--o{ MEMBERSHIPS : contains
    USERS ||--o{ MEMBERSHIPS : joins
    MEMBERSHIPS ||--o{ ROLE_ASSIGNMENTS : receives
    ROLES ||--o{ ROLE_ASSIGNMENTS : grants
    ROLES ||--o{ ROLE_PERMISSIONS : contains
    PERMISSIONS ||--o{ ROLE_PERMISSIONS : includes
~~~

Any tenant model requires explicit tenant-scoped database constraints, authorization checks on every operation, isolation tests and a reviewed migration plan. A role row alone is not a tenant boundary. See [roadmap initiative 02](roadmap/02-multi-tenancy-rbac.md).

---

<a id="russian"></a>
## Русский

### Текущая схема PostgreSQL

~~~mermaid
erDiagram
    USERS ||--o| LOCAL_CREDENTIALS : authenticates
    USERS ||--o{ USER_ROLES : assigned
    AUTH_ROLES ||--o{ USER_ROLES : grants
    USERS o|--o{ USER_ROLES : assigns
    USERS o|--o{ SECURITY_AUDIT_EVENTS : acts
    USERS o|--o{ SECURITY_AUDIT_EVENTS : targets
    USERS {
        uuid id PK
        string email UK
        string full_name
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    LOCAL_CREDENTIALS {
        uuid user_id PK,FK
        string password_hash
        boolean is_enabled
        integer session_version
        datetime updated_at
    }
    AUTH_ROLES {
        string name PK
    }
    USER_ROLES {
        uuid user_id PK,FK
        string role_name PK,FK
        uuid assigned_by FK
        datetime assigned_at
    }
    SECURITY_AUDIT_EVENTS {
        uuid id PK
        uuid actor_user_id FK
        uuid target_user_id FK
        string event_type
        string source_ip
        datetime occurred_at
    }
~~~

Источники истины — [общая SQLAlchemy-модель профиля](../app/db/user_model.py), [модели аутентификации](../app/auth/models.py), [миграция 0001](../migrations/versions/0001_create_users.py) и [0002](../migrations/versions/0002_local_auth_rbac.py). PostgreSQL хранит хеши паролей и состояние ролей. Сырые bearer-токены и payload сессий там не хранятся.

### Назначение сущностей

| Сущность | Ответственность | Важный инвариант |
| --- | --- | --- |
| <code>users</code> | Атрибуты профиля и флаг активности | Email нормализован и уникален; идентификатор — UUID |
| <code>local_credentials</code> | Проверочное значение локального пароля, enabled state и версия сессии | Связь один-к-одному; создание профиля не создаёт credentials |
| <code>auth_roles</code> | Справочник ролей | Сейчас встроена роль <code>admin</code> |
| <code>user_roles</code> | Назначение роли пользователю и provenance назначения | Составной ключ исключает дублирование назначения |
| <code>security_audit_events</code> | События жизненного цикла безопасности | Ссылки actor/target можно очистить, не удаляя само событие |

PostgreSQL является источником истины для состояния аккаунтов и ролей. Redis хранит короткоживущие сессии и счётчики попыток входа. Значение сессии содержит UUID пользователя и версию credentials; ключ основан на хеше токена. Авторизация всё равно читает состояние аккаунта, credentials и роли из PostgreSQL, поэтому деактивация или изменение роли вступают в силу при следующем аутентифицированном запросе.

### Правила данных и lifecycle

- <code>local_credentials.user_id</code> и <code>users.id</code> связаны отношением один-к-одному.
- <code>user_roles</code> использует составной первичный ключ; сейчас встроена роль <code>admin</code>.
- Профиль сам по себе не является учётной записью для входа. Локальная аутентификация требует отдельную строку credentials и активную роль admin.
- CRUD сохраняет email в нормализованном регистре. Уникальный constraint БД остаётся последней защитой от конкурентной записи дубликатов.
- Ссылки <code>assigned_by</code>, audit actor и audit target допускают NULL и используют <code>ON DELETE SET NULL</code>; удаление пользователя не стирает audit-событие.
- Audit содержит изменения безопасности и успешные события lifecycle аутентификации. Неуспешные входы учитываются rate counters, а не audit-строками.
- Retention аудита автоматически не реализован. Операторы должны определить политику хранения и удаления с учётом privacy.
- Состояние Redis-сессий временное. Потеря Redis сбрасывает сессии и счётчики; PostgreSQL сохраняет роль и credential state.
- Список профилей сортируется по <code>created_at DESC, id ASC</code> с ограничением <code>offset/limit</code>; это поведение запроса, а не отдельная сущность.

### Возможная будущая tenant-модель

Organizations, external identity-provider IDs, granular permissions и tenant-scoped записи **не реализованы**. Следующая схема — только один из вариантов проектирования:

~~~mermaid
erDiagram
    ORGANIZATIONS ||--o{ MEMBERSHIPS : contains
    USERS ||--o{ MEMBERSHIPS : joins
    MEMBERSHIPS ||--o{ ROLE_ASSIGNMENTS : receives
    ROLES ||--o{ ROLE_ASSIGNMENTS : grants
    ROLES ||--o{ ROLE_PERMISSIONS : contains
    PERMISSIONS ||--o{ ROLE_PERMISSIONS : includes
~~~

Любая tenant-модель требует явных tenant-scoped constraints в БД, проверки авторизации на каждой операции, тестов изоляции и проверенного плана миграции. Одна строка роли не является границей tenant-безопасности. См. [инициативу roadmap 02](roadmap/02-multi-tenancy-rbac.md).
