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

Локальный API: `https://127.0.0.1:8000`; `/docs`, `/openapi.json` и `/redoc`
доступны только через HTTPS. Браузер будет предупреждать о self-signed
сертификате — это ожидаемо только для разработки. Не используйте его в
production. TLS завершается на Nginx; backend, PostgreSQL и Redis не
публикуются напрямую на host. Приложение получает HTTP только из внутренней
Docker-сети. Этот Compose рассчитан на локальную разработку, а не на
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
opaque bearer-токен. Передавайте его в заголовке
`Authorization: Bearer <token>`.
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

### Веб-панель

После запуска стека откройте `https://127.0.0.1:8000/` и войдите под активной
учётной записью администратора. Панель позволяет просматривать список
профилей с постраничной навигацией, искать на загруженной странице, создавать
и редактировать профиль, менять его активность и удалять его. Поиск работает
только по текущей странице; сам API возвращает не более 25 записей на страницу
в интерфейсе. Создание профиля не создаёт credentials или права входа.

Bearer-токен хранится только в памяти открытой вкладки и не записывается в
local storage; после перезагрузки страницы нужно войти повторно. Для локальной
работы без Docker соберите TypeScript перед запуском: `make frontend-install`
и `make frontend-build`. Docker image собирает frontend автоматически.

### Фоны и музыка

Панель предлагает анимированные CSS-заглушки для мегаполиса, природы, океана,
пляжа и аниме-вдохновлённой сцены, переключатель RU/EN и управление анимацией.
Реальных изображений/музыки в репозитории нет. Администратор может выбрать
защищённый API-каталог или файл из браузера. Локальные файлы не отправляются
на сервер; API-каталог доступен только авторизованным администраторам.

Каталог оператора находится в `media/backgrounds/{city,nature,ocean,beach,anime}`
и `media/music/ambient`; поддерживаются JPG/JPEG, PNG, WebP, MP3, OGG и WAV,
до 15 MiB на файл. Добавляйте только медиа с проверенными правами использования.
Endpoint загрузки и worker обработки пользовательских файлов пока отключены;
не подключайте недоверенный каталог на запись. Ограничения, поведение и
будущая спецификация обработки описаны в [docs/media.md](docs/media.md) и
[docs/roadmap/05-media-pipeline.md](docs/roadmap/05-media-pipeline.md).

### Разработка и проверки

```sh
uv sync --locked --all-groups
make frontend-install
make frontend-build
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
[безопасность](docs/security.md), [медиа](docs/media.md),
[наблюдаемость](docs/observability.md),
[нагрузочные проверки](docs/performance.md), [обзор продукта](docs/product-overview.md),
[план развития и будущие ТЗ](docs/roadmap.md),
[участие в разработке](CONTRIBUTING.md) и [политика раскрытия](SECURITY.md).

### Лицензия и поддержка

Проект распространяется по собственной лицензии
[Almir Open Attribution License (AOAL) 1.0](LICENSE): использование,
изменение, коммерческое распространение и форки разрешены при сохранении
атрибуции автора и ссылки на первоисточник. Учитывайте отдельные лицензии
сторонних компонентов; AOAL является собственной, не стандартной лицензией.
См. также [правила сообщества](CODE_OF_CONDUCT.md),
[поддержку](SUPPORT.md) и [цитирование проекта](CITATION.cff).

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

Local API: `https://127.0.0.1:8000`; `/docs`, `/openapi.json`, and `/redoc`
are HTTPS-only. TLS terminates at Nginx; the backend, PostgreSQL, and Redis
are not published directly to the host. The application receives HTTP only
from the internal Docker network. This Compose stack is for local development,
not production. Browsers will warn about the self-signed certificate; never
use it in production.

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
opaque bearer token. Send it as `Authorization: Bearer <token>`. `/users` routes
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

### Web console

After starting the stack, open `https://127.0.0.1:8000/` and sign in with an
active administrator account. The console lists profiles with pagination,
searches the loaded page, and supports create, edit, activate/deactivate, and
delete actions. Search is limited to the current page; the UI requests up to
25 records per page. Creating a profile does not create credentials or grant
login access.

The bearer token stays in the current tab's memory and is not written to local
storage; re-authenticate after reloading the page. For a non-Docker local run,
build TypeScript with `make frontend-install` and `make frontend-build`. Docker
builds the frontend automatically.

### Backgrounds and music

The console offers animated CSS placeholder scenes for city, nature, ocean,
beach, and anime-inspired styles, a RU/EN language switch, and a motion
control. No actual image or music assets are bundled. Administrators can use
the protected API catalog or choose a browser-local file. Local files are
never uploaded; the API catalog requires administrator authentication.

The operator-managed catalog lives under
`media/backgrounds/{city,nature,ocean,beach,anime}` and `media/music/ambient`.
Supported formats are JPG/JPEG, PNG, WebP, MP3, OGG, and WAV, up to 15 MiB per
file. Add only media with verified usage rights. Upload endpoints and a worker
for user files are not implemented; do not mount an untrusted writable media
directory. See [docs/media.md](docs/media.md) and the future
[media-pipeline specification](docs/roadmap/05-media-pipeline.md).

### Development and checks

```sh
uv sync --locked --all-groups
make frontend-install
make frontend-build
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
[security](docs/security.md), [media](docs/media.md),
[observability](docs/observability.md),
[load testing](docs/performance.md), [product overview](docs/product-overview.md),
[proposed roadmap and future specifications](docs/roadmap.md),
[contributing](CONTRIBUTING.md), and [responsible disclosure](SECURITY.md).

The roadmap is a planning document, not a feature or delivery commitment.
Its detailed technical specifications are currently maintained in Russian.

### License and support

This project is distributed under the custom
[Almir Open Attribution License (AOAL) 1.0](LICENSE). Use, modification,
commercial distribution, and forks are permitted when author attribution and
the original source link are retained. Third-party components may have
separate licenses; AOAL is a custom, non-standard license. See the
[Code of Conduct](CODE_OF_CONDUCT.md),
[support guide](SUPPORT.md), and [citation metadata](CITATION.cff).
