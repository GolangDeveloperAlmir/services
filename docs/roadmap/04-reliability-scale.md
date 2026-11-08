# PLAN-04: Reliability, performance and scale

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Status:** conditional future specification. Numeric latency/throughput SLOs are not approved; no production benchmark baseline exists.

<a id="english"></a>
## English

### Goal

Measure the API under an agreed workload and remove demonstrated bottlenecks. Do not add caching, queues, read replicas, new databases or service decomposition without evidence, an operational owner and a failure model. Existing load tests must remain loopback-only and use a disposable database whose name ends in _test.

### Establish a reproducible baseline

Record commit/image, Python and dependency versions, API/DB/Redis configuration, pool sizes, TLS settings, CPU/RAM/disk/network, database size and row distribution, endpoint mix, read/write/auth mix, payloads, concurrency, warm-up, duration, errors, p50/p95/p99/max and throughput. Repeat runs and report spread; do not select only the best result. Use synthetic data and keep personal data/tokens out of reports.

A local benchmark is not a forecast of production capacity.

### Decision process

1. Identify user-visible SLI and business-critical workflows.
2. Capture a baseline and reproduce the bottleneck.
3. Form a hypothesis with measurable expected improvement and regression risk.
4. Change one cause category at a time: SQL/index/pagination, connection pool/timeouts, CPU/serialization or dependency behaviour.
5. Repeat the same profile and compare endpoint percentiles, error rate, throughput, resource saturation and cost.
6. Add cache, queue or infrastructure only after simpler options are exhausted and freshness/delivery/cost requirements are documented.

### Candidates requiring evidence

| Candidate | What to measure first |
| --- | --- |
| Offset pagination | Query plans and response time at large offsets; keyset changes API semantics |
| PostgreSQL indexes | Selectivity, execution plans, write overhead and storage cost |
| DB pool | Aggregate connections across processes/replicas and wait time |
| Redis outage/latency | Session and throttling failure behaviour; no permissive in-memory auth fallback |
| Serialization/validation | CPU profile and unchanged API contract |
| Logs/traces | Cardinality and cost without exposing personal data |

### Non-functional objectives and resilience

Numeric values require owner approval after baseline. Define availability window/exclusions, endpoint latency percentiles, error budget, throughput demand, resource ceilings, backup/restore expectations and recovery. Do not invent target values.

In dedicated test/staging, simulate PostgreSQL outage/latency, Redis outage, pool exhaustion, collector failure, slow startup/shutdown and migration failure. Confirm access is denied safely, no misleading success is returned, and recovery works after dependencies return. Fault injection must not target production or third parties without explicit authorization.

| Stage | Work | Exit evidence |
| --- | --- | --- |
| 04-A Baseline | Capture repeatable profile | Metadata and comparable runs |
| 04-B SLO | Approve SLI/SLO and error budget | Owner-approved objectives |
| 04-C Bottleneck | Reproduce with profiler/query plan | Root cause verified |
| 04-D Improvement | Implement smallest effective change | Measured improvement and regression tests |
| 04-E Resilience | Test failures and recovery | Safe failure behaviour and runbook |
| 04-F Capacity review | Compare results with demand/cost | Documented capacity decision |

Acceptance requires repeatable safe tests, approved objectives, like-for-like comparison, latency/errors/throughput/resources review, bounded retry/cache/queue states, fail-closed behaviour and a capacity runbook that does not promise unlimited growth.

---

<a id="russian"></a>
## Русский

### Цель

Измерить поведение API при согласованной нагрузке и устранить подтверждённые узкие места. Не добавлять cache, queue, read replicas, новые БД или разделение на сервисы без evidence, владельца эксплуатации и модели отказов. Все load tests должны оставаться loopback-only и использовать отдельную одноразовую БД, имя которой заканчивается на _test.

### Воспроизводимый baseline

Зафиксировать commit/image, версии Python и зависимостей, настройки API/БД/Redis, pool sizes, TLS, CPU/RAM/disk/network, размер и распределение строк БД, endpoint mix, read/write/auth mix, payload, concurrency, warm-up, длительность, ошибки, p50/p95/p99/max и throughput. Повторять запуск и указывать разброс; нельзя выбирать только лучший результат. Использовать synthetic data, не помещать персональные данные и токены в отчёты.

Локальный benchmark не является прогнозом production capacity.

### Порядок решений

1. Определить пользовательские SLI и критичные бизнес-сценарии.
2. Снять baseline и воспроизвести узкое место.
3. Сформулировать гипотезу с измеримым улучшением и риском регрессии.
4. Менять по одной категории причин: SQL/index/pagination, DB pool/timeouts, CPU/serialization или поведение зависимости.
5. Повторить тот же профиль и сравнить endpoint percentiles, error rate, throughput, насыщение ресурсов и стоимость.
6. Добавлять cache, queue или инфраструктуру только после исчерпания простых решений и документирования требований свежести/доставки/стоимости.

### Кандидаты, требующие evidence

| Кандидат | Что измерить сначала |
| --- | --- |
| Offset pagination | Query plans и response time на больших offsets; keyset меняет семантику API |
| PostgreSQL indexes | Selectivity, execution plans, стоимость записи и хранения |
| DB pool | Совокупное число соединений всех процессов/реплик и wait time |
| Redis outage/latency | Поведение сессий и throttling; permissive in-memory auth fallback запрещён |
| Serialization/validation | CPU profile при неизменном API-контракте |
| Logs/traces | Cardinality и стоимость без раскрытия персональных данных |

### Нефункциональные цели и resilience

Числа утверждаются владельцем только после baseline. Нужно определить окно availability и исключения, endpoint latency percentiles, error budget, throughput demand, лимиты ресурсов, backup/restore и recovery. Не выдумывать целевые значения.

В отдельной test/staging среде моделировать outage/latency PostgreSQL, outage Redis, исчерпание pool, отказ collector, медленные startup/shutdown и ошибки миграций. Проверить безопасный отказ доступа, отсутствие ложного успеха и восстановление после возвращения зависимости. Fault injection нельзя направлять на production или сторонние системы без явного разрешения.

| Этап | Работа | Доказательство выхода |
| --- | --- | --- |
| 04-A Baseline | Снять повторяемый профиль | Метаданные и сопоставимые запуски |
| 04-B SLO | Утвердить SLI/SLO и error budget | Цели утверждены владельцем |
| 04-C Bottleneck | Воспроизвести profiler/query plan | Причина подтверждена |
| 04-D Improvement | Реализовать минимально достаточное изменение | Измеренное улучшение и regression tests |
| 04-E Resilience | Проверить отказ и восстановление | Безопасное поведение и runbook |
| 04-F Capacity review | Сравнить результаты со спросом и стоимостью | Зафиксированное решение о capacity |

Приёмка требует безопасных повторяемых тестов, утверждённых целей, сравнения при одинаковых условиях, оценки latency/errors/throughput/resources, ограниченных retry/cache/queue состояний, fail-closed поведения и capacity runbook без обещаний неограниченного роста.
