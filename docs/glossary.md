# Glossary and shared terminology

> **Language / Язык:** [English](#english) · [Русский](#russian)

<a id="english"></a>
## English

Use these definitions consistently in code reviews, API descriptions, diagrams and product discussions. They describe the current project unless a term is explicitly marked as a future concept.

| Term | Definition in this project | Avoid confusing it with |
| --- | --- | --- |
| Profile | Record containing attributes such as email and full name | A login account |
| Identity / account | Subject that can authenticate and receive authorization | A public profile record |
| Local credential | Password verifier and credential state associated with a user | The submitted password |
| Role | Named authorization grouping; the current built-in role is <code>admin</code> | A tenant or resource |
| RBAC | Role-based access control: permissions are derived from assigned roles | Tenant isolation |
| Administrator | Active authenticated principal holding the <code>admin</code> role | A profile without credentials |
| Bearer token | Secret presented by a client to prove possession of a session | A public identifier |
| Opaque token | Random token whose internal meaning is not encoded in the value | A self-describing JWT |
| Session | Server-side state tying a token to a user and credential version | The raw token itself |
| TTL | Time to live: expiry window for a session or counter | Audit retention policy |
| Rate limit | Bound on repeated actions during a time window | General DDoS protection |
| Tenant / organization | Future isolation boundary for users or resources | A currently implemented data boundary |
| Fail closed | Deny access when required validation or dependency state is unavailable | A permissive fallback |
| ASGI | Asynchronous Server Gateway Interface for Python web apps | An HTTP server |
| Reverse proxy | Server accepting client traffic and forwarding it to an upstream | The application server |
| TLS termination | Point where encrypted transport is decrypted | Automatic encryption of proxy-to-app traffic |
| Migration | Versioned database schema change | A backup or rollback plan |
| Liveness | Check that a process is alive enough to remain running | Dependency readiness |
| Readiness | Check that the application can serve intended requests | A complete synthetic customer journey |
| Structured log | Machine-readable record with stable fields | A trace or metric |
| Trace | Distributed representation of one request or operation | A single log entry |
| Span | Timed operation inside a trace | A separate request |
| OTLP | OpenTelemetry Protocol used to export telemetry | A metrics backend |
| p50 / p95 / p99 | Median and upper-tail latency percentiles | Average response time |
| Throughput / RPS | Completed requests per second under a stated workload | A meaningful benchmark without workload details |
| Virtual user (VU) | Simulated Locust client executing a workload | A real concurrent human user |
| OpenAPI | Machine-readable description of HTTP operations and schemas | The implementation itself |
| AsyncAPI | Contract format for message-driven APIs | An event broker |
| ADR | Architecture Decision Record documenting a decision and consequences | A roadmap proposal |
| SLO | Service Level Objective: agreed reliability target | A contractual SLA |
| SLA | Service Level Agreement with contractual obligations | An internal target |
| RPO / RTO | Recovery Point Objective / Recovery Time Objective | An untested aspiration |
| Quarantine | Isolated holding area for untrusted uploads before processing | A current media upload feature |

### Naming rules

Use **profile** for the <code>users</code> resource; **administrator** for an authenticated principal with the <code>admin</code> role; **credential** for password-verifier state; **session** for expiring access state; **catalog media** for trusted operator-managed files; and **local media** for files selected only in the browser. Use **planned**, **proposed** or **future specification** for work not present in runtime code.

---

<a id="russian"></a>
## Русский

Используйте эти определения одинаково в code review, описаниях API, диаграммах и продуктовых обсуждениях. Они описывают текущий проект, если термин явно не отмечен как будущая концепция.

| Термин | Определение в проекте | Не путать с |
| --- | --- | --- |
| Profile / профиль | Запись с атрибутами, например email и полным именем | Учётной записью для входа |
| Identity / account | Субъект, который может проходить аутентификацию и получать права | Публичной записью профиля |
| Local credential | Проверочное значение пароля и состояние credentials пользователя | Переданным паролем |
| Role / роль | Именованная группа полномочий; сейчас встроена роль <code>admin</code> | Tenant или ресурсом |
| RBAC | Role-Based Access Control: права выводятся из назначенных ролей | Изоляцией арендаторов |
| Administrator | Активный аутентифицированный субъект с ролью <code>admin</code> | Профилем без credentials |
| Bearer token | Секрет, которым клиент подтверждает владение сессией | Публичным идентификатором |
| Opaque token | Случайный токен, внутренний смысл которого не закодирован в значении | Самоописывающим JWT |
| Session / сессия | Серверное состояние, связывающее токен с пользователем и версией credentials | Самим сырым токеном |
| TTL | Time To Live: время жизни сессии или счётчика | Политикой хранения audit-записей |
| Rate limit | Ограничение повторных действий за временное окно | Универсальной DDoS-защитой |
| Tenant / organization | Будущая граница изоляции пользователей или ресурсов | Реализованной сейчас границей данных |
| Fail closed | Запретить доступ при недоступной обязательной проверке или зависимости | Разрешающим fallback |
| ASGI | Асинхронный интерфейс Python web-приложений | HTTP-сервером |
| Reverse proxy | Сервер, принимающий клиентский трафик и пересылающий его upstream | Сервером приложения |
| TLS termination | Место расшифровки защищённого транспорта | Автоматическим шифрованием связи proxy → app |
| Migration / миграция | Версионируемое изменение схемы БД | Резервной копией или планом отката |
| Liveness | Проверка, что процесс достаточно жив для продолжения работы | Готовностью всех зависимостей |
| Readiness | Проверка, что приложение может обслуживать предназначенные запросы | Полным synthetic-сценарием клиента |
| Structured log | Машиночитаемая запись с устойчивыми полями | Trace или metric |
| Trace | Распределённое представление запроса или операции | Одной записью лога |
| Span | Измеряемая операция внутри trace | Отдельным запросом |
| OTLP | OpenTelemetry Protocol для экспорта телеметрии | Metrics backend |
| p50 / p95 / p99 | Медиана и верхние перцентили latency | Средним временем ответа |
| Throughput / RPS | Число завершённых запросов в секунду при указанной нагрузке | Полноценным benchmark без описания нагрузки |
| Virtual user (VU) | Симулируемый клиент Locust, выполняющий сценарий | Реальным человеком с параллельным запросом |
| OpenAPI | Машиночитаемое описание HTTP-операций и схем | Самой реализацией |
| AsyncAPI | Формат контракта message-driven API | Event broker |
| ADR | Architecture Decision Record с решением и последствиями | Предложением roadmap |
| SLO | Service Level Objective: согласованная цель надёжности | Договорным SLA |
| SLA | Service Level Agreement с договорными обязательствами | Внутренней целью |
| RPO / RTO | Recovery Point Objective / Recovery Time Objective | Непроверенным намерением |
| Quarantine / карантин | Изолированное место для недоверенных файлов до обработки | Текущей функцией загрузки медиа |

### Правила именования

Используйте **profile** для ресурса <code>users</code>; **administrator** для аутентифицированного субъекта с ролью <code>admin</code>; **credential** для проверочного состояния пароля; **session** для временного состояния доступа; **catalog media** для доверенных файлов оператора; **local media** для файлов, выбранных только в браузере. Для отсутствующего в runtime функционала используйте **planned**, **proposed** или **future specification**.
