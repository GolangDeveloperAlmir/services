# HTTP API reference

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Status:** current API surface. The generated schema is the contract source to verify before a release.

<a id="english"></a>
## English

### Base URL and interactive schema

In the local Compose environment, the service is available at <code>https://127.0.0.1:8000</code>. Nginx terminates TLS and forwards requests to the private application network; the API container has no published host port. Cleartext HTTP is rejected except for loopback health checks.

| Resource | Path | Notes |
| --- | --- | --- |
| Web console | <code>/</code> | Same-origin administrator UI |
| OpenAPI JSON | <code>/openapi.json</code> | Generated from the FastAPI application |
| Swagger UI | <code>/docs</code> | HTTPS only |
| ReDoc | <code>/redoc</code> | HTTPS only |

### Authentication endpoints

| Method | Path | Purpose | Success |
| --- | --- | --- | --- |
| POST | <code>/auth/login</code> | Authenticate an active local administrator | 200 |
| POST | <code>/auth/logout</code> | Revoke the current bearer session | 204 |
| GET | <code>/auth/me</code> | Return the authenticated administrator | 200 |
| POST | <code>/auth/password</code> | Change password after current-password verification | 204 |
| POST | <code>/auth/admins/{target_user_id}</code> | Grant admin after reauthentication | 204 |
| POST | <code>/auth/admins/{target_user_id}/revoke</code> | Revoke admin after reauthentication | 204 |
| GET | <code>/auth/audit</code> | Read recent security events; limit 1–500 | 200 |

Login returns an opaque bearer token and <code>expires_in</code>. Send the token as <code>Authorization: Bearer &lt;token&gt;</code>. Tokens are short-lived; never log them or store them in browser local storage. Password fields reject unknown JSON fields. A failed or limited login returns 401 or 429 respectively; rate-limit responses include <code>Retry-After</code>.

The admin-only <code>GET /auth/audit</code> endpoint returns recent events newest first. It includes authentication and administrator lifecycle events, as well as profile mutation events: <code>user.profile.created</code>, <code>user.profile.updated</code> and <code>user.profile.deleted</code>. Each event records the acting administrator, target profile when it still exists, request source IP when available, and timestamp. The endpoint does not expose passwords, bearer tokens or submitted profile values.

### Profile endpoints

All profile routes require a valid session for an active <code>admin</code> account. There is no public registration or non-admin access.

| Method | Path | Purpose | Success |
| --- | --- | --- | --- |
| POST | <code>/users</code> | Create a profile, not credentials or an administrator account | 201 |
| GET | <code>/users</code> | List profiles; offset ≥ 0, limit 1–100, newest first | 200 |
| GET | <code>/users/{user_id}</code> | Read profile by UUID | 200 |
| PATCH | <code>/users/{user_id}</code> | Update supplied fields | 200 |
| DELETE | <code>/users/{user_id}</code> | Delete profile | 204 |

Create requires a valid email and a trimmed <code>full_name</code> of 1–120 characters. PATCH accepts <code>email</code>, <code>full_name</code> and <code>is_active</code>; at least one field must be supplied and fields cannot be null. Unknown fields are rejected.

Email is case-folded before persistence and uniqueness checks. Duplicate addresses return 409; unknown UUIDs return 404. Listing uses <code>created_at DESC, id ASC</code> with bounded pagination. The database unique constraint remains the final guard against concurrent duplicate writes.

Creating a profile inserts only a profile row. It does not create credentials, enable login or assign a role. Administrator access is provisioned separately through the protected admin-management flow. An administrator cannot disable or delete their own account, and an operation that would leave no active administrator is rejected. Deactivation/deletion of an administrator invalidates relevant sessions.

Create request:

~~~json
{
  "email": "person@example.com",
  "full_name": "Example Person"
}
~~~

PATCH request:

~~~json
{
  "full_name": "Updated Name"
}
~~~

Empty PATCH bodies, explicit null values, unknown fields and invalid pagination are rejected with 422. Delete returns an empty 204 response.

### Curated media endpoints

| Method | Path | Purpose | Success |
| --- | --- | --- | --- |
| GET | <code>/media/catalog</code> | List curated background and audio metadata | 200 |
| GET | <code>/media/{media_id}</code> | Stream one item by opaque ID | 200 |

