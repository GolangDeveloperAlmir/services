# Обзор продукта / Product overview

## Для клиентов и компаний / For customers and companies

### Управление пользовательскими профилями через API

User Service — компактный HTTPS API для профилей с локальной аутентификацией
администраторов. Он подходит как контролируемый backend-компонент для команд,
которым нужны CRUD-операции с OpenAPI-контрактом, PostgreSQL и контейнерным
локальным окружением. Все операции над профилями доступны только активным
администраторам.

User Service is a focused HTTPS profile API with local administrator
authentication. It can serve as a controlled backend component for teams that
need profile CRUD, an OpenAPI contract, PostgreSQL, and a containerized local
development environment. Profile operations are restricted to active admins.

### Что доступно сегодня / Available today

- REST endpoints for user profiles, including pagination.
- Email format validation, case normalization, and unique-email conflict
  handling (`409` for duplicate addresses).
- UUID identifiers, active flag, and created/updated timestamps.
- Admin-only create/read/list/update/delete workflows; profile creation does
  not grant a login credential or role.
- OpenAPI documentation and generated schema.
- Async Python persistence with PostgreSQL migrations.
- Redis-backed opaque admin sessions, Argon2id password hashes, login
  throttling, and security audit events.
- HTTPS/HTTP2 transport, restrictive host validation, and CI security gates.
- Structured JSON request logs and optional OTLP request tracing.

- REST endpoints для профилей пользователей, включая пагинацию.
- Проверка и нормализация email, обработка конфликтов уникальности (`409`).
- UUID, флаг активности, даты создания и обновления.
- Admin-only операции создания/чтения/списка/изменения/удаления; создание
  профиля не выдаёт credential и роль.
- OpenAPI-документация и генерируемая схема.
- Асинхронный Python backend и миграции PostgreSQL.
- Opaque admin-сессии в Redis, Argon2id-хеши паролей, ограничение частоты
  входа и security audit events.
- HTTPS/HTTP2, строгая проверка host и security gates в CI.
- Структурированные JSON request logs и опциональный OTLP tracing.

### Важно знать / Important limitations

This is an administrative profile API, not a complete IAM/customer identity
platform. It has one built-in admin role and no end-user accounts, MFA,
password-reset workflow, SSO/OIDC, granular permissions, tenant isolation, or
object ownership model. Production operation requires real certificates,
TLS-enabled database/cache, managed secrets, backups, audit retention, and
deployment review. Do not expose it as a general public user-profile API.

Это административный profile API, а не готовая IAM/customer identity
платформа. Реализована только роль admin; нет пользовательских аккаунтов,
MFA, восстановления пароля, SSO/OIDC, granular permissions, tenant isolation
и владения объектами. Production требует настоящих сертификатов,
TLS-enabled БД/кэша, managed secrets, резервных копий, retention audit и
проверки deployment. Не публикуйте сервис как открытый API для всех клиентов.

### Возможное направление развития / Potential roadmap

Subject to customer requirements and security review, the service could evolve
toward organization-scoped accounts, external identity-provider references,
MFA, granular roles, tenant-aware authorization, and managed account recovery.
These are roadmap ideas, not current product capabilities or delivery
commitments.

С учётом требований клиентов и security review продукт можно развивать в
сторону организаций, внешних identity-provider, ролей и разрешений,
административных workflows, audit events и подтверждения аккаунтов. Это идеи
развития, а не реализованные функции или обещание сроков.

### Короткое описание / Short description

**RU:** HTTPS API для управления профилями с локальными admin-аккаунтами,
PostgreSQL и OpenAPI. Подходит для контролируемых внутренних сценариев;
полноценные identity и tenant функции требуют отдельной реализации.

**EN:** An HTTPS profile API with local administrator accounts, PostgreSQL, and
OpenAPI documentation. Intended for controlled internal use; full identity and
tenant features require separate implementation.
