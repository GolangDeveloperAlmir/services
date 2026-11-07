# Logging and tracing

## Application logs

The application configures standard-library logging to emit JSON lines to
stderr. HTTP request completion records include the method, URL path, response
status, and elapsed time. Query strings, authorization headers, passwords,
bearer tokens, and request bodies are intentionally not logged. The URL path
can include a profile UUID; restrict log access and apply the deployment's
retention/privacy policy.
CRUD request bodies, email values, query strings, and authorization credentials
are not included in the request log. The response status and duration can be
used to correlate `404` lookups and `409` uniqueness conflicts without
recording submitted profile data.

## OpenTelemetry tracing

FastAPI request spans are exported using OTLP over gRPC when
`OTEL_EXPORTER_OTLP_ENDPOINT` is set. For example, with a local OpenTelemetry
Collector listening on its default gRPC port:

```sh
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
OTEL_SERVICE_NAME=user-service \
uv run hypercorn app.main:app --bind 127.0.0.1:8000 \
  --certfile certs/server.crt --keyfile certs/server.key
```

Without an endpoint, tracing instrumentation and exporters are not started.
Configure collector authentication and TLS according to the collector
deployment; do not put credentials in the repository. OpenTelemetry exporter
environment options such as `OTEL_EXPORTER_OTLP_HEADERS` can be used where
appropriate. Treat traces as potentially sensitive operational data; do not
export authentication headers or request bodies.

## API schema

FastAPI builds the OpenAPI schema from the registered routes and Pydantic
models at runtime. Browse `/docs` for Swagger UI or retrieve `/openapi.json`
for the generated JSON document. The generated OpenAPI snapshot is checked into the repository and validated
with `make validate-specs`.

## Наблюдаемость

Приложение пишет JSON-lines в stderr. Для HTTP-запросов логируются метод,
путь, статус и время обработки; query-параметры и тела запросов не записываются.
Путь может содержать UUID профиля; ограничивайте доступ к логам и задавайте
политику хранения. Email и тела CRUD-запросов не логируются; по статусу и
времени можно анализировать ответы `404`/`409` без записи данных профиля.

### Трассировка

FastAPI request spans экспортируются по OTLP/gRPC, если задан
`OTEL_EXPORTER_OTLP_ENDPOINT`. Без endpoint инструментирование не запускается.
Не храните секреты экспортера в репозитории; используйте окружение deployment.

### API-схема

FastAPI генерирует OpenAPI во время выполнения из роутов и моделей Pydantic.
Swagger UI доступен по `/docs`, JSON — по `/openapi.json`, ReDoc — по `/redoc`.
Версия схемы в репозитории обновляется командой `make openapi`.

## Подключение коллектора / Collector setup

```sh
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
OTEL_SERVICE_NAME=user-service \
uv run hypercorn app.main:app --bind 127.0.0.1:8000 \
  --certfile certs/server.crt --keyfile certs/server.key
```

Для внешнего collector настройте TLS и аутентификацию в соответствии с его
deployment. Поддерживаемые параметры exporter, например
`OTEL_EXPORTER_OTLP_HEADERS`, передавайте через защищённые переменные окружения.
Не экспортируйте auth headers или request bodies; traces следует считать
потенциально чувствительными операционными данными.