The catalog is operator-managed and read-only. It includes regular files under <code>media/backgrounds/{city,nature,ocean,beach,anime}</code> and <code>media/music/ambient</code>. Supported extensions are JPG/JPEG, PNG, WebP, MP3, OGG and WAV; each file is limited to 15 MiB and the catalog to 500 eligible files. Symlinks, unsupported extensions and files outside fixed directories are excluded. The API does not scan or transcode operator-provided files. There is no upload endpoint.

Catalog and media requests require an active administrator session and HTTPS. An unavailable catalog root or an excessive file count returns 503; unknown media IDs return 404. A local file selected in the browser is not sent to the server.

### Health endpoints

| Method | Path | Meaning |
| --- | --- | --- |
| GET | <code>/health/live</code> | Liveness probe |
| GET | <code>/health/ready</code> | Readiness probe for required dependencies |

Health endpoints are intended for infrastructure checks. They are not substitutes for an end-to-end user journey or an externally monitored availability SLO.

### Common status codes

| Status | Meaning |
| --- | --- |
| 200 / 201 | Successful read/update or profile creation |
| 204 | Successful operation with no response body |
| 401 | Missing/invalid session or credentials |
| 403 | Authenticated identity lacks administrator authorization |
| 404 | Profile or media identifier not found |
| 409 | Duplicate email or administrator invariant would be violated |
| 422 | Invalid payload, UUID or query parameter |
| 426 | HTTPS is required |
| 429 | Login rate limit exceeded; check <code>Retry-After</code> |
| 503 | Readiness dependency or media catalog unavailable |

### Contract verification

FastAPI generates the committed [OpenAPI snapshot](../openapi.yaml). After changing routes or schemas, run <code>make openapi</code> and <code>make validate-specs</code>, then review the resulting diff. The bundled AsyncAPI validation currently records that no event-driven channels are implemented.

---

<a id="russian"></a>
## Русский

### Базовый URL и интерактивная схема

В локальном Compose-окружении сервис доступен по адресу <code>https://127.0.0.1:8000</code>. Nginx завершает TLS и передаёт запросы во внутреннюю сеть приложения; API-контейнер не публикует host-порт. Обычный HTTP отклоняется, кроме loopback health checks.

| Ресурс | Путь | Примечание |
| --- | --- | --- |
| Веб-панель | <code>/</code> | Same-origin интерфейс администратора |
| OpenAPI JSON | <code>/openapi.json</code> | Генерируется FastAPI |
| Swagger UI | <code>/docs</code> | Только HTTPS |
| ReDoc | <code>/redoc</code> | Только HTTPS |

### Маршруты аутентификации

| Метод | Путь | Назначение | Успех |
| --- | --- | --- | --- |
| POST | <code>/auth/login</code> | Аутентификация активного локального администратора | 200 |
| POST | <code>/auth/logout</code> | Отзыв текущей bearer-сессии | 204 |
| GET | <code>/auth/me</code> | Получение текущего администратора | 200 |
| POST | <code>/auth/password</code> | Смена пароля после проверки текущего | 204 |
| POST | <code>/auth/admins/{target_user_id}</code> | Назначение admin после повторной аутентификации | 204 |
| POST | <code>/auth/admins/{target_user_id}/revoke</code> | Отзыв admin после повторной аутентификации | 204 |
| GET | <code>/auth/audit</code> | Получение последних security events; limit 1–500 | 200 |

Вход возвращает непрозрачный bearer-токен и <code>expires_in</code>. Передавайте его как <code>Authorization: Bearer &lt;token&gt;</code>. Токены короткоживущие: не записывайте их в логи или browser local storage. Поля паролей отклоняют неизвестные JSON-поля. Неуспешный вход возвращает 401, превышение лимита — 429 с заголовком <code>Retry-After</code>.

Admin-only endpoint <code>GET /auth/audit</code> возвращает последние события в порядке от новых к старым. Помимо аутентификации и управления администраторами, он включает изменения профилей: <code>user.profile.created</code>, <code>user.profile.updated</code> и <code>user.profile.deleted</code>. Каждая запись содержит инициатора, целевой профиль, пока он существует, IP запроса при его наличии и время события. Пароли, bearer-токены и переданные значения полей профиля в журнал не попадают.

### Маршруты профилей

Все маршруты профилей требуют действующую сессию активного пользователя с ролью <code>admin</code>. Публичной регистрации и доступа для non-admin нет.

