FROM node:22-alpine AS frontend-builder

WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/public ./public
COPY frontend/src ./src
COPY frontend/tsconfig.json ./
RUN npm run build

FROM python:3.14-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY app ./app
COPY migrations ./migrations
COPY scripts ./scripts
COPY alembic.ini ./
RUN uv sync --locked --no-dev

FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    APP_MEDIA_ROOT=/media

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app ./app
COPY --from=builder /app/migrations ./migrations
COPY --from=builder /app/scripts ./scripts
COPY --from=builder /app/alembic.ini ./
COPY --from=frontend-builder /frontend/public ./frontend/public

RUN mkdir -p /media \
    && useradd --create-home --uid 10001 app \
    && chown -R app:app /app
USER 10001:10001

EXPOSE 8000

CMD ["hypercorn", "app.main:app", "--bind", "0.0.0.0:8000", "--certfile", "/certs/server.crt", "--keyfile", "/certs/server.key", "--alpn-protocols", "h2,http/1.1"]
