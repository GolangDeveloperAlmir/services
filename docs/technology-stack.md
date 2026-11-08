# Technology stack and engineering decisions

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Status:** current stack inventory as checked on 2026-11-08.

<a id="english"></a>
## English

### Runtime and application

| Technology | Current role | Why it is used | Benefits | Trade-offs / risks | Alternatives |
| --- | --- | --- | --- | --- | --- |
| Python 3.14+ | Application runtime | One language for service, tools and tests | Readable domain code; mature async ecosystem | Runtime upgrades can expose dependency incompatibilities | Go, Java/Kotlin, .NET, Node.js |
| FastAPI | HTTP application and OpenAPI source | Typed contracts and dependency injection | Schema generation; async support; familiar HTTP model | Framework conventions can leak into domain layers; generated schema needs review | Starlette directly, Django REST Framework, Litestar |
| Starlette | ASGI foundation | Middleware, routing and ASGI primitives | Small standards-based foundation | Behaviour follows FastAPI/Starlette compatibility | Pure ASGI app, another ASGI framework |
| Hypercorn | ASGI server | HTTP/2 and TLS-capable direct run path | ASGI and ALPN support | Additional component to configure and patch | Uvicorn, Daphne, Gunicorn ASGI workers |
| Pydantic v2 + pydantic-settings | Validation and configuration | Typed schemas and startup settings validation | Clear validation rules and useful errors | Validation is not authorization; defaults need review | msgspec, attrs/dataclasses plus custom validation |
| Standard-library logging | Application log API | Avoids an unnecessary logging framework | Low dependency count; project-owned JSON formatter | Advanced context propagation and sinks need extra design | structlog, loguru, platform logging |

### Persistence, identity and security

| Technology | Current role | Why it is used | Benefits | Trade-offs / risks | Alternatives |
| --- | --- | --- | --- | --- | --- |
| PostgreSQL 16 (Compose image) | Authoritative relational store | Profiles, credentials, roles and audit records need transactions and constraints | Constraints, transactions, mature operations | Backups, upgrades, TLS and pool capacity remain operator responsibilities | MySQL, CockroachDB, managed PostgreSQL |
| SQLAlchemy async 2.1+ | ORM and async session layer | Request-scoped database access and repository queries | Mature SQL toolkit; explicit session lifecycle | ORM can hide query cost; async does not automatically make every operation faster | SQLAlchemy Core, SQLModel, direct driver |
| asyncpg 0.30+ | PostgreSQL async driver | Async database I/O under SQLAlchemy | Efficient native async driver | Driver-specific behaviour and pool tuning matter | psycopg 3 async |
| Alembic 1.17+ | Schema migrations | Versioned database evolution | Reviewable, repeatable migration history | Live migrations need expand/backfill/contract discipline | Atlas, Sqitch, framework migrations |
| Redis 7 (Compose image) | Ephemeral sessions and rate-limit counters | Short-lived state, TTL and atomic Lua scripts | Fast lookup and expiry | Not the source of truth; availability and memory limits matter | PostgreSQL sessions, Valkey, managed Redis |
| argon2-cffi | Password hashing | Argon2id password verifier | Memory-hard hashing; rehash support | CPU/RAM cost requires operational tuning | scrypt, bcrypt; PBKDF2 only for specific compatibility/compliance requirements |
| secrets + hashlib | Token creation and derived session keys | Secure random opaque tokens; no plaintext token storage | Standard library; small trusted surface | Expiry and revocation remain application responsibilities | Dedicated identity provider |

### Frontend and delivery

| Technology | Current role | Why it is used | Benefits | Trade-offs / risks | Alternatives |
| --- | --- | --- | --- | --- | --- |
| TypeScript 5.9.3 | Admin console source | Typed interaction without a large UI framework | Small dependency footprint; compile-time checks | The project owns DOM state, accessibility and component patterns | React, Vue, Svelte |
| HTML and CSS | Console presentation | Compact same-origin interface | Minimal runtime and build complexity | Styling and interaction conventions need discipline | Component framework, design system |
| Nginx 1.28 Alpine (validation/config) | TLS ingress and reverse proxy in Compose | Central TLS boundary and private upstream network | Mature proxy; simple local topology | Proxy headers and TLS settings are security-sensitive | Caddy, Envoy, cloud load balancer |
| Docker and Compose | Local multi-service environment and image build | Reproducible developer stack | Isolated networks, service limits and repeatable build | Compose alone is not a production orchestrator | Podman Compose, Kubernetes, managed containers |
| uv | Python dependency/environment management | Locked resolution and repeatable sync | Fast resolver and lockfile workflow | Python support range and lockfile must stay aligned | Poetry, PDM, pip-tools |
| npm lockfile | Frontend dependencies | Reproducible npm ci | Deterministic install | Node/npm versions should be pinned by contributors | pnpm, Yarn |

### Quality, contracts and operations

