# Contributing

## Кратко

Используйте Python 3.14 и `uv` либо откройте проект в Dev Container:

```sh
uv sync --locked --all-groups
make frontend-install
make frontend-build
uv run pre-commit install -c .pre-commit-config.yaml
```

Скопируйте `.env.example` в `.env`, замените локальные пароли, создайте
development TLS certificate командой `make dev-certs`, затем запустите
PostgreSQL, Redis и API командой `make up`.
Перед PR выполните `make check`, `make validate-specs` и `make architecture`.
Frontend-проверки требуют `make frontend-install`; для локальной раздачи
интерфейса также выполните `make frontend-build`.
После изменения роутов/схем сгенерируйте OpenAPI командой `make openapi`.

Добавляйте тесты и обновляйте документацию вместе с поведением. Не добавляйте
`.env`, токены и production-данные. Нагрузочный тест запускайте только локально
на disposable `_test` database; профиль и ограничения описаны в
[docs/performance.md](docs/performance.md). Изменения auth/RBAC должны
проверять deny-by-default и инвариант последнего активного admin.
Добавляйте содержательные docstrings для новых публичных модулей, классов и
функций: описывайте контракт, ошибки и важные ограничения, а не пересказывайте
имя функции. CRUD-изменения проверяйте на уровне service и HTTP API.
Отправляя вклад, убедитесь, что вправе его предоставить, и соглашаетесь на
распространение вклада по лицензии репозитория [LICENSE](LICENSE). Соблюдайте
[правила сообщества](CODE_OF_CONDUCT.md).

## Development environment

Use Python 3.14 and `uv`, or open the repository in its Dev Container.

```sh
uv sync --locked --all-groups
uv run pre-commit install -c .pre-commit-config.yaml
```

For a local environment, create `.env` from `.env.example`, replace the local
password placeholders, run `make dev-certs`, and start the Compose stack with
`make up`. It applies migrations before starting the API.
The development override exposes PostgreSQL only on `127.0.0.1:5433`.

## Before opening a pull request

```sh
make check
make frontend-check
make nginx-check
make validate-specs
make architecture
make security
```

For frontend changes, run `make frontend-check` and `make frontend-build`.
Commit the regenerated `frontend/public/assets/app.js` together with its
TypeScript source. CI installs the locked npm dependencies before running
`make check`; `make security` also audits the frontend lockfile.

Run `make openapi` after changing routes or schemas, and commit the regenerated
`openapi.yaml`. `asyncapi.yaml` documents the current absence of messaging
channels; update it if asynchronous interfaces are introduced.

Keep changes focused, add or update tests, and document configuration or
operational changes. Never commit `.env` files, tokens, or production data.
Add meaningful docstrings to new public modules, classes, and functions;
describe contracts, errors, and relevant constraints instead of repeating
symbol names. Cover CRUD changes at both service and HTTP API levels.
By submitting a contribution, you confirm that you have the right to do so
and agree that it is distributed under the repository's [LICENSE](LICENSE).
Please also follow the [Code of Conduct](CODE_OF_CONDUCT.md).
Review `.secrets.baseline` changes carefully; never baseline real credentials.
Run `uv lock` and commit `uv.lock` when dependencies change. Pin third-party
GitHub Actions to full commit SHAs.
Pull requests should follow the repository template and receive CODEOWNERS
review.

## Architecture

See [docs/architecture.md](docs/architecture.md) for module boundaries and
dependency rules. Architecture rules are checked by both pytest and
Import Linter.

Security controls, administrator provisioning, threat boundaries, and
production prerequisites are documented in
[docs/security.md](docs/security.md).

## Documentation and ownership

The documentation index is [docs/index.md](docs/index.md). Please keep the
Russian and English sections in sync. Pull requests use the template in
`.github/pull_request_template.md` and require review from CODEOWNERS.
