# Product overview

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Product status:** implemented narrow-scope service, not a hosted platform.

<a id="english"></a>
## English

### A profile service with a deliberately small trust surface

User Service provides an HTTP API and a lightweight web console for administrators who need to create, inspect, update and remove user-profile records. Its defining choice is separation: profile data, local credentials, role assignments and expiring sessions are different parts of the model.

The service is built for controlled administrative workflows and engineering review. It is not marketed as a drop-in identity provider, customer directory SaaS or turnkey production deployment.

### The value proposition

| Product principle | What it means in practice |
| --- | --- |
| Narrow by design | Profile CRUD is the product boundary; identity expansion requires a separate decision. |
| Explicit authorization | Every profile endpoint requires an active administrator. |
| Data integrity | Normalized unique email, UUID identifiers and bounded deterministic pagination. |
| Fail closed | Missing/invalid credentials, roles, sessions or dependencies do not grant access. |
| Inspectable operations | Compose topology, health checks, JSON request logs and optional traces. |
| Contract-first visibility | FastAPI generates OpenAPI; validation is part of the development checks. |

### What is available today

- Local administrator login and logout with short-lived opaque bearer tokens.
- Argon2id password hashing and protected password rotation.
- Administrator grant/revocation with password reauthentication, audit events and safeguards around the last active administrator.
- Admin-only profile create, list, read, update and delete operations.
- A same-origin TypeScript console; the access token remains in tab memory.
- A read-only catalog of operator-managed images and audio; local browser files are never uploaded.
- PostgreSQL persistence, Alembic migrations and Redis-backed session/rate-limit state.
- Liveness/readiness endpoints, structured request logs and optional OpenTelemetry tracing.
- Docker Compose development topology and automated engineering checks.

### Intended audience and use cases

**Backend developers** can study a compact FastAPI service with explicit module boundaries, asynchronous persistence, session handling and API contracts.

**Small engineering teams** can evaluate the code as a starting point for a tightly controlled internal profile-management component, provided they review the operational and security requirements before deployment.

**Reviewers and learners** can inspect how an intentionally limited service handles profile/credential separation, administrator invariants, migration discipline and local security checks.

Possible use cases are internal admin tooling, a learning reference for Python service engineering, or a codebase to adapt after a threat-model and product review. They are not a claim of vendor support or production certification.

### What it is not

| Not included today | Why the distinction matters |
| --- | --- |
| Public registration and end-user self-service | All profile routes are administrator-only. |
| MFA, SSO or OIDC | Local administrator authentication is the only built-in login flow. |
| Tenant isolation | The current data model has no organization boundary or tenant query filter. |
| User account recovery | No recovery workflow is implemented. |
| Media uploads and processing workers | The media catalog is read-only; upload is intentionally absent. |
| Production SLOs and managed hosting | The repository does not publish a measured production baseline or hosted service. |

### Product boundaries and future direction

The roadmap proposes a staged decision process: establish operational readiness first; add tenant-aware authorization only when multi-organization demand is proven; add identity lifecycle features only for agreed workflows; and optimize scale only after repeatable measurements. A future media pipeline requires an isolated quarantine/processing design. None of those proposals should be represented as an existing capability.

### Short description for a project listing

> User Service is an administrator-only profile API built with FastAPI, PostgreSQL and Redis. It separates profile records from credentials and roles, exposes an OpenAPI contract, and includes a TypeScript admin console plus a Docker Compose development environment.

### Project links