| Tool | Purpose here | Benefits | Limitations |
| --- | --- | --- | --- |
| pytest | Automated tests | Business, API and security regression checks | Passing tests do not prove production safety |
| Ruff | Python lint and formatting | Fast unified static checks | Project lint policy still needs review |
| Import Linter | Module dependency boundaries | Detects configured forbidden imports | Does not assess all design quality |
| Bandit, pip-audit, detect-secrets | Static security, dependency and secret checks | Catches common classes of accidental risk | Findings need triage; clean scans are not certification |
| CodeQL and Zizmor | Code and workflow analysis | Repository-level static checks | Coverage depends on configuration and supported languages |
| Locust | Local load-test client | Repeatable endpoint workloads and reports | Loopback restriction is intentional; results are not production capacity claims |
| OpenAPI | HTTP API contract | Generated from FastAPI and checked as a snapshot | Must be regenerated when routes/schemas change |
| AsyncAPI schema validation | Event contract state | Makes the current absence of event channels explicit | No broker or application event bus is implemented |
| OpenTelemetry API/SDK + OTLP gRPC | Optional request tracing | Standard trace export when configured | No Prometheus metrics endpoint, dashboards or alert manager are included |

### Why the stack stays small

The current workload is a small administrative API, not a high-volume event platform. PostgreSQL already provides transactional persistence; Redis covers ephemeral session state; FastAPI generates the HTTP contract; and the frontend is a compact same-origin console. Adding Kafka, Celery, Kubernetes, Elasticsearch, a service mesh or a full UI framework before a measured requirement appears would add failure modes, operational cost and security boundaries without demonstrated benefit.

### Replacement decision checklist

Before replacing a component, record the unmet requirement, measured evidence, compatibility and migration plan, failure behaviour, security impact, operational owner, rollback path and reason the alternative is materially better. Update this page and the architecture/API documents in the same change.


### Primary references

