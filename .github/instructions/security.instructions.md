---
name: Security-Critical Changes
description: "Use when changing authentication, authorization, security settings, persistence, migrations, proxy or TLS configuration, deployment, media access, or security tests."
applyTo:
  - "app/auth/**"
  - "app/core/config.py"
  - "app/db/**"
  - "app/main.py"
  - "app/media/**"
  - "migrations/**"
  - "docker-compose*.yml"
  - "Dockerfile"
  - "nginx/**"
  - "tests/test_security_controls.py"
---

# Security-critical changes

> **Language / Язык:** [English](#english) · [Русский](#russian)

<a id="english"></a>
## English

Read [docs/security.md](../../docs/security.md) and the existing tests before changing security-sensitive behaviour. Implemented controls and documented limitations are the baseline; do not imply the service is a complete identity platform or certified secure.

- Preserve deny-by-default access: every profile route requires an active administrator; PostgreSQL account and role state is authoritative. Redis failure must reject authentication rather than bypass it.
- Preserve the last-active-administrator invariant, password reauthentication for role changes, credential-version checks, session revocation and non-enumerating login failures. Extend tests when changing these paths.
- Never log or return passwords, raw bearer tokens, credentials or request bodies containing secrets. Never pass passwords as CLI arguments or place real secrets in fixtures, examples, snapshots or test output.
- Do not trust arbitrary forwarded headers. Only use explicitly configured proxy IPs; preserve host validation and production TLS checks. Production requires TLS for PostgreSQL and Redis, explicit non-loopback hosts and trusted-proxy configuration.
- Treat development Compose, local passwords and self-signed certificates as development-only. Do not target production or third-party systems. Run provisioning and performance tests only against localhost and a disposable <code>_test</code> database.
- Keep media access admin-only and read-only. User uploads and a processing worker are not implemented. Do not add unsafe writable mounts or broaden supported types/limits without explicit design and tests.
- Review migrations for data loss and operational impact. Never run migrations or destructive commands against a live or unapproved database; do not remove database volumes or existing user data without explicit approval.
- Do not disable or weaken security tests, audit tools, dependency checks or workflow protections to obtain a passing result. Report unresolved findings and validation failures explicitly.

See [architecture](../../docs/architecture.md) for module boundaries and [performance guidance](../../docs/performance.md) for local-only test requirements. Public documentation changes must follow the English-first/Russian-second [documentation standard](../../docs/documentation-standard.md).

---

<a id="russian"></a>
## Русский

Перед изменением поведения, связанного с безопасностью, прочитайте [docs/security.md](../../docs/security.md) и соответствующие тесты. Реализованные контроли и явно описанные ограничения являются исходной точкой; не представляйте сервис как полноценную Identity-платформу или сертифицированное безопасное решение.

- Сохраняйте deny-by-default: каждый маршрут профилей требует активного администратора; PostgreSQL является источником истины для состояния аккаунта и ролей. При отказе Redis аутентификация должна завершаться отказом, а не обходить проверку.
- Сохраняйте инвариант последнего активного администратора, повторную проверку пароля при изменении ролей, проверку credential version, отзыв сессий и защиту от перечисления аккаунтов при входе. При изменении этих путей расширяйте тесты.
- Не записывайте и не возвращайте пароли, сырые bearer-токены, credentials и request bodies с секретами. Не передавайте пароли в аргументах CLI и не помещайте реальные секреты в fixtures, примеры, snapshots или вывод тестов.
- Не доверяйте произвольным forwarded headers. Используйте только явно настроенные proxy IP; сохраняйте host validation и production TLS checks. Для production обязательны TLS PostgreSQL и Redis, явные non-loopback hosts и доверенная proxy-конфигурация.
- Compose для разработки, локальные пароли и self-signed сертификаты предназначены только для dev. Не направляйте проверки на production или сторонние системы. Provisioning и performance tests запускайте только на localhost и отдельной БД <code>_test</code>.
- Сохраняйте admin-only и read-only доступ к media. Пользовательские загрузки и processing worker не реализованы. Не добавляйте небезопасные writable mounts и не расширяйте допустимые типы/лимиты без явного дизайна и тестов.
- Проверяйте миграции на потерю данных и эксплуатационное влияние. Не выполняйте migrations или destructive commands на рабочей или неутверждённой БД; не удаляйте database volumes и пользовательские данные без явного согласия.
- Не отключайте и не ослабляйте security tests, audit tools, dependency checks или workflow protections ради успешного статуса. Явно сообщайте о нерешённых находках и ошибках валидации.

См. [архитектуру](../../docs/architecture.md) для границ модулей и [руководство по performance](../../docs/performance.md) для требований к локальным тестам. Изменения публичной документации должны соответствовать [стандарту документации](../../docs/documentation-standard.md): английская версия первой, русская второй.
