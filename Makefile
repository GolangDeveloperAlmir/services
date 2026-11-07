.PHONY: install lint format test architecture specs openapi validate-specs hooks check security run migrate docker-build compose-config dev-certs up perf-smoke perf

PERF_USERS ?= 100
PERF_SPAWN_RATE ?= 10
PERF_RUN_TIME ?= 5m

install:
	uv sync --all-groups

lint:
	uv run ruff check app migrations tests
	uv run ruff format --check app migrations tests

format:
	uv run ruff format app migrations tests

test:
	uv run pytest

architecture:
	uv run lint-imports
	uv run pytest tests/test_architecture.py

specs:
	uv run pytest tests/test_specs.py

openapi:
	PYTHONPATH=. uv run python scripts/export_openapi.py

validate-specs:
	uv run python scripts/validate_asyncapi.py
	uv run pytest tests/test_specs.py

security:
	@tmpfile=$$(mktemp); \
	trap 'rm -f "$$tmpfile"' EXIT; \
	uv export --locked --format requirements-txt --all-groups --no-emit-project > "$$tmpfile"; \
	uv run pip-audit --vulnerability-service osv --strict --require-hashes --requirement "$$tmpfile"
	uv run bandit -ll -ii -c pyproject.toml -r app
	uv run zizmor .github
	uv run pre-commit run --all-files --config .pre-commit-config.yaml

hooks:
	uv run pre-commit run --all-files --config .pre-commit-config.yaml

check: lint test architecture validate-specs security

run:
	uv run hypercorn app.main:app --bind 127.0.0.1:8000 --certfile certs/server.crt --keyfile certs/server.key --alpn-protocols h2,http/1.1 --reload

migrate:
	uv run alembic upgrade head

dev-certs:
	mkdir -p certs
	openssl req -x509 -newkey rsa:3072 -nodes -days 30 \
		-keyout certs/server.key -out certs/server.crt \
		-subj "/CN=localhost" \
		-addext "subjectAltName=DNS:localhost,IP:127.0.0.1" \
		-addext "basicConstraints=critical,CA:TRUE" \
		-addext "keyUsage=critical,digitalSignature,keyEncipherment,keyCertSign" \
		-addext "extendedKeyUsage=serverAuth"

up:
	LOCAL_UID=$$(id -u) LOCAL_GID=$$(id -g) docker compose up --build --wait

docker-build:
	docker build -t user-service .

compose-config:
	docker compose config --quiet

perf-smoke:
	mkdir -p reports
	REQUESTS_CA_BUNDLE=certs/server.crt uv run locust -f tests/performance/locustfile.py --headless --host https://127.0.0.1:8000 --users 5 --spawn-rate 1 --run-time 30s --html reports/load-smoke.html --csv reports/load-smoke

perf:
	mkdir -p reports
	REQUESTS_CA_BUNDLE=certs/server.crt uv run locust -f tests/performance/locustfile.py --headless --host https://127.0.0.1:8000 --users $(PERF_USERS) --spawn-rate $(PERF_SPAWN_RATE) --run-time $(PERF_RUN_TIME) --html reports/load-test.html --csv reports/load-test
