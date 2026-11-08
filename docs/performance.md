# Performance and safe load testing

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Status:** a guarded local Locust suite exists; no production benchmark or capacity claim is published.

<a id="english"></a>
## English

### Safety boundary

The Locust suite in <code>tests/performance/locustfile.py</code> is intentionally restricted to <code>localhost</code> and loopback IP addresses. It rejects non-loopback targets and enforces hard caps of 250 virtual users and 15 minutes. Keep these safeguards. Do not point the suite at production, a third-party host or a shared database.

The suite requires authenticated access and a disposable database whose name ends in <code>_test</code>. It uses the local development certificate. Do not weaken TLS checks or change the test target guard to obtain a larger number.

### Prepare the local environment

~~~sh
cp -n .env.example .env
# Set unique local POSTGRES_PASSWORD and REDIS_PASSWORD values.
make dev-certs
make up
docker compose exec app python -m app.auth.cli bootstrap-admin
~~~

Create a performance-only administrator and configure the expected local test credentials. The test helper uses <code>PERF_AUTH_TOKEN</code>; never reuse a production token. Run tests only after verifying that the host is loopback and the selected database is disposable.

### Run the smoke profile

~~~sh
make perf-smoke
~~~

The smoke profile runs a small local workload and writes HTML/CSV reports under <code>reports/</code>. It is intended to catch gross regressions and broken test wiring, not to establish capacity.

### Run a bounded local profile

~~~sh
PERF_USERS=100 PERF_SPAWN_RATE=10 PERF_RUN_TIME=5m make perf
~~~

The command-line values are configurable, but test code still enforces the hard limits. Store the output with the tested commit and environment details. Do not commit reports containing tokens, emails or other sensitive test data.

### Workload and interpretation

The suite exercises authenticated service workflows defined in the Locust task set. Interpret the result alongside:

- request count and endpoint mix;
- success and error counts, including timeouts;
- p50, p95 and p99 latency per endpoint;
- throughput and virtual-user count;
- CPU, memory and container limits;
- PostgreSQL connection-pool pressure and query time;
- Redis latency, memory pressure and availability.

A single average latency is insufficient. A high request rate with elevated errors is not a successful result. Change one variable at a time and repeat the same profile.

### Diagnosing a slow run

1. Compare endpoint percentiles and error counts in HTML/CSV reports.
2. Correlate the slow path with JSON request logs and optional OpenTelemetry traces.
3. Check database CPU, connections, slow queries and pool saturation.
4. Check Redis latency and memory limits.
5. Repeat the same workload after changing one parameter.

### Reporting a benchmark

Record commit SHA, date, OS/hardware, container limits, dependency versions, database state, endpoint mix, payload, virtual users, spawn rate, duration, warm-up, percentiles, throughput and errors. A result without its workload and environment is not a reproducible benchmark. See [metrics.md](metrics.md) for definitions and publication rules.

---

<a id="russian"></a>
## Русский

### Ограничения безопасности

Набор Locust в <code>tests/performance/locustfile.py</code> намеренно ограничен адресами <code>localhost</code> и loopback IP. Внешние цели отклоняются; жёсткие пределы — 250 виртуальных пользователей и 15 минут. Сохраняйте эти safeguards. Не направляйте набор на production, сторонние host или общую базу данных.

Набору требуются аутентифицированный доступ и отдельная одноразовая БД, имя которой заканчивается на <code>_test</code>. Используется локальный development certificate. Не ослабляйте TLS-проверки и target guard ради большего числа.

### Подготовка окружения

~~~sh
cp -n .env.example .env
# Установите уникальные локальные значения POSTGRES_PASSWORD и REDIS_PASSWORD.
make dev-certs
make up
docker compose exec app python -m app.auth.cli bootstrap-admin
~~~

Создайте отдельного администратора для performance-тестов и задайте локальные тестовые credentials. Test helper использует <code>PERF_AUTH_TOKEN</code>; не переиспользуйте production-токен. Запускайте тесты только после проверки loopback host и disposable database.

### Smoke-профиль

~~~sh
make perf-smoke
~~~

Smoke-профиль создаёт небольшую локальную нагрузку и сохраняет HTML/CSV отчёты в <code>reports/</code>. Его задача — найти грубые регрессии и сломанную тестовую конфигурацию, а не определить capacity.

### Ограниченный локальный профиль

~~~sh
PERF_USERS=100 PERF_SPAWN_RATE=10 PERF_RUN_TIME=5m make perf
~~~

Значения команды можно менять, но код теста всё равно проверяет жёсткие ограничения. Сохраняйте отчёт вместе с commit и параметрами окружения. Не коммитьте отчёты, содержащие токены, email и другие чувствительные тестовые данные.

### Нагрузка и интерпретация

Набор выполняет аутентифицированные сценарии, определённые в Locust task set. Результат нужно оценивать вместе с:

- числом запросов и распределением по endpoint;
- количеством успехов и ошибок, включая timeout;
- p50, p95 и p99 latency для каждого endpoint;
- throughput и числом виртуальных пользователей;
- CPU, памятью и лимитами контейнеров;
- давлением на PostgreSQL connection pool и временем запросов;
- latency, памятью и доступностью Redis.

Одного среднего времени ответа недостаточно. Высокий RPS при увеличении ошибок не является успешным результатом. Меняйте по одному параметру и повторяйте тот же профиль.

### Разбор медленного запуска

1. Сравните перцентили и ошибки по endpoint в HTML/CSV отчётах.
2. Сопоставьте медленный path с JSON request logs и опциональными OpenTelemetry traces.
3. Проверьте CPU БД, соединения, медленные запросы и заполнение pool.
4. Проверьте latency Redis и лимиты памяти.
5. Повторите тот же workload после изменения одного параметра.

### Публикация benchmark

Укажите commit SHA, дату, ОС/оборудование, лимиты контейнеров, версии зависимостей, состояние БД, набор endpoint, payload, число виртуальных пользователей, spawn rate, длительность, warm-up, перцентили, throughput и ошибки. Результат без workload и описания окружения не является воспроизводимым benchmark. Определения и правила публикации описаны в [metrics.md](metrics.md).
