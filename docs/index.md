# Documentation hub

> **Language / Язык:** [English](#english) · [Русский](#russian)

<a id="english"></a>
## English

This index is the front door to the engineering handbook. Pages are ordered by reader intent rather than by file-system location. Each page should distinguish implemented behaviour from planned work.

![Documentation map](assets/documentation-map.svg)

### Choose a reading path

| Reader | Start with | Then continue with |
| --- | --- | --- |
| Evaluating the project | [Product overview](product-overview.md) | [Architecture](architecture.md), [technology decisions](technology-stack.md), [API](api.md) |
| Joining development | [README quick start](../README.md#english) | [Architecture](architecture.md), [API](api.md), [contribution guide](../CONTRIBUTING.md) |
| Reviewing security | [Security model](security.md) | [Data model](data-model.md), [observability](observability.md), [performance safety](performance.md) |
| Operating locally | [README quick start](../README.md#english) | [Security](security.md), [media catalog](media.md), [performance](performance.md) |
| Learning the vocabulary | [Glossary](glossary.md) | [Technology decisions](technology-stack.md), [architecture](architecture.md) |
| Planning future work | [Roadmap](roadmap.md) | [Detailed initiatives](roadmap/), [documentation standard](documentation-standard.md) |

### Product and design

- [Product overview](product-overview.md): value proposition, audience, capabilities and non-goals.
- [Architecture](architecture.md): runtime components, trust boundaries, request path and module rules.
- [Data model](data-model.md): implemented PostgreSQL entities and relationship constraints.
- [HTTP API](api.md): routes, request semantics, authorization and errors.

### Engineering and operations

- [Technology stack and decisions](technology-stack.md): selected tools, rationale, alternatives, benefits and risks.
- [Security architecture and operations](security.md): authentication, sessions, transport, secrets and residual risks.
- [Observability](observability.md): JSON logs, optional OpenTelemetry tracing and what is not instrumented.
- [Performance and load testing](performance.md): safe test boundaries, Locust scenarios and interpretation.
- [Metrics and project facts](metrics.md): repository inventory, metric definitions and baseline status.
- [Media catalog](media.md): curated assets, supported formats and upload limitations.

### Governance and contribution

- [Documentation standard](documentation-standard.md): English-first bilingual policy, structure, translation and diagrams.
- [Contributing](../CONTRIBUTING.md): environment, checks, pull requests and ownership.
- [Authorship and attribution](../AUTHORS.md): original project materials and reuse terms.
- [Security reporting](../SECURITY.md): responsible vulnerability disclosure.
- [Code of Conduct](../CODE_OF_CONDUCT.md): participation expectations.
- [Support](../SUPPORT.md): questions, defect reports and feature proposals.
- [License](../LICENSE): AOAL 1.0 and third-party license boundaries.
- [Changelog](../CHANGELOG.md): repository change history.
- [AI-agent guidance](../AGENTS.md): repository-specific implementation constraints.

### Roadmap

The roadmap contains proposals and decision records, not delivery promises:

1. [Platform foundation](roadmap/01-platform-foundation.md)
2. [Multi-tenancy and RBAC](roadmap/02-multi-tenancy-rbac.md)
3. [Identity lifecycle](roadmap/03-identity-lifecycle.md)
4. [Reliability and scale](roadmap/04-reliability-scale.md)
5. [Media pipeline](roadmap/05-media-pipeline.md)

### Documentation status vocabulary

| Label | Meaning |
| --- | --- |
| **Implemented** | The behaviour exists in the checked-in code and is covered by relevant checks. |
| **Partial** | Some of the described workflow exists; missing pieces are named explicitly. |
| **Planned** | A proposal only. It is not available at runtime. |
| **Deprecated** | Kept for migration or historical context; do not build new work on it. |
| **Unverified** | Not checked against the current implementation or environment. |

The absence of a label does not turn a roadmap item into a shipped feature. When in doubt, check source code, tests and the generated OpenAPI contract.

---

<a id="russian"></a>
## Русский

Этот индекс служит главной точкой входа в инженерную документацию. Страницы сгруппированы по задачам читателя, а не по расположению файлов. Каждый документ обязан отделять действующее поведение от планов.

### Маршрут чтения

| Читатель | Начать с | Затем |
| --- | --- | --- |
| Оценивает проект | [Обзор продукта](product-overview.md) | [Архитектура](architecture.md), [выбор технологий](technology-stack.md), [API](api.md) |
| Присоединяется к разработке | [Быстрый старт README](../README.md#russian) | [Архитектура](architecture.md), [API](api.md), [руководство участника](../CONTRIBUTING.md) |
| Проверяет безопасность | [Модель безопасности](security.md) | [Модель данных](data-model.md), [наблюдаемость](observability.md), [безопасность нагрузочных тестов](performance.md) |
| Запускает локально | [Быстрый старт README](../README.md#russian) | [Безопасность](security.md), [каталог медиа](media.md), [производительность](performance.md) |
| Разбирается в терминах | [Глоссарий](glossary.md) | [Выбор технологий](technology-stack.md), [архитектура](architecture.md) |
| Планирует развитие | [Roadmap](roadmap.md) | [Подробные инициативы](roadmap/), [стандарт документации](documentation-standard.md) |

### Продукт и проектирование

- [Обзор продукта](product-overview.md): ценность, аудитория, возможности и границы.
- [Архитектура](architecture.md): runtime-компоненты, границы доверия, путь запроса и правила модулей.
- [Модель данных](data-model.md): реализованные сущности PostgreSQL и ограничения связей.
- [HTTP API](api.md): маршруты, семантика запросов, авторизация и ошибки.

### Разработка и эксплуатация

- [Стек технологий и решения](technology-stack.md): инструменты, причины выбора, альтернативы, преимущества и риски.
- [Архитектура безопасности](security.md): аутентификация, сессии, транспорт, секреты и остаточные риски.
- [Наблюдаемость](observability.md): JSON-логи, опциональная OpenTelemetry-трассировка и отсутствующие инструменты.
- [Производительность и нагрузочные тесты](performance.md): безопасные ограничения, Locust-сценарии и интерпретация.
- [Метрики и факты проекта](metrics.md): инвентаризация репозитория, определения метрик и состояние baseline.
- [Каталог медиа](media.md): подготовленные оператором файлы, форматы и ограничения загрузки.

### Правила и участие

- [Стандарт документации](documentation-standard.md): сначала английский, затем русский, структура, перевод и схемы.
- [Участие в разработке](../CONTRIBUTING.md): окружение, проверки, pull request и авторство.
- [Авторство и атрибуция](../AUTHORS.md): оригинальные материалы проекта и условия использования.
- [Сообщение об уязвимости](../SECURITY.md): ответственное раскрытие.
- [Правила сообщества](../CODE_OF_CONDUCT.md): нормы участия.
- [Поддержка](../SUPPORT.md): вопросы, сообщения об ошибках и предложения.
- [Лицензия](../LICENSE): AOAL 1.0 и границы сторонних лицензий.
- [Журнал изменений](../CHANGELOG.md): история изменений репозитория.
- [Инструкции для AI-агентов](../AGENTS.md): проектные ограничения для автоматизированных помощников.

### План развития

Roadmap содержит предложения и точки принятия решений, а не обещания сроков:

1. [Платформенная основа](roadmap/01-platform-foundation.md)
2. [Мультитенантность и RBAC](roadmap/02-multi-tenancy-rbac.md)
3. [Жизненный цикл identity](roadmap/03-identity-lifecycle.md)
4. [Надёжность и масштабирование](roadmap/04-reliability-scale.md)
5. [Конвейер медиа](roadmap/05-media-pipeline.md)

### Термины статуса документации

| Метка | Значение |
| --- | --- |
| **Implemented** | Поведение присутствует в коде и покрыто соответствующими проверками. |
| **Partial** | Реализована только часть сценария; недостающие части названы явно. |
| **Planned** | Только предложение. В runtime функция недоступна. |
| **Deprecated** | Сохранено для истории или перехода; не использовать как основу новой разработки. |
| **Unverified** | Не сверено с текущей реализацией или окружением. |

Отсутствие метки не превращает пункт roadmap в готовую функцию. При сомнениях проверяйте исходный код, тесты и сгенерированный OpenAPI-контракт.
