# HTTP API / HTTP API

The API is served over HTTPS at `https://localhost:8000` in the local Compose
environment. OpenAPI JSON is `/openapi.json`, Swagger UI is `/docs`, and ReDoc
is `/redoc`; none is served over cleartext HTTP.

Локальный Compose публикует API по `https://localhost:8000`. OpenAPI JSON
доступен по `/openapi.json`, Swagger UI — `/docs`, ReDoc — `/redoc`; обычный
HTTP не обслуживается.

## Authentication / Аутентификация

| Method | Path | Purpose | Success |
| --- | --- | --- | --- |
| `POST` | `/auth/login` | Authenticate an active local administrator | `200` |
| `POST` | `/auth/logout` | Revoke the current bearer session | `204` |
| `GET` | `/auth/me` | Return the authenticated administrator | `200` |
| `POST` | `/auth/password` | Change password after current-password verification | `204` |
| `POST` | `/auth/admins/{target_user_id}` | Grant admin after reauthentication | `204` |
| `POST` | `/auth/admins/{target_user_id}/revoke` | Revoke admin after reauthentication | `204` |
| `GET` | `/auth/audit` | Read recent security events (limit 1–500) | `200` |

`POST /auth/login` returns an opaque bearer token and `expires_in`; send the
token in `Authorization: Bearer <token>`. Tokens are short-lived and must not
be logged or stored in browser local storage. All authentication endpoints
require HTTPS. Password fields reject unknown JSON fields.

`POST /auth/login` возвращает opaque bearer-токен и `expires_in`; передавайте
его в `Authorization: Bearer <token>`. Токен короткоживущий, его нельзя
логировать или хранить в browser local storage. Все auth endpoints требуют
HTTPS.

## User profiles / Профили пользователей

All profile routes require a valid session for an active `admin` account.
There is no public registration or non-admin access.

Все profile-маршруты требуют действующую сессию активного пользователя с
ролью `admin`. Публичной регистрации и non-admin доступа нет.

| Method | Path | Purpose | Success |
| --- | --- | --- | --- |
| `POST` | `/users` | Create a profile, not credentials or an admin account | `201` |
| `GET` | `/users` | List profiles (`offset >= 0`, `1 <= limit <= 100`), newest first | `200` |
| `GET` | `/users/{user_id}` | Read profile by UUID | `200` |
| `PATCH` | `/users/{user_id}` | Update provided fields | `200` |
| `DELETE` | `/users/{user_id}` | Delete profile | `204` |

`UserCreate` requires a valid email and `full_name` of 1–120 trimmed
characters. PATCH accepts `email`, `full_name`, and `is_active`; at least one
field must be provided and fields cannot be null. Extra fields are rejected.
Deactivating or deleting an administrator is denied if it would leave no
active administrator; an administrator cannot disable/delete their own
account. Email addresses are normalized consistently for creation, update, and
authentication. Duplicate email addresses return `409`; unknown profile IDs
return `404`. Listing is ordered by descending creation time with UUID as a
stable tie-breaker.

Creating a profile creates only a `users` row. It does not create local
credentials, enable login, or assign a role. Administrator access is provisioned
separately through the protected admin-management flow. Email is case-folded
before persistence and duplicate checks; the database unique constraint remains
the final guard against concurrent duplicate creates/updates.

Create request:

```json
{
  "email": "person@example.com",
  "full_name": "Example Person"
}
```

PATCH request:

```json
{
  "full_name": "Updated Name"
}
```

An empty PATCH body, explicit `null`, an unknown field, or an out-of-range
pagination value is rejected with `422`. Profile creation and update return
`409` on duplicate email. Deletion returns an empty `204` response. Deactivating
or deleting an admin invalidates its sessions; admin self-deactivation,
self-deletion, and loss of the last active admin are rejected with `409`.

`UserCreate` требует корректный email и `full_name` длиной 1–120 символов
после обрезки пробелов. PATCH принимает `email`, `full_name` и `is_active`;
нужно передать хотя бы одно поле, `null` запрещён. Неизвестные поля
отклоняются. Последнего активного администратора нельзя отключить или
удалить; администратор не может отключить или удалить собственный аккаунт.
Email нормализуется одинаково при создании, обновлении и аутентификации.
Дубликат email возвращает `409`, неизвестный UUID профиля — `404`. Список
сортируется по времени создания от новых к старым, UUID разрешает совпадения.

Создание профиля добавляет только запись `users`: пароль, локальный credential
и роль при этом не создаются. Административный доступ выдаётся отдельно через
защищённое управление ролями. Email приводится к case-folded виду перед
сохранением и проверкой уникальности; ограничение БД защищает также от
конкурентного создания/обновления дубликатов.

Пример создания:

```json
{
  "email": "person@example.com",
  "full_name": "Example Person"
}
```

Пустой PATCH, явный `null`, неизвестное поле и неверная пагинация отклоняются
с `422`. Дубликат email при создании/обновлении возвращает `409`. Удаление
возвращает пустой ответ `204`. Деактивация или удаление администратора
инвалидирует его сессии; self-deactivation, self-delete и потеря последнего
активного администратора отклоняются с `409`.

## Errors / Ошибки

| Status | Meaning |
| --- | --- |
| `401` | Missing/invalid session or credentials |
| `403` | Authenticated identity lacks admin authorization |
| `404` | User UUID not found |
| `409` | Duplicate email or administrator invariant would be violated |
| `422` | Invalid payload, UUID, or query parameter |
| `426` | HTTPS is required |
| `429` | Login rate limit exceeded; check `Retry-After` |
| `503` | Readiness check reports unavailable dependencies |

| Статус | Значение |
| --- | --- |
| `401` | Нет сессии или credentials неверны |
| `403` | У аутентифицированного пользователя нет прав admin |
| `404` | UUID пользователя не найден |
| `409` | Email занят или нарушится инвариант администратора |
| `422` | Некорректный payload, UUID или query-параметр |
| `426` | Требуется HTTPS |
| `429` | Превышен login rate limit; смотрите `Retry-After` |
| `503` | Проверка readiness обнаружила недоступную зависимость |

The generated [OpenAPI snapshot](../openapi.yaml) is validated against the
FastAPI application by `make validate-specs`.
