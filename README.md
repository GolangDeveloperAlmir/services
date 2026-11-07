# User Service

## Русский

User Service — FastAPI-сервис профилей с локальной аутентификацией
администраторов, PostgreSQL, Redis-сессиями и HTTPS/HTTP2. Все CRUD-маршруты
профилей требуют активную роль `admin`. Это не публичная identity-платформа:
MFA, SSO/OIDC, tenant isolation и пользовательское самообслуживание не входят
в текущий scope.

### Быстрый старт

Нужны Python 3.14+, [`uv`](https://docs.astral.sh/uv/), Docker и Docker
Compose. Создайте локальный env-файл из шаблона, установите свои случайные
пароли (только alphanumeric для удобной сборки URL) и выпустите локальный
self-signed сертификат:

```sh
cp -n .env.example .env
# Замените POSTGRES_PASSWORD и REDIS_PASSWORD уникальными локальными значениями.
make dev-certs
make up
```

Локальный API: `https://localhost:8000`; `/docs`, `/openapi.json` и `/redoc`
доступны только через HTTPS. Браузер будет предупреждать о self-signed
сертификате — это ожидаемо только для разработки. Не используйте его в
production.

Создайте первого администратора после старта стека:

```sh
docker compose exec app python -m app.auth.cli bootstrap-admin
```

CLI интерактивно запросит email и пароль без отображения ввода. Bootstrap
работает только до появления первой admin-роли. Не передавайте пароли как
аргументы командной строки.

### Конфигурация и доступ

Обязательные параметры: `DATABASE_URL`, `REDIS_URL`, `APP_ALLOWED_HOSTS`,
`APP_ENV`. Production требует `APP_ENV=production`, `rediss://`, TLS в
PostgreSQL URL и явные non-loopback hosts. Значения и лимиты перечислены в
[документе безопасности](docs/security.md).

Вход выполняется через `POST /auth/login`; ответ содержит короткоживущий
opaque bearer-токен. Передавайте его как `Authorization: Bearer ...`.
Маршруты `/users` закрыты для неаутентифицированных и не-admin пользователей.
Пароль можно сменить через `POST /auth/password`; отзыв/назначение admin
требуют повторной проверки пароля.

### CRUD профилей

`POST /users`, `GET /users`, `GET /users/{id}`, `PATCH /users/{id}` и
`DELETE /users/{id}` доступны только активному администратору. Создание
профиля не создаёт пароль, credential или admin-роль. Email нормализуется
перед проверкой уникальности и сохранением; дубликат возвращает `409`,
отсутствующий UUID — `404`. Список ограничен 100 записями за страницу и
сортируется по времени создания от новых к старым. PATCH принимает только
переданные ненулевые поля `email`, `full_name`, `is_active`.

Контракт запросов, ошибок и правила защиты профиля описаны в
[документации API](docs/api.md).

### Разработка и проверки

```sh
uv sync --locked --all-groups
make check
make validate-specs
make architecture
```

Для локального запуска без Compose: скопируйте `.env.example` в `.env`,
настройте PostgreSQL и Redis, выполните `make dev-certs`,
`uv run alembic upgrade head`, затем `make run`. Все проверки безопасности и
настройка локальных секретов описаны в [docs/security.md](docs/security.md).

Нагрузочные тесты разрешены только на localhost/loopback и disposable `_test`
базе. Они требуют `PERF_AUTH_TOKEN`; инструкция и пределы есть в
[docs/performance.md](docs/performance.md).

### Документация

Начните с [индекса документации](docs/index.md): [архитектура](docs/architecture.md),
[модель данных и ER-диаграммы](docs/data-model.md), [HTTP API](docs/api.md),
[безопасность](docs/security.md), [наблюдаемость](docs/observability.md),
[нагрузочные проверки](docs/performance.md), [обзор продукта](docs/product-overview.md),
[участие в разработке](CONTRIBUTING.md) и [политика раскрытия](SECURITY.md).

## English

User Service is a FastAPI profile service with local administrator
authentication, PostgreSQL, Redis-backed sessions, and HTTPS/HTTP2. Every
profile CRUD route requires an active `admin` role. It is not a public identity
platform: MFA, SSO/OIDC, tenant isolation, and end-user self-service are out of
scope.

### Quick start

Requirements: Python 3.14+, [`uv`](https://docs.astral.sh/uv/), Docker, and
Docker Compose. Copy the environment template, set unique random local
passwords (alphanumeric values simplify the database URL), and create a local
self-signed certificate:

```sh
cp -n .env.example .env
# Replace POSTGRES_PASSWORD and REDIS_PASSWORD with unique local values.
make dev-certs
make up
```

Local API: `https://localhost:8000`; `/docs`, `/openapi.json`, and `/redoc`
are HTTPS-only. Browsers will warn about the self-signed certificate; that is
expected only in development. Never use it in production.

Create the first administrator after the stack is ready:

```sh
docker compose exec app python -m app.auth.cli bootstrap-admin
```

The CLI prompts for the email and password without echoing the password.
Bootstrap works only until an administrator role exists. Never pass passwords
as command-line arguments.

### Configuration and access

Required settings are `DATABASE_URL`, `REDIS_URL`, `APP_ALLOWED_HOSTS`, and
`APP_ENV`. Production requires `APP_ENV=production`, `rediss://`, TLS in the
PostgreSQL URL, and explicit non-loopback hosts. See
[security documentation](docs/security.md) for all settings and controls.

Authenticate with `POST /auth/login`; the response contains a short-lived
opaque bearer token. Send it as `Authorization: Bearer ...`. `/users` routes
reject unauthenticated and non-admin callers. Change a password at
`POST /auth/password`; administrator role changes require password
reauthentication.

### Profile CRUD

`POST /users`, `GET /users`, `GET /users/{id}`, `PATCH /users/{id}`, and
`DELETE /users/{id}` are restricted to active administrators. Creating a
profile does not create a password, local credential, or admin role. Email is
normalized before uniqueness checks and persistence; duplicates return `409`,
and unknown UUIDs return `404`. Listing is capped at 100 records per page and
ordered newest first. PATCH accepts only supplied, non-null `email`,
`full_name`, and `is_active` fields.

See the [API documentation](docs/api.md) for request contracts, errors, and
profile safety rules.

### Development and checks

```sh
uv sync --locked --all-groups
make check
make validate-specs
make architecture
```

For a non-Compose local run, copy `.env.example` to `.env`, configure
PostgreSQL/Redis, run `make dev-certs` and `uv run alembic upgrade head`, then
`make run`. Security checks and local secret handling are documented in
[docs/security.md](docs/security.md).

Load tests are restricted to localhost/loopback and a disposable `_test`
database. They require `PERF_AUTH_TOKEN`; see
[docs/performance.md](docs/performance.md) for setup and limits.

### Documentation

Start at the [documentation index](docs/index.md): [architecture](docs/architecture.md),
[data model and ER diagrams](docs/data-model.md), [HTTP API](docs/api.md),
[security](docs/security.md), [observability](docs/observability.md),
[load testing](docs/performance.md), [product overview](docs/product-overview.md),
[contributing](CONTRIBUTING.md), and [responsible disclosure](SECURITY.md).
