# Documentation and translation standard

> **Language / Язык:** [English](#english) · [Русский](#russian)
> **Applies to:** README, Markdown guides, architecture records, runbooks, API explanations and roadmap specifications.

<a id="english"></a>
## English

### 1. Language order and navigation

Every public Markdown document must use one canonical file with two complete language sections in this order: **English first, Russian second**. The language selector appears near the top, immediately after the title or hero: [English](#english) · [Русский](#russian).

Use explicit anchors when generated heading slugs may be ambiguous:

~~~html
<a id="english"></a>
## English

...

<a id="russian"></a>
## Русский

...
~~~

Avoid separate translated copies unless a publishing system explicitly requires them. One canonical file reduces translation drift and keeps the choice of language visible.

### 2. Required information architecture

Use the sections that fit the page, while keeping the reader's route predictable:

1. **Purpose:** what question the page answers and who should read it.
2. **Status:** implemented, partial, planned, deprecated or unverified.
3. **Context:** assumptions, scope and non-goals.
4. **Main content:** steps, architecture, contract or decision.
5. **Examples:** executable snippets with prerequisites and safe defaults.
6. **Failure modes and risks:** what can fail and how the system behaves.
7. **Verification:** tests, commands or evidence supporting the claims.
8. **Related pages:** a small set of useful next links.

A changelog remains chronological; a security policy prioritises disclosure instructions; an API guide prioritises contract and authorization.

### 3. Truth and implementation status

| Label | Rule |
| --- | --- |
| **Implemented** | Present in checked-in runtime code; link to the relevant source or contract. |
| **Partial** | Part of the workflow exists; list missing pieces. |
| **Planned** | Proposal only; never describe it in present tense as an available feature. |
| **Deprecated** | Retained for compatibility/history; name the replacement or removal condition. |
| **Unverified** | Not checked against current source, tests or environment. |

A roadmap, architecture proposal, mock UI, empty directory or badge is not evidence that a feature is implemented. Prefer “optional trace export is configured” over “the platform has full observability” when metrics, dashboards and alerting are absent.

### 4. Writing and formatting

- Write for readers who have not opened the source code. Expand acronyms on first use.
- Prefer concrete nouns and active verbs. Name the actor, operation, resource and result.
- Keep paragraphs focused. Use tables for comparisons, not as a replacement for explanations.
- Use ordered lists for procedures and unordered lists for independent facts.
- Label code fences: <code>sh</code>, <code>json</code>, <code>yaml</code>, <code>mermaid</code>.
- Every command must state where it runs, what it changes and whether it is safe outside a disposable local environment.
- Use relative repository links and verify target paths and fragments before merge.
- Keep terminology consistent: administrator, profile, credential, session, tenant, readiness and liveness.
- Avoid decorative badge spam, fake ratings, unverified benchmark claims and screenshots implying unavailable functionality.

### 5. Translation policy

English is the reference language for public-document structure and terminology. Russian must preserve the same technical meaning, constraints, examples, status and warnings.

Translation must not soften a security requirement, change a limit or HTTP status, turn planned work into an implemented feature, replace exact technology names with vague synonyms, or omit caveats.

Keep identifiers, endpoint paths, environment variables, file paths, protocol names and product/tool names unchanged; translate the explanation around them. If a term has no stable Russian equivalent, retain the English term and define it in the [glossary](glossary.md).

When one language changes, update the other in the same pull request. A page is incomplete when its language sections materially disagree.

### 6. Diagrams and images

Use Mermaid for source-controlled diagrams when GitHub rendering is sufficient: flowcharts for request paths, sequence diagrams for interactions and ER diagrams for data relationships. Add a short text explanation; the source should remain understandable without rendered graphics.

Use SVG or PNG assets under <code>docs/assets/</code> when consistent visual styling or README embedding is useful. Every image needs descriptive alt text. Keep assets local, lightweight, attributable and licensed for repository distribution. Do not present an illustration as a live screenshot.

### 7. Tables, links and references

Use meaningful table headers and avoid paragraphs inside table cells. Use descriptive link text rather than “click here”. Cite exact sources for version requirements, generated contracts and external standards. Prefer primary vendor documentation. Add an “as of” date to volatile inventories and metrics.

### 8. Metrics and claims

Every number must be one of:
- a static value verified in code/configuration;
- a measurement with workload, environment, date and method;
- an explicit target approved by the project owner.

Never mix these categories. Mark repository inventory as a snapshot. A benchmark must state hardware, commit, configuration, concurrency, duration, error rate and percentiles. If no measurement exists, write **not measured** rather than estimating.

### 9. Review checklist

- [ ] English appears before Russian.
- [ ] Language links point to working anchors.
- [ ] Both language sections agree on features, limits and warnings.
- [ ] Implemented and planned behaviour are separated.
- [ ] Commands are safe and copyable; secrets are placeholders.
- [ ] Diagrams/images have alt text and correct relative paths.
- [ ] Internal links resolve.
- [ ] Metrics have provenance or are marked not measured.
- [ ] Related pages and source references are current.

---

<a id="russian"></a>
## Русский

### 1. Порядок языков и навигация

Каждый публичный Markdown-документ должен иметь один канонический файл с двумя полноценными языковыми версиями в строгом порядке: **сначала английский, затем русский**. Селектор размещается сразу после заголовка или hero-блока: [English](#english) · [Русский](#russian).

Используйте явные якоря, если автоматически созданные GitHub fragments могут быть неоднозначными:

~~~html
<a id="english"></a>
## English

...

<a id="russian"></a>
## Русский

...
~~~

Не создавайте отдельные копии перевода, если этого явно не требует система публикации. Один канонический файл уменьшает расхождение переводов и сохраняет выбор языка на виду.

### 2. Информационная архитектура документа

Используйте подходящие разделы, сохраняя предсказуемый маршрут читателя:

1. **Назначение:** на какой вопрос отвечает страница и кому она нужна.
2. **Статус:** реализовано, частично, запланировано, устарело или не проверено.
3. **Контекст:** предположения, scope и не-цели.
4. **Основная часть:** шаги, архитектура, контракт или решение.
5. **Примеры:** исполняемые фрагменты с предварительными условиями и безопасными значениями.
6. **Отказы и риски:** что может сломаться и как поведёт себя система.
7. **Проверка:** тесты, команды или доказательства утверждений.
8. **Связанные страницы:** небольшой набор следующих полезных ссылок.

Changelog остаётся хронологическим; security policy ставит на первое место порядок раскрытия уязвимостей; API guide делает акцент на контракте и авторизации.

### 3. Достоверность и статус реализации

| Метка | Правило |
| --- | --- |
| **Implemented** | Присутствует в runtime-коде; добавьте ссылку на исходник или контракт. |
| **Partial** | Реализована часть workflow; перечислите недостающие компоненты. |
| **Planned** | Только предложение; не описывайте его в настоящем времени как доступную функцию. |
| **Deprecated** | Сохранено для совместимости или истории; укажите замену/условие удаления. |
| **Unverified** | Не проверено по актуальным исходникам, тестам или окружению. |

Roadmap, архитектурное предложение, макет интерфейса, пустой каталог или badge не доказывают реализацию функции. Предпочитайте точное «настроен опциональный экспорт traces» вместо «платформа обладает полной наблюдаемостью», если metrics, dashboards и alerting отсутствуют.

### 4. Текст и форматирование

- Пишите для читателя, который ещё не открывал исходный код. Раскрывайте сокращения при первом упоминании.
- Предпочитайте конкретные существительные и активные глаголы. Называйте участника, действие, ресурс и результат.
- Держите абзацы сфокусированными. Используйте таблицы для сравнений, а не вместо объяснений.
- Нумерованные списки применяйте для процедур, ненумерованные — для независимых фактов.
- Маркируйте code fences: <code>sh</code>, <code>json</code>, <code>yaml</code>, <code>mermaid</code>.
- Для команды указывайте место запуска, последствия и возможность использования вне одноразового локального окружения.
- Используйте относительные ссылки в репозитории и проверяйте пути/fragments перед merge.
- Сохраняйте единую терминологию: administrator, profile, credential, session, tenant, readiness и liveness.
- Не используйте декоративные россыпи badge, выдуманные рейтинги, неподтверждённые benchmark-значения и скриншоты отсутствующих функций.

### 5. Правила перевода

Английский является опорным языком структуры и терминологии публичной документации. Русская версия должна сохранять тот же технический смысл, ограничения, примеры, статус и предупреждения.

Нельзя смягчать требования безопасности, менять лимиты и HTTP status, превращать планы в реализованные функции, заменять точные названия технологий расплывчатыми синонимами или удалять оговорки.

Идентификаторы, endpoint paths, environment variables, file paths, названия протоколов и инструментов не переводятся; переводится пояснение вокруг них. Если устойчивого русского эквивалента нет, оставьте английский термин и определите его в [глоссарии](glossary.md).

При изменении одной языковой версии вторую нужно обновить в том же pull request. Документ неполон, если языковые версии существенно расходятся.

### 6. Диаграммы и изображения

Используйте Mermaid для диаграмм в исходниках, если возможностей GitHub достаточно: flowchart для пути запроса, sequence diagram для взаимодействий, ER diagram для связей данных. Добавляйте короткое текстовое объяснение; исходник должен быть понятен и без отрисовки.

SVG и PNG храните в <code>docs/assets/</code>, когда нужен единый визуальный стиль или вставка в README. Каждому изображению нужен описательный alt text. Материалы должны быть локальными, лёгкими, атрибутированными и разрешёнными к распространению. Не выдавайте иллюстрацию за живой скриншот.

### 7. Таблицы, ссылки и источники

У таблиц должны быть содержательные заголовки; избегайте больших абзацев в ячейках. Используйте описательные названия ссылок. Указывайте точные источники требований к версиям, сгенерированных контрактов и внешних стандартов. Предпочитайте первичную документацию производителя. Для изменяемой инвентаризации и метрик добавляйте дату среза.

### 8. Метрики и утверждения

Каждое число должно относиться к одной категории:
- статическое значение, проверенное в коде/конфигурации;
- измерение с workload, окружением, датой и методом;
- явная цель, утверждённая владельцем проекта.

Не смешивайте категории. Инвентаризацию репозитория помечайте как snapshot. Для benchmark указывайте оборудование, commit, настройки, concurrency, длительность, error rate и перцентили. При отсутствии измерения пишите **не измерено**, а не угадывайте.

### 9. Чек-лист ревью

- [ ] Английская версия расположена перед русской.
- [ ] Ссылки выбора языка ведут на рабочие якоря.
- [ ] Обе версии одинаково описывают функции, лимиты и предупреждения.
- [ ] Реализованное поведение отделено от будущего.
- [ ] Команды безопасны и копируемы; секреты заменены placeholder.
- [ ] У диаграмм/изображений есть alt text и правильные относительные пути.
- [ ] Внутренние ссылки разрешаются.
- [ ] Для метрик указано происхождение или написано «не измерено».
- [ ] Связанные страницы и ссылки на исходники актуальны.
