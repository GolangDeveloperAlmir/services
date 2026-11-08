# Metrics, evidence and project snapshot

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Inventory date:** 2026-11-08

<a id="english"></a>
## English

### Repository inventory

These are static facts obtained from the repository tree and checked-in test/configuration files. They are not usage, adoption, availability or performance metrics.

| Indicator | Value | Source |
| --- | ---: | --- |
| Tracked repository files | 140 | Recursive Git tree on the default branch |
| Automated test modules | 10 | tests/test_*.py |
| Detailed roadmap specifications | 5 | docs/roadmap/ |
| Compose runtime services | 4 | docker-compose.yml |
| Python minimum version | 3.14 | pyproject.toml |
| Frontend TypeScript version | 5.9.3 | frontend/package.json |
| Maximum configured load-test users | 250 | docs/performance.md and test safeguards |
| Maximum configured load-test duration | 15 minutes | tests/performance/ safeguards |

Inventory changes as the repository changes. Refresh the values before publishing release notes or an external project profile.

### Measurement status

| Metric | Current status | Evidence needed before publishing a value |
| --- | --- | --- |
| Request latency (p50/p95/p99) | Not published | Repeatable run, commit, machine, payload and workload |
| Throughput (RPS) | Not published | Completed requests, duration, concurrency and error rate |
| Error rate | Not published | Defined workload and classified failures |
| Database pool saturation | Not published | Pool configuration and observed checkout/wait data |
| Redis latency and availability | Not published | Instrumentation and observed time window |
| CPU and memory | Not published | Process/container measurements under a documented profile |
| Production availability | Not established | Production deployment, monitoring period and agreed SLO |
| RPO/RTO | Not established | Approved backup design and witnessed restore exercise |
| Adoption, stars and downloads | Not represented here | Authoritative analytics captured on a stated date |

### Metric definitions

| Metric | Definition | Interpretation |
| --- | --- | --- |
| p50 | Median response time | Typical request in the sample |
| p95 | 95th percentile latency | 5% of observed requests took longer |
| p99 | 99th percentile latency | Tail behaviour, sensitive to queueing and pauses |
| RPS | Completed requests per second | Publish success and error counts alongside it |
| Error rate | Failed requests divided by total requests | Classify 4xx, 5xx, timeouts and client aborts separately |
| Saturation | Resource pressure relative to configured capacity | Examine CPU, memory, DB pool, file descriptors and Redis memory |
| Availability | Fraction of time a defined service check succeeds | Requires a precise check and observation window |

### Telemetry currently available

The application emits JSON request-completion logs with timestamp, severity, logger, message, method, path, status code and duration. OpenTelemetry tracing can be enabled with <code>OTEL_EXPORTER_OTLP_ENDPOINT</code>; traces are exported over OTLP gRPC. This integration does not add a Prometheus endpoint, metrics exporter, dashboard, alert manager or hosted observability backend.

### Publishing a benchmark responsibly

A useful report identifies the exact commit, hardware/OS, container limits, dependency versions, database state and size, endpoint mix, payload, virtual users, spawn rate, duration, warm-up, p50/p95/p99, throughput and errors. Include raw HTML/CSV reports where possible. Do not compare runs with different workloads as if they were equivalent.

Performance tests are restricted to localhost/loopback and a disposable test database whose name ends in <code>_test</code>. Do not bypass those restrictions to obtain a public benchmark.

---

<a id="russian"></a>
## Русский

### Инвентаризация репозитория

Это статические факты, полученные из Git tree и файлов тестов/конфигурации. Они не являются метриками использования, популярности, доступности или производительности.

| Показатель | Значение | Источник |
| --- | ---: | --- |
| Отслеживаемые файлы репозитория | 134 | Рекурсивный Git tree основной ветки |
| Модули автоматических тестов | 10 | tests/test_*.py |
| Подробные спецификации roadmap | 5 | docs/roadmap/ |
| Группы runtime-сервисов Compose | 4 | docker-compose.yml |
| Минимальная версия Python | 3.14 | pyproject.toml |
| Версия TypeScript frontend | 5.9.3 | frontend/package.json |
| Максимум пользователей load test | 250 | docs/performance.md и safeguards тестов |
| Максимальная длительность load test | 15 минут | Ограничения tests/performance/ |

Инвентаризация меняется вместе с репозиторием. Обновляйте значения перед публикацией release notes или внешнего описания проекта.

### Состояние измерений

| Метрика | Текущее состояние | Что требуется для публикации значения |
| --- | --- | --- |
| Latency запросов (p50/p95/p99) | Не опубликовано | Повторяемый запуск, commit, машина, payload и workload |
| Throughput (RPS) | Не опубликовано | Завершённые запросы, длительность, concurrency и error rate |
| Доля ошибок | Не опубликована | Определённый workload и классификация ошибок |
| Насыщение DB connection pool | Не опубликовано | Конфигурация pool и наблюдения checkout/wait |
| Latency и availability Redis | Не опубликовано | Инструментация и наблюдаемый интервал |
| CPU и память | Не опубликовано | Измерения процесса/контейнера под описанным профилем |
| Production availability | Не установлена | Production deployment, период мониторинга и согласованный SLO |
| RPO/RTO | Не установлены | Утверждённая схема backup и проверенное восстановление |
| Adoption, stars и downloads | Здесь не представлены | Авторитетная аналитика с указанной датой |

### Определения метрик

| Метрика | Определение | Интерпретация |
| --- | --- | --- |
| p50 | Медианное время ответа | Типичный запрос в выборке |
| p95 | 95-й перцентиль latency | 5% наблюдавшихся запросов выполнялись дольше |
| p99 | 99-й перцентиль latency | Хвост распределения, чувствительный к очередям и паузам |
| RPS | Число завершённых запросов в секунду | Публикуйте рядом число успехов и ошибок |
| Error rate | Неуспешные запросы / все запросы | Разделяйте 4xx, 5xx, timeout и client abort |
| Saturation | Давление на ресурс относительно настроенной ёмкости | Проверяйте CPU, память, DB pool, file descriptors и Redis memory |
| Availability | Доля времени, когда заданная проверка сервиса успешна | Нужны точная проверка и окно наблюдения |

### Доступная телеметрия

Приложение выдаёт JSON request-completion logs с timestamp, severity, logger, message, method, path, status code и duration. OpenTelemetry tracing включается через <code>OTEL_EXPORTER_OTLP_ENDPOINT</code>; traces экспортируются по OTLP gRPC. Интеграция не добавляет Prometheus endpoint, metrics exporter, dashboard, alert manager или hosted observability backend.

### Ответственная публикация benchmark

Отчёт должен указывать точный commit, оборудование/ОС, лимиты контейнеров, версии зависимостей, состояние и размер БД, набор endpoint, payload, виртуальных пользователей, spawn rate, длительность, warm-up, p50/p95/p99, throughput и ошибки. По возможности приложите исходные HTML/CSV-отчёты. Нельзя сравнивать разные workloads как одинаковые условия.

Нагрузочные тесты ограничены localhost/loopback и отдельной тестовой БД с именем, заканчивающимся на <code>_test</code>. Не обходите ограничения ради публичного benchmark.
