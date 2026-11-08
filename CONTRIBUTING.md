# Contributing

> **Language / Язык:** [English](#english) · [Русский](#russian)

<a id="english"></a>
## English

Thank you for considering a contribution. This repository is a FastAPI profile service for controlled administrator use. Read the [product overview](docs/product-overview.md) and [architecture](docs/architecture.md) before changing its boundaries.

### Development environment

Use Python 3.14 and [uv](https://docs.astral.sh/uv/), or open the repository in its Dev Container.

~~~sh
uv sync --locked --all-groups
make frontend-install
make frontend-build
uv run pre-commit install -c .pre-commit-config.yaml
~~~

For a local environment, copy <code>.env.example</code> to <code>.env</code>, replace local password placeholders with unique values, run <code>make dev-certs</code>, and start the stack with <code>make up</code>. Compose applies migrations before the API starts. The development override exposes PostgreSQL only on <code>127.0.0.1:5433</code>.

### Before opening a pull request

~~~sh
make check
make frontend-check
make nginx-check
make validate-specs
make architecture
make security
~~~

Run the narrowest relevant checks while developing, then run the complete set before requesting review. <code>make check</code> already includes lint/format, tests, architecture, contract, security and frontend type checks; repeated commands above are shown separately for clarity where they have dedicated workflows.

For frontend changes, run <code>make frontend-check</code> and <code>make frontend-build</code>. Commit the generated <code>frontend/public/assets/app.js</code> together with its TypeScript source. CI installs locked npm dependencies before running the project checks.

After changing routes or schemas, run <code>make openapi</code>, commit the regenerated <code>openapi.yaml</code>, and validate with <code>make validate-specs</code>. <code>asyncapi.yaml</code> documents the current absence of messaging channels; update it only when asynchronous interfaces are introduced.

### Engineering expectations

Keep changes focused, inspect the relevant implementation and tests first, and preserve unrelated work. Add or update tests and documentation with behaviour changes. Public Python modules, classes and functions should have docstrings describing contracts, errors and important constraints, not merely repeating symbol names. Cover CRUD changes at both service and HTTP levels.

Never commit .env files, tokens, private keys, certificates, production data or real credentials. Use placeholders in examples. Review <code>.secrets.baseline</code> changes carefully; never baseline real credentials. When dependencies change, regenerate <code>uv.lock</code> or <code>frontend/package-lock.json</code> and run the appropriate checks. Pin third-party GitHub Actions to full commit SHAs.

Performance tests and provisioning are local-only and require a disposable database whose name ends in <code>_test</code>. Never target production, third-party systems or shared environments. See [performance safety](docs/performance.md).

Authentication/RBAC changes must preserve deny-by-default behaviour, last-active-administrator protection, password reauthentication for role changes, session revocation and non-enumerating login failures. Read [security architecture](docs/security.md) and follow the [security-critical instructions](.github/instructions/security.instructions.md).

### Documentation and ownership

Public Markdown documentation follows the [documentation and translation standard](docs/documentation-standard.md): English first, Russian second, with matching meaning and scope. Update both language sections in the same pull request. Check internal links, anchors, images and status labels.

By submitting a contribution, you confirm that you have the right to provide it and agree that it may be distributed under the repository [LICENSE](LICENSE). Respect [authorship and attribution](AUTHORS.md) and the [Code of Conduct](CODE_OF_CONDUCT.md). Pull requests require review according to CODEOWNERS.

### Architecture references

- [Architecture and module boundaries](docs/architecture.md)
- [API and generated OpenAPI contract](docs/api.md)
- [Security architecture and operations](docs/security.md)
- [Documentation index](docs/index.md)

---

<a id="russian"></a>
## Русский

Спасибо за интерес к проекту и желание внести вклад. Репозиторий представляет собой FastAPI-сервис профилей для контролируемого администраторского использования. Перед изменением границ продукта изучите [обзор](docs/product-overview.md) и [архитектуру](docs/architecture.md).

### Окружение разработки

Используйте Python 3.14 и [uv](https://docs.astral.sh/uv/) либо откройте репозиторий в Dev Container.

~~~sh
uv sync --locked --all-groups
make frontend-install
make frontend-build
uv run pre-commit install -c .pre-commit-config.yaml
~~~

Для локального окружения скопируйте <code>.env.example</code> в <code>.env</code>, замените placeholders паролей уникальными значениями, выполните <code>make dev-certs</code> и запустите стек командой <code>make up</code>. Compose применяет миграции до запуска API. Development override публикует PostgreSQL только на <code>127.0.0.1:5433</code>.

### Перед отправкой pull request

~~~sh
make check
make frontend-check
make nginx-check
make validate-specs
make architecture
make security
~~~

Во время разработки запускайте минимальный набор релевантных проверок, а перед запросом ревью — полный комплект. <code>make check</code> уже включает lint/format, тесты, architecture, contract, security и frontend type checks; остальные команды приведены отдельно для ясности их собственных сценариев.

При изменениях frontend выполните <code>make frontend-check</code> и <code>make frontend-build</code>. Вместе с TypeScript-исходниками коммитьте сгенерированный <code>frontend/public/assets/app.js</code>. CI устанавливает frontend-зависимости по lockfile до запуска проверок.

После изменения маршрутов или схем выполните <code>make openapi</code>, закоммитьте обновлённый <code>openapi.yaml</code> и запустите <code>make validate-specs</code>. <code>asyncapi.yaml</code> фиксирует отсутствие messaging channels; меняйте его только при появлении асинхронных интерфейсов.

### Инженерные ожидания

Держите изменения сфокусированными, сначала изучайте относящиеся к задаче исходники и тесты, не затрагивайте посторонние изменения. Вместе с изменением поведения обновляйте тесты и документацию. Docstrings публичных Python-модулей, классов и функций должны описывать контракт, ошибки и важные ограничения, а не повторять имя символа. CRUD-изменения проверяйте на уровнях service и HTTP.

Не коммитьте .env, токены, private keys, сертификаты, production-данные или реальные credentials. В примерах используйте placeholders. Внимательно проверяйте изменения <code>.secrets.baseline</code>; никогда не добавляйте реальные credentials в baseline. При изменении зависимостей обновляйте <code>uv.lock</code> или <code>frontend/package-lock.json</code> и выполняйте соответствующие проверки. Сторонние GitHub Actions фиксируйте полными commit SHA.

Нагрузочные тесты и provisioning разрешены только локально и требуют отдельную БД, имя которой заканчивается на <code>_test</code>. Не направляйте их на production, сторонние системы или общее окружение. См. [ограничения performance-тестирования](docs/performance.md).

Изменения authentication/RBAC должны сохранять deny-by-default, защиту последнего активного администратора, повторную проверку пароля при изменении ролей, отзыв сессий и защиту от перечисления аккаунтов через login errors. Перед такой работой изучите [архитектуру безопасности](docs/security.md) и следуйте [инструкциям для security-critical изменений](.github/instructions/security.instructions.md).

### Документация и авторство

Публичная Markdown-документация подчиняется [стандарту документации и перевода](docs/documentation-standard.md): сначала английская версия, затем русская, с одинаковым смыслом и scope. Обновляйте обе версии в одном pull request. Проверяйте внутренние ссылки, якоря, изображения и метки статуса.

Отправляя вклад, вы подтверждаете право его предоставить и соглашаетесь с возможностью распространения по [LICENSE](LICENSE) репозитория. Соблюдайте [правила авторства и атрибуции](AUTHORS.md) и [правила сообщества](CODE_OF_CONDUCT.md). Pull request требует ревью в соответствии с CODEOWNERS.

### Архитектурные документы

- [Архитектура и границы модулей](docs/architecture.md)
- [API и сгенерированный OpenAPI-контракт](docs/api.md)
- [Архитектура безопасности и эксплуатация](docs/security.md)
- [Индекс документации](docs/index.md)
