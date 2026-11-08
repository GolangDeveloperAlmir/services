# Guidance for AI agents

> **Language / Язык:** [English](#english) · [Русский](#russian)

<a id="english"></a>
## English

This file is shared context for coding agents. Checked-in code, tests and generated contracts are the source of truth. A roadmap item is not an implemented feature or a delivery commitment.

### Project boundaries

- This is a FastAPI profile service for controlled administrator use, not a public identity platform. Every <code>/users</code> endpoint requires an active administrator. Do not silently add end-user access, tenant isolation, MFA, SSO/OIDC or password recovery.
- Profile creation does not create credentials or grant roles. The only built-in role is <code>admin</code>.
- <code>app.main</code> composes the application; <code>app.auth</code> owns local credentials, sessions and authorization; <code>app.users</code> owns profile API/business rules; <code>app.db</code> owns persistence; <code>app.core</code> owns shared settings, logging and telemetry. Preserve [architecture rules](docs/architecture.md).
- PostgreSQL is authoritative for account and role state. Redis stores ephemeral sessions and rate counters; Redis failure must never grant access or trigger an unauthenticated fallback.
- The web console keeps its bearer token in tab memory. Browser-local media is not uploaded; there is no upload endpoint or processing worker. Keep the curated catalog read-only and admin-only.
- Compose, self-signed certificates and example credentials are for local development only.

### Security and safety

- Read [security architecture](docs/security.md) before changing authentication, authorization, settings, database models/migrations, proxy/TLS, deployment, media access or security tests. Follow [security-critical instructions](.github/instructions/security.instructions.md).
- Preserve deny-by-default authorization, the last-active-administrator invariant, password reauthentication for role changes, session revocation and generic login failures. Add regression tests.
- Never print, commit, copy into patches or expose .env contents, tokens, private keys, certificates, production data or credentials. Use placeholders; do not inspect local secret files unless explicitly required.
- Never run commands, tests, migrations, provisioning, scans or load against production, third-party or unapproved systems. Performance tests/provisioning are local-only and require a disposable _test database. See [performance safety](docs/performance.md).
- Do not weaken controls or trust boundaries to make a test pass. Do not delete data, volumes, certificates or user changes without explicit approval.
- Verify media rights before adding assets. Preserve third-party notices and repository attribution under [LICENSE](LICENSE).

### Implementation and verification

- Inspect the implementation and tests before changing behaviour; preserve unrelated worktree changes. Use existing patterns, typed interfaces and explicit error handling. Do not swallow errors or return success-shaped fallbacks.
- Add/update tests and docs with behaviour changes. Public documentation must follow [the bilingual standard](docs/documentation-standard.md): English first, Russian second, synchronized in meaning.
- For API/schema changes, regenerate <code>openapi.yaml</code> with <code>make openapi</code> and validate with <code>make validate-specs</code>. For frontend source changes, run <code>make frontend-check</code> and <code>make frontend-build</code>, and commit generated <code>frontend/public/assets/app.js</code>.
- Use Python 3.14 and <code>uv</code>. Relevant commands include <code>make test</code>, <code>make lint</code>, <code>make architecture</code>, <code>make validate-specs</code>, <code>make security</code> and <code>make check</code>. Frontend checks require <code>make frontend-install</code>. See [CONTRIBUTING.md](CONTRIBUTING.md).
- If dependency manifests change, regenerate the relevant lockfile (<code>uv.lock</code> or <code>frontend/package-lock.json</code>).
- Before finishing, review the diff for unrelated edits, generated files, secrets, broken links and whitespace errors. Report checks run and not run; never claim unrun checks passed.

### Further context

[README](README.md) · [Documentation map](docs/index.md) · [Contributing](CONTRIBUTING.md) · [Security reporting](SECURITY.md) · [Code of Conduct](CODE_OF_CONDUCT.md) · [Support](SUPPORT.md)

---

<a id="russian"></a>
## Русский

Этот файл содержит общий контекст для coding agents. Источником истины являются коммитнутый код, тесты и сгенерированные контракты. Пункт roadmap не означает, что функция уже реализована или обещана к выпуску.

### Границы проекта

- Это FastAPI-сервис профилей для контролируемого администраторского использования, а не публичная Identity-платформа. Каждый <code>/users</code> endpoint требует активного администратора. Не добавляйте неявно доступ конечным пользователям, tenant isolation, MFA, SSO/OIDC или восстановление пароля.
- Создание профиля не создаёт credentials и не назначает роль. Единственная встроенная роль — <code>admin</code>.
- <code>app.main</code> собирает приложение; <code>app.auth</code> отвечает за локальные credentials, сессии и авторизацию; <code>app.users</code> — за API профилей и бизнес-правила; <code>app.db</code> — за хранение; <code>app.core</code> — за общие настройки, logging и telemetry. Соблюдайте [архитектурные правила](docs/architecture.md).
- PostgreSQL является источником истины для состояния аккаунтов и ролей. Redis хранит временные сессии и rate counters; отказ Redis никогда не должен открывать доступ или создавать unauthenticated fallback.
- Веб-панель хранит bearer-токен только в памяти вкладки. Browser-local media не загружается; endpoint загрузки и processing worker отсутствуют. Сохраняйте read-only и admin-only модель каталога.
- Compose, self-signed сертификаты и примерные credentials предназначены только для локальной разработки.

### Безопасность и ограничения

- Перед изменением authentication, authorization, settings, моделей/миграций БД, proxy/TLS, deployment, media access или security tests прочитайте [архитектуру безопасности](docs/security.md). Следуйте [инструкциям для security-critical изменений](.github/instructions/security.instructions.md).
- Сохраняйте deny-by-default, инвариант последнего активного администратора, повторную проверку пароля при изменении ролей, отзыв сессий и унифицированные login errors. Добавляйте регрессионные тесты.
- Никогда не выводите, не коммитьте и не раскрывайте содержимое .env, токены, private keys, сертификаты, production-данные и credentials. Используйте placeholders; не изучайте локальные секретные файлы без явной необходимости.
- Не запускайте команды, тесты, миграции, provisioning, scans или нагрузку против production, сторонних или неутверждённых систем. Performance tests/provisioning допустимы только локально и на отдельной БД _test. См. [ограничения performance-тестирования](docs/performance.md).
- Не ослабляйте controls и trust boundaries ради прохождения теста. Не удаляйте данные, volumes, сертификаты или пользовательские изменения без явного согласия.
- Перед добавлением media проверяйте права использования. Сохраняйте сторонние license notices и требования атрибуции проекта из [LICENSE](LICENSE).

### Разработка и проверки

- Перед изменением поведения изучите реализацию и тесты; сохраняйте посторонние изменения. Используйте существующие паттерны, типизированные интерфейсы и явную обработку ошибок. Не скрывайте ошибки и не возвращайте фиктивный успех.
- Вместе с изменением поведения обновляйте тесты и документацию. Публичная документация следует [двуязычному стандарту](docs/documentation-standard.md): английский первым, русский вторым, с одинаковым смыслом.
- При изменении API/schema пересоздайте <code>openapi.yaml</code> через <code>make openapi</code> и проверьте <code>make validate-specs</code>. При изменении frontend выполните <code>make frontend-check</code> и <code>make frontend-build</code>, затем закоммитьте <code>frontend/public/assets/app.js</code>.
- Используйте Python 3.14 и <code>uv</code>. Релевантные команды: <code>make test</code>, <code>make lint</code>, <code>make architecture</code>, <code>make validate-specs</code>, <code>make security</code>, <code>make check</code>. Для frontend-проверок требуется <code>make frontend-install</code>. Подробности — в [CONTRIBUTING.md](CONTRIBUTING.md).
- При изменении dependency manifests обновляйте соответствующий lockfile (<code>uv.lock</code> или <code>frontend/package-lock.json</code>).
- Перед завершением проверьте diff на посторонние изменения, generated files, secrets, сломанные ссылки и whitespace. Укажите выполненные и невыполненные проверки; не утверждайте, что непроведённые проверки прошли.

### Дополнительный контекст

[README](README.md) · [Карта документации](docs/index.md) · [Участие в разработке](CONTRIBUTING.md) · [Сообщение об уязвимости](SECURITY.md) · [Правила сообщества](CODE_OF_CONDUCT.md) · [Поддержка](SUPPORT.md)