- [Python documentation](https://docs.python.org/3/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Pydantic documentation](https://docs.pydantic.dev/latest/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/)
- [Alembic documentation](https://alembic.sqlalchemy.org/en/latest/)
- [Redis documentation](https://redis.io/docs/latest/)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Docker Compose documentation](https://docs.docker.com/compose/)
- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
- [Locust documentation](https://docs.locust.io/)
- [uv documentation](https://docs.astral.sh/uv/)


<a id="russian"></a>
## Русский

### Runtime и приложение

| Технология | Роль сейчас | Причина выбора | Преимущества | Компромиссы и риски | Альтернативы |
| --- | --- | --- | --- | --- | --- |
| Python 3.14+ | Runtime приложения | Один язык для сервиса, инструментов и тестов | Читаемый доменный код, зрелая async-экосистема | Обновление runtime может выявить несовместимость библиотек | Go, Java/Kotlin, .NET, Node.js |
| FastAPI | HTTP-приложение и источник OpenAPI | Типизированные контракты и dependency injection | Генерация схемы, async, привычная HTTP-модель | Конвенции framework могут проникать в домен; schema требует ревью | Starlette напрямую, Django REST Framework, Litestar |
| Starlette | ASGI-основа | Middleware, routing и ASGI-примитивы | Небольшой стандартный фундамент | Поведение зависит от совместимости с FastAPI | Чистое ASGI-приложение, другой ASGI-framework |
| Hypercorn | ASGI-сервер | HTTP/2 и TLS для прямого запуска | Поддержка ASGI и ALPN | Дополнительный компонент для настройки и обновления | Uvicorn, Daphne, Gunicorn ASGI workers |
| Pydantic v2 и pydantic-settings | Валидация и конфигурация | Типизированные схемы и проверка настроек при старте | Ясные правила и ошибки | Валидация не равна авторизации; defaults требуют ревью | msgspec, attrs/dataclasses и своя валидация |
| logging из стандартной библиотеки | API логирования | Не нужен отдельный logging-framework | Мало зависимостей, собственный JSON formatter | Для сложного propagation и sinks нужна дополнительная архитектура | structlog, loguru, logging платформы |

### Хранение, identity и безопасность

| Технология | Роль сейчас | Причина выбора | Преимущества | Компромиссы и риски | Альтернативы |
| --- | --- | --- | --- | --- | --- |
| PostgreSQL 16 (Compose image) | Основная реляционная БД | Профилям, credentials, ролям и audit нужны транзакции и constraints | Ограничения, транзакции, зрелая эксплуатация | Backup, обновления, TLS и ёмкость pool остаются ответственностью оператора | MySQL, CockroachDB, managed PostgreSQL |
| SQLAlchemy async 2.1+ | ORM и async session layer | Request-scoped доступ к БД и repository queries | Зрелый SQL toolkit, явный lifecycle сессии | ORM может скрывать стоимость SQL; async не ускоряет любую операцию автоматически | SQLAlchemy Core, SQLModel, прямой driver |
| asyncpg 0.30+ | Async PostgreSQL driver | Асинхронный DB I/O под SQLAlchemy | Эффективный нативный driver | Важны особенности драйвера и настройки pool | psycopg 3 async |
| Alembic 1.17+ | Миграции схемы | Версионируемое развитие БД | Повторяемая история миграций | Для live-систем нужны expand/backfill/contract-переходы | Atlas, Sqitch, framework migrations |
| Redis 7 (Compose image) | Временные сессии и rate-limit counters | TTL и атомарные Lua-скрипты | Быстрый доступ и expiry | Не источник истины; важны availability и лимиты памяти | Сессии в PostgreSQL, Valkey, managed Redis |
| argon2-cffi | Хеширование паролей | Argon2id password verifier | Memory-hard hashing, rehash support | Требует настройки затрат CPU/RAM | scrypt, bcrypt; PBKDF2 при специальных требованиях |
| secrets + hashlib | Создание токенов и производных ключей сессии | Криптографически случайные opaque-токены без хранения plaintext | Стандартная библиотека, небольшая trusted surface | Expiry и revoke остаются ответственностью приложения | Выделенный identity provider |

### Frontend и доставка

| Технология | Роль сейчас | Причина выбора | Преимущества | Компромиссы и риски | Альтернативы |
| --- | --- | --- | --- | --- | --- |
| TypeScript 5.9.3 | Исходники панели администратора | Типизация без крупного UI-framework | Малый dependency footprint, compile-time checks | DOM-state, accessibility и component patterns контролирует проект | React, Vue, Svelte |
| HTML и CSS | Представление панели | Компактный same-origin интерфейс | Минимум runtime/build-сложности | Нужна дисциплина UI и стилей | Component framework, design system |
| Nginx 1.28 Alpine (конфигурация/проверка) | TLS ingress и reverse proxy в Compose | Центральная TLS-граница и private upstream network | Зрелый proxy, простая локальная топология | Proxy headers и TLS критичны для безопасности | Caddy, Envoy, cloud load balancer |
| Docker и Compose | Локальная multi-service среда и сборка image | Воспроизводимое окружение разработчика | Изолированные сети, лимиты сервисов, повторяемая сборка | Compose сам по себе не production-orchestrator | Podman Compose, Kubernetes, managed containers |
| uv | Управление Python-зависимостями и окружением | Locked resolution и repeatable sync | Быстрый resolver, lockfile workflow | Нужно согласовывать версию Python и lockfile | Poetry, PDM, pip-tools |
| npm lockfile | Frontend dependencies | Воспроизводимый npm ci | Детерминированная установка | Версии Node/npm должны быть зафиксированы разработчиком | pnpm, Yarn |

### Качество, контракты и эксплуатация

| Инструмент | Назначение | Преимущества | Ограничения |
| --- | --- | --- | --- |
| pytest | Автоматические тесты | Регрессии бизнес-логики, API и security | Успешные тесты не доказывают production-безопасность |
| Ruff | Python lint и форматирование | Быстрые унифицированные проверки | Политика lint всё равно требует ревью |
| Import Linter | Границы зависимостей модулей | Находит заданные запрещённые импорты | Не оценивает качество дизайна целиком |
| Bandit, pip-audit, detect-secrets | Security, dependency и secret checks | Ловит распространённые классы случайных рисков | Результаты требуют триажа; чистый scan не является сертификацией |
| CodeQL и Zizmor | Анализ кода и workflows | Статические проверки репозитория | Покрытие зависит от конфигурации и поддержки языков |
| Locust | Локальный load-test клиент | Повторяемые сценарии нагрузки и отчёты | Loopback-ограничение намеренно; результаты не доказывают production capacity |
| OpenAPI | HTTP API contract | Генерируется FastAPI и проверяется как snapshot | Обновлять после изменения маршрутов/схем |
| AsyncAPI schema validation | Состояние event contract | Явно фиксирует отсутствие event channels | Broker и прикладной event bus не реализованы |
| OpenTelemetry API/SDK + OTLP gRPC | Опциональная трассировка | Стандартный экспорт traces при настройке | Нет Prometheus metrics endpoint, dashboards или alert manager |

### Почему стек остаётся небольшим

Текущая задача — небольшой административный API, а не высоконагруженная event-платформа. PostgreSQL уже обеспечивает транзакционное хранение; Redis отвечает за временные сессии; FastAPI генерирует HTTP-контракт; frontend — компактная same-origin панель. Kafka, Celery, Kubernetes, Elasticsearch, service mesh или полноценный UI-framework без измеренного требования добавили бы новые отказы, стоимость эксплуатации и границы доверия без доказанной пользы.

### Чек-лист замены

Перед заменой компонента зафиксируйте невыполненное требование, измеримые доказательства, совместимость и план миграции, поведение при отказе, влияние на безопасность, владельца эксплуатации, путь rollback и конкретное преимущество альтернативы. Обновите эту страницу, архитектуру и API-документацию в том же изменении.


### Основные первоисточники

- [Документация Python](https://docs.python.org/3/)
- [Документация FastAPI](https://fastapi.tiangolo.com/)
- [Документация Pydantic](https://docs.pydantic.dev/latest/)
- [Документация PostgreSQL](https://www.postgresql.org/docs/current/)
- [Документация SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Документация Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Документация Redis](https://redis.io/docs/latest/)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Документация Docker Compose](https://docs.docker.com/compose/)
- [Документация OpenTelemetry](https://opentelemetry.io/docs/)
- [Документация Locust](https://docs.locust.io/)
- [Документация uv](https://docs.astral.sh/uv/)
