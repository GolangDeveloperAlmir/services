# Нагрузочное тестирование / Load testing

## Безопасность запуска / Safe execution

The Locust suite in `tests/performance/locustfile.py` is intentionally restricted
to `localhost` and loopback IP addresses. It rejects hostnames on other
interfaces and enforces hard caps of 250 virtual users and 15 minutes. Do not
remove those safeguards or point the suite at production or third-party hosts.

Набор Locust в `tests/performance/locustfile.py` допускает только `localhost`
и loopback IP. Другие адреса блокируются; жёсткие ограничения — 250
виртуальных пользователей и 15 минут. Не отключайте ограничения и не
направляйте тест на production или сторонние системы.

The workload is authenticated and the service rejects cleartext HTTP. Start
the local stack after creating the self-signed development certificate:

```sh
cp -n .env.example .env
make dev-certs
make up
token="$(docker compose exec -T -e APP_ENV=test app python -m scripts.provision_perf_admin)"
PERF_AUTH_TOKEN="$token" make perf-smoke
```

The one-time provisioning command refuses to run unless `APP_ENV=test` and
the database name ends in `_test`. It creates a random temporary password
in-process and prints only the short-lived bearer token. Keep the token in
memory/environment only; do not paste it into source files, command arguments,
logs, or reports. Repeat provisioning on a freshly created test database.

Запускайте только локальный Compose-стек после создания self-signed
сертификата разработки. Нагрузочный токен обязателен:

```sh
make dev-certs
make up
token="$(docker compose exec -T -e APP_ENV=test app python -m scripts.provision_perf_admin)"
PERF_AUTH_TOKEN="$token" make perf-smoke
```

Provisioning откажется работать, если `APP_ENV` не равен `test` или имя базы
не заканчивается на `_test`. Случайный временный пароль создаётся только в
процессе, команда выводит только короткоживущий bearer-токен. Не записывайте
токен в исходники, аргументы процесса, логи или отчёты.

The smoke profile uses 5 users for 30 seconds. The default load profile uses
100 users, ramps at 10 users/second, and runs for 5 minutes. Values can be
reduced or increased within the enforced safety caps:

```sh
PERF_AUTH_TOKEN="$token" make perf PERF_USERS=150 PERF_SPAWN_RATE=15 PERF_RUN_TIME=8m
```

Session TTL по умолчанию 15 минут; при более длинном прогоне создайте новый
токен или увеличьте `AUTH_SESSION_TTL_SECONDS` в пределах установленного
максимума до 3600 секунд.

Smoke-профиль: 5 пользователей, 30 секунд. Профиль нагрузки по умолчанию:
100 пользователей, запуск по 10 пользователей/секунду, 5 минут. Параметры
можно менять в пределах ограничений:

```sh
make perf PERF_USERS=150 PERF_SPAWN_RATE=15 PERF_RUN_TIME=8m
```

## Сценарии / Scenarios

- User create/read/update/delete lifecycle.
- Profile creation is deliberately independent of credential and role
  provisioning; each lifecycle user is isolated by a generated email.
- List pagination at first page, max page size, large offset, and invalid
  boundaries.
- Missing and malformed UUIDs.
- Invalid payloads: malformed email, missing fields, unknown fields, blank and
  overlong names.
- Duplicate-email requests that contend on a shared unique key.
- Minimum and maximum accepted name lengths.

Сценарии включают полный CRUD lifecycle, создание профиля без credentials или
роли, границы пагинации, отсутствующие и некорректные UUID, невалидные
payloads, конкурентные запросы с одинаковым email и граничные длины имени.

## Метрики и интерпретация / Metrics and interpretation

Locust reports request count, failures, average and median duration, p95/p99,
maximum response time, and requests/second overall and per endpoint. Each run
writes an HTML report, CSV statistics, and `reports/load-summary.json`.
Reports are local artifacts and are excluded from Git.

Отчёты Locust содержат число запросов и ошибок, среднее и медианное время,
p95/p99, максимум и запросы/секунду в целом и по endpoints. `make perf`
создаёт HTML, CSV и `reports/load-summary.json`. Эти локальные отчёты
исключены из Git.

No latency or throughput SLA has been measured or approved. Compare runs only
when the application commit, database, hardware, and test profile are recorded.
Run multiple times and treat a local result as a baseline, not a production
capacity guarantee. The duplicate-email contention scenario can leave at most
one test user in the database; use a disposable database.

SLA по задержкам или пропускной способности не измерялся и не согласовывался.
Сравнивайте прогоны только при зафиксированных commit, базе, оборудовании и
профиле нагрузки. Повторяйте замеры; локальный результат — baseline, а не
гарантия production capacity. Сценарий конкурентного email может оставить в
БД одного тестового пользователя — используйте disposable database.

## Diagnosing a slow run / Разбор медленного прогона

1. Compare endpoint percentiles and error counts in the HTML/JSON reports.
2. Correlate with JSON request logs and optional OpenTelemetry traces.
3. Check database CPU, connections, slow queries, and pool saturation.
4. Change one variable at a time and rerun the same profile.

1. Сравните percentiles и ошибки по endpoint в HTML/JSON.
2. Сопоставьте их с JSON-логами и, если включено, OpenTelemetry traces.
3. Проверьте CPU БД, соединения, медленные запросы и заполнение пула.
4. Меняйте по одному параметру и повторяйте одинаковый профиль.