[Source repository](https://github.com/GolangDeveloperAlmir/services) · [Documentation](index.md) · [API schema](../openapi.yaml) · [Security model](security.md) · [Roadmap](roadmap.md)

---

<a id="russian"></a>
## Русский

### Сервис профилей с осознанно небольшой поверхностью доверия

User Service предоставляет HTTP API и лёгкую веб-панель для администраторов, которым нужно создавать, просматривать, изменять и удалять записи пользовательских профилей. Ключевое проектное решение — разделение: данные профиля, локальные credentials, назначения ролей и временные сессии являются разными частями модели.

Сервис предназначен для контролируемых административных сценариев и инженерного изучения. Он не позиционируется как готовый Identity Provider, SaaS-каталог клиентов или production-развёртывание «под ключ».

### Ценность продукта

| Принцип | Практическое значение |
| --- | --- |
| Узкий scope | Граница продукта — CRUD профилей; расширение identity требует отдельного решения. |
| Явная авторизация | Каждый endpoint профилей требует активного администратора. |
| Целостность данных | Нормализованный уникальный email, UUID и ограниченная детерминированная пагинация. |
| Fail closed | Отсутствие или некорректность credentials, ролей, сессий и зависимостей не открывает доступ. |
| Наблюдаемая эксплуатация | Compose-топология, health checks, JSON request logs и опциональные traces. |
| Видимый контракт | FastAPI генерирует OpenAPI, а его валидация входит в проверки разработки. |

### Что доступно сейчас

- Локальный вход и выход администратора с короткоживущим непрозрачным bearer-токеном.
- Хеширование паролей Argon2id и защищённая смена пароля.
- Назначение и отзыв роли администратора с повторной проверкой пароля, audit-событиями и защитой последнего активного администратора.
- Создание, получение списка, чтение, обновление и удаление профилей только администраторами.
- TypeScript-панель с тем же origin; токен хранится только в памяти вкладки.
- Read-only каталог изображений и аудио, подготовленных оператором; локальные файлы браузера не загружаются на сервер.
- PostgreSQL, миграции Alembic и Redis для сессий/счётчиков ограничений.
- Liveness/readiness endpoints, структурированные request logs и опциональная OpenTelemetry-трассировка.
- Docker Compose для разработки и автоматизированные инженерные проверки.

### Для кого предназначен проект

**Backend-разработчики** могут изучить компактный FastAPI-сервис с явными границами модулей, асинхронным доступом к данным, управлением сессиями и API-контрактами.

**Небольшие инженерные команды** могут оценить код как основу контролируемого внутреннего инструмента управления профилями, но перед эксплуатацией обязаны проверить требования к безопасности и инфраструктуре.

**Ревьюеры и изучающие backend** могут посмотреть, как ограниченный сервис разделяет профиль и credentials, защищает инварианты администратора и организует миграции и локальные проверки.

Возможные сценарии — внутренний admin-инструмент, учебная база по инженерии Python-сервисов или кодовая основа для адаптации после анализа угроз и требований. Это не обещание поддержки поставщика и не сертификат production-готовности.

### Чего пока нет

| Не входит в текущую реализацию | Почему это важно |
| --- | --- |
| Публичная регистрация и self-service | Все маршруты профилей доступны только администраторам. |
| MFA, SSO или OIDC | Встроен только локальный вход администратора. |
| Изоляция арендаторов | В текущей модели нет границы организации и tenant-фильтров запросов. |
| Восстановление аккаунта | Workflow восстановления не реализован. |
| Загрузка медиа и worker обработки | Каталог read-only, endpoint загрузки намеренно отсутствует. |
| Production SLO и managed hosting | Нет опубликованного измеренного production baseline или размещённого сервиса. |

### Границы продукта и развитие

Roadmap предлагает последовательность решений: сначала эксплуатационная готовность; затем tenant-aware авторизация только при подтверждённой потребности в нескольких организациях; далее identity-функции только под согласованные сценарии; оптимизация масштаба только после воспроизводимых измерений. Будущая загрузка медиа требует отдельной изолированной схемы карантина и обработки. Ни одно из этих предложений не является действующей функцией.

### Краткое описание проекта

> User Service — административный API профилей на FastAPI, PostgreSQL и Redis. Он отделяет записи профилей от credentials и ролей, публикует OpenAPI-контракт и включает TypeScript-панель администратора и Docker Compose-окружение для разработки.

### Ссылки

[Репозиторий](https://github.com/GolangDeveloperAlmir/services) · [Индекс документации](index.md) · [API-схема](../openapi.yaml) · [Модель безопасности](security.md) · [План развития](roadmap.md)