| Метод | Путь | Назначение | Успех |
| --- | --- | --- | --- |
| POST | <code>/users</code> | Создание профиля, но не credentials или administrator account | 201 |
| GET | <code>/users</code> | Список профилей; offset ≥ 0, limit 1–100, сначала новые | 200 |
| GET | <code>/users/{user_id}</code> | Получение профиля по UUID | 200 |
| PATCH | <code>/users/{user_id}</code> | Обновление переданных полей | 200 |
| DELETE | <code>/users/{user_id}</code> | Удаление профиля | 204 |

Для создания требуется корректный email и обрезанный по краям <code>full_name</code> длиной 1–120 символов. PATCH принимает <code>email</code>, <code>full_name</code> и <code>is_active</code>; нужно передать хотя бы одно поле, а значения null запрещены. Неизвестные поля отклоняются.

Email приводится к case-folded виду перед сохранением и проверкой уникальности. Дубликат возвращает 409, неизвестный UUID — 404. Список сортируется по <code>created_at DESC, id ASC</code> с ограниченной пагинацией. Уникальный constraint БД остаётся последней защитой от конкурентной записи дубликатов.

Создание профиля добавляет только строку профиля. Credentials, право входа и роль не создаются. Доступ администратора назначается отдельно через защищённое управление ролями. Администратор не может отключить или удалить собственную учётную запись; операция, после которой не останется активных администраторов, отклоняется. Деактивация/удаление администратора отзывает соответствующие сессии.

Пример создания:

~~~json
{
  "email": "person@example.com",
  "full_name": "Example Person"
}
~~~

Пример PATCH:

~~~json
{
  "full_name": "Updated Name"
}
~~~

Пустой PATCH, явный null, неизвестные поля и неверная пагинация отклоняются с 422. DELETE возвращает пустой ответ 204.

### Маршруты каталога медиа

| Метод | Путь | Назначение | Успех |
| --- | --- | --- | --- |
| GET | <code>/media/catalog</code> | Список метаданных фонов и аудио | 200 |
| GET | <code>/media/{media_id}</code> | Потоковая выдача по непрозрачному ID | 200 |

Каталог доступен только для чтения и управляется оператором. Он включает обычные файлы в <code>media/backgrounds/{city,nature,ocean,beach,anime}</code> и <code>media/music/ambient</code>. Поддерживаются JPG/JPEG, PNG, WebP, MP3, OGG и WAV; до 15 MiB на файл и до 500 подходящих файлов в каталоге. Символические ссылки, неподдерживаемые расширения и файлы вне фиксированных каталогов исключаются. API не сканирует и не перекодирует файлы оператора. Endpoint загрузки отсутствует.

Запросы к каталогу и медиа требуют активную сессию администратора и HTTPS. Недоступный корень каталога или превышение лимита файлов дают 503; неизвестный media ID — 404. Локальный файл, выбранный в браузере, на сервер не отправляется.

### Health endpoints

| Метод | Путь | Значение |
| --- | --- | --- |
| GET | <code>/health/live</code> | Liveness probe |
| GET | <code>/health/ready</code> | Readiness probe обязательных зависимостей |

Health endpoints предназначены для инфраструктурных проверок. Они не заменяют end-to-end пользовательский сценарий или внешний SLO мониторинга доступности.

### Основные status codes

| Статус | Значение |
| --- | --- |
| 200 / 201 | Успешное чтение/обновление или создание профиля |
| 204 | Успешная операция без тела ответа |
| 401 | Сессия отсутствует/некорректна или credentials неверны |
| 403 | У аутентифицированного субъекта нет прав администратора |
| 404 | Профиль или media ID не найден |
| 409 | Email занят или нарушится инвариант администратора |
| 422 | Некорректный payload, UUID или query-параметр |
| 426 | Требуется HTTPS |
| 429 | Превышен login rate limit; проверьте <code>Retry-After</code> |
| 503 | Недоступна обязательная зависимость readiness или каталог медиа |

### Проверка контракта

FastAPI генерирует коммитнутый [OpenAPI snapshot](../openapi.yaml). После изменения маршрутов или схем выполните <code>make openapi</code> и <code>make validate-specs</code>, затем проверьте diff. Проверка AsyncAPI пока фиксирует отсутствие реализованных event-driven channels.
