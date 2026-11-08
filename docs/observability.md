# Observability: logs and tracing

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Status:** structured request logs are implemented; OpenTelemetry tracing is optional.

<a id="english"></a>
## English

### Application logs

The application configures Python standard-library logging with a JSON-lines formatter and writes to stderr. HTTP request-completion records include:

| Field | Meaning |
| --- | --- |
| <code>timestamp</code> | UTC timestamp |
| <code>level</code> | Log severity |
| <code>logger</code> | Logger name |
| <code>message</code> | Human-readable event message |
| <code>http_method</code> | HTTP method |
| <code>http_path</code> | URL path, without query string |
| <code>http_status_code</code> | Response status |
| <code>duration_ms</code> | Request elapsed time in milliseconds |
| <code>service_name</code> | Included for telemetry configuration events when present |
| <code>exception</code> | Formatted exception details when a log record contains exception info |

Query strings, authorization headers, passwords, bearer tokens and request bodies are not deliberately included in the request-completion log. The URL path can contain a profile UUID; restrict log access and apply a deployment-specific privacy and retention policy. The formatter does not provide a central log store, retention engine or alerting system.

Example shape:

~~~json
{
  "timestamp": "2026-11-08T08:00:00+00:00",
  "level": "INFO",
  "logger": "app.main",
  "message": "HTTP request completed",
  "http_method": "GET",
  "http_path": "/health/ready",
  "http_status_code": 200,
  "duration_ms": 4.27
}
~~~

### OpenTelemetry tracing

FastAPI request tracing is enabled only when <code>OTEL_EXPORTER_OTLP_ENDPOINT</code> is configured. The application uses the OpenTelemetry SDK and OTLP exporter over gRPC. <code>OTEL_SERVICE_NAME</code> overrides the default service name; otherwise <code>APP_NAME</code> is used.

Local example with an OpenTelemetry Collector listening on its OTLP gRPC port:

~~~sh
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
OTEL_SERVICE_NAME=user-service \
uv run hypercorn app.main:app --bind 127.0.0.1:8000 \
  --certfile certs/server.crt --keyfile certs/server.key
~~~

This is a local example. For production, use an authenticated and encrypted collector endpoint, restrict network egress and review which span attributes may contain identifiers or personal data.

### What is not provided

The repository does not currently configure a Prometheus metrics endpoint, metrics exporter, Grafana dashboards, alert manager, centralized log platform or production trace backend. OpenTelemetry tracing is not equivalent to full observability. Metric definitions and measurement gaps are listed in [metrics.md](metrics.md).

### Operational use

Correlate a slow request using the request path, status and duration fields, then inspect database/Redis health and optional traces. Avoid adding raw payloads, passwords, tokens or personal data to logs. Define log access, retention, deletion, incident export and monitoring ownership before any production deployment.

---

<a id="russian"></a>
## Русский

### Логи приложения

Приложение использует logging из стандартной библиотеки Python с JSON-lines formatter и пишет в stderr. Записи о завершении HTTP-запроса содержат:

| Поле | Значение |
| --- | --- |
| <code>timestamp</code> | Timestamp в UTC |
| <code>level</code> | Уровень сообщения |
| <code>logger</code> | Имя logger |
| <code>message</code> | Читаемое описание события |
| <code>http_method</code> | HTTP-метод |
| <code>http_path</code> | URL path без query string |
| <code>http_status_code</code> | Status ответа |
| <code>duration_ms</code> | Длительность запроса в миллисекундах |
| <code>service_name</code> | Присутствует у событий конфигурации telemetry, если задан |
| <code>exception</code> | Форматированная информация об исключении при наличии exception info |

Query strings, authorization headers, пароли, bearer-токены и тела запросов намеренно не добавляются в request-completion log. В URL path может находиться UUID профиля; ограничьте доступ к логам и задайте privacy/retention policy для конкретной среды. Formatter не создаёт централизованное хранилище логов, механизм retention или систему alerting.

Пример структуры:

~~~json
{
  "timestamp": "2026-11-08T08:00:00+00:00",
  "level": "INFO",
  "logger": "app.main",
  "message": "HTTP request completed",
  "http_method": "GET",
  "http_path": "/health/ready",
  "http_status_code": 200,
  "duration_ms": 4.27
}
~~~

### OpenTelemetry tracing

Трассировка FastAPI включается только при настройке <code>OTEL_EXPORTER_OTLP_ENDPOINT</code>. Приложение использует OpenTelemetry SDK и OTLP exporter поверх gRPC. <code>OTEL_SERVICE_NAME</code> переопределяет имя сервиса; иначе берётся <code>APP_NAME</code>.

Локальный пример с OpenTelemetry Collector на OTLP gRPC port:

~~~sh
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
OTEL_SERVICE_NAME=user-service \
uv run hypercorn app.main:app --bind 127.0.0.1:8000 \
  --certfile certs/server.crt --keyfile certs/server.key
~~~

Это локальный пример. В production используйте аутентифицированный и зашифрованный collector endpoint, ограничьте сетевой egress и проверьте, какие span attributes могут содержать идентификаторы или персональные данные.

### Чего пока нет

Репозиторий пока не настраивает Prometheus metrics endpoint, metrics exporter, Grafana dashboards, alert manager, централизованную log-платформу или production trace backend. OpenTelemetry tracing не равна полной observability. Определения метрик и пробелы измерений перечислены в [metrics.md](metrics.md).

### Эксплуатационное применение

Для разбора медленного запроса сопоставляйте path, status и duration, затем проверяйте состояние PostgreSQL/Redis и опциональные traces. Не добавляйте в логи raw payloads, пароли, токены или персональные данные. До production-развёртывания определите владельцев мониторинга, доступа к логам, retention, удаления и экспорта данных при инциденте.
